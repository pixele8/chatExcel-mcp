#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的 MCP 工具测试脚本
直接模拟用户可能遇到的 tabulate ImportError 问题
"""

import sys
import os
import tempfile
import pandas as pd
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def create_test_excel_file():
    """
    创建测试用的 Excel 文件
    """
    # 创建临时 Excel 文件
    temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
    temp_path = temp_file.name
    temp_file.close()
    
    # 创建测试数据
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'London', 'Tokyo']
    })
    
    # 保存到 Excel 文件
    df.to_excel(temp_path, index=False)
    
    return temp_path

def test_run_excel_code_with_tabulate():
    """
    测试 run_excel_code 工具中的 tabulate 相关功能
    """
    print("=== 测试 run_excel_code 工具 ===")
    
    try:
        # 导入服务器模块
        import server
        
        # 创建测试 Excel 文件
        excel_path = create_test_excel_file()
        print(f"创建测试文件: {excel_path}")
        
        # 测试用例 1: 基本的 to_markdown() 调用
        print("\n--- 测试 1: 基本 to_markdown() ---")
        test_code_1 = '''# 读取数据并转换为 markdown
result = df.to_markdown()'''
        
        try:
            result = server.run_excel_code(
                file_path=excel_path,
                code=test_code_1,
                allow_file_write=False
            )
            
            print(f"执行成功: {result.get('success', False)}")
            if result.get('success'):
                print(f"结果类型: {type(result.get('result'))}")
                print(f"结果预览: {str(result.get('result'))[:200]}...")
            else:
                print(f"错误: {result.get('error')}")
                print(f"建议: {result.get('suggestions', [])}")
                
                # 检查是否是 tabulate 相关错误
                error_msg = str(result.get('error', '')).lower()
                if 'importerror' in error_msg and 'tabulate' in error_msg:
                    print("*** 发现 tabulate ImportError！***")
                    
        except Exception as e:
            print(f"测试 1 异常: {e}")
            import traceback
            traceback.print_exc()
        
        # 测试用例 2: 直接导入 tabulate
        print("\n--- 测试 2: 直接导入 tabulate ---")
        test_code_2 = '''# 直接使用 tabulate
try:
    import tabulate
    data = df.values.tolist()
    headers = df.columns.tolist()
    result = tabulate.tabulate(data, headers=headers, tablefmt="pipe")
except ImportError as e:
    result = f"ImportError: {e}"
except Exception as e:
    result = f"Other error: {e}"'''
        
        try:
            result = server.run_excel_code(
                file_path=excel_path,
                code=test_code_2,
                allow_file_write=False
            )
            
            print(f"执行成功: {result.get('success', False)}")
            if result.get('success'):
                result_str = str(result.get('result', ''))
                print(f"结果: {result_str}")
                
                # 检查结果中是否包含 ImportError
                if 'ImportError' in result_str:
                    print("*** 在结果中发现 ImportError！***")
            else:
                print(f"错误: {result.get('error')}")
                error_msg = str(result.get('error', '')).lower()
                if 'importerror' in error_msg and 'tabulate' in error_msg:
                    print("*** 发现 tabulate ImportError！***")
                    
        except Exception as e:
            print(f"测试 2 异常: {e}")
            import traceback
            traceback.print_exc()
        
        # 测试用例 3: 检查 pandas to_markdown 的依赖
        print("\n--- 测试 3: 检查 pandas to_markdown 依赖 ---")
        test_code_3 = '''# 检查 to_markdown 方法的可用性和依赖
import pandas as pd
print(f"pandas version: {pd.__version__}")
print(f"to_markdown available: {hasattr(df, 'to_markdown')}")

# 尝试调用 to_markdown
try:
    result = df.to_markdown()
    print("to_markdown 调用成功")
except Exception as e:
    result = f"to_markdown error: {e}"
    print(result)'''
        
        try:
            result = server.run_excel_code(
                file_path=excel_path,
                code=test_code_3,
                allow_file_write=False
            )
            
            print(f"执行成功: {result.get('success', False)}")
            if result.get('success'):
                print(f"结果: {result.get('result')}")
            else:
                print(f"错误: {result.get('error')}")
                
        except Exception as e:
            print(f"测试 3 异常: {e}")
        
        # 清理临时文件
        try:
            os.unlink(excel_path)
            print(f"\n清理临时文件: {excel_path}")
        except:
            pass
            
    except ImportError as e:
        print(f"无法导入 server 模块: {e}")
    except Exception as e:
        print(f"测试出错: {e}")
        import traceback
        traceback.print_exc()

def test_environment_info():
    """
    显示环境信息
    """
    print("=== 环境信息 ===")
    print(f"Python: {sys.version}")
    print(f"工作目录: {os.getcwd()}")
    print(f"虚拟环境: {os.environ.get('VIRTUAL_ENV', 'None')}")
    
    # 检查关键库
    for lib_name in ['pandas', 'tabulate', 'numpy']:
        try:
            lib = __import__(lib_name)
            version = getattr(lib, '__version__', 'Unknown')
            location = getattr(lib, '__file__', 'Unknown')
            print(f"{lib_name}: {version} @ {location}")
        except ImportError:
            print(f"{lib_name}: 未安装")
        except Exception as e:
            print(f"{lib_name}: 错误 - {e}")

def test_direct_tabulate_usage():
    """
    直接测试 tabulate 的使用
    """
    print("\n=== 直接测试 tabulate ===")
    
    try:
        import tabulate
        print(f"tabulate 版本: {tabulate.__version__}")
        print(f"tabulate 位置: {tabulate.__file__}")
        
        # 测试基本功能
        data = [['Alice', 25], ['Bob', 30]]
        headers = ['Name', 'Age']
        result = tabulate.tabulate(data, headers=headers, tablefmt='pipe')
        print(f"tabulate 测试结果:\n{result}")
        
    except ImportError as e:
        print(f"tabulate ImportError: {e}")
    except Exception as e:
        print(f"tabulate 其他错误: {e}")

def test_pandas_to_markdown():
    """
    直接测试 pandas to_markdown
    """
    print("\n=== 直接测试 pandas to_markdown ===")
    
    try:
        import pandas as pd
        
        df = pd.DataFrame({
            'Name': ['Alice', 'Bob'],
            'Age': [25, 30]
        })
        
        print(f"pandas 版本: {pd.__version__}")
        print(f"DataFrame 创建成功")
        print(f"to_markdown 方法可用: {hasattr(df, 'to_markdown')}")
        
        if hasattr(df, 'to_markdown'):
            try:
                result = df.to_markdown()
                print(f"to_markdown 调用成功:\n{result}")
            except Exception as e:
                print(f"to_markdown 调用失败: {e}")
                # 检查是否是 tabulate 相关错误
                if 'tabulate' in str(e).lower():
                    print("*** 这是 tabulate 相关错误！***")
        else:
            print("to_markdown 方法不可用")
            
    except ImportError as e:
        print(f"pandas ImportError: {e}")
    except Exception as e:
        print(f"pandas 其他错误: {e}")

def main():
    """
    主函数
    """
    print("简化 MCP 工具测试")
    print("=" * 50)
    
    # 显示环境信息
    test_environment_info()
    
    # 直接测试库
    test_direct_tabulate_usage()
    test_pandas_to_markdown()
    
    # 测试 MCP 工具
    test_run_excel_code_with_tabulate()
    
    print("\n" + "=" * 50)
    print("测试完成")
    
    print("\n=== 分析 ===")
    print("如果在测试中发现了 ImportError，这表明：")
    print("1. tabulate 库在某些执行环境中不可用")
    print("2. pandas.to_markdown() 依赖 tabulate 但导入失败")
    print("3. 可能需要检查虚拟环境配置或依赖安装")
    print("\n如果没有发现 ImportError，可能的原因：")
    print("1. 问题已经被修复")
    print("2. 问题只在特定的 MCP 服务器运行时环境中出现")
    print("3. 问题与特定的代码执行路径有关")

if __name__ == "__main__":
    main()