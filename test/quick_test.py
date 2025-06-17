#!/usr/bin/env python3
from security.secure_code_executor import execute_safe_code

# 测试1: 基本功能
print("测试1: 基本功能")
code1 = "import pandas as pd\nprint('pandas imported')\ndf = pd.DataFrame({'A': [1,2,3]})\nprint(df)"
result1 = execute_safe_code(code1)
print(f"成功: {result1['success']}")
if result1['success']:
    print(f"输出: {result1['output']}")
else:
    print(f"错误: {result1.get('error', 'Unknown')}")
    print(f"消息: {result1.get('message', 'No message')}")

print("\n" + "="*40)

# 测试2: tabulate功能
print("测试2: tabulate功能")
code2 = "import pandas as pd\ntry:\n    import tabulate\n    print('tabulate available')\n    df = pd.DataFrame({'Name': ['Alice'], 'Age': [25]})\n    table = tabulate.tabulate(df, headers='keys')\n    print(table)\nexcept Exception as e:\n    print('tabulate error:', e)"
result2 = execute_safe_code(code2)
print(f"成功: {result2['success']}")
if result2['success']:
    print(f"输出: {result2['output']}")
else:
    print(f"错误: {result2.get('error', 'Unknown')}")
    print(f"消息: {result2.get('message', 'No message')}")

print("\n" + "="*40)

# 测试3: 模块导入
print("测试3: 模块导入")
code3 = "modules = ['os', 'sys', 'json', 'numpy']\nfor m in modules:\n    try:\n        exec(f'import {m}')\n        print(f'{m}: OK')\n    except Exception as e:\n        print(f'{m}: FAIL - {e}')"
result3 = execute_safe_code(code3)
print(f"成功: {result3['success']}")
if result3['success']:
    print(f"输出: {result3['output']}")
else:
    print(f"错误: {result3.get('error', 'Unknown')}")
    print(f"消息: {result3.get('message', 'No message')}")

print("\n测试完成")