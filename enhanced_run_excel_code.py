#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版 run_excel_code 函数
解决 pandas NameError 问题的全面解决方案
"""

import pandas as pd
import numpy as np
import sys
import os
import traceback
import importlib
from io import StringIO
from typing import Dict, Any, Optional

# 安全检查黑名单
BLACKLIST = [
    'import os', 'import sys', 'import subprocess', 'import shutil',
    'os.', 'sys.', 'subprocess.', 'shutil.', 'eval(', 'exec(',
    'open(', '__import__', 'globals()', 'locals()', 'vars(',
    'dir(', 'getattr(', 'setattr(', 'delattr(', 'hasattr(',
    'input(', 'raw_input(', 'file(', 'execfile(', 'reload(',
    'compile(', '__builtins__', '__file__', '__name__'
]

def diagnose_environment() -> Dict[str, Any]:
    """诊断当前 Python 环境"""
    diagnosis = {
        'python_version': sys.version,
        'python_path': sys.path[:5],  # 只显示前5个路径
        'current_directory': os.getcwd(),
        'modules': {}
    }
    
    # 检查关键模块
    modules_to_check = ['pandas', 'numpy', 'openpyxl', 'xlrd']
    for module_name in modules_to_check:
        try:
            module = importlib.import_module(module_name)
            diagnosis['modules'][module_name] = {
                'available': True,
                'version': getattr(module, '__version__', 'unknown'),
                'location': getattr(module, '__file__', 'unknown')
            }
        except ImportError as e:
            diagnosis['modules'][module_name] = {
                'available': False,
                'error': str(e)
            }
    
    return diagnosis

def safe_import_modules() -> Dict[str, Any]:
    """安全导入所需模块"""
    modules = {}
    errors = []
    
    # 导入 pandas
    try:
        import pandas as pd
        modules['pd'] = pd
        modules['pandas'] = pd
    except ImportError as e:
        errors.append(f"Failed to import pandas: {e}")
        # 尝试重新安装或使用备用方案
        try:
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])
            import pandas as pd
            modules['pd'] = pd
            modules['pandas'] = pd
        except Exception as e2:
            errors.append(f"Failed to install/reimport pandas: {e2}")
    
    # 导入 numpy
    try:
        import numpy as np
        modules['np'] = np
        modules['numpy'] = np
    except ImportError as e:
        errors.append(f"Failed to import numpy: {e}")
        try:
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy'])
            import numpy as np
            modules['np'] = np
            modules['numpy'] = np
        except Exception as e2:
            errors.append(f"Failed to install/reimport numpy: {e2}")
    
    return modules, errors

def validate_file_access(file_path: str) -> Dict[str, Any]:
    """验证文件访问权限"""
    if not os.path.exists(file_path):
        return {
            "status": "ERROR",
            "message": f"File not found: {file_path}"
        }
    
    if not os.path.isfile(file_path):
        return {
            "status": "ERROR",
            "message": f"Path is not a file: {file_path}"
        }
    
    if not os.access(file_path, os.R_OK):
        return {
            "status": "ERROR",
            "message": f"No read permission for file: {file_path}"
        }
    
    return {"status": "SUCCESS"}

def enhanced_run_excel_code(
    code: str,
    file_path: str,
    sheet_name: Optional[str] = None,
    skiprows: Optional[int] = None,
    header: Optional[int] = None,
    usecols: Optional[str] = None,
    encoding: Optional[str] = None,
    auto_detect: bool = True,
    debug_mode: bool = False
) -> Dict[str, Any]:
    """增强版 Excel 代码执行函数
    
    Args:
        code: 要执行的 Python 代码
        file_path: Excel 文件路径
        sheet_name: 工作表名称
        skiprows: 跳过的行数
        header: 标题行
        usecols: 使用的列
        encoding: 编码
        auto_detect: 是否自动检测
        debug_mode: 是否启用调试模式
    
    Returns:
        执行结果字典
    """
    
    # 初始化结果
    result = {
        'success': False,
        'debug_info': {} if debug_mode else None
    }
    
    if debug_mode:
        result['debug_info']['environment'] = diagnose_environment()
    
    # 安全检查
    for forbidden in BLACKLIST:
        if forbidden in code:
            result['error'] = {
                "type": "SECURITY_VIOLATION",
                "message": f"Forbidden operation detected: {forbidden}",
                "solution": "Remove restricted operations from your code"
            }
            return result
    
    # 验证文件访问
    validation_result = validate_file_access(file_path)
    if validation_result["status"] != "SUCCESS":
        result['error'] = {
            "type": "FILE_ACCESS_ERROR",
            "message": validation_result["message"],
            "solution": "请确保文件路径正确且文件存在。"
        }
        return result
    
    # 安全导入模块
    modules, import_errors = safe_import_modules()
    if import_errors and debug_mode:
        result['debug_info']['import_errors'] = import_errors
    
    if 'pd' not in modules:
        result['error'] = {
            "type": "IMPORT_ERROR",
            "message": "Failed to import pandas",
            "details": import_errors,
            "solution": "请确保 pandas 已正确安装: pip install pandas"
        }
        return result
    
    pd = modules['pd']
    np = modules.get('np')
    
    # 读取 Excel 文件
    try:
        read_params = {}
        if sheet_name is not None:
            read_params['sheet_name'] = sheet_name
        if skiprows is not None:
            read_params['skiprows'] = skiprows
        if header is not None:
            read_params['header'] = header
        if usecols is not None:
            read_params['usecols'] = usecols
        
        df = pd.read_excel(file_path, **read_params)
        
        if debug_mode:
            result['debug_info']['read_params'] = read_params
            result['debug_info']['dataframe_info'] = {
                'shape': df.shape,
                'columns': list(df.columns),
                'dtypes': str(df.dtypes)
            }
    
    except Exception as e:
        result['error'] = {
            "type": "READ_ERROR",
            "message": f"Failed to read Excel file: {str(e)}",
            "traceback": traceback.format_exc() if debug_mode else None,
            "solution": "请检查文件格式和参数设置"
        }
        return result
    
    # 准备执行环境
    local_vars = {
        'pd': pd,
        'df': df,
        'file_path': file_path,
        'sheet_name': sheet_name
    }
    
    if np is not None:
        local_vars['np'] = np
    
    # 添加常用函数
    local_vars.update({
        'len': len,
        'str': str,
        'int': int,
        'float': float,
        'list': list,
        'dict': dict,
        'print': print,
        'range': range,
        'enumerate': enumerate,
        'zip': zip,
        'sum': sum,
        'max': max,
        'min': min,
        'abs': abs,
        'round': round
    })
    
    if debug_mode:
        result['debug_info']['local_vars_keys'] = list(local_vars.keys())
    
    # 捕获输出
    stdout_capture = StringIO()
    old_stdout = sys.stdout
    sys.stdout = stdout_capture
    
    try:
        # 执行用户代码
        exec(code, {}, local_vars)
        
        # 获取结果
        execution_result = local_vars.get('result', None)
        output = stdout_capture.getvalue()
        
        # 处理结果
        if execution_result is None:
            result.update({
                'success': True,
                'output': output,
                'warning': "No 'result' variable found in code"
            })
        elif isinstance(execution_result, (pd.DataFrame, pd.Series)):
            result.update({
                'success': True,
                'result': {
                    "type": "dataframe" if isinstance(execution_result, pd.DataFrame) else "series",
                    "shape": execution_result.shape,
                    "dtypes": str(execution_result.dtypes),
                    "data": execution_result.head().to_dict() if isinstance(execution_result, pd.DataFrame) else execution_result.to_dict()
                },
                'output': output
            })
        else:
            result.update({
                'success': True,
                'result': str(execution_result),
                'output': output
            })
    
    except NameError as e:
        error_msg = str(e)
        suggestions = []
        
        if "'pd'" in error_msg:
            suggestions.extend([
                "pandas 模块导入失败，请检查安装: pip install pandas",
                "尝试在代码中显式导入: import pandas as pd",
                "检查虚拟环境是否正确激活"
            ])
        
        if "'np'" in error_msg:
            suggestions.extend([
                "numpy 模块导入失败，请检查安装: pip install numpy",
                "尝试在代码中显式导入: import numpy as np"
            ])
        
        if "'df'" in error_msg:
            suggestions.extend([
                "DataFrame 未正确加载，请检查文件路径和格式",
                "尝试使用 pd.read_excel() 手动读取文件"
            ])
        
        result['error'] = {
            "type": "NameError",
            "message": error_msg,
            "traceback": traceback.format_exc(),
            "output": stdout_capture.getvalue(),
            "suggestions": suggestions,
            "environment_check": diagnose_environment() if debug_mode else None
        }
    
    except Exception as e:
        error_msg = str(e)
        suggestions = []
        
        if "No such file or directory" in error_msg:
            suggestions.append("Use raw strings for paths: r'path\\to\\file.xlsx'")
        if "Worksheet named" in error_msg and "not found" in error_msg:
            suggestions.append("Check the sheet_name parameter. Ensure the sheet name exists in the Excel file.")
        if "could not convert string to float" in error_msg:
            suggestions.append("Try: pd.to_numeric(df['col'], errors='coerce')")
        if "AttributeError" in error_msg and "str" in error_msg:
            suggestions.append("Try: df['col'].astype(str).str.strip()")
        if "encoding" in error_msg.lower():
            suggestions.append("Try specifying encoding parameter")
        
        result['error'] = {
            "type": type(e).__name__,
            "message": error_msg,
            "traceback": traceback.format_exc(),
            "output": stdout_capture.getvalue(),
            "suggestions": suggestions if suggestions else None
        }
    
    finally:
        sys.stdout = old_stdout
    
    return result

def create_diagnostic_tool():
    """创建诊断工具"""
    print("🔍 Excel MCP 服务器诊断工具")
    print("=" * 50)
    
    # 环境诊断
    print("\n📋 环境诊断:")
    env_info = diagnose_environment()
    print(f"Python 版本: {env_info['python_version'].split()[0]}")
    print(f"当前目录: {env_info['current_directory']}")
    
    print("\n📦 模块检查:")
    for module_name, info in env_info['modules'].items():
        if info['available']:
            print(f"✅ {module_name}: v{info['version']}")
        else:
            print(f"❌ {module_name}: {info['error']}")
    
    # 模块导入测试
    print("\n🧪 模块导入测试:")
    modules, errors = safe_import_modules()
    if errors:
        print("❌ 导入错误:")
        for error in errors:
            print(f"   {error}")
    else:
        print("✅ 所有模块导入成功")
    
    # 功能测试
    print("\n⚡ 功能测试:")
    test_code = """
print(f"pandas 版本: {pd.__version__}")
print(f"numpy 版本: {np.__version__}")
test_df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
result = test_df.sum()
print(f"测试计算结果: {result.tolist()}")
"""
    
    # 创建临时测试文件
    test_data = pd.DataFrame({'测试列': [1, 2, 3]})
    test_file = 'diagnostic_test.xlsx'
    test_data.to_excel(test_file, index=False)
    
    try:
        test_result = enhanced_run_excel_code(test_code, test_file, debug_mode=True)
        if test_result['success']:
            print("✅ 功能测试通过")
            print(f"   输出: {test_result['output'].strip()}")
        else:
            print("❌ 功能测试失败")
            print(f"   错误: {test_result['error']['message']}")
    except Exception as e:
        print(f"❌ 功能测试异常: {e}")
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)
    
    print("\n" + "=" * 50)
    print("✅ 诊断完成")

if __name__ == "__main__":
    create_diagnostic_tool()