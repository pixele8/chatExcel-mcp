#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接函数测试脚本

通过访问FastMCP内部的原始函数来测试run_excel_code
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_run_excel_code_function():
    """
    直接测试run_excel_code的原始函数
    """
    print("🚀 开始直接测试run_excel_code原始函数...")
    
    # 导入server模块
    try:
        import server
        print("✅ 成功导入server模块")
    except Exception as e:
        print(f"❌ 导入server模块失败: {e}")
        return
    
    # 检查mcp对象和其工具
    if hasattr(server, 'mcp'):
        print("✅ 找到mcp对象")
        
        # 查看mcp对象的属性
        mcp_obj = server.mcp
        print(f"MCP对象类型: {type(mcp_obj)}")
        
        # 尝试访问工具
        if hasattr(mcp_obj, '_tools'):
            tools = mcp_obj._tools
            print(f"注册的工具数量: {len(tools)}")
            
            # 查找run_excel_code工具
            if 'run_excel_code' in tools:
                tool = tools['run_excel_code']
                print(f"找到run_excel_code工具: {type(tool)}")
                
                # 尝试获取原始函数
                if hasattr(tool, 'func'):
                    original_func = tool.func
                    print(f"原始函数: {original_func}")
                    
                    # 测试原始函数
                    test_file = str(project_root / "test_data.xlsx")
                    
                    if not os.path.exists(test_file):
                        print(f"❌ 测试文件不存在: {test_file}")
                        return
                    
                    print(f"✅ 测试文件存在: {test_file}")
                    
                    # 测试用例: 基本数据查看
                    print("\n📊 测试用例: 基本数据查看")
                    code = """
# 查看数据基本信息
print(f"数据形状: {df.shape}")
print(f"列名: {list(df.columns)}")
result = {
    "shape": df.shape,
    "columns": list(df.columns)
}
"""
                    
                    try:
                        result = original_func(
                            file_path=test_file,
                            code=code
                        )
                        print("✅ 测试执行成功")
                        print(f"执行状态: {result.get('success', 'unknown')}")
                        if result.get('success'):
                            print(f"输出: {result.get('output', 'no output')}")
                            print(f"结果: {result.get('result', 'no result')}")
                        else:
                            print(f"错误: {result.get('error', 'unknown error')}")
                    except Exception as e:
                        print(f"❌ 测试执行失败: {e}")
                        import traceback
                        traceback.print_exc()
                else:
                    print("❌ 工具对象没有func属性")
            else:
                print("❌ 未找到run_excel_code工具")
                print(f"可用工具: {list(tools.keys())}")
        else:
            print("❌ mcp对象没有_tools属性")
            print(f"mcp对象属性: {dir(mcp_obj)}")
    else:
        print("❌ 未找到mcp对象")
    
    print("\n🎉 直接函数测试完成")

def test_pandas_import():
    """
    测试pandas导入
    """
    print("\n🐼 测试pandas导入...")
    try:
        import pandas as pd
        import numpy as np
        print(f"✅ pandas版本: {pd.__version__}")
        print(f"✅ numpy版本: {np.__version__}")
        
        # 测试读取Excel文件
        test_file = str(project_root / "test_data.xlsx")
        if os.path.exists(test_file):
            df = pd.read_excel(test_file)
            print(f"✅ 成功读取Excel文件，数据形状: {df.shape}")
            print(f"列名: {list(df.columns)}")
        else:
            print(f"❌ 测试文件不存在: {test_file}")
    except Exception as e:
        print(f"❌ pandas导入或使用失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # 检查虚拟环境
    if not os.path.exists(project_root / "venv" / "bin" / "python"):
        print("❌ 虚拟环境不存在，请先创建虚拟环境")
        sys.exit(1)
    
    print("🔧 环境检查通过，开始测试...")
    test_pandas_import()
    test_run_excel_code_function()