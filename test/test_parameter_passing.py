#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试create_excel_read_template_tool函数的参数传递功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from excel_smart_tools import create_excel_read_template

def test_parameter_passing():
    """测试参数传递功能"""
    file_path = "/Users/wangdada/Downloads/mcp/pandasmcp/pandas-mcp-server/sample_data.xlsx"
    
    print("=== 测试1: 仅使用智能推荐参数 ===")
    result1 = create_excel_read_template(file_path, "复杂格式")
    print(f"推荐参数: {result1['recommended_params']}")
    print(f"生成的代码:\n{result1['code_template']}")
    print("\n" + "="*50 + "\n")
    
    print("=== 测试2: 使用用户自定义参数 ===")
    result2 = create_excel_read_template(
        file_path=file_path,
        sheet_name="复杂格式", 
        skiprows=3, 
        header=0, 
        usecols="A:D"
    )
    print(f"最终参数: {result2['recommended_params']}")
    print(f"生成的代码:\n{result2['code_template']}")
    print("\n" + "="*50 + "\n")
    
    print("=== 测试3: 部分用户参数 ===")
    result3 = create_excel_read_template(
        file_path=file_path,
        sheet_name="复杂格式", 
        skiprows=1
    )
    print(f"最终参数: {result3['recommended_params']}")
    print(f"生成的代码:\n{result3['code_template']}")

if __name__ == "__main__":
    test_parameter_passing()