
# 标准化错误处理机制
import traceback
import logging
from typing import Dict, Any, Optional
from datetime import datetime

class StandardErrorHandler:
    """标准化错误处理器"""
    
    def __init__(self, logger_name: str = 'mcp_tools'):
        self.logger = logging.getLogger(logger_name)
    
    def handle_error(self, error: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """标准化错误处理"""
        error_info = {
            'success': False,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'timestamp': datetime.now().isoformat(),
            'traceback': traceback.format_exc()
        }
        
        if context:
            error_info['context'] = context
            
        # 记录错误
        self.logger.error(f"错误处理: {error_info['error_type']} - {error_info['error_message']}")
        
        # 根据错误类型提供建议
        error_info['suggestion'] = self._get_error_suggestion(error)
        
        return error_info
    
    def _get_error_suggestion(self, error: Exception) -> str:
        """根据错误类型提供建议"""
        suggestions = {
            'FileNotFoundError': '请检查文件路径是否正确',
            'PermissionError': '请检查文件权限设置',
            'UnicodeDecodeError': '请检查文件编码格式',
            'ValueError': '请检查输入参数的格式和范围',
            'TypeError': '请检查参数类型是否正确',
            'KeyError': '请检查字典键是否存在',
            'IndexError': '请检查列表索引是否越界',
            'ImportError': '请检查模块是否已安装',
            'SyntaxError': '请检查代码语法是否正确'
        }
        
        error_type = type(error).__name__
        return suggestions.get(error_type, '请检查错误信息并重试')
    
    def create_success_response(self, data: Any, message: str = '操作成功') -> Dict[str, Any]:
        """创建成功响应"""
        return {
            'success': True,
            'data': data,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
