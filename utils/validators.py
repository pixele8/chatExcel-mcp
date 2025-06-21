"""Parameter Validation Module.

Provides intelligent parameter validation with suggestions
and automatic corrections for Excel processing operations.
"""

import os
import re
from typing import Dict, Any, Optional, List, Union, Tuple
from dataclasses import dataclass
from pathlib import Path

try:
    from core.exceptions import ValidationError
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    # 如果core不可用，创建简单的ValidationError类
    class ValidationError(Exception):
        def __init__(self, field_name: str, error_details: str):
            super().__init__(f"Validation error for {field_name}: {error_details}")


@dataclass
class ValidationResult:
    """Result of parameter validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    corrected_params: Dict[str, Any]


class ParameterValidator:
    """Intelligent parameter validator for Excel operations."""
    
    def __init__(self):
        """Initialize parameter validator."""
        self.supported_formats = {'.xlsx', '.xls', '.csv', '.json', '.html', '.xml'}
        self.encoding_options = ['utf-8', 'gbk', 'gb2312', 'latin1', 'ascii']
        self.separator_options = [',', ';', '\t', '|', ' ']
    
    def validate_file_path(self, file_path: str) -> ValidationResult:
        """Validate file path parameter.
        
        Args:
            file_path: File path to validate
            
        Returns:
            ValidationResult with validation details
        """
        errors = []
        warnings = []
        suggestions = []
        corrected_params = {}
        
        if not file_path:
            errors.append("文件路径不能为空")
            return ValidationResult(False, errors, warnings, suggestions, corrected_params)
        
        # Convert to Path object for easier handling
        try:
            path = Path(file_path)
            corrected_params['file_path'] = str(path.absolute())
        except Exception as e:
            errors.append(f"无效的文件路径格式: {e}")
            return ValidationResult(False, errors, warnings, suggestions, corrected_params)
        
        # Check if file exists
        if not path.exists():
            errors.append(f"文件不存在: {file_path}")
            
            # Suggest similar files in the same directory
            if path.parent.exists():
                similar_files = self._find_similar_files(path)
                if similar_files:
                    suggestions.append(f"您是否想要打开以下文件之一: {', '.join(similar_files)}")
        
        # Check file extension
        file_ext = path.suffix.lower()
        if file_ext not in self.supported_formats:
            if file_ext:
                errors.append(f"不支持的文件格式: {file_ext}")
                suggestions.append(f"支持的格式: {', '.join(sorted(self.supported_formats))}")
            else:
                warnings.append("文件没有扩展名，可能导致格式检测问题")
                suggestions.append("建议为文件添加适当的扩展名")
        
        # Check file size
        if path.exists():
            file_size = path.stat().st_size
            if file_size == 0:
                warnings.append("文件为空")
            elif file_size > 100 * 1024 * 1024:  # 100MB
                warnings.append(f"文件较大 ({file_size / (1024*1024):.1f}MB)，处理可能较慢")
                suggestions.append("考虑使用分块读取或指定列范围")
        
        # Check file permissions
        if path.exists() and not os.access(path, os.R_OK):
            errors.append("没有文件读取权限")
            suggestions.append("检查文件权限设置")
        
        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors, warnings, suggestions, corrected_params)
    
    def validate_sheet_name(self, sheet_name: Union[str, int], 
                           available_sheets: Optional[List[str]] = None) -> ValidationResult:
        """Validate sheet name parameter.
        
        Args:
            sheet_name: Sheet name or index to validate
            available_sheets: List of available sheet names
            
        Returns:
            ValidationResult with validation details
        """
        errors = []
        warnings = []
        suggestions = []
        corrected_params = {}
        
        if sheet_name is None:
            corrected_params['sheet_name'] = 0
            suggestions.append("使用默认工作表 (第一个)")
        elif isinstance(sheet_name, int):
            if available_sheets and (sheet_name < 0 or sheet_name >= len(available_sheets)):
                errors.append(f"工作表索引 {sheet_name} 超出范围 (0-{len(available_sheets)-1})")
                if available_sheets:
                    suggestions.append(f"可用工作表: {', '.join(available_sheets)}")
            else:
                corrected_params['sheet_name'] = sheet_name
        elif isinstance(sheet_name, str):
            if available_sheets and sheet_name not in available_sheets:
                errors.append(f"工作表 '{sheet_name}' 不存在")
                # Find similar sheet names
                similar_sheets = self._find_similar_strings(sheet_name, available_sheets)
                if similar_sheets:
                    suggestions.append(f"您是否想要: {', '.join(similar_sheets)}")
                else:
                    suggestions.append(f"可用工作表: {', '.join(available_sheets)}")
            else:
                corrected_params['sheet_name'] = sheet_name
        else:
            errors.append(f"无效的工作表名称类型: {type(sheet_name)}")
            suggestions.append("工作表名称应为字符串或整数索引")
        
        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors, warnings, suggestions, corrected_params)
    
    def validate_encoding(self, encoding: Optional[str], 
                         file_path: Optional[str] = None) -> ValidationResult:
        """Validate encoding parameter.
        
        Args:
            encoding: Encoding to validate
            file_path: File path for auto-detection
            
        Returns:
            ValidationResult with validation details
        """
        errors = []
        warnings = []
        suggestions = []
        corrected_params = {}
        
        if encoding is None:
            # Try to auto-detect encoding
            if file_path and os.path.exists(file_path):
                detected_encoding = self._detect_file_encoding(file_path)
                corrected_params['encoding'] = detected_encoding
                suggestions.append(f"自动检测到编码: {detected_encoding}")
            else:
                corrected_params['encoding'] = 'utf-8'
                suggestions.append("使用默认编码: utf-8")
        elif encoding.lower() not in [enc.lower() for enc in self.encoding_options]:
            warnings.append(f"不常见的编码: {encoding}")
            suggestions.append(f"常用编码: {', '.join(self.encoding_options)}")
            corrected_params['encoding'] = encoding
        else:
            corrected_params['encoding'] = encoding
        
        # Test encoding if file exists
        if file_path and os.path.exists(file_path) and 'encoding' in corrected_params:
            try:
                with open(file_path, 'r', encoding=corrected_params['encoding']) as f:
                    f.read(1000)  # Test read first 1000 characters
            except UnicodeDecodeError:
                errors.append(f"编码 {corrected_params['encoding']} 无法解码文件")
                # Try alternative encodings
                for alt_encoding in self.encoding_options:
                    try:
                        with open(file_path, 'r', encoding=alt_encoding) as f:
                            f.read(1000)
                        suggestions.append(f"建议使用编码: {alt_encoding}")
                        break
                    except UnicodeDecodeError:
                        continue
        
        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors, warnings, suggestions, corrected_params)
    
    def validate_separator(self, separator: Optional[str], 
                          file_path: Optional[str] = None) -> ValidationResult:
        """Validate CSV separator parameter.
        
        Args:
            separator: Separator to validate
            file_path: File path for auto-detection
            
        Returns:
            ValidationResult with validation details
        """
        errors = []
        warnings = []
        suggestions = []
        corrected_params = {}
        
        if separator is None:
            # Try to auto-detect separator
            if file_path and os.path.exists(file_path) and file_path.lower().endswith('.csv'):
                detected_sep = self._detect_csv_separator(file_path)
                corrected_params['separator'] = detected_sep
                suggestions.append(f"自动检测到分隔符: '{detected_sep}'")
            else:
                corrected_params['separator'] = ','
                suggestions.append("使用默认分隔符: ','")
        elif len(separator) != 1:
            errors.append("分隔符必须是单个字符")
            suggestions.append(f"常用分隔符: {', '.join(repr(s) for s in self.separator_options)}")
        else:
            corrected_params['separator'] = separator
            if separator not in self.separator_options:
                warnings.append(f"不常见的分隔符: '{separator}'")
        
        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors, warnings, suggestions, corrected_params)
    
    def validate_column_specification(self, columns: Union[str, List[str], None], 
                                    available_columns: Optional[List[str]] = None) -> ValidationResult:
        """Validate column specification.
        
        Args:
            columns: Column specification to validate
            available_columns: List of available column names
            
        Returns:
            ValidationResult with validation details
        """
        errors = []
        warnings = []
        suggestions = []
        corrected_params = {}
        
        if columns is None:
            suggestions.append("将使用所有列")
            return ValidationResult(True, errors, warnings, suggestions, corrected_params)
        
        # Convert to list if string
        if isinstance(columns, str):
            if ',' in columns:
                column_list = [col.strip() for col in columns.split(',')]
            else:
                column_list = [columns.strip()]
        elif isinstance(columns, list):
            column_list = columns
        else:
            errors.append(f"无效的列规格类型: {type(columns)}")
            return ValidationResult(False, errors, warnings, suggestions, corrected_params)
        
        corrected_params['columns'] = column_list
        
        # Validate against available columns
        if available_columns:
            missing_columns = [col for col in column_list if col not in available_columns]
            if missing_columns:
                errors.append(f"列不存在: {', '.join(missing_columns)}")
                
                # Suggest similar column names
                for missing_col in missing_columns:
                    similar_cols = self._find_similar_strings(missing_col, available_columns)
                    if similar_cols:
                        suggestions.append(f"'{missing_col}' 的相似列: {', '.join(similar_cols)}")
                
                suggestions.append(f"可用列: {', '.join(available_columns)}")
        
        # Check for duplicates
        if len(column_list) != len(set(column_list)):
            warnings.append("列规格中有重复项")
            corrected_params['columns'] = list(set(column_list))
        
        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors, warnings, suggestions, corrected_params)
    
    def validate_numeric_range(self, value: Union[int, str, None], 
                              param_name: str, min_val: int = 0, 
                              max_val: Optional[int] = None) -> ValidationResult:
        """Validate numeric range parameters.
        
        Args:
            value: Value to validate
            param_name: Parameter name for error messages
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            
        Returns:
            ValidationResult with validation details
        """
        errors = []
        warnings = []
        suggestions = []
        corrected_params = {}
        
        if value is None:
            return ValidationResult(True, errors, warnings, suggestions, corrected_params)
        
        # Convert to int if string
        try:
            if isinstance(value, str):
                int_value = int(value)
            else:
                int_value = int(value)
        except (ValueError, TypeError):
            errors.append(f"{param_name} 必须是整数")
            return ValidationResult(False, errors, warnings, suggestions, corrected_params)
        
        # Check range
        if int_value < min_val:
            errors.append(f"{param_name} 不能小于 {min_val}")
            corrected_params[param_name.lower()] = min_val
            suggestions.append(f"已调整为最小值: {min_val}")
        elif max_val is not None and int_value > max_val:
            errors.append(f"{param_name} 不能大于 {max_val}")
            corrected_params[param_name.lower()] = max_val
            suggestions.append(f"已调整为最大值: {max_val}")
        else:
            corrected_params[param_name.lower()] = int_value
        
        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors, warnings, suggestions, corrected_params)
    
    def validate_code_safety(self, code: str) -> ValidationResult:
        """Validate code for basic safety.
        
        Args:
            code: Python code to validate
            
        Returns:
            ValidationResult with validation details
        """
        errors = []
        warnings = []
        suggestions = []
        corrected_params = {}
        
        if not code or not code.strip():
            errors.append("代码不能为空")
            return ValidationResult(False, errors, warnings, suggestions, corrected_params)
        
        # Check for dangerous patterns
        dangerous_patterns = [
            (r'\b(import|from)\s+os\b', "导入 os 模块可能不安全"),
            (r'\b(import|from)\s+subprocess\b', "导入 subprocess 模块可能不安全"),
            (r'\beval\s*\(', "使用 eval() 函数可能不安全"),
            (r'\bexec\s*\(', "使用 exec() 函数可能不安全"),
            (r'\b__import__\s*\(', "使用 __import__() 函数可能不安全"),
            (r'\bopen\s*\(', "直接使用 open() 函数，建议使用提供的文件操作工具"),
        ]
        
        for pattern, message in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                warnings.append(message)
        
        # Check for common issues
        if 'pandas' not in code and 'pd' not in code:
            suggestions.append("代码中没有使用 pandas，确认这是预期的吗？")
        
        if code.count('(') != code.count(')'):
            errors.append("括号不匹配")
        
        if code.count('[') != code.count(']'):
            errors.append("方括号不匹配")
        
        if code.count('{') != code.count('}'):
            errors.append("花括号不匹配")
        
        # Check for basic syntax
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            errors.append(f"语法错误: {e}")
        
        corrected_params['code'] = code.strip()
        
        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors, warnings, suggestions, corrected_params)
    
    def _find_similar_files(self, target_path: Path) -> List[str]:
        """Find similar files in the same directory."""
        if not target_path.parent.exists():
            return []
        
        target_name = target_path.name.lower()
        similar_files = []
        
        try:
            for file_path in target_path.parent.iterdir():
                if file_path.is_file():
                    file_name = file_path.name.lower()
                    # Simple similarity check
                    if (target_name in file_name or file_name in target_name or
                        self._calculate_similarity(target_name, file_name) > 0.6):
                        similar_files.append(file_path.name)
        except PermissionError:
            pass
        
        return similar_files[:5]  # Return top 5 matches
    
    def _find_similar_strings(self, target: str, candidates: List[str]) -> List[str]:
        """Find similar strings from candidates."""
        target_lower = target.lower()
        similar = []
        
        for candidate in candidates:
            candidate_lower = candidate.lower()
            similarity = self._calculate_similarity(target_lower, candidate_lower)
            if similarity > 0.6:  # 60% similarity threshold
                similar.append(candidate)
        
        return similar[:3]  # Return top 3 matches
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate string similarity using simple algorithm."""
        if not str1 or not str2:
            return 0.0
        
        # Simple Jaccard similarity
        set1 = set(str1.lower())
        set2 = set(str2.lower())
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    def _detect_file_encoding(self, file_path: str) -> str:
        """Detect file encoding."""
        try:
            import chardet
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)
                result = chardet.detect(raw_data)
                return result.get('encoding', 'utf-8')
        except ImportError:
            # Fallback method
            for encoding in self.encoding_options:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        f.read(1000)
                    return encoding
                except UnicodeDecodeError:
                    continue
            return 'utf-8'
    
    def _detect_csv_separator(self, file_path: str) -> str:
        """Detect CSV separator."""
        try:
            import csv
            with open(file_path, 'r', encoding='utf-8') as f:
                sample = f.read(1024)
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                return delimiter
        except:
            # Fallback method
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    first_line = f.readline()
                    for sep in self.separator_options:
                        if sep in first_line:
                            return sep
            except:
                pass
            return ','