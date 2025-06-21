"""Code Executor Service Module.

Provides secure code execution with timeout control, sandboxing,
and comprehensive error handling.
"""

import ast
import sys
import io
import contextlib
import time
import threading
import traceback
from typing import Dict, Any, Optional, List, Tuple, Union
from datetime import datetime
import pandas as pd
import numpy as np

try:
    from core.config import get_config
    from core.exceptions import (
        CodeExecutionError, SecurityError, TimeoutError,
        ValidationError
    )
    from core.types import ExecutionResult, ExecutionStatus
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    # Fallback types
    class ExecutionResult:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
    
    class ExecutionStatus:
        SUCCESS = "success"
        ERROR = "error"
        TIMEOUT = "timeout"
        SECURITY_VIOLATION = "security_violation"


class CodeExecutor:
    """Secure code executor with advanced features."""
    
    def __init__(self):
        """Initialize code executor."""
        self.config = get_config() if CORE_AVAILABLE else None
        self.execution_history = []
        self._setup_safe_environment()
    
    def _setup_safe_environment(self):
        """Setup safe execution environment."""
        # Define allowed modules and functions
        self.allowed_modules = {
            'pandas', 'numpy', 'math', 'datetime', 'json', 're',
            'collections', 'itertools', 'functools', 'operator'
        }
        
        # Define forbidden functions and attributes
        self.forbidden_names = {
            '__import__', 'eval', 'exec', 'compile', 'open', 'file',
            'input', 'raw_input', 'reload', 'vars', 'dir', 'globals',
            'locals', 'hasattr', 'getattr', 'setattr', 'delattr',
            'isinstance', 'issubclass', 'callable', '__builtins__'
        }
        
        # Define safe built-ins
        self.safe_builtins = {
            'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'enumerate',
            'filter', 'float', 'format', 'frozenset', 'hex', 'int', 'len',
            'list', 'map', 'max', 'min', 'oct', 'ord', 'pow', 'range',
            'reversed', 'round', 'set', 'slice', 'sorted', 'str', 'sum',
            'tuple', 'type', 'zip', 'print'
        }
    
    def validate_code(self, code: str) -> Tuple[bool, List[str]]:
        """Validate code for security issues.
        
        Args:
            code: Python code to validate
            
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        try:
            # Parse the code into AST
            tree = ast.parse(code)
            
            # Check for forbidden constructs
            for node in ast.walk(tree):
                # Check for imports
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if alias.name.split('.')[0] not in self.allowed_modules:
                                issues.append(f"不允许导入模块: {alias.name}")
                    elif isinstance(node, ast.ImportFrom):
                        if node.module and node.module.split('.')[0] not in self.allowed_modules:
                            issues.append(f"不允许从模块导入: {node.module}")
                
                # Check for function calls
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in self.forbidden_names:
                            issues.append(f"不允许调用函数: {node.func.id}")
                
                # Check for attribute access
                elif isinstance(node, ast.Attribute):
                    if node.attr.startswith('_'):
                        issues.append(f"不允许访问私有属性: {node.attr}")
                
                # Check for name access
                elif isinstance(node, ast.Name):
                    if node.id in self.forbidden_names:
                        issues.append(f"不允许使用名称: {node.id}")
        
        except SyntaxError as e:
            issues.append(f"语法错误: {e}")
        except Exception as e:
            issues.append(f"代码分析错误: {e}")
        
        return len(issues) == 0, issues
    
    def execute_code(self, code: str, context: Optional[Dict[str, Any]] = None,
                    timeout: Optional[int] = None) -> ExecutionResult:
        """Execute Python code safely.
        
        Args:
            code: Python code to execute
            context: Execution context with variables
            timeout: Execution timeout in seconds
            
        Returns:
            ExecutionResult with execution details
        """
        start_time = datetime.now()
        
        # Set timeout
        if timeout is None:
            timeout = self.config.performance.execution_timeout if self.config else 30
        
        # Validate code first
        is_valid, issues = self.validate_code(code)
        if not is_valid:
            error_msg = "代码安全检查失败:\n" + "\n".join(issues)
            if CORE_AVAILABLE:
                raise SecurityError(operation="代码安全检查", reason=error_msg)
            else:
                raise Exception(error_msg)
        
        # Prepare execution context
        exec_context = self._prepare_context(context)
        
        # Execute with timeout
        try:
            result = self._execute_with_timeout(code, exec_context, timeout)
            
            execution_result = ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                result=result['result'],
                output=result['output'],
                error=None,
                execution_time=(datetime.now() - start_time).total_seconds(),
                context_variables=self._extract_variables(result['namespace']),
                code=code
            )
            
        except TimeoutError as e:
            execution_result = ExecutionResult(
                status=ExecutionStatus.TIMEOUT,
                result=None,
                output="",
                error=str(e),
                execution_time=timeout,
                context_variables={},
                code=code
            )
            
        except Exception as e:
            error_details = traceback.format_exc()
            if CORE_AVAILABLE:
                # 确保将详细错误信息作为 error_details 传递
                raise CodeExecutionError(code=code, error_details=error_details) from e
            else:
                execution_result = ExecutionResult(
                    status=ExecutionStatus.ERROR,
                    result=None,
                    output="",
                    error=error_details,
                    execution_time=(datetime.now() - start_time).total_seconds(),
                    context_variables={},
                    code=code
                )
        
        # Store in history
        self.execution_history.append(execution_result)
        
        return execution_result
    
    def _prepare_context(self, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Prepare safe execution context."""
        # Start with safe built-ins
        safe_context = {
            '__builtins__': {name: getattr(__builtins__, name) 
                           for name in self.safe_builtins 
                           if hasattr(__builtins__, name)}
        }
        
        # Add common libraries
        safe_context.update({
            'pd': pd,
            'pandas': pd,
            'np': np,
            'numpy': np
        })
        
        # Add user context if provided
        if context:
            for key, value in context.items():
                if not key.startswith('_') and key not in self.forbidden_names:
                    safe_context[key] = value
        
        return safe_context
    
    def _execute_with_timeout(self, code: str, context: Dict[str, Any], 
                             timeout: int) -> Dict[str, Any]:
        """Execute code with timeout control."""
        result = {'result': None, 'output': '', 'namespace': context.copy()}
        exception_holder = []
        
        def target():
            try:
                # Capture stdout
                old_stdout = sys.stdout
                sys.stdout = captured_output = io.StringIO()
                
                try:
                    # Execute the code
                    exec_result = None
                    
                    # Try to evaluate as expression first
                    try:
                        exec_result = eval(code, result['namespace'])
                    except SyntaxError:
                        # If not an expression, execute as statement
                        exec(code, result['namespace'])
                    
                    result['result'] = exec_result
                    result['output'] = captured_output.getvalue()
                    
                finally:
                    sys.stdout = old_stdout
                    
            except Exception as e:
                exception_holder.append(e)
        
        # Start execution thread
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        thread.join(timeout)
        
        if thread.is_alive():
            # Timeout occurred
            if CORE_AVAILABLE:
                raise TimeoutError(f"代码执行超时 ({timeout}秒)")
            else:
                raise Exception(f"代码执行超时 ({timeout}秒)")
        
        if exception_holder:
            raise exception_holder[0]
        
        return result
    
    def _extract_variables(self, namespace: Dict[str, Any]) -> Dict[str, Any]:
        """Extract user-defined variables from namespace."""
        variables = {}
        
        for name, value in namespace.items():
            # Skip built-ins and modules
            if (not name.startswith('_') and 
                name not in self.safe_builtins and
                name not in ['pd', 'pandas', 'np', 'numpy'] and
                not callable(value) or isinstance(value, (pd.DataFrame, pd.Series))):
                
                # Convert to serializable format
                try:
                    if isinstance(value, (pd.DataFrame, pd.Series)):
                        variables[name] = {
                            'type': type(value).__name__,
                            'shape': getattr(value, 'shape', None),
                            'dtype': str(getattr(value, 'dtype', None)),
                            'preview': str(value.head() if hasattr(value, 'head') else value)
                        }
                    elif isinstance(value, (list, dict, str, int, float, bool)):
                        variables[name] = value
                    else:
                        variables[name] = str(value)
                except:
                    variables[name] = f"<{type(value).__name__} object>"
        
        return variables
    
    def analyze_code_dependencies(self, code: str) -> Dict[str, Any]:
        """Analyze code dependencies and complexity.
        
        Args:
            code: Python code to analyze
            
        Returns:
            Analysis results
        """
        try:
            tree = ast.parse(code)
            
            analysis = {
                'imports': [],
                'functions_called': [],
                'variables_assigned': [],
                'complexity_score': 0,
                'line_count': len(code.split('\n')),
                'has_loops': False,
                'has_conditions': False
            }
            
            for node in ast.walk(tree):
                # Track imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        analysis['imports'].append(node.module)
                
                # Track function calls
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        analysis['functions_called'].append(node.func.id)
                    elif isinstance(node.func, ast.Attribute):
                        analysis['functions_called'].append(node.func.attr)
                
                # Track variable assignments
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            analysis['variables_assigned'].append(target.id)
                
                # Track control structures
                elif isinstance(node, (ast.For, ast.While)):
                    analysis['has_loops'] = True
                    analysis['complexity_score'] += 2
                elif isinstance(node, (ast.If, ast.IfExp)):
                    analysis['has_conditions'] = True
                    analysis['complexity_score'] += 1
            
            # Remove duplicates
            analysis['imports'] = list(set(analysis['imports']))
            analysis['functions_called'] = list(set(analysis['functions_called']))
            analysis['variables_assigned'] = list(set(analysis['variables_assigned']))
            
            return analysis
            
        except Exception as e:
            return {'error': f"代码分析失败: {e}"}
    
    def get_execution_history(self, limit: int = 10) -> List[ExecutionResult]:
        """Get recent execution history.
        
        Args:
            limit: Maximum number of results to return
            
        Returns:
            List of recent execution results
        """
        return self.execution_history[-limit:]
    
    def clear_history(self):
        """Clear execution history."""
        self.execution_history.clear()
    
    def get_suggestions_for_error(self, error: str, code: str) -> List[str]:
        """Get suggestions for fixing code errors.
        
        Args:
            error: Error message
            code: Original code
            
        Returns:
            List of suggestions
        """
        suggestions = []
        
        error_lower = error.lower()
        
        # Common error patterns and suggestions
        if 'nameError' in error or 'not defined' in error_lower:
            suggestions.append("检查变量名是否正确拼写")
            suggestions.append("确保变量在使用前已定义")
            suggestions.append("检查是否需要导入相关模块")
        
        elif 'syntaxError' in error or 'invalid syntax' in error_lower:
            suggestions.append("检查代码语法，特别是括号、引号的匹配")
            suggestions.append("确保缩进正确")
            suggestions.append("检查是否有多余的逗号或分号")
        
        elif 'keyError' in error:
            suggestions.append("检查字典键名是否存在")
            suggestions.append("使用 .get() 方法安全访问字典")
            suggestions.append("检查数据框列名是否正确")
        
        elif 'indexError' in error:
            suggestions.append("检查列表或数组索引是否超出范围")
            suggestions.append("使用 len() 检查序列长度")
        
        elif 'typeError' in error:
            suggestions.append("检查数据类型是否匹配")
            suggestions.append("确保函数参数类型正确")
            suggestions.append("检查是否需要类型转换")
        
        elif 'attributeError' in error:
            suggestions.append("检查对象是否有该属性或方法")
            suggestions.append("确保对象类型正确")
        
        elif 'fileNotFoundError' in error or 'no such file' in error_lower:
            suggestions.append("检查文件路径是否正确")
            suggestions.append("确保文件存在")
            suggestions.append("使用绝对路径或检查工作目录")
        
        # Add general suggestions
        if not suggestions:
            suggestions.extend([
                "检查代码逻辑是否正确",
                "尝试分步执行代码以定位问题",
                "查看完整的错误堆栈信息"
            ])
        
        return suggestions