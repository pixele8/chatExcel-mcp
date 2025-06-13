#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel智能处理功能演示脚本

本脚本演示了chatExcel的所有Excel处理增强功能：
1. 智能参数推荐
2. Excel文件结构检测
3. 代码模板生成
4. 增强的Excel读取和代码执行
"""

import pandas as pd
import numpy as np
from server import read_excel_metadata, run_excel_code
from excel_smart_tools import (
    suggest_excel_read_parameters,
    detect_excel_file_structure,
    create_excel_read_template
)
import os

def create_demo_excel():
    """创建演示用的Excel文件"""
    print("📊 创建演示Excel文件...")
    
    with pd.ExcelWriter('demo_data.xlsx', engine='xlsxwriter') as writer:
        # 工作表1：标准数据
        df1 = pd.DataFrame({
            '产品名称': ['iPhone 15', 'MacBook Pro', 'iPad Air', 'Apple Watch', 'AirPods'],
            '销售量': [1200, 800, 600, 1500, 2000],
            '单价': [6999, 12999, 4599, 2999, 1299],
            '销售额': [8398800, 10399200, 2759400, 4498500, 2598000],
            '利润率': [0.25, 0.30, 0.28, 0.35, 0.40]
        })
        df1.to_excel(writer, sheet_name='产品销售数据', index=False)
        
        # 工作表2：带标题行的数据
        title_data = [['', '', '2024年第一季度销售报告', '', ''],
                     ['', '', '', '', ''],
                     ['地区', 'Q1销售额', 'Q2销售额', 'Q3销售额', '年度总计']]
        
        df2 = pd.DataFrame({
            '地区': ['北京', '上海', '广州', '深圳', '杭州'],
            'Q1销售额': [2500000, 3200000, 2800000, 3500000, 1800000],
            'Q2销售额': [2800000, 3600000, 3100000, 3800000, 2100000],
            'Q3销售额': [3100000, 3900000, 3400000, 4100000, 2300000],
            '年度总计': [8400000, 10700000, 9300000, 11400000, 6200000]
        })
        
        # 写入标题行
        worksheet = writer.book.add_worksheet('季度销售报告')
        for i, row in enumerate(title_data):
            for j, value in enumerate(row):
                worksheet.write(i, j, value)
        
        # 写入数据（从第4行开始）
        df2.to_excel(writer, sheet_name='季度销售报告', startrow=3, index=False)
    
    print("✅ 演示Excel文件创建完成: demo_data.xlsx")
    return 'demo_data.xlsx'

def demo_smart_parameter_suggestion(file_path):
    """演示智能参数推荐功能"""
    print("\n🧠 智能参数推荐功能演示")
    print("=" * 50)
    
    # 分析不同工作表
    sheets = ['产品销售数据', '季度销售报告']
    
    for sheet in sheets:
        print(f"\n📋 分析工作表: {sheet}")
        result = suggest_excel_read_parameters(file_path, sheet)
        
        print(f"推荐参数: {result.get('recommended_params', {})}")
        
        if result.get('warnings'):
            print("⚠️  警告:")
            for warning in result['warnings']:
                print(f"   - {warning}")
        
        if result.get('tips'):
            print("💡 提示:")
            for tip in result['tips']:
                print(f"   - {tip}")

def demo_structure_detection(file_path):
    """演示Excel文件结构检测功能"""
    print("\n🔍 Excel文件结构检测演示")
    print("=" * 50)
    
    result = detect_excel_file_structure(file_path)
    
    print(f"检测到 {len(result.get('sheets', []))} 个工作表:")
    for sheet in result.get('sheets', []):
        print(f"  📄 {sheet.get('name', 'Unknown')}: {sheet.get('rows', 0)}行 x {sheet.get('columns', 0)}列")
    
    if result.get('merged_cells'):
        print(f"\n🔗 合并单元格: {len(result['merged_cells'])} 个")
    
    if result.get('data_range'):
        print(f"📊 数据范围: {result['data_range']}")

def demo_template_generation(file_path):
    """演示代码模板生成功能"""
    print("\n📝 代码模板生成演示")
    print("=" * 50)
    
    sheets = ['产品销售数据', '季度销售报告']
    
    for sheet in sheets:
        print(f"\n📋 为工作表 '{sheet}' 生成代码模板:")
        result = create_excel_read_template(file_path, sheet)
        
        if result.get('code_template'):
            print("生成的代码:")
            print("-" * 40)
            print(result['code_template'])
            print("-" * 40)
        
        if result.get('tips'):
            print("💡 使用提示:")
            for tip in result['tips']:
                print(f"   - {tip}")

def demo_enhanced_metadata_reading(file_path):
    """演示增强的元数据读取功能"""
    print("\n📊 增强的元数据读取演示")
    print("=" * 50)
    
    # 读取标准工作表
    print("\n📋 读取标准工作表 '产品销售数据':")
    result1 = read_excel_metadata(file_path, sheet_name='产品销售数据')
    print(f"状态: {result1.get('status', 'UNKNOWN')}")
    print(f"数据集信息: {result1.get('dataset', {})}")
    print(f"列数: {len(result1.get('columns_metadata', []))}")
    
    # 读取带标题的工作表（使用推荐参数）
    print("\n📋 读取带标题工作表 '季度销售报告' (使用智能参数):")
    result2 = read_excel_metadata(file_path, sheet_name='季度销售报告', skiprows=3, header=0)
    print(f"状态: {result2.get('status', 'UNKNOWN')}")
    print(f"数据集信息: {result2.get('dataset', {})}")
    print(f"列数: {len(result2.get('columns_metadata', []))}")

def demo_enhanced_code_execution(file_path):
    """演示增强的代码执行功能"""
    print("\n⚡ 增强的代码执行演示")
    print("=" * 50)
    
    # 分析产品销售数据
    print("\n📊 分析产品销售数据:")
    code1 = """
