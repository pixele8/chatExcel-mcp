"""Performance Monitor Module.

Provides comprehensive performance monitoring for the ChatExcel MCP server,
including execution time tracking, resource usage monitoring, and performance metrics.
"""

import time
import psutil
import threading
import functools
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, field
from collections import defaultdict, deque
from contextlib import contextmanager
import statistics

try:
    from core.config import get_config
    from core.exceptions import PerformanceError
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    def get_config():
        return {'monitoring': {'performance_history_size': 1000}}
    
    class PerformanceError(Exception):
        pass


@dataclass
class PerformanceMetric:
    """Performance metric data structure."""
    name: str
    value: float
    unit: str
    timestamp: float
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class ExecutionStats:
    """Execution statistics."""
    count: int = 0
    total_time: float = 0.0
    min_time: float = float('inf')
    max_time: float = 0.0
    avg_time: float = 0.0
    last_execution: Optional[float] = None
    errors: int = 0
    
    def update(self, execution_time: float, error: bool = False) -> None:
        """Update statistics with new execution.
        
        Args:
            execution_time: Execution time in seconds
            error: Whether execution resulted in error
        """
        self.count += 1
        self.total_time += execution_time
        self.min_time = min(self.min_time, execution_time)
        self.max_time = max(self.max_time, execution_time)
        self.avg_time = self.total_time / self.count
        self.last_execution = time.time()
        
        if error:
            self.errors += 1


@dataclass
class ResourceSnapshot:
    """Resource usage snapshot."""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_used: int
    disk_io_read: int
    disk_io_write: int
    network_sent: int
    network_recv: int


