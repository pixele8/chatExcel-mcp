#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进的Excel读取修复方案
既能处理简单列头又能保留多级列头检测能力
"""

import pandas as pd
import os
from excel_helper import _suggest_excel_read_parameters
from enhanced_excel_helper import smart_read_excel

def improved_smart_read_excel(file_path, auto_detect_params=True, **kwargs):
    """
    改进的智能Excel读取函数
    
    Args:
        file_path: Excel文件路径
        auto_detect_params: 是否启用自动参数检测
        **kwargs: 其他pandas.read_excel参数
    
    Returns:
        dict: 包含读取结果的字典
    """
    
    if not auto_detect_params:
        # 如果禁用自动检测，直接使用用户提供的参数
        return smart_read_excel(file_path, auto_detect_params=False, **kwargs)
    
    # 启用自动检测时的改进逻辑
    try:
        # 1. 获取参数建议
        suggestions = _suggest_excel_read_parameters(file_path)
        recommended_params = suggestions.get('recommended_params', {})
        
        # 2. 检查是否检测到多级列头
        is_multi_level = suggestions.get('analysis', {}).get('multi_level_header_detected', False)
        
        # 3. 智能参数选择策略
        if is_multi_level:
            # 对于多级列头，使用建议的参数
            final_params = recommended_params.copy()
            final_params.update(kwargs)  # 用户参数优先
            print(f"检测到多级列头，使用建议参数: {final_params}")
        else:
            # 对于简单列头，优先使用header=0，除非用户明确指定
            final_params = kwargs.copy()
            if 'header' not in final_params:
                # 检查建议的header参数是否合理
                suggested_header = recommended_params.get('header', 0)
                if isinstance(suggested_header, int) and suggested_header <= 2:
                    # 如果建议的header在合理范围内（0-2），使用建议值
                    final_params['header'] = suggested_header
                else:
                    # 否则使用默认的header=0
                    final_params['header'] = 0
                    print(f"建议的header={suggested_header}可能不合理，使用header=0")
            
            print(f"简单列头处理，使用参数: {final_params}")
        
        # 4. 尝试读取
        result = smart_read_excel(file_path, auto_detect_params=False, **final_params)
        
        # 5. 验证读取结果
        if result['success']:
            df = result['dataframe']
            
            # 检查列名质量
            unnamed_cols = [col for col in df.columns if 'Unnamed' in str(col)]
            if len(unnamed_cols) > len(df.columns) * 0.5:  # 超过一半是未命名列
                print(f"警告: 检测到过多未命名列({len(unnamed_cols)}/{len(df.columns)})，尝试header=0")
                # 回退到header=0
                fallback_params = kwargs.copy()
                fallback_params['header'] = 0
                result = smart_read_excel(file_path, auto_detect_params=False, **fallback_params)
        
        return result
        
    except Exception as e:
        print(f"自动检测失败: {e}，回退到header=0")
        # 出错时回退到简单的header=0
        fallback_params = kwargs.copy()
        fallback_params['header'] = 0
        return smart_read_excel(file_path, auto_detect_params=False, **fallback_params)

def create_test_files():
    """创建测试文件"""
    # 1. 简单列头文件
    simple_data = {
        '姓名': ['张三', '李四', '王五'],
        '年龄': [25, 30, 35],
        '部门': ['技术', '销售', '市场']
    }
    simple_df = pd.DataFrame(simple_data)
    simple_file = 'test_simple.xlsx'
    simple_df.to_excel(simple_file, index=False)
    
    # 2. 多级列头文件
    multi_data = [
        ['销售数据', '销售数据', '销售数据', '财务数据', '财务数据'],  # 第一级
        ['产品A', '产品B', '产品C', '收入', '支出'],  # 第二级
        [100, 200, 150, 1000, 800],
        [120, 180, 160, 1200, 900],
        [110, 220, 140, 1100, 850],
    ]
    multi_df = pd.DataFrame(multi_data)
    multi_file = 'test_multi.xlsx'
    multi_df.to_excel(multi_file, index=False, header=False)
    
    # 3. 复杂格式文件（有空行）
    complex_data = [
        ['', '', '', '', ''],  # 空行
        ['公司报表', '', '', '', ''],  # 标题行
        ['', '', '', '', ''],  # 空行
        ['姓名', '年龄', '部门', '薪资', '城市'],  # 列头
        ['张三', 25, '技术', 8000, '北京'],
        ['李四', 30, '销售', 12000, '上海'],
    ]
    complex_df = pd.DataFrame(complex_data)
    complex_file = 'test_complex.xlsx'
    complex_df.to_excel(complex_file, index=False, header=False)
    
    return simple_file, multi_file, complex_file

def test_improved_function():
    """测试改进的函数"""
    print("🧪 测试改进的Excel读取函数")
    print("=" * 50)
    
    simple_file, multi_file, complex_file = create_test_files()
    
    test_cases = [
        (simple_file, "简单列头文件"),
        (multi_file, "多级列头文件"),
        (complex_file, "复杂格式文件")
    ]
    
    try:
        for file_path, description in test_cases:
            print(f"\n📋 测试 {description}")
            print("-" * 30)
            
            # 测试改进的函数
            result = improved_smart_read_excel(file_path, auto_detect_params=True)
            
            if result['success']:
                df = result['dataframe']
                print(f"✅ 读取成功")
                print(f"  数据形状: {df.shape}")
                print(f"  列名: {list(df.columns)}")
                print(f"  前3行数据:")
                print(df.head(3).to_string(index=False, max_cols=10))
                
                # 检查列名质量
                unnamed_cols = [col for col in df.columns if 'Unnamed' in str(col)]
                if unnamed_cols:
                    print(f"  ⚠️ 未命名列: {len(unnamed_cols)}个")
                else:
                    print(f"  ✅ 所有列都有合适的名称")
            else:
                print(f"❌ 读取失败: {result.get('errors', [])}")
    
    finally:
        # 清理测试文件
        for file in [simple_file, multi_file, complex_file]:
            if os.path.exists(file):
                os.remove(file)
                print(f"🧹 已清理: {file}")

def generate_server_patch():
    """生成server.py的改进补丁"""
    print("\n📝 生成server.py改进补丁")
    print("=" * 50)
    
    patch_code = '''
# 在server.py中替换原有的Excel读取逻辑

def improved_run_excel_code_logic(file_path, read_kwargs):
    """
    改进的Excel读取逻辑
    """
    from excel_helper import _suggest_excel_read_parameters
    
    try:
        # 1. 获取参数建议
        suggestions = _suggest_excel_read_parameters(file_path)
        recommended_params = suggestions.get('recommended_params', {})
        
        # 2. 检查是否检测到多级列头
        is_multi_level = suggestions.get('analysis', {}).get('multi_level_header_detected', False)
        
        # 3. 智能参数选择
        if is_multi_level:
            # 多级列头：使用建议参数
            final_params = recommended_params.copy()
            final_params.update(read_kwargs)
        else:
            # 简单列头：优先使用header=0
            final_params = read_kwargs.copy()
            if 'header' not in final_params:
                suggested_header = recommended_params.get('header', 0)
                if isinstance(suggested_header, int) and suggested_header <= 2:
                    final_params['header'] = suggested_header
                else:
                    final_params['header'] = 0
        
        # 4. 执行读取
        read_result = smart_read_excel(file_path, auto_detect_params=False, **final_params)
        
        # 5. 验证并可能回退
        if read_result['success']:
            df = read_result['dataframe']
            unnamed_cols = [col for col in df.columns if 'Unnamed' in str(col)]
            if len(unnamed_cols) > len(df.columns) * 0.5:
                # 回退到header=0
                fallback_params = read_kwargs.copy()
                fallback_params['header'] = 0
                read_result = smart_read_excel(file_path, auto_detect_params=False, **fallback_params)
        
        return read_result
        
    except Exception as e:
        # 出错时回退
        fallback_params = read_kwargs.copy()
        fallback_params['header'] = 0
        return smart_read_excel(file_path, auto_detect_params=False, **fallback_params)

# 替换server.py中第756-758行的代码：
# 原代码：
#   read_kwargs['header'] = 0
#   read_result = smart_read_excel(file_path, auto_detect_params=False, **read_kwargs)
# 
# 新代码：
#   read_result = improved_run_excel_code_logic(file_path, read_kwargs)
'''
    
    print(patch_code)
    
    return patch_code

if __name__ == "__main__":
    test_improved_function()
    generate_server_patch()