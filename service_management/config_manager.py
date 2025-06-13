# -*- coding: utf-8 -*-
"""
集成配置管理器
统一管理安全配置、服务配置和运行时配置
"""

import os
import json
import yaml
import threading
import time
from typing import Dict, Any, Optional, List, Union, Callable
from dataclasses import dataclass, field, asdict
from pathlib import Path
from enum import Enum
import logging
from cryptography.fernet import Fernet
import base64
import hashlib
from contextlib import contextmanager
import tempfile
import shutil

# 配置日志
logger = logging.getLogger(__name__)

class ConfigFormat(Enum):
    """配置文件格式"""
    JSON = "json"
    YAML = "yaml"
    ENV = "env"
    TOML = "toml"

class ConfigScope(Enum):
    """配置作用域"""
    GLOBAL = "global"
    SERVICE = "service"
    SECURITY = "security"
    RUNTIME = "runtime"
    USER = "user"

class ConfigPriority(Enum):
    """配置优先级"""
    SYSTEM = 1
    GLOBAL = 2
    SERVICE = 3
    USER = 4
    RUNTIME = 5
    OVERRIDE = 6

@dataclass
class ConfigSource:
    """配置源"""
    name: str
    path: Path
    format: ConfigFormat
    scope: ConfigScope
    priority: ConfigPriority
    encrypted: bool = False
    watch: bool = True
    last_modified: Optional[float] = None
    checksum: Optional[str] = None

@dataclass
class SecurityConfig:
    """安全配置"""
    # API 安全
    api_key_required: bool = True
    jwt_secret: Optional[str] = None
    jwt_expiry: int = 3600
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    
    # 文件安全
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    allowed_file_types: List[str] = field(default_factory=lambda: ['.xlsx', '.xls', '.csv'])
    upload_path_whitelist: List[str] = field(default_factory=list)
    
    # 代码执行安全
    code_execution_enabled: bool = False
    code_execution_timeout: int = 30
    code_execution_memory_limit: int = 512  # MB
    blacklisted_modules: List[str] = field(default_factory=lambda: [
        'os', 'sys', 'subprocess', 'importlib', '__import__'
    ])
    
    # 网络安全
    allowed_hosts: List[str] = field(default_factory=lambda: ['localhost', '127.0.0.1'])
    ssl_enabled: bool = False
    ssl_cert_path: Optional[str] = None
    ssl_key_path: Optional[str] = None
    
    # 日志安全
    log_sensitive_data: bool = False
    audit_log_enabled: bool = True
    audit_log_path: str = "logs/audit.log"

@dataclass
class ServiceConfig:
    """服务配置"""
    # 基本配置
    name: str
    host: str = "localhost"
    port: int = 8080
    debug: bool = False
    
    # 性能配置
    workers: int = 1
    max_connections: int = 1000
    timeout: int = 30
    keep_alive: int = 2
    
    # 健康检查
    health_check_enabled: bool = True
    health_check_interval: int = 30
    health_check_timeout: int = 5
    health_check_retries: int = 3
    
    # 重启策略
    auto_restart: bool = True
    max_restart_attempts: int = 3
    restart_delay: int = 10
    graceful_shutdown_timeout: int = 30
    
    # 依赖服务
    dependencies: List[str] = field(default_factory=list)
    
    # 环境变量
    environment: Dict[str, str] = field(default_factory=dict)

@dataclass
class RuntimeConfig:
    """运行时配置"""
    # 资源限制
    max_memory_usage: int = 1024  # MB
    max_cpu_usage: float = 80.0  # 百分比
    max_disk_usage: int = 10 * 1024  # MB
    
    # 缓存配置
    cache_enabled: bool = True
    cache_size: int = 100  # MB
    cache_ttl: int = 3600  # 秒
    
    # 日志配置
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: str = "logs/app.log"
    log_max_size: int = 10 * 1024 * 1024  # 10MB
    log_backup_count: int = 5
    
    # 监控配置
    metrics_enabled: bool = True
    metrics_port: int = 9090
    tracing_enabled: bool = False
    
    # 临时文件
    temp_dir: str = "/tmp/chatexcel"
    temp_cleanup_interval: int = 3600

