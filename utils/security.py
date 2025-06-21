"""Security Management Module.

Provides security controls for code execution, file access,
and system resource protection.
"""

import os
import re
import ast
import sys
import time
import json
import hashlib
import tempfile
from typing import Dict, Any, List, Set, Optional, Tuple, Union
from pathlib import Path
from dataclasses import dataclass
from contextlib import contextmanager

try:
    from core.config import get_config
    from core.exceptions import SecurityError
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    def get_config():
        return {'security': {'enabled': True, 'max_execution_time': 30}}
    
    # 如果core不可用，创建简单的SecurityError类
    class SecurityError(Exception):
        def __init__(self, security_type: str, error_details: str):
            super().__init__(f"Security error ({security_type}): {error_details}")


@dataclass
class SecurityPolicy:
    """Security policy configuration."""
    allowed_modules: Set[str]
    forbidden_functions: Set[str]
    max_execution_time: int
    max_memory_usage: int
    allowed_file_extensions: Set[str]
    allowed_directories: List[str]
    enable_network: bool = False
    enable_subprocess: bool = False


class SecurityManager:
    """Comprehensive security manager for code execution and file access."""
    
    def __init__(self):
        """Initialize security manager."""
        self.config = get_config() if CORE_AVAILABLE else get_config()
        self.security_config = self.config.get('security', {})
        
        # Default security policy
        self.policy = SecurityPolicy(
            allowed_modules={
                'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly',
                'openpyxl', 'xlrd', 'xlsxwriter', 'json', 'csv',
                'datetime', 'math', 'statistics', 're', 'collections',
                'itertools', 'functools', 'operator', 'copy', 'decimal'
            },
            forbidden_functions={
                'eval', 'exec', 'compile', '__import__', 'open',
                'input', 'raw_input', 'file', 'execfile', 'reload',
                'vars', 'locals', 'globals', 'dir', 'hasattr',
                'getattr', 'setattr', 'delattr'
            },
            max_execution_time=self.security_config.get('max_execution_time', 30),
            max_memory_usage=self.security_config.get('max_memory_usage', 100 * 1024 * 1024),
            allowed_file_extensions={'.xlsx', '.xls', '.csv', '.json', '.txt'},
            allowed_directories=self.security_config.get('allowed_directories', [])
        )
        
        # Load custom policy if available
        self._load_custom_policy()
    
    def validate_code(self, code: str) -> Tuple[bool, List[str]]:
        """Validate code for security issues.
        
        Args:
            code: Python code to validate
            
        Returns:
            Tuple of (is_safe, security_issues)
        """
        issues = []
        
        try:
            # Parse code into AST
            tree = ast.parse(code)
        except SyntaxError as e:
            issues.append(f"语法错误: {e}")
            return False, issues
        
        # Check for dangerous patterns
        visitor = SecurityASTVisitor(self.policy)
        visitor.visit(tree)
        issues.extend(visitor.security_issues)
        
        # Check for dangerous imports
        import_issues = self._check_imports(code)
        issues.extend(import_issues)
        
        # Check for dangerous function calls
        function_issues = self._check_function_calls(code)
        issues.extend(function_issues)
        
        # Check for file operations
        file_issues = self._check_file_operations(code)
        issues.extend(file_issues)
        
        is_safe = len(issues) == 0
        return is_safe, issues
    
    def validate_file_access(self, file_path: str, operation: str = 'read') -> Tuple[bool, str]:
        """Validate file access permissions.
        
        Args:
            file_path: Path to file
            operation: Type of operation ('read', 'write', 'delete')
            
        Returns:
            Tuple of (is_allowed, reason)
        """
        try:
            path = Path(file_path).resolve()
        except Exception as e:
            return False, f"无效的文件路径: {e}"
        
        # Check if file exists for read operations
        if operation == 'read' and not path.exists():
            return False, "文件不存在"
        
        # Check file extension
        if path.suffix.lower() not in self.policy.allowed_file_extensions:
            return False, f"不允许的文件类型: {path.suffix}"
        
        # Check directory permissions
        if self.policy.allowed_directories:
            allowed = False
            for allowed_dir in self.policy.allowed_directories:
                try:
                    allowed_path = Path(allowed_dir).resolve()
                    if path.is_relative_to(allowed_path):
                        allowed = True
                        break
                except Exception:
                    continue
            
            if not allowed:
                return False, "文件不在允许的目录中"
        
        # Check file size for read operations
        if operation == 'read' and path.exists():
            file_size = path.stat().st_size
            max_size = 100 * 1024 * 1024  # 100MB
            if file_size > max_size:
                return False, f"文件过大 ({file_size / (1024*1024):.1f}MB > {max_size / (1024*1024):.1f}MB)"
        
        # Check write permissions
        if operation in ['write', 'delete']:
            parent_dir = path.parent
            if not os.access(parent_dir, os.W_OK):
                return False, "没有写入权限"
        
        return True, "允许访问"
    
    def create_safe_environment(self, additional_globals: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a safe execution environment.
        
        Args:
            additional_globals: Additional safe globals to include
            
        Returns:
            Safe globals dictionary
        """
        # Start with minimal safe builtins
        safe_builtins = {
            'abs', 'all', 'any', 'bin', 'bool', 'bytearray', 'bytes',
            'chr', 'complex', 'dict', 'divmod', 'enumerate', 'filter',
            'float', 'format', 'frozenset', 'hex', 'int', 'isinstance',
            'issubclass', 'iter', 'len', 'list', 'map', 'max', 'min',
            'oct', 'ord', 'pow', 'print', 'range', 'repr', 'reversed',
            'round', 'set', 'slice', 'sorted', 'str', 'sum', 'tuple',
            'type', 'zip'
        }
        
        # Create restricted builtins
        restricted_builtins = {}
        for name in safe_builtins:
            if hasattr(__builtins__, name):
                restricted_builtins[name] = getattr(__builtins__, name)
        
        # Create safe globals
        safe_globals = {
            '__builtins__': restricted_builtins,
            '__name__': '__main__',
            '__doc__': None
        }
        
        # Add additional safe globals
        if additional_globals:
            for key, value in additional_globals.items():
                if self._is_safe_object(key, value):
                    safe_globals[key] = value
        
        return safe_globals
    
    @contextmanager
    def execution_timeout(self, timeout: Optional[int] = None):
        """Context manager for execution timeout.
        
        Args:
            timeout: Timeout in seconds
        """
        timeout = timeout or self.policy.max_execution_time
        
        import signal
        
        def timeout_handler(signum, frame):
            raise SecurityError(operation="代码执行", reason=f"代码执行超时 ({timeout}秒)")
        
        # Set timeout
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)
        
        try:
            yield
        finally:
            # Restore old handler
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
    
    def generate_execution_hash(self, code: str, context: Dict[str, Any]) -> str:
        """Generate hash for code execution caching.
        
        Args:
            code: Python code
            context: Execution context
            
        Returns:
            SHA256 hash of code and context
        """
        # Create deterministic string representation
        context_str = json.dumps(context, sort_keys=True, default=str)
        combined = f"{code}:{context_str}"
        
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()
    
    def audit_log(self, action: str, details: Dict[str, Any]) -> None:
        """Log security-related actions.
        
        Args:
            action: Action type
            details: Action details
        """
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_entry = {
            'timestamp': timestamp,
            'action': action,
            'details': details
        }
        
        # In a real implementation, this would write to a secure log file
        # For now, we'll just print to stderr
        print(f"SECURITY_AUDIT: {json.dumps(log_entry)}", file=sys.stderr)
    
    def _load_custom_policy(self) -> None:
        """Load custom security policy from configuration."""
        security_config = self.security_config
        
        # Update allowed modules
        if 'allowed_modules' in security_config:
            self.policy.allowed_modules.update(security_config['allowed_modules'])
        
        # Update forbidden functions
        if 'forbidden_functions' in security_config:
            self.policy.forbidden_functions.update(security_config['forbidden_functions'])
        
        # Update other settings
        if 'allowed_file_extensions' in security_config:
            self.policy.allowed_file_extensions.update(security_config['allowed_file_extensions'])
    
    def _check_imports(self, code: str) -> List[str]:
        """Check for dangerous imports."""
        issues = []
        
        # Pattern for import statements
        import_patterns = [
            r'import\s+([\w\.]+)',
            r'from\s+([\w\.]+)\s+import'
        ]
        
        for pattern in import_patterns:
            matches = re.finditer(pattern, code)
            for match in matches:
                module_name = match.group(1).split('.')[0]
                if module_name not in self.policy.allowed_modules:
                    issues.append(f"不允许导入模块: {module_name}")
        
        return issues
    
    def _check_function_calls(self, code: str) -> List[str]:
        """Check for dangerous function calls."""
        issues = []
        
        for func_name in self.policy.forbidden_functions:
            pattern = rf'\b{re.escape(func_name)}\s*\('
            if re.search(pattern, code):
                issues.append(f"不允许调用函数: {func_name}")
        
        return issues
    
    def _check_file_operations(self, code: str) -> List[str]:
        """Check for direct file operations."""
        issues = []
        
        # Check for direct file operations
        file_patterns = [
            r'\bopen\s*\(',
            r'\bfile\s*\(',
            r'\bwith\s+open\s*\('
        ]
        
        for pattern in file_patterns:
            if re.search(pattern, code):
                issues.append("检测到直接文件操作，建议使用提供的安全文件操作接口")
                break
        
        return issues
    
    def _is_safe_object(self, name: str, obj: Any) -> bool:
        """Check if an object is safe to include in execution environment."""
        # Check name
        if name.startswith('_'):
            return False
        
        # Check for dangerous types
        dangerous_types = (type, type(lambda: None), type(open))
        if isinstance(obj, dangerous_types):
            return False
        
        # Check for modules
        if hasattr(obj, '__module__'):
            module_name = getattr(obj, '__module__', '')
            if module_name and module_name.split('.')[0] not in self.policy.allowed_modules:
                return False
        
        return True


class SecurityASTVisitor(ast.NodeVisitor):
    """AST visitor for security analysis."""
    
    def __init__(self, policy: SecurityPolicy):
        """Initialize visitor.
        
        Args:
            policy: Security policy
        """
        self.policy = policy
        self.security_issues = []
    
    def visit_Import(self, node: ast.Import) -> None:
        """Visit import statements."""
        for alias in node.names:
            module_name = alias.name.split('.')[0]
            if module_name not in self.policy.allowed_modules:
                self.security_issues.append(f"不允许导入模块: {module_name}")
        
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit from-import statements."""
        if node.module:
            module_name = node.module.split('.')[0]
            if module_name not in self.policy.allowed_modules:
                self.security_issues.append(f"不允许导入模块: {module_name}")
        
        self.generic_visit(node)
    
    def visit_Call(self, node: ast.Call) -> None:
        """Visit function calls."""
        # Check for forbidden function calls
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in self.policy.forbidden_functions:
                self.security_issues.append(f"不允许调用函数: {func_name}")
        
        # Check for attribute calls on forbidden functions
        elif isinstance(node.func, ast.Attribute):
            attr_name = node.func.attr
            if attr_name in self.policy.forbidden_functions:
                self.security_issues.append(f"不允许调用方法: {attr_name}")
        
        self.generic_visit(node)
    
    def visit_Attribute(self, node: ast.Attribute) -> None:
        """Visit attribute access."""
        # Check for dangerous attribute access
        dangerous_attrs = {'__globals__', '__locals__', '__code__', '__func__'}
        if node.attr in dangerous_attrs:
            self.security_issues.append(f"不允许访问属性: {node.attr}")
        
        self.generic_visit(node)


# Global security manager instance
_global_security_manager = None


def get_security_manager() -> SecurityManager:
    """Get global security manager instance.
    
    Returns:
        Global SecurityManager instance
    """
    global _global_security_manager
    if _global_security_manager is None:
        _global_security_manager = SecurityManager()
    return _global_security_manager


def secure_execution(timeout: Optional[int] = None):
    """Decorator for secure code execution.
    
    Args:
        timeout: Execution timeout in seconds
        
    Returns:
        Decorated function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            security_manager = get_security_manager()
            
            with security_manager.execution_timeout(timeout):
                return func(*args, **kwargs)
        
        return wrapper
    return decorator