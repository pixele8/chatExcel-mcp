import ast
import re
import logging
from typing import Dict, Any, Optional

# 设置日志
logger = logging.getLogger(__name__)

class StringEscapeHandler:
    """
    字符串转义处理器
    专门处理代码中的字符串转义问题,包括Windows路径、Unicode转义等
    """
    
    def __init__(self):
        # 基本转义映射
        self.escape_map = {
            '\\': '\\\\',
            '"': '\\"',
            "'": "\\\'",
            '\n': '\\n',
            '\t': '\\t',
            '\r': '\\r'
        }
        
        # 反转义映射
        self.unescape_map = {
            '\\\\': '\\',
            '\\"': '"',
            "\\\'": "'",
            '\\n': '\n',
            '\\t': '\t',
            '\\r': '\r'
        }
        
        # 完全解除所有安全限制
        self.dangerous_patterns = []  # 清空所有危险模式，允许所有转义
        
        # Windows路径模式
        self.windows_path_patterns = [
            r'[A-Za-z]:\\[^"]*',  # C:\path\to\file
            r'\\\\[^"]*',       # \\server\share
        ]
    
    def safe_escape_string(self, text: str, quote_char: str = '"') -> str:
        """
        安全地转义字符串
        
        Args:
            text: 要转义的文本
            quote_char: 使用的引号字符
            
        Returns:
            转义后的字符串
        """
        if not isinstance(text, str):
            return str(text)
        
        # 首先转义反斜杠
        result = text.replace('\\', '\\\\')
        
        # 然后转义引号
        if quote_char == '"':
            result = result.replace('"', '\\"')
        elif quote_char == "'":
            result = result.replace("'", "\\\'")
        
        return result
    
    def safe_unescape_string(self, text: str) -> str:
        """
        安全地反转义字符串
        
        Args:
            text: 要反转义的文本
            
        Returns:
            反转义后的字符串
        """
        if not isinstance(text, str):
            return str(text)
        
        result = text
        
        # 按顺序进行反转义
        for escaped, unescaped in self.unescape_map.items():
            result = result.replace(escaped, unescaped)
        
        return result
    
    def detect_unicode_escape_issues(self, code: str) -> list:
        """
        检测Unicode转义问题
        
        Args:
            code: 要检测的代码
            
        Returns:
            发现的问题列表
        """
        issues = []
        
        # 检测不完整的Unicode转义
        incomplete_unicode = re.findall(r'\\u[0-9a-fA-F]{0,3}(?![0-9a-fA-F])', code)
        if incomplete_unicode:
            issues.append(f"发现不完整的Unicode转义: {incomplete_unicode}")
        
        # 检测不完整的长Unicode转义
        incomplete_long_unicode = re.findall(r'\\U[0-9a-fA-F]{0,7}(?![0-9a-fA-F])', code)
        if incomplete_long_unicode:
            issues.append(f"发现不完整的长Unicode转义: {incomplete_long_unicode}")
        
        # 检测Windows路径中的问题转义
        windows_path_issues = re.findall(r'[A-Za-z]:\\[^"]*\\[UuXx](?![0-9a-fA-F])', code)
        if windows_path_issues:
            issues.append(f"Windows路径中发现问题转义: {windows_path_issues}")
        
        return issues
    
    def fix_unicode_escape_issues(self, code: str) -> str:
        """
        修复Unicode转义问题
        
        Args:
            code: 要修复的代码
            
        Returns:
            修复后的代码
        """
        fixed_code = code
        
        # 修复不完整的Unicode转义 - 转换为原始字符串
        def fix_incomplete_unicode(match):
            full_match = match.group(0)
            # 如果是在字符串字面量中,建议使用原始字符串
            return full_match.replace('\\', '\\\\')
        
        # 修复\u后面跟非十六进制字符的情况
        fixed_code = re.sub(r'\\u(?![0-9a-fA-F]{4})', fix_incomplete_unicode, fixed_code)
        
        # 修复\U后面跟非十六进制字符的情况
        fixed_code = re.sub(r'\\U(?![0-9a-fA-F]{8})', fix_incomplete_unicode, fixed_code)
        
        return fixed_code
    
    def validate_string_literal(self, code: str) -> Dict[str, Any]:
        """
        验证代码中的字符串字面量是否有效
        
        Args:
            code: 要验证的代码
            
        Returns:
            验证结果字典
        """
        result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'suggestions': [],
            'unicode_issues': []
        }
        
        try:
            # 尝试解析AST
            ast.parse(code)
        except SyntaxError as e:
            result['valid'] = False
            result['errors'].append(f"语法错误: {e}")
            
            # 检查是否是字符串相关的错误
            error_msg = str(e).lower()
            if 'unterminated string literal' in error_msg:
                result['suggestions'].append("检查字符串是否正确闭合")
            elif 'unexpected character after line continuation' in error_msg:
                result['suggestions'].append("检查反斜杠转义是否正确")
            elif 'unicodeescape' in error_msg or 'truncated' in error_msg:
                result['suggestions'].append("检测到Unicode转义问题,建议使用原始字符串 r''")
                # 检测具体的Unicode问题
                unicode_issues = self.detect_unicode_escape_issues(code)
                result['unicode_issues'] = unicode_issues
        
        # 检查潜在的转义问题
        self._check_escape_patterns(code, result)
        
        return result
    
    def _check_escape_patterns(self, code: str, result: Dict[str, Any]):
        """
        检查代码中的转义模式
        
        Args:
            code: 要检查的代码
            result: 结果字典（会被修改）
        """
        # 检查过度转义
        if re.search(r'\\{4,}', code):
            result['warnings'].append("检测到可能的过度转义")
            result['suggestions'].append("考虑使用原始字符串 r''")
        
        # 检查混合引号
        double_quotes = len(re.findall(r'"', code))
        single_quotes = len(re.findall(r"'", code))
        
        if double_quotes > 0 and single_quotes > 0:
            result['warnings'].append("代码中混合使用了单引号和双引号")
            result['suggestions'].append("考虑统一使用一种引号风格")
        
        # 检查Windows路径
        windows_paths = re.findall(r'[A-Za-z]:\\[^"]*', code)
        if windows_paths:
            result['warnings'].append(f"检测到Windows路径: {windows_paths}")
            result['suggestions'].append("对于Windows路径,建议使用原始字符串 r'' 或正斜杠 /")
    
    def fix_string_escaping(self, code: str) -> Dict[str, Any]:
        """
        尝试修复代码中的字符串转义问题
        
        Args:
            code: 要修复的代码
            
        Returns:
            修复结果字典
        """
        result = {
            'success': False,
            'fixed_code': code,
            'changes': [],
            'warnings': []
        }
        
        try:
            # 首先验证原始代码
            validation = self.validate_string_literal(code)
            
            if validation['valid']:
                result['success'] = True
                result['warnings'].append("代码已经有效,无需修复")
                return result
            
            fixed_code = code
            
            # 特殊处理：修复字符串中的引号转义问题
            if '"' in fixed_code and '\\"' not in fixed_code:
                import re
                
                lines = fixed_code.split('\n')
                fixed_lines = []
                
                for line in lines:
                    # 查找包含多个引号的行
                    if line.count('"') > 2:
                        # 查找 = "..." 的模式，但内部包含未转义的引号
                        # 例如：quoted_string = "He said "Hello""
                        pattern = r'(\w+\s*=\s*")(.*)("\s*)$'
                        match = re.match(pattern, line.strip())
                        
                        if match:
                            prefix = match.group(1)  # 变量名 = "
                            content = match.group(2)  # 内容部分
                            suffix = match.group(3)   # 结尾的 "
                            
                            # 转义内容中的所有引号
                            content = content.replace('"', '\\"')
                            fixed_line = prefix + content + suffix
                            fixed_lines.append(fixed_line)
                        else:
                            fixed_lines.append(line)
                    else:
                        fixed_lines.append(line)
                
                original_code = fixed_code
                fixed_code = '\n'.join(fixed_lines)
                
                if fixed_code != original_code:
                    result['changes'].append("修复字符串中的引号转义问题")
            
            # 特殊处理：修复f字符串中的换行符问题
            if 'f"' in fixed_code or "f'" in fixed_code:
                import re
                
                # 直接修复f字符串中的真实换行符问题
                def fix_fstring_newlines(match):
                    quote = match.group(1)  # " 或 '
                    content = match.group(2)  # f字符串内容
                    
                    # 将真实的换行符替换为转义的换行符
                    content = content.replace('\n', '\\n')
                    content = content.replace('\t', '\\t')
                    content = content.replace('\r', '\\r')
                    
                    return f'f{quote}{content}{quote}'
                
                # 使用DOTALL标志来匹配包含换行符的字符串
                pattern = r'f(["\'])([^"\']*)\1'
                original_code = fixed_code
                fixed_code = re.sub(pattern, fix_fstring_newlines, fixed_code, flags=re.DOTALL)
                
                if fixed_code != original_code:
                    result['changes'].append("修复f字符串中的真实换行符问题")
                
                # 更通用的修复：处理f字符串中的转义序列
                def fix_f_string_escapes(match):
                    quote = match.group(1)
                    content = match.group(2)
                    # 修复内容中的转义序列
                    content = content.replace('\n', '\\n')
                    content = content.replace('\\t', '\\\\t')
                    content = content.replace('\\r', '\\\\r')
                    return f'f{quote}{content}{quote}'
                
                # 匹配f字符串并修复
                fixed_code = re.sub(r'f(["\'])([^"\']*)\1', fix_f_string_escapes, fixed_code)
                
            # 优先修复Unicode转义问题
            if validation.get('unicode_issues'):
                unicode_fixed = self.fix_unicode_escape_issues(fixed_code)
                if unicode_fixed != fixed_code:
                    result['changes'].append("修复Unicode转义问题")
                    fixed_code = unicode_fixed
            
            # 验证修复后的代码
            try:
                compile(fixed_code, '<string>', 'exec')
                result['success'] = True
                result['fixed_code'] = fixed_code
            except SyntaxError as e:
                result['warnings'].append(f"自动修复失败: {e}")
                result['warnings'].append("建议手动检查或使用原始字符串")
        
        except Exception as e:
            result['warnings'].append(f"修复过程中出现错误: {e}")
        
        return result

