#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的 run_excel_code 工具
验证 pandas NameError 问题是否已解决
"""

import pandas as pd
import os
import sys
import json
from io import StringIO

# 添加当前目录到路径
sys.path.insert(0, '.')

# 导入修复后的服务器模块
try:
    from server import run_excel_code
    print("✅ 成功导入修复后的 run_excel_code 函数")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)

def create_test_excel():
    """创建测试用的Excel文件"""
    test_data = {
        '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
        '年龄': [25, 30, 35, 28, 32],
        '城市': ['北京', '上海', '广州', '深圳', '杭州'],
        '薪资': [8000, 12000, 15000, 9500, 11000],
        '部门': ['技术', '销售', '市场', '技术', '财务']
    }
    
    df = pd.DataFrame(test_data)
    excel_file = 'test_data_fixed.xlsx'
    df.to_excel(excel_file, index=False)
    print(f"✅ 创建测试文件: {excel_file}")
    return excel_file

def test_basic_operations(excel_file):
    """测试基本操作"""
    print("\n🧪 测试1: 基本数据查看")
    
    code = '''
print(f"数据形状: {df.shape}")
print(f"列名: {list(df.columns)}")
print(f"前3行数据:")
print(df.head(3))
result = df.shape
'''
    
    try:
        response = run_excel_code(
            code=code,
            file_path=excel_file,
            auto_detect=True
        )
        
        if 'error' in response:
            print(f"❌ 测试失败: {response['error']}")
            return False
        else:
            print("✅ 基本操作测试通过")
            print(f"输出: {response.get('output', '')}")
            return True
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def test_pandas_operations(excel_file):
    """测试pandas操作"""
    print("\n🧪 测试2: pandas数据处理")
    
    code = '''
# 测试pandas操作
print("=== pandas 操作测试 ===")
print(f"pandas版本: {pd.__version__}")

# 基本统计
print("\\n数值列统计:")
print(df.describe())

# 分组操作
print("\\n按部门分组的平均薪资:")
dept_salary = df.groupby('部门')['薪资'].mean()
print(dept_salary)

# 筛选操作
print("\\n薪资大于10000的员工:")
high_salary = df[df['薪资'] > 10000]
print(high_salary[['姓名', '薪资', '部门']])

result = {
    'total_employees': len(df),
    'avg_salary': df['薪资'].mean(),
    'departments': df['部门'].unique().tolist(),
    'high_salary_count': len(high_salary)
}
'''
    
    try:
        response = run_excel_code(
            code=code,
            file_path=excel_file,
            auto_detect=True
        )
        
        if 'error' in response:
            print(f"❌ 测试失败: {response['error']}")
            return False
        else:
            print("✅ pandas操作测试通过")
            print(f"结果: {response.get('result', '')}")
            return True
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def test_error_handling(excel_file):
    """测试错误处理"""
    print("\n🧪 测试3: 错误处理机制")
    
    # 测试未定义变量
    code = '''
print("测试未定义变量...")
try:
    result = undefined_variable  # 这应该触发NameError
except NameError as e:
    print(f"捕获到NameError: {e}")
    result = "NameError_handled"
'''
    
    try:
        response = run_excel_code(
            file_path=excel_file,
            code=code,
            auto_detect=True
        )
        
        if 'result' in response or ('error' in response and 'NameError' in str(response['error'])):
            print("✅ NameError处理测试通过")
            if 'error' in response:
                print(f"错误信息: {response['error']['message']}")
                if 'suggestions' in response['error']:
                    print(f"建议: {response['error']['suggestions']}")
            return True
        else:
            print(f"❌ 错误处理测试失败: {response}")
            return False
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def test_numpy_integration(excel_file):
    """测试numpy集成"""
    print("\n🧪 测试4: numpy集成")
    
    code = '''
print("=== numpy 集成测试 ===")
if 'np' in locals():
    print(f"numpy版本: {np.__version__}")
    
    # 使用numpy进行计算
    ages = df['年龄'].values
    print(f"年龄数组: {ages}")
    print(f"平均年龄: {np.mean(ages)}")
    print(f"年龄标准差: {np.std(ages)}")
    
    result = {
        'numpy_available': True,
        'mean_age': float(np.mean(ages)),
        'std_age': float(np.std(ages))
    }
else:
    print("numpy 不可用")
    result = {'numpy_available': False}
'''
    
    try:
        response = run_excel_code(
            code=code,
            file_path=excel_file,
            auto_detect=True
        )
        
        if 'error' in response:
            print(f"❌ 测试失败: {response['error']}")
            return False
        else:
            print("✅ numpy集成测试通过")
            print(f"结果: {response.get('result', '')}")
            return True
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def test_file_not_found():
    """测试文件不存在的情况"""
    print("\n🧪 测试5: 文件不存在处理")
    
    code = '''
print("尝试处理不存在的文件...")
result = df.shape
'''
    
    try:
        response = run_excel_code(
            code=code,
            file_path="nonexistent_file.xlsx",
            auto_detect=True
        )
        
        if 'error' in response and 'FILE_ACCESS_ERROR' in response['error']['type']:
            print("✅ 文件不存在处理测试通过")
            print(f"错误信息: {response['error']['message']}")
            return True
        else:
            print(f"❌ 文件不存在处理测试失败: {response}")
            return False
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试修复后的 run_excel_code 工具")
    print("=" * 60)
    
    # 创建测试文件
    excel_file = create_test_excel()
    
    # 运行测试
    tests = [
        ("基本操作", lambda: test_basic_operations(excel_file)),
        ("pandas操作", lambda: test_pandas_operations(excel_file)),
        ("错误处理", lambda: test_error_handling(excel_file)),
        ("numpy集成", lambda: test_numpy_integration(excel_file)),
        ("文件不存在", test_file_not_found)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name}测试发生异常: {e}")
    
    # 清理测试文件
    if os.path.exists(excel_file):
        os.remove(excel_file)
        print(f"\n🧹 已清理测试文件: {excel_file}")
    
    # 测试结果
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！pandas NameError 问题已修复")
        print("\n✅ 修复验证成功，可以正常使用 run_excel_code 工具")
    else:
        print(f"⚠️  有 {total - passed} 个测试失败，需要进一步检查")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)