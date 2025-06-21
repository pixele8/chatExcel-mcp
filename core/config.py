#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一配置管理模块
提供安全、性能、日志和监控的配置管理
"""

import os
import json
import yaml
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict
from pathlib import Path
import logging

# 配置日志
logger = logging.getLogger(__name__)

@dataclass
class SecurityConfig:
    """安全配置"""
    # 文件安全
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    allowed_file_types: List[str] = field(default_factory=lambda: ['xlsx', 'xls', 'csv', 'json'])
    upload_path_whitelist: List[str] = field(default_factory=lambda: ['/tmp', '/Users/wangdada/Downloads'])
    
    # 代码执行安全
    code_execution_enabled: bool = True
    code_execution_timeout: int = 30  # 30秒
    code_execution_memory_limit: int = 512 * 1024 * 1024  # 512MB
    blacklisted_modules: List[str] = field(default_factory=lambda: ['subprocess', 'os.system', 'eval', 'exec'])
    
    # API安全
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # 60秒
    
    # 审计日志
    audit_log_enabled: bool = True
    audit_log_path: str = "logs/audit.log"
    log_sensitive_data: bool = False

@dataclass
class PerformanceConfig:
    """性能配置"""
    # 缓存配置
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 1小时
    cache_max_size: int = 1000
    cache_directory: str = ".excel_analysis_cache"
    
    # 并发配置
    max_concurrent_requests: int = 10
    worker_threads: int = 4
    
    # 内存配置
    max_memory_usage: int = 1024 * 1024 * 1024  # 1GB
    gc_threshold: int = 100
    
    # 文件处理
    chunk_size: int = 10000  # 分块处理大文件
    streaming_threshold: int = 50 * 1024 * 1024  # 50MB启用流式处理

@dataclass
class LoggingConfig:
    """日志配置"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: str = "logs/chatexcel.log"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    console_output: bool = True
    
@dataclass
class MonitoringConfig:
    """监控配置"""
    health_check_enabled: bool = True
    health_check_interval: int = 30  # 30秒
    metrics_enabled: bool = True
    metrics_endpoint: str = "/metrics"
    alert_enabled: bool = True
    alert_thresholds: Dict[str, float] = field(default_factory=lambda: {
        "cpu_usage": 80.0,
        "memory_usage": 85.0,
        "error_rate": 5.0
    })

@dataclass
class Config:
    """主配置类"""
    security: SecurityConfig = field(default_factory=SecurityConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)
    
    # 基础配置
    version: str = "2.1.0"
    debug: bool = False
    template_dir: str = "templates"
    charts_dir: str = "charts"
    
    @classmethod
    def from_env(cls) -> 'Config':
        """从环境变量加载配置"""
        config = cls()
        
        # 安全配置
        if os.getenv('MAX_FILE_SIZE'):
            config.security.max_file_size = int(os.getenv('MAX_FILE_SIZE'))
        if os.getenv('CODE_TIMEOUT'):
            config.security.code_execution_timeout = int(os.getenv('CODE_TIMEOUT'))
            
        # 性能配置
        if os.getenv('CACHE_ENABLED'):
            config.performance.cache_enabled = os.getenv('CACHE_ENABLED').lower() == 'true'
        if os.getenv('MAX_WORKERS'):
            config.performance.worker_threads = int(os.getenv('MAX_WORKERS'))
            
        # 日志配置
        if os.getenv('LOG_LEVEL'):
            config.logging.level = os.getenv('LOG_LEVEL')
        if os.getenv('LOG_FILE'):
            config.logging.file_path = os.getenv('LOG_FILE')
            
        return config
    
    @classmethod
    def from_file(cls, file_path: str) -> 'Config':
        """从配置文件加载配置"""
        path = Path(file_path)
        if not path.exists():
            logger.warning(f"配置文件不存在: {file_path}，使用默认配置")
            return cls()
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                if path.suffix.lower() == '.json':
                    data = json.load(f)
                elif path.suffix.lower() in ['.yml', '.yaml']:
                    data = yaml.safe_load(f)
                else:
                    logger.error(f"不支持的配置文件格式: {path.suffix}")
                    return cls()
                    
            return cls.from_dict(data)
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            return cls()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Config':
        """从字典创建配置"""
        config = cls()
        
        if 'security' in data:
            config.security = SecurityConfig(**data['security'])
        if 'performance' in data:
            config.performance = PerformanceConfig(**data['performance'])
        if 'logging' in data:
            config.logging = LoggingConfig(**data['logging'])
        if 'monitoring' in data:
            config.monitoring = MonitoringConfig(**data['monitoring'])
            
        # 基础配置
        for key in ['version', 'debug', 'template_dir', 'charts_dir']:
            if key in data:
                setattr(config, key, data[key])
                
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    def save_to_file(self, file_path: str) -> None:
        """保存到配置文件"""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        data = self.to_dict()
        
        try:
            with open(path, 'w', encoding='utf-8') as f:
                if path.suffix.lower() == '.json':
                    json.dump(data, f, indent=2, ensure_ascii=False)
                elif path.suffix.lower() in ['.yml', '.yaml']:
                    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
                else:
                    logger.error(f"不支持的配置文件格式: {path.suffix}")
                    return
                    
            logger.info(f"配置已保存到: {file_path}")
        except Exception as e:
            logger.error(f"保存配置文件失败: {e}")