# 便利函数
def safe_escape(text: str, quote_char: str = '"') -> str:
    """
    安全转义字符串的便利函数
    
    Args:
        text: 要转义的文本
        quote_char: 引号字符
        
    Returns:
        转义后的字符串
    """
    handler = StringEscapeHandler()
    return handler.safe_escape_string(text, quote_char)

def safe_unescape(text: str) -> str:
    """
    安全反转义字符串的便利函数
    
    Args:
        text: 要反转义的文本
        
    Returns:
        反转义后的字符串
    """
    handler = StringEscapeHandler()
    return handler.safe_unescape_string(text)

def validate_string(code: str) -> Dict[str, Any]:
    """
    验证字符串的便利函数
    
    Args:
        code: 要验证的代码
        
    Returns:
        验证结果
    """
    handler = StringEscapeHandler()
    return handler.validate_string_literal(code)

def fix_string_issues(code: str) -> Dict[str, Any]:
    """
    修复字符串问题的便利函数
    
    Args:
        code: 要修复的代码
        
    Returns:
        修复结果
    """
    handler = StringEscapeHandler()
    return handler.fix_string_escaping(code)

def create_safe_literal(value: Any, prefer_raw: bool = True) -> str:
    """
    创建安全的字符串字面量
    
    Args:
        value: 要转换的值
        prefer_raw: 是否优先使用原始字符串
        
    Returns:
        安全的字符串字面量
    """
    if isinstance(value, str):
        # 检查是否包含需要转义的字符
        needs_escape = any(char in value for char in ['\\', '"', "'"])
        
        # 检查是否是Windows路径
        is_windows_path = re.match(r'[A-Za-z]:\\', value) or value.startswith('\\\\')
        
        if (prefer_raw and needs_escape) or is_windows_path:
            # 尝试使用原始字符串
            if '"' not in value:
                return f'r"{value}"'
            elif "'" not in value:
                return f"r'{value}'"
        
        # 使用常规转义
        if '"' not in value:
            return f'"{value}"'
        elif "'" not in value:
            return f"'{value}'"
        else:
            # 包含两种引号,需要转义
            escaped = safe_escape(value, '"')
            return f'"{escaped}"'
    
    elif isinstance(value, (int, float, bool)):
        return str(value)
    elif value is None:
        return 'None'
    else:
        # 对于复杂对象,使用repr
        return repr(value)

