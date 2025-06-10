#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门测试 run_excel_code 中 pandas NameError 问题
"""

import pandas as pd
import numpy as np
import os
from server import run_excel_code

def create_test_data():
    """创建测试数据"""
    data = {
        '姓名': ['张三', '李四', '王五', '赵六'],
        '年龄': [25, 30, 35, 28],
        '部门': ['技术部', '销售部', '人事部', '财务部'],
        '薪资': [8000, 6000, 7000, 7500]
    }
    df = pd.DataFrame(data)
    test_file = 'test_pandas_error.xlsx'
    df.to_excel(test_file, index=False)
    print(f"✅ 创建测试文件: {test_file}")
    return test_file, df

def test_case_1_basic_pandas():
    """测试用例1：基本 pandas 操作"""
    print("\n=== 测试用例1：基本 pandas 操作 ===")
    
    test_file, original_df = create_test_data()
    
    code = """
# 基本信息
print(f"pandas 版本: {pd.__version__}")
print(f"数据形状: {df.shape}")
print(f"列名: {list(df.columns)}")

# 基本统计
result = df.describe()
print("\n描述性统计:")
print(result)
"""
    
    try:
        result = run_excel_code(code, test_file)
        print("✅ 测试用例1 - 成功")
        print(f"输出: {result.get('output', 'No output')}")
        if 'error' in result:
            print(f"❌ 错误: {result['error']}")
    except Exception as e:
        print(f"❌ 测试用例1 - 异常: {e}")
    
    return test_file

def test_case_2_without_import():
    """测试用例2：不显式导入 pandas"""
    print("\n=== 测试用例2：不显式导入 pandas ===")
    
    test_file = 'test_pandas_error.xlsx'
    
    code = """
# 直接使用 pd，不导入
print(f"直接使用 pd: {pd.__version__}")
print(f"数据类型: {type(df)}")
print(f"数据形状: {df.shape}")

# 进行一些操作
result = df.groupby('部门')['薪资'].mean()
print("\n各部门平均薪资:")
print(result)
"""
    
    try:
        result = run_excel_code(code, test_file)
        print("✅ 测试用例2 - 成功")
        print(f"输出: {result.get('output', 'No output')}")
        if 'error' in result:
            print(f"❌ 错误: {result['error']}")
    except Exception as e:
        print(f"❌ 测试用例2 - 异常: {e}")

def test_case_3_reimport_pandas():
    """测试用例3：重新导入 pandas"""
    print("\n=== 测试用例3：重新导入 pandas ===")
    
    test_file = 'test_pandas_error.xlsx'
    
    code = """
# 重新导入 pandas
import pandas as pd
import numpy as np

print(f"重新导入 pandas 版本: {pd.__version__}")
print(f"numpy 版本: {np.__version__}")

# 检查 df 是否还存在
if 'df' in locals():
    print(f"df 仍然存在，形状: {df.shape}")
    result = df.head()
else:
    print("df 不存在，需要重新读取")
    result = "df not found"
"""
    
    try:
        result = run_excel_code(code, test_file)
        print("✅ 测试用例3 - 成功")
        print(f"输出: {result.get('output', 'No output')}")
        if 'error' in result:
            print(f"❌ 错误: {result['error']}")
    except Exception as e:
        print(f"❌ 测试用例3 - 异常: {e}")

def test_case_4_namespace_check():
    """测试用例4：检查命名空间"""
    print("\n=== 测试用例4：检查命名空间 ===")
    
    test_file = 'test_pandas_error.xlsx'
    
    code = """
# 检查当前命名空间
print("=== 命名空间检查 ===")
print(f"locals() 中的变量: {sorted(locals().keys())}")
print(f"globals() 中的变量: {sorted([k for k in globals().keys() if not k.startswith('_')])}")

# 检查特定变量
vars_to_check = ['pd', 'np', 'df', 'pandas', 'numpy']
for var in vars_to_check:
    if var in locals():
        print(f"✅ {var} 在 locals() 中: {type(locals()[var])}")
    elif var in globals():
        print(f"✅ {var} 在 globals() 中: {type(globals()[var])}")
    else:
        print(f"❌ {var} 不存在")

result = "命名空间检查完成"
"""
    
    try:
        result = run_excel_code(code, test_file)
        print("✅ 测试用例4 - 成功")
        print(f"输出: {result.get('output', 'No output')}")
        if 'error' in result:
            print(f"❌ 错误: {result['error']}")
    except Exception as e:
        print(f"❌ 测试用例4 - 异常: {e}")

def test_case_5_force_error():
    """测试用例5：强制触发 NameError"""
    print("\n=== 测试用例5：强制触发 NameError ===")
    
    test_file = 'test_pandas_error.xlsx'
    
    code = """
# 删除 pd 变量然后尝试使用
if 'pd' in locals():
    del pd
    print("已删除 pd 变量")

# 尝试使用已删除的 pd
print(f"尝试使用 pd: {pd.__version__}")
result = "这不应该成功"
"""
    
    try:
        result = run_excel_code(code, test_file)
        print("🤔 测试用例5 - 意外成功")
        print(f"输出: {result.get('output', 'No output')}")
        if 'error' in result:
            print(f"✅ 预期错误: {result['error']}")
    except Exception as e:
        print(f"✅ 测试用例5 - 预期异常: {e}")

def main():
    """主函数"""
    print("🔍 开始测试 run_excel_code 中的 pandas NameError 问题")
    print("=" * 70)
    
    try:
        # 运行所有测试用例
        test_file = test_case_1_basic_pandas()
        test_case_2_without_import()
        test_case_3_reimport_pandas()
        test_case_4_namespace_check()
        test_case_5_force_error()
        
        print("\n" + "=" * 70)
        print("✅ 所有测试用例完成")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理测试文件
        test_files = ['test_pandas_error.xlsx']
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
                print(f"🗑️ 清理测试文件: {file}")

if __name__ == "__main__":
    main()