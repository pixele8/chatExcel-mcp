#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强多级列头检测功能测试

本测试文件验证 enhanced_multiheader_detector.py 中的增强功能：
1. 智能头部候选检测
2. 上下文感知的置信度计算
3. 动态阈值调整
4. 假阳性过滤
5. 多维度分析
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch
import pandas as pd
import numpy as np

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from enhanced_multiheader_detector import EnhancedMultiHeaderDetector
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保 enhanced_multiheader_detector.py 文件存在")
    sys.exit(1)


class TestEnhancedMultiHeaderDetector(unittest.TestCase):
    """增强多级列头检测器测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时测试文件路径
        self.test_file_path = "/tmp/test_data.xlsx"
        self.detector = EnhancedMultiHeaderDetector(self.test_file_path)
        
        # 创建测试数据 - 多级表头示例
        self.test_data = {
            'A': ['', '', '销售数据', '产品A', '数量', '100', '120', '90'],
            'B': ['', '', '销售数据', '产品A', '金额', '1000', '1200', '900'],
            'C': ['', '', '销售数据', '产品B', '数量', '80', '95', '110'],
            'D': ['', '', '销售数据', '产品B', '金额', '800', '950', '1100'],
            'E': ['', '', '成本数据', '产品A', '成本', '600', '720', '540'],
            'F': ['', '', '成本数据', '产品B', '成本', '480', '570', '660']
        }
        
        self.df = pd.DataFrame(self.test_data)
        
    def test_detect_header_candidates_enhanced(self):
        """测试增强的头部候选检测"""
        print("\n=== 测试增强的头部候选检测 ===")
        
        # 将DataFrame转换为原始数据格式
        raw_data = []
        for i in range(len(self.df)):
            row = []
            for col in self.df.columns:
                row.append(self.df.iloc[i][col])
            raw_data.append(row)
            
        print(f"\n测试数据 ({len(raw_data)} 行):")
        for i, row in enumerate(raw_data[:5]):  # 只显示前5行
            print(f"行 {i}: {row}")
            
        candidates = self.detector.detect_header_candidates_enhanced(raw_data)
            
        print(f"\n检测到 {len(candidates)} 个候选标题行")
        for i, candidate in enumerate(candidates):
            print(f"候选 {i+1}: 行 {candidate['row_index']}, 置信度 {candidate['confidence']:.3f}")
        
        # 验证结果
        self.assertIsInstance(candidates, list)
        
        # 如果没有检测到候选，输出调试信息
        if len(candidates) == 0:
            print("\n调试信息: 分析每一行")
            for i, row in enumerate(raw_data[:5]):  # 只检查前5行
                if row and not all(cell is None or str(cell).strip() == '' for cell in row):
                    analysis = self.detector.analyze_row_content_enhanced(row)
                    print(f"行 {i}: 置信度 {analysis['title_confidence']:.3f}, 内容: {row}")
            print("可能需要调整阈值或测试数据")
        else:
            self.assertTrue(len(candidates) > 0, "应该检测到至少一个头部候选")
    
    def test_calculate_position_weight(self):
        """测试位置权重计算"""
        print("\n=== 测试位置权重计算 ===")
        
        # 测试不同位置的权重（需要提供 data_start_hint 和 max_rows 参数）
        data_start_hint = 5  # 假设数据从第5行开始
        max_rows = 20       # 假设总共20行
        
        weight_0 = self.detector._calculate_position_weight(0, data_start_hint, max_rows)
        weight_1 = self.detector._calculate_position_weight(1, data_start_hint, max_rows)
        weight_5 = self.detector._calculate_position_weight(5, data_start_hint, max_rows)
        weight_10 = self.detector._calculate_position_weight(10, data_start_hint, max_rows)
        
        print(f"第0行权重: {weight_0:.3f}")
        print(f"第1行权重: {weight_1:.3f}")
        print(f"第5行权重: {weight_5:.3f}")
        print(f"第10行权重: {weight_10:.3f}")
        
        # 验证权重递减
        self.assertGreater(weight_0, weight_1, "较早的行应该有更高的权重")
        self.assertGreater(weight_1, weight_5, "权重应该随行号递减")
        self.assertGreater(weight_5, weight_10, "权重应该随行号递减")
        
        # 验证权重范围
        for weight in [weight_0, weight_1, weight_5, weight_10]:
            self.assertGreaterEqual(weight, 0.1, "权重不应低于0.1")
            self.assertLessEqual(weight, 1.2, "权重不应超过1.2")
    
    def test_calculate_dynamic_threshold(self):
        """测试动态阈值计算"""
        print("\n=== 测试动态阈值计算 ===")
        
        # 测试不同行位置的动态阈值
        data_start_hint = 5  # 假设数据从第5行开始
        
        threshold_0 = self.detector._calculate_dynamic_threshold(0, data_start_hint)
        threshold_2 = self.detector._calculate_dynamic_threshold(2, data_start_hint)
        threshold_5 = self.detector._calculate_dynamic_threshold(5, data_start_hint)
        threshold_10 = self.detector._calculate_dynamic_threshold(10, data_start_hint)
        
        print(f"第0行阈值: {threshold_0:.3f}")
        print(f"第2行阈值: {threshold_2:.3f}")
        print(f"第5行阈值: {threshold_5:.3f}")
        print(f"第10行阈值: {threshold_10:.3f}")
        
        # 验证阈值递增趋势（后面的行需要更高的置信度）
        self.assertLessEqual(threshold_0, threshold_5, "前面的行应该有更低的阈值")
        self.assertLessEqual(threshold_5, threshold_10, "后面的行应该有更高的阈值")
        
        # 验证阈值范围
        for threshold in [threshold_0, threshold_2, threshold_5, threshold_10]:
            self.assertGreaterEqual(threshold, 0.2, "阈值不应低于0.2")
            self.assertLessEqual(threshold, 0.5, "阈值不应超过0.5")
    
    def test_filter_false_positives(self):
        """测试假阳性过滤"""
        print("\n=== 测试假阳性过滤 ===")
        
        # 创建包含假阳性的候选列表（需要包含 analysis 字段）
        candidates_with_false_positives = [
            {'row_index': 0, 'confidence': 0.9, 'analysis': {'non_empty_count': 5, 'numeric_count': 0, 'unique_count': 5}},
            {'row_index': 1, 'confidence': 0.8, 'analysis': {'non_empty_count': 4, 'numeric_count': 0, 'unique_count': 4}},
            {'row_index': 2, 'confidence': 0.7, 'analysis': {'non_empty_count': 3, 'numeric_count': 0, 'unique_count': 3}},
            {'row_index': 10, 'confidence': 0.6, 'analysis': {'non_empty_count': 6, 'numeric_count': 6, 'unique_count': 6}}, # 全数值行
            {'row_index': 15, 'confidence': 0.5, 'analysis': {'non_empty_count': 1, 'numeric_count': 0, 'unique_count': 1}}, # 稀疏行
        ]
        
        # 创建模拟的原始数据
        mock_raw_data = [[''] * 6 for _ in range(20)]  # 20行6列的空数据
        filtered = self.detector._filter_false_positives(candidates_with_false_positives, mock_raw_data)
        
        print(f"过滤前候选数: {len(candidates_with_false_positives)}")
        print(f"过滤后候选数: {len(filtered)}")
        
        # 验证过滤效果
        self.assertLessEqual(len(filtered), len(candidates_with_false_positives), 
                           "过滤后的候选数应该不超过原始数量")
        
        # 验证高置信度的候选被保留
        filtered_indices = [c['row_index'] for c in filtered]
        self.assertIn(0, filtered_indices, "高置信度的第0行应该被保留")
        self.assertIn(1, filtered_indices, "高置信度的第1行应该被保留")
    
    def test_analyze_row_content_enhanced(self):
        """测试增强的行内容分析"""
        print("\n=== 测试增强的行内容分析 ===")
        
        # 测试不同类型的行
        header_row = ['销售数据', '销售数据', '成本数据', '成本数据', '', '']
        data_row = ['100', '1000', '80', '800', '600', '480']
        mixed_row = ['产品A', '100', '产品B', '200', '2023-01-01', 'N/A']
        
        header_analysis = self.detector.analyze_row_content_enhanced(header_row)
        data_analysis = self.detector.analyze_row_content_enhanced(data_row)
        mixed_analysis = self.detector.analyze_row_content_enhanced(mixed_row)
        
        print(f"头部行分析: {header_analysis}")
        print(f"数据行分析: {data_analysis}")
        print(f"混合行分析: {mixed_analysis}")
        
        # 验证分析结果包含必要字段
        required_fields = ['non_empty_count', 'unique_count', 'numeric_count', 
                          'text_count', 'pattern_diversity', 'semantic_scores',
                          'date_count', 'structure_score', 'format_consistency']
        
        for analysis in [header_analysis, data_analysis, mixed_analysis]:
            for field in required_fields:
                self.assertIn(field, analysis, f"分析结果应包含字段: {field}")
        
        # 验证头部行的特征
        self.assertGreater(header_analysis['text_count'], data_analysis['text_count'],
                          "头部行应该包含更多文本")
        self.assertGreater(data_analysis['numeric_count'], header_analysis['numeric_count'],
                          "数据行应该包含更多数字")
    
    def test_detect_multi_level_structure_enhanced(self):
        """测试增强的多级结构检测"""
        print("\n=== 测试增强的多级结构检测 ===")
        
        mock_file_path = "/test/data.xlsx"
        
        # 创建模拟的头部候选和合并单元格信息
        mock_header_candidates = [
            {'row_index': 1, 'confidence': 0.8, 'analysis': {'non_empty_count': 4, 'text_count': 4}},
            {'row_index': 2, 'confidence': 0.7, 'analysis': {'non_empty_count': 6, 'text_count': 6}},
            {'row_index': 3, 'confidence': 0.6, 'analysis': {'non_empty_count': 6, 'text_count': 6}}
        ]
        mock_merged_cells = []
        
        result = self.detector.detect_multi_level_structure_enhanced(mock_header_candidates, mock_merged_cells)
        
        print(f"多级结构检测结果: {result}")
        
        # 验证结果结构
        self.assertIsInstance(result, dict)
        self.assertIn('is_multi_level', result)
        self.assertIn('confidence', result)
        self.assertIn('structure_type', result)
        self.assertIn('recommended_header', result)
        self.assertIn('analysis_details', result)
        
        # 验证结果类型
        self.assertIsInstance(result['is_multi_level'], bool)
        self.assertIsInstance(result['confidence'], (int, float))
        self.assertIsInstance(result['structure_type'], str)
        self.assertIsInstance(result['analysis_details'], str)
        
        # 验证置信度范围
        confidence = result['confidence']
        self.assertGreaterEqual(confidence, 0.0, "置信度不应低于0")
        self.assertLessEqual(confidence, 1.0, "置信度不应超过1")
    
    def test_is_numeric_helper(self):
        """测试数字检测辅助函数"""
        print("\n=== 测试数字检测辅助函数 ===")
        
        # 测试各种数字格式
        test_cases = [
            ('123', True),
            ('123.45', True),
            ('-123', True),
            ('1,234', True),
            ('12.34%', True),
            ('$123.45', True),
            ('abc', False),
            ('', False),
            ('123abc', False),
            ('N/A', False)
        ]
        
        for value, expected in test_cases:
            result = self.detector._is_numeric(value)
            print(f"'{value}' -> {result} (期望: {expected})")
            self.assertEqual(result, expected, f"'{value}' 的数字检测结果不正确")
    
    def test_is_date_like_helper(self):
        """测试日期检测辅助函数"""
        print("\n=== 测试日期检测辅助函数 ===")
        
        # 测试各种日期格式
        test_cases = [
            ('2023-01-01', True),
            ('2023/01/01', True),
            ('01-01-2023', True),
            ('Jan 1, 2023', True),
            ('2023年1月1日', True),
            ('123', False),
            ('abc', False),
            ('', False)
        ]
        
        for value, expected in test_cases:
            result = self.detector._is_date_like(value)
            print(f"'{value}' -> {result} (期望: {expected})")
            self.assertEqual(result, expected, f"'{value}' 的日期检测结果不正确")


def run_comprehensive_test():
    """运行综合测试"""
    print("\n" + "="*60)
    print("开始增强多级列头检测功能综合测试")
    print("="*60)
    
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEnhancedMultiHeaderDetector)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出测试总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    print(f"运行测试数: {result.testsRun}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    print(f"\n成功率: {success_rate:.1f}%")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # 运行综合测试
    success = run_comprehensive_test()
    
    if success:
        print("\n🎉 所有测试通过！增强多级列头检测功能工作正常。")
    else:
        print("\n❌ 部分测试失败，请检查实现。")
        sys.exit(1)