#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模拟 MCP 客户端调用 run_excel_code 工具的测试用例
"""

import json
import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入 MCP 服务器
import mcp
from mcp import ClientSession, StdioServerParameters
from mcp.client import stdio
import asyncio
import pandas as pd

def create_test_excel():
    """创建测试 Excel 文件"""
    data = {
        '产品名称': ['iPhone 15', 'Samsung S24', 'Pixel 8', 'OnePlus 12'],
        '价格': [999, 899, 699, 799],
        '销量': [1000, 800, 600, 400],
        '评分': [4.5, 4.3, 4.4, 4.2]
    }
    df = pd.DataFrame(data)
    test_file = 'mcp_test_products.xlsx'
    df.to_excel(test_file, index=False)
    print(f"✅ 创建测试文件: {test_file}")
    return test_file

def test_direct_import():
    """直接测试导入和函数调用"""
    print("\n=== 直接测试 run_excel_code 函数 ===")
    
    try:
        from server import run_excel_code
        test_file = create_test_excel()
        
        # 测试代码
        test_code = """
print(f"pandas 版本: {pd.__version__}")
print(f"数据形状: {df.shape}")
print(f"列名: {list(df.columns)}")

# 计算总销售额
df['总销售额'] = df['价格'] * df['销量']
print(f"\n总销售额列已添加")

# 按价格排序
result = df.sort_values('价格', ascending=False)
print(f"\n按价格排序完成")
"""
        
        print(f"执行代码:\n{test_code}")
        print("-" * 50)
        
        result = run_excel_code(test_code, test_file)
        
        if 'error' in result:
            print(f"❌ 错误: {result['error']}")
            if 'traceback' in result['error']:
                print(f"详细错误:\n{result['error']['traceback']}")
        else:
            print(f"✅ 成功执行")
            print(f"输出: {result.get('output', 'No output')}")
            if 'result' in result:
                print(f"结果类型: {result['result'].get('type', 'unknown')}")
                print(f"结果形状: {result['result'].get('shape', 'unknown')}")
        
        return result
        
    except Exception as e:
        print(f"❌ 直接测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_problematic_code():
    """测试可能导致 NameError 的代码"""
    print("\n=== 测试可能导致 NameError 的代码 ===")
    
    try:
        from server import run_excel_code
        test_file = 'mcp_test_products.xlsx'
        
        # 这个代码可能会导致问题
        problematic_code = """
# 不显式导入，直接使用 pd
print("开始处理数据...")
print(f"使用 pandas 版本: {pd.__version__}")

# 检查数据
if df is not None:
    print(f"数据形状: {df.shape}")
    
    # 进行一些复杂操作
    summary_stats = df.describe()
    print("\n描述性统计:")
    print(summary_stats)
    
    # 分组统计
    high_price = df[df['价格'] > 800]
    print(f"\n高价产品数量: {len(high_price)}")
    
    result = high_price
else:
    print("数据为空")
    result = None
"""
        
        print(f"执行可能有问题的代码:\n{problematic_code}")
        print("-" * 50)
        
        result = run_excel_code(problematic_code, test_file)
        
        if 'error' in result:
            print(f"❌ 错误: {result['error']}")
            if result['error'].get('type') == 'NameError':
                print("🎯 发现 NameError！")
            if 'traceback' in result['error']:
                print(f"详细错误:\n{result['error']['traceback']}")
        else:
            print(f"✅ 意外成功")
            print(f"输出: {result.get('output', 'No output')}")
        
        return result
        
    except Exception as e:
        print(f"❌ 问题代码测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_namespace_isolation():
    """测试命名空间隔离"""
    print("\n=== 测试命名空间隔离 ===")
    
    try:
        from server import run_excel_code
        test_file = 'mcp_test_products.xlsx'
        
        # 第一次调用
        code1 = """
print("第一次调用")
print(f"pd 可用: {'pd' in locals()}")
print(f"df 可用: {'df' in locals()}")
custom_var = "第一次调用的变量"
result = df.head(2)
"""
        
        print("第一次调用:")
        result1 = run_excel_code(code1, test_file)
        if 'error' in result1:
            print(f"❌ 第一次调用错误: {result1['error']}")
        else:
            print(f"✅ 第一次调用成功")
            print(f"输出: {result1.get('output', 'No output')}")
        
        # 第二次调用，检查是否能访问第一次的变量
        code2 = """
print("第二次调用")
print(f"pd 可用: {'pd' in locals()}")
print(f"df 可用: {'df' in locals()}")
print(f"custom_var 可用: {'custom_var' in locals()}")

if 'custom_var' in locals():
    print(f"custom_var 值: {custom_var}")
else:
    print("custom_var 不可用（正常，命名空间隔离）")

result = df.tail(2)
"""
        
        print("\n第二次调用:")
        result2 = run_excel_code(code2, test_file)
        if 'error' in result2:
            print(f"❌ 第二次调用错误: {result2['error']}")
        else:
            print(f"✅ 第二次调用成功")
            print(f"输出: {result2.get('output', 'No output')}")
        
        return result1, result2
        
    except Exception as e:
        print(f"❌ 命名空间测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def main():
    """主函数"""
    print("🔍 MCP 环境下的 run_excel_code 测试")
    print("=" * 60)
    
    try:
        # 运行所有测试
        test_direct_import()
        test_problematic_code()
        test_namespace_isolation()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理测试文件
        test_files = ['mcp_test_products.xlsx']
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
                print(f"🗑️ 清理测试文件: {file}")

if __name__ == "__main__":
    main()