class ConfigEncryption:
    """配置加密器"""
    
    def __init__(self, key: Optional[bytes] = None):
        if key:
            self.key = key
        else:
            # 从环境变量或生成新密钥
            key_str = os.environ.get('CONFIG_ENCRYPTION_KEY')
            if key_str:
                self.key = base64.urlsafe_b64decode(key_str.encode())
            else:
                self.key = Fernet.generate_key()
                logger.warning("生成了新的加密密钥，请保存到环境变量 CONFIG_ENCRYPTION_KEY")
                logger.warning(f"密钥: {base64.urlsafe_b64encode(self.key).decode()}")
        
        self.cipher = Fernet(self.key)
    
    def encrypt(self, data: str) -> str:
        """加密数据"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """解密数据"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
    
    def encrypt_file(self, file_path: Path) -> Path:
        """加密文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        encrypted_content = self.encrypt(content)
        encrypted_path = file_path.with_suffix(file_path.suffix + '.enc')
        
        with open(encrypted_path, 'w', encoding='utf-8') as f:
            f.write(encrypted_content)
        
        return encrypted_path
    
    def decrypt_file(self, encrypted_file_path: Path) -> str:
        """解密文件"""
        with open(encrypted_file_path, 'r', encoding='utf-8') as f:
            encrypted_content = f.read()
        
        return self.decrypt(encrypted_content)

class ConfigValidator:
    """配置验证器"""
    
    def __init__(self):
        self.validators: Dict[str, Callable] = {}
        self._register_default_validators()
    
    def _register_default_validators(self):
        """注册默认验证器"""
        self.validators.update({
            'port': self._validate_port,
            'host': self._validate_host,
            'timeout': self._validate_positive_int,
            'memory_limit': self._validate_positive_int,
            'file_size': self._validate_positive_int,
            'log_level': self._validate_log_level,
            'file_path': self._validate_file_path,
            'directory_path': self._validate_directory_path
        })
    
    def register_validator(self, name: str, validator: Callable):
        """注册自定义验证器"""
        self.validators[name] = validator
    
    def validate_config(self, config: Dict[str, Any], schema: Dict[str, str]) -> List[str]:
        """验证配置"""
        errors = []
        
        for key, validator_name in schema.items():
            if key in config:
                validator = self.validators.get(validator_name)
                if validator:
                    try:
                        if not validator(config[key]):
                            errors.append(f"配置项 {key} 验证失败")
                    except Exception as e:
                        errors.append(f"配置项 {key} 验证异常: {e}")
        
        return errors
    
    def _validate_port(self, value: Any) -> bool:
        """验证端口号"""
        return isinstance(value, int) and 1 <= value <= 65535
    
    def _validate_host(self, value: Any) -> bool:
        """验证主机地址"""
        if not isinstance(value, str):
            return False
        # 简单验证，实际应该更严格
        return len(value) > 0 and not value.isspace()
    
    def _validate_positive_int(self, value: Any) -> bool:
        """验证正整数"""
        return isinstance(value, int) and value > 0
    
    def _validate_log_level(self, value: Any) -> bool:
        """验证日志级别"""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        return isinstance(value, str) and value.upper() in valid_levels
    
    def _validate_file_path(self, value: Any) -> bool:
        """验证文件路径"""
        if not isinstance(value, str):
            return False
        path = Path(value)
        return path.exists() and path.is_file()
    
    def _validate_directory_path(self, value: Any) -> bool:
        """验证目录路径"""
        if not isinstance(value, str):
            return False
        path = Path(value)
        return path.exists() and path.is_dir()

class ConfigWatcher:
    """配置文件监控器"""
    
    def __init__(self, callback: Callable[[Path], None]):
        self.callback = callback
        self.watched_files: Dict[Path, float] = {}
        self.watching = False
        self.watch_thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()
    
    def add_file(self, file_path: Path):
        """添加监控文件"""
        with self.lock:
            if file_path.exists():
                self.watched_files[file_path] = file_path.stat().st_mtime
    
    def remove_file(self, file_path: Path):
        """移除监控文件"""
        with self.lock:
            self.watched_files.pop(file_path, None)
    
    def start_watching(self):
        """开始监控"""
        if self.watching:
            return
        
        self.watching = True
        self.watch_thread = threading.Thread(target=self._watch_loop, daemon=True)
        self.watch_thread.start()
        logger.info("配置文件监控已启动")
    
    def stop_watching(self):
        """停止监控"""
        self.watching = False
        if self.watch_thread:
            self.watch_thread.join(timeout=5)
        logger.info("配置文件监控已停止")
    
    def _watch_loop(self):
        """监控循环"""
        while self.watching:
            try:
                with self.lock:
                    files_to_check = dict(self.watched_files)
                
                for file_path, last_mtime in files_to_check.items():
                    if file_path.exists():
                        current_mtime = file_path.stat().st_mtime
                        if current_mtime > last_mtime:
                            logger.info(f"检测到配置文件变化: {file_path}")
                            self.watched_files[file_path] = current_mtime
                            try:
                                self.callback(file_path)
                            except Exception as e:
                                logger.error(f"处理配置文件变化失败: {e}")
                    else:
                        logger.warning(f"监控的配置文件不存在: {file_path}")
                
                time.sleep(1)  # 每秒检查一次
                
            except Exception as e:
                logger.error(f"配置监控异常: {e}")
                time.sleep(5)

class ConfigManager:
    """配置管理器主类"""
    
    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path.cwd() / "config"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # 配置源
        self.config_sources: List[ConfigSource] = []
        self.merged_config: Dict[str, Any] = {}
        
        # 组件
        self.encryptor = ConfigEncryption()
        self.validator = ConfigValidator()
        self.watcher = ConfigWatcher(self._on_config_changed)
        
        # 锁
        self.lock = threading.Lock()
        
        # 回调
        self.change_callbacks: List[Callable[[str, Any, Any], None]] = []
        
        # 初始化
        self._discover_config_files()
        self._load_all_configs()
        
        # 启动监控
        self.watcher.start_watching()
    
    def _discover_config_files(self):
        """发现配置文件"""
        # 系统配置
        system_configs = [
            ("system.json", ConfigScope.GLOBAL, ConfigPriority.SYSTEM),
            ("security.json", ConfigScope.SECURITY, ConfigPriority.SYSTEM),
            ("services.yaml", ConfigScope.SERVICE, ConfigPriority.SYSTEM)
        ]
        
        for filename, scope, priority in system_configs:
            file_path = self.config_dir / filename
            if file_path.exists():
                format_type = ConfigFormat.JSON if filename.endswith('.json') else ConfigFormat.YAML
                source = ConfigSource(
                    name=filename,
                    path=file_path,
                    format=format_type,
                    scope=scope,
                    priority=priority
                )
                self.config_sources.append(source)
                self.watcher.add_file(file_path)
        
        # 环境变量配置
        env_source = ConfigSource(
            name="environment",
            path=Path("/dev/null"),  # 虚拟路径
            format=ConfigFormat.ENV,
            scope=ConfigScope.RUNTIME,
            priority=ConfigPriority.OVERRIDE,
            watch=False
        )
        self.config_sources.append(env_source)
        
        logger.info(f"发现 {len(self.config_sources)} 个配置源")
    
    def add_config_source(self, source: ConfigSource):
        """添加配置源"""
        with self.lock:
            self.config_sources.append(source)
            if source.watch and source.path.exists():
                self.watcher.add_file(source.path)
            
            # 重新加载配置
            self._load_all_configs()
    
    def _load_all_configs(self):
        """加载所有配置"""
        with self.lock:
            # 按优先级排序
            sorted_sources = sorted(self.config_sources, key=lambda x: x.priority.value)
            
            merged = {}
            
            for source in sorted_sources:
                try:
                    config_data = self._load_config_source(source)
                    if config_data:
                        # 深度合并配置
                        merged = self._deep_merge(merged, config_data)
                        logger.debug(f"加载配置源: {source.name}")
                except Exception as e:
                    logger.error(f"加载配置源 {source.name} 失败: {e}")
            
            # 验证配置
            validation_errors = self._validate_merged_config(merged)
            if validation_errors:
                logger.warning(f"配置验证发现问题: {validation_errors}")
            
            old_config = self.merged_config.copy()
            self.merged_config = merged
            
            # 触发变化回调
            self._trigger_change_callbacks(old_config, merged)
            
            logger.info("配置加载完成")
    
    def _load_config_source(self, source: ConfigSource) -> Optional[Dict[str, Any]]:
        """加载单个配置源"""
        if source.format == ConfigFormat.ENV:
            return self._load_env_config()
        
        if not source.path.exists():
            return None
        
        try:
            # 检查文件是否加密
            if source.encrypted:
                content = self.encryptor.decrypt_file(source.path)
            else:
                with open(source.path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            # 解析配置
            if source.format == ConfigFormat.JSON:
                return json.loads(content)
            elif source.format == ConfigFormat.YAML:
                return yaml.safe_load(content)
            else:
                logger.warning(f"不支持的配置格式: {source.format}")
                return None
        
        except Exception as e:
            logger.error(f"解析配置文件 {source.path} 失败: {e}")
            return None
    
    def _load_env_config(self) -> Dict[str, Any]:
        """加载环境变量配置"""
        env_config = {}
        
        # 定义环境变量映射
        env_mappings = {
            'CHATEXCEL_HOST': 'service.host',
            'CHATEXCEL_PORT': 'service.port',
            'CHATEXCEL_DEBUG': 'service.debug',
            'CHATEXCEL_LOG_LEVEL': 'runtime.log_level',
            'CHATEXCEL_MAX_FILE_SIZE': 'security.max_file_size',
            'CHATEXCEL_API_KEY_REQUIRED': 'security.api_key_required',
            'CHATEXCEL_JWT_SECRET': 'security.jwt_secret',
            'CHATEXCEL_RATE_LIMIT': 'security.rate_limit_requests'
        }
        
        for env_var, config_path in env_mappings.items():
            value = os.environ.get(env_var)
            if value is not None:
                # 类型转换
                if env_var.endswith('_PORT') or env_var.endswith('_SIZE') or env_var.endswith('_LIMIT'):
                    try:
                        value = int(value)
                    except ValueError:
                        continue
                elif env_var.endswith('_DEBUG') or env_var.endswith('_REQUIRED'):
                    value = value.lower() in ('true', '1', 'yes', 'on')
                
                # 设置嵌套配置
                self._set_nested_config(env_config, config_path, value)
        
        return env_config
    
    def _set_nested_config(self, config: Dict[str, Any], path: str, value: Any):
        """设置嵌套配置"""
        keys = path.split('.')
        current = config
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def _deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
        """深度合并字典"""
        result = base.copy()
        
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _validate_merged_config(self, config: Dict[str, Any]) -> List[str]:
        """验证合并后的配置"""
        errors = []
        
        # 定义验证规则
        validation_schema = {
            'service.port': 'port',
            'service.host': 'host',
            'service.timeout': 'timeout',
            'runtime.log_level': 'log_level',
            'security.max_file_size': 'file_size'
        }
        
        # 展平配置进行验证
        flat_config = self._flatten_config(config)
        
        return self.validator.validate_config(flat_config, validation_schema)
    
    def _flatten_config(self, config: Dict[str, Any], prefix: str = '') -> Dict[str, Any]:
        """展平配置字典"""
        flat = {}
        
        for key, value in config.items():
            full_key = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                flat.update(self._flatten_config(value, full_key))
            else:
                flat[full_key] = value
        
        return flat
    
    def _on_config_changed(self, file_path: Path):
        """配置文件变化回调"""
        logger.info(f"重新加载配置文件: {file_path}")
        self._load_all_configs()
    
    def _trigger_change_callbacks(self, old_config: Dict[str, Any], new_config: Dict[str, Any]):
        """触发变化回调"""
        # 找出变化的配置项
        changes = self._find_config_changes(old_config, new_config)
        
        for path, old_value, new_value in changes:
            for callback in self.change_callbacks:
                try:
                    callback(path, old_value, new_value)
                except Exception as e:
                    logger.error(f"配置变化回调执行失败: {e}")
    
    def _find_config_changes(self, old: Dict[str, Any], new: Dict[str, Any], prefix: str = '') -> List[Tuple[str, Any, Any]]:
        """找出配置变化"""
        changes = []
        
        # 检查新增和修改
        for key, new_value in new.items():
            full_key = f"{prefix}.{key}" if prefix else key
            
            if key not in old:
                changes.append((full_key, None, new_value))
            elif old[key] != new_value:
                if isinstance(old[key], dict) and isinstance(new_value, dict):
                    changes.extend(self._find_config_changes(old[key], new_value, full_key))
                else:
                    changes.append((full_key, old[key], new_value))
        
        # 检查删除
        for key, old_value in old.items():
            if key not in new:
                full_key = f"{prefix}.{key}" if prefix else key
                changes.append((full_key, old_value, None))
        
        return changes
    
    def get(self, path: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = path.split('.')
        current = self.merged_config
        
        try:
            for key in keys:
                current = current[key]
            return current
        except (KeyError, TypeError):
            return default
    
    def set(self, path: str, value: Any, persist: bool = False):
        """设置配置值"""
        with self.lock:
            keys = path.split('.')
            current = self.merged_config
            
            # 导航到父级
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            
            old_value = current.get(keys[-1])
            current[keys[-1]] = value
            
            # 触发回调
            for callback in self.change_callbacks:
                try:
                    callback(path, old_value, value)
                except Exception as e:
                    logger.error(f"配置变化回调执行失败: {e}")
            
            # 持久化
            if persist:
                self._persist_config_change(path, value)
    
    def _persist_config_change(self, path: str, value: Any):
        """持久化配置变化"""
        try:
            # 保存到用户配置文件
            user_config_file = self.config_dir / "user.json"
            
            if user_config_file.exists():
                with open(user_config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
            else:
                user_config = {}
            
            # 设置嵌套值
            self._set_nested_config(user_config, path, value)
            
            # 保存
            with open(user_config_file, 'w', encoding='utf-8') as f:
                json.dump(user_config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"配置已持久化: {path} = {value}")
            
        except Exception as e:
            logger.error(f"持久化配置失败: {e}")
    
    def get_security_config(self) -> SecurityConfig:
        """获取安全配置"""
        security_data = self.get('security', {})
        
        # 使用默认值填充缺失的字段
        default_security = SecurityConfig()
        
        for field_name, field_def in default_security.__dataclass_fields__.items():
            if field_name not in security_data:
                if field_def.default != field_def.default_factory:
                    security_data[field_name] = field_def.default
                else:
                    security_data[field_name] = field_def.default_factory()
        
        return SecurityConfig(**security_data)
    
    def get_service_config(self, service_name: str = 'default') -> ServiceConfig:
        """获取服务配置"""
        service_data = self.get(f'service.{service_name}', self.get('service', {}))
        
        # 使用默认值填充
        default_service = ServiceConfig(name=service_name)
        
        for field_name, field_def in default_service.__dataclass_fields__.items():
            if field_name not in service_data:
                if field_def.default != field_def.default_factory:
                    service_data[field_name] = field_def.default
                else:
                    service_data[field_name] = field_def.default_factory()
        
        return ServiceConfig(**service_data)
    
    def get_runtime_config(self) -> RuntimeConfig:
        """获取运行时配置"""
        runtime_data = self.get('runtime', {})
        
        # 使用默认值填充
        default_runtime = RuntimeConfig()
        
        for field_name, field_def in default_runtime.__dataclass_fields__.items():
            if field_name not in runtime_data:
                if field_def.default != field_def.default_factory:
                    runtime_data[field_name] = field_def.default
                else:
                    runtime_data[field_name] = field_def.default_factory()
        
        return RuntimeConfig(**runtime_data)
    
    def register_change_callback(self, callback: Callable[[str, Any, Any], None]):
        """注册配置变化回调"""
        self.change_callbacks.append(callback)
    
    def export_config(self, output_file: Path, format_type: ConfigFormat = ConfigFormat.JSON, encrypt: bool = False):
        """导出配置"""
        try:
            if format_type == ConfigFormat.JSON:
                content = json.dumps(self.merged_config, indent=2, ensure_ascii=False)
            elif format_type == ConfigFormat.YAML:
                content = yaml.dump(self.merged_config, default_flow_style=False, allow_unicode=True)
            else:
                raise ValueError(f"不支持的导出格式: {format_type}")
            
            if encrypt:
                content = self.encryptor.encrypt(content)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"配置已导出到: {output_file}")
            
        except Exception as e:
            logger.error(f"导出配置失败: {e}")
    
    def import_config(self, input_file: Path, merge: bool = True, encrypted: bool = False):
        """导入配置"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if encrypted:
                content = self.encryptor.decrypt(content)
            
            # 解析配置
            if input_file.suffix.lower() == '.json':
                imported_config = json.loads(content)
            elif input_file.suffix.lower() in ['.yaml', '.yml']:
                imported_config = yaml.safe_load(content)
            else:
                raise ValueError(f"不支持的文件格式: {input_file.suffix}")
            
            with self.lock:
                if merge:
                    old_config = self.merged_config.copy()
                    self.merged_config = self._deep_merge(self.merged_config, imported_config)
                    self._trigger_change_callbacks(old_config, self.merged_config)
                else:
                    old_config = self.merged_config.copy()
                    self.merged_config = imported_config
                    self._trigger_change_callbacks(old_config, self.merged_config)
            
            logger.info(f"配置已从 {input_file} 导入")
            
        except Exception as e:
            logger.error(f"导入配置失败: {e}")
    
    def create_backup(self) -> Path:
        """创建配置备份"""
        try:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            backup_file = self.config_dir / f"backup_config_{timestamp}.json"
            
            self.export_config(backup_file, ConfigFormat.JSON, encrypt=True)
            
            logger.info(f"配置备份已创建: {backup_file}")
            return backup_file
            
        except Exception as e:
            logger.error(f"创建配置备份失败: {e}")
            raise
    
    def restore_backup(self, backup_file: Path):
        """恢复配置备份"""
        try:
            self.import_config(backup_file, merge=False, encrypted=True)
            logger.info(f"配置已从备份恢复: {backup_file}")
            
        except Exception as e:
            logger.error(f"恢复配置备份失败: {e}")
            raise
    
    def get_config_summary(self) -> Dict[str, Any]:
        """获取配置摘要"""
        return {
            'sources': [
                {
                    'name': source.name,
                    'path': str(source.path),
                    'format': source.format.value,
                    'scope': source.scope.value,
                    'priority': source.priority.value,
                    'encrypted': source.encrypted,
                    'watch': source.watch
                }
                for source in self.config_sources
            ],
            'total_keys': len(self._flatten_config(self.merged_config)),
            'security_enabled': self.get('security.api_key_required', False),
            'debug_mode': self.get('service.debug', False),
            'log_level': self.get('runtime.log_level', 'INFO')
        }
    
    @contextmanager
    def temporary_config(self, **kwargs):
        """临时配置上下文管理器"""
        old_values = {}
        
        try:
            # 保存旧值并设置新值
            for path, value in kwargs.items():
                old_values[path] = self.get(path)
                self.set(path, value)
            
            yield
            
        finally:
            # 恢复旧值
            for path, old_value in old_values.items():
                if old_value is not None:
                    self.set(path, old_value)
    
    def shutdown(self):
        """关闭配置管理器"""
        logger.info("关闭配置管理器")
        
        # 停止监控
        self.watcher.stop_watching()
        
        # 创建最终备份
        try:
            self.create_backup()
        except Exception as e:
            logger.error(f"创建最终备份失败: {e}")
        
        logger.info("配置管理器已关闭")

