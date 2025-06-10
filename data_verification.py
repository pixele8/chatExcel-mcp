#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据验证和核实模块
提供数据比对、统计验证、质量评估等功能
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Union, Tuple
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


class DataVerificationEngine:
    """数据验证引擎"""
    
    def __init__(self):
        self.tolerance = 1e-10  # 数值比较容差
        self.verification_history = []
    
    def compare_dataframes(self, 
                          df1: pd.DataFrame, 
                          df2: pd.DataFrame,
                          name1: str = "数据集1",
                          name2: str = "数据集2",
                          key_columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """比较两个DataFrame的差异
        
        Args:
            df1: 第一个DataFrame
            df2: 第二个DataFrame
            name1: 第一个数据集名称
            name2: 第二个数据集名称
            key_columns: 用于匹配的关键列
            
        Returns:
            dict: 详细的比较结果
        """
        comparison_result = {
            'summary': {},
            'structural_differences': {},
            'content_differences': {},
            'statistical_comparison': {},
            'recommendations': [],
            'match_score': 0.0
        }
        
        try:
            # 基本信息比较
            basic_info = {
                name1: {
                    'shape': df1.shape,
                    'columns': df1.columns.tolist(),
                    'dtypes': df1.dtypes.to_dict(),
                    'memory_usage': df1.memory_usage(deep=True).sum()
                },
                name2: {
                    'shape': df2.shape,
                    'columns': df2.columns.tolist(),
                    'dtypes': df2.dtypes.to_dict(),
                    'memory_usage': df2.memory_usage(deep=True).sum()
                }
            }
            comparison_result['summary'] = basic_info
            
            # 结构差异分析
            structural_diff = self._analyze_structural_differences(df1, df2, name1, name2)
            comparison_result['structural_differences'] = structural_diff
            
            # 内容差异分析
            if structural_diff['columns_match'] and structural_diff['shape_compatible']:
                content_diff = self._analyze_content_differences(df1, df2, name1, name2, key_columns)
                comparison_result['content_differences'] = content_diff
                
                # 统计比较
                stats_comparison = self._compare_statistics(df1, df2, name1, name2)
                comparison_result['statistical_comparison'] = stats_comparison
                
                # 计算匹配得分
                match_score = self._calculate_match_score(structural_diff, content_diff, stats_comparison)
                comparison_result['match_score'] = match_score
            
            # 生成建议
            recommendations = self._generate_recommendations(comparison_result)
            comparison_result['recommendations'] = recommendations
            
        except Exception as e:
            comparison_result['error'] = str(e)
        
        return comparison_result
    
    def _analyze_structural_differences(self, df1: pd.DataFrame, df2: pd.DataFrame, 
                                      name1: str, name2: str) -> Dict[str, Any]:
        """分析结构差异"""
        structural_diff = {
            'shape_match': df1.shape == df2.shape,
            'shape_compatible': True,
            'columns_match': False,
            'column_differences': {},
            'dtype_differences': {}
        }
        
        # 列名比较
        cols1, cols2 = set(df1.columns), set(df2.columns)
        common_cols = cols1.intersection(cols2)
        only_in_1 = cols1 - cols2
        only_in_2 = cols2 - cols1
        
        structural_diff['columns_match'] = len(only_in_1) == 0 and len(only_in_2) == 0
        structural_diff['column_differences'] = {
            'common_columns': list(common_cols),
            f'only_in_{name1}': list(only_in_1),
            f'only_in_{name2}': list(only_in_2),
            'common_count': len(common_cols),
            'total_unique': len(cols1.union(cols2))
        }
        
        # 数据类型比较
        dtype_diff = {}
        for col in common_cols:
            if df1[col].dtype != df2[col].dtype:
                dtype_diff[col] = {
                    name1: str(df1[col].dtype),
                    name2: str(df2[col].dtype)
                }
        
        structural_diff['dtype_differences'] = dtype_diff
        
        # 形状兼容性检查
        if abs(df1.shape[0] - df2.shape[0]) > max(df1.shape[0], df2.shape[0]) * 0.1:
            structural_diff['shape_compatible'] = False
        
        return structural_diff
    
    def _analyze_content_differences(self, df1: pd.DataFrame, df2: pd.DataFrame,
                                   name1: str, name2: str, 
                                   key_columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """分析内容差异"""
        content_diff = {
            'identical_rows': 0,
            'different_rows': 0,
            'missing_in_1': 0,
            'missing_in_2': 0,
            'column_differences': {},
            'value_differences': []
        }
        
        try:
            # 获取公共列
            common_cols = list(set(df1.columns).intersection(set(df2.columns)))
            
            if not common_cols:
                content_diff['error'] = "没有公共列可供比较"
                return content_diff
            
            # 如果指定了关键列，使用关键列进行匹配
            if key_columns:
                valid_keys = [col for col in key_columns if col in common_cols]
                if valid_keys:
                    content_diff.update(self._compare_by_key_columns(df1, df2, valid_keys, common_cols))
                else:
                    content_diff['warning'] = "指定的关键列不在公共列中，使用索引比较"
                    content_diff.update(self._compare_by_index(df1, df2, common_cols))
            else:
                content_diff.update(self._compare_by_index(df1, df2, common_cols))
            
        except Exception as e:
            content_diff['error'] = str(e)
        
        return content_diff
    
    def _compare_by_key_columns(self, df1: pd.DataFrame, df2: pd.DataFrame,
                               key_columns: List[str], common_cols: List[str]) -> Dict[str, Any]:
        """基于关键列进行比较"""
        result = {
            'comparison_method': 'key_columns',
            'key_columns': key_columns
        }
        
        try:
            # 基于关键列合并
            merged = pd.merge(df1[common_cols], df2[common_cols], 
                            on=key_columns, how='outer', 
                            suffixes=('_1', '_2'), indicator=True)
            
            # 统计匹配情况
            both_count = (merged['_merge'] == 'both').sum()
            left_only = (merged['_merge'] == 'left_only').sum()
            right_only = (merged['_merge'] == 'right_only').sum()
            
            result.update({
                'matched_records': both_count,
                'missing_in_2': left_only,
                'missing_in_1': right_only,
                'total_unique_records': len(merged)
            })
            
            # 比较匹配记录的值差异
            both_data = merged[merged['_merge'] == 'both']
            value_cols = [col for col in common_cols if col not in key_columns]
            
            differences = []
            for col in value_cols:
                col1, col2 = f"{col}_1", f"{col}_2"
                if col1 in both_data.columns and col2 in both_data.columns:
                    diff_mask = both_data[col1] != both_data[col2]
                    if diff_mask.any():
                        diff_count = diff_mask.sum()
                        differences.append({
                            'column': col,
                            'different_values': diff_count,
                            'total_compared': len(both_data),
                            'difference_rate': diff_count / len(both_data)
                        })
            
            result['column_differences'] = differences
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _compare_by_index(self, df1: pd.DataFrame, df2: pd.DataFrame,
                         common_cols: List[str]) -> Dict[str, Any]:
        """基于索引进行比较"""
        result = {
            'comparison_method': 'index'
        }
        
        try:
            # 取较小的行数进行比较
            min_rows = min(len(df1), len(df2))
            
            df1_subset = df1[common_cols].iloc[:min_rows]
            df2_subset = df2[common_cols].iloc[:min_rows]
            
            # 逐列比较
            differences = []
            identical_rows = 0
            
            for i in range(min_rows):
                row_identical = True
                for col in common_cols:
                    val1, val2 = df1_subset.iloc[i][col], df2_subset.iloc[i][col]
                    
                    # 处理NaN值
                    if pd.isna(val1) and pd.isna(val2):
                        continue
                    elif pd.isna(val1) or pd.isna(val2):
                        row_identical = False
                        break
                    elif val1 != val2:
                        row_identical = False
                        break
                
                if row_identical:
                    identical_rows += 1
            
            result.update({
                'compared_rows': min_rows,
                'identical_rows': identical_rows,
                'different_rows': min_rows - identical_rows,
                'rows_only_in_1': max(0, len(df1) - min_rows),
                'rows_only_in_2': max(0, len(df2) - min_rows)
            })
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _compare_statistics(self, df1: pd.DataFrame, df2: pd.DataFrame,
                          name1: str, name2: str) -> Dict[str, Any]:
        """比较统计信息"""
        stats_comparison = {
            'numeric_columns': {},
            'categorical_columns': {},
            'overall_similarity': 0.0
        }
        
        try:
            # 数值列统计比较
            numeric_cols = df1.select_dtypes(include=[np.number]).columns
            common_numeric = [col for col in numeric_cols if col in df2.columns]
            
            for col in common_numeric:
                try:
                    stats1 = df1[col].describe()
                    stats2 = df2[col].describe()
                    
                    # 计算统计量差异
                    stat_diff = {}
                    for stat in ['mean', 'std', 'min', 'max', '25%', '50%', '75%']:
                        if stat in stats1.index and stat in stats2.index:
                            val1, val2 = stats1[stat], stats2[stat]
                            if not (pd.isna(val1) or pd.isna(val2)):
                                diff_pct = abs(val1 - val2) / (abs(val1) + 1e-10) * 100
                                stat_diff[stat] = {
                                    name1: val1,
                                    name2: val2,
                                    'difference_pct': diff_pct
                                }
                    
                    # 进行统计检验
                    try:
                        # 去除NaN值
                        data1 = df1[col].dropna()
                        data2 = df2[col].dropna()
                        
                        if len(data1) > 10 and len(data2) > 10:
                            # Kolmogorov-Smirnov检验
                            ks_stat, ks_pvalue = stats.ks_2samp(data1, data2)
                            stat_diff['ks_test'] = {
                                'statistic': ks_stat,
                                'p_value': ks_pvalue,
                                'significant': ks_pvalue < 0.05
                            }
                    except Exception:
                        pass
                    
                    stats_comparison['numeric_columns'][col] = stat_diff
                    
                except Exception:
                    continue
            
            # 分类列比较
            categorical_cols = df1.select_dtypes(include=['object', 'category']).columns
            common_categorical = [col for col in categorical_cols if col in df2.columns]
            
            for col in common_categorical:
                try:
                    value_counts1 = df1[col].value_counts()
                    value_counts2 = df2[col].value_counts()
                    
                    # 比较唯一值
                    unique1 = set(value_counts1.index)
                    unique2 = set(value_counts2.index)
                    
                    cat_comparison = {
                        'unique_values_1': len(unique1),
                        'unique_values_2': len(unique2),
                        'common_values': len(unique1.intersection(unique2)),
                        'only_in_1': list(unique1 - unique2),
                        'only_in_2': list(unique2 - unique1)
                    }
                    
                    stats_comparison['categorical_columns'][col] = cat_comparison
                    
                except Exception:
                    continue
            
        except Exception as e:
            stats_comparison['error'] = str(e)
        
        return stats_comparison
    
    def _calculate_match_score(self, structural_diff: Dict, content_diff: Dict, 
                              stats_comparison: Dict) -> float:
        """计算匹配得分"""
        score_components = []
        
        # 结构匹配得分 (40%)
        structure_score = 0.0
        if structural_diff.get('columns_match', False):
            structure_score += 0.5
        if structural_diff.get('shape_match', False):
            structure_score += 0.3
        if len(structural_diff.get('dtype_differences', {})) == 0:
            structure_score += 0.2
        
        score_components.append(('structure', structure_score, 0.4))
        
        # 内容匹配得分 (40%)
        content_score = 0.0
        if 'identical_rows' in content_diff and 'compared_rows' in content_diff:
            compared = content_diff['compared_rows']
            if compared > 0:
                content_score = content_diff['identical_rows'] / compared
        
        score_components.append(('content', content_score, 0.4))
        
        # 统计匹配得分 (20%)
        stats_score = 0.0
        numeric_cols = stats_comparison.get('numeric_columns', {})
        if numeric_cols:
            col_scores = []
            for col, stats in numeric_cols.items():
                if 'mean' in stats:
                    mean_diff = stats['mean'].get('difference_pct', 100)
                    col_score = max(0, 1 - mean_diff / 100)
                    col_scores.append(col_score)
            
            if col_scores:
                stats_score = sum(col_scores) / len(col_scores)
        
        score_components.append(('statistics', stats_score, 0.2))
        
        # 计算加权总分
        total_score = sum(score * weight for _, score, weight in score_components)
        
        return min(1.0, max(0.0, total_score))
    
    def _generate_recommendations(self, comparison_result: Dict) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        match_score = comparison_result.get('match_score', 0)
        
        if match_score >= 0.9:
            recommendations.append("数据匹配度很高，质量良好")
        elif match_score >= 0.7:
            recommendations.append("数据匹配度较好，建议检查少量差异")
        elif match_score >= 0.5:
            recommendations.append("数据存在明显差异，需要详细检查")
        else:
            recommendations.append("数据差异很大，建议重新检查数据处理流程")
        
        # 结构建议
        structural = comparison_result.get('structural_differences', {})
        if not structural.get('columns_match', True):
            recommendations.append("列结构不匹配，检查列名和数据源")
        
        if structural.get('dtype_differences'):
            recommendations.append("存在数据类型差异，可能影响计算结果")
        
        # 内容建议
        content = comparison_result.get('content_differences', {})
        if content.get('different_rows', 0) > 0:
            recommendations.append("存在内容差异，建议逐行检查关键字段")
        
        return recommendations


def verify_data_processing_result(original_data: Union[str, pd.DataFrame],
                                processed_data: pd.DataFrame,
                                processing_description: str = "",
                                key_columns: Optional[List[str]] = None) -> Dict[str, Any]:
    """验证数据处理结果
    
    Args:
        original_data: 原始数据（文件路径或DataFrame）
        processed_data: 处理后的数据
        processing_description: 处理过程描述
        key_columns: 关键列名
        
    Returns:
        dict: 验证结果
    """
    verification_engine = DataVerificationEngine()
    
    result = {
        'verification_summary': {},
        'detailed_comparison': {},
        'quality_assessment': {},
        'recommendations': [],
        'processing_info': {
            'description': processing_description,
            'timestamp': pd.Timestamp.now().isoformat()
        }
    }
    
    try:
        # 加载原始数据
        if isinstance(original_data, str):
            from enhanced_excel_helper import smart_read_excel
            read_result = smart_read_excel(original_data)
            if not read_result['success']:
                result['error'] = f"无法读取原始数据: {read_result.get('errors', [])}" 
                return result
            original_df = read_result['dataframe']
        else:
            original_df = original_data
        
        # 执行详细比较
        comparison = verification_engine.compare_dataframes(
            original_df, processed_data, 
            "原始数据", "处理后数据",
            key_columns
        )
        
        result['detailed_comparison'] = comparison
        
        # 生成验证摘要
        summary = {
            'match_score': comparison.get('match_score', 0),
            'data_integrity': 'good' if comparison.get('match_score', 0) > 0.8 else 'needs_review',
            'structural_changes': not comparison.get('structural_differences', {}).get('columns_match', True),
            'content_changes': comparison.get('content_differences', {}).get('different_rows', 0) > 0
        }
        
        result['verification_summary'] = summary
        
        # 质量评估
        quality_assessment = {
            'completeness': _assess_completeness(original_df, processed_data),
            'consistency': _assess_consistency(processed_data),
            'accuracy': _assess_accuracy(comparison),
            'validity': _assess_validity(processed_data)
        }
        
        result['quality_assessment'] = quality_assessment
        
        # 综合建议
        recommendations = comparison.get('recommendations', [])
        if summary['match_score'] < 0.7:
            recommendations.append("建议重新检查数据处理逻辑")
        
        result['recommendations'] = recommendations
        
    except Exception as e:
        result['error'] = str(e)
    
    return result


def _assess_completeness(original_df: pd.DataFrame, processed_df: pd.DataFrame) -> Dict[str, Any]:
    """评估数据完整性"""
    return {
        'row_retention_rate': len(processed_df) / len(original_df) if len(original_df) > 0 else 0,
        'column_retention_rate': len(processed_df.columns) / len(original_df.columns) if len(original_df.columns) > 0 else 0,
        'null_value_rate': processed_df.isnull().sum().sum() / (processed_df.shape[0] * processed_df.shape[1]) if processed_df.size > 0 else 0
    }


def _assess_consistency(df: pd.DataFrame) -> Dict[str, Any]:
    """评估数据一致性"""
    return {
        'duplicate_rate': df.duplicated().sum() / len(df) if len(df) > 0 else 0,
        'data_type_consistency': len(df.dtypes.unique()) / len(df.columns) if len(df.columns) > 0 else 0
    }


def _assess_accuracy(comparison: Dict) -> Dict[str, Any]:
    """评估数据准确性"""
    return {
        'match_score': comparison.get('match_score', 0),
        'statistical_similarity': len(comparison.get('statistical_comparison', {}).get('numeric_columns', {}))
    }


def _assess_validity(df: pd.DataFrame) -> Dict[str, Any]:
    """评估数据有效性"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    validity_issues = 0
    
    for col in numeric_cols:
        if df[col].isin([np.inf, -np.inf]).any():
            validity_issues += 1
    
    return {
        'infinite_values': validity_issues,
        'validity_score': 1 - (validity_issues / len(numeric_cols)) if len(numeric_cols) > 0 else 1
    }