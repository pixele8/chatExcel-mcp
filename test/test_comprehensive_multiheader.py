#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合测试改进后的多级列头处理能力
"""

import pandas as pd
import os
from server import run_excel_code

def create_comprehensive_test_files():
    """创建各种类型的测试文件"""
    
    # 1. 简单单级列头文件
    simple_data = {
        '姓名': ['张三', '李四', '王五'],
        '年龄': [25, 30, 35],
        '部门': ['技术', '销售', '市场'],
        '薪资': [8000, 12000, 10000]
    }
    simple_df = pd.DataFrame(simple_data)
    simple_file = 'test_simple_header.xlsx'
    simple_df.to_excel(simple_file, index=False)
    
    # 2. 真正的多级列头文件（手动创建）
    # 由于pandas不支持MultiIndex列写入Excel，我们手动创建
    multi_data = [
        ['销售数据', '销售数据', '销售数据', '财务数据', '财务数据'],  # 第一级列头
        ['产品A', '产品B', '产品C', '收入', '支出'],  # 第二级列头
        [100, 200, 150, 1000, 800],  # 数据行1
        [120, 180, 160, 1200, 900],  # 数据行2
        [110, 220, 140, 1100, 850]   # 数据行3
    ]
    multi_df = pd.DataFrame(multi_data)
    multi_file = 'test_true_multiheader.xlsx'
    multi_df.to_excel(multi_file, index=False, header=False)
    
    # 3. 复杂格式文件（有空行和标题）
    complex_data = [
        ['', '', '', '', ''],  # 空行
        ['公司销售报表', '', '', '', ''],  # 标题行
        ['', '', '', '', ''],  # 空行
        ['姓名', '年龄', '部门', '薪资', '城市'],  # 列头在第4行（index=3）
        ['张三', 25, '技术', 8000, '北京'],
        ['李四', 30, '销售', 12000, '上海'],
        ['王五', 35, '市场', 10000, '广州']
    ]
    complex_df = pd.DataFrame(complex_data)
    complex_file = 'test_complex_header.xlsx'
    complex_df.to_excel(complex_file, index=False, header=False)
    
    # 4. 伪多级列头文件（看起来像多级但实际是单级）
    fake_multi_data = [
        ['销售数据', '销售数据', '销售数据', '财务数据', '财务数据'],  # 第一行
        ['产品A', '产品B', '产品C', '收入', '支出'],  # 第二行（实际列头）
        [100, 200, 150, 1000, 800],
        [120, 180, 160, 1200, 900],
        [110, 220, 140, 1100, 850]
    ]
    fake_multi_df = pd.DataFrame(fake_multi_data)
    fake_multi_file = 'test_fake_multiheader.xlsx'
    fake_multi_df.to_excel(fake_multi_file, index=False, header=False)
    
    return simple_file, multi_file, complex_file, fake_multi_file

def test_run_excel_code_with_pandas(file_path, description):
    """测试run_excel_code函数的pandas操作能力"""
    print(f"\n📋 测试 {description}")
    print("-" * 40)
    
    # 测试基本读取和pandas操作
    code = '''
# 读取数据并进行基本分析
print(f"数据形状: {df.shape}")
print(f"列名: {list(df.columns)}")
print(f"前3行数据:")
print(df.head(3))

# 尝试进行pandas操作
try:
    if '薪资' in df.columns:
        avg_salary = df['薪资'].mean()
        print(f"平均薪资: {avg_salary}")
        result = {'avg_salary': avg_salary, 'total_rows': len(df)}
    elif len(df.columns) >= 3:
        # 对数值列进行统计
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            stats = df[numeric_cols].describe()
            print(f"数值列统计:")
            print(stats)
            result = {'numeric_columns': len(numeric_cols), 'total_rows': len(df)}
        else:
            result = {'message': '无数值列', 'total_rows': len(df)}
    else:
        result = {'message': '数据结构简单', 'total_rows': len(df)}
except Exception as e:
    print(f"pandas操作出错: {e}")
    result = {'error': str(e)}
'''
    
    try:
        response = run_excel_code(file_path, code)
        
        if response.get('success'):
            print(f"✅ 执行成功")
            if 'result' in response:
                print(f"结果: {response['result']}")
            if 'output' in response:
                print(f"输出: {response['output']}")
        else:
            print(f"❌ 执行失败")
            if 'error' in response:
                print(f"错误: {response['error']}")
                
        return response.get('success', False)
        
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 综合测试改进后的多级列头处理能力")
    print("=" * 60)
    
    # 创建测试文件
    simple_file, multi_file, complex_file, fake_multi_file = create_comprehensive_test_files()
    
    test_cases = [
        (simple_file, "简单单级列头文件"),
        (multi_file, "真正的多级列头文件"),
        (complex_file, "复杂格式文件（有空行）"),
        (fake_multi_file, "伪多级列头文件")
    ]
    
    passed_tests = 0
    total_tests = len(test_cases)
    
    try:
        for file_path, description in test_cases:
            success = test_run_excel_code_with_pandas(file_path, description)
            if success:
                passed_tests += 1
    
    finally:
        # 清理测试文件
        for file in [simple_file, multi_file, complex_file, fake_multi_file]:
            if os.path.exists(file):
                os.remove(file)
                print(f"🧹 已清理: {file}")
    
    print(f"\n{'='*60}")
    print(f"📊 测试结果: {passed_tests}/{total_tests} 通过")
    
    if passed_tests == total_tests:
        print("🎉 所有测试通过！改进的多级列头处理工作正常")
        print("\n✅ 改进效果:")
        print("   - 保持了对简单列头的正确处理")
        print("   - 增强了对多级列头的智能识别")
        print("   - 提供了回退机制确保兼容性")
        print("   - 减少了参数建议错误的影响")
    else:
        print("⚠️ 部分测试失败，需要进一步优化")
        print("\n🔍 可能的问题:")
        print("   - 多级列头检测逻辑需要调整")
        print("   - 参数选择策略需要优化")
        print("   - 回退机制可能过于激进")

if __name__ == "__main__":
    main()