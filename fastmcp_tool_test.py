#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastMCP工具测试脚本

使用FastMCP的get_tool方法来正确访问和测试run_excel_code工具
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_fastmcp_tools():
    """
    使用FastMCP的get_tool方法测试工具
    """
    print("🚀 开始FastMCP工具测试...")
    
    # 导入server模块
    try:
        import server
        print("✅ 成功导入server模块")
    except Exception as e:
        print(f"❌ 导入server模块失败: {e}")
        return
    
    # 获取mcp对象
    if hasattr(server, 'mcp'):
        mcp_obj = server.mcp
        print(f"✅ 找到mcp对象: {type(mcp_obj)}")
        
        # 获取所有工具
        try:
            tools = mcp_obj.get_tools()
            print(f"✅ 获取到 {len(tools)} 个工具")
            
            # 查找run_excel_code工具
            run_excel_tool = None
            for tool in tools:
                if tool.name == 'run_excel_code':
                    run_excel_tool = tool
                    break
            
            if run_excel_tool:
                print(f"✅ 找到run_excel_code工具")
                print(f"工具描述: {run_excel_tool.description}")
                
                # 获取工具的原始函数
                try:
                    tool_func = mcp_obj.get_tool('run_excel_code')
                    print(f"✅ 获取到工具函数: {type(tool_func)}")
                    
                    # 检查工具函数的属性
                    if hasattr(tool_func, 'func'):
                        original_func = tool_func.func
                        print(f"✅ 找到原始函数: {original_func}")
                        
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
print(f"数据类型: {df.dtypes.to_dict()}")
result = {
    "shape": df.shape,
    "columns": list(df.columns),
    "dtypes": df.dtypes.to_dict()
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
                                if 'result' in result:
                                    print(f"结果: {result['result']}")
                            else:
                                print(f"错误: {result.get('error', 'unknown error')}")
                                if 'suggestions' in result:
                                    print(f"建议: {result['suggestions']}")
                        except Exception as e:
                            print(f"❌ 测试执行失败: {e}")
                            import traceback
                            traceback.print_exc()
                    else:
                        print(f"❌ 工具函数没有func属性，属性: {dir(tool_func)}")
                        
                        # 尝试直接调用工具函数
                        print("\n🔧 尝试直接调用工具函数...")
                        try:
                            # 如果工具函数本身就是可调用的
                            if callable(tool_func):
                                test_file = str(project_root / "test_data.xlsx")
                                code = """
print(f"数据形状: {df.shape}")
result = {"shape": df.shape}
"""
                                result = tool_func(
                                    file_path=test_file,
                                    code=code
                                )
                                print("✅ 直接调用成功")
                                print(f"结果: {result}")
                            else:
                                print("❌ 工具函数不可调用")
                        except Exception as e:
                            print(f"❌ 直接调用失败: {e}")
                            import traceback
                            traceback.print_exc()
                            
                except Exception as e:
                    print(f"❌ 获取工具函数失败: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print("❌ 未找到run_excel_code工具")
                print("可用工具:")
                for tool in tools:
                    print(f"  - {tool.name}: {tool.description}")
                    
        except Exception as e:
            print(f"❌ 获取工具列表失败: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ 未找到mcp对象")
    
    print("\n🎉 FastMCP工具测试完成")

def test_manual_execution():
    """
    手动执行Excel代码处理逻辑
    """
    print("\n🔧 手动执行Excel代码处理逻辑...")
    
    try:
        import pandas as pd
        import numpy as np
        from security.code_executor import execute_code_safely
        
        test_file = str(project_root / "test_data.xlsx")
        
        if not os.path.exists(test_file):
            print(f"❌ 测试文件不存在: {test_file}")
            return
        
        # 读取Excel文件
        df = pd.read_excel(test_file)
        print(f"✅ 成功读取Excel文件，数据形状: {df.shape}")
        
        # 测试代码
        code = """
# 查看数据基本信息
print(f"数据形状: {df.shape}")
print(f"列名: {list(df.columns)}")
result = {
    "shape": df.shape,
    "columns": list(df.columns)
}
"""
        
        # 执行代码
        result = execute_code_safely(code, df, test_file)
        print("✅ 手动执行成功")
        print(f"结果: {result}")
        
    except Exception as e:
        print(f"❌ 手动执行失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # 检查虚拟环境
    if not os.path.exists(project_root / "venv" / "bin" / "python"):
        print("❌ 虚拟环境不存在，请先创建虚拟环境")
        sys.exit(1)
    
    # 检查测试数据文件
    test_file = project_root / "test_data.xlsx"
    if not test_file.exists():
        print(f"❌ 测试数据文件不存在: {test_file}")
        print("请先运行 create_test_excel.py 创建测试数据")
        sys.exit(1)
    
    print("🔧 环境检查通过，开始测试...")
    test_fastmcp_tools()
    test_manual_execution()