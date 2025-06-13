# -*- coding: utf-8 -*-
"""
安全代码执行器
实现基于 AST 分析的安全代码执行环境
"""

import ast
import sys
import time
import threading
import resource
import signal
import traceback
from typing import Dict, Any, List, Optional, Set
from io import StringIO
from contextlib import contextmanager
import pandas as pd
import numpy as np
import logging

# 配置日志
logger = logging.getLogger(__name__)

class SecurityViolationError(Exception):
    """安全违规异常"""
    pass

class ExecutionTimeoutError(Exception):
    """执行超时异常"""
    pass

class MemoryLimitError(Exception):
    """内存限制异常"""
    pass

class ASTSecurityAnalyzer(ast.NodeVisitor):
    """AST 安全分析器"""
    
    def __init__(self):
        self.violations = []
        self.imports = set()
        self.function_calls = set()
        self.attribute_accesses = set()
        
        # 危险的内置函数
        self.dangerous_builtins = {
            'eval', 'exec', 'compile', '__import__', 'open', 'file',
            'input', 'raw_input', 'execfile', 'reload', 'vars', 'dir',
            'globals', 'locals', 'getattr', 'setattr', 'delattr', 'hasattr'
        }
        
        # 危险的模块
        self.dangerous_modules = {
            'os', 'sys', 'subprocess', 'shutil', 'socket', 'urllib',
            'requests', 'http', 'ftplib', 'smtplib', 'telnetlib',
            'pickle', 'marshal', 'shelve', 'dbm', 'sqlite3'
        }
        
        # 允许的模块
        self.allowed_modules = {
            'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly',
            'math', 'statistics', 'datetime', 'json', 're'
        }
        
        # 危险的属性访问
        self.dangerous_attributes = {
            '__class__', '__bases__', '__subclasses__', '__mro__',
            '__globals__', '__code__', '__func__', '__self__',
            'func_globals', 'func_code', 'gi_frame', 'cr_frame'
        }
    
    def visit_Import(self, node):
        """检查 import 语句"""
        for alias in node.names:
            module_name = alias.name.split('.')[0]
            self.imports.add(module_name)
            
            if module_name in self.dangerous_modules:
                self.violations.append(
                    f"危险模块导入: {alias.name} (行 {node.lineno})"
                )
            elif module_name not in self.allowed_modules:
                self.violations.append(
                    f"未授权模块导入: {alias.name} (行 {node.lineno})"
                )
        
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """检查 from ... import 语句"""
        if node.module:
            module_name = node.module.split('.')[0]
            self.imports.add(module_name)
            
            if module_name in self.dangerous_modules:
                self.violations.append(
                    f"危险模块导入: from {node.module} (行 {node.lineno})"
                )
            elif module_name not in self.allowed_modules:
                self.violations.append(
                    f"未授权模块导入: from {node.module} (行 {node.lineno})"
                )
        
        self.generic_visit(node)
    
    def visit_Call(self, node):
        """检查函数调用"""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            self.function_calls.add(func_name)
            
            if func_name in self.dangerous_builtins:
                self.violations.append(
                    f"危险函数调用: {func_name}() (行 {node.lineno})"
                )
        
        self.generic_visit(node)
    
    def visit_Attribute(self, node):
        """检查属性访问"""
        attr_name = node.attr
        self.attribute_accesses.add(attr_name)
        
        if attr_name in self.dangerous_attributes:
            self.violations.append(
                f"危险属性访问: .{attr_name} (行 {node.lineno})"
            )
        
        self.generic_visit(node)
    
    def visit_Subscript(self, node):
        """检查下标访问（可能的代码注入）"""
        if isinstance(node.slice, ast.Str):
            # 检查是否尝试访问危险的字符串键
            key = node.slice.s
            if key.startswith('__') and key.endswith('__'):
                self.violations.append(
                    f"可疑的魔术方法访问: [{repr(key)}] (行 {node.lineno})"
                )
        
        self.generic_visit(node)
    
    def analyze(self, code: str) -> List[str]:
        """分析代码并返回安全违规列表"""
        try:
            tree = ast.parse(code)
            self.visit(tree)
            return self.violations
        except SyntaxError as e:
            return [f"语法错误: {e}"]