# 全局配置实例
_global_config: Optional[Config] = None

def get_config() -> Config:
    """获取全局配置实例"""
    global _global_config
    if _global_config is None:
        # 优先从环境变量加载，然后尝试配置文件
        config_file = os.getenv('CONFIG_FILE', 'config/config.yaml')
        if os.path.exists(config_file):
            _global_config = Config.from_file(config_file)
        else:
            _global_config = Config.from_env()
    return _global_config

def set_config(config: Config) -> None:
    """设置全局配置实例"""
    global _global_config
    _global_config = config

def reload_config() -> Config:
    """重新加载配置"""
    global _global_config
    _global_config = None
    return get_config()

def load_config(file_path: Optional[str] = None) -> Config:
    """加载配置文件"""
    if file_path:
        return Config.from_file(file_path)
    
    # 尝试默认配置文件路径
    default_paths = [
        'config/config.yaml',
        'config/config.yml',
        'config/config.json',
        'config.yaml',
        'config.yml',
        'config.json'
    ]
    
    for path in default_paths:
        if os.path.exists(path):
            return Config.from_file(path)
    
    # 如果没有找到配置文件，从环境变量加载
    return Config.from_env()

def save_config(config: Config, file_path: str) -> bool:
    """保存配置到文件"""
    try:
        config.save_to_file(file_path)
        return True
    except Exception as e:
        logger.error(f"保存配置失败: {e}")
        return False

def validate_config(config: Config) -> List[str]:
    """验证配置的有效性"""
    errors = []
    
    # 验证安全配置
    if config.security.max_file_size <= 0:
        errors.append("最大文件大小必须大于0")
    
    if config.security.code_execution_timeout <= 0:
        errors.append("代码执行超时时间必须大于0")
    
    if not config.security.allowed_file_types:
        errors.append("允许的文件类型不能为空")
    
    # 验证性能配置
    if config.performance.max_concurrent_requests <= 0:
        errors.append("最大并发请求数必须大于0")
    
    if config.performance.worker_threads <= 0:
        errors.append("工作线程数必须大于0")
    
    # 验证日志配置
    valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    if config.logging.level not in valid_log_levels:
        errors.append(f"日志级别必须是以下之一: {', '.join(valid_log_levels)}")
    
    # 验证监控配置
    if config.monitoring.health_check_interval <= 0:
        errors.append("健康检查间隔必须大于0")
    
    # 验证路径
    try:
        Path(config.logging.file_path).parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        errors.append(f"无法创建日志目录: {config.logging.file_path}")
    
    return errors