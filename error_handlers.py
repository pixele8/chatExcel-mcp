#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
错误处理器实现 - 责任链模式

提供各种类型的错误处理器：
- 文件访问错误处理器
- 编码错误处理器
- 列头解析错误处理器
- 代码执行错误处理器
- 自动修复处理器

作者: AI Assistant
创建时间: 2024-12-19
版本: 1.0.0
"""

import os
import re
import logging
import traceback
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, Optional, List
from pathlib import Path

import pandas as pd
import numpy as np

# 设置日志
logger = logging.getLogger(__name__)

class ErrorHandlerChain:
    """
    错误处理器链
    
    实现责任链模式，按顺序处理各种错误
    """
    
    def __init__(self):
        self.handlers = []
    
    def add_handler(self, handler):
        """添加错误处理器"""
        self.handlers.append(handler)
    
    def handle_error(self, error: Exception, context: Dict[str, Any]) -> Tuple[bool, Any]:
        """处理错误"""
        for handler in self.handlers:
            try:
                handled, result = handler.handle(error, context)
                if handled:
                    return True, result
            except Exception as e:
                logger.error(f"错误处理器 {handler.name} 处理失败: {e}")
                continue
        return False, None
    
    def handle(self, error: Exception, context: Dict[str, Any]) -> Tuple[bool, Any]:
        """处理错误的别名方法，兼容性接口"""
        return self.handle_error(error, context)
    
    @classmethod
    def create_default_chain(cls):
        """创建默认错误处理器链"""
        chain = cls()
        # 这里可以添加默认的错误处理器
        return chain


class BaseErrorHandler(ABC):
    """错误处理器基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.handled_count = 0
        self.success_count = 0
    
    @abstractmethod
    def can_handle(self, error: Exception, context: Dict[str, Any]) -> bool:
        """判断是否能处理该错误"""
        pass
    
    @abstractmethod
    def _handle_error(self, error: Exception, context: Dict[str, Any]) -> Tuple[bool, Any]:
        """具体的错误处理逻辑"""
        pass
    
    def handle(self, error: Exception, context: Dict[str, Any]) -> Tuple[bool, Any]:
        """处理错误的统一入口"""
        if not self.can_handle(error, context):
            return False, None
        
        self.handled_count += 1
        try:
            success, result = self._handle_error(error, context)
            if success:
                self.success_count += 1
            return success, result
        except Exception as e:
            logger.error(f"错误处理器 {self.name} 处理失败: {e}")
            return False, None
    
    def get_stats(self) -> Dict[str, int]:
        """获取处理统计信息"""
        return {
            "handled_count": self.handled_count,
            "success_count": self.success_count,
            "success_rate": self.success_count / max(self.handled_count, 1)
        }


class FileAccessErrorHandler(BaseErrorHandler):
    """文件访问错误处理器"""
    
    def __init__(self):
        super().__init__("FileAccessErrorHandler")
    
    def can_handle(self, error: Exception, context: Dict[str, Any]) -> bool:
        """判断是否为文件访问错误"""
        return isinstance(error, (FileNotFoundError, PermissionError, OSError))
    
    def _handle_error(self, error: Exception, context: Dict[str, Any]) -> Tuple[bool, Any]:
        """处理文件访问错误"""
        file_path = context.get('file_path', '')
        
        if isinstance(error, FileNotFoundError):
            # 尝试查找相似文件名
            similar_files = self._find_similar_files(file_path)
            if similar_files:
                return True, {
                    "error_type": "file_not_found",
                    "suggestions": similar_files,
                    "message": f"文件未找到，建议的替代文件: {', '.join(similar_files[:3])}"
                }
        
        elif isinstance(error, PermissionError):
            return True, {
                "error_type": "permission_denied",
                "message": f"文件访问权限不足: {file_path}",
                "suggestion": "请检查文件权限或使用管理员权限运行"
            }
        
        return False, None
    
    def _find_similar_files(self, file_path: str) -> List[str]:
        """查找相似的文件名"""
        try:
            path = Path(file_path)
            directory = path.parent
            filename = path.name
            
            if not directory.exists():
                return []
            
            similar_files = []
            for file in directory.iterdir():
                if file.is_file() and self._is_similar(filename, file.name):
                    similar_files.append(str(file))
            
            return similar_files[:5]  # 最多返回5个
        except Exception:
            return []
    
    def _is_similar(self, name1: str, name2: str) -> bool:
        """判断文件名是否相似"""
        # 简单的相似度判断
        name1_lower = name1.lower()
        name2_lower = name2.lower()
        
        # 检查是否包含相同的词根
        if len(name1_lower) > 3 and len(name2_lower) > 3:
            return name1_lower[:3] == name2_lower[:3] or name1_lower in name2_lower or name2_lower in name1_lower
        
        return False


