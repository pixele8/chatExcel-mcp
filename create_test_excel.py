#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建测试Excel文件
"""

import pandas as pd
import numpy as np

# 创建测试数据
data = {
    '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
    '年龄': [25, 30, 35, 28, 32],
    '工资': [5000, 8000, 12000, 6500, 9500],
    '部门': ['销售', '技术', '管理', '销售', '技术'],
    '入职日期': pd.date_range('2020-01-01', periods=5, freq='6M')
}

df = pd.DataFrame(data)

# 保存为Excel文件
output_path = '/Users/wangdada/Downloads/mcp/chatExcel-mcp/test_data.xlsx'
df.to_excel(output_path, index=False, sheet_name='员工信息')

print(f"✅ 测试Excel文件已创建: {output_path}")
print(f"📊 数据形状: {df.shape}")
print("📋 数据预览:")
print(df.head())