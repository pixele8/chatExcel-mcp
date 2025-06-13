# -*- coding: utf-8 -*-
"""
服务健康管理器
实现智能的服务健康监控、故障检测和自动恢复
"""

import time
import threading
import requests
import subprocess
import psutil
import logging
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import json
import signal
from contextlib import contextmanager

# 配置日志
logger = logging.getLogger(__name__)

class ServiceStatus(Enum):
    """服务状态枚举"""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    STARTING = "starting"
    STOPPING = "stopping"
    STOPPED = "stopped"
    UNKNOWN = "unknown"

class HealthCheckType(Enum):
    """健康检查类型"""
    HTTP = "http"
    TCP = "tcp"
    PROCESS = "process"
    CUSTOM = "custom"

@dataclass
class HealthCheckConfig:
    """健康检查配置"""
    check_type: HealthCheckType
    endpoint: Optional[str] = None
    port: Optional[int] = None
    timeout: int = 5
    interval: int = 30
    retries: int = 3
    retry_delay: int = 5
    expected_status: int = 200
    custom_check: Optional[Callable] = None

@dataclass
class ServiceConfig:
    """服务配置"""
    name: str
    description: str
    health_check: HealthCheckConfig
    start_command: List[str]
    stop_command: Optional[List[str]] = None
    working_directory: Optional[str] = None
    environment: Dict[str, str] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    max_restart_attempts: int = 3
    restart_delay: int = 10
    graceful_shutdown_timeout: int = 30
    fallback_strategy: Optional[str] = None

@dataclass
class ServiceMetrics:
    """服务指标"""
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    response_time: float = 0.0
    error_rate: float = 0.0
    uptime: float = 0.0
    restart_count: int = 0
    last_health_check: Optional[float] = None
    last_error: Optional[str] = None