class PerformanceMonitor:
    """Comprehensive performance monitoring system."""
    
    def __init__(self):
        """Initialize performance monitor."""
        self.config = get_config() if CORE_AVAILABLE else get_config()
        self.monitoring_config = self.config.get('monitoring', {})
        
        # Performance data storage
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(
            maxlen=self.monitoring_config.get('performance_history_size', 1000)
        ))
        self.execution_stats: Dict[str, ExecutionStats] = defaultdict(ExecutionStats)
        self.resource_history: deque = deque(
            maxlen=self.monitoring_config.get('resource_history_size', 100)
        )
        
        # Monitoring state
        self.monitoring_active = False
        self.monitoring_thread: Optional[threading.Thread] = None
        self.start_time = time.time()
        
        # Performance thresholds
        self.thresholds = {
            'cpu_warning': 70.0,
            'cpu_critical': 90.0,
            'memory_warning': 70.0,
            'memory_critical': 90.0,
            'execution_time_warning': 5.0,
            'execution_time_critical': 10.0
        }
        self.thresholds.update(self.monitoring_config.get('thresholds', {}))
        
        # Lock for thread safety
        self._lock = threading.Lock()
    
    def record_metric(self, name: str, value: float, unit: str = '', 
                     tags: Optional[Dict[str, str]] = None) -> None:
        """Record a performance metric.
        
        Args:
            name: Metric name
            value: Metric value
            unit: Unit of measurement
            tags: Additional tags for the metric
        """
        metric = PerformanceMetric(
            name=name,
            value=value,
            unit=unit,
            timestamp=time.time(),
            tags=tags or {}
        )
        
        with self._lock:
            self.metrics[name].append(metric)
    
    def record_execution(self, operation: str, execution_time: float, 
                        error: bool = False) -> None:
        """Record execution statistics.
        
        Args:
            operation: Operation name
            execution_time: Execution time in seconds
            error: Whether execution resulted in error
        """
        with self._lock:
            self.execution_stats[operation].update(execution_time, error)
        
        # Record as metric
        self.record_metric(
            f"execution_time.{operation}",
            execution_time,
            "seconds",
            {'operation': operation, 'error': str(error)}
        )
    
    def get_execution_stats(self, operation: Optional[str] = None) -> Dict[str, Any]:
        """Get execution statistics.
        
        Args:
            operation: Specific operation to get stats for
            
        Returns:
            Execution statistics dictionary
        """
        with self._lock:
            if operation:
                if operation in self.execution_stats:
                    stats = self.execution_stats[operation]
                    return {
                        'operation': operation,
                        'count': stats.count,
                        'total_time': stats.total_time,
                        'avg_time': stats.avg_time,
                        'min_time': stats.min_time if stats.min_time != float('inf') else 0,
                        'max_time': stats.max_time,
                        'error_rate': stats.errors / stats.count if stats.count > 0 else 0,
                        'last_execution': stats.last_execution
                    }
                else:
                    return {'operation': operation, 'count': 0}
            else:
                return {
                    op: {
                        'count': stats.count,
                        'avg_time': stats.avg_time,
                        'error_rate': stats.errors / stats.count if stats.count > 0 else 0
                    }
                    for op, stats in self.execution_stats.items()
                }
    
    def get_metric_stats(self, name: str, window_seconds: Optional[int] = None) -> Dict[str, Any]:
        """Get statistics for a specific metric.
        
        Args:
            name: Metric name
            window_seconds: Time window for statistics (None for all data)
            
        Returns:
            Metric statistics dictionary
        """
        with self._lock:
            if name not in self.metrics:
                return {'name': name, 'count': 0}
            
            metrics = list(self.metrics[name])
            
            # Filter by time window if specified
            if window_seconds:
                cutoff_time = time.time() - window_seconds
                metrics = [m for m in metrics if m.timestamp >= cutoff_time]
            
            if not metrics:
                return {'name': name, 'count': 0}
            
            values = [m.value for m in metrics]
            
            return {
                'name': name,
                'count': len(values),
                'min': min(values),
                'max': max(values),
                'avg': statistics.mean(values),
                'median': statistics.median(values),
                'std_dev': statistics.stdev(values) if len(values) > 1 else 0,
                'latest': values[-1],
                'unit': metrics[-1].unit,
                'first_timestamp': metrics[0].timestamp,
                'last_timestamp': metrics[-1].timestamp
            }
    
    def capture_resource_snapshot(self) -> ResourceSnapshot:
        """Capture current resource usage snapshot.
        
        Returns:
            Resource usage snapshot
        """
        try:
            # Get CPU and memory info
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            
            # Get disk I/O info
            disk_io = psutil.disk_io_counters()
            disk_read = disk_io.read_bytes if disk_io else 0
            disk_write = disk_io.write_bytes if disk_io else 0
            
            # Get network I/O info
            network_io = psutil.net_io_counters()
            network_sent = network_io.bytes_sent if network_io else 0
            network_recv = network_io.bytes_recv if network_io else 0
            
            snapshot = ResourceSnapshot(
                timestamp=time.time(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used=memory.used,
                disk_io_read=disk_read,
                disk_io_write=disk_write,
                network_sent=network_sent,
                network_recv=network_recv
            )
            
            with self._lock:
                self.resource_history.append(snapshot)
            
            # Record as metrics
            self.record_metric('cpu_percent', cpu_percent, '%')
            self.record_metric('memory_percent', memory.percent, '%')
            self.record_metric('memory_used', memory.used, 'bytes')
            
            return snapshot
            
        except Exception as e:
            raise PerformanceError(metric="resource_snapshot", threshold=0.0, current=-1.0)
    
    def get_resource_stats(self, window_seconds: Optional[int] = None) -> Dict[str, Any]:
        """Get resource usage statistics.
        
        Args:
            window_seconds: Time window for statistics
            
        Returns:
            Resource statistics dictionary
        """
        with self._lock:
            snapshots = list(self.resource_history)
        
        if not snapshots:
            return {'count': 0}
        
        # Filter by time window if specified
        if window_seconds:
            cutoff_time = time.time() - window_seconds
            snapshots = [s for s in snapshots if s.timestamp >= cutoff_time]
        
        if not snapshots:
            return {'count': 0}
        
        # Calculate statistics
        cpu_values = [s.cpu_percent for s in snapshots]
        memory_values = [s.memory_percent for s in snapshots]
        
        return {
            'count': len(snapshots),
            'cpu': {
                'min': min(cpu_values),
                'max': max(cpu_values),
                'avg': statistics.mean(cpu_values),
                'current': cpu_values[-1]
            },
            'memory': {
                'min': min(memory_values),
                'max': max(memory_values),
                'avg': statistics.mean(memory_values),
                'current': memory_values[-1]
            },
            'latest_snapshot': {
                'timestamp': snapshots[-1].timestamp,
                'cpu_percent': snapshots[-1].cpu_percent,
                'memory_percent': snapshots[-1].memory_percent,
                'memory_used': snapshots[-1].memory_used
            }
        }
    
    def check_performance_alerts(self) -> List[Dict[str, Any]]:
        """Check for performance alerts based on thresholds.
        
        Returns:
            List of performance alerts
        """
        alerts = []
        
        # Check latest resource snapshot
        if self.resource_history:
            latest = self.resource_history[-1]
            
            # CPU alerts
            if latest.cpu_percent >= self.thresholds['cpu_critical']:
                alerts.append({
                    'type': 'cpu',
                    'level': 'critical',
                    'message': f'CPU usage critical: {latest.cpu_percent:.1f}%',
                    'value': latest.cpu_percent,
                    'threshold': self.thresholds['cpu_critical']
                })
            elif latest.cpu_percent >= self.thresholds['cpu_warning']:
                alerts.append({
                    'type': 'cpu',
                    'level': 'warning',
                    'message': f'CPU usage high: {latest.cpu_percent:.1f}%',
                    'value': latest.cpu_percent,
                    'threshold': self.thresholds['cpu_warning']
                })
            
            # Memory alerts
            if latest.memory_percent >= self.thresholds['memory_critical']:
                alerts.append({
                    'type': 'memory',
                    'level': 'critical',
                    'message': f'Memory usage critical: {latest.memory_percent:.1f}%',
                    'value': latest.memory_percent,
                    'threshold': self.thresholds['memory_critical']
                })
            elif latest.memory_percent >= self.thresholds['memory_warning']:
                alerts.append({
                    'type': 'memory',
                    'level': 'warning',
                    'message': f'Memory usage high: {latest.memory_percent:.1f}%',
                    'value': latest.memory_percent,
                    'threshold': self.thresholds['memory_warning']
                })
        
        # Check execution time alerts
        for operation, stats in self.execution_stats.items():
            if stats.avg_time >= self.thresholds['execution_time_critical']:
                alerts.append({
                    'type': 'execution_time',
                    'level': 'critical',
                    'message': f'Slow execution for {operation}: {stats.avg_time:.2f}s avg',
                    'operation': operation,
                    'value': stats.avg_time,
                    'threshold': self.thresholds['execution_time_critical']
                })
            elif stats.avg_time >= self.thresholds['execution_time_warning']:
                alerts.append({
                    'type': 'execution_time',
                    'level': 'warning',
                    'message': f'Slow execution for {operation}: {stats.avg_time:.2f}s avg',
                    'operation': operation,
                    'value': stats.avg_time,
                    'threshold': self.thresholds['execution_time_warning']
                })
        
        return alerts
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary.
        
        Returns:
            Performance summary dictionary
        """
        return {
            'uptime': time.time() - self.start_time,
            'resource_stats': self.get_resource_stats(window_seconds=300),  # Last 5 minutes
            'execution_stats': self.get_execution_stats(),
            'alerts': self.check_performance_alerts(),
            'metrics_count': {name: len(metrics) for name, metrics in self.metrics.items()},
            'monitoring_active': self.monitoring_active
        }
    
    def start_monitoring(self, interval: int = 30) -> None:
        """Start continuous performance monitoring.
        
        Args:
            interval: Monitoring interval in seconds
        """
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        
        def monitor_loop():
            while self.monitoring_active:
                try:
                    self.capture_resource_snapshot()
                    time.sleep(interval)
                except Exception as e:
                    print(f"Performance monitoring error: {e}")
                    time.sleep(interval)
        
        self.monitoring_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitoring_thread.start()
    
    def stop_monitoring(self) -> None:
        """Stop continuous performance monitoring."""
        self.monitoring_active = False
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5)
    
    @contextmanager
    def measure_execution(self, operation: str):
        """Context manager for measuring execution time.
        
        Args:
            operation: Operation name
        """
        start_time = time.time()
        error_occurred = False
        
        try:
            yield
        except Exception as e:
            error_occurred = True
            raise
        finally:
            execution_time = time.time() - start_time
            self.record_execution(operation, execution_time, error_occurred)
    
    def performance_decorator(self, operation: Optional[str] = None):
        """Decorator for measuring function performance.
        
        Args:
            operation: Operation name (defaults to function name)
        """
        def decorator(func: Callable) -> Callable:
            op_name = operation or func.__name__
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                with self.measure_execution(op_name):
                    return func(*args, **kwargs)
            
            return wrapper
        
        return decorator


# Global performance monitor instance
_global_performance_monitor = None


def get_performance_monitor() -> PerformanceMonitor:
    """Get global performance monitor instance.
    
    Returns:
        Global PerformanceMonitor instance
    """
    global _global_performance_monitor
    if _global_performance_monitor is None:
        _global_performance_monitor = PerformanceMonitor()
    return _global_performance_monitor


# Convenience decorators
def measure_performance(operation: Optional[str] = None):
    """Decorator for measuring function performance.
    
    Args:
        operation: Operation name (defaults to function name)
    """
    return get_performance_monitor().performance_decorator(operation)