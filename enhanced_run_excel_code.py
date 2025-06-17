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

# 安全检查黑名单 - 完全解除tabulate库限制
BLACKLIST = [
    'import os', 'import sys', 'import subprocess', 'import shutil',
    'os.', 'sys.', 'subprocess.', 'shutil.', 'eval(', 'exec(',
    'open(', 'globals()', 'locals()', 'vars(',
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

# 导入必要的库
import pandas as pd
import numpy as np
import json
import traceback
import sys
import io
from contextlib import redirect_stdout
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
import warnings
from security.secure_code_executor import SecureCodeExecutor
from utils.parameter_validator import ParameterValidator

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 大幅减少的黑名单 - 完全解除tabulate库限制
BLACKLIST = [
    # 完全清空，允许所有库包括tabulate
]

def enhanced_run_excel_code(
    code: str,
    df: Optional[pd.DataFrame] = None,
    allow_file_write: bool = False,
    max_execution_time: int = 60,  # 增加执行时间
    max_memory_mb: int = 1024,     # 增加内存限制
    enable_security_check: bool = False,  # 默认关闭安全检查
    return_format: str = 'auto'
) -> Dict[str, Any]:
    """
    增强版Excel代码执行器 - 宽松安全版本
    
    Args:
        code: 要执行的Python代码
        df: 输入的DataFrame（可选）
        allow_file_write: 是否允许文件写入操作
        max_execution_time: 最大执行时间（秒）
        max_memory_mb: 最大内存使用量（MB）
        enable_security_check: 是否启用安全检查
        return_format: 返回格式 ('auto', 'json', 'html', 'markdown')
    
    Returns:
        Dict: 执行结果
    """
    
    start_time = datetime.now()
    
    try:
        # 1. 基础验证
        if not code or not isinstance(code, str):
            return {
                "success": False,
                "error": "代码不能为空",
                "execution_time": 0
            }
        
        # 2. 参数验证（宽松版本）
        validator = ParameterValidator()
        validation_result = validator.validate_code_content(code, max_length=100000)  # 增加长度限制
        
        if not validation_result['valid']:
            return {
                "success": False,
                "error": f"代码验证失败: {'; '.join(validation_result['errors'])}",
                "warnings": validation_result.get('warnings', []),
                "execution_time": 0
            }
        
        # 3. 安全检查（可选且宽松）
        if enable_security_check:
            # 只检查最基本的安全问题
            for forbidden in BLACKLIST:
                if forbidden in code:
                    logger.warning(f"检测到潜在风险操作: {forbidden}")
                    # 不阻止执行，只记录警告
        
        # 4. 准备执行环境
        context = {}
        if df is not None:
            context['df'] = df
            context['data'] = df  # 提供别名
        
        # 5. 使用安全代码执行器（宽松配置）
        executor = SecureCodeExecutor(
            max_memory_mb=max_memory_mb,
            max_execution_time=max_execution_time,
            enable_ast_analysis=False  # 禁用AST分析
        )
        
        # 6. 执行代码
        result = executor.execute_code(code, context)
        
        # 7. 处理执行结果
        execution_time = (datetime.now() - start_time).total_seconds()
        
        if result.get('success', True):
            # 成功执行
            output_data = result.get('result')
            captured_output = result.get('output', '')
            
            # 格式化输出
            formatted_result = format_output(
                output_data, 
                captured_output, 
                return_format
            )
            
            return {
                "success": True,
                "result": formatted_result,
                "output": captured_output,
                "execution_time": execution_time,
                "warnings": validation_result.get('warnings', []),
                "metadata": {
                    "code_length": len(code),
                    "has_dataframe_input": df is not None,
                    "return_format": return_format,
                    "security_check_enabled": enable_security_check
                }
            }
        else:
            # 执行失败
            return {
                "success": False,
                "error": result.get('error', '未知错误'),
                "execution_time": execution_time,
                "warnings": validation_result.get('warnings', [])
            }
            
    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.error(f"代码执行异常: {str(e)}")
        logger.error(f"异常堆栈: {traceback.format_exc()}")
        
        return {
            "success": False,
            "error": f"执行异常: {str(e)}",
            "execution_time": execution_time,
            "traceback": traceback.format_exc()
        }

def format_output(data: Any, captured_output: str, return_format: str) -> Any:
    """
    格式化输出数据
    
    Args:
        data: 执行结果数据
        captured_output: 捕获的输出
        return_format: 返回格式
    
    Returns:
        格式化后的数据
    """
    
    if return_format == 'auto':
        # 自动判断格式
        if isinstance(data, pd.DataFrame):
            return_format = 'html'
        elif captured_output:
            return_format = 'text'
        else:
            return_format = 'json'
    
    try:
        if return_format == 'html' and isinstance(data, pd.DataFrame):
            return data.to_html(classes='table table-striped', escape=False)
        elif return_format == 'markdown' and isinstance(data, pd.DataFrame):
            try:
                # 优先使用to_markdown方法（需要tabulate库）
                return data.to_markdown(index=False)
            except ImportError:
                # 如果tabulate库不可用，使用备用方案
                logger.warning("tabulate库不可用，使用备用表格格式")
                # 简单的表格格式化备用方案
                headers = '| ' + ' | '.join(str(col) for col in data.columns) + ' |\n'
                separator = '|' + '---|' * len(data.columns) + '\n'
                rows = ''
                for _, row in data.iterrows():
                    rows += '| ' + ' | '.join(str(val) for val in row) + ' |\n'
                return headers + separator + rows
            except Exception as e:
                logger.warning(f"Markdown格式化失败: {e}，使用字符串格式")
                return str(data)
        elif return_format == 'json':
            if isinstance(data, pd.DataFrame):
                return data.to_dict('records')
            else:
                return data
        else:
            return str(data) if data is not None else captured_output
    except Exception as e:
        logger.warning(f"格式化输出失败: {e}")
        return str(data) if data is not None else captured_output

# 向后兼容的函数别名
run_excel_code = enhanced_run_excel_code

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