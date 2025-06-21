#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合数据验证模块
提供全面的数据质量检查和验证功能
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
import re
from datetime import datetime, date
import warnings
from dataclasses import dataclass
from enum import Enum

class ValidationLevel(Enum):
    """验证级别"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class ValidationResult:
    """验证结果"""
    rule_name: str
    level: ValidationLevel
    passed: bool
    message: str
    details: Optional[Dict[str, Any]] = None
    affected_rows: Optional[List[int]] = None
    affected_columns: Optional[List[str]] = None
    suggestions: Optional[List[str]] = None

class ComprehensiveDataVerifier:
    """综合数据验证器"""
    
    def __init__(self, df: Optional[pd.DataFrame] = None):
        self.df = df
        self.validation_rules = {}
        self.results = []
        self._register_default_rules()
    
    def set_dataframe(self, df: pd.DataFrame) -> None:
        """设置要验证的DataFrame"""
        self.df = df
        self.results.clear()
    
    def _register_default_rules(self) -> None:
        """注册默认验证规则"""
        self.validation_rules = {
            'missing_values': self._check_missing_values,
            'duplicate_rows': self._check_duplicate_rows,
            'data_types': self._check_data_types,
            'outliers': self._check_outliers,
            'data_consistency': self._check_data_consistency,
            'column_names': self._check_column_names,
            'data_range': self._check_data_range,
            'string_patterns': self._check_string_patterns,
            'date_validity': self._check_date_validity,
            'referential_integrity': self._check_referential_integrity
        }
    
    def verify_all(self, rules: Optional[List[str]] = None) -> Dict[str, Any]:
        """执行所有验证规则"""
        if self.df is None:
            return {
                'success': False,
                'error': 'DataFrame未设置',
                'results': []
            }
        
        rules_to_run = rules or list(self.validation_rules.keys())
        self.results.clear()
        
        for rule_name in rules_to_run:
            if rule_name in self.validation_rules:
                try:
                    rule_func = self.validation_rules[rule_name]
                    result = rule_func()
                    if isinstance(result, list):
                        self.results.extend(result)
                    else:
                        self.results.append(result)
                except Exception as e:
                    error_result = ValidationResult(
                        rule_name=rule_name,
                        level=ValidationLevel.ERROR,
                        passed=False,
                        message=f"验证规则执行失败: {str(e)}"
                    )
                    self.results.append(error_result)
        
        return self._generate_summary()
    
    def _check_missing_values(self) -> List[ValidationResult]:
        """检查缺失值"""
        results = []
        missing_stats = self.df.isnull().sum()
        total_rows = len(self.df)
        
        for column, missing_count in missing_stats.items():
            if missing_count > 0:
                missing_percentage = (missing_count / total_rows) * 100
                
                if missing_percentage > 50:
                    level = ValidationLevel.CRITICAL
                elif missing_percentage > 20:
                    level = ValidationLevel.ERROR
                elif missing_percentage > 5:
                    level = ValidationLevel.WARNING
                else:
                    level = ValidationLevel.INFO
                
                results.append(ValidationResult(
                    rule_name="missing_values",
                    level=level,
                    passed=missing_percentage <= 5,
                    message=f"列 '{column}' 有 {missing_count} 个缺失值 ({missing_percentage:.1f}%)",
                    details={
                        'column': column,
                        'missing_count': missing_count,
                        'missing_percentage': missing_percentage,
                        'total_rows': total_rows
                    },
                    affected_columns=[column],
                    suggestions=[
                        "考虑删除缺失值过多的列" if missing_percentage > 50 else "使用适当的方法填充缺失值",
                        "检查数据收集过程是否存在问题"
                    ]
                ))
        
        if not results:
            results.append(ValidationResult(
                rule_name="missing_values",
                level=ValidationLevel.INFO,
                passed=True,
                message="所有列都没有缺失值"
            ))
        
        return results
    
    def _check_duplicate_rows(self) -> ValidationResult:
        """检查重复行"""
        duplicate_mask = self.df.duplicated()
        duplicate_count = duplicate_mask.sum()
        total_rows = len(self.df)
        
        if duplicate_count > 0:
            duplicate_percentage = (duplicate_count / total_rows) * 100
            duplicate_indices = self.df[duplicate_mask].index.tolist()
            
            level = ValidationLevel.WARNING if duplicate_percentage < 10 else ValidationLevel.ERROR
            
            return ValidationResult(
                rule_name="duplicate_rows",
                level=level,
                passed=False,
                message=f"发现 {duplicate_count} 行重复数据 ({duplicate_percentage:.1f}%)",
                details={
                    'duplicate_count': duplicate_count,
                    'duplicate_percentage': duplicate_percentage,
                    'total_rows': total_rows
                },
                affected_rows=duplicate_indices,
                suggestions=[
                    "使用 df.drop_duplicates() 删除重复行",
                    "检查数据源是否存在重复录入"
                ]
            )
        else:
            return ValidationResult(
                rule_name="duplicate_rows",
                level=ValidationLevel.INFO,
                passed=True,
                message="没有发现重复行"
            )
    
    def _check_data_types(self) -> List[ValidationResult]:
        """检查数据类型"""
        results = []
        
        for column in self.df.columns:
            col_data = self.df[column]
            current_dtype = str(col_data.dtype)
            
            # 检查是否应该是数值类型但被识别为object
            if current_dtype == 'object':
                # 尝试转换为数值
                try:
                    numeric_converted = pd.to_numeric(col_data, errors='coerce')
                    non_numeric_count = numeric_converted.isnull().sum() - col_data.isnull().sum()
                    
                    if non_numeric_count == 0 and not col_data.isnull().all():
                        results.append(ValidationResult(
                            rule_name="data_types",
                            level=ValidationLevel.WARNING,
                            passed=False,
                            message=f"列 '{column}' 可能应该是数值类型而不是文本类型",
                            details={
                                'column': column,
                                'current_type': current_dtype,
                                'suggested_type': 'numeric'
                            },
                            affected_columns=[column],
                            suggestions=[f"使用 pd.to_numeric(df['{column}']) 转换为数值类型"]
                        ))
                except:
                    pass
                
                # 检查是否应该是日期类型
                try:
                    date_converted = pd.to_datetime(col_data, errors='coerce')
                    non_date_count = date_converted.isnull().sum() - col_data.isnull().sum()
                    
                    if non_date_count == 0 and not col_data.isnull().all():
                        # 进一步检查是否真的像日期
                        sample_values = col_data.dropna().astype(str).head(10)
                        date_like_patterns = [r'\d{4}-\d{2}-\d{2}', r'\d{2}/\d{2}/\d{4}', r'\d{4}/\d{2}/\d{2}']
                        
                        if any(re.match(pattern, str(val)) for val in sample_values for pattern in date_like_patterns):
                            results.append(ValidationResult(
                                rule_name="data_types",
                                level=ValidationLevel.INFO,
                                passed=False,
                                message=f"列 '{column}' 可能应该是日期类型",
                                details={
                                    'column': column,
                                    'current_type': current_dtype,
                                    'suggested_type': 'datetime'
                                },
                                affected_columns=[column],
                                suggestions=[f"使用 pd.to_datetime(df['{column}']) 转换为日期类型"]
                            ))
                except:
                    pass
        
        if not results:
            results.append(ValidationResult(
                rule_name="data_types",
                level=ValidationLevel.INFO,
                passed=True,
                message="数据类型检查通过"
            ))
        
        return results
    
    def _check_outliers(self) -> List[ValidationResult]:
        """检查异常值"""
        results = []
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        
        for column in numeric_columns:
            col_data = self.df[column].dropna()
            if len(col_data) < 4:  # 数据太少无法检测异常值
                continue
            
            # 使用IQR方法检测异常值
            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers_mask = (col_data < lower_bound) | (col_data > upper_bound)
            outliers_count = outliers_mask.sum()
            
            if outliers_count > 0:
                outliers_percentage = (outliers_count / len(col_data)) * 100
                outlier_indices = col_data[outliers_mask].index.tolist()
                
                level = ValidationLevel.WARNING if outliers_percentage < 5 else ValidationLevel.ERROR
                
                results.append(ValidationResult(
                    rule_name="outliers",
                    level=level,
                    passed=outliers_percentage < 1,
                    message=f"列 '{column}' 发现 {outliers_count} 个异常值 ({outliers_percentage:.1f}%)",
                    details={
                        'column': column,
                        'outliers_count': outliers_count,
                        'outliers_percentage': outliers_percentage,
                        'lower_bound': lower_bound,
                        'upper_bound': upper_bound,
                        'outlier_values': col_data[outliers_mask].tolist()[:10]  # 只显示前10个
                    },
                    affected_rows=outlier_indices,
                    affected_columns=[column],
                    suggestions=[
                        "检查异常值是否为数据录入错误",
                        "考虑使用适当的方法处理异常值（删除、替换或保留）"
                    ]
                ))
        
        if not results:
            results.append(ValidationResult(
                rule_name="outliers",
                level=ValidationLevel.INFO,
                passed=True,
                message="未发现明显异常值"
            ))
        
        return results
    
    def _check_data_consistency(self) -> List[ValidationResult]:
        """检查数据一致性"""
        results = []
        
        # 检查字符串列的一致性（大小写、空格等）
        string_columns = self.df.select_dtypes(include=['object']).columns
        
        for column in string_columns:
            col_data = self.df[column].dropna().astype(str)
            if len(col_data) == 0:
                continue
            
            # 检查大小写不一致
            unique_values = col_data.unique()
            lowercase_groups = {}
            
            for value in unique_values:
                lower_val = value.lower().strip()
                if lower_val in lowercase_groups:
                    lowercase_groups[lower_val].append(value)
                else:
                    lowercase_groups[lower_val] = [value]
            
            inconsistent_groups = {k: v for k, v in lowercase_groups.items() if len(v) > 1}
            
            if inconsistent_groups:
                results.append(ValidationResult(
                    rule_name="data_consistency",
                    level=ValidationLevel.WARNING,
                    passed=False,
                    message=f"列 '{column}' 存在大小写或空格不一致的值",
                    details={
                        'column': column,
                        'inconsistent_groups': dict(list(inconsistent_groups.items())[:5])  # 只显示前5组
                    },
                    affected_columns=[column],
                    suggestions=[
                        "使用 df[column].str.lower().str.strip() 标准化文本",
                        "检查数据录入规范"
                    ]
                ))
        
        if not results:
            results.append(ValidationResult(
                rule_name="data_consistency",
                level=ValidationLevel.INFO,
                passed=True,
                message="数据一致性检查通过"
            ))
        
        return results
    
    def _check_column_names(self) -> ValidationResult:
        """检查列名规范"""
        issues = []
        
        for column in self.df.columns:
            col_str = str(column)
            
            # 检查空格
            if ' ' in col_str:
                issues.append(f"列名 '{column}' 包含空格")
            
            # 检查特殊字符
            if re.search(r'[^a-zA-Z0-9_\u4e00-\u9fff]', col_str):
                issues.append(f"列名 '{column}' 包含特殊字符")
            
            # 检查是否以数字开头
            if col_str[0].isdigit():
                issues.append(f"列名 '{column}' 以数字开头")
        
        if issues:
            return ValidationResult(
                rule_name="column_names",
                level=ValidationLevel.WARNING,
                passed=False,
                message=f"发现 {len(issues)} 个列名规范问题",
                details={'issues': issues},
                suggestions=[
                    "使用下划线替代空格",
                    "避免使用特殊字符",
                    "列名不要以数字开头"
                ]
            )
        else:
            return ValidationResult(
                rule_name="column_names",
                level=ValidationLevel.INFO,
                passed=True,
                message="列名规范检查通过"
            )
    
    def _check_data_range(self) -> List[ValidationResult]:
        """检查数据范围合理性"""
        results = []
        
        # 这里可以添加特定的业务规则检查
        # 例如：年龄不应该超过150，百分比应该在0-100之间等
        
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        
        for column in numeric_columns:
            col_data = self.df[column].dropna()
            if len(col_data) == 0:
                continue
            
            min_val = col_data.min()
            max_val = col_data.max()
            
            # 检查是否有负数（对于某些业务场景可能不合理）
            if '年龄' in str(column).lower() or 'age' in str(column).lower():
                if min_val < 0 or max_val > 150:
                    results.append(ValidationResult(
                        rule_name="data_range",
                        level=ValidationLevel.ERROR,
                        passed=False,
                        message=f"年龄列 '{column}' 的值范围不合理: {min_val} - {max_val}",
                        details={'column': column, 'min': min_val, 'max': max_val},
                        affected_columns=[column],
                        suggestions=["检查年龄数据的录入是否正确"]
                    ))
            
            # 检查百分比列
            if '百分比' in str(column) or 'percent' in str(column).lower() or '%' in str(column):
                if min_val < 0 or max_val > 100:
                    results.append(ValidationResult(
                        rule_name="data_range",
                        level=ValidationLevel.WARNING,
                        passed=False,
                        message=f"百分比列 '{column}' 的值超出0-100范围: {min_val} - {max_val}",
                        details={'column': column, 'min': min_val, 'max': max_val},
                        affected_columns=[column],
                        suggestions=["确认百分比数据的单位和格式"]
                    ))
        
        if not results:
            results.append(ValidationResult(
                rule_name="data_range",
                level=ValidationLevel.INFO,
                passed=True,
                message="数据范围检查通过"
            ))
        
        return results
    
    def _check_string_patterns(self) -> List[ValidationResult]:
        """检查字符串模式"""
        results = []
        string_columns = self.df.select_dtypes(include=['object']).columns
        
        # 常见模式检查
        patterns = {
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone': r'^[\d\-\+\(\)\s]{10,}$',
            'id_card': r'^\d{15}$|^\d{17}[\dXx]$'  # 简化的身份证号模式
        }
        
        for column in string_columns:
            col_data = self.df[column].dropna().astype(str)
            if len(col_data) == 0:
                continue
            
            # 根据列名推测可能的模式
            column_lower = str(column).lower()
            
            for pattern_name, pattern in patterns.items():
                if pattern_name in column_lower or (pattern_name == 'email' and 'mail' in column_lower):
                    invalid_count = 0
                    invalid_values = []
                    
                    for value in col_data:
                        if not re.match(pattern, str(value)):
                            invalid_count += 1
                            if len(invalid_values) < 5:
                                invalid_values.append(value)
                    
                    if invalid_count > 0:
                        invalid_percentage = (invalid_count / len(col_data)) * 100
                        
                        results.append(ValidationResult(
                            rule_name="string_patterns",
                            level=ValidationLevel.WARNING,
                            passed=invalid_percentage < 5,
                            message=f"列 '{column}' 有 {invalid_count} 个值不符合 {pattern_name} 格式 ({invalid_percentage:.1f}%)",
                            details={
                                'column': column,
                                'pattern_type': pattern_name,
                                'invalid_count': invalid_count,
                                'invalid_percentage': invalid_percentage,
                                'sample_invalid_values': invalid_values
                            },
                            affected_columns=[column],
                            suggestions=[f"检查 {pattern_name} 格式的数据录入"]
                        ))
        
        if not results:
            results.append(ValidationResult(
                rule_name="string_patterns",
                level=ValidationLevel.INFO,
                passed=True,
                message="字符串模式检查通过"
            ))
        
        return results
    
    def _check_date_validity(self) -> List[ValidationResult]:
        """检查日期有效性"""
        results = []
        date_columns = self.df.select_dtypes(include=['datetime64']).columns
        
        for column in date_columns:
            col_data = self.df[column].dropna()
            if len(col_data) == 0:
                continue
            
            # 检查未来日期（可能不合理）
            future_dates = col_data[col_data > pd.Timestamp.now()]
            if len(future_dates) > 0:
                results.append(ValidationResult(
                    rule_name="date_validity",
                    level=ValidationLevel.WARNING,
                    passed=False,
                    message=f"列 '{column}' 包含 {len(future_dates)} 个未来日期",
                    details={
                        'column': column,
                        'future_dates_count': len(future_dates),
                        'sample_future_dates': future_dates.head().tolist()
                    },
                    affected_columns=[column],
                    suggestions=["检查未来日期是否合理"]
                ))
            
            # 检查过于久远的日期
            very_old_dates = col_data[col_data < pd.Timestamp('1900-01-01')]
            if len(very_old_dates) > 0:
                results.append(ValidationResult(
                    rule_name="date_validity",
                    level=ValidationLevel.WARNING,
                    passed=False,
                    message=f"列 '{column}' 包含 {len(very_old_dates)} 个过于久远的日期",
                    details={
                        'column': column,
                        'old_dates_count': len(very_old_dates),
                        'sample_old_dates': very_old_dates.head().tolist()
                    },
                    affected_columns=[column],
                    suggestions=["检查历史日期是否正确"]
                ))
        
        if not results:
            results.append(ValidationResult(
                rule_name="date_validity",
                level=ValidationLevel.INFO,
                passed=True,
                message="日期有效性检查通过"
            ))
        
        return results
    
    def _check_referential_integrity(self) -> ValidationResult:
        """检查引用完整性（简化版）"""
        # 这里可以添加更复杂的引用完整性检查
        # 例如：外键约束、主键唯一性等
        
        return ValidationResult(
            rule_name="referential_integrity",
            level=ValidationLevel.INFO,
            passed=True,
            message="引用完整性检查跳过（需要业务规则定义）"
        )
    
    def _generate_summary(self) -> Dict[str, Any]:
        """生成验证摘要"""
        total_checks = len(self.results)
        passed_checks = sum(1 for r in self.results if r.passed)
        failed_checks = total_checks - passed_checks
        
        # 按级别统计
        level_counts = {level.value: 0 for level in ValidationLevel}
        for result in self.results:
            level_counts[result.level.value] += 1
        
        # 按规则统计
        rule_counts = {}
        for result in self.results:
            if result.rule_name not in rule_counts:
                rule_counts[result.rule_name] = {'passed': 0, 'failed': 0}
            if result.passed:
                rule_counts[result.rule_name]['passed'] += 1
            else:
                rule_counts[result.rule_name]['failed'] += 1
        
        return {
            'success': True,
            'summary': {
                'total_checks': total_checks,
                'passed_checks': passed_checks,
                'failed_checks': failed_checks,
                'pass_rate': (passed_checks / total_checks * 100) if total_checks > 0 else 0
            },
            'level_distribution': level_counts,
            'rule_distribution': rule_counts,
            'results': [{
                'rule_name': r.rule_name,
                'level': r.level.value,
                'passed': r.passed,
                'message': r.message,
                'details': r.details,
                'affected_rows': r.affected_rows,
                'affected_columns': r.affected_columns,
                'suggestions': r.suggestions
            } for r in self.results],
            'recommendations': self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 基于验证结果生成建议
        critical_issues = [r for r in self.results if r.level == ValidationLevel.CRITICAL]
        error_issues = [r for r in self.results if r.level == ValidationLevel.ERROR]
        
        if critical_issues:
            recommendations.append("立即处理关键问题，这些问题可能严重影响数据质量")
        
        if error_issues:
            recommendations.append("优先处理错误级别的问题")
        
        # 具体建议
        missing_value_issues = [r for r in self.results if r.rule_name == 'missing_values' and not r.passed]
        if missing_value_issues:
            recommendations.append("建立数据收集规范，减少缺失值")
        
        duplicate_issues = [r for r in self.results if r.rule_name == 'duplicate_rows' and not r.passed]
        if duplicate_issues:
            recommendations.append("实施数据去重流程")
        
        type_issues = [r for r in self.results if r.rule_name == 'data_types' and not r.passed]
        if type_issues:
            recommendations.append("标准化数据类型，确保数据一致性")
        
        return recommendations

def create_comprehensive_verifier(df: pd.DataFrame) -> ComprehensiveDataVerifier:
    """创建综合数据验证器实例"""
    return ComprehensiveDataVerifier(df)