class ServiceInstance:
    """服务实例"""
    
    def __init__(self, config: ServiceConfig):
        self.config = config
        self.status = ServiceStatus.STOPPED
        self.process: Optional[subprocess.Popen] = None
        self.metrics = ServiceMetrics()
        self.start_time: Optional[float] = None
        self.restart_attempts = 0
        self.last_restart_time: Optional[float] = None
        self.health_check_failures = 0
        self.lock = threading.Lock()
    
    def start(self) -> bool:
        """启动服务"""
        with self.lock:
            if self.status in [ServiceStatus.HEALTHY, ServiceStatus.STARTING]:
                logger.info(f"服务 {self.config.name} 已在运行")
                return True
            
            try:
                logger.info(f"启动服务: {self.config.name}")
                self.status = ServiceStatus.STARTING
                
                # 准备环境
                env = {**os.environ, **self.config.environment}
                
                # 启动进程
                self.process = subprocess.Popen(
                    self.config.start_command,
                    cwd=self.config.working_directory,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    preexec_fn=os.setsid if hasattr(os, 'setsid') else None
                )
                
                self.start_time = time.time()
                self.restart_attempts += 1
                self.last_restart_time = time.time()
                
                # 等待服务启动
                startup_timeout = 30
                start_check_time = time.time()
                
                while time.time() - start_check_time < startup_timeout:
                    if self._perform_health_check():
                        self.status = ServiceStatus.HEALTHY
                        self.health_check_failures = 0
                        logger.info(f"服务 {self.config.name} 启动成功")
                        return True
                    
                    # 检查进程是否还在运行
                    if self.process.poll() is not None:
                        stdout, stderr = self.process.communicate()
                        logger.error(f"服务 {self.config.name} 启动失败: {stderr.decode()}")
                        self.status = ServiceStatus.STOPPED
                        return False
                    
                    time.sleep(1)
                
                logger.warning(f"服务 {self.config.name} 启动超时")
                self.status = ServiceStatus.UNHEALTHY
                return False
                
            except Exception as e:
                logger.error(f"启动服务 {self.config.name} 失败: {e}")
                self.status = ServiceStatus.STOPPED
                self.metrics.last_error = str(e)
                return False
    
    def stop(self, graceful: bool = True) -> bool:
        """停止服务"""
        with self.lock:
            if self.status == ServiceStatus.STOPPED:
                return True
            
            try:
                logger.info(f"停止服务: {self.config.name}")
                self.status = ServiceStatus.STOPPING
                
                if self.process:
                    if graceful:
                        # 优雅关闭
                        self.process.terminate()
                        try:
                            self.process.wait(timeout=self.config.graceful_shutdown_timeout)
                        except subprocess.TimeoutExpired:
                            logger.warning(f"服务 {self.config.name} 优雅关闭超时，强制终止")
                            self.process.kill()
                            self.process.wait()
                    else:
                        # 强制关闭
                        self.process.kill()
                        self.process.wait()
                    
                    self.process = None
                
                self.status = ServiceStatus.STOPPED
                self.start_time = None
                logger.info(f"服务 {self.config.name} 已停止")
                return True
                
            except Exception as e:
                logger.error(f"停止服务 {self.config.name} 失败: {e}")
                self.metrics.last_error = str(e)
                return False
    
    def restart(self) -> bool:
        """重启服务"""
        logger.info(f"重启服务: {self.config.name}")
        if self.stop():
            time.sleep(self.config.restart_delay)
            return self.start()
        return False
    
    def _perform_health_check(self) -> bool:
        """执行健康检查"""
        try:
            check_start_time = time.time()
            
            if self.config.health_check.check_type == HealthCheckType.HTTP:
                response = requests.get(
                    self.config.health_check.endpoint,
                    timeout=self.config.health_check.timeout
                )
                success = response.status_code == self.config.health_check.expected_status
                
            elif self.config.health_check.check_type == HealthCheckType.TCP:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.config.health_check.timeout)
                result = sock.connect_ex(('localhost', self.config.health_check.port))
                sock.close()
                success = result == 0
                
            elif self.config.health_check.check_type == HealthCheckType.PROCESS:
                success = self.process is not None and self.process.poll() is None
                
            elif self.config.health_check.check_type == HealthCheckType.CUSTOM:
                if self.config.health_check.custom_check:
                    success = self.config.health_check.custom_check(self)
                else:
                    success = False
            else:
                success = False
            
            # 更新指标
            self.metrics.response_time = time.time() - check_start_time
            self.metrics.last_health_check = time.time()
            
            if success:
                self.health_check_failures = 0
            else:
                self.health_check_failures += 1
            
            return success
            
        except Exception as e:
            logger.warning(f"服务 {self.config.name} 健康检查失败: {e}")
            self.health_check_failures += 1
            self.metrics.last_error = str(e)
            return False
    
    def update_metrics(self):
        """更新服务指标"""
        if self.process and self.process.poll() is None:
            try:
                # 获取进程信息
                proc = psutil.Process(self.process.pid)
                self.metrics.cpu_usage = proc.cpu_percent()
                self.metrics.memory_usage = proc.memory_info().rss / (1024 * 1024)  # MB
                
                # 计算运行时间
                if self.start_time:
                    self.metrics.uptime = time.time() - self.start_time
                
                self.metrics.restart_count = self.restart_attempts
                
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    
    def get_status_info(self) -> Dict[str, Any]:
        """获取服务状态信息"""
        return {
            "name": self.config.name,
            "status": self.status.value,
            "metrics": {
                "cpu_usage": self.metrics.cpu_usage,
                "memory_usage": self.metrics.memory_usage,
                "response_time": self.metrics.response_time,
                "uptime": self.metrics.uptime,
                "restart_count": self.metrics.restart_count,
                "health_check_failures": self.health_check_failures,
                "last_health_check": self.metrics.last_health_check,
                "last_error": self.metrics.last_error
            },
            "process_id": self.process.pid if self.process else None,
            "start_time": self.start_time
        }

class FallbackStrategy:
    """降级策略"""
    
    def __init__(self):
        self.strategies = {}
    
    def register_strategy(self, service_name: str, strategy_func: Callable):
        """注册降级策略"""
        self.strategies[service_name] = strategy_func
    
    def execute_fallback(self, service_name: str, *args, **kwargs) -> Any:
        """执行降级策略"""
        if service_name in self.strategies:
            logger.info(f"执行服务 {service_name} 的降级策略")
            return self.strategies[service_name](*args, **kwargs)
        else:
            logger.warning(f"服务 {service_name} 没有配置降级策略")
            return None

