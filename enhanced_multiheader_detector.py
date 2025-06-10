#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强的多级列头检测器
提供更准确的多级列头识别和最优参数推荐
"""

import pandas as pd
import openpyxl
from typing import Dict, Any, List, Optional, Tuple, Union
import re
from collections import Counter
import logging

class EnhancedMultiHeaderDetector:
    """增强的多级列头检测器"""
    
    def __init__(self, file_path: str, sheet_name: Optional[str] = None):
        """
        初始化检测器
        
        Args:
            file_path: Excel文件路径
            sheet_name: 工作表名称
        """
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.workbook = None
        self.sheet = None
        self.raw_data = []
        self.merged_cells_info = []
        
    def __enter__(self):
        """上下文管理器入口"""
        self.workbook = openpyxl.load_workbook(self.file_path, read_only=True)
        self.sheet = self.workbook[self.sheet_name] if self.sheet_name else self.workbook.active
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        if self.workbook:
            self.workbook.close()
    
    def analyze_merged_cells(self) -> List[Dict[str, Any]]:
        """
        分析合并单元格信息
        
        Returns:
            合并单元格信息列表
        """
        merged_info = []
        
        # 重新打开工作簿以获取合并单元格信息
        temp_workbook = openpyxl.load_workbook(self.file_path)
        temp_sheet = temp_workbook[self.sheet_name] if self.sheet_name else temp_workbook.active
        
        for merged_range in temp_sheet.merged_cells.ranges:
            merged_info.append({
                'range': str(merged_range),
                'min_row': merged_range.min_row,
                'max_row': merged_range.max_row,
                'min_col': merged_range.min_col,
                'max_col': merged_range.max_col,
                'span_rows': merged_range.max_row - merged_range.min_row + 1,
                'span_cols': merged_range.max_col - merged_range.min_col + 1
            })
        
        temp_workbook.close()
        return merged_info
    
    def extract_raw_data(self, max_rows: int = 15, max_cols: int = 30) -> List[List[Any]]:
        """
        提取原始数据
        
        Args:
            max_rows: 最大行数
            max_cols: 最大列数
            
        Returns:
            原始数据矩阵
        """
        raw_data = []
        actual_max_row = min(max_rows, self.sheet.max_row)
        actual_max_col = min(max_cols, self.sheet.max_column)
        
        for row_idx in range(1, actual_max_row + 1):
            row_data = []
            for col_idx in range(1, actual_max_col + 1):
                cell = self.sheet.cell(row=row_idx, column=col_idx)
                row_data.append(cell.value)
            raw_data.append(row_data)
        
        return raw_data
    
    def detect_empty_rows(self, data: List[List[Any]]) -> List[int]:
        """
        检测空行
        
        Args:
            data: 原始数据矩阵
            
        Returns:
            空行索引列表
        """
        empty_rows = []
        
        for i, row in enumerate(data):
            if all(cell is None or str(cell).strip() == '' for cell in row):
                empty_rows.append(i)
        
        return empty_rows
    
    def analyze_row_content(self, row: List[Any]) -> Dict[str, Any]:
        """
        分析行内容特征
        
        Args:
            row: 行数据
            
        Returns:
            行特征分析结果
        """
        non_empty_cells = [cell for cell in row if cell is not None and str(cell).strip()]
        
        if not non_empty_cells:
            return {
                'is_empty': True,
                'non_empty_count': 0,
                'text_count': 0,
                'numeric_count': 0,
                'unique_count': 0,
                'content_types': [],
                'has_repeated_values': False
            }
        
        text_count = 0
        numeric_count = 0
        content_types = []
        
        for cell in non_empty_cells:
            cell_str = str(cell).strip()
            if cell_str.replace('.', '').replace('-', '').isdigit():
                numeric_count += 1
                content_types.append('numeric')
            elif isinstance(cell, (int, float)):
                numeric_count += 1
                content_types.append('numeric')
            else:
                text_count += 1
                content_types.append('text')
        
        # 检测重复值（可能表示合并单元格的效果）
        value_counts = Counter(str(cell).strip() for cell in non_empty_cells)
        has_repeated_values = any(count > 1 for count in value_counts.values())
        
        return {
            'is_empty': False,
            'non_empty_count': len(non_empty_cells),
            'text_count': text_count,
            'numeric_count': numeric_count,
            'unique_count': len(set(str(cell).strip() for cell in non_empty_cells)),
            'content_types': content_types,
            'has_repeated_values': has_repeated_values,
            'text_ratio': text_count / len(non_empty_cells) if non_empty_cells else 0
        }
    
    def detect_header_candidates(self, data: List[List[Any]]) -> List[Dict[str, Any]]:
        """
        检测标题行候选
        
        Args:
            data: 原始数据矩阵
            
        Returns:
            标题行候选信息列表
        """
        candidates = []
        
        for i, row in enumerate(data):
            analysis = self.analyze_row_content(row)
            
            # 标题行的特征：
            # 1. 非空单元格数量合理（至少2个）
            # 2. 主要包含文本内容
            # 3. 唯一值较多（不是数据行）
            if (not analysis['is_empty'] and 
                analysis['non_empty_count'] >= 2 and
                analysis['text_ratio'] >= 0.5):
                
                candidates.append({
                    'row_index': i,
                    'analysis': analysis,
                    'is_likely_header': True,
                    'confidence': self._calculate_header_confidence(analysis)
                })
        
        return candidates
    
    def _calculate_header_confidence(self, analysis: Dict[str, Any]) -> float:
        """
        计算标题行置信度
        
        Args:
            analysis: 行分析结果
            
        Returns:
            置信度分数 (0-1)
        """
        confidence = 0.0
        
        # 文本比例越高，越可能是标题
        confidence += analysis['text_ratio'] * 0.4
        
        # 非空单元格数量适中
        if 2 <= analysis['non_empty_count'] <= 20:
            confidence += 0.3
        
        # 唯一值比例高
        if analysis['non_empty_count'] > 0:
            unique_ratio = analysis['unique_count'] / analysis['non_empty_count']
            confidence += unique_ratio * 0.3
        
        return min(confidence, 1.0)
    
    def detect_multi_level_structure(self, header_candidates: List[Dict[str, Any]], 
                                   merged_cells: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        检测多级列头结构
        
        Args:
            header_candidates: 标题行候选
            merged_cells: 合并单元格信息
            
        Returns:
            多级结构检测结果
        """
        if len(header_candidates) < 2:
            return {
                'is_multi_level': False,
                'confidence': 0.0,
                'structure_type': 'single_level',
                'recommended_header': header_candidates[0]['row_index'] if header_candidates else 0
            }
        
        # 检查是否有相邻的标题行
        adjacent_pairs = []
        for i in range(len(header_candidates) - 1):
            curr_row = header_candidates[i]['row_index']
            next_row = header_candidates[i + 1]['row_index']
            if next_row - curr_row <= 2:  # 允许中间有一行空行
                adjacent_pairs.append((i, i + 1))
        
        if not adjacent_pairs:
            return {
                'is_multi_level': False,
                'confidence': 0.0,
                'structure_type': 'separated_headers',
                'recommended_header': header_candidates[-1]['row_index']
            }
        
        # 分析最有希望的相邻对
        best_pair = None
        best_confidence = 0.0
        
        for pair_idx, (i, j) in enumerate(adjacent_pairs):
            row1_idx = header_candidates[i]['row_index']
            row2_idx = header_candidates[j]['row_index']
            
            # 检查层次关系
            hierarchy_confidence = self._analyze_hierarchy_relationship(
                self.raw_data[row1_idx], 
                self.raw_data[row2_idx],
                merged_cells,
                row1_idx + 1,  # 转换为1基索引
                row2_idx + 1
            )
            
            if hierarchy_confidence > best_confidence:
                best_confidence = hierarchy_confidence
                best_pair = (row1_idx, row2_idx)
        
        # 判断是否为真正的多级结构
        is_multi_level = best_confidence >= 0.6
        
        if is_multi_level and best_pair:
            return {
                'is_multi_level': True,
                'confidence': best_confidence,
                'structure_type': 'true_multi_level',
                'header_rows': list(best_pair),
                'recommended_header': list(best_pair)
            }
        else:
            return {
                'is_multi_level': False,
                'confidence': best_confidence,
                'structure_type': 'pseudo_multi_level',
                'recommended_header': header_candidates[-1]['row_index']
            }
    
    def _analyze_hierarchy_relationship(self, row1: List[Any], row2: List[Any], 
                                      merged_cells: List[Dict[str, Any]],
                                      row1_num: int, row2_num: int) -> float:
        """
        分析两行之间的层次关系
        
        Args:
            row1: 第一行数据
            row2: 第二行数据
            merged_cells: 合并单元格信息
            row1_num: 第一行行号（1基索引）
            row2_num: 第二行行号（1基索引）
            
        Returns:
            层次关系置信度 (0-1)
        """
        confidence = 0.0
        
        # 分析内容特征
        # 确保传递的是列表而不是字典
        if isinstance(row1, dict):
            row1 = list(row1.values()) if row1 else []
        if isinstance(row2, dict):
            row2 = list(row2.values()) if row2 else []
            
        row1_analysis = self.analyze_row_content(row1)
        row2_analysis = self.analyze_row_content(row2)
        
        # 检查是否有合并单元格跨越这两行
        has_spanning_merges = any(
            merge['min_row'] <= row1_num <= merge['max_row'] and
            merge['min_row'] <= row2_num <= merge['max_row']
            for merge in merged_cells
        )
        
        if has_spanning_merges:
            confidence += 0.4
        
        # 检查第一行是否有更少的唯一值（表示更高层次的分类）
        if (row1_analysis['unique_count'] < row2_analysis['unique_count'] and
            row1_analysis['unique_count'] > 0):
            confidence += 0.3
        
        # 检查第二行是否更详细（更多非空单元格）
        if row2_analysis['non_empty_count'] > row1_analysis['non_empty_count']:
            confidence += 0.2
        
        # 检查重复值模式（第一行可能有重复值表示分组）
        if row1_analysis['has_repeated_values'] and not row2_analysis['has_repeated_values']:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def suggest_optimal_parameters(self) -> Dict[str, Any]:
        """
        建议最优读取参数
        
        Returns:
            参数建议结果
        """
        # 提取数据和分析结构
        self.raw_data = self.extract_raw_data()
        merged_cells = self.analyze_merged_cells()
        empty_rows = self.detect_empty_rows(self.raw_data)
        header_candidates = self.detect_header_candidates(self.raw_data)
        
        # 检测多级结构
        multi_level_result = self.detect_multi_level_structure(header_candidates, merged_cells)
        
        # 构建建议
        suggestions = {
            "recommended_params": {},
            "analysis": {
                "empty_rows": empty_rows,
                "header_candidates": [c['row_index'] for c in header_candidates],
                "merged_cells_count": len(merged_cells),
                "multi_level_header_detected": multi_level_result['is_multi_level'],
                "structure_type": multi_level_result['structure_type'],
                "confidence": multi_level_result['confidence']
            },
            "warnings": [],
            "tips": []
        }
        
        # 处理skiprows
        if empty_rows and empty_rows[0] == 0:
            consecutive_empty = 0
            for i in empty_rows:
                if i == consecutive_empty:
                    consecutive_empty += 1
                else:
                    break
            if consecutive_empty > 0:
                suggestions["recommended_params"]["skiprows"] = consecutive_empty
                suggestions["tips"].append(f"检测到前{consecutive_empty}行为空行")
        
        # 处理header参数
        if multi_level_result['is_multi_level']:
            # 真正的多级列头
            header_rows = multi_level_result['header_rows']
            # 调整skiprows影响
            if "skiprows" in suggestions["recommended_params"]:
                skiprows = suggestions["recommended_params"]["skiprows"]
                adjusted_headers = [max(0, h - skiprows) for h in header_rows]
            else:
                adjusted_headers = header_rows
            
            suggestions["recommended_params"]["header"] = adjusted_headers
            suggestions["tips"].append(f"检测到多级列头结构，置信度: {multi_level_result['confidence']:.2f}")
            suggestions["warnings"].append("多级列头将创建MultiIndex，可能需要特殊处理")
        else:
            # 单级列头
            recommended_header = multi_level_result['recommended_header']
            if "skiprows" in suggestions["recommended_params"]:
                skiprows = suggestions["recommended_params"]["skiprows"]
                adjusted_header = max(0, recommended_header - skiprows)
            else:
                adjusted_header = recommended_header
            
            suggestions["recommended_params"]["header"] = adjusted_header
            suggestions["tips"].append(f"使用第{recommended_header + 1}行作为列头")
        
        # 添加额外建议
        if merged_cells:
            suggestions["warnings"].append(f"检测到{len(merged_cells)}个合并单元格，可能影响数据读取")
        
        # 验证参数
        self._validate_parameters(suggestions)
        
        return suggestions
    
    def _validate_parameters(self, suggestions: Dict[str, Any]) -> None:
        """
        验证参数的有效性
        
        Args:
            suggestions: 参数建议字典
        """
        try:
            # 尝试用建议的参数读取少量数据
            test_params = suggestions["recommended_params"].copy()
            test_params["nrows"] = 3
            
            test_df = pd.read_excel(self.file_path, sheet_name=self.sheet_name, **test_params)
            
            # 检查结果质量
            unnamed_cols = [col for col in test_df.columns if 'Unnamed' in str(col)]
            if unnamed_cols:
                suggestions["warnings"].append(f"参数验证发现{len(unnamed_cols)}个未命名列")
            
            if len(test_df) == 0:
                suggestions["warnings"].append("参数验证发现无数据行，可能需要调整header参数")
            
        except Exception as e:
            suggestions["warnings"].append(f"参数验证失败: {str(e)}")

def enhanced_suggest_excel_read_parameters(file_path: str, sheet_name: str = None) -> Dict[str, Any]:
    """
    增强的Excel读取参数建议函数
    
    Args:
        file_path: Excel文件路径
        sheet_name: 工作表名称
        
    Returns:
        参数建议结果
    """
    try:
        with EnhancedMultiHeaderDetector(file_path, sheet_name) as detector:
            return detector.suggest_optimal_parameters()
    except Exception as e:
        # 回退到基本参数
        return {
            "recommended_params": {"header": 0},
            "analysis": {
                "multi_level_header_detected": False,
                "error": str(e)
            },
            "warnings": [f"增强检测失败，使用默认参数: {str(e)}"],
            "tips": ["建议手动检查文件格式"]
        }