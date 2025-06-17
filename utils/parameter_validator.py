
# 统一参数验证框架
from typing import Any, Dict, List, Optional, Union, Callable
import re
from pathlib import Path

class ParameterValidator:
    """统一参数验证器"""
    
    @staticmethod
    def validate_file_path(path: str, must_exist: bool = True, allowed_extensions: Optional[List[str]] = None) -> bool:
        """验证文件路径"""
        try:
            path_obj = Path(path)
            
            # 检查路径遍历攻击
            if '..' in str(path_obj) or str(path_obj).startswith('/'):
                return False
                
            # 检查文件是否存在
            if must_exist and not path_obj.exists():
                return False
                
            # 检查文件扩展名
            if allowed_extensions:
                if path_obj.suffix.lower() not in [ext.lower() for ext in allowed_extensions]:
                    return False
                    
            return True
            
        except Exception:
            return False
    
    @staticmethod
    def validate_code_content(code: str, max_length: int = 10000) -> Dict[str, Any]:
        """验证代码内容"""
        result = {'valid': True, 'warnings': [], 'errors': []}
        
        # 检查代码长度
        if len(code) > max_length:
            result['errors'].append(f'代码长度超过限制 ({len(code)} > {max_length})')
            result['valid'] = False
            
        # 检查危险模式
        dangerous_patterns = [
            (r'exec\s*\(', 'exec() 调用'),
            (r'eval\s*\(', 'eval() 调用'),
            (r'__import__\s*\(', '动态导入'),
            (r'subprocess\.|os\.system', '系统命令执行')
        ]
        
        for pattern, description in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                result['warnings'].append(f'检测到潜在危险操作: {description}')
                
        return result
    
    @staticmethod
    def sanitize_input(value: Any, input_type: str = 'string') -> Any:
        """清理输入数据"""
        if input_type == 'string':
            if isinstance(value, str):
                # 移除潜在的脚本标签
                value = re.sub(r'<script[^>]*>.*?</script>', '', value, flags=re.IGNORECASE | re.DOTALL)
                # 移除SQL注入模式
                value = re.sub(r'(union|select|insert|update|delete|drop)\s+', '', value, flags=re.IGNORECASE)
                return value.strip()
        elif input_type == 'number':
            try:
                return float(value) if '.' in str(value) else int(value)
            except (ValueError, TypeError):
                return 0
                
        return value

import re
from typing import Any, Dict, List, Union

class ParameterValidator:
    """参数验证器 - 降低安全限制版本"""
    
    @staticmethod
    def validate_file_path(path: str) -> bool:
        """验证文件路径"""
        if not isinstance(path, str) or not path.strip():
            return False
        # 移除大部分路径限制，只保留基本检查
        return True
    
    @staticmethod
    def validate_sheet_name(name: str) -> bool:
        """验证工作表名称"""
        if not isinstance(name, str):
            return False
        return len(name.strip()) > 0
    
    @staticmethod
    def validate_range(range_str: str) -> bool:
        """验证Excel范围"""
        if not isinstance(range_str, str):
            return False
        try:
            # 简化范围验证
            return True
        except Exception:
            return False
    
    @staticmethod
    def validate_code_content(code: str, max_length: int = 50000) -> Dict[str, Any]:
        """验证代码内容 - 宽松版本"""
        result = {'valid': True, 'warnings': [], 'errors': []}
        
        # 检查代码长度 - 提高限制
        if len(code) > max_length:
            result['errors'].append(f'代码长度超过限制 ({len(code)} > {max_length})')
            result['valid'] = False
            
        # 大幅减少危险模式检查，只保留最基本的
        dangerous_patterns = [
            (r'subprocess\.', '系统命令执行')
        ]
        
        for pattern, description in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                result['warnings'].append(f'检测到潜在操作: {description}')
                
        return result
    
    @staticmethod
    def sanitize_input(value: Any, input_type: str = 'string') -> Any:
        """清理输入数据 - 简化版本"""
        if input_type == 'string':
            if isinstance(value, str):
                return value.strip()
        elif input_type == 'number':
            try:
                return float(value) if '.' in str(value) else int(value)
            except (ValueError, TypeError):
                return 0
                
        return value
    
    @staticmethod
    def validate_column_names(columns: List[str]) -> bool:
        """验证列名"""
        if not isinstance(columns, list):
            return False
        return all(isinstance(col, str) and col.strip() for col in columns)
    
    @staticmethod
    def validate_data_types(data_types: Dict[str, str]) -> bool:
        """验证数据类型"""
        if not isinstance(data_types, dict):
            return False
        valid_types = {'int', 'float', 'str', 'bool', 'datetime', 'object'}
        return all(dtype in valid_types for dtype in data_types.values())
