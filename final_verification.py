#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终验证脚本：确认pandas分组操作问题已修复
"""

import pandas as pd
import os
import sys
from server import run_excel_code

def test_basic_groupby():
    """测试基本分组操作"""
    print("🧪 测试基本分组操作")
    
    # 创建测试数据
    test_data = {
        '姓名': ['张三', '李四', '王五', '赵六'],
        '部门': ['技术', '销售', '技术', '销售'],
        '薪资': [8000, 12000, 9000, 11000]
    }
    
    df = pd.DataFrame(test_data)
    excel_file = 'groupby_test.xlsx'
    df.to_excel(excel_file, index=False)
    
    try:
        # 测试分组操作
        code = '''
print("=== 分组操作测试 ===")
print(f"数据形状: {df.shape}")
print(f"列名: {list(df.columns)}")
print("按部门分组的平均薪资:")
result = df.groupby('部门')['薪资'].mean()
print(result)
print(f"结果类型: {type(result)}")
'''
        
        response = run_excel_code(
            code=code,
            file_path=excel_file,
            auto_detect=False  # 关闭自动检测避免干扰
        )
        
        if 'error' in response:
            print(f"❌ 分组操作失败: {response['error']}")
            return False
        else:
            print("✅ 分组操作成功")
            print(f"输出:\n{response.get('output', '')}")
            return True
            
    finally:
        if os.path.exists(excel_file):
            os.remove(excel_file)

def test_complex_operations():
    """测试复杂操作"""
    print("\n🧪 测试复杂pandas操作")
    
    # 创建更复杂的测试数据
    test_data = {
        '员工ID': [1, 2, 3, 4, 5],
        '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
        '部门': ['技术', '销售', '技术', '销售', '财务'],
        '薪资': [8000, 12000, 9000, 11000, 10000],
        '年龄': [25, 30, 28, 32, 29]
    }
    
    df = pd.DataFrame(test_data)
    excel_file = 'complex_test.xlsx'
    df.to_excel(excel_file, index=False)
    
    try:
        code = '''
print("=== 复杂操作测试 ===")

# 多列分组
print("1. 按部门统计:")
dept_stats = df.groupby('部门').agg({
    '薪资': ['mean', 'max', 'min'],
    '年龄': 'mean'
})
print(dept_stats)

# 筛选和分组
print("2. 高薪员工分组:")
high_salary = df[df['薪资'] > 9000]
print(high_salary.groupby('部门')['薪资'].count())

# 排序操作
print("3. 按薪资排序:")
sorted_df = df.sort_values('薪资', ascending=False)
print(sorted_df[['姓名', '部门', '薪资']].head(3))

result = {
    'total_employees': len(df),
    'departments': df['部门'].nunique(),
    'avg_salary': df['薪资'].mean(),
    'max_salary': df['薪资'].max()
}
'''
        
        response = run_excel_code(
            code=code,
            file_path=excel_file,
            auto_detect=False
        )
        
        if 'error' in response:
            print(f"❌ 复杂操作失败: {response['error']}")
            return False
        else:
            print("✅ 复杂操作成功")
            print(f"结果: {response.get('result', '')}")
            return True
            
    finally:
        if os.path.exists(excel_file):
            os.remove(excel_file)

def main():
    """主测试函数"""
    print("🚀 最终验证：pandas分组操作修复测试")
    print("=" * 50)
    
    tests = [
        ("基本分组操作", test_basic_groupby),
        ("复杂pandas操作", test_complex_operations)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 通过")
            else:
                print(f"❌ {test_name} 失败")
        except Exception as e:
            print(f"❌ {test_name} 异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 最终结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！pandas分组操作问题已完全修复")
        print("✅ run_excel_code工具现在可以正常处理pandas分组操作")
        return True
    else:
        print(f"⚠️ 还有 {total - passed} 个测试失败")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)