print("=== 产品销售分析 ===")
print(f"总销售额: {df['销售额'].sum():,} 元")
print(f"平均利润率: {df['利润率'].mean():.1%}")
print(f"最畅销产品: {df.loc[df['销售量'].idxmax(), '产品名称']}")
print(f"最高单价产品: {df.loc[df['单价'].idxmax(), '产品名称']}")
"""
    
    result1 = run_excel_code(code1, file_path, sheet_name='产品销售数据')
    if result1.get('output'):
        print(result1['output'])
    
    # 分析季度销售数据（使用参数）
    print("\n📈 分析季度销售数据:")
    code2 = """
print("=== 季度销售分析 ===")
print(f"年度总销售额: {df['年度总计'].sum():,} 元")
print(f"最佳销售地区: {df.loc[df['年度总计'].idxmax(), '地区']}")
print(f"平均季度增长率: {((df['Q3销售额'] / df['Q1销售额']) - 1).mean():.1%}")
"""
    
    result2 = run_excel_code(code2, file_path, sheet_name='季度销售报告', skiprows=3, header=0)
    if result2.get('output'):
        print(result2['output'])

def main():
    """主演示函数"""
    print("🎯 Excel智能处理功能完整演示")
    print("=" * 60)
    
    try:
        # 创建演示数据
        file_path = create_demo_excel()
        
        # 演示各项功能
        demo_smart_parameter_suggestion(file_path)
        demo_structure_detection(file_path)
        demo_template_generation(file_path)
        demo_enhanced_metadata_reading(file_path)
        demo_enhanced_code_execution(file_path)
        
        print("\n🎉 演示完成！")
        print("\n📋 功能总结:")
        print("  ✅ 智能参数推荐 - 自动分析Excel结构并推荐最佳读取参数")
        print("  ✅ 结构检测 - 详细分析Excel文件的工作表、合并单元格等信息")
        print("  ✅ 代码模板生成 - 根据分析结果生成Excel读取代码")
        print("  ✅ 增强元数据读取 - 支持skiprows、header、usecols等参数")
        print("  ✅ 增强代码执行 - 支持复杂Excel格式的数据分析")
        
    except Exception as e:
        print(f"❌ 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理演示文件
        if os.path.exists('demo_data.xlsx'):
            os.remove('demo_data.xlsx')
            print("\n🧹 已清理演示文件")

if __name__ == "__main__":
    main()