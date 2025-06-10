#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强功能测试脚本
测试新增的Excel智能读取、编码检测和数据验证功能
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_excel_helper import (
    EncodingCache, 
    detect_file_encoding, 
    smart_read_excel,
    validate_excel_data_integrity
)
from data_verification import DataVerificationEngine, verify_data_processing_result

def create_test_excel_files():
    """创建测试用的Excel文件"""
    print("创建测试Excel文件...")
    
    # 创建测试数据
    test_data = {
        '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
        '年龄': [25, 30, 35, 28, 32],
        '城市': ['北京', '上海', '广州', '深圳', '杭州'],
        '薪资': [8000, 12000, 15000, 9500, 11000],
        '部门': ['技术', '销售', '市场', '技术', '人事']
    }
    
    df = pd.DataFrame(test_data)
    
    # 保存为Excel文件
    test_file1 = 'test_data_original.xlsx'
    test_file2 = 'test_data_modified.xlsx'
    
    df.to_excel(test_file1, index=False)
    
    # 创建修改后的数据（用于对比测试）
    df_modified = df.copy()
    df_modified.loc[0, '年龄'] = 26  # 修改一个值
    df_modified = df_modified.drop(4)  # 删除一行
    df_modified.to_excel(test_file2, index=False)
    
    print(f"测试文件已创建: {test_file1}, {test_file2}")
    return test_file1, test_file2

def test_encoding_detection():
    """测试编码检测功能"""
    print("\n=== 测试编码检测功能 ===")
    
    # 创建编码缓存
    cache = EncodingCache()
    
    # 创建测试CSV文件
    test_csv = 'test_encoding.csv'
    test_data = "姓名,年龄,城市\n张三,25,北京\n李四,30,上海\n王五,28,广州"
    
    try:
        # 写入UTF-8编码的CSV文件
        with open(test_csv, 'w', encoding='utf-8') as f:
            f.write(test_data)
        
        # 测试编码检测
        encoding_result = detect_file_encoding(test_csv)
        print(f"检测结果: {encoding_result}")
        
        # 测试缓存功能
        cache.set(test_csv, encoding_result['encoding'])
        cached_encoding = cache.get(test_csv)
        print(f"缓存的编码: {cached_encoding}")
        
        # 清理测试文件
        os.remove(test_csv)
        
        return encoding_result['confidence'] > 0.5
    except Exception as e:
        print(f"编码检测测试失败: {e}")
        if os.path.exists(test_csv):
            os.remove(test_csv)
        return False

def test_smart_excel_reading():
    """测试智能Excel读取功能"""
    print("\n=== 测试智能Excel读取功能 ===")
    
    test_file = 'test_data_original.xlsx'
    if not os.path.exists(test_file):
        print("测试文件不存在")
        return False
    
    try:
        # 测试智能读取
        result = smart_read_excel(test_file, auto_detect_params=True)
        
        if result['success']:
            print("智能读取成功!")
            print(f"数据形状: {result['dataframe'].shape}")
            print(f"列名: {list(result['dataframe'].columns)}")
            print(f"读取信息: {result['info']}")
            
            if result.get('warnings'):
                print(f"警告: {result['warnings']}")
            
            return True
        else:
            print(f"智能读取失败: {result.get('errors', [])}")
            return False
            
    except Exception as e:
        print(f"智能读取测试出错: {str(e)}")
        return False

def test_data_verification():
    """测试数据验证功能"""
    print("\n=== 测试数据验证功能 ===")
    
    test_file1 = 'test_data_original.xlsx'
    test_file2 = 'test_data_modified.xlsx'
    
    if not (os.path.exists(test_file1) and os.path.exists(test_file2)):
        print("测试文件不存在")
        return False
    
    try:
        # 创建验证引擎
        verifier = DataVerificationEngine()
        
        # 读取数据
        df1 = pd.read_excel(test_file1)
        df2 = pd.read_excel(test_file2)
        
        print(f"原始数据形状: {df1.shape}")
        print(f"修改数据形状: {df2.shape}")
        
        # 执行比较
        comparison_result = verifier.compare_dataframes(
            df1, df2, 
            name1="原始数据", 
            name2="修改数据"
        )
        
        print("\n比较结果:")
        print(f"匹配得分: {comparison_result.get('match_score', 0):.2f}")
        print(f"存在差异: {comparison_result.get('has_differences', True)}")
        
        if comparison_result.get('structure_differences'):
            print(f"结构差异: {comparison_result['structure_differences']}")
        
        if comparison_result.get('content_differences'):
            print(f"内容差异数量: {len(comparison_result['content_differences'])}")
        
        return True
        
    except Exception as e:
        print(f"数据验证测试出错: {str(e)}")
        return False

def test_data_integrity_validation():
    """测试数据完整性验证"""
    print("\n=== 测试数据完整性验证 ===")
    
    test_file = 'test_data_original.xlsx'
    if not os.path.exists(test_file):
        print("测试文件不存在")
        return False
    
    try:
        # 读取原始数据
        df_original = pd.read_excel(test_file)
        
        # 模拟数据处理（添加一列计算结果）
        df_processed = df_original.copy()
        df_processed['薪资等级'] = df_processed['薪资'].apply(
            lambda x: '高' if x > 10000 else '中' if x > 8000 else '低'
        )
        
        # 执行完整性验证
        verification_result = verify_data_processing_result(
            test_file, df_processed, processing_description="测试数据处理"
        )
        
        print("\n完整性验证结果:")
        print(f"验证状态: {verification_result.get('status', 'unknown')}")
        print(f"质量评分: {verification_result.get('quality_score', 0):.2f}")
        
        if verification_result.get('summary'):
            summary = verification_result['summary']
            print(f"数据行数变化: {summary.get('row_count_change', 0)}")
            print(f"数据列数变化: {summary.get('column_count_change', 0)}")
        
        return True
        
    except Exception as e:
        print(f"完整性验证测试出错: {str(e)}")
        return False

def cleanup_test_files():
    """清理测试文件"""
    test_files = ['test_data_original.xlsx', 'test_data_modified.xlsx']
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"已删除测试文件: {file}")

def main():
    """主测试函数"""
    print("开始增强功能测试...")
    
    # 创建测试文件
    try:
        test_file1, test_file2 = create_test_excel_files()
    except Exception as e:
        print(f"创建测试文件失败: {str(e)}")
        return
    
    # 执行各项测试
    tests = [
        ("编码检测", test_encoding_detection),
        ("智能Excel读取", test_smart_excel_reading),
        ("数据验证", test_data_verification),
        ("数据完整性验证", test_data_integrity_validation)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"{test_name}测试出错: {str(e)}")
            results[test_name] = False
    
    # 输出测试结果总结
    print("\n=== 测试结果总结 ===")
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    # 清理测试文件
    cleanup_test_files()
    
    # 总体结果
    all_passed = all(results.values())
    print(f"\n总体测试结果: {'✅ 全部通过' if all_passed else '❌ 存在失败'}")
    
    return all_passed

if __name__ == "__main__":
    main()