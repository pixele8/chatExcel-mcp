#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试当前修复对多级列头处理的影响
"""

import pandas as pd
import os
from server import run_excel_code
from excel_helper import _suggest_excel_read_parameters
from enhanced_excel_helper import smart_read_excel

def create_multiheader_test_file():
    """创建包含多级列头的测试文件"""
    # 创建多级列头数据
    data = [
        ['销售数据', '销售数据', '销售数据', '财务数据', '财务数据'],  # 第一级标题
        ['产品A', '产品B', '产品C', '收入', '支出'],  # 第二级标题
        [100, 200, 150, 1000, 800],  # 数据行1
        [120, 180, 160, 1200, 900],  # 数据行2
        [110, 220, 140, 1100, 850],  # 数据行3
    ]
    
    df = pd.DataFrame(data)
    excel_file = 'multiheader_test.xlsx'
    df.to_excel(excel_file, index=False, header=False)
    return excel_file

def create_simple_header_test_file():
    """创建简单单级列头的测试文件"""
    data = {
        '姓名': ['张三', '李四', '王五'],
        '年龄': [25, 30, 35],
        '部门': ['技术', '销售', '市场']
    }
    
    df = pd.DataFrame(data)
    excel_file = 'simple_header_test.xlsx'
    df.to_excel(excel_file, index=False)
    return excel_file

def test_parameter_suggestions(excel_file, file_description):
    """测试参数建议功能"""
    print(f"\n🔍 测试 {file_description} 的参数建议")
    print("=" * 50)
    
    try:
        suggestions = _suggest_excel_read_parameters(excel_file)
        print(f"建议参数: {suggestions['recommended_params']}")
        print(f"多级列头检测: {suggestions['analysis'].get('multi_level_header_detected', False)}")
        
        if suggestions['warnings']:
            print(f"警告: {suggestions['warnings']}")
        if suggestions['tips']:
            print(f"提示: {suggestions['tips']}")
            
        return suggestions
    except Exception as e:
        print(f"❌ 参数建议失败: {e}")
        return None

def test_smart_read_excel(excel_file, file_description):
    """测试智能读取功能"""
    print(f"\n📖 测试 {file_description} 的智能读取")
    print("=" * 50)
    
    # 测试自动检测模式
    print("\n1. 自动检测模式 (auto_detect_params=True):")
    try:
        result = smart_read_excel(excel_file, auto_detect_params=True)
        if result['success']:
            df = result['dataframe']
            print(f"  ✅ 读取成功")
            print(f"  数据形状: {df.shape}")
            print(f"  列名: {list(df.columns)}")
            print(f"  前3行数据:")
            print(df.head(3).to_string(index=False))
        else:
            print(f"  ❌ 读取失败: {result.get('errors', [])}")
    except Exception as e:
        print(f"  ❌ 异常: {e}")
    
    # 测试禁用自动检测模式（当前修复的方式）
    print("\n2. 禁用自动检测模式 (auto_detect_params=False, header=0):")
    try:
        result = smart_read_excel(excel_file, auto_detect_params=False, header=0)
        if result['success']:
            df = result['dataframe']
            print(f"  ✅ 读取成功")
            print(f"  数据形状: {df.shape}")
            print(f"  列名: {list(df.columns)}")
            print(f"  前3行数据:")
            print(df.head(3).to_string(index=False))
        else:
            print(f"  ❌ 读取失败: {result.get('errors', [])}")
    except Exception as e:
        print(f"  ❌ 异常: {e}")

def test_run_excel_code(excel_file, file_description):
    """测试run_excel_code功能"""
    print(f"\n🔧 测试 {file_description} 的run_excel_code")
    print("=" * 50)
    
    code = '''
print(f"数据形状: {df.shape}")
print(f"列名: {list(df.columns)}")
print("前3行数据:")
print(df.head(3))

# 尝试访问列
try:
    if len(df.columns) > 0:
        first_col = df.iloc[:, 0]
        print(f"\n第一列数据: {first_col.tolist()}")
except Exception as e:
    print(f"访问列数据失败: {e}")
'''
    
    try:
        response = run_excel_code(
            code=code,
            file_path=excel_file,
            auto_detect=True
        )
        
        if 'error' in response:
            print(f"❌ 执行失败: {response['error']}")
        elif 'result' in response:
            print(f"✅ 执行成功")
            if 'output' in response:
                print(f"输出:\n{response['output']}")
        else:
            print(f"⚠️ 未知响应格式: {response}")
            
    except Exception as e:
        print(f"❌ 异常: {e}")

def main():
    """主测试函数"""
    print("🧪 测试当前修复对多级列头处理的影响")
    print("=" * 60)
    
    # 创建测试文件
    multiheader_file = create_multiheader_test_file()
    simple_file = create_simple_header_test_file()
    
    try:
        # 测试多级列头文件
        print("\n" + "=" * 60)
        print("📊 多级列头文件测试")
        print("=" * 60)
        
        test_parameter_suggestions(multiheader_file, "多级列头文件")
        test_smart_read_excel(multiheader_file, "多级列头文件")
        test_run_excel_code(multiheader_file, "多级列头文件")
        
        # 测试简单列头文件
        print("\n" + "=" * 60)
        print("📋 简单列头文件测试")
        print("=" * 60)
        
        test_parameter_suggestions(simple_file, "简单列头文件")
        test_smart_read_excel(simple_file, "简单列头文件")
        test_run_excel_code(simple_file, "简单列头文件")
        
        # 分析结论
        print("\n" + "=" * 60)
        print("📝 分析结论")
        print("=" * 60)
        print("""
当前修复方案的影响分析:

1. 优点:
   - 解决了简单列头文件的读取问题
   - 避免了错误的参数建议导致的列名识别错误
   
2. 潜在缺陷:
   - 强制设置header=0可能无法正确处理多级列头
   - 忽略了excel_helper.py中的多级列头检测逻辑
   - 可能导致复杂Excel文件结构的误读
   
3. 建议:
   - 需要更智能的参数选择策略
   - 保留多级列头检测能力的同时修复简单列头问题
        """)
        
    finally:
        # 清理测试文件
        for file in [multiheader_file, simple_file]:
            if os.path.exists(file):
                os.remove(file)
                print(f"🧹 已清理测试文件: {file}")

if __name__ == "__main__":
    main()