#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块

提供Excel处理系统的统一配置管理：
- 全局配置管理
- 环境变量处理
- 配置文件加载
- 动态配置更新
- 配置验证
- 默认配置

作者: AI Assistant
创建时间: 2024-12-19
版本: 1.0.0
"""

import os
import json
import yaml
import configparser
from pathlib import Path
from typing import Dict, Any, Optional, Union, List, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging
from threading import Lock

try:
    from error_codes import ErrorCode, ErrorCodeManager
except ImportError:
    # 如果error_codes模块不存在，创建占位符
    class ErrorCode:
        E500_CONFIG_FILE_NOT_FOUND = "E500"
        E501_CONFIG_PARSE_ERROR = "E501"
        E502_CONFIG_VALIDATION_FAILED = "E502"
    
    class ErrorCodeManager:
        @staticmethod
        def create_error_response(error_code, context=None):
            return {"error": error_code, "context": context}


class ConfigFormat(Enum):
    """配置文件格式"""
    JSON = "json"
    YAML = "yaml"
    INI = "ini"
    ENV = "env"


class LogLevel(Enum):
    """日志级别"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class CacheConfig:
    """缓存配置"""
    enabled: bool = True
    max_size: int = 100
    ttl_seconds: int = 3600
    cleanup_interval: int = 300
    memory_threshold_mb: float = 500.0
    disk_cache_enabled: bool = False
    disk_cache_path: Optional[str] = None
    disk_cache_size_mb: float = 1000.0


@dataclass
class PerformanceConfig:
    """性能配置"""
    max_workers: int = 4
    chunk_size: int = 10000
    memory_limit_mb: float = 1000.0
    timeout_seconds: int = 300
    enable_profiling: bool = False
    profile_output_dir: Optional[str] = None
    gc_threshold: int = 1000
    parallel_processing: bool = True


@dataclass
class SecurityConfig:
    """安全配置"""
    max_file_size_mb: float = 100.0
    allowed_extensions: List[str] = field(default_factory=lambda: ['.xlsx', '.xls', '.csv', '.tsv'])
    blocked_functions: List[str] = field(default_factory=lambda: ['exec', 'eval', 'open', '__import__'])
    sandbox_mode: bool = True
    code_execution_timeout: int = 30
    max_code_length: int = 10000
    allowed_modules: List[str] = field(default_factory=lambda: ['pandas', 'numpy', 'math', 'datetime'])


@dataclass
class LoggingConfig:
    """日志配置"""
    level: LogLevel = LogLevel.INFO
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_enabled: bool = True
    file_path: Optional[str] = None
    file_max_size_mb: float = 10.0
    file_backup_count: int = 5
    console_enabled: bool = True
    structured_logging: bool = False


@dataclass
class ExcelConfig:
    """Excel处理配置"""
    default_encoding: str = "utf-8"
    encoding_detection_enabled: bool = True
    multiheader_detection_enabled: bool = True
    auto_column_mapping: bool = True
    smart_type_inference: bool = True
    error_recovery_enabled: bool = True
    max_header_rows: int = 5
    min_data_rows: int = 1
    column_name_normalization: bool = True
    duplicate_column_handling: str = "rename"  # rename, drop, error


@dataclass
class APIConfig:
    """API配置"""
    version: str = "1.0.0"
    request_timeout: int = 300
    max_request_size_mb: float = 50.0
    rate_limit_enabled: bool = False
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600
    cors_enabled: bool = True
    cors_origins: List[str] = field(default_factory=lambda: ["*"])


@dataclass
class MCPToolsConfig:
    """MCP工具配置"""
    server_name: str = "chatExcel-mcp"
    server_version: str = "1.0.0"
    max_tools: int = 50
    enable_tool_validation: bool = True
    tool_timeout_seconds: int = 120
    enable_tool_caching: bool = True
    tool_cache_size: int = 100
    log_tool_usage: bool = True
    enable_async_execution: bool = True
    max_concurrent_tools: int = 10
    tool_registry_path: str = "./mcp_tools_registry.json"
    enable_tool_metrics: bool = True
    metrics_collection_interval: int = 60
    enable_error_recovery: bool = True
    max_retry_attempts: int = 3
    retry_delay_seconds: int = 1