class ResourceMonitor:
    """资源监控器"""
    
    def __init__(self, max_memory_mb: int = 512, max_execution_time: int = 30):
        self.max_memory = max_memory_mb * 1024 * 1024  # 转换为字节
        self.max_execution_time = max_execution_time
        self.start_time = None
        self.timeout_occurred = False
    
    def check_memory_usage(self):
        """检查内存使用情况"""
        try:
            # 获取当前进程的内存使用情况
            usage = resource.getrusage(resource.RUSAGE_SELF)
            memory_usage = usage.ru_maxrss
            
            # macOS 返回的是字节，Linux 返回的是 KB
            if sys.platform == 'darwin':  # macOS
                memory_usage_bytes = memory_usage
            else:  # Linux
                memory_usage_bytes = memory_usage * 1024
            
            if memory_usage_bytes > self.max_memory:
                raise MemoryLimitError(
                    f"内存使用超限: {memory_usage_bytes / (1024*1024):.1f}MB > {self.max_memory / (1024*1024)}MB"
                )
        except Exception as e:
            logger.warning(f"内存检查失败: {e}")
    
    def timeout_handler(self, signum, frame):
        """超时处理器"""
        self.timeout_occurred = True
        raise ExecutionTimeoutError(f"代码执行超时: {self.max_execution_time}秒")
    
    @contextmanager
    def monitor_execution(self):
        """监控代码执行"""
        self.start_time = time.time()
        self.timeout_occurred = False
        
        # 设置超时信号
        old_handler = signal.signal(signal.SIGALRM, self.timeout_handler)
        signal.alarm(self.max_execution_time)
        
        try:
            yield self
        finally:
            # 恢复原始信号处理器
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)

