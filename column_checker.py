#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
列检查器模块
提供DataFrame列的验证、检查和建议功能
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Set
import re
from difflib import SequenceMatcher

class ColumnChecker:
    """DataFrame列检查器"""
    
    def __init__(self, df: Optional[pd.DataFrame] = None):
        self.df = df
        self.column_cache = {}
        self.similarity_threshold = 0.6
    
    def set_dataframe(self, df: pd.DataFrame) -> None:
        """设置要检查的DataFrame"""
        self.df = df
        self.column_cache.clear()
    
    def check_column_exists(self, column_name: str) -> bool:
        """检查列是否存在"""
        if self.df is None:
            return False
        return column_name in self.df.columns
    
    def suggest_similar_columns(self, target_column: str, max_suggestions: int = 5) -> List[Dict[str, Any]]:
        """建议相似的列名"""
        if self.df is None:
            return []
        
        suggestions = []
        
        for col in self.df.columns:
            similarity = self._calculate_similarity(target_column, str(col))
            if similarity > self.similarity_threshold:
                suggestions.append({
                    'column': col,
                    'similarity': similarity,
                    'type': str(self.df[col].dtype),
                    'non_null_count': self.df[col].count(),
                    'unique_count': self.df[col].nunique()
                })
        
        # 按相似度排序
        suggestions.sort(key=lambda x: x['similarity'], reverse=True)
        return suggestions[:max_suggestions]
    
    def validate_columns(self, required_columns: List[str]) -> Dict[str, Any]:
        """验证必需的列是否存在"""
        if self.df is None:
            return {
                'valid': False,
                'error': 'DataFrame未设置',
                'missing_columns': required_columns,
                'suggestions': {}
            }
        
        existing_columns = set(self.df.columns)
        required_set = set(required_columns)
        missing_columns = list(required_set - existing_columns)
        
        result = {
            'valid': len(missing_columns) == 0,
            'missing_columns': missing_columns,
            'existing_columns': list(required_set & existing_columns),
            'suggestions': {}
        }
        
        # 为缺失的列提供建议
        for missing_col in missing_columns:
            suggestions = self.suggest_similar_columns(missing_col)
            if suggestions:
                result['suggestions'][missing_col] = suggestions
        
        return result
    
    def analyze_column_types(self) -> Dict[str, Dict[str, Any]]:
        """分析所有列的类型和统计信息"""
        if self.df is None:
            return {}
        
        analysis = {}
        
        for col in self.df.columns:
            col_data = self.df[col]
            analysis[col] = {
                'dtype': str(col_data.dtype),
                'non_null_count': col_data.count(),
                'null_count': col_data.isnull().sum(),
                'unique_count': col_data.nunique(),
                'memory_usage': col_data.memory_usage(deep=True),
                'is_numeric': pd.api.types.is_numeric_dtype(col_data),
                'is_datetime': pd.api.types.is_datetime64_any_dtype(col_data),
                'is_categorical': pd.api.types.is_categorical_dtype(col_data)
            }
            
            # 添加数值列的统计信息
            if analysis[col]['is_numeric']:
                analysis[col].update({
                    'min': col_data.min(),
                    'max': col_data.max(),
                    'mean': col_data.mean(),
                    'std': col_data.std()
                })
            
            # 添加分类列的信息
            if col_data.nunique() < 20:  # 假设唯一值少于20的为分类列
                analysis[col]['value_counts'] = col_data.value_counts().to_dict()
        
        return analysis
    
    def check_column_compatibility(self, column_name: str, expected_type: str) -> Dict[str, Any]:
        """检查列的类型兼容性"""
        if self.df is None or column_name not in self.df.columns:
            return {
                'compatible': False,
                'error': f'列 {column_name} 不存在',
                'suggestions': []
            }
        
        col_data = self.df[column_name]
        current_type = str(col_data.dtype)
        
        # 类型兼容性映射
        type_compatibility = {
            'numeric': ['int64', 'int32', 'float64', 'float32', 'int8', 'int16'],
            'string': ['object', 'string'],
            'datetime': ['datetime64[ns]', 'datetime64'],
            'boolean': ['bool', 'boolean'],
            'category': ['category']
        }
        
        compatible = False
        suggestions = []
        
        # 检查直接兼容性
        for type_group, dtypes in type_compatibility.items():
            if expected_type.lower() in type_group.lower():
                if any(dtype in current_type for dtype in dtypes):
                    compatible = True
                    break
                else:
                    # 提供转换建议
                    if type_group == 'numeric' and col_data.dtype == 'object':
                        try:
                            pd.to_numeric(col_data, errors='coerce')
                            suggestions.append(f"可以使用 pd.to_numeric() 转换为数值类型")
                        except:
                            suggestions.append(f"无法转换为数值类型，请检查数据")
                    
                    elif type_group == 'datetime' and col_data.dtype == 'object':
                        try:
                            pd.to_datetime(col_data, errors='coerce')
                            suggestions.append(f"可以使用 pd.to_datetime() 转换为日期类型")
                        except:
                            suggestions.append(f"无法转换为日期类型，请检查数据格式")
        
        return {
            'compatible': compatible,
            'current_type': current_type,
            'expected_type': expected_type,
            'suggestions': suggestions
        }
    
    def find_columns_by_pattern(self, pattern: str, use_regex: bool = False) -> List[str]:
        """根据模式查找列名"""
        if self.df is None:
            return []
        
        matching_columns = []
        
        for col in self.df.columns:
            col_str = str(col)
            if use_regex:
                if re.search(pattern, col_str, re.IGNORECASE):
                    matching_columns.append(col)
            else:
                if pattern.lower() in col_str.lower():
                    matching_columns.append(col)
        
        return matching_columns
    
    def get_column_summary(self, column_name: str) -> Dict[str, Any]:
        """获取列的详细摘要信息"""
        if self.df is None or column_name not in self.df.columns:
            return {'error': f'列 {column_name} 不存在'}
        
        col_data = self.df[column_name]
        
        summary = {
            'name': column_name,
            'dtype': str(col_data.dtype),
            'shape': len(col_data),
            'non_null_count': col_data.count(),
            'null_count': col_data.isnull().sum(),
            'null_percentage': (col_data.isnull().sum() / len(col_data)) * 100,
            'unique_count': col_data.nunique(),
            'unique_percentage': (col_data.nunique() / len(col_data)) * 100,
            'memory_usage_bytes': col_data.memory_usage(deep=True)
        }
        
        # 数值列的额外信息
        if pd.api.types.is_numeric_dtype(col_data):
            summary.update({
                'min': col_data.min(),
                'max': col_data.max(),
                'mean': col_data.mean(),
                'median': col_data.median(),
                'std': col_data.std(),
                'quantiles': {
                    '25%': col_data.quantile(0.25),
                    '75%': col_data.quantile(0.75)
                }
            })
        
        # 文本列的额外信息
        elif col_data.dtype == 'object':
            summary.update({
                'avg_length': col_data.astype(str).str.len().mean(),
                'max_length': col_data.astype(str).str.len().max(),
                'min_length': col_data.astype(str).str.len().min()
            })
        
        # 前几个唯一值示例
        if col_data.nunique() <= 10:
            summary['unique_values'] = col_data.unique().tolist()
        else:
            summary['sample_values'] = col_data.unique()[:10].tolist()
        
        return summary
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """计算两个字符串的相似度"""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def suggest_column_operations(self, column_name: str) -> List[Dict[str, Any]]:
        """建议对列可以执行的操作"""
        if self.df is None or column_name not in self.df.columns:
            return []
        
        col_data = self.df[column_name]
        suggestions = []
        
        # 基础操作
        suggestions.append({
            'operation': 'describe',
            'description': '获取列的统计描述',
            'code': f'df["{column_name}"].describe()'
        })
        
        # 数值列操作
        if pd.api.types.is_numeric_dtype(col_data):
            suggestions.extend([
                {
                    'operation': 'histogram',
                    'description': '绘制直方图',
                    'code': f'df["{column_name}"].hist()'
                },
                {
                    'operation': 'normalize',
                    'description': '标准化数值',
                    'code': f'(df["{column_name}"] - df["{column_name}"].mean()) / df["{column_name}"].std()'
                }
            ])
        
        # 文本列操作
        elif col_data.dtype == 'object':
            suggestions.extend([
                {
                    'operation': 'value_counts',
                    'description': '统计值频次',
                    'code': f'df["{column_name}"].value_counts()'
                },
                {
                    'operation': 'string_length',
                    'description': '计算字符串长度',
                    'code': f'df["{column_name}"].str.len()'
                }
            ])
        
        # 缺失值处理
        if col_data.isnull().any():
            suggestions.append({
                'operation': 'fill_missing',
                'description': '填充缺失值',
                'code': f'df["{column_name}"].fillna(method="ffill")'
            })
        
        return suggestions

def create_column_checker(df: pd.DataFrame) -> ColumnChecker:
    """创建列检查器实例"""
    return ColumnChecker(df)