#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据质量工具模块
提供全面的数据质量检查、清理和改进功能
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
import re
from datetime import datetime, date
import warnings
from dataclasses import dataclass
from enum import Enum
import json
from collections import Counter

class QualityIssueType(Enum):
    """数据质量问题类型"""
    MISSING_VALUES = "missing_values"
    DUPLICATE_ROWS = "duplicate_rows"
    INVALID_FORMAT = "invalid_format"
    OUTLIERS = "outliers"
    INCONSISTENT_DATA = "inconsistent_data"
    INVALID_RANGE = "invalid_range"
    ENCODING_ISSUES = "encoding_issues"
    TYPE_MISMATCH = "type_mismatch"
    CONSTRAINT_VIOLATION = "constraint_violation"
    REFERENTIAL_INTEGRITY = "referential_integrity"

class QualitySeverity(Enum):
    """质量问题严重程度"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class QualityIssue:
    """数据质量问题"""
    issue_type: QualityIssueType
    severity: QualitySeverity
    description: str
    affected_columns: List[str]
    affected_rows: List[int]
    count: int
    percentage: float
    suggestion: str
    auto_fixable: bool = False
    fix_function: Optional[str] = None

@dataclass
class QualityReport:
    """数据质量报告"""
    total_rows: int
    total_columns: int
    issues: List[QualityIssue]
    overall_score: float
    summary: Dict[str, Any]
    recommendations: List[str]
    timestamp: datetime

class DataQualityTools:
    """数据质量工具"""
    
    def __init__(self, df: Optional[pd.DataFrame] = None):
        self.df = df
        self.quality_rules = {}
        self.custom_validators = {}
        self._setup_default_rules()
    
    def set_dataframe(self, df: pd.DataFrame) -> None:
        """设置DataFrame"""
        self.df = df
    
    def _setup_default_rules(self) -> None:
        """设置默认质量规则"""
        self.quality_rules = {
            'missing_threshold': 0.05,  # 缺失值阈值5%
            'duplicate_threshold': 0.01,  # 重复行阈值1%
            'outlier_method': 'iqr',  # 异常值检测方法
            'outlier_threshold': 1.5,  # IQR倍数
            'min_string_length': 1,  # 最小字符串长度
            'max_string_length': 1000,  # 最大字符串长度
            'date_format_patterns': [  # 日期格式模式
                '%Y-%m-%d',
                '%Y/%m/%d',
                '%d-%m-%Y',
                '%d/%m/%Y',
                '%Y-%m-%d %H:%M:%S',
                '%Y/%m/%d %H:%M:%S'
            ],
            'email_pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone_pattern': r'^[\+]?[1-9]?[0-9]{7,15}$',
            'url_pattern': r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w*))?)?$'
        }
    
    def comprehensive_quality_check(self, 
                                  custom_rules: Optional[Dict[str, Any]] = None) -> QualityReport:
        """全面的数据质量检查"""
        if self.df is None:
            raise ValueError("请先设置DataFrame")
        
        # 更新自定义规则
        if custom_rules:
            self.quality_rules.update(custom_rules)
        
        issues = []
        
        # 1. 检查缺失值
        issues.extend(self._check_missing_values())
        
        # 2. 检查重复行
        issues.extend(self._check_duplicate_rows())
        
        # 3. 检查数据类型
        issues.extend(self._check_data_types())
        
        # 4. 检查异常值
        issues.extend(self._check_outliers())
        
        # 5. 检查数据格式
        issues.extend(self._check_data_formats())
        
        # 6. 检查数据一致性
        issues.extend(self._check_data_consistency())
        
        # 7. 检查数据范围
        issues.extend(self._check_data_ranges())
        
        # 8. 检查约束条件
        issues.extend(self._check_constraints())
        
        # 计算总体质量分数
        overall_score = self._calculate_quality_score(issues)
        
        # 生成摘要
        summary = self._generate_summary(issues)
        
        # 生成建议
        recommendations = self._generate_recommendations(issues)
        
        return QualityReport(
            total_rows=len(self.df),
            total_columns=len(self.df.columns),
            issues=issues,
            overall_score=overall_score,
            summary=summary,
            recommendations=recommendations,
            timestamp=datetime.now()
        )
    
    def _check_missing_values(self) -> List[QualityIssue]:
        """检查缺失值"""
        issues = []
        threshold = self.quality_rules['missing_threshold']
        
        for column in self.df.columns:
            missing_count = self.df[column].isna().sum()
            missing_percentage = missing_count / len(self.df)
            
            if missing_percentage > threshold:
                severity = QualitySeverity.HIGH if missing_percentage > 0.2 else QualitySeverity.MEDIUM
                
                issues.append(QualityIssue(
                    issue_type=QualityIssueType.MISSING_VALUES,
                    severity=severity,
                    description=f"列 '{column}' 有 {missing_count} 个缺失值 ({missing_percentage:.2%})",
                    affected_columns=[column],
                    affected_rows=self.df[self.df[column].isna()].index.tolist(),
                    count=missing_count,
                    percentage=missing_percentage,
                    suggestion=self._suggest_missing_value_treatment(column),
                    auto_fixable=True,
                    fix_function="fill_missing_values"
                ))
        
        return issues
    
    def _check_duplicate_rows(self) -> List[QualityIssue]:
        """检查重复行"""
        issues = []
        threshold = self.quality_rules['duplicate_threshold']
        
        duplicate_mask = self.df.duplicated()
        duplicate_count = duplicate_mask.sum()
        duplicate_percentage = duplicate_count / len(self.df)
        
        if duplicate_percentage > threshold:
            severity = QualitySeverity.HIGH if duplicate_percentage > 0.1 else QualitySeverity.MEDIUM
            
            issues.append(QualityIssue(
                issue_type=QualityIssueType.DUPLICATE_ROWS,
                severity=severity,
                description=f"发现 {duplicate_count} 行重复数据 ({duplicate_percentage:.2%})",
                affected_columns=list(self.df.columns),
                affected_rows=self.df[duplicate_mask].index.tolist(),
                count=duplicate_count,
                percentage=duplicate_percentage,
                suggestion="建议删除重复行或检查数据源",
                auto_fixable=True,
                fix_function="remove_duplicates"
            ))
        
        return issues
    
    def _check_data_types(self) -> List[QualityIssue]:
        """检查数据类型"""
        issues = []
        
        for column in self.df.columns:
            col_data = self.df[column].dropna()
            if len(col_data) == 0:
                continue
            
            # 检查数值列中的非数值数据
            if self.df[column].dtype in ['int64', 'float64']:
                continue  # 数值类型正常
            
            # 检查可能应该是数值的字符串列
            if self.df[column].dtype == 'object':
                numeric_convertible = 0
                for value in col_data:
                    try:
                        float(str(value).replace(',', '').replace('$', '').replace('%', ''))
                        numeric_convertible += 1
                    except (ValueError, TypeError):
                        pass
                
                if numeric_convertible / len(col_data) > 0.8:  # 80%可转换为数值
                    issues.append(QualityIssue(
                        issue_type=QualityIssueType.TYPE_MISMATCH,
                        severity=QualitySeverity.MEDIUM,
                        description=f"列 '{column}' 可能应该是数值类型",
                        affected_columns=[column],
                        affected_rows=[],
                        count=len(col_data) - numeric_convertible,
                        percentage=(len(col_data) - numeric_convertible) / len(col_data),
                        suggestion="考虑将此列转换为数值类型",
                        auto_fixable=True,
                        fix_function="convert_to_numeric"
                    ))
        
        return issues
    
    def _check_outliers(self) -> List[QualityIssue]:
        """检查异常值"""
        issues = []
        method = self.quality_rules['outlier_method']
        threshold = self.quality_rules['outlier_threshold']
        
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        
        for column in numeric_columns:
            col_data = self.df[column].dropna()
            if len(col_data) < 10:  # 数据太少，跳过异常值检测
                continue
            
            if method == 'iqr':
                Q1 = col_data.quantile(0.25)
                Q3 = col_data.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
                outliers = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]
            
            elif method == 'zscore':
                z_scores = np.abs((col_data - col_data.mean()) / col_data.std())
                outliers = self.df[z_scores > threshold]
            
            else:
                continue
            
            if len(outliers) > 0:
                outlier_percentage = len(outliers) / len(self.df)
                severity = QualitySeverity.HIGH if outlier_percentage > 0.05 else QualitySeverity.MEDIUM
                
                issues.append(QualityIssue(
                    issue_type=QualityIssueType.OUTLIERS,
                    severity=severity,
                    description=f"列 '{column}' 发现 {len(outliers)} 个异常值",
                    affected_columns=[column],
                    affected_rows=outliers.index.tolist(),
                    count=len(outliers),
                    percentage=outlier_percentage,
                    suggestion="检查异常值是否为数据错误或真实的极端值",
                    auto_fixable=False
                ))
        
        return issues
    
    def _check_data_formats(self) -> List[QualityIssue]:
        """检查数据格式"""
        issues = []
        
        for column in self.df.columns:
            if self.df[column].dtype != 'object':
                continue
            
            col_data = self.df[column].dropna().astype(str)
            if len(col_data) == 0:
                continue
            
            # 检查邮箱格式
            if any(keyword in column.lower() for keyword in ['email', 'mail', '邮箱']):
                invalid_emails = []
                email_pattern = re.compile(self.quality_rules['email_pattern'])
                
                for idx, value in col_data.items():
                    if not email_pattern.match(value):
                        invalid_emails.append(idx)
                
                if invalid_emails:
                    issues.append(QualityIssue(
                        issue_type=QualityIssueType.INVALID_FORMAT,
                        severity=QualitySeverity.MEDIUM,
                        description=f"列 '{column}' 有 {len(invalid_emails)} 个无效邮箱格式",
                        affected_columns=[column],
                        affected_rows=invalid_emails,
                        count=len(invalid_emails),
                        percentage=len(invalid_emails) / len(col_data),
                        suggestion="检查并修正邮箱格式",
                        auto_fixable=False
                    ))
            
            # 检查电话号码格式
            if any(keyword in column.lower() for keyword in ['phone', 'tel', '电话', '手机']):
                invalid_phones = []
                phone_pattern = re.compile(self.quality_rules['phone_pattern'])
                
                for idx, value in col_data.items():
                    cleaned_value = re.sub(r'[\s\-\(\)]', '', str(value))
                    if not phone_pattern.match(cleaned_value):
                        invalid_phones.append(idx)
                
                if invalid_phones:
                    issues.append(QualityIssue(
                        issue_type=QualityIssueType.INVALID_FORMAT,
                        severity=QualitySeverity.MEDIUM,
                        description=f"列 '{column}' 有 {len(invalid_phones)} 个无效电话格式",
                        affected_columns=[column],
                        affected_rows=invalid_phones,
                        count=len(invalid_phones),
                        percentage=len(invalid_phones) / len(col_data),
                        suggestion="检查并修正电话号码格式",
                        auto_fixable=False
                    ))
            
            # 检查日期格式
            if any(keyword in column.lower() for keyword in ['date', 'time', '日期', '时间']):
                invalid_dates = []
                
                for idx, value in col_data.items():
                    is_valid_date = False
                    for pattern in self.quality_rules['date_format_patterns']:
                        try:
                            datetime.strptime(str(value), pattern)
                            is_valid_date = True
                            break
                        except ValueError:
                            continue
                    
                    if not is_valid_date:
                        try:
                            pd.to_datetime(value)
                            is_valid_date = True
                        except (ValueError, TypeError):
                            pass
                    
                    if not is_valid_date:
                        invalid_dates.append(idx)
                
                if invalid_dates:
                    issues.append(QualityIssue(
                        issue_type=QualityIssueType.INVALID_FORMAT,
                        severity=QualitySeverity.MEDIUM,
                        description=f"列 '{column}' 有 {len(invalid_dates)} 个无效日期格式",
                        affected_columns=[column],
                        affected_rows=invalid_dates,
                        count=len(invalid_dates),
                        percentage=len(invalid_dates) / len(col_data),
                        suggestion="检查并修正日期格式",
                        auto_fixable=True,
                        fix_function="standardize_dates"
                    ))
        
        return issues
    
    def _check_data_consistency(self) -> List[QualityIssue]:
        """检查数据一致性"""
        issues = []
        
        # 检查字符串列的大小写一致性
        for column in self.df.columns:
            if self.df[column].dtype != 'object':
                continue
            
            col_data = self.df[column].dropna().astype(str)
            if len(col_data) == 0:
                continue
            
            # 检查是否有相同内容但大小写不同的值
            value_counts = col_data.str.lower().value_counts()
            original_counts = col_data.value_counts()
            
            inconsistent_values = []
            for lower_value, count in value_counts.items():
                original_variants = [v for v in original_counts.index if v.lower() == lower_value]
                if len(original_variants) > 1:
                    inconsistent_values.extend(original_variants)
            
            if inconsistent_values:
                affected_rows = self.df[self.df[column].isin(inconsistent_values)].index.tolist()
                
                issues.append(QualityIssue(
                    issue_type=QualityIssueType.INCONSISTENT_DATA,
                    severity=QualitySeverity.MEDIUM,
                    description=f"列 '{column}' 存在大小写不一致的重复值",
                    affected_columns=[column],
                    affected_rows=affected_rows,
                    count=len(affected_rows),
                    percentage=len(affected_rows) / len(self.df),
                    suggestion="统一大小写格式",
                    auto_fixable=True,
                    fix_function="standardize_case"
                ))
        
        return issues
    
    def _check_data_ranges(self) -> List[QualityIssue]:
        """检查数据范围"""
        issues = []
        
        # 检查数值列的合理范围
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        
        for column in numeric_columns:
            col_data = self.df[column].dropna()
            if len(col_data) == 0:
                continue
            
            # 检查负值（对于通常应该为正的列）
            if any(keyword in column.lower() for keyword in ['age', 'price', 'amount', 'count', '年龄', '价格', '数量']):
                negative_values = self.df[self.df[column] < 0]
                if len(negative_values) > 0:
                    issues.append(QualityIssue(
                        issue_type=QualityIssueType.INVALID_RANGE,
                        severity=QualitySeverity.HIGH,
                        description=f"列 '{column}' 有 {len(negative_values)} 个负值",
                        affected_columns=[column],
                        affected_rows=negative_values.index.tolist(),
                        count=len(negative_values),
                        percentage=len(negative_values) / len(self.df),
                        suggestion="检查负值是否合理",
                        auto_fixable=False
                    ))
            
            # 检查年龄范围
            if 'age' in column.lower() or '年龄' in column:
                invalid_ages = self.df[(self.df[column] < 0) | (self.df[column] > 150)]
                if len(invalid_ages) > 0:
                    issues.append(QualityIssue(
                        issue_type=QualityIssueType.INVALID_RANGE,
                        severity=QualitySeverity.HIGH,
                        description=f"列 '{column}' 有 {len(invalid_ages)} 个不合理的年龄值",
                        affected_columns=[column],
                        affected_rows=invalid_ages.index.tolist(),
                        count=len(invalid_ages),
                        percentage=len(invalid_ages) / len(self.df),
                        suggestion="年龄应在0-150之间",
                        auto_fixable=False
                    ))
        
        return issues
    
    def _check_constraints(self) -> List[QualityIssue]:
        """检查约束条件"""
        issues = []
        
        # 检查字符串长度约束
        for column in self.df.columns:
            if self.df[column].dtype != 'object':
                continue
            
            col_data = self.df[column].dropna().astype(str)
            if len(col_data) == 0:
                continue
            
            min_length = self.quality_rules['min_string_length']
            max_length = self.quality_rules['max_string_length']
            
            # 检查过短的字符串
            too_short = self.df[self.df[column].astype(str).str.len() < min_length]
            if len(too_short) > 0:
                issues.append(QualityIssue(
                    issue_type=QualityIssueType.CONSTRAINT_VIOLATION,
                    severity=QualitySeverity.MEDIUM,
                    description=f"列 '{column}' 有 {len(too_short)} 个过短的值",
                    affected_columns=[column],
                    affected_rows=too_short.index.tolist(),
                    count=len(too_short),
                    percentage=len(too_short) / len(self.df),
                    suggestion=f"字符串长度应至少为 {min_length}",
                    auto_fixable=False
                ))
            
            # 检查过长的字符串
            too_long = self.df[self.df[column].astype(str).str.len() > max_length]
            if len(too_long) > 0:
                issues.append(QualityIssue(
                    issue_type=QualityIssueType.CONSTRAINT_VIOLATION,
                    severity=QualitySeverity.MEDIUM,
                    description=f"列 '{column}' 有 {len(too_long)} 个过长的值",
                    affected_columns=[column],
                    affected_rows=too_long.index.tolist(),
                    count=len(too_long),
                    percentage=len(too_long) / len(self.df),
                    suggestion=f"字符串长度应不超过 {max_length}",
                    auto_fixable=True,
                    fix_function="truncate_strings"
                ))
        
        return issues
    
    def _suggest_missing_value_treatment(self, column: str) -> str:
        """建议缺失值处理方法"""
        col_data = self.df[column].dropna()
        
        if self.df[column].dtype in ['int64', 'float64']:
            return "建议使用均值、中位数或插值填充数值缺失值"
        elif self.df[column].dtype == 'object':
            if len(col_data.unique()) < 10:
                return "建议使用众数填充分类缺失值"
            else:
                return "建议使用'未知'或删除文本缺失值"
        else:
            return "建议根据业务逻辑处理缺失值"
    
    def _calculate_quality_score(self, issues: List[QualityIssue]) -> float:
        """计算数据质量分数"""
        if not issues:
            return 100.0
        
        total_penalty = 0
        severity_weights = {
            QualitySeverity.LOW: 1,
            QualitySeverity.MEDIUM: 3,
            QualitySeverity.HIGH: 7,
            QualitySeverity.CRITICAL: 15
        }
        
        for issue in issues:
            penalty = severity_weights[issue.severity] * issue.percentage * 100
            total_penalty += penalty
        
        score = max(0, 100 - total_penalty)
        return round(score, 2)
    
    def _generate_summary(self, issues: List[QualityIssue]) -> Dict[str, Any]:
        """生成质量问题摘要"""
        summary = {
            'total_issues': len(issues),
            'by_type': {},
            'by_severity': {},
            'most_affected_columns': [],
            'auto_fixable_count': 0
        }
        
        # 按类型统计
        for issue in issues:
            issue_type = issue.issue_type.value
            summary['by_type'][issue_type] = summary['by_type'].get(issue_type, 0) + 1
        
        # 按严重程度统计
        for issue in issues:
            severity = issue.severity.value
            summary['by_severity'][severity] = summary['by_severity'].get(severity, 0) + 1
        
        # 统计受影响最多的列
        column_counts = Counter()
        for issue in issues:
            for column in issue.affected_columns:
                column_counts[column] += 1
        
        summary['most_affected_columns'] = column_counts.most_common(5)
        
        # 统计可自动修复的问题
        summary['auto_fixable_count'] = sum(1 for issue in issues if issue.auto_fixable)
        
        return summary
    
    def _generate_recommendations(self, issues: List[QualityIssue]) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 基于问题类型生成建议
        issue_types = set(issue.issue_type for issue in issues)
        
        if QualityIssueType.MISSING_VALUES in issue_types:
            recommendations.append("建立数据收集标准，减少缺失值产生")
            recommendations.append("实施数据验证规则，确保关键字段完整性")
        
        if QualityIssueType.DUPLICATE_ROWS in issue_types:
            recommendations.append("建立唯一性约束，防止重复数据录入")
            recommendations.append("定期执行重复数据检查和清理")
        
        if QualityIssueType.INVALID_FORMAT in issue_types:
            recommendations.append("实施输入格式验证，确保数据格式一致性")
            recommendations.append("提供数据录入模板和示例")
        
        if QualityIssueType.OUTLIERS in issue_types:
            recommendations.append("建立异常值检测和处理流程")
            recommendations.append("定期审查数据范围和业务规则")
        
        if QualityIssueType.INCONSISTENT_DATA in issue_types:
            recommendations.append("建立数据标准化流程")
            recommendations.append("使用下拉列表等控件限制输入选项")
        
        # 通用建议
        recommendations.extend([
            "建立数据质量监控仪表板",
            "定期进行数据质量评估",
            "培训数据录入人员，提高数据质量意识",
            "建立数据质量反馈机制"
        ])
        
        return recommendations
    
    def auto_fix_issues(self, issues: List[QualityIssue]) -> Dict[str, Any]:
        """自动修复可修复的问题"""
        if self.df is None:
            raise ValueError("请先设置DataFrame")
        
        fixed_issues = []
        failed_fixes = []
        
        for issue in issues:
            if not issue.auto_fixable or not issue.fix_function:
                continue
            
            try:
                if issue.fix_function == "fill_missing_values":
                    self._fix_missing_values(issue.affected_columns[0])
                elif issue.fix_function == "remove_duplicates":
                    self._fix_duplicates()
                elif issue.fix_function == "convert_to_numeric":
                    self._fix_numeric_conversion(issue.affected_columns[0])
                elif issue.fix_function == "standardize_dates":
                    self._fix_date_formats(issue.affected_columns[0])
                elif issue.fix_function == "standardize_case":
                    self._fix_case_consistency(issue.affected_columns[0])
                elif issue.fix_function == "truncate_strings":
                    self._fix_string_length(issue.affected_columns[0])
                
                fixed_issues.append(issue)
            except Exception as e:
                failed_fixes.append({
                    'issue': issue,
                    'error': str(e)
                })
        
        return {
            'fixed_count': len(fixed_issues),
            'failed_count': len(failed_fixes),
            'fixed_issues': fixed_issues,
            'failed_fixes': failed_fixes
        }
    
    def _fix_missing_values(self, column: str) -> None:
        """修复缺失值"""
        if self.df[column].dtype in ['int64', 'float64']:
            # 数值列用中位数填充
            median_value = self.df[column].median()
            self.df[column].fillna(median_value, inplace=True)
        elif self.df[column].dtype == 'object':
            # 分类列用众数填充
            mode_value = self.df[column].mode()
            if len(mode_value) > 0:
                self.df[column].fillna(mode_value[0], inplace=True)
            else:
                self.df[column].fillna('未知', inplace=True)
    
    def _fix_duplicates(self) -> None:
        """修复重复行"""
        self.df.drop_duplicates(inplace=True)
        self.df.reset_index(drop=True, inplace=True)
    
    def _fix_numeric_conversion(self, column: str) -> None:
        """修复数值转换"""
        def clean_numeric(value):
            if pd.isna(value):
                return value
            try:
                # 清理常见的非数值字符
                cleaned = str(value).replace(',', '').replace('$', '').replace('%', '')
                return float(cleaned)
            except (ValueError, TypeError):
                return np.nan
        
        self.df[column] = self.df[column].apply(clean_numeric)
    
    def _fix_date_formats(self, column: str) -> None:
        """修复日期格式"""
        self.df[column] = pd.to_datetime(self.df[column], errors='coerce')
    
    def _fix_case_consistency(self, column: str) -> None:
        """修复大小写一致性"""
        # 转换为标题格式
        self.df[column] = self.df[column].astype(str).str.title()
    
    def _fix_string_length(self, column: str) -> None:
        """修复字符串长度"""
        max_length = self.quality_rules['max_string_length']
        self.df[column] = self.df[column].astype(str).str[:max_length]
    
    def export_quality_report(self, report: QualityReport, 
                            format: str = 'json', 
                            filepath: Optional[str] = None) -> str:
        """导出质量报告"""
        if format == 'json':
            report_dict = {
                'timestamp': report.timestamp.isoformat(),
                'total_rows': report.total_rows,
                'total_columns': report.total_columns,
                'overall_score': report.overall_score,
                'summary': report.summary,
                'recommendations': report.recommendations,
                'issues': [
                    {
                        'type': issue.issue_type.value,
                        'severity': issue.severity.value,
                        'description': issue.description,
                        'affected_columns': issue.affected_columns,
                        'count': issue.count,
                        'percentage': issue.percentage,
                        'suggestion': issue.suggestion,
                        'auto_fixable': issue.auto_fixable
                    }
                    for issue in report.issues
                ]
            }
            
            report_json = json.dumps(report_dict, indent=2, ensure_ascii=False)
            
            if filepath:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(report_json)
            
            return report_json
        
        elif format == 'html':
            # 生成HTML报告
            html_content = self._generate_html_report(report)
            
            if filepath:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            
            return html_content
        
        else:
            raise ValueError(f"不支持的格式: {format}")
    
    def _generate_html_report(self, report: QualityReport) -> str:
        """生成HTML格式的质量报告"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>数据质量报告</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .score {{ font-size: 24px; font-weight: bold; color: {'green' if report.overall_score >= 80 else 'orange' if report.overall_score >= 60 else 'red'}; }}
                .section {{ margin: 20px 0; }}
                .issue {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }}
                .severity-high {{ border-left: 5px solid #ff4444; }}
                .severity-medium {{ border-left: 5px solid #ffaa00; }}
                .severity-low {{ border-left: 5px solid #44ff44; }}
                .severity-critical {{ border-left: 5px solid #aa0000; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>数据质量报告</h1>
                <p>生成时间: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>数据规模: {report.total_rows} 行 × {report.total_columns} 列</p>
                <p class="score">质量分数: {report.overall_score}/100</p>
            </div>
            
            <div class="section">
                <h2>问题摘要</h2>
                <p>总问题数: {report.summary['total_issues']}</p>
                <p>可自动修复: {report.summary['auto_fixable_count']}</p>
                
                <h3>按严重程度分布</h3>
                <table>
                    <tr><th>严重程度</th><th>数量</th></tr>
        """
        
        for severity, count in report.summary['by_severity'].items():
            html += f"<tr><td>{severity}</td><td>{count}</td></tr>"
        
        html += """
                </table>
                
                <h3>按问题类型分布</h3>
                <table>
                    <tr><th>问题类型</th><th>数量</th></tr>
        """
        
        for issue_type, count in report.summary['by_type'].items():
            html += f"<tr><td>{issue_type}</td><td>{count}</td></tr>"
        
        html += """
                </table>
            </div>
            
            <div class="section">
                <h2>详细问题</h2>
        """
        
        for issue in report.issues:
            severity_class = f"severity-{issue.severity.value}"
            html += f"""
                <div class="issue {severity_class}">
                    <h4>{issue.description}</h4>
                    <p><strong>类型:</strong> {issue.issue_type.value}</p>
                    <p><strong>严重程度:</strong> {issue.severity.value}</p>
                    <p><strong>影响列:</strong> {', '.join(issue.affected_columns)}</p>
                    <p><strong>影响行数:</strong> {issue.count} ({issue.percentage:.2%})</p>
                    <p><strong>建议:</strong> {issue.suggestion}</p>
                    <p><strong>可自动修复:</strong> {'是' if issue.auto_fixable else '否'}</p>
                </div>
            """
        
        html += """
            </div>
            
            <div class="section">
                <h2>改进建议</h2>
                <ul>
        """
        
        for recommendation in report.recommendations:
            html += f"<li>{recommendation}</li>"
        
        html += """
                </ul>
            </div>
        </body>
        </html>
        """
        
        return html

def create_data_quality_tools(df: Optional[pd.DataFrame] = None) -> DataQualityTools:
    """创建数据质量工具实例"""
    return DataQualityTools(df)