class EncodingErrorHandler(BaseErrorHandler):
    """编码错误处理器"""
    
    def __init__(self):
        super().__init__("EncodingErrorHandler")
        self.encoding_fallbacks = ['utf-8', 'gbk', 'gb2312', 'latin1', 'cp1252']
    
    def can_handle(self, error: Exception, context: Dict[str, Any]) -> bool:
        """判断是否为编码错误"""
        return isinstance(error, (UnicodeDecodeError, UnicodeError))
    
    def _handle_error(self, error: Exception, context: Dict[str, Any]) -> Tuple[bool, Any]:
        """处理编码错误"""
        file_path = context.get('file_path', '')
        
        # 尝试不同的编码
        for encoding in self.encoding_fallbacks:
            try:
                if file_path and os.path.exists(file_path):
                    with open(file_path, 'r', encoding=encoding) as f:
                        f.read(100)  # 尝试读取前100个字符
                    
                    return True, {
                        "error_type": "encoding_fixed",
                        "suggested_encoding": encoding,
                        "message": f"建议使用编码: {encoding}"
                    }
            except Exception:
                continue
        
        return True, {
            "error_type": "encoding_detection_failed",
            "message": "无法自动检测文件编码",
            "suggestions": self.encoding_fallbacks
        }


class ColumnParsingErrorHandler(BaseErrorHandler):
    """列头解析错误处理器"""
    
    def __init__(self):
        super().__init__("ColumnParsingErrorHandler")
    
    def can_handle(self, error: Exception, context: Dict[str, Any]) -> bool:
        """判断是否为列解析错误"""
        error_msg = str(error).lower()
        return any(keyword in error_msg for keyword in [
            'column', 'header', 'index', 'key', 'duplicate'
        ])
    
    def _handle_error(self, error: Exception, context: Dict[str, Any]) -> Tuple[bool, Any]:
        """处理列解析错误"""
        error_msg = str(error).lower()
        
        if 'duplicate' in error_msg:
            return True, {
                "error_type": "duplicate_columns",
                "message": "检测到重复列名",
                "suggestion": "建议使用 mangle_dupe_cols=True 参数"
            }
        
        if 'header' in error_msg or 'column' in error_msg:
            return True, {
                "error_type": "header_parsing",
                "message": "列头解析失败",
                "suggestions": [
                    "尝试设置 header=None",
                    "检查文件是否有多级表头",
                    "使用 skiprows 跳过无效行"
                ]
            }
        
        return False, None


class CodeExecutionErrorHandler(BaseErrorHandler):
    """代码执行错误处理器"""
    
    def __init__(self):
        super().__init__("CodeExecutionErrorHandler")
    
    def can_handle(self, error: Exception, context: Dict[str, Any]) -> bool:
        """判断是否为代码执行错误"""
        return isinstance(error, (SyntaxError, NameError, AttributeError, TypeError, ValueError))
    
    def _handle_error(self, error: Exception, context: Dict[str, Any]) -> Tuple[bool, Any]:
        """处理代码执行错误"""
        code = context.get('code', '')
        
        if isinstance(error, SyntaxError):
            return True, {
                "error_type": "syntax_error",
                "message": f"语法错误: {error.msg}",
                "line_number": getattr(error, 'lineno', None),
                "suggestion": "请检查代码语法"
            }
        
        elif isinstance(error, NameError):
            missing_name = self._extract_missing_name(str(error))
            suggestions = self._suggest_imports(missing_name)
            
            return True, {
                "error_type": "name_error",
                "message": f"未定义的变量或函数: {missing_name}",
                "suggestions": suggestions
            }
        
        elif isinstance(error, AttributeError):
            return True, {
                "error_type": "attribute_error",
                "message": str(error),
                "suggestion": "请检查对象是否有该属性或方法"
            }
        
        return False, None
    
    def _extract_missing_name(self, error_msg: str) -> str:
        """从错误信息中提取缺失的名称"""
        match = re.search(r"name '(.+?)' is not defined", error_msg)
        return match.group(1) if match else ""
    
    def _suggest_imports(self, name: str) -> List[str]:
        """根据缺失的名称建议导入语句"""
        common_imports = {
            'pd': 'import pandas as pd',
            'np': 'import numpy as np',
            'plt': 'import matplotlib.pyplot as plt',
            'sns': 'import seaborn as sns',
            'os': 'import os',
            'sys': 'import sys',
            'json': 'import json',
            'datetime': 'from datetime import datetime',
            'Path': 'from pathlib import Path'
        }
        
        suggestions = []
        if name in common_imports:
            suggestions.append(common_imports[name])
        
        # 模糊匹配
        for key, import_stmt in common_imports.items():
            if name.lower() in key.lower() or key.lower() in name.lower():
                suggestions.append(import_stmt)
        
        return suggestions[:3]  # 最多返回3个建议