class SecureCodeExecutor:
    """安全代码执行器"""
    
    def __init__(self, 
                 max_memory_mb: int = 512,
                 max_execution_time: int = 30,
                 enable_ast_analysis: bool = True):
        """
        初始化安全代码执行器
        
        Args:
            max_memory_mb: 最大内存使用量（MB）
            max_execution_time: 最大执行时间（秒）
            enable_ast_analysis: 是否启用 AST 安全分析
        """
        self.max_memory_mb = max_memory_mb
        self.max_execution_time = max_execution_time
        self.enable_ast_analysis = enable_ast_analysis
        
        self.analyzer = ASTSecurityAnalyzer()
        self.monitor = ResourceMonitor(max_memory_mb, max_execution_time)
        
        # 安全的内置函数白名单
        self.safe_builtins = {
            'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'enumerate',
            'filter', 'float', 'format', 'frozenset', 'hex', 'int', 'len',
            'list', 'map', 'max', 'min', 'oct', 'ord', 'pow', 'range',
            'reversed', 'round', 'set', 'slice', 'sorted', 'str', 'sum',
            'tuple', 'type', 'zip'
        }
        
        # 安全的模块白名单
        self.safe_modules = {
            'pandas': pd,
            'pd': pd,
            'numpy': np,
            'np': np
        }
    
    def create_safe_globals(self) -> Dict[str, Any]:
        """创建安全的全局命名空间"""
        safe_globals = {
            '__builtins__': {
                name: __builtins__[name] 
                for name in self.safe_builtins 
                if name in __builtins__
            }
        }
        
        # 添加安全的模块
        safe_globals.update(self.safe_modules)
        
        return safe_globals
    
    def execute_code(self, 
                     code: str, 
                     context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        安全执行代码
        
        Args:
            code: 要执行的代码
            context: 执行上下文（如数据框等）
            
        Returns:
            Dict: 执行结果
        """
        logger.info(f"开始安全代码执行，代码长度: {len(code)} 字符")
        
        try:
            # 1. AST 安全分析
            if self.enable_ast_analysis:
                violations = self.analyzer.analyze(code)
                if violations:
                    return {
                        "success": False,
                        "error": "安全检查失败",
                        "violations": violations,
                        "suggestion": "请移除代码中的危险操作"
                    }
            
            # 2. 准备执行环境
            safe_globals = self.create_safe_globals()
            safe_locals = context.copy() if context else {}
            
            # 3. 捕获输出
            old_stdout = sys.stdout
            captured_output = StringIO()
            sys.stdout = captured_output
            
            # 4. 在资源监控下执行代码
            with self.monitor.monitor_execution():
                try:
                    # 定期检查内存使用
                    def memory_check_thread():
                        while not self.monitor.timeout_occurred:
                            self.monitor.check_memory_usage()
                            time.sleep(1)
                    
                    # 启动内存监控线程
                    monitor_thread = threading.Thread(target=memory_check_thread, daemon=True)
                    monitor_thread.start()
                    
                    # 执行代码
                    exec(code, safe_globals, safe_locals)
                    
                except Exception as e:
                    raise e
            
            # 5. 处理执行结果
            output = captured_output.getvalue()
            
            # 检查结果变量
            result_data = None
            if 'result' in safe_locals:
                result = safe_locals['result']
                result_data = self._process_result(result)
            
            execution_time = time.time() - self.monitor.start_time
            
            logger.info(f"代码执行成功，耗时: {execution_time:.2f}秒")
            
            return {
                "success": True,
                "output": output,
                "result": result_data,
                "execution_time": execution_time,
                "memory_peak": self._get_memory_usage(),
                "suggestion": "代码执行成功。使用 'result' 变量存储最终输出。"
            }
            
        except SecurityViolationError as e:
            logger.warning(f"安全违规: {e}")
            return {
                "success": False,
                "error": "安全违规",
                "message": str(e),
                "suggestion": "请检查代码中的安全问题"
            }
            
        except ExecutionTimeoutError as e:
            logger.warning(f"执行超时: {e}")
            return {
                "success": False,
                "error": "执行超时",
                "message": str(e),
                "suggestion": f"请优化代码性能或增加超时限制（当前: {self.max_execution_time}秒）"
            }
            
        except MemoryLimitError as e:
            logger.warning(f"内存超限: {e}")
            return {
                "success": False,
                "error": "内存超限",
                "message": str(e),
                "suggestion": f"请减少内存使用或增加内存限制（当前: {self.max_memory_mb}MB）"
            }
            
        except Exception as e:
            logger.error(f"代码执行失败: {e}")
            return {
                "success": False,
                "error": "执行失败",
                "message": str(e),
                "traceback": traceback.format_exc(),
                "suggestion": "请检查代码语法和逻辑错误"
            }
            
        finally:
            # 恢复标准输出
            sys.stdout = old_stdout
    
    def _process_result(self, result: Any) -> Dict[str, Any]:
        """处理执行结果"""
        if isinstance(result, pd.DataFrame):
            return {
                "type": "DataFrame",
                "shape": result.shape,
                "columns": result.columns.tolist(),
                "data": result.head(10).to_dict('records'),
                "dtypes": result.dtypes.astype(str).to_dict()
            }
        elif isinstance(result, pd.Series):
            return {
                "type": "Series",
                "name": result.name,
                "length": len(result),
                "data": result.head(10).tolist(),
                "dtype": str(result.dtype)
            }
        elif isinstance(result, np.ndarray):
            return {
                "type": "ndarray",
                "shape": result.shape,
                "dtype": str(result.dtype),
                "data": result.flatten()[:10].tolist() if result.size > 0 else []
            }
        else:
            return {
                "type": type(result).__name__,
                "value": str(result)
            }
    
    def _get_memory_usage(self) -> float:
        """获取当前内存使用量（MB）"""
        try:
            usage = resource.getrusage(resource.RUSAGE_SELF)
            memory_usage = usage.ru_maxrss
            
            if sys.platform == 'darwin':  # macOS
                return memory_usage / (1024 * 1024)
            else:  # Linux
                return memory_usage / 1024
        except Exception:
            return 0.0

# 便捷函数
def execute_safe_code(code: str, 
                      context: Optional[Dict[str, Any]] = None,
                      max_memory_mb: int = 512,
                      max_execution_time: int = 30) -> Dict[str, Any]:
    """便捷的安全代码执行函数"""
    executor = SecureCodeExecutor(
        max_memory_mb=max_memory_mb,
        max_execution_time=max_execution_time
    )
    return executor.execute_code(code, context)

if __name__ == "__main__":
    # 测试代码
    test_code = """
import pandas as pd
import numpy as np

# 创建测试数据
data = {'A': [1, 2, 3, 4, 5], 'B': [10, 20, 30, 40, 50]}
df = pd.DataFrame(data)

# 计算统计信息
result = df.describe()
print("数据统计:")
print(result)
"""
    
    executor = SecureCodeExecutor()
    result = executor.execute_code(test_code)
    print("执行结果:", result)