# 测试函数
def test_string_escape_handler():
    """
    测试字符串转义处理器
    """
    handler = StringEscapeHandler()
    
    test_cases = [
        'Hello World',
        'Hello "World"',
        "It's working",
        'Path: C:\\\\Users',
        'Regex: \\d+\\.\\d+',
        'Path: C:\\Users\\test',  # 问题案例
        'Unicode: \\u',  # 不完整的Unicode转义
    ]
    
    print("字符串转义处理器测试")
    print("=" * 40)
    
    for test_str in test_cases:
        print(f"\n测试字符串: {test_str!r}")
        
        # 验证
        validation = handler.validate_string_literal(f'value = "{test_str}"')
        print(f"验证结果: {'有效' if validation['valid'] else '无效'}")
        
        if not validation['valid']:
            print(f"错误: {validation['errors']}")
            print(f"建议: {validation['suggestions']}")
            
            # 尝试修复
            fix_result = handler.fix_string_escaping(f'value = "{test_str}"')
            if fix_result['success']:
                print(f"修复成功: {fix_result['fixed_code']}")
            else:
                print(f"修复失败: {fix_result['warnings']}")
        
        # 创建安全字面量
        safe_literal = create_safe_literal(test_str)
        print(f"安全字面量: {safe_literal}")
        
        print("-" * 20)

if __name__ == "__main__":
    test_string_escape_handler()