class ServiceHealthManager:
    """服务健康管理器"""
    
    def __init__(self):
        self.services: Dict[str, ServiceInstance] = {}
        self.fallback_strategy = FallbackStrategy()
        self.monitoring_thread: Optional[threading.Thread] = None
        self.monitoring_active = False
        self.alert_callbacks: List[Callable] = []
        
        # 配置文件路径
        self.config_file = Path("service_health_config.json")
        
        # 加载配置
        self._load_configuration()
    
    def register_service(self, config: ServiceConfig) -> bool:
        """注册服务"""
        try:
            if config.name in self.services:
                logger.warning(f"服务 {config.name} 已存在，将覆盖配置")
            
            self.services[config.name] = ServiceInstance(config)
            logger.info(f"服务 {config.name} 注册成功")
            
            # 保存配置
            self._save_configuration()
            return True
            
        except Exception as e:
            logger.error(f"注册服务 {config.name} 失败: {e}")
            return False
    
    def start_service(self, service_name: str) -> bool:
        """启动指定服务"""
        if service_name not in self.services:
            logger.error(f"服务 {service_name} 未注册")
            return False
        
        service = self.services[service_name]
        
        # 检查依赖服务
        for dep_name in service.config.dependencies:
            if dep_name in self.services:
                dep_service = self.services[dep_name]
                if dep_service.status != ServiceStatus.HEALTHY:
                    logger.info(f"启动依赖服务: {dep_name}")
                    if not self.start_service(dep_name):
                        logger.error(f"依赖服务 {dep_name} 启动失败")
                        return False
        
        return service.start()
    
    def stop_service(self, service_name: str, graceful: bool = True) -> bool:
        """停止指定服务"""
        if service_name not in self.services:
            logger.error(f"服务 {service_name} 未注册")
            return False
        
        return self.services[service_name].stop(graceful)
    
    def restart_service(self, service_name: str) -> bool:
        """重启指定服务"""
        if service_name not in self.services:
            logger.error(f"服务 {service_name} 未注册")
            return False
        
        return self.services[service_name].restart()
    
    def start_monitoring(self):
        """启动监控"""
        if self.monitoring_active:
            logger.info("监控已在运行")
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        logger.info("服务监控已启动")
    
    def stop_monitoring(self):
        """停止监控"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("服务监控已停止")
    
    def _monitoring_loop(self):
        """监控循环"""
        while self.monitoring_active:
            try:
                for service_name, service in self.services.items():
                    self._check_service_health(service)
                    service.update_metrics()
                
                time.sleep(10)  # 每10秒检查一次
                
            except Exception as e:
                logger.error(f"监控循环异常: {e}")
                time.sleep(5)
    
    def _check_service_health(self, service: ServiceInstance):
        """检查服务健康状态"""
        if service.status in [ServiceStatus.STOPPED, ServiceStatus.STOPPING]:
            return
        
        # 执行健康检查
        is_healthy = service._perform_health_check()
        
        if is_healthy:
            if service.status != ServiceStatus.HEALTHY:
                service.status = ServiceStatus.HEALTHY
                logger.info(f"服务 {service.config.name} 恢复健康")
                self._trigger_alert("service_recovered", service)
        else:
            # 健康检查失败
            if service.health_check_failures >= service.config.health_check.retries:
                if service.status == ServiceStatus.HEALTHY:
                    service.status = ServiceStatus.UNHEALTHY
                    logger.warning(f"服务 {service.config.name} 变为不健康状态")
                    self._trigger_alert("service_unhealthy", service)
                
                # 尝试自动重启
                if service.restart_attempts < service.config.max_restart_attempts:
                    logger.info(f"尝试自动重启服务: {service.config.name}")
                    if service.restart():
                        self._trigger_alert("service_restarted", service)
                    else:
                        self._trigger_alert("service_restart_failed", service)
                else:
                    logger.error(f"服务 {service.config.name} 重启次数超限")
                    self._trigger_alert("service_restart_limit_exceeded", service)
    
    def _trigger_alert(self, alert_type: str, service: ServiceInstance):
        """触发告警"""
        alert_data = {
            "type": alert_type,
            "service": service.config.name,
            "timestamp": time.time(),
            "status": service.status.value,
            "metrics": service.get_status_info()["metrics"]
        }
        
        for callback in self.alert_callbacks:
            try:
                callback(alert_data)
            except Exception as e:
                logger.error(f"告警回调执行失败: {e}")
    
    def register_alert_callback(self, callback: Callable):
        """注册告警回调"""
        self.alert_callbacks.append(callback)
    
    def register_fallback_strategy(self, service_name: str, strategy_func: Callable):
        """注册降级策略"""
        self.fallback_strategy.register_strategy(service_name, strategy_func)
    
    def execute_fallback(self, service_name: str, *args, **kwargs) -> Any:
        """执行降级策略"""
        return self.fallback_strategy.execute_fallback(service_name, *args, **kwargs)
    
    def get_service_status(self, service_name: Optional[str] = None) -> Dict[str, Any]:
        """获取服务状态"""
        if service_name:
            if service_name in self.services:
                return self.services[service_name].get_status_info()
            else:
                return {"error": f"服务 {service_name} 未找到"}
        else:
            return {
                service_name: service.get_status_info()
                for service_name, service in self.services.items()
            }
    
    def _load_configuration(self):
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                for service_data in config_data.get('services', []):
                    # 重建服务配置
                    health_check = HealthCheckConfig(
                        check_type=HealthCheckType(service_data['health_check']['check_type']),
                        endpoint=service_data['health_check'].get('endpoint'),
                        port=service_data['health_check'].get('port'),
                        timeout=service_data['health_check'].get('timeout', 5),
                        interval=service_data['health_check'].get('interval', 30),
                        retries=service_data['health_check'].get('retries', 3)
                    )
                    
                    service_config = ServiceConfig(
                        name=service_data['name'],
                        description=service_data['description'],
                        health_check=health_check,
                        start_command=service_data['start_command'],
                        stop_command=service_data.get('stop_command'),
                        working_directory=service_data.get('working_directory'),
                        environment=service_data.get('environment', {}),
                        dependencies=service_data.get('dependencies', [])
                    )
                    
                    self.register_service(service_config)
                
                logger.info(f"从配置文件加载了 {len(config_data.get('services', []))} 个服务")
                
            except Exception as e:
                logger.error(f"加载配置文件失败: {e}")
    
    def _save_configuration(self):
        """保存配置文件"""
        try:
            config_data = {
                "services": [
                    {
                        "name": service.config.name,
                        "description": service.config.description,
                        "health_check": {
                            "check_type": service.config.health_check.check_type.value,
                            "endpoint": service.config.health_check.endpoint,
                            "port": service.config.health_check.port,
                            "timeout": service.config.health_check.timeout,
                            "interval": service.config.health_check.interval,
                            "retries": service.config.health_check.retries
                        },
                        "start_command": service.config.start_command,
                        "stop_command": service.config.stop_command,
                        "working_directory": service.config.working_directory,
                        "environment": service.config.environment,
                        "dependencies": service.config.dependencies
                    }
                    for service in self.services.values()
                ]
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"保存配置文件失败: {e}")
    
    def shutdown(self):
        """关闭管理器"""
        logger.info("关闭服务健康管理器")
        
        # 停止监控
        self.stop_monitoring()
        
        # 停止所有服务
        for service_name in list(self.services.keys()):
            self.stop_service(service_name)
        
        logger.info("服务健康管理器已关闭")

# 便捷函数
def create_excel_service_config() -> ServiceConfig:
    """创建 Excel Go 服务配置"""
    return ServiceConfig(
        name="excel-go-service",
        description="Excel Go 高性能处理服务",
        health_check=HealthCheckConfig(
            check_type=HealthCheckType.HTTP,
            endpoint="http://localhost:8080/api/v1/health",
            timeout=5,
            interval=30,
            retries=3
        ),
        start_command=["./excel-service"],
        working_directory="excel-service",
        environment={"PORT": "8080"},
        max_restart_attempts=3,
        restart_delay=10
    )

if __name__ == "__main__":
    # 测试代码
    import os
    
    # 创建健康管理器
    manager = ServiceHealthManager()
    
    # 注册 Excel 服务
    excel_config = create_excel_service_config()
    manager.register_service(excel_config)
    
    # 注册告警回调
    def alert_handler(alert_data):
        print(f"告警: {alert_data}")
    
    manager.register_alert_callback(alert_handler)
    
    # 启动监控
    manager.start_monitoring()
    
    try:
        # 启动服务
        manager.start_service("excel-go-service")
        
        # 运行一段时间
        time.sleep(60)
        
        # 获取状态
        status = manager.get_service_status()
        print(f"服务状态: {status}")
        
    finally:
        manager.shutdown()