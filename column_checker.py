#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
列名检查和匹配工具
创建日期: 2025-06-18
功能: 提供Excel文件列名检查、匹配和建议功能
"""

import pandas as pd
import difflib
import re
from typing import List, Dict, Any, Optional


class ColumnChecker:
    """Excel列名检查和匹配工具类"""
    
    def __init__(self):
        # 中文列名常见变体映射
        self.chinese_variants = {
            '消耗日期': ['消费日期', '使用日期', '支出日期', '花费日期', '消耗时间', '消费时间'],
            '消费日期': ['消耗日期', '使用日期', '支出日期', '花费日期', '消费时间', '消耗时间'],
            '日期': ['时间', 'Date', 'date', '创建日期', '更新日期', '记录日期', '发生日期'],
            '金额': ['数量', '价格', '费用', '成本', 'Amount', 'amount', '总额', '金钱'],
            '名称': ['姓名', '品名', '项目', 'Name', 'name', '标题', '名字'],
            '类型': ['分类', '种类', 'Type', 'type', '类别', '类型'],
            '数量': ['金额', '个数', '件数', 'Quantity', 'quantity', '总数'],
            '备注': ['说明', '描述', 'Note', 'note', 'Remark', 'remark', '注释']
        }
        
        # 英文列名常见变体
        self.english_variants = {
            'date': ['time', 'datetime', 'timestamp', 'created_at', 'updated_at'],
            'amount': ['price', 'cost', 'value', 'total', 'sum'],
            'name': ['title', 'label', 'description', 'item'],
            'type': ['category', 'class', 'kind', 'group'],
            'quantity': ['count', 'number', 'amount', 'total']
        }
    
    def check_file_columns(self, file_path: str, sheet_name: Optional[str] = None) -> Dict[str, Any]:
        """检查Excel文件的列名信息
        
        Args:
            file_path: Excel文件路径
            sheet_name: 工作表名称（可选）
            
        Returns:
            dict: 包含列名信息的字典
        """
        try:
            # 读取Excel文件
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                df = pd.read_excel(file_path)
            
            columns = list(df.columns)
            
            return {
                'success': True,
                'columns': columns,
                'column_count': len(columns),
                'data_shape': df.shape,
                'column_types': df.dtypes.to_dict(),
                'sample_data': df.head(3).to_dict(),
                'has_unnamed_columns': any('Unnamed' in str(col) for col in columns),
                'duplicate_columns': self._find_duplicate_columns(columns)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'suggestion': '请检查文件路径和格式是否正确'
            }
    
    def match_column(self, target_column: str, available_columns: List[str]) -> Dict[str, Any]:
        """智能列名匹配
        
        Args:
            target_column: 目标列名
            available_columns: 可用的列名列表
            
        Returns:
            dict: 匹配结果和建议
        """
        result = {
            'target': target_column,
            'exact_match': None,
            'case_insensitive_match': None,
            'normalized_matches': [],
            'fuzzy_matches': [],
            'variant_matches': [],
            'suggestions': [],
            'confidence_score': 0.0
        }
        
        if not available_columns:
            result['suggestions'].append('没有可用的列名进行匹配')
            return result
        
        # 1. 精确匹配
        if target_column in available_columns:
            result['exact_match'] = target_column
            result['confidence_score'] = 1.0
            result['suggestions'].append(f"找到精确匹配: '{target_column}'")
            return result
        
        # 2. 大小写不敏感匹配
        target_lower = target_column.lower()
        for col in available_columns:
            if col.lower() == target_lower:
                result['case_insensitive_match'] = col
                result['confidence_score'] = 0.95
                result['suggestions'].append(f"找到大小写不同的匹配: '{col}'")
                return result
        
        # 3. 标准化匹配（去除空格、下划线、连字符）
        target_normalized = re.sub(r'[\s_-]', '', target_column.lower())
        for col in available_columns:
            col_normalized = re.sub(r'[\s_-]', '', col.lower())
            if col_normalized == target_normalized:
                result['normalized_matches'].append(col)
        
        if result['normalized_matches']:
            result['confidence_score'] = 0.9
            result['suggestions'].append(f"标准化匹配: {', '.join(result['normalized_matches'])}")
        
        # 4. 模糊匹配
        fuzzy_matches = difflib.get_close_matches(
            target_column, available_columns, n=5, cutoff=0.6
        )
        result['fuzzy_matches'] = fuzzy_matches
        
        if fuzzy_matches and not result['normalized_matches']:
            result['confidence_score'] = 0.8
            result['suggestions'].append(f"相似列名: {', '.join(fuzzy_matches)}")
        
        # 5. 变体匹配
        variant_matches = self._find_variant_matches(target_column, available_columns)
        result['variant_matches'] = variant_matches
        
        if variant_matches:
            result['confidence_score'] = max(result['confidence_score'], 0.85)
            result['suggestions'].extend([f"发现变体匹配: '{match}'" for match in variant_matches])
        
        # 6. 生成最终建议
        self._generate_suggestions(result, available_columns)
        
        return result
    
    def match_column_with_dataframe(self, target_column: str, df: pd.DataFrame) -> Dict[str, Any]:
        """基于DataFrame进行智能列名匹配，包含增强的列头检测算法
        
        Args:
            target_column: 目标列名
            df: 数据框
            
        Returns:
            dict: 匹配结果和建议
        """
        # 首先使用原有的列名匹配逻辑
        available_columns = list(df.columns)
        result = self.match_column(target_column, available_columns)
        
        # 如果没有找到满意的匹配，尝试使用增强的列头检测算法
        if result['confidence_score'] < 0.8:
            header_analysis = self._analyze_potential_headers(df, target_column)
            if header_analysis['found_potential_header']:
                result['header_analysis'] = header_analysis
                result['confidence_score'] = max(result['confidence_score'], header_analysis['confidence'])
                result['suggestions'].extend(header_analysis['suggestions'])
        
        return result
    
    def _analyze_potential_headers(self, df: pd.DataFrame, target_column: str) -> Dict[str, Any]:
        """分析数据框中的潜在列头行
        
        实现规则：
        1. 同一行中，当所有列不为空时，最小行序号对应行的单元格为对应列的列头名称
        2. 优先选择整个表格数据的前5行进行匹配确认列头
        3. 当前5行不满足规则1要求时，5行一组向后排查按照规则1进行匹配
        
        Args:
            df: 数据框
            target_column: 目标列名
            
        Returns:
            dict: 列头分析结果
        """
        result = {
            'found_potential_header': False,
            'header_row_index': -1,
            'potential_matches': [],
            'confidence': 0.0,
            'suggestions': []
        }
        
        if df.empty:
            return result
        
        # 第一阶段：检查前5行
        header_row = self._find_complete_row_in_range(df, 0, min(5, len(df)))
        
        # 第二阶段：如果前5行没有找到，以5行为组向后排查
        if header_row == -1:
            for start_row in range(5, len(df), 5):
                end_row = min(start_row + 5, len(df))
                header_row = self._find_complete_row_in_range(df, start_row, end_row)
                if header_row != -1:
                    break
        
        if header_row != -1:
            # 分析找到的列头行
            header_values = df.iloc[header_row].astype(str).tolist()
            matches = self._find_header_matches(target_column, header_values)
            
            if matches:
                result['found_potential_header'] = True
                result['header_row_index'] = header_row
                result['potential_matches'] = matches
                result['confidence'] = max([match['similarity'] for match in matches])
                
                # 生成建议
                best_match = max(matches, key=lambda x: x['similarity'])
                result['suggestions'].append(
                    f"在第{header_row + 1}行发现潜在列头：'{best_match['header_value']}' "
                    f"(相似度: {best_match['similarity']:.2f})"
                )
                result['suggestions'].append(
                    f"建议将第{header_row + 1}行设为列头，然后使用列索引{best_match['column_index']}访问数据"
                )
        
        return result
    
    def _find_complete_row_in_range(self, df: pd.DataFrame, start_row: int, end_row: int) -> int:
        """在指定范围内查找所有列都不为空的最小行序号
        
        Args:
            df: 数据框
            start_row: 开始行索引
            end_row: 结束行索引（不包含）
            
        Returns:
            int: 找到的行索引，如果没找到返回-1
        """
        for i in range(start_row, end_row):
            if i >= len(df):
                break
            
            # 检查该行是否所有列都不为空
            row_data = df.iloc[i]
            if self._is_complete_row(row_data):
                return i
        
        return -1
    
    def _is_complete_row(self, row_data: pd.Series) -> bool:
        """检查行数据是否完整（所有列都不为空）
        
        Args:
            row_data: 行数据
            
        Returns:
            bool: 是否为完整行
        """
        # 检查是否有空值、NaN或空字符串
        for value in row_data:
            if pd.isna(value) or str(value).strip() == '' or str(value).lower() in ['nan', 'none', 'null']:
                return False
        return True
    
    def _find_header_matches(self, target_column: str, header_values: List[str]) -> List[Dict[str, Any]]:
        """在列头值中查找与目标列名的匹配
        
        Args:
            target_column: 目标列名
            header_values: 列头值列表
            
        Returns:
            List[Dict]: 匹配结果列表
        """
        matches = []
        
        for i, header_value in enumerate(header_values):
            # 计算相似度
            similarity = self._calculate_similarity(target_column, str(header_value))
            
            # 如果相似度足够高，添加到匹配结果
            if similarity >= 0.6:  # 设置阈值
                matches.append({
                    'column_index': i,
                    'header_value': str(header_value),
                    'similarity': similarity
                })
        
        # 按相似度排序
        matches.sort(key=lambda x: x['similarity'], reverse=True)
        return matches
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """计算两个字符串的相似度
        
        Args:
            str1: 字符串1
            str2: 字符串2
            
        Returns:
            float: 相似度分数 (0-1)
        """
        # 使用多种方法计算相似度，取最高值
        similarities = []
        
        # 1. 直接相似度
        similarities.append(difflib.SequenceMatcher(None, str1, str2).ratio())
        
        # 2. 大小写不敏感相似度
        similarities.append(difflib.SequenceMatcher(None, str1.lower(), str2.lower()).ratio())
        
        # 3. 标准化后相似度（去除空格和特殊字符）
        normalized_str1 = re.sub(r'[\s_-]', '', str1.lower())
        normalized_str2 = re.sub(r'[\s_-]', '', str2.lower())
        similarities.append(difflib.SequenceMatcher(None, normalized_str1, normalized_str2).ratio())
        
        # 4. 检查变体匹配
        if self._is_variant_match(str1, str2):
            similarities.append(0.9)
        
        return max(similarities)
    
    def _is_variant_match(self, str1: str, str2: str) -> bool:
        """检查两个字符串是否为变体匹配
        
        Args:
            str1: 字符串1
            str2: 字符串2
            
        Returns:
            bool: 是否为变体匹配
        """
        # 检查中文变体
        for key, variants in self.chinese_variants.items():
            if (str1 == key and str2 in variants) or (str2 == key and str1 in variants):
                return True
            if str1 in variants and str2 in variants:
                return True
        
        # 检查英文变体
        str1_lower = str1.lower()
        str2_lower = str2.lower()
        for key, variants in self.english_variants.items():
            if (str1_lower == key and str2_lower in variants) or (str2_lower == key and str1_lower in variants):
                return True
            if str1_lower in variants and str2_lower in variants:
                return True
        
        return False
    
    def _find_duplicate_columns(self, columns: List[str]) -> List[str]:
        """查找重复的列名"""
        seen = set()
        duplicates = set()
        
        for col in columns:
            if col in seen:
                duplicates.add(col)
            else:
                seen.add(col)
        
        return list(duplicates)
    
    def _find_variant_matches(self, target: str, available: List[str]) -> List[str]:
        """查找变体匹配"""
        matches = []
        target_lower = target.lower()
        
        # 检查中文变体
        if target in self.chinese_variants:
            for variant in self.chinese_variants[target]:
                if variant in available:
                    matches.append(variant)
        
        # 检查英文变体
        if target_lower in self.english_variants:
            for variant in self.english_variants[target_lower]:
                for col in available:
                    if variant.lower() == col.lower():
                        matches.append(col)
        
        # 反向检查：目标是否是某个变体
        for key, variants in self.chinese_variants.items():
            if target in variants and key in available:
                matches.append(key)
        
        for key, variants in self.english_variants.items():
            if target_lower in [v.lower() for v in variants]:
                for col in available:
                    if key.lower() == col.lower():
                        matches.append(col)
        
        return list(set(matches))  # 去重
    
    def _generate_suggestions(self, result: Dict[str, Any], available_columns: List[str]):
        """生成建议"""
        target = result['target']
        
        # 根据匹配结果生成建议
        if result['normalized_matches']:
            best_match = result['normalized_matches'][0]
            result['suggestions'].append(f"建议使用: df['{best_match}']")
        elif result['fuzzy_matches']:
            best_match = result['fuzzy_matches'][0]
            result['suggestions'].append(f"最佳匹配建议: df['{best_match}']")
        elif result['variant_matches']:
            best_match = result['variant_matches'][0]
            result['suggestions'].append(f"变体匹配建议: df['{best_match}']")
        
        # 通用建议
        result['suggestions'].append("检查列名的拼写、大小写和空格")
        result['suggestions'].append(f"所有可用列名: {', '.join(available_columns)}")
        
        # 如果没有找到任何匹配
        if (not result['normalized_matches'] and 
            not result['fuzzy_matches'] and 
            not result['variant_matches']):
            result['suggestions'].append("未找到相似列名，请检查Excel文件的列标题")
            result['suggestions'].append("建议使用 df.columns.tolist() 查看所有列名")
    
    def generate_code_suggestions(self, target_column: str, match_result: Dict[str, Any]) -> List[str]:
        """生成代码建议"""
        suggestions = []
        
        # 查看列名的代码
        suggestions.append("# 查看所有列名")
        suggestions.append("print('可用列名:', df.columns.tolist())")
        suggestions.append("")
        
        # 根据匹配结果生成具体建议
        if match_result['exact_match']:
            suggestions.append(f"# 使用精确匹配")
            suggestions.append(f"df['{match_result['exact_match']}']")
        elif match_result['case_insensitive_match']:
            suggestions.append(f"# 使用大小写匹配")
            suggestions.append(f"df['{match_result['case_insensitive_match']}']")
        elif match_result['normalized_matches']:
            best_match = match_result['normalized_matches'][0]
            suggestions.append(f"# 使用标准化匹配")
            suggestions.append(f"df['{best_match}']")
        elif match_result['fuzzy_matches']:
            best_match = match_result['fuzzy_matches'][0]
            suggestions.append(f"# 使用模糊匹配")
            suggestions.append(f"df['{best_match}']")
        elif match_result['variant_matches']:
            best_match = match_result['variant_matches'][0]
            suggestions.append(f"# 使用变体匹配")
            suggestions.append(f"df['{best_match}']")
        else:
            suggestions.append(f"# 原始代码（需要修正列名）")
            suggestions.append(f"# df['{target_column}']  # 此列名不存在")
        
        return suggestions


# 便捷函数
def check_columns(file_path: str, sheet_name: Optional[str] = None) -> Dict[str, Any]:
    """检查Excel文件列名的便捷函数"""
    checker = ColumnChecker()
    return checker.check_file_columns(file_path, sheet_name)


def match_column(target_column: str, available_columns: List[str]) -> Dict[str, Any]:
    """列名匹配的便捷函数"""
    checker = ColumnChecker()
    return checker.match_column(target_column, available_columns)


def match_column_with_dataframe(target_column: str, df: pd.DataFrame) -> Dict[str, Any]:
    """基于DataFrame进行智能列名匹配的便捷函数，包含增强的列头检测算法"""
    checker = ColumnChecker()
    return checker.match_column_with_dataframe(target_column, df)


if __name__ == "__main__":
    # 测试代码
    checker = ColumnChecker()
    
    # 测试原有列名匹配功能
    print("=== 测试原有列名匹配功能 ===")
    test_columns = ['消费日期', '金额', '商品名称', '类别', '备注']
    result = checker.match_column('消耗日期', test_columns)
    
    print("匹配结果:")
    print(f"目标列名: {result['target']}")
    print(f"置信度: {result['confidence_score']}")
    print("建议:")
    for suggestion in result['suggestions']:
        print(f"  - {suggestion}")
    
    print("\n=== 测试增强的列头检测算法 ===")
    
    # 创建测试数据：模拟Excel文件中列头不在第一行的情况
    test_data = {
        'A': ['', '', '日期', '2023-01-01', '2023-01-02', '2023-01-03'],
        'B': ['', '', '金额', 100, 150, 200],
        'C': ['', '', '类别', '餐饮', '交通', '购物'],
        'D': ['', '', '备注', '午餐', '地铁', '衣服']
    }
    test_df = pd.DataFrame(test_data)
    
    print("测试数据框:")
    print(test_df)
    print()
    
    # 测试新的列头检测功能
    targets = ['消耗日期', '金额', '分类', '说明']
    
    for target in targets:
        print(f"--- 测试目标列名: '{target}' ---")
        result = checker.match_column_with_dataframe(target, test_df)
        
        print(f"置信度: {result['confidence_score']:.2f}")
        print("建议:")
        for suggestion in result['suggestions']:
            print(f"  - {suggestion}")
        
        if 'header_analysis' in result:
            header_info = result['header_analysis']
            print(f"列头分析: 在第{header_info['header_row_index'] + 1}行发现潜在列头")
            if header_info['potential_matches']:
                best_match = header_info['potential_matches'][0]
                print(f"最佳匹配: '{best_match['header_value']}' (列索引: {best_match['column_index']}, 相似度: {best_match['similarity']:.2f})")
        print()
    
    print("=== 测试完整行检测功能 ===")
    
    # 创建另一个测试数据：第1行有完整数据
    test_data2 = {
        'A': ['消费日期', '2023-01-01', '2023-01-02'],
        'B': ['金额', 100, 150],
        'C': ['类别', '餐饮', '交通'],
        'D': ['备注', '午餐', '地铁']
    }
    test_df2 = pd.DataFrame(test_data2)
    
    print("测试数据框2 (第1行为完整列头):")
    print(test_df2)
    print()
    
    result2 = checker.match_column_with_dataframe('消耗日期', test_df2)
    print("匹配结果:")
    print(f"置信度: {result2['confidence_score']:.2f}")
    for suggestion in result2['suggestions']:
        print(f"  - {suggestion}")
    
    if 'header_analysis' in result2:
        header_info = result2['header_analysis']
        print(f"列头分析: 在第{header_info['header_row_index'] + 1}行发现潜在列头")
        if header_info['potential_matches']:
            best_match = header_info['potential_matches'][0]
            print(f"最佳匹配: '{best_match['header_value']}' (列索引: {best_match['column_index']}, 相似度: {best_match['similarity']:.2f})")
    
    print("\n=== 测试便捷函数 ===")
    result3 = match_column_with_dataframe('日期', test_df)
    print(f"便捷函数测试结果置信度: {result3['confidence_score']:.2f}")
    print("便捷函数建议:")
    for suggestion in result3['suggestions']:
        print(f"  - {suggestion}")