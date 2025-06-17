"""配置管理模块"""
import os
from typing import Dict, Any

class Config:
    """应用配置类"""
    
    def __init__(self):
        self.MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 200 * 1024 * 1024))  # 200MB
        self.BLACKLIST = [
            'subprocess.', '__import__'
        ]
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