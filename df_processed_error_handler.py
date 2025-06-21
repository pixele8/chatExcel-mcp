#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DataFrame处理错误处理器
提供变量生命周期管理、名称错误处理和增强的错误处理功能
"""

import sys
import traceback
from typing import Dict, Any, List, Optional, Set, Tuple
import ast
import re
from io import StringIO
import pandas as pd

# 使用core.exceptions中统一定义的DataProcessingError
try:
    from core.exceptions import DataProcessingError
except ImportError:
    # 如果core不可用，创建简单的DataProcessingError类
    class DataProcessingError(Exception):
        def __init__(self, operation: str, error_details: str):
            super().__init__(f"Data processing error in {operation}: {error_details}")

class VariableLifecycleManager:
    """变量生命周期管理器"""
    
    def __init__(self):
        self.variables = {}
        self.history = []
        self.temp_variables = set()
    
    def register_variable(self, name: str, value: Any, is_temp: bool = False) -> None:
        """注册变量"""
        self.variables[name] = value
        self.history.append(('register', name, type(value).__name__))
        if is_temp:
            self.temp_variables.add(name)
    
    def get_variable(self, name: str) -> Any:
        """获取变量"""
        return self.variables.get(name)
    
    def remove_variable(self, name: str) -> bool:
        """移除变量"""
        if name in self.variables:
            del self.variables[name]
            self.history.append(('remove', name, None))
            self.temp_variables.discard(name)
            return True
        return False
    
    def cleanup_temp_variables(self) -> List[str]:
        """清理临时变量"""
        cleaned = []
        for var_name in list(self.temp_variables):
            if self.remove_variable(var_name):
                cleaned.append(var_name)
        return cleaned
    
    def get_available_variables(self) -> Dict[str, str]:
        """获取可用变量列表"""
        return {name: type(value).__name__ for name, value in self.variables.items()}

class NameErrorHandler:
    """名称错误处理器"""
    
    def __init__(self, variable_manager: VariableLifecycleManager):
        self.variable_manager = variable_manager
        self.common_fixes = {
            'df': ['data', 'dataframe', 'df1', 'df_result'],
            'data': ['df', 'dataframe', 'dataset'],
            'result': ['df_result', 'output', 'processed_data']
        }
    
    def suggest_fixes(self, error_name: str) -> List[str]:
        """建议修复方案"""
        suggestions = []
        available_vars = self.variable_manager.get_available_variables()
        
        # 直接匹配
        if error_name in available_vars:
            return [f"变量 '{error_name}' 已存在"]
        
        # 模糊匹配
        for var_name in available_vars.keys():
            if error_name.lower() in var_name.lower() or var_name.lower() in error_name.lower():
                suggestions.append(f"使用 '{var_name}' 替代 '{error_name}'")
        
        # 常见修复建议
        if error_name in self.common_fixes:
            for fix in self.common_fixes[error_name]:
                if fix in available_vars:
                    suggestions.append(f"使用 '{fix}' 替代 '{error_name}'")
        
        return suggestions[:5]  # 限制建议数量
    
    def auto_fix_code(self, code: str, error_name: str) -> Optional[str]:
        """自动修复代码中的名称错误"""
        available_vars = self.variable_manager.get_available_variables()
        
        # 寻找最佳替换候选
        best_match = None
        best_score = 0
        
        for var_name in available_vars.keys():
            score = self._calculate_similarity(error_name, var_name)
            if score > best_score and score > 0.6:  # 相似度阈值
                best_score = score
                best_match = var_name
        
        if best_match:
            # 使用正则表达式替换，确保只替换完整的变量名
            pattern = r'\b' + re.escape(error_name) + r'\b'
            fixed_code = re.sub(pattern, best_match, code)
            return fixed_code
        
        return None
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """计算字符串相似度"""
        from difflib import SequenceMatcher
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def analyze_code_variables(code: str) -> Dict[str, List[str]]:
    """分析代码中的变量使用情况"""
    try:
        tree = ast.parse(code)
        
        class VariableAnalyzer(ast.NodeVisitor):
            def __init__(self):
                self.assigned = set()
                self.used = set()
                self.imported = set()
            
            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Store):
                    self.assigned.add(node.id)
                elif isinstance(node.ctx, ast.Load):
                    self.used.add(node.id)
                self.generic_visit(node)
            
            def visit_Import(self, node):
                for alias in node.names:
                    self.imported.add(alias.asname or alias.name)
                self.generic_visit(node)
            
            def visit_ImportFrom(self, node):
                for alias in node.names:
                    self.imported.add(alias.asname or alias.name)
                self.generic_visit(node)
        
        analyzer = VariableAnalyzer()
        analyzer.visit(tree)
        
        return {
            'assigned': list(analyzer.assigned),
            'used': list(analyzer.used),
            'imported': list(analyzer.imported),
            'undefined': list(analyzer.used - analyzer.assigned - analyzer.imported)
        }
    
    except SyntaxError as e:
        return {
            'error': f'语法错误: {str(e)}',
            'assigned': [],
            'used': [],
            'imported': [],
            'undefined': []
        }

def enhanced_execute_with_error_handling(code: str, 
                                       global_vars: Optional[Dict[str, Any]] = None,
                                       variable_manager: Optional[VariableLifecycleManager] = None) -> Dict[str, Any]:
    """增强的代码执行与错误处理"""
    if global_vars is None:
        global_vars = {}
    
    if variable_manager is None:
        variable_manager = VariableLifecycleManager()
    
    # 添加常用模块到全局变量
    global_vars.update({
        'pd': pd,
        'np': __import__('numpy'),
        'plt': __import__('matplotlib.pyplot'),
        'sns': __import__('seaborn')
    })
    
    # 将变量管理器中的变量添加到全局变量
    global_vars.update(variable_manager.variables)
    
    # 捕获输出
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    stdout_capture = StringIO()
    stderr_capture = StringIO()
    
    result = {
        'success': False,
        'output': '',
        'error': '',
        'variables_created': [],
        'suggestions': []
    }
    
    try:
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture
        
        # 分析代码变量
        var_analysis = analyze_code_variables(code)
        
        # 执行代码
        exec(code, global_vars)
        
        # 检查新创建的变量
        for var_name in var_analysis.get('assigned', []):
            if var_name in global_vars:
                variable_manager.register_variable(var_name, global_vars[var_name])
                result['variables_created'].append(var_name)
        
        result['success'] = True
        result['output'] = stdout_capture.getvalue()
        
    except NameError as e:
        error_msg = str(e)
        # 提取未定义的变量名
        match = re.search(r"name '(.+?)' is not defined", error_msg)
        if match:
            undefined_var = match.group(1)
            name_handler = NameErrorHandler(variable_manager)
            suggestions = name_handler.suggest_fixes(undefined_var)
            
            # 尝试自动修复
            fixed_code = name_handler.auto_fix_code(code, undefined_var)
            if fixed_code:
                suggestions.append(f"自动修复建议: {fixed_code}")
            
            result['suggestions'] = suggestions
        
        result['error'] = f"名称错误: {error_msg}"
        result['error'] += f"\n可用变量: {list(variable_manager.get_available_variables().keys())}"
        
    except Exception as e:
        error_details = traceback.format_exc()
        data_info = {
            'available_variables': list(variable_manager.get_available_variables().keys()),
            'code_snippet': code[:100]  # 截取部分代码
        }
        # 使用新的异常类封装错误
        processing_error = DataProcessingError(
            f"执行错误: {str(e)}",
            data_info=data_info,
            error_details=error_details
        )
        result['error'] = str(processing_error)
        
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        
        # 添加stderr内容到错误信息
        stderr_content = stderr_capture.getvalue()
        if stderr_content:
            result['error'] += f"\nStderr: {stderr_content}"
    
    return result

# 全局变量管理器实例
_global_variable_manager = VariableLifecycleManager()

def get_global_variable_manager() -> VariableLifecycleManager:
    """获取全局变量管理器"""
    return _global_variable_manager