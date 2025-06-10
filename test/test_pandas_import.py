#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试pandas导入和基本功能
用于验证MCP服务中pandas的工作状态
"""

import sys
import os
import traceback
from io import StringIO

def test_pandas_import():
    """测试pandas导入功能"""
    try:
        import pandas as pd
        print(f"✅ pandas导入成功，版本: {pd.__version__}")
        return True, pd
    except ImportError as e:
        print(f"❌ pandas导入失败: {e}")
        return False, None
    except Exception as e:
        print(f"❌ pandas导入异常: {e}")
        return False, None

def test_pandas_basic_operations(pd):
    """测试pandas基本操作"""
    try:
        # 创建测试数据
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': ['a', 'b', 'c', 'd', 'e'],
            'C': [1.1, 2.2, 3.3, 4.4, 5.5]
        })
        
        print(f"✅ DataFrame创建成功，形状: {df.shape}")
        print(f"✅ 列名: {list(df.columns)}")
        print(f"✅ 数据类型: {df.dtypes.to_dict()}")
        
        return True
    except Exception as e:
        print(f"❌ pandas基本操作失败: {e}")
        print(f"错误详情: {traceback.format_exc()}")
        return False

def test_excel_operations(pd):
    """测试Excel相关操作"""
    try:
        # 检查openpyxl是否可用
        import openpyxl
        print(f"✅ openpyxl导入成功，版本: {openpyxl.__version__}")
        
        # 创建测试Excel文件
        test_data = pd.DataFrame({
            'Name': ['张三', '李四', '王五'],
            'Age': [25, 30, 35],
            'Score': [85.5, 92.0, 78.5]
        })
        
        test_file = 'test_pandas.xlsx'
        test_data.to_excel(test_file, index=False)
        print(f"✅ Excel文件创建成功: {test_file}")
        
        # 读取Excel文件
        df_read = pd.read_excel(test_file)
        print(f"✅ Excel文件读取成功，形状: {df_read.shape}")
        
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"✅ 测试文件已清理")
            
        return True
    except Exception as e:
        print(f"❌ Excel操作失败: {e}")
        print(f"错误详情: {traceback.format_exc()}")
        return False

def test_code_execution_environment():
    """测试代码执行环境（模拟MCP中的exec环境）"""
    try:
        import pandas as pd
        
        # 模拟MCP中的代码执行环境
        code = """
# 测试代码
df_test = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
result = df_test.sum()
"""
        
        local_vars = {'pd': pd}
        stdout_capture = StringIO()
        old_stdout = sys.stdout
        sys.stdout = stdout_capture
        
        try:
            exec(code, {}, local_vars)
            result = local_vars.get('result', None)
            
            if result is not None:
                print(f"✅ 代码执行成功，结果类型: {type(result)}")
                print(f"✅ 结果内容: {result}")
                return True
            else:
                print("❌ 代码执行后未找到result变量")
                return False
                
        finally:
            sys.stdout = old_stdout
            
    except Exception as e:
        print(f"❌ 代码执行环境测试失败: {e}")
        print(f"错误详情: {traceback.format_exc()}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("pandas功能测试开始")
    print("=" * 50)
    
    # 测试1: pandas导入
    success, pd = test_pandas_import()
    if not success:
        print("\n❌ pandas导入失败，无法继续测试")
        return False
    
    print("\n" + "-" * 30)
    
    # 测试2: 基本操作
    print("测试pandas基本操作...")
    if not test_pandas_basic_operations(pd):
        print("\n❌ pandas基本操作测试失败")
        return False
    
    print("\n" + "-" * 30)
    
    # 测试3: Excel操作
    print("测试Excel操作...")
    if not test_excel_operations(pd):
        print("\n❌ Excel操作测试失败")
        return False
    
    print("\n" + "-" * 30)
    
    # 测试4: 代码执行环境
    print("测试代码执行环境...")
    if not test_code_execution_environment():
        print("\n❌ 代码执行环境测试失败")
        return False
    
    print("\n" + "=" * 50)
    print("✅ 所有测试通过！pandas功能正常")
    print("=" * 50)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)