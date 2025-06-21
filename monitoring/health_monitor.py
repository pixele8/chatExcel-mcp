"""Health Monitor Module.

Provides comprehensive health monitoring for the ChatExcel MCP server,
including service status, dependency checks, and health reporting.
"""

import os
import time
import psutil
import threading
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

try:
    from core.config import get_config
    from core.exceptions import HealthCheckError
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    def get_config():
        return {'monitoring': {'health_check_interval': 60}}
    
    # 如果core不可用，创建简单的HealthCheckError类
    class HealthCheckError(Exception):
        def __init__(self, check_type: str, error_details: str):
            super().__init__(f"Health check failed for {check_type}: {error_details}")


class HealthStatus(Enum):
    """Health status enumeration."""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


@dataclass
class HealthCheck:
    """Health check configuration."""
    name: str
    check_function: Callable[[], bool]
    description: str
    timeout: int = 30
    critical: bool = True
    enabled: bool = True
    last_check: Optional[float] = None
    last_result: Optional[bool] = None
    last_error: Optional[str] = None


@dataclass
class HealthReport:
    """Health report data structure."""
    timestamp: float
    overall_status: HealthStatus
    checks: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    system_info: Dict[str, Any] = field(default_factory=dict)
    uptime: float = 0.0
    version: str = "2.0"


