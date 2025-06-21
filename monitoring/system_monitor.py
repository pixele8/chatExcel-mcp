"""System Monitor Module.

Provides system-level monitoring for the ChatExcel MCP server,
including process monitoring, file system monitoring, and system events.
"""

import os
import time
import psutil
import threading
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from pathlib import Path
import logging
from collections import defaultdict, deque

try:
    from core.config import get_config
    from core.exceptions import SystemMonitorError
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    def get_config():
        return {'monitoring': {'system_check_interval': 60}}
    
    class SystemMonitorError(Exception):
        pass


@dataclass
class ProcessInfo:
    """Process information data structure."""
    pid: int
    name: str
    status: str
    cpu_percent: float
    memory_percent: float
    memory_rss: int
    memory_vms: int
    create_time: float
    num_threads: int
    num_fds: int = 0  # File descriptors (Unix only)
    connections: int = 0


@dataclass
class FileSystemInfo:
    """File system information."""
    path: str
    total: int
    used: int
    free: int
    percent: float
    fstype: str = ""
    device: str = ""


@dataclass
class SystemEvent:
    """System event data structure."""
    timestamp: float
    event_type: str
    severity: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


class SystemMonitor:
    """Comprehensive system monitoring."""
    
    def __init__(self):
        """Initialize system monitor."""
        self.config = get_config() if CORE_AVAILABLE else get_config()
        self.monitoring_config = self.config.get('monitoring', {})
        
        # Process monitoring
        self.current_process = psutil.Process()
        self.monitored_processes: Dict[int, ProcessInfo] = {}
        
        # File system monitoring
        self.file_systems: Dict[str, FileSystemInfo] = {}
        self.watched_paths: List[str] = []
        
        # Event tracking
        self.events: deque = deque(
            maxlen=self.monitoring_config.get('max_events', 1000)
        )
        
        # System state
        self.boot_time = psutil.boot_time()
        self.start_time = time.time()
        
        # Monitoring thread
        self.monitoring_active = False
        self.monitoring_thread: Optional[threading.Thread] = None
        
        # Thresholds
        self.thresholds = {
            'cpu_warning': 70.0,
            'cpu_critical': 90.0,
            'memory_warning': 70.0,
            'memory_critical': 90.0,
            'disk_warning': 80.0,
            'disk_critical': 95.0,
            'fd_warning': 80.0,  # Percentage of max file descriptors
            'fd_critical': 95.0
        }
        self.thresholds.update(self.monitoring_config.get('thresholds', {}))
        
        # Lock for thread safety
        self._lock = threading.Lock()
        
        # Initialize monitoring
        self._initialize_monitoring()
    
    def _initialize_monitoring(self) -> None:
        """Initialize monitoring components."""
        # Add current working directory to watched paths
        self.watched_paths.append(os.getcwd())
        
        # Add common system paths if they exist
        common_paths = ['/tmp', '/var/log', '/var/tmp']
        for path in common_paths:
            if os.path.exists(path):
                self.watched_paths.append(path)
        
        # Initial file system scan
        self._scan_file_systems()
        
        # Log initialization
        self._log_event('system', 'info', 'System monitor initialized')
    
    def get_process_info(self, pid: Optional[int] = None) -> ProcessInfo:
        """Get process information.
        
        Args:
            pid: Process ID (defaults to current process)
            
        Returns:
            Process information
        """
        try:
            process = psutil.Process(pid) if pid else self.current_process
            
            # Get memory info
            memory_info = process.memory_info()
            
            # Get number of file descriptors (Unix only)
            num_fds = 0
            try:
                num_fds = process.num_fds()
            except (AttributeError, psutil.AccessDenied):
                pass
            
            # Get connections
            connections = 0
            try:
                connections = len(process.connections())
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass
            
            return ProcessInfo(
                pid=process.pid,
                name=process.name(),
                status=process.status(),
                cpu_percent=process.cpu_percent(),
                memory_percent=process.memory_percent(),
                memory_rss=memory_info.rss,
                memory_vms=memory_info.vms,
                create_time=process.create_time(),
                num_threads=process.num_threads(),
                num_fds=num_fds,
                connections=connections
            )
            
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            raise SystemMonitorError(monitor_type="process_info", error_details=f"Failed to get process info: {e}")
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information.
        
        Returns:
            System information dictionary
        """
        try:
            # CPU information
            cpu_info = {
                'count': psutil.cpu_count(),
                'count_logical': psutil.cpu_count(logical=True),
                'percent': psutil.cpu_percent(interval=1),
                'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
            }
            
            # Memory information
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            memory_info = {
                'virtual': memory._asdict(),
                'swap': swap._asdict()
            }
            
            # Disk information
            disk_info = {}
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info[partition.mountpoint] = {
                        'device': partition.device,
                        'fstype': partition.fstype,
                        'total': usage.total,
                        'used': usage.used,
                        'free': usage.free,
                        'percent': (usage.used / usage.total) * 100
                    }
                except (PermissionError, FileNotFoundError):
                    continue
            
            # Network information
            network_info = {}
            try:
                network_io = psutil.net_io_counters()
                if network_io:
                    network_info = network_io._asdict()
            except Exception:
                pass
            
            # System uptime
            uptime = time.time() - self.boot_time
            
            return {
                'cpu': cpu_info,
                'memory': memory_info,
                'disk': disk_info,
                'network': network_info,
                'uptime': uptime,
                'boot_time': self.boot_time,
                'load_avg': os.getloadavg() if hasattr(os, 'getloadavg') else None,
                'process_count': len(psutil.pids())
            }
            
        except Exception as e:
            raise SystemMonitorError(monitor_type="system_info", error_details=f"Failed to get system info: {e}")
    
    def _scan_file_systems(self) -> None:
        """Scan and update file system information."""
        try:
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    
                    fs_info = FileSystemInfo(
                        path=partition.mountpoint,
                        total=usage.total,
                        used=usage.used,
                        free=usage.free,
                        percent=(usage.used / usage.total) * 100,
                        fstype=partition.fstype,
                        device=partition.device
                    )
                    
                    with self._lock:
                        self.file_systems[partition.mountpoint] = fs_info
                    
                except (PermissionError, FileNotFoundError):
                    continue
                    
        except Exception as e:
            self._log_event('filesystem', 'error', f'File system scan failed: {e}')
    
    def get_file_system_info(self, path: Optional[str] = None) -> Dict[str, Any]:
        """Get file system information.
        
        Args:
            path: Specific path to check (defaults to all)
            
        Returns:
            File system information
        """
        with self._lock:
            if path:
                # Find the file system containing this path
                for mount_point, fs_info in self.file_systems.items():
                    if path.startswith(mount_point):
                        return {
                            'path': path,
                            'mount_point': mount_point,
                            'total': fs_info.total,
                            'used': fs_info.used,
                            'free': fs_info.free,
                            'percent': fs_info.percent,
                            'fstype': fs_info.fstype,
                            'device': fs_info.device
                        }
                return {'path': path, 'error': 'File system not found'}
            else:
                return {
                    mount_point: {
                        'total': fs_info.total,
                        'used': fs_info.used,
                        'free': fs_info.free,
                        'percent': fs_info.percent,
                        'fstype': fs_info.fstype,
                        'device': fs_info.device
                    }
                    for mount_point, fs_info in self.file_systems.items()
                }
    
    def check_system_health(self) -> Dict[str, Any]:
        """Check overall system health.
        
        Returns:
            System health report
        """
        health_report = {
            'status': 'healthy',
            'issues': [],
            'warnings': [],
            'timestamp': time.time()
        }
        
        try:
            # Check CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent >= self.thresholds['cpu_critical']:
                health_report['status'] = 'critical'
                health_report['issues'].append(f'Critical CPU usage: {cpu_percent:.1f}%')
            elif cpu_percent >= self.thresholds['cpu_warning']:
                if health_report['status'] == 'healthy':
                    health_report['status'] = 'warning'
                health_report['warnings'].append(f'High CPU usage: {cpu_percent:.1f}%')
            
            # Check memory usage
            memory = psutil.virtual_memory()
            if memory.percent >= self.thresholds['memory_critical']:
                health_report['status'] = 'critical'
                health_report['issues'].append(f'Critical memory usage: {memory.percent:.1f}%')
            elif memory.percent >= self.thresholds['memory_warning']:
                if health_report['status'] == 'healthy':
                    health_report['status'] = 'warning'
                health_report['warnings'].append(f'High memory usage: {memory.percent:.1f}%')
            
            # Check disk usage
            for mount_point, fs_info in self.file_systems.items():
                if fs_info.percent >= self.thresholds['disk_critical']:
                    health_report['status'] = 'critical'
                    health_report['issues'].append(
                        f'Critical disk usage on {mount_point}: {fs_info.percent:.1f}%'
                    )
                elif fs_info.percent >= self.thresholds['disk_warning']:
                    if health_report['status'] == 'healthy':
                        health_report['status'] = 'warning'
                    health_report['warnings'].append(
                        f'High disk usage on {mount_point}: {fs_info.percent:.1f}%'
                    )
            
            # Check process health
            try:
                process_info = self.get_process_info()
                
                # Check file descriptors (Unix only)
                if process_info.num_fds > 0:
                    try:
                        # Get system limit for file descriptors
                        import resource
                        fd_limit = resource.getrlimit(resource.RLIMIT_NOFILE)[0]
                        fd_percent = (process_info.num_fds / fd_limit) * 100
                        
                        if fd_percent >= self.thresholds['fd_critical']:
                            health_report['status'] = 'critical'
                            health_report['issues'].append(
                                f'Critical file descriptor usage: {fd_percent:.1f}%'
                            )
                        elif fd_percent >= self.thresholds['fd_warning']:
                            if health_report['status'] == 'healthy':
                                health_report['status'] = 'warning'
                            health_report['warnings'].append(
                                f'High file descriptor usage: {fd_percent:.1f}%'
                            )
                    except (ImportError, OSError):
                        pass
                
            except SystemMonitorError:
                health_report['warnings'].append('Unable to check process health')
            
        except Exception as e:
            health_report['status'] = 'error'
            health_report['issues'].append(f'Health check failed: {e}')
        
        return health_report
    
    def _log_event(self, event_type: str, severity: str, message: str, 
                   details: Optional[Dict[str, Any]] = None) -> None:
        """Log a system event.
        
        Args:
            event_type: Type of event
            severity: Event severity (info, warning, error, critical)
            message: Event message
            details: Additional event details
        """
        event = SystemEvent(
            timestamp=time.time(),
            event_type=event_type,
            severity=severity,
            message=message,
            details=details or {}
        )
        
        with self._lock:
            self.events.append(event)
        
        # Also log to Python logging if available
        try:
            logger = logging.getLogger(__name__)
            log_level = getattr(logging, severity.upper(), logging.INFO)
            logger.log(log_level, f"[{event_type}] {message}")
        except Exception:
            pass
    
    def get_events(self, event_type: Optional[str] = None, 
                   severity: Optional[str] = None,
                   limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get system events.
        
        Args:
            event_type: Filter by event type
            severity: Filter by severity
            limit: Maximum number of events to return
            
        Returns:
            List of events
        """
        with self._lock:
            events = list(self.events)
        
        # Apply filters
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        if severity:
            events = [e for e in events if e.severity == severity]
        
        # Sort by timestamp (newest first)
        events.sort(key=lambda e: e.timestamp, reverse=True)
        
        # Apply limit
        if limit:
            events = events[:limit]
        
        return [
            {
                'timestamp': e.timestamp,
                'event_type': e.event_type,
                'severity': e.severity,
                'message': e.message,
                'details': e.details
            }
            for e in events
        ]
    
    def start_monitoring(self, interval: int = 60) -> None:
        """Start continuous system monitoring.
        
        Args:
            interval: Monitoring interval in seconds
        """
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        
        def monitor_loop():
            while self.monitoring_active:
                try:
                    # Update file system information
                    self._scan_file_systems()
                    
                    # Check system health
                    health = self.check_system_health()
                    
                    # Log health issues
                    if health['status'] != 'healthy':
                        self._log_event(
                            'health_check',
                            health['status'],
                            f"System health: {health['status']}",
                            {'issues': health['issues'], 'warnings': health['warnings']}
                        )
                    
                    time.sleep(interval)
                    
                except Exception as e:
                    self._log_event('monitoring', 'error', f'Monitoring error: {e}')
                    time.sleep(interval)
        
        self.monitoring_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitoring_thread.start()
        
        self._log_event('monitoring', 'info', 'System monitoring started')
    
    def stop_monitoring(self) -> None:
        """Stop continuous system monitoring."""
        if not self.monitoring_active:
            return
        
        self.monitoring_active = False
        
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5)
        
        self._log_event('monitoring', 'info', 'System monitoring stopped')
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get monitoring status.
        
        Returns:
            Monitoring status information
        """
        return {
            'active': self.monitoring_active,
            'uptime': time.time() - self.start_time,
            'events_count': len(self.events),
            'watched_paths': self.watched_paths,
            'file_systems_count': len(self.file_systems),
            'current_process': {
                'pid': self.current_process.pid,
                'name': self.current_process.name(),
                'status': self.current_process.status()
            }
        }


# Global system monitor instance
_global_system_monitor = None


def get_system_monitor() -> SystemMonitor:
    """Get global system monitor instance.
    
    Returns:
        Global SystemMonitor instance
    """
    global _global_system_monitor
    if _global_system_monitor is None:
        _global_system_monitor = SystemMonitor()
    return _global_system_monitor