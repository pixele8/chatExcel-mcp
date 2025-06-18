#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强列头匹配算法使用示例
创建日期: 2025-06-18
功能: 演示如何使用增强的列头匹配算法来处理Excel文件中列头不在第一行的情况
"""

import pandas as pd
from column_checker import ColumnChecker, match_column_with_dataframe


def demo_basic_usage():
    """演示基本用法"""
    print("=== 基本用法演示 ===")
    
    # 创建模拟Excel数据：列头在第3行
    data = {
        'A': ['标题行', '空行', '日期', '2023-01-01', '2023-01-02', '2023-01-03'],
        'B': ['', '', '金额', 100.50, 200.75, 150.25],
        'C': ['', '', '类别', '餐饮', '交通', '购物'],
        'D': ['', '', '备注', '午餐费用', '地铁票', '买衣服']
    }
    df = pd.DataFrame(data)
    
    print("原始数据框:")
    print(df)
    print()
    
    # 使用增强的列头匹配算法
    checker = ColumnChecker()
    
    target_columns = ['消耗日期', '金额', '分类', '说明']
    
    for target in target_columns:
        print(f"--- 查找列名: '{target}' ---")
        result = checker.match_column_with_dataframe(target, df)
        
        print(f"匹配置信度: {result['confidence_score']:.2f}")
        
        if 'header_analysis' in result and result['header_analysis']['found_potential_header']:
            header_info = result['header_analysis']
            print(f"✓ 在第{header_info['header_row_index'] + 1}行发现列头")
            
            if header_info['potential_matches']:
                best_match = header_info['potential_matches'][0]
                print(f"  最佳匹配: '{best_match['header_value']}'")
                print(f"  列索引: {best_match['column_index']}")
                print(f"  相似度: {best_match['similarity']:.2f}")
                
                # 演示如何使用这个信息来重新构建DataFrame
                print(f"  建议代码: df.iloc[{header_info['header_row_index'] + 1}:, {best_match['column_index']}]")
        else:
            print("✗ 未找到匹配的列头")
        
        print()


def demo_reconstruct_dataframe():
    """演示如何根据检测结果重新构建DataFrame"""
    print("=== DataFrame重构演示 ===")
    
    # 创建测试数据
    data = {
        'A': ['', '', '消费日期', '2023-01-01', '2023-01-02'],
        'B': ['', '', '金额', 100, 200],
        'C': ['', '', '类别', '餐饮', '交通'],
        'D': ['', '', '备注', '午餐', '地铁']
    }
    original_df = pd.DataFrame(data)
    
    print("原始数据框:")
    print(original_df)
    print()
    
    # 检测列头位置
    checker = ColumnChecker()
    result = checker.match_column_with_dataframe('消费日期', original_df)
    
    if 'header_analysis' in result and result['header_analysis']['found_potential_header']:
        header_row = result['header_analysis']['header_row_index']
        print(f"检测到列头在第{header_row + 1}行")
        
        # 重新构建DataFrame
        # 使用检测到的行作为列名
        new_columns = original_df.iloc[header_row].tolist()
        # 使用该行之后的数据作为数据内容
        new_data = original_df.iloc[header_row + 1:].reset_index(drop=True)
        new_data.columns = new_columns
        
        print("\n重构后的DataFrame:")
        print(new_data)
        print()
        
        # 现在可以正常使用列名访问数据
        print("现在可以使用正确的列名:")
        print(f"消费日期列: {new_data['消费日期'].tolist()}")
        print(f"金额列: {new_data['金额'].tolist()}")
        print(f"类别列: {new_data['类别'].tolist()}")


def demo_batch_processing():
    """演示批量处理多个目标列名"""
    print("=== 批量处理演示 ===")
    
    # 创建复杂的测试数据
    data = {
        'Col1': ['报表标题', '', '日期', '2023-01-01', '2023-01-02', '2023-01-03'],
        'Col2': ['', '', '消费金额', 100, 150, 200],
        'Col3': ['', '', '支出类型', '餐饮', '交通', '购物'],
        'Col4': ['', '', '详细说明', '午餐', '地铁', '衣服'],
        'Col5': ['', '', '支付方式', '现金', '刷卡', '支付宝']
    }
    df = pd.DataFrame(data)
    
    print("测试数据:")
    print(df)
    print()
    
    # 要查找的目标列名
    target_columns = {
        '消耗日期': '日期相关',
        '金额': '金额相关', 
        '类别': '分类相关',
        '备注': '说明相关',
        '付款方式': '支付相关'
    }
    
    checker = ColumnChecker()
    matches = {}
    
    for target, description in target_columns.items():
        print(f"查找 '{target}' ({description}):")
        result = checker.match_column_with_dataframe(target, df)
        
        if 'header_analysis' in result and result['header_analysis']['found_potential_header']:
            header_info = result['header_analysis']
            if header_info['potential_matches']:
                best_match = header_info['potential_matches'][0]
                matches[target] = {
                    'found_header': best_match['header_value'],
                    'column_index': best_match['column_index'],
                    'similarity': best_match['similarity'],
                    'row_index': header_info['header_row_index']
                }
                print(f"  ✓ 找到: '{best_match['header_value']}' (相似度: {best_match['similarity']:.2f})")
            else:
                print(f"  ✗ 未找到匹配")
        else:
            print(f"  ✗ 未找到匹配")
    
    print("\n=== 匹配汇总 ===")
    for target, match_info in matches.items():
        print(f"'{target}' -> '{match_info['found_header']}' (列{match_info['column_index']}, 相似度: {match_info['similarity']:.2f})")


def demo_edge_cases():
    """演示边缘情况处理"""
    print("=== 边缘情况演示 ===")
    
    # 情况1: 没有完整行
    print("情况1: 没有完整行的数据")
    incomplete_data = {
        'A': ['日期', '', '2023-01-01'],
        'B': ['', '金额', 100],
        'C': ['类别', '', '餐饮']
    }
    incomplete_df = pd.DataFrame(incomplete_data)
    print(incomplete_df)
    
    checker = ColumnChecker()
    result = checker.match_column_with_dataframe('日期', incomplete_df)
    print(f"匹配结果置信度: {result['confidence_score']:.2f}")
    print()
    
    # 情况2: 多个完整行，选择最小行号
    print("情况2: 多个完整行，应选择最小行号")
    multiple_complete_data = {
        'A': ['标题1', '标题2', '日期', '消费日期', '2023-01-01'],
        'B': ['副标题1', '副标题2', '金额', '消费金额', 100],
        'C': ['说明1', '说明2', '类别', '消费类别', '餐饮']
    }
    multiple_df = pd.DataFrame(multiple_complete_data)
    print(multiple_df)
    
    result = checker.match_column_with_dataframe('日期', multiple_df)
    if 'header_analysis' in result and result['header_analysis']['found_potential_header']:
        header_row = result['header_analysis']['header_row_index']
        print(f"选择的列头行: 第{header_row + 1}行 (符合最小行号规则)")
    print()


if __name__ == "__main__":
    print("增强列头匹配算法演示程序")
    print("=" * 50)
    
    demo_basic_usage()
    print("\n" + "=" * 50)
    
    demo_reconstruct_dataframe()
    print("\n" + "=" * 50)
    
    demo_batch_processing()
    print("\n" + "=" * 50)
    
    demo_edge_cases()
    
    print("\n演示完成！")
    print("\n使用说明:")
    print("1. 使用 match_column_with_dataframe() 函数进行增强匹配")
    print("2. 检查返回结果中的 'header_analysis' 字段")
    print("3. 根据检测到的列头行重新构建DataFrame")
    print("4. 优先检查前5行，不满足时以5行为组向后排查")
    print("5. 选择同一行所有列都不为空的最小行序号作为列头行")