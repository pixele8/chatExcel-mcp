#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强的Excel处理助手模块
提供智能编码检测、缓存机制和数据完整性保障功能
"""

import os
import hashlib
import json
import time
from typing import Dict, Any, List, Optional, Tuple, Union
import pandas as pd
import openpyxl
import chardet
from pathlib import Path


class EncodingCache:
    """编码检测缓存管理器"""
    
    def __init__(self, cache_dir: str = ".encoding_cache", max_cache_size_mb: int = 10, config_file: str = None):
        # 加载配置
        self.config = self._load_config(config_file)
        
        # 应用配置
        self.cache_dir = Path(self.config.get('paths', {}).get('cache_directory', cache_dir))
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_file = self.cache_dir / "encoding_cache.json"
        self.backup_file = self.cache_dir / "encoding_cache_backup.json"
        
        # 缓存设置
        cache_settings = self.config.get('cache_settings', {})
        self.max_cache_size_mb = cache_settings.get('max_cache_size_mb', max_cache_size_mb)
        self.cache_expiry_days = cache_settings.get('cache_expiry_days', 7)
        self.auto_cleanup_interval = cache_settings.get('auto_cleanup_interval', 10)
        self.enable_auto_backup = cache_settings.get('enable_auto_backup', True)
        
        # 监控设置
        monitoring = self.config.get('monitoring', {})
        self.enable_size_monitoring = monitoring.get('enable_size_monitoring', True)
        self.size_warning_threshold_mb = monitoring.get('size_warning_threshold_mb', 8)
        self.enable_performance_logging = monitoring.get('enable_performance_logging', False)
        
        # 维护设置
        maintenance = self.config.get('maintenance', {})
        self.auto_reduce_cache_percentage = maintenance.get('auto_reduce_cache_percentage', 50)
        self.enable_startup_cleanup = maintenance.get('enable_startup_cleanup', True)
        
        self.cache = self._load_cache()
        
        # 启动时执行清理和监控（如果启用）
        if self.enable_startup_cleanup:
            self._cleanup_expired_cache()
        if self.enable_size_monitoring:
            self._monitor_cache_size()
    
    def _load_config(self, config_file: str = None) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            'cache_settings': {
                'max_cache_size_mb': 10,
                'cache_expiry_days': 7,
                'auto_cleanup_interval': 10,
                'enable_auto_backup': True
            },
            'monitoring': {
                'enable_size_monitoring': True,
                'size_warning_threshold_mb': 8,
                'enable_performance_logging': False
            },
            'maintenance': {
                'auto_reduce_cache_percentage': 50,
                'enable_startup_cleanup': True
            },
            'paths': {
                'cache_directory': '.encoding_cache'
            }
        }
        
        if config_file:
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                # 合并配置
                self._merge_config(default_config, user_config)
            except Exception as e:
                print(f"加载配置文件失败，使用默认配置: {e}")
        
        return default_config
    
    def _merge_config(self, default: Dict, user: Dict):
        """递归合并配置"""
        for key, value in user.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                self._merge_config(default[key], value)
            else:
                default[key] = value
    
    def _load_cache(self) -> Dict[str, Any]:
        """加载缓存文件"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    def _save_cache(self):
        """保存缓存文件"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def _get_file_hash(self, file_path: str) -> str:
        """获取文件哈希值"""
        try:
            stat = os.stat(file_path)
            # 使用文件路径、大小和修改时间生成哈希
            content = f"{file_path}_{stat.st_size}_{stat.st_mtime}"
            return hashlib.md5(content.encode()).hexdigest()
        except Exception:
            return hashlib.md5(file_path.encode()).hexdigest()
    
    def get(self, file_path: str) -> Optional[str]:
        """获取缓存的编码信息"""
        file_hash = self._get_file_hash(file_path)
        cache_entry = self.cache.get(file_hash)
        
        if cache_entry:
            # 检查缓存是否过期（使用配置的过期天数）
            expiry_seconds = self.cache_expiry_days * 24 * 3600
            if time.time() - cache_entry.get('timestamp', 0) < expiry_seconds:
                return cache_entry.get('encoding')
        
        return None
    
    def set(self, file_path: str, encoding: str):
        """设置编码缓存"""
        file_hash = self._get_file_hash(file_path)
        self.cache[file_hash] = {
            'encoding': encoding,
            'timestamp': time.time(),
            'file_path': file_path
        }
        self._save_cache()
        # 定期清理和监控（使用配置的间隔）
        if len(self.cache) % self.auto_cleanup_interval == 0:
            if self.enable_startup_cleanup:
                self._cleanup_expired_cache()
            if self.enable_size_monitoring:
                self._monitor_cache_size()
        # 自动备份（如果启用）
        if self.enable_auto_backup and len(self.cache) % (self.auto_cleanup_interval * 2) == 0:
            self.create_backup()
    
    def _cleanup_expired_cache(self):
        """清理过期的缓存条目"""
        try:
            current_time = time.time()
            expired_keys = []
            expiry_seconds = self.cache_expiry_days * 24 * 3600
            
            for key, entry in self.cache.items():
                # 检查是否过期（使用配置的过期天数）
                if current_time - entry.get('timestamp', 0) > expiry_seconds:
                    expired_keys.append(key)
            
            # 删除过期条目
            for key in expired_keys:
                del self.cache[key]
            
            if expired_keys:
                self._save_cache()
                if self.enable_performance_logging:
                    print(f"编码缓存清理完成，删除了 {len(expired_keys)} 个过期条目")
                
        except Exception as e:
            print(f"缓存清理失败: {e}")
    
    def _monitor_cache_size(self):
        """监控缓存文件大小"""
        try:
            if self.cache_file.exists():
                file_size_mb = self.cache_file.stat().st_size / (1024 * 1024)
                
                if file_size_mb > self.max_cache_size_mb:
                    if self.enable_performance_logging:
                        print(f"警告：编码缓存文件大小 {file_size_mb:.2f}MB 超过限制 {self.max_cache_size_mb}MB")
                    # 如果超过限制，删除最旧的50%条目
                    self._reduce_cache_size()
                elif file_size_mb > self.size_warning_threshold_mb:
                    if self.enable_performance_logging:
                        print(f"警告：缓存文件大小 ({file_size_mb:.2f} MB) 接近限制 ({self.max_cache_size_mb} MB)")
                else:
                    if self.enable_performance_logging:
                        print(f"编码缓存文件大小: {file_size_mb:.2f}MB (限制: {self.max_cache_size_mb}MB)")
                    
        except Exception as e:
            if self.enable_performance_logging:
                print(f"缓存大小监控失败: {e}")
    
    def _reduce_cache_size(self):
        """减少缓存大小，删除最旧的条目"""
        try:
            # 按时间戳排序，删除最旧的指定百分比
            sorted_items = sorted(self.cache.items(), 
                                key=lambda x: x[1].get('timestamp', 0))
            
            items_to_remove = int(len(sorted_items) * self.auto_reduce_cache_percentage / 100)
            
            for i in range(items_to_remove):
                key = sorted_items[i][0]
                del self.cache[key]
            
            self._save_cache()
            if self.enable_performance_logging:
                print(f"缓存大小优化完成，删除了 {items_to_remove} 个最旧条目")
            
        except Exception as e:
            if self.enable_performance_logging:
                print(f"缓存大小优化失败: {e}")
    
    def create_backup(self):
        """创建缓存备份"""
        try:
            if self.cache_file.exists():
                import shutil
                shutil.copy2(self.cache_file, self.backup_file)
                if self.enable_performance_logging:
                    print(f"缓存备份已创建: {self.backup_file}")
                return True
            else:
                if self.enable_performance_logging:
                    print("缓存文件不存在，无法创建备份")
        except Exception as e:
            if self.enable_performance_logging:
                print(f"创建备份时出错: {e}")
        return False
    
    def restore_from_backup(self):
        """从备份恢复缓存"""
        try:
            if self.backup_file.exists():
                import shutil
                shutil.copy2(self.backup_file, self.cache_file)
                self.cache = self._load_cache()
                if self.enable_performance_logging:
                    print(f"缓存已从备份恢复: {self.backup_file}")
                return True
            else:
                if self.enable_performance_logging:
                    print("备份文件不存在，无法恢复")
                return False
        except Exception as e:
            if self.enable_performance_logging:
                print(f"从备份恢复时出错: {e}")
            return False
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        try:
            stats = {
                'total_entries': len(self.cache),
                'file_size_mb': 0,
                'oldest_entry': None,
                'newest_entry': None,
                'expired_count': 0
            }
            
            if self.cache_file.exists():
                stats['file_size_mb'] = self.cache_file.stat().st_size / (1024 * 1024)
            
            if self.cache:
                timestamps = [entry.get('timestamp', 0) for entry in self.cache.values()]
                stats['oldest_entry'] = min(timestamps)
                stats['newest_entry'] = max(timestamps)
                
                # 计算过期条目数量
                current_time = time.time()
                stats['expired_count'] = sum(1 for entry in self.cache.values() 
                                           if current_time - entry.get('timestamp', 0) > 7 * 24 * 3600)
            
            return stats
        except Exception as e:
            return {'error': str(e)}


# 创建全局编码缓存实例（使用配置文件）
_encoding_cache = EncodingCache(config_file="cache_config.json")


def detect_file_encoding(file_path: str, use_cache: bool = True) -> Dict[str, Any]:
    """智能检测文件编码
    
    Args:
        file_path: 文件路径
        use_cache: 是否使用缓存
        
    Returns:
        dict: 包含编码信息和检测详情
    """
    result = {
        'encoding': 'utf-8',
        'confidence': 0.0,
        'method': 'default',
        'alternatives': [],
        'cached': False
    }
    
    try:
        # 检查缓存
        if use_cache:
            cached_encoding = _encoding_cache.get(file_path)
            if cached_encoding:
                result.update({
                    'encoding': cached_encoding,
                    'confidence': 1.0,
                    'method': 'cache',
                    'cached': True
                })
                return result
        
        # 获取文件扩展名
        file_ext = Path(file_path).suffix.lower()
        
        # Excel文件通常使用UTF-8或系统默认编码
        if file_ext in ['.xlsx', '.xlsm', '.xlsb']:
            # 新版Excel文件通常是UTF-8
            result.update({
                'encoding': 'utf-8',
                'confidence': 0.9,
                'method': 'file_extension'
            })
        elif file_ext == '.xls':
            # 老版Excel文件可能使用系统编码
            import locale
            system_encoding = locale.getpreferredencoding()
            result.update({
                'encoding': system_encoding,
                'confidence': 0.7,
                'method': 'system_default'
            })
        
        # 对于CSV等文本文件，使用chardet检测
        if file_ext in ['.csv', '.txt'] or result['confidence'] < 0.8:
            try:
                # 读取文件前几KB进行检测
                with open(file_path, 'rb') as f:
                    raw_data = f.read(min(10240, os.path.getsize(file_path)))  # 最多读取10KB
                
                if raw_data:
                    detected = chardet.detect(raw_data)
                    if detected and detected['confidence'] > result['confidence']:
                        result.update({
                            'encoding': detected['encoding'] or 'utf-8',
                            'confidence': detected['confidence'],
                            'method': 'chardet'
                        })
                        
                        # 添加备选编码
                        common_encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5']
                        for enc in common_encodings:
                            if enc != result['encoding']:
                                try:
                                    raw_data.decode(enc)
                                    result['alternatives'].append(enc)
                                except UnicodeDecodeError:
                                    pass
            except Exception:
                pass
        
        # 缓存结果
        if use_cache and result['confidence'] > 0.5:
            _encoding_cache.set(file_path, result['encoding'])
            
    except Exception as e:
        result['error'] = str(e)
    
    return result


def smart_read_excel(file_path: str, 
                    sheet_name: Optional[Union[str, int]] = None,
                    encoding: Optional[str] = None,
                    auto_detect_params: bool = True,
                    **kwargs) -> Dict[str, Any]:
    """智能读取Excel文件
    
    Args:
        file_path: Excel文件路径
        sheet_name: 工作表名称或索引
        encoding: 指定编码（可选）
        auto_detect_params: 是否自动检测读取参数
        **kwargs: 其他pandas.read_excel参数
        
    Returns:
        dict: 包含DataFrame和读取信息
    """
    result = {
        'success': False,
        'dataframe': None,
        'info': {},
        'warnings': [],
        'errors': []
    }
    
    try:
        # 验证文件存在
        if not os.path.exists(file_path):
            result['errors'].append(f"文件不存在: {file_path}")
            return result
        
        # 检测编码
        if not encoding:
            encoding_info = detect_file_encoding(file_path)
            encoding = encoding_info['encoding']
            result['info']['encoding_detection'] = encoding_info
        
        # 获取文件基本信息
        file_info = {
            'file_size': os.path.getsize(file_path),
            'file_ext': Path(file_path).suffix.lower(),
            'encoding': encoding
        }
        result['info']['file_info'] = file_info
        
        # 自动检测读取参数
        read_params = kwargs.copy()
        if auto_detect_params:
            try:
                from excel_helper import _suggest_excel_read_parameters
                suggestions = _suggest_excel_read_parameters(file_path, sheet_name)
                
                # 只有当用户没有明确指定参数时，才使用建议的参数
                for key, value in suggestions.get('recommended_params', {}).items():
                    if key not in kwargs:  # 用户参数优先
                        read_params[key] = value
                
                result['info']['parameter_suggestions'] = suggestions
                
            except Exception as e:
                result['warnings'].append(f"参数自动检测失败: {str(e)}")
        
        # 设置工作表
        if sheet_name is not None:
            read_params['sheet_name'] = sheet_name
        
        # 尝试读取Excel文件
        attempts = []
        
        # 第一次尝试：使用检测到的编码和参数
        try:
            df = pd.read_excel(file_path, **read_params)
            
            # 修复列名：如果是元组格式，转换为字符串格式
            if hasattr(df, 'columns'):
                new_columns = []
                for col in df.columns:
                    if isinstance(col, tuple):
                        # 将元组列名转换为字符串，确保所有元素都是字符串类型
                        col_parts = []
                        for part in col:
                            if part is not None:
                                part_str = str(part).strip()
                                if part_str:  # 只添加非空字符串
                                    col_parts.append(part_str)
                        
                        if col_parts:
                            # 使用下划线连接多级列名，或取最后一个非空元素
                            if len(col_parts) > 1:
                                new_columns.append('_'.join(col_parts))
                            else:
                                new_columns.append(col_parts[0])
                        else:
                            new_columns.append(str(col))
                    else:
                        # 确保单级列名也是字符串
                        new_columns.append(str(col))
                df.columns = new_columns
            
            result['success'] = True
            result['dataframe'] = df
            result['info']['read_params'] = read_params
            attempts.append({'method': 'primary', 'success': True})
            
        except Exception as e:
            attempts.append({'method': 'primary', 'error': str(e)})
            
            # 第二次尝试：使用默认参数
            try:
                basic_params = {'sheet_name': sheet_name} if sheet_name else {}
                df = pd.read_excel(file_path, **basic_params)
                result['success'] = True
                result['dataframe'] = df
                result['info']['read_params'] = basic_params
                result['warnings'].append("使用默认参数读取成功")
                attempts.append({'method': 'fallback', 'success': True})
                
            except Exception as e2:
                attempts.append({'method': 'fallback', 'error': str(e2)})
                result['errors'].append(f"读取失败: {str(e2)}")
        
        result['info']['read_attempts'] = attempts
        
        # 如果成功读取，添加数据质量信息
        if result['success'] and result['dataframe'] is not None:
            df = result['dataframe']
            quality_info = {
                'shape': df.shape,
                'columns': df.columns.tolist(),
                'dtypes': df.dtypes.to_dict(),
                'null_counts': df.isnull().sum().to_dict(),
                'memory_usage': df.memory_usage(deep=True).sum(),
                'duplicate_rows': df.duplicated().sum()
            }
            result['info']['data_quality'] = quality_info
            
            # 检查数据质量问题
            if quality_info['duplicate_rows'] > 0:
                result['warnings'].append(f"发现{quality_info['duplicate_rows']}行重复数据")
            
            null_percentage = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
            if null_percentage > 10:
                result['warnings'].append(f"缺失值比例较高: {null_percentage:.1f}%")
    
    except Exception as e:
        result['errors'].append(f"读取过程出错: {str(e)}")
    
    return result


def validate_excel_data_integrity(original_file: str, 
                                processed_data: pd.DataFrame,
                                sheet_name: Optional[str] = None) -> Dict[str, Any]:
    """验证Excel数据处理的完整性
    
    Args:
        original_file: 原始Excel文件路径
        processed_data: 处理后的DataFrame
        sheet_name: 工作表名称
        
    Returns:
        dict: 完整性验证结果
    """
    validation_result = {
        'integrity_score': 0.0,
        'issues': [],
        'statistics': {},
        'recommendations': []
    }
    
    try:
        # 读取原始数据
        original_result = smart_read_excel(original_file, sheet_name=sheet_name)
        
        if not original_result['success']:
            validation_result['issues'].append("无法读取原始文件进行对比")
            return validation_result
        
        original_df = original_result['dataframe']
        
        # 基本统计对比
        original_stats = {
            'rows': len(original_df),
            'columns': len(original_df.columns),
            'null_count': original_df.isnull().sum().sum(),
            'memory_usage': original_df.memory_usage(deep=True).sum()
        }
        
        processed_stats = {
            'rows': len(processed_data),
            'columns': len(processed_data.columns),
            'null_count': processed_data.isnull().sum().sum(),
            'memory_usage': processed_data.memory_usage(deep=True).sum()
        }
        
        validation_result['statistics'] = {
            'original': original_stats,
            'processed': processed_stats
        }
        
        # 完整性检查
        integrity_checks = []
        
        # 行数检查
        if processed_stats['rows'] < original_stats['rows'] * 0.9:
            validation_result['issues'].append(f"数据行数显著减少: {original_stats['rows']} -> {processed_stats['rows']}")
            integrity_checks.append(0.5)
        else:
            integrity_checks.append(1.0)
        
        # 列数检查
        if processed_stats['columns'] < original_stats['columns'] * 0.8:
            validation_result['issues'].append(f"数据列数显著减少: {original_stats['columns']} -> {processed_stats['columns']}")
            integrity_checks.append(0.7)
        else:
            integrity_checks.append(1.0)
        
        # 缺失值检查
        null_increase = processed_stats['null_count'] - original_stats['null_count']
        if null_increase > original_stats['rows'] * 0.1:  # 缺失值增加超过10%的行数
            validation_result['issues'].append(f"缺失值显著增加: +{null_increase}")
            integrity_checks.append(0.8)
        else:
            integrity_checks.append(1.0)
        
        # 计算完整性得分
        validation_result['integrity_score'] = sum(integrity_checks) / len(integrity_checks)
        
        # 生成建议
        if validation_result['integrity_score'] < 0.8:
            validation_result['recommendations'].extend([
                "建议检查数据处理逻辑是否正确",
                "验证筛选条件是否过于严格",
                "确认数据类型转换是否合适"
            ])
        
        if len(validation_result['issues']) == 0:
            validation_result['recommendations'].append("数据完整性良好")
    
    except Exception as e:
        validation_result['issues'].append(f"验证过程出错: {str(e)}")
    
    return validation_result