#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一的安全代码执行模块

提供一个标准化的、安全的代码执行环境，供项目中所有需要执行
用户提供代码的工具使用。
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

def execute_code_safely(
    code: str, 
    df: pd.DataFrame, 
    file_path: Optional[str] = None, 
    extra_globals: Optional[Dict[str, Any]] = None
) -> Any:
    """
    在安全的环境中执行给定的Python代码。

    Args:
        code (str): 要执行的Python代码字符串。
        df (pd.DataFrame): 作为主要数据源的DataFrame，在执行环境中名为 'df'。
        file_path (Optional[str]): 文件的路径，在执行环境中名为 'file_path'。
        extra_globals (Optional[Dict[str, Any]]): 其他需要注入到执行环境的全局变量。

    Returns:
        Any: 代码执行后的 'result' 变量或修改后的 'df'。

    Raises:
        ValueError: 如果代码包含不安全的操作。
        Exception: 代码执行期间发生的其他异常。
    """
    # 检查代码安全性 (简化版，可以根据需要扩展)
    if not _is_code_safe(code):
        raise ValueError("代码包含不安全的操作 (例如，导入 os/sys 或文件操作)")

    # 创建安全的执行环境
    safe_builtins = {
        'len': len, 'str': str, 'int': int, 'float': float, 'bool': bool,
        'list': list, 'dict': dict, 'tuple': tuple, 'set': set,
        'range': range, 'enumerate': enumerate, 'zip': zip,
        'map': map, 'filter': filter, 'sum': sum, 'min': min, 'max': max,
        'abs': abs, 'round': round, 'sorted': sorted, 'reversed': reversed,
        'print': print, 'locals': locals
    }

    safe_globals = {
        '__builtins__': safe_builtins,
        'pd': pd,
        'np': np,
        'df': df.copy(),
        'result': None  # 预定义一个用于存放结果的变量
    }

    if file_path:
        safe_globals['file_path'] = file_path

    if extra_globals:
        safe_globals.update(extra_globals)

    # 执行代码
    exec(code, safe_globals)

    # 返回结果，优先返回 'result' 变量，否则返回修改后的 'df'
    return safe_globals.get('result', safe_globals['df'])

def _is_code_safe(code: str) -> bool:
    """
    检查代码是否包含潜在的危险操作。
    这是一个基础的检查，主要防止明显的不安全调用。

    Args:
        code (str): 要检查的代码字符串。

    Returns:
        bool: 如果代码被认为是安全的，则返回True。
    """
    # 禁止导入不安全的模块
    dangerous_imports = ['os', 'sys', 'subprocess', 'shutil', 'requests']
    for module in dangerous_imports:
        if f'import {module}' in code or f'from {module}' in code:
            return False

    # 禁止直接的文件I/O操作 (允许pandas的读写)
    if 'open(' in code and not any(s in code for s in ['pd.read', 'df.to_']):
        return False

    # 禁止使用 eval 和 exec
    if 'eval(' in code or 'exec(' in code:
        return False
        
    # 禁止访问 __builtins__
    if '__builtins__' in code:
        return False

    return True