#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细的测试结果捕获脚本
"""

import sys
import os
import tempfile
import pandas as pd
from pathlib import Path
import json
from datetime import datetime

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def capture_test_results():
    """
    捕获详细的测试结果
    """
    results = {
        'timestamp': datetime.now().isoformat(),
        'environment': {},
        'direct_tests': {},
        'mcp_tool_tests': {},
        'summary': {}
    }
    
    # 环境信息
    results['environment'] = {
        'python_version': sys.version,
        'working_directory': os.getcwd(),
        'virtual_env': os.environ.get('VIRTUAL_ENV', 'None'),
        'libraries': {}
    }
    
    # 检查关键库
    for lib_name in ['pandas', 'tabulate', 'numpy']:
        try:
            lib = __import__(lib_name)
            version = getattr(lib, '__version__', 'Unknown')
            location = getattr(lib, '__file__', 'Unknown')
            results['environment']['libraries'][lib_name] = {
                'version': version,
                'location': location,
                'available': True
            }
        except ImportError as e:
            results['environment']['libraries'][lib_name] = {
                'available': False,
                'error': str(e)
            }
        except Exception as e:
            results['environment']['libraries'][lib_name] = {
                'available': False,
                'error': f'Other error: {e}'
            }
    
    # 直接测试 tabulate
    try:
        import tabulate
        data = [['Alice', 25], ['Bob', 30]]
        headers = ['Name', 'Age']
        result = tabulate.tabulate(data, headers=headers, tablefmt='pipe')
        results['direct_tests']['tabulate'] = {
            'success': True,
            'version': tabulate.__version__,
            'location': tabulate.__file__,
            'test_result': result
        }
    except Exception as e:
        results['direct_tests']['tabulate'] = {
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__
        }
    
    # 直接测试 pandas to_markdown
    try:
        import pandas as pd
        df = pd.DataFrame({
            'Name': ['Alice', 'Bob'],
            'Age': [25, 30]
        })
        
        to_markdown_available = hasattr(df, 'to_markdown')
        
        if to_markdown_available:
            try:
                result = df.to_markdown()
                results['direct_tests']['pandas_to_markdown'] = {
                    'success': True,
                    'pandas_version': pd.__version__,
                    'method_available': True,
                    'test_result': result
                }
            except Exception as e:
                results['direct_tests']['pandas_to_markdown'] = {
                    'success': False,
                    'pandas_version': pd.__version__,
                    'method_available': True,
                    'error': str(e),
                    'error_type': type(e).__name__,
                    'is_tabulate_error': 'tabulate' in str(e).lower()
                }
        else:
            results['direct_tests']['pandas_to_markdown'] = {
                'success': False,
                'pandas_version': pd.__version__,
                'method_available': False,
                'error': 'to_markdown method not available'
            }
    except Exception as e:
        results['direct_tests']['pandas_to_markdown'] = {
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__
        }
    
    # 测试 MCP 工具
    try:
        import server
        
        # 创建测试 Excel 文件
        temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
        temp_path = temp_file.name
        temp_file.close()
        
        df = pd.DataFrame({
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'City': ['New York', 'London', 'Tokyo']
        })
        df.to_excel(temp_path, index=False)
        
        # 测试用例 1: to_markdown()
        test_code_1 = '''result = df.to_markdown()'''
        try:
            result = server.run_excel_code(
                file_path=temp_path,
                code=test_code_1,
                allow_file_write=False
            )
            
            results['mcp_tool_tests']['to_markdown'] = {
                'success': result.get('success', False),
                'result_type': type(result.get('result')).__name__ if result.get('result') else None,
                'result_preview': str(result.get('result', ''))[:200] if result.get('result') else None,
                'error': result.get('error'),
                'suggestions': result.get('suggestions', []),
                'has_tabulate_error': False
            }
            
            if not result.get('success'):
                error_msg = str(result.get('error', '')).lower()
                results['mcp_tool_tests']['to_markdown']['has_tabulate_error'] = (
                    'importerror' in error_msg and 'tabulate' in error_msg
                )
                
        except Exception as e:
            results['mcp_tool_tests']['to_markdown'] = {
                'success': False,
                'exception': str(e),
                'exception_type': type(e).__name__
            }
        
        # 测试用例 2: 直接导入 tabulate
        test_code_2 = '''try:
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
                file_path=temp_path,
                code=test_code_2,
                allow_file_write=False
            )
            
            result_str = str(result.get('result', ''))
            
            results['mcp_tool_tests']['direct_tabulate'] = {
                'success': result.get('success', False),
                'result': result_str,
                'has_import_error_in_result': 'ImportError' in result_str,
                'error': result.get('error'),
                'has_tabulate_error': False
            }
            
            if not result.get('success'):
                error_msg = str(result.get('error', '')).lower()
                results['mcp_tool_tests']['direct_tabulate']['has_tabulate_error'] = (
                    'importerror' in error_msg and 'tabulate' in error_msg
                )
                
        except Exception as e:
            results['mcp_tool_tests']['direct_tabulate'] = {
                'success': False,
                'exception': str(e),
                'exception_type': type(e).__name__
            }
        
        # 清理临时文件
        try:
            os.unlink(temp_path)
        except:
            pass
            
    except ImportError as e:
        results['mcp_tool_tests']['server_import'] = {
            'success': False,
            'error': f'Cannot import server module: {e}'
        }
    except Exception as e:
        results['mcp_tool_tests']['general_error'] = {
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__
        }
    
    # 生成总结
    tabulate_errors_found = []
    
    # 检查直接测试中的错误
    if not results['direct_tests'].get('tabulate', {}).get('success', True):
        tabulate_errors_found.append('Direct tabulate test failed')
    
    if results['direct_tests'].get('pandas_to_markdown', {}).get('is_tabulate_error', False):
        tabulate_errors_found.append('pandas.to_markdown() has tabulate dependency issue')
    
    # 检查 MCP 工具测试中的错误
    for test_name, test_result in results['mcp_tool_tests'].items():
        if test_result.get('has_tabulate_error', False):
            tabulate_errors_found.append(f'MCP tool test {test_name} has tabulate ImportError')
        if test_result.get('has_import_error_in_result', False):
            tabulate_errors_found.append(f'MCP tool test {test_name} returned ImportError in result')
    
    results['summary'] = {
        'tabulate_errors_found': tabulate_errors_found,
        'has_any_tabulate_issues': len(tabulate_errors_found) > 0,
        'environment_status': 'OK' if results['environment']['libraries']['tabulate']['available'] else 'MISSING',
        'direct_tests_status': 'OK' if all(t.get('success', False) for t in results['direct_tests'].values()) else 'FAILED',
        'mcp_tests_status': 'OK' if all(t.get('success', False) for t in results['mcp_tool_tests'].values()) else 'FAILED'
    }
    
    return results

def main():
    print("开始详细测试...")
    
    results = capture_test_results()
    
    # 保存结果到文件
    with open('test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # 打印关键信息
    print("\n=== 测试结果总结 ===")
    print(f"时间戳: {results['timestamp']}")
    print(f"环境状态: {results['summary']['environment_status']}")
    print(f"直接测试状态: {results['summary']['direct_tests_status']}")
    print(f"MCP 工具测试状态: {results['summary']['mcp_tests_status']}")
    print(f"发现 tabulate 问题: {results['summary']['has_any_tabulate_issues']}")
    
    if results['summary']['tabulate_errors_found']:
        print("\n发现的 tabulate 相关问题:")
        for error in results['summary']['tabulate_errors_found']:
            print(f"  - {error}")
    else:
        print("\n未发现 tabulate 相关问题")
    
    print(f"\n详细结果已保存到: test_results.json")
    
    # 打印一些关键的测试结果
    print("\n=== 关键测试结果 ===")
    
    # tabulate 直接测试
    tabulate_test = results['direct_tests'].get('tabulate', {})
    if tabulate_test.get('success'):
        print(f"✅ tabulate 直接测试成功 (版本: {tabulate_test.get('version')})")
    else:
        print(f"❌ tabulate 直接测试失败: {tabulate_test.get('error')}")
    
    # pandas to_markdown 测试
    pandas_test = results['direct_tests'].get('pandas_to_markdown', {})
    if pandas_test.get('success'):
        print(f"✅ pandas.to_markdown() 测试成功")
    else:
        print(f"❌ pandas.to_markdown() 测试失败: {pandas_test.get('error')}")
        if pandas_test.get('is_tabulate_error'):
            print("   ⚠️  这是 tabulate 相关错误")
    
    # MCP 工具测试
    for test_name, test_result in results['mcp_tool_tests'].items():
        if test_result.get('success'):
            print(f"✅ MCP 工具测试 {test_name} 成功")
        else:
            print(f"❌ MCP 工具测试 {test_name} 失败: {test_result.get('error', test_result.get('exception'))}")
            if test_result.get('has_tabulate_error'):
                print("   ⚠️  这是 tabulate ImportError")

if __name__ == "__main__":
    main()