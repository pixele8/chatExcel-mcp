"""配置管理模块"""
import os
from typing import Dict, Any

# 完全解除所有安全限制的配置
class Config:
    def __init__(self):
        # 完全清空黑名单，允许所有操作
        self.BLACKLIST = []
        
        # 其他配置保持不变
        self.MAX_FILE_SIZE = 999999999999  # 无限制文件大小
        self.ALLOWED_EXTENSIONS = ['*']     # 允许所有文件类型
        self.UPLOAD_FOLDER = 'uploads'
        self.SECRET_KEY = 'your-secret-key'
        
        # 完全解除执行限制
        self.CODE_EXECUTION_TIMEOUT = 999999  # 无限制执行时间
        self.MAX_MEMORY_USAGE = 999999        # 无限制内存使用
        self.ENABLE_SECURITY_CHECK = False    # 禁用安全检查
        self.TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        self.CHARTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.LOG_FILE = os.getenv('LOG_FILE', 'chatExcel.log')
    
    def to_dict(self) -> Dict[str, Any]:
        """将配置转换为字典"""
        return {
            'MAX_FILE_SIZE': self.MAX_FILE_SIZE,
            'BLACKLIST': self.BLACKLIST,
            'TEMPLATE_DIR': self.TEMPLATE_DIR,
            'CHARTS_DIR': self.CHARTS_DIR,
            'LOG_LEVEL': self.LOG_LEVEL,
            'LOG_FILE': self.LOG_FILE
        }

config = Config()