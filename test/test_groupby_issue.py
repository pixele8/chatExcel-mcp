#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试pandas分组操作问题
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from server import run_excel_code
import pandas as pd

def create_test_excel():
    """创建测试Excel文件"""
    data = {
        '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
        '年龄': [25, 30, 35, 28, 32],
        '城市': ['北京', '上海', '广州', '深圳', '杭州'],
        '薪资': [8000, 12000, 15000, 9500, 11000],
        '部门': ['技术', '销售', '市场', '技术', '财务']
    }
    df = pd.DataFrame(data)
    test_file = 'test_groupby.xlsx'
    df.to_excel(test_file, index=False)
    print(f"✅ 创建测试文件: {test_file}")
    return test_file

def test_groupby_operations():
    """测试分组操作"""
    test_file = create_test_excel()
    
    print("\n=== 测试1: 基本分组操作 ===")
    code1 = "result = df.groupby('部门')['薪资'].mean()"
    result1 = run_excel_code(test_file, code1, auto_detect=True)
    print(f"结果1: {result1}")
    
    print("\n=== 测试2: 分组操作带调试信息 ===")
    code2 = """
print(f"DataFrame shape: {df.shape}")
print(f"DataFrame columns: {df.columns.tolist()}")
print(f"DataFrame dtypes: {df.dtypes}")
print(f"部门列的唯一值: {df['部门'].unique()}")
print(f"部门列的数据类型: {type(df['部门'])}")
print(f"部门列是否为Series: {isinstance(df['部门'], pd.Series)}")

try:
    result = df.groupby('部门')['薪资'].mean()
    print(f"分组成功: {result}")
except Exception as e:
    print(f"分组失败: {e}")
    print(f"错误类型: {type(e)}")
    import traceback
    traceback.print_exc()
"""
    result2 = run_excel_code(test_file, code2, auto_detect=True)
    print(f"结果2: {result2}")
    
    print("\n=== 测试3: 传统读取方式 ===")
    code3 = "result = df.groupby('部门')['薪资'].mean()"
    result3 = run_excel_code(test_file, code3, auto_detect=False)
    print(f"结果3: {result3}")
    
    # 清理测试文件
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"\n🗑️ 清理测试文件: {test_file}")

if __name__ == "__main__":
    test_groupby_operations()