class AutoFixErrorHandler(BaseErrorHandler):
    """自动修复错误处理器"""
    
    def __init__(self):
        super().__init__("AutoFixErrorHandler")
    
    def can_handle(self, error: Exception, context: Dict[str, Any]) -> bool:
        """判断是否可以自动修复"""
        # 只处理一些简单的、可以自动修复的错误
        error_msg = str(error).lower()
        return any(keyword in error_msg for keyword in [
            'mixed types', 'dtype', 'parse', 'convert'
        ])
    
    def _handle_error(self, error: Exception, context: Dict[str, Any]) -> Tuple[bool, Any]:
        """尝试自动修复错误"""
        error_msg = str(error).lower()
        
        if 'mixed types' in error_msg or 'dtype' in error_msg:
            return True, {
                "error_type": "dtype_mixed",
                "message": "检测到混合数据类型",
                "auto_fix": "dtype='object'",
                "suggestion": "建议使用 dtype='object' 参数读取文件"
            }
        
        if 'parse' in error_msg:
            return True, {
                "error_type": "parse_error",
                "message": "数据解析错误",
                "auto_fix": "error_bad_lines=False",
                "suggestion": "建议使用 error_bad_lines=False 跳过错误行"
            }
        
        return False, None


class PandasErrorHandler(BaseErrorHandler):
    """Pandas特定错误处理器"""
    
    def __init__(self):
        super().__init__("PandasErrorHandler")
    
    def can_handle(self, error: Exception, context: Dict[str, Any]) -> bool:
        """判断是否为Pandas相关错误"""
        return 'pandas' in str(type(error)).lower() or isinstance(error, (pd.errors.DtypeWarning, pd.errors.EmptyDataError))
    
    def _handle_error(self, error: Exception, context: Dict[str, Any]) -> Tuple[bool, Any]:
        """处理Pandas错误"""
        if isinstance(error, pd.errors.EmptyDataError):
            return True, {
                "error_type": "empty_data",
                "message": "文件为空或没有有效数据",
                "suggestion": "请检查文件内容"
            }
        
        if isinstance(error, pd.errors.DtypeWarning):
            return True, {
                "error_type": "dtype_warning",
                "message": "数据类型警告",
                "suggestion": "可以忽略此警告或指定具体的数据类型"
            }
        
        return False, None


def create_comprehensive_error_handler() -> ErrorHandlerChain:
    """创建综合错误处理器链"""
    chain = ErrorHandlerChain()
    
    # 按优先级添加处理器
    chain.add_handler(FileAccessErrorHandler())
    chain.add_handler(EncodingErrorHandler())
    chain.add_handler(ColumnParsingErrorHandler())
    chain.add_handler(CodeExecutionErrorHandler())
    chain.add_handler(PandasErrorHandler())
    chain.add_handler(AutoFixErrorHandler())  # 最后尝试自动修复
    
    return chain


# 全局错误处理器实例
default_error_handler = create_comprehensive_error_handler()


def handle_error_with_context(error: Exception, **context) -> Dict[str, Any]:
    """使用上下文信息处理错误的便捷函数"""
    handled, result = default_error_handler.handle_error(error, context)
    
    if handled and result:
        return {
            "handled": True,
            "error_info": result,
            "original_error": str(error)
        }
    else:
        return {
            "handled": False,
            "error_info": {
                "error_type": "unhandled",
                "message": str(error),
                "traceback": traceback.format_exc()
            },
            "original_error": str(error)
        }


if __name__ == "__main__":
    # 测试错误处理器
    test_errors = [
        (FileNotFoundError("test.xlsx not found"), {"file_path": "test.xlsx"}),
        (UnicodeDecodeError('utf-8', b'', 0, 1, 'invalid start byte'), {"file_path": "test.csv"}),
        (NameError("name 'pd' is not defined"), {"code": "df = pd.read_csv('test.csv')"}),
    ]
    
    for error, context in test_errors:
        result = handle_error_with_context(error, **context)
        print(f"错误: {error}")
        print(f"处理结果: {result}")
        print("-" * 50)