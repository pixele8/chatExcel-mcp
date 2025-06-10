#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建测试Excel文件用于演示create_excel_read_template_tool功能
"""

import pandas as pd
import os

def create_test_excel():
    """创建一个包含复杂格式的测试Excel文件"""
    
    # 创建测试数据
    data = {
        '产品名称': ['iPhone 15', 'Samsung Galaxy S24', 'Huawei P60', 'Xiaomi 14', 'OPPO Find X7'],
        '销售额(万元)': [1250.5, 980.3, 756.8, 645.2, 523.9],
        '销售数量(台)': [15000, 12500, 9800, 11200, 8900],
        '市场份额(%)': [28.5, 22.3, 17.2, 20.1, 11.9],
        '发布日期': ['2023-09-15', '2024-01-17', '2023-03-23', '2023-10-26', '2024-01-08']
    }
    
    df = pd.DataFrame(data)
    
    # 创建Excel文件路径
    excel_path = '/Users/wangdada/Downloads/mcp/excel-mcp/chatExcel-mcp-server/sample_data.xlsx'
    
    # 使用ExcelWriter创建包含多个工作表的Excel文件
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        # 工作表1: 标准数据
        df.to_excel(writer, sheet_name='销售数据', index=False)
        
        # 工作表2: 带有空行和标题的复杂格式
        complex_df = pd.DataFrame({
            '': ['', '', '2024年第一季度销售报告', '', '产品', '销售额', '增长率'],
            ' ': ['', '', '', '', 'iPhone 15', '1250.5', '15.2%'],
            '  ': ['', '', '', '', 'Samsung S24', '980.3', '8.7%'],
            '   ': ['', '', '', '', 'Huawei P60', '756.8', '-5.3%']
        })
        complex_df.to_excel(writer, sheet_name='复杂格式', index=False, header=False)
        
        # 工作表3: 包含合并单元格的数据
        summary_data = {
            '指标': ['总销售额', '平均销售额', '最高销售额', '最低销售额'],
            '数值': [4156.7, 831.34, 1250.5, 523.9],
            '单位': ['万元', '万元', '万元', '万元']
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='汇总数据', index=False)
    
    print(f"测试Excel文件已创建: {excel_path}")
    return excel_path

if __name__ == "__main__":
    create_test_excel()