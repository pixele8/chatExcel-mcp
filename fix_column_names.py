#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复enhanced_excel_helper.py中的列名处理逻辑
"""

import re
from pathlib import Path

def fix_enhanced_excel_helper():
    """修复enhanced_excel_helper.py文件"""
    file_path = Path("enhanced_excel_helper.py")
    
    if not file_path.exists():
        print(f"文件不存在: {file_path}")
        return False
    
    # 读取原文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 备份原文件
    backup_path = file_path.with_suffix('.py.backup')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"已备份原文件到: {backup_path}")
    
    # 查找需要修改的位置
    # 在成功读取DataFrame后添加列名修复逻辑
    pattern = r"(\s+)(df = pd\.read_excel\(file_path, \*\*read_params\))\n(\s+)(result\['success'\] = True)"
    
    replacement = r"""\1\2
\1
\1# 修复列名：如果是元组格式，转换为字符串格式
\1if hasattr(df, 'columns'):
\1    new_columns = []
\1    for col in df.columns:
\1        if isinstance(col, tuple):
\1            # 将元组列名转换为字符串，取最后一个非空元素
\1            col_parts = [str(part).strip() for part in col if part is not None and str(part).strip()]
\1            if col_parts:
\1                new_columns.append(col_parts[-1])
\1            else:
\1                new_columns.append(str(col))
\1        else:
\1            new_columns.append(col)
\1    df.columns = new_columns
\1
\3\4"""
    
    # 执行替换
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        # 写入修改后的文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("已成功修复enhanced_excel_helper.py文件")
        return True
    else:
        print("未找到需要修改的代码模式")
        return False

def main():
    """主函数"""
    print("开始修复enhanced_excel_helper.py文件...")
    
    success = fix_enhanced_excel_helper()
    
    if success:
        print("修复完成！")
    else:
        print("修复失败，请检查文件内容")

if __name__ == "__main__":
    main()