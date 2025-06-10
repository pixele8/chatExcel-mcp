#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复run_excel_code函数的参数顺序问题
"""

import os
import shutil
from datetime import datetime

def fix_parameter_order():
    """修复参数顺序问题"""
    
    # 备份当前文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"server_backup_param_fix_{timestamp}.py"
    shutil.copy2("server.py", backup_file)
    print(f"✅ 备份文件: {backup_file}")
    
    # 读取当前文件
    with open("server.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 查找并替换函数定义
    old_signature = """def run_excel_code(
    code: str, 
    file_path: str, 
    sheet_name: str = None, 
    skiprows: int = None, 
    header: int = None, 
    usecols: str = None, 
    encoding: str = None,
    auto_detect: bool = True
) -> dict:"""
    
    new_signature = """def run_excel_code(
    file_path: str,
    code: str, 
    sheet_name: str = None, 
    skiprows: int = None, 
    header: int = None, 
    usecols: str = None, 
    encoding: str = None,
    auto_detect: bool = True
) -> dict:"""
    
    if old_signature in content:
        content = content.replace(old_signature, new_signature)
        print("✅ 修复函数签名")
    else:
        print("⚠️ 未找到需要修复的函数签名")
    
    # 写入修复后的文件
    with open("server.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ 参数顺序修复完成")
    
    # 验证修复结果
    print("\n=== 验证修复结果 ===")
    try:
        from server import run_excel_code
        import inspect
        sig = inspect.signature(run_excel_code)
        params = list(sig.parameters.keys())
        print(f"当前参数顺序: {params}")
        
        if params[0] == 'file_path' and params[1] == 'code':
            print("✅ 参数顺序正确")
        else:
            print("❌ 参数顺序仍有问题")
            
    except Exception as e:
        print(f"❌ 验证失败: {e}")

if __name__ == "__main__":
    fix_parameter_order()