#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的字符串修复测试
"""

def fix_f_string_simple(code):
    """
    简单直接的f字符串修复
    """
    import re
    
    # 查找包含真实换行符的f字符串
    # 模式：f"...真实换行符...{...}"
    def fix_fstring_newlines(match):
        quote = match.group(1)  # " 或 '
        content = match.group(2)  # f字符串内容
        
        # 将真实的换行符替换为转义的换行符
        content = content.replace('\n', '\\n')
        content = content.replace('\t', '\\t')
        content = content.replace('\r', '\\r')
        
        return f'f{quote}{content}{quote}'
    
    # 使用DOTALL标志来匹配包含换行符的字符串
    pattern = r'f(["\'])([^"\']*)\1'
    fixed_code = re.sub(pattern, fix_fstring_newlines, code, flags=re.DOTALL)
    
    return fixed_code

def test_fix():
    # 测试代码 - 注意这里的\n是真实的换行符
    problematic_code = '''import pandas as pd
data = {"Name": ["Alice", "Bob"], "Age": [25, 30]}
df = pd.DataFrame(data)
print(f"数据创建成功:\n{df}")'''
    
    print("原始代码:")
    print(repr(problematic_code))
    
    # 显示问题行
    lines = problematic_code.split('\n')
    print(f"\n问题行 (第4行): {repr(lines[3])}")
    
    # 修复
    fixed_code = fix_f_string_simple(problematic_code)
    print("\n修复后代码:")
    print(repr(fixed_code))
    
    # 显示修复后的行
    fixed_lines = fixed_code.split('\n')
    print(f"\n修复后行 (第4行): {repr(fixed_lines[3])}")
    
    # 测试语法
    print("\n语法测试:")
    try:
        compile(fixed_code, '<string>', 'exec')
        print("✓ 语法正确")
        
        # 测试执行
        print("\n执行测试:")
        exec(fixed_code)
        print("✓ 执行成功")
        
    except SyntaxError as e:
        print(f"✗ 语法错误: {e}")
        print(f"错误位置: 行 {e.lineno}, 列 {e.offset}")
        if e.text:
            print(f"错误行: {repr(e.text)}")
    except Exception as e:
        print(f"✗ 执行错误: {e}")

if __name__ == "__main__":
    test_fix()