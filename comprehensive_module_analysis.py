#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面的模块导入和pandas可用性分析
系统性检查虚拟环境中的依赖问题和模块导入限制
"""

import sys
import os
import subprocess
import importlib
import traceback
from pathlib import Path

def check_virtual_environment():
    """
    检查虚拟环境配置
    """
    print("=== 虚拟环境检查 ===")
    
    # 检查Python解释器路径
    python_path = sys.executable
    print(f"当前Python解释器: {python_path}")
    
    # 检查是否在虚拟环境中
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"是否在虚拟环境中: {in_venv}")
    
    if in_venv:
        print(f"虚拟环境路径: {sys.prefix}")
        expected_venv = "/Users/wangdada/Downloads/mcp/chatExcel-mcp/venv"
        if expected_venv in python_path:
            print("✅ 使用正确的项目虚拟环境")
        else:
            print(f"⚠️ 当前虚拟环境可能不是项目环境")
            print(f"期望路径: {expected_venv}")
    else:
        print("❌ 未在虚拟环境中运行")
    
    # 检查PYTHONPATH
    pythonpath = os.environ.get('PYTHONPATH', '')
    print(f"PYTHONPATH: {pythonpath}")
    
    # 检查sys.path
    print("\nPython模块搜索路径:")
    for i, path in enumerate(sys.path[:5]):  # 只显示前5个
        print(f"  {i}: {path}")
    if len(sys.path) > 5:
        print(f"  ... 还有 {len(sys.path) - 5} 个路径")

def check_pandas_availability():
    """
    检查pandas库的可用性
    """
    print("\n=== Pandas可用性检查 ===")
    
    try:
        import pandas as pd
        print(f"✅ pandas导入成功")
        print(f"pandas版本: {pd.__version__}")
        print(f"pandas安装路径: {pd.__file__}")
        
        # 测试基本功能
        test_df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        print(f"✅ pandas基本功能测试通过")
        print(f"测试DataFrame形状: {test_df.shape}")
        
        return True, pd
        
    except ImportError as e:
        print(f"❌ pandas导入失败: {e}")
        return False, None
    except Exception as e:
        print(f"❌ pandas功能测试失败: {e}")
        return False, None

def check_other_critical_modules():
    """
    检查其他关键模块的可用性
    """
    print("\n=== 关键模块可用性检查 ===")
    
    critical_modules = {
        'numpy': 'np',
        'openpyxl': None,
        'xlrd': None,
        'matplotlib': 'plt',
        'seaborn': 'sns',
        'fastmcp': None,
        'collections': None,
        'datetime': 'dt',
        'json': None,
        'csv': None,
        'io': None,
        'tempfile': None
    }
    
    results = {}
    
    for module_name, alias in critical_modules.items():
        try:
            if alias:
                exec(f"import {module_name} as {alias}")
            else:
                exec(f"import {module_name}")
            
            module = importlib.import_module(module_name)
            version = getattr(module, '__version__', 'Unknown')
            print(f"✅ {module_name}: {version}")
            results[module_name] = {'status': 'success', 'version': version}
            
        except ImportError as e:
            print(f"❌ {module_name}: 导入失败 - {e}")
            results[module_name] = {'status': 'failed', 'error': str(e)}
        except Exception as e:
            print(f"⚠️ {module_name}: 部分问题 - {e}")
            results[module_name] = {'status': 'partial', 'error': str(e)}
    
    return results

def check_mcp_server_imports():
    """
    检查MCP服务器中的导入语句
    """
    print("\n=== MCP服务器导入检查 ===")
    
    server_file = "/Users/wangdada/Downloads/mcp/chatExcel-mcp/server.py"
    
    if not os.path.exists(server_file):
        print(f"❌ 服务器文件不存在: {server_file}")
        return
    
    try:
        # 添加项目路径到sys.path
        project_root = "/Users/wangdada/Downloads/mcp/chatExcel-mcp"
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        # 尝试导入服务器模块
        import server
        print("✅ server.py模块导入成功")
        
        # 检查关键函数是否存在
        key_functions = ['run_excel_code', '_execute_code_safely']
        for func_name in key_functions:
            if hasattr(server, func_name):
                print(f"✅ 函数 {func_name} 存在")
            else:
                print(f"❌ 函数 {func_name} 不存在")
        
        return True
        
    except Exception as e:
        print(f"❌ server.py导入失败: {e}")
        print(f"错误详情: {traceback.format_exc()}")
        return False

def test_code_execution_environments():
    """
    测试不同代码执行环境中的pandas可用性
    """
    print("\n=== 代码执行环境测试 ===")
    
    # 测试1: 直接执行
    print("\n测试1: 直接执行环境")
    try:
        exec("import pandas as pd; result = pd.DataFrame({'test': [1, 2, 3]})")
        print("✅ 直接执行环境中pandas可用")
    except Exception as e:
        print(f"❌ 直接执行环境中pandas不可用: {e}")
    
    # 测试2: 受限环境（模拟security/code_executor.py）
    print("\n测试2: 受限执行环境")
    try:
        safe_builtins = {
            'len': len, 'str': str, 'int': int, 'float': float, 'bool': bool,
            'list': list, 'dict': dict, 'tuple': tuple, 'set': set,
            'range': range, 'enumerate': enumerate, 'zip': zip,
            'map': map, 'filter': filter, 'sum': sum, 'min': min, 'max': max,
            'abs': abs, 'round': round, 'sorted': sorted, 'reversed': reversed,
            'print': print
        }
        
        safe_globals = {
            '__builtins__': safe_builtins,
            'pd': None  # 预设为None，看是否能导入
        }
        
        # 尝试在受限环境中导入pandas
        exec("import pandas as pd", safe_globals)
        if safe_globals.get('pd'):
            print("✅ 受限环境中pandas可用")
        else:
            print("❌ 受限环境中pandas不可用")
            
    except Exception as e:
        print(f"❌ 受限环境测试失败: {e}")
    
    # 测试3: 增强环境（模拟_execute_code_safely）
    print("\n测试3: 增强执行环境")
    try:
        enhanced_globals = {
            '__builtins__': {
                'len': len, 'str': str, 'int': int, 'float': float, 'bool': bool,
                'print': print, 'type': type, 'isinstance': isinstance,
                'hasattr': hasattr, 'getattr': getattr,
                '__import__': __import__,
            }
        }
        
        exec("import pandas as pd; result = pd.DataFrame({'test': [1, 2, 3]})", enhanced_globals)
        if 'result' in enhanced_globals and enhanced_globals['result'] is not None:
            print("✅ 增强环境中pandas可用")
        else:
            print("❌ 增强环境中pandas不可用")
            
    except Exception as e:
        print(f"❌ 增强环境测试失败: {e}")

def check_requirements_and_dependencies():
    """
    检查requirements.txt和已安装的依赖
    """
    print("\n=== 依赖检查 ===")
    
    # 检查requirements.txt
    req_file = "/Users/wangdada/Downloads/mcp/chatExcel-mcp/requirements.txt"
    if os.path.exists(req_file):
        print("\nrequirements.txt内容:")
        with open(req_file, 'r') as f:
            requirements = f.read().strip().split('\n')
            for req in requirements[:10]:  # 只显示前10个
                if req.strip():
                    print(f"  {req}")
            if len(requirements) > 10:
                print(f"  ... 还有 {len(requirements) - 10} 个依赖")
    else:
        print("❌ requirements.txt文件不存在")
    
    # 检查已安装的包
    print("\n检查关键包的安装状态:")
    key_packages = ['pandas', 'numpy', 'openpyxl', 'fastmcp', 'matplotlib']
    
    for package in key_packages:
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'show', package],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                # 提取版本信息
                lines = result.stdout.split('\n')
                version_line = next((line for line in lines if line.startswith('Version:')), None)
                if version_line:
                    version = version_line.split(':', 1)[1].strip()
                    print(f"✅ {package}: {version}")
                else:
                    print(f"✅ {package}: 已安装")
            else:
                print(f"❌ {package}: 未安装")
        except Exception as e:
            print(f"⚠️ {package}: 检查失败 - {e}")

def generate_recommendations():
    """
    生成改进建议
    """
    print("\n=== 改进建议 ===")
    
    recommendations = [
        "1. 确保在正确的虚拟环境中运行:",
        "   source /Users/wangdada/Downloads/mcp/chatExcel-mcp/venv/bin/activate",
        "",
        "2. 如果pandas导入失败，重新安装:",
        "   pip install pandas openpyxl xlrd",
        "",
        "3. 检查PYTHONPATH设置:",
        "   export PYTHONPATH=/Users/wangdada/Downloads/mcp/chatExcel-mcp",
        "",
        "4. 更新所有依赖:",
        "   pip install -r requirements.txt --upgrade",
        "",
        "5. 如果仍有问题，重建虚拟环境:",
        "   rm -rf venv",
        "   python3 -m venv venv",
        "   source venv/bin/activate",
        "   pip install -r requirements.txt"
    ]
    
    for rec in recommendations:
        print(rec)

def main():
    """
    主函数：执行全面的模块导入分析
    """
    print("ChatExcel MCP 项目 - 全面模块导入分析")
    print("=" * 50)
    
    # 执行各项检查
    check_virtual_environment()
    pandas_available, pd_module = check_pandas_availability()
    module_results = check_other_critical_modules()
    server_import_ok = check_mcp_server_imports()
    test_code_execution_environments()
    check_requirements_and_dependencies()
    
    # 生成总结报告
    print("\n" + "=" * 50)
    print("=== 总结报告 ===")
    
    # 关键指标
    critical_issues = []
    if not pandas_available:
        critical_issues.append("pandas不可用")
    if not server_import_ok:
        critical_issues.append("server.py导入失败")
    
    failed_modules = [name for name, result in module_results.items() if result['status'] == 'failed']
    if failed_modules:
        critical_issues.append(f"模块导入失败: {', '.join(failed_modules)}")
    
    if critical_issues:
        print("❌ 发现关键问题:")
        for issue in critical_issues:
            print(f"   - {issue}")
        print("\n建议按照下面的改进建议进行修复。")
    else:
        print("✅ 所有关键模块和功能正常")
        print("项目环境配置良好，MCP工具应该能正常调用pandas库。")
    
    generate_recommendations()

if __name__ == "__main__":
    main()