class HealthMonitor:
    """Comprehensive health monitoring system."""
    
    def __init__(self):
        """Initialize health monitor."""
        self.config = get_config() if CORE_AVAILABLE else get_config()
        self.monitoring_config = self.config.get('monitoring', {})
        
        self.checks: Dict[str, HealthCheck] = {}
        self.start_time = time.time()
        self.last_report: Optional[HealthReport] = None
        self.monitoring_thread: Optional[threading.Thread] = None
        self.monitoring_active = False
        
        # Register default health checks
        self._register_default_checks()
    
    def register_check(self, check: HealthCheck) -> None:
        """Register a health check.
        
        Args:
            check: Health check to register
        """
        self.checks[check.name] = check
    
    def unregister_check(self, name: str) -> None:
        """Unregister a health check.
        
        Args:
            name: Name of check to unregister
        """
        if name in self.checks:
            del self.checks[name]
    
    def run_check(self, name: str) -> Dict[str, Any]:
        """Run a specific health check.
        
        Args:
            name: Name of check to run
            
        Returns:
            Check result dictionary
        """
        if name not in self.checks:
            return {
                'status': HealthStatus.UNKNOWN.value,
                'error': f'Check {name} not found',
                'timestamp': time.time()
            }
        
        check = self.checks[name]
        
        if not check.enabled:
            return {
                'status': HealthStatus.UNKNOWN.value,
                'message': 'Check disabled',
                'timestamp': time.time()
            }
        
        start_time = time.time()
        
        try:
            # Run check with timeout
            result = self._run_with_timeout(check.check_function, check.timeout)
            
            check.last_check = time.time()
            check.last_result = result
            check.last_error = None
            
            status = HealthStatus.HEALTHY if result else (
                HealthStatus.CRITICAL if check.critical else HealthStatus.WARNING
            )
            
            return {
                'status': status.value,
                'result': result,
                'duration': time.time() - start_time,
                'timestamp': check.last_check,
                'description': check.description
            }
            
        except Exception as e:
            check.last_check = time.time()
            check.last_result = False
            check.last_error = str(e)
            
            status = HealthStatus.CRITICAL if check.critical else HealthStatus.WARNING
            
            return {
                'status': status.value,
                'error': str(e),
                'duration': time.time() - start_time,
                'timestamp': check.last_check,
                'description': check.description
            }
    
    def run_all_checks(self) -> HealthReport:
        """Run all registered health checks.
        
        Returns:
            Complete health report
        """
        report = HealthReport(
            timestamp=time.time(),
            overall_status=HealthStatus.HEALTHY,
            uptime=time.time() - self.start_time
        )
        
        # Run all checks
        critical_failed = False
        warning_failed = False
        
        for name, check in self.checks.items():
            result = self.run_check(name)
            report.checks[name] = result
            
            if result['status'] == HealthStatus.CRITICAL.value:
                critical_failed = True
            elif result['status'] == HealthStatus.WARNING.value:
                warning_failed = True
        
        # Determine overall status
        if critical_failed:
            report.overall_status = HealthStatus.CRITICAL
        elif warning_failed:
            report.overall_status = HealthStatus.WARNING
        else:
            report.overall_status = HealthStatus.HEALTHY
        
        # Add system information
        report.system_info = self._get_system_info()
        
        self.last_report = report
        return report
    
    def get_status(self) -> Dict[str, Any]:
        """Get current health status.
        
        Returns:
            Current health status dictionary
        """
        if self.last_report is None:
            report = self.run_all_checks()
        else:
            report = self.last_report
        
        return {
            'status': report.overall_status.value,
            'timestamp': report.timestamp,
            'uptime': report.uptime,
            'version': report.version,
            'checks_total': len(self.checks),
            'checks_healthy': sum(1 for check in report.checks.values() 
                                if check['status'] == HealthStatus.HEALTHY.value),
            'checks_warning': sum(1 for check in report.checks.values() 
                                if check['status'] == HealthStatus.WARNING.value),
            'checks_critical': sum(1 for check in report.checks.values() 
                                 if check['status'] == HealthStatus.CRITICAL.value)
        }
    
    def start_monitoring(self, interval: Optional[int] = None) -> None:
        """Start continuous health monitoring.
        
        Args:
            interval: Monitoring interval in seconds
        """
        if self.monitoring_active:
            return
        
        interval = interval or self.monitoring_config.get('health_check_interval', 60)
        self.monitoring_active = True
        
        def monitor_loop():
            while self.monitoring_active:
                try:
                    self.run_all_checks()
                    time.sleep(interval)
                except Exception as e:
                    print(f"Health monitoring error: {e}")
                    time.sleep(interval)
        
        self.monitoring_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitoring_thread.start()
    
    def stop_monitoring(self) -> None:
        """Stop continuous health monitoring."""
        self.monitoring_active = False
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5)
    
    def _register_default_checks(self) -> None:
        """Register default health checks."""
        # System resource checks
        self.register_check(HealthCheck(
            name="cpu_usage",
            check_function=self._check_cpu_usage,
            description="Check CPU usage is below threshold",
            critical=False
        ))
        
        self.register_check(HealthCheck(
            name="memory_usage",
            check_function=self._check_memory_usage,
            description="Check memory usage is below threshold",
            critical=False
        ))
        
        self.register_check(HealthCheck(
            name="disk_space",
            check_function=self._check_disk_space,
            description="Check available disk space",
            critical=True
        ))
        
        # Application checks
        self.register_check(HealthCheck(
            name="python_environment",
            check_function=self._check_python_environment,
            description="Check Python environment and dependencies",
            critical=True
        ))
        
        self.register_check(HealthCheck(
            name="file_permissions",
            check_function=self._check_file_permissions,
            description="Check file system permissions",
            critical=True
        ))
        
        self.register_check(HealthCheck(
            name="configuration",
            check_function=self._check_configuration,
            description="Check configuration validity",
            critical=True
        ))
    
    def _check_cpu_usage(self) -> bool:
        """Check CPU usage."""
        cpu_percent = psutil.cpu_percent(interval=1)
        threshold = self.monitoring_config.get('cpu_threshold', 80)
        return cpu_percent < threshold
    
    def _check_memory_usage(self) -> bool:
        """Check memory usage."""
        memory = psutil.virtual_memory()
        threshold = self.monitoring_config.get('memory_threshold', 80)
        return memory.percent < threshold
    
    def _check_disk_space(self) -> bool:
        """Check disk space."""
        disk = psutil.disk_usage('/')
        threshold = self.monitoring_config.get('disk_threshold', 90)
        return (disk.used / disk.total * 100) < threshold
    
    def _check_python_environment(self) -> bool:
        """Check Python environment."""
        try:
            import pandas
            import numpy
            import openpyxl
            return True
        except ImportError:
            return False
    
    def _check_file_permissions(self) -> bool:
        """Check file permissions."""
        try:
            # Check if we can read/write in current directory
            test_file = Path('health_check_test.tmp')
            test_file.write_text('test')
            content = test_file.read_text()
            test_file.unlink()
            return content == 'test'
        except Exception:
            return False
    
    def _check_configuration(self) -> bool:
        """Check configuration validity."""
        try:
            config = self.config
            return isinstance(config, dict) and len(config) > 0
        except Exception:
            return False
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get system information."""
        try:
            return {
                'platform': os.name,
                'cpu_count': psutil.cpu_count(),
                'memory_total': psutil.virtual_memory().total,
                'disk_total': psutil.disk_usage('/').total,
                'python_version': f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
                'process_id': os.getpid(),
                'working_directory': os.getcwd()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _run_with_timeout(self, func: Callable, timeout: int) -> Any:
        """Run function with timeout.
        
        Args:
            func: Function to run
            timeout: Timeout in seconds
            
        Returns:
            Function result
        """
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError(f"Health check timed out after {timeout} seconds")
        
        # Set timeout
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)
        
        try:
            result = func()
            return result
        finally:
            # Restore old handler
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)


# Global health monitor instance
_global_health_monitor = None


def get_health_monitor() -> HealthMonitor:
    """Get global health monitor instance.
    
    Returns:
        Global HealthMonitor instance
    """
    global _global_health_monitor
    if _global_health_monitor is None:
        _global_health_monitor = HealthMonitor()
    return _global_health_monitor