# 全局配置管理器实例
_global_config_manager: Optional[ConfigManager] = None

def get_config_manager() -> ConfigManager:
    """获取全局配置管理器"""
    global _global_config_manager
    if _global_config_manager is None:
        _global_config_manager = ConfigManager()
    return _global_config_manager

def get_config(path: str, default: Any = None) -> Any:
    """获取配置的便捷函数"""
    return get_config_manager().get(path, default)

def set_config(path: str, value: Any, persist: bool = False):
    """设置配置的便捷函数"""
    get_config_manager().set(path, value, persist)

if __name__ == "__main__":
    # 测试代码
    import tempfile
    
    # 创建临时配置目录
    with tempfile.TemporaryDirectory() as temp_dir:
        config_dir = Path(temp_dir) / "config"
        config_dir.mkdir()
        
        # 创建测试配置文件
        test_config = {
            "service": {
                "host": "localhost",
                "port": 8080,
                "debug": True
            },
            "security": {
                "api_key_required": True,
                "max_file_size": 104857600
            }
        }
        
        with open(config_dir / "system.json", 'w') as f:
            json.dump(test_config, f, indent=2)
        
        # 创建配置管理器
        manager = ConfigManager(config_dir)
        
        # 测试配置获取
        print(f"服务端口: {manager.get('service.port')}")
        print(f"调试模式: {manager.get('service.debug')}")
        
        # 测试配置设置
        manager.set('service.port', 9090, persist=True)
        print(f"新端口: {manager.get('service.port')}")
        
        # 测试结构化配置
        security_config = manager.get_security_config()
        print(f"安全配置: {security_config}")
        
        # 测试配置摘要
        summary = manager.get_config_summary()
        print(f"配置摘要: {summary}")
        
        # 测试临时配置
        with manager.temporary_config(**{'service.debug': False}):
            print(f"临时调试模式: {manager.get('service.debug')}")
        
        print(f"恢复后调试模式: {manager.get('service.debug')}")
        
        # 关闭管理器
        manager.shutdown()