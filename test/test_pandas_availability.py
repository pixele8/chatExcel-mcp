#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试pandas模块在run_excel_code执行环境中的可用性
"""

import pandas as pd
import os
import sys
from server import run_excel_code

def create_test_file():
    """创建测试文件"""
    test_data = {
        '姓名': ['张三', '李四'],
        '部门': ['技术', '销售'],
        '薪资': [8000, 12000]
    }
    
    df = pd.DataFrame(test_data)
    excel_file = 'pandas_test.xlsx'
    df.to_excel(excel_file, index=False)
    return excel_file

def test_pandas_module_availability(excel_file):
    """测试pandas模块在执行环境中的可用性"""
    print("🔍 测试pandas模块可用性")
    print("=" * 40)
    
    # 测试1: 检查pd变量是否存在
    code1 = '''
print("=== 测试1: 检查pd变量 ===")
print(f"pd变量类型: {type(pd)}")
print(f"pd是否为None: {pd is None}")
if hasattr(pd, '__version__'):
    print(f"pandas版本: {pd.__version__}")
else:
    print("pd没有__version__属性")
result = "pd_available" if pd is not None else "pd_not_available"
'''
    
    print("执行测试1...")
    response1 = run_excel_code(code=code1, file_path=excel_file, auto_detect=False)
    print(f"测试1结果: {response1}")
    
    # 测试2: 尝试使用pandas功能
    code2 = '''
print("=== 测试2: 使用pandas功能 ===")
try:
    print(f"DataFrame形状: {df.shape}")
    print(f"列名: {list(df.columns)}")
    
    # 尝试分组操作
    group_result = df.groupby('部门')['薪资'].mean()
    print(f"分组结果: {group_result}")
    print(f"分组结果类型: {type(group_result)}")
    
    result = {
        "pandas_works": True,
        "groupby_works": True,
        "group_result": group_result.to_dict()
    }
except Exception as e:
    print(f"pandas操作失败: {e}")
    result = {
        "pandas_works": False,
        "error": str(e)
    }
'''
    
    print("\n执行测试2...")
    response2 = run_excel_code(code=code2, file_path=excel_file, auto_detect=False)
    print(f"测试2结果: {response2}")
    
    # 测试3: 检查执行环境中的所有变量
    code3 = '''
print("=== 测试3: 检查执行环境变量 ===")
available_vars = []
for var_name in ['pd', 'df', 'np', 'file_path', 'sheet_name']:
    if var_name in locals():
        var_value = locals()[var_name]
        print(f"{var_name}: {type(var_value)} - {var_value is not None}")
        available_vars.append(var_name)
    else:
        print(f"{var_name}: 不存在")
        
result = {
    "available_vars": available_vars,
    "locals_keys": list(locals().keys())
}
'''
    
    print("\n执行测试3...")
    response3 = run_excel_code(code=code3, file_path=excel_file, auto_detect=False)
    print(f"测试3结果: {response3}")
    
    return response1, response2, response3

def main():
    """主测试函数"""
    print("🧪 pandas模块可用性测试")
    print("=" * 50)
    
    excel_file = create_test_file()
    
    try:
        response1, response2, response3 = test_pandas_module_availability(excel_file)
        
        print("\n" + "=" * 50)
        print("📊 测试总结:")
        
        # 分析结果
        if 'error' not in response1:
            print("✅ 测试1 (pd变量检查): 通过")
        else:
            print(f"❌ 测试1 (pd变量检查): 失败 - {response1.get('error', {})}")
        
        if 'error' not in response2:
            result2 = response2.get('result', {})
            if isinstance(result2, dict) and result2.get('pandas_works', False):
                print("✅ 测试2 (pandas功能): 通过")
            else:
                print(f"❌ 测试2 (pandas功能): 失败 - {result2}")
        else:
            print(f"❌ 测试2 (pandas功能): 失败 - {response2.get('error', {})}")
        
        if 'error' not in response3:
            print("✅ 测试3 (环境变量): 通过")
        else:
            print(f"❌ 测试3 (环境变量): 失败 - {response3.get('error', {})}")
        
    finally:
        if os.path.exists(excel_file):
            os.remove(excel_file)
            print(f"\n🧹 已清理测试文件: {excel_file}")

if __name__ == "__main__":
    main()