@dataclass
class EncodingConfig:
    """编码检测配置"""
    default_encoding: str = "utf-8"
    fallback_encodings: List[str] = field(default_factory=lambda: ["utf-8", "gbk", "gb2312", "latin-1", "cp1252"])
    enable_bom_detection: bool = True
    confidence_threshold: float = 0.8
    cache_encoding_results: bool = True
    encoding_cache_size: int = 1000
    enable_chardet: bool = True
    chardet_timeout: int = 5
    enable_fallback_chain: bool = True


@dataclass
class HeaderDetectionConfig:
    """列头检测配置"""
    enable_multiheader_detection: bool = True
    max_header_rows: int = 5
    min_confidence_score: float = 0.7
    enable_semantic_analysis: bool = True
    cache_header_patterns: bool = True
    header_cache_size: int = 500
    enable_fuzzy_matching: bool = True
    fuzzy_threshold: float = 0.8
    default_header_row: int = 0
    skip_blank_headers: bool = True
    enable_pattern_learning: bool = True
    pattern_learning_threshold: int = 10


@dataclass
class GlobalConfig:
    """全局配置"""
    # 基本配置
    app_name: str = "Excel Processor"
    version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"  # development, testing, production
    
    # 子配置
    cache: CacheConfig = field(default_factory=CacheConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    excel: ExcelConfig = field(default_factory=ExcelConfig)
    api: APIConfig = field(default_factory=APIConfig)
    mcp_tools: MCPToolsConfig = field(default_factory=MCPToolsConfig)
    encoding: EncodingConfig = field(default_factory=EncodingConfig)
    header_detection: HeaderDetectionConfig = field(default_factory=HeaderDetectionConfig)
    
    # 自定义配置
    custom: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    def update_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """从字典更新配置"""
        for key, value in config_dict.items():
            if hasattr(self, key):
                attr = getattr(self, key)
                if hasattr(attr, '__dict__'):  # 是dataclass对象
                    if isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            if hasattr(attr, sub_key):
                                setattr(attr, sub_key, sub_value)
                else:
                    setattr(self, key, value)
            elif key == 'custom':
                if isinstance(value, dict):
                    self.custom.update(value)


class ConfigManager:
    """配置管理器"""
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self._config = GlobalConfig()
        self._config_file_path = None
        self._watchers = []
        self._initialized = True
        
        # 设置默认日志路径
        if self._config.logging.file_path is None:
            self._config.logging.file_path = str(Path.cwd() / "logs" / "excel_processor.log")
        
        # 设置默认缓存路径
        if self._config.cache.disk_cache_path is None:
            self._config.cache.disk_cache_path = str(Path.cwd() / "cache")
        
        # 从环境变量加载配置
        self._load_from_env()
    
    @property
    def config(self) -> GlobalConfig:
        """获取配置"""
        return self._config
    
    def load_from_file(self, file_path: Union[str, Path], format: Optional[ConfigFormat] = None) -> Union[bool, Dict[str, Any]]:
        """从文件加载配置"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                logging.warning(f"配置文件不存在: {file_path}")
                return ErrorCodeManager.create_error_response(
                    ErrorCode.E500_CONFIG_FILE_NOT_FOUND,
                    context={"file_path": str(file_path)}
                )
            
            # 自动检测格式
            if format is None:
                format = self._detect_format(file_path)
            
            config_dict = self._load_config_file(file_path, format)
            if config_dict:
                self._config.update_from_dict(config_dict)
                self._config_file_path = str(file_path)
                logging.info(f"成功加载配置文件: {file_path}")
                return True
            else:
                return ErrorCodeManager.create_error_response(
                    ErrorCode.E501_CONFIG_PARSE_ERROR,
                    context={"file_path": str(file_path), "format": format.value}
                )
            
        except Exception as e:
            logging.error(f"加载配置文件失败: {e}")
            return ErrorCodeManager.create_error_response(
                ErrorCode.E501_CONFIG_PARSE_ERROR,
                context={"file_path": str(file_path), "error": str(e)}
            )
    
    def save_to_file(self, file_path: Union[str, Path], format: ConfigFormat = ConfigFormat.JSON) -> bool:
        """保存配置到文件"""
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            config_dict = self._config.to_dict()
            
            if format == ConfigFormat.JSON:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(config_dict, f, indent=2, ensure_ascii=False, default=str)
            
            elif format == ConfigFormat.YAML:
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(config_dict, f, default_flow_style=False, allow_unicode=True)
            
            elif format == ConfigFormat.INI:
                config = configparser.ConfigParser()
                self._dict_to_ini(config_dict, config)
                with open(file_path, 'w', encoding='utf-8') as f:
                    config.write(f)
            
            logging.info(f"配置已保存到: {file_path}")
            return True
            
        except Exception as e:
            logging.error(f"保存配置文件失败: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        try:
            keys = key.split('.')
            value = self._config
            
            for k in keys:
                if hasattr(value, k):
                    value = getattr(value, k)
                elif isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            
            return value
        except Exception:
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """设置配置值"""
        try:
            keys = key.split('.')
            target = self._config
            
            # 导航到目标对象
            for k in keys[:-1]:
                if hasattr(target, k):
                    target = getattr(target, k)
                elif isinstance(target, dict):
                    if k not in target:
                        target[k] = {}
                    target = target[k]
                else:
                    return False
            
            # 设置值
            final_key = keys[-1]
            if hasattr(target, final_key):
                setattr(target, final_key, value)
            elif isinstance(target, dict):
                target[final_key] = value
            else:
                return False
            
            # 通知观察者
            self._notify_watchers(key, value)
            return True
            
        except Exception as e:
            logging.error(f"设置配置失败: {e}")
            return False
    
    def update(self, config_dict: Dict[str, Any]) -> None:
        """批量更新配置"""
        self._config.update_from_dict(config_dict)
        self._notify_watchers("*", config_dict)
    
    def reset_to_defaults(self) -> None:
        """重置为默认配置"""
        self._config = GlobalConfig()
        self._load_from_env()
        logging.info("配置已重置为默认值")
    
    def validate(self) -> Union[Tuple[bool, List[str]], Dict[str, Any]]:
        """验证配置"""
        errors = []
        
        try:
            # 验证性能配置
            if self._config.performance.max_workers <= 0:
                errors.append("performance.max_workers 必须大于0")
            
            if self._config.performance.chunk_size <= 0:
                errors.append("performance.chunk_size 必须大于0")
            
            if self._config.performance.memory_limit_mb <= 0:
                errors.append("performance.memory_limit_mb 必须大于0")
            
            # 验证安全配置
            if self._config.security.max_file_size_mb <= 0:
                errors.append("security.max_file_size_mb 必须大于0")
            
            if not self._config.security.allowed_extensions:
                errors.append("security.allowed_extensions 不能为空")
            
            # 验证缓存配置
            if self._config.cache.max_size <= 0:
                errors.append("cache.max_size 必须大于0")
            
            if self._config.cache.ttl_seconds <= 0:
                errors.append("cache.ttl_seconds 必须大于0")
            
            # 验证Excel配置
            if self._config.excel.max_header_rows <= 0:
                errors.append("excel.max_header_rows 必须大于0")
            
            if self._config.excel.min_data_rows < 0:
                errors.append("excel.min_data_rows 不能小于0")
            
            # 验证MCP工具配置
            if self._config.mcp_tools.max_tools <= 0:
                errors.append("mcp_tools.max_tools 必须大于0")
            
            if self._config.mcp_tools.tool_timeout_seconds <= 0:
                errors.append("mcp_tools.tool_timeout_seconds 必须大于0")
            
            if self._config.mcp_tools.max_concurrent_tools <= 0:
                errors.append("mcp_tools.max_concurrent_tools 必须大于0")
            
            # 验证编码配置
            if not self._config.encoding.default_encoding:
                errors.append("encoding.default_encoding 不能为空")
            
            if self._config.encoding.confidence_threshold < 0 or self._config.encoding.confidence_threshold > 1:
                errors.append("encoding.confidence_threshold 必须在0-1之间")
            
            # 验证列头检测配置
            if self._config.header_detection.max_header_rows <= 0:
                errors.append("header_detection.max_header_rows 必须大于0")
            
            if self._config.header_detection.min_confidence_score < 0 or self._config.header_detection.min_confidence_score > 1:
                errors.append("header_detection.min_confidence_score 必须在0-1之间")
            
            if errors:
                return ErrorCodeManager.create_error_response(
                    ErrorCode.E502_CONFIG_VALIDATION_FAILED,
                    context={"validation_errors": errors}
                )
            
            return len(errors) == 0, errors
            
        except Exception as e:
            return ErrorCodeManager.create_error_response(
                ErrorCode.E502_CONFIG_VALIDATION_FAILED,
                context={"error": str(e)}
            )
    
    def add_watcher(self, callback) -> None:
        """添加配置变化监听器"""
        self._watchers.append(callback)
    
    def remove_watcher(self, callback) -> None:
        """移除配置变化监听器"""
        if callback in self._watchers:
            self._watchers.remove(callback)
    
    def _load_from_env(self) -> None:
        """从环境变量加载配置"""
        env_mappings = {
            'EXCEL_PROCESSOR_DEBUG': ('debug', lambda x: x.lower() == 'true'),
            'EXCEL_PROCESSOR_ENVIRONMENT': ('environment', str),
            'EXCEL_PROCESSOR_LOG_LEVEL': ('logging.level', lambda x: LogLevel(x.upper())),
            'EXCEL_PROCESSOR_CACHE_ENABLED': ('cache.enabled', lambda x: x.lower() == 'true'),
            'EXCEL_PROCESSOR_MAX_WORKERS': ('performance.max_workers', int),
            'EXCEL_PROCESSOR_MEMORY_LIMIT': ('performance.memory_limit_mb', float),
            'EXCEL_PROCESSOR_MAX_FILE_SIZE': ('security.max_file_size_mb', float),
            'EXCEL_PROCESSOR_SANDBOX_MODE': ('security.sandbox_mode', lambda x: x.lower() == 'true'),
        }
        
        for env_var, (config_key, converter) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                try:
                    converted_value = converter(value)
                    self.set(config_key, converted_value)
                except Exception as e:
                    logging.warning(f"环境变量 {env_var} 转换失败: {e}")
    
    def _detect_format(self, file_path: Path) -> ConfigFormat:
        """检测配置文件格式"""
        suffix = file_path.suffix.lower()
        if suffix in ['.json']:
            return ConfigFormat.JSON
        elif suffix in ['.yaml', '.yml']:
            return ConfigFormat.YAML
        elif suffix in ['.ini', '.cfg']:
            return ConfigFormat.INI
        else:
            return ConfigFormat.JSON  # 默认JSON
    
    def _load_config_file(self, file_path: Path, format: ConfigFormat) -> Optional[Dict[str, Any]]:
        """加载配置文件"""
        try:
            if format == ConfigFormat.JSON:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif format == ConfigFormat.YAML:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            
            elif format == ConfigFormat.INI:
                config = configparser.ConfigParser()
                config.read(file_path, encoding='utf-8')
                return self._ini_to_dict(config)
            
        except Exception as e:
            logging.error(f"解析配置文件失败: {e}")
        
        return None
    
    def _ini_to_dict(self, config: configparser.ConfigParser) -> Dict[str, Any]:
        """将INI配置转换为字典"""
        result = {}
        for section_name in config.sections():
            section = {}
            for key, value in config.items(section_name):
                # 尝试转换数据类型
                if value.lower() in ['true', 'false']:
                    section[key] = value.lower() == 'true'
                elif value.isdigit():
                    section[key] = int(value)
                elif '.' in value and value.replace('.', '').isdigit():
                    section[key] = float(value)
                else:
                    section[key] = value
            result[section_name] = section
        return result
    
    def _dict_to_ini(self, data: Dict[str, Any], config: configparser.ConfigParser, section_prefix: str = "") -> None:
        """将字典转换为INI配置"""
        for key, value in data.items():
            if isinstance(value, dict):
                section_name = f"{section_prefix}.{key}" if section_prefix else key
                if section_name not in config:
                    config.add_section(section_name)
                self._dict_to_ini(value, config, section_name)
            else:
                if not section_prefix:
                    section_name = "DEFAULT"
                else:
                    section_name = section_prefix
                
                if section_name not in config and section_name != "DEFAULT":
                    config.add_section(section_name)
                
                config.set(section_name, key, str(value))
    
    def _notify_watchers(self, key: str, value: Any) -> None:
        """通知配置变化监听器"""
        for watcher in self._watchers:
            try:
                watcher(key, value)
            except Exception as e:
                logging.error(f"配置监听器执行失败: {e}")


class ConfigValidator:
    """配置验证器"""
    
    @staticmethod
    def validate_file_path(path: str) -> bool:
        """验证文件路径"""
        try:
            path_obj = Path(path)
            return path_obj.parent.exists() or path_obj.parent == Path('.')
        except Exception:
            return False
    
    @staticmethod
    def validate_memory_size(size_mb: float) -> bool:
        """验证内存大小"""
        return 0 < size_mb <= 10240  # 最大10GB
    
    @staticmethod
    def validate_timeout(timeout: int) -> bool:
        """验证超时时间"""
        return 1 <= timeout <= 3600  # 1秒到1小时
    
    @staticmethod
    def validate_worker_count(count: int) -> bool:
        """验证工作线程数"""
        import multiprocessing
        max_workers = multiprocessing.cpu_count() * 2
        return 1 <= count <= max_workers


# 全局配置管理器实例
config_manager = ConfigManager()


def get_config() -> GlobalConfig:
    """获取全局配置"""
    return config_manager.config


def get_setting(key: str, default: Any = None) -> Any:
    """获取配置项"""
    return config_manager.get(key, default)


def set_setting(key: str, value: Any) -> bool:
    """设置配置项"""
    return config_manager.set(key, value)


def load_config_file(file_path: Union[str, Path]) -> bool:
    """加载配置文件"""
    return config_manager.load_from_file(file_path)


def save_config_file(file_path: Union[str, Path], format: ConfigFormat = ConfigFormat.JSON) -> bool:
    """保存配置文件"""
    return config_manager.save_to_file(file_path, format)


if __name__ == "__main__":
    # 测试配置管理器
    config = get_config()
    print(f"应用名称: {config.app_name}")
    print(f"版本: {config.version}")
    print(f"调试模式: {config.debug}")
    print(f"最大工作线程: {config.performance.max_workers}")
    print(f"缓存启用: {config.cache.enabled}")
    
    # 测试配置验证
    is_valid, errors = config_manager.validate()
    print(f"\n配置验证: {'通过' if is_valid else '失败'}")
    if errors:
        for error in errors:
            print(f"  - {error}")
    
    # 测试保存配置
    test_config_path = Path("test_config.json")
    if save_config_file(test_config_path):
        print(f"\n配置已保存到: {test_config_path}")
        
        # 测试加载配置
        if load_config_file(test_config_path):
            print("配置加载成功")
        
        # 清理测试文件
        test_config_path.unlink(missing_ok=True)
    
    print("\n配置管理模块测试完成")