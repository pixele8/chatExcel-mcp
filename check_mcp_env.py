#!/usr/bin/env python3
"""
检查MCP服务器运行环境的tabulate库状态
"""

import sys
import os

print("=== MCP服务器环境检查 ===")
print(f"Python可执行文件: {sys.executable}")
print(f"Python版本: {sys.version}")
print(f"当前工作目录: {os.getcwd()}")
print(f"VIRTUAL_ENV: {os.environ.get('VIRTUAL_ENV', 'Not set')}")
print(f"Python路径: {sys.path[:3]}...")  # 只显示前3个路径

print("\n=== 关键库检查 ===")

# 检查pandas
try:
    import pandas as pd
    print(f"✅ pandas: {pd.__version__} - {pd.__file__}")
except ImportError as e:
    print(f"❌ pandas导入失败: {e}")

# 检查tabulate
try:
    import tabulate
    print(f"✅ tabulate: {tabulate.__version__} - {tabulate.__file__}")
except ImportError as e:
    print(f"❌ tabulate导入失败: {e}")

# 检查to_markdown功能
print("\n=== to_markdown功能检查 ===")
try:
    import pandas as pd
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    markdown_result = df.to_markdown()
    print(f"✅ to_markdown功能正常")
    print(f"示例输出:\n{markdown_result}")
except Exception as e:
    print(f"❌ to_markdown功能失败: {e}")

# 检查安全执行器环境
print("\n=== 安全执行器环境检查 ===")
try:
    from security.secure_code_executor import SecureCodeExecutor
    executor = SecureCodeExecutor()
    
    if 'tabulate' in executor.safe_modules:
        tabulate_module = executor.safe_modules['tabulate']
        print(f"✅ 安全执行器中tabulate可用: {tabulate_module.__version__}")
    else:
        print("❌ 安全执行器中tabulate不可用")
        
    # 测试安全执行器中的to_markdown
    test_code = """
import pandas as pd
df = pd.DataFrame({'Test': [1, 2], 'Data': [3, 4]})
result = df.to_markdown()
print("to_markdown in secure executor:", result)
"""
    
    exec_result = executor.execute_code(test_code, {})
    if exec_result.get('success'):
        print("✅ 安全执行器中to_markdown功能正常")
    else:
        print(f"❌ 安全执行器中to_markdown功能失败: {exec_result.get('error')}")
        
except Exception as e:
    print(f"❌ 安全执行器检查失败: {e}")

print("\n=== 检查完成 ===")