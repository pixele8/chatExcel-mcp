#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的MCP客户端测试脚本

直接导入server.py中的run_excel_code函数进行测试
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_run_excel_code_direct():
    """
    直接测试run_excel_code函数
    """
    print("🚀 开始直接测试run_excel_code函数...")
    
    # 导入server模块
    try:
        import server
        print("✅ 成功导入server模块")
    except Exception as e:
        print(f"❌ 导入server模块失败: {e}")
        return
    
    # 检查run_excel_code函数是否存在
    if not hasattr(server, 'run_excel_code'):
        print("❌ server模块中未找到run_excel_code函数")
        return
    
    print("✅ 找到run_excel_code函数")
    
    # 测试文件路径
    test_file = str(project_root / "test_data.xlsx")
    
    if not os.path.exists(test_file):
        print(f"❌ 测试文件不存在: {test_file}")
        return
    
    print(f"✅ 测试文件存在: {test_file}")
    
    # 测试用例1: 基本数据查看
    print("\n📊 测试用例1: 基本数据查看")
    code1 = """
# 查看数据基本信息
print(f"数据形状: {df.shape}")
print(f"列名: {list(df.columns)}")
print(f"数据类型:\n{df.dtypes}")
print(f"前5行数据:\n{df.head()}")
result = {
    "shape": df.shape,
    "columns": list(df.columns),
    "dtypes": df.dtypes.to_dict(),
    "head": df.head().to_dict()
}
"""
    
    try:
        result1 = server.run_excel_code(
            file_path=test_file,
            code=code1
        )
        print("✅ 测试用例1执行成功")
        print(f"执行状态: {result1.get('success', 'unknown')}")
        if result1.get('success'):
            print(f"输出: {result1.get('output', 'no output')}")
            print(f"结果: {result1.get('result', 'no result')}")
        else:
            print(f"错误: {result1.get('error', 'unknown error')}")
    except Exception as e:
        print(f"❌ 测试用例1执行失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试用例2: 简单统计
    print("\n📈 测试用例2: 简单统计")
    code2 = """
# 简单统计
print(f"数据行数: {len(df)}")
print(f"数值列统计:\n{df.select_dtypes(include=['number']).describe()}")
result = {
    "row_count": len(df),
    "numeric_stats": df.select_dtypes(include=['number']).describe().to_dict()
}
"""
    
    try:
        result2 = server.run_excel_code(
            file_path=test_file,
            code=code2
        )
        print("✅ 测试用例2执行成功")
        print(f"执行状态: {result2.get('success', 'unknown')}")
        if result2.get('success'):
            print(f"输出: {result2.get('output', 'no output')}")
            print(f"结果: {result2.get('result', 'no result')}")
        else:
            print(f"错误: {result2.get('error', 'unknown error')}")
    except Exception as e:
        print(f"❌ 测试用例2执行失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎉 直接测试完成")

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
    test_run_excel_code_direct()