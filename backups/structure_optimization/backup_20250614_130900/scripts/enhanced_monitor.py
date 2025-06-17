#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强监控系统
用于实时监控项目状态、性能指标和依赖健康状况
"""

import json
import time
import psutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import threading
import queue
import logging
from dataclasses import dataclass, asdict

@dataclass
class SystemMetrics:
    """系统指标数据类"""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    memory_used_gb: float
    memory_total_gb: float
    disk_percent: float
    disk_used_gb: float
    disk_total_gb: float
    network_sent_mb: float
    network_recv_mb: float
    process_count: int
    load_average: List[float]

@dataclass
class DependencyStatus:
    """依赖状态数据类"""
    name: str
    version: str
    status: str  # 'ok', 'outdated', 'vulnerable', 'missing'
    latest_version: Optional[str] = None
    vulnerabilities: List[str] = None
    last_checked: str = None

@dataclass
class ServiceHealth:
    """服务健康状态数据类"""
    service_name: str
    status: str  # 'running', 'stopped', 'error'
    response_time_ms: Optional[float] = None
    error_message: Optional[str] = None
    last_check: str = None
    uptime_seconds: Optional[float] = None

class EnhancedMonitor:
    """增强监控系统"""
    
    def __init__(self, project_root: str, config_file: str = None):
        """初始化监控系统
        
        Args:
            project_root: 项目根目录
            config_file: 配置文件路径
        """
        self.project_root = Path(project_root)
        self.config_file = config_file or self.project_root / "config" / "monitor_config.json"
        self.metrics_queue = queue.Queue()
        self.is_monitoring = False
        self.monitor_thread = None
        
        # 设置日志
        self._setup_logging()
        
        # 加载配置
        self.config = self._load_config()
        
        # 初始化监控数据存储
        self.metrics_history = []
        self.dependency_status = {}
        self.service_health = {}
        
        # 网络基线数据
        self.network_baseline = self._get_network_baseline()
        
    def _setup_logging(self):
        """设置日志系统"""
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "monitor.log"),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("EnhancedMonitor")
        
    def _load_config(self) -> Dict:
        """加载监控配置
        
        Returns:
            配置字典
        """
        default_config = {
            "monitoring_interval": 30,  # 秒
            "dependency_check_interval": 3600,  # 秒
            "service_check_interval": 60,  # 秒
            "metrics_retention_hours": 24,
            "alert_thresholds": {
                "cpu_percent": 80,
                "memory_percent": 85,
                "disk_percent": 90,
                "response_time_ms": 5000
            },
            "services_to_monitor": [
                {
                    "name": "mcp_server",
                    "type": "http",
                    "url": "http://localhost:8080/health",
                    "timeout": 5
                }
            ],
            "dependencies_to_monitor": [
                "fastmcp", "pandas", "numpy", "openpyxl", "xlsxwriter"
            ]
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 合并默认配置
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception as e:
                self.logger.warning(f"无法加载配置文件，使用默认配置: {e}")
                
        return default_config
        
    def _get_network_baseline(self) -> Dict:
        """获取网络基线数据
        
        Returns:
            网络基线数据
        """
        try:
            net_io = psutil.net_io_counters()
            return {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'timestamp': time.time()
            }
        except Exception:
            return {'bytes_sent': 0, 'bytes_recv': 0, 'timestamp': time.time()}
            
    def collect_system_metrics(self) -> SystemMetrics:
        """收集系统指标
        
        Returns:
            系统指标对象
        """
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 内存使用情况
            memory = psutil.virtual_memory()
            memory_used_gb = memory.used / (1024**3)
            memory_total_gb = memory.total / (1024**3)
            
            # 磁盘使用情况
            disk = psutil.disk_usage('/')
            disk_used_gb = disk.used / (1024**3)
            disk_total_gb = disk.total / (1024**3)
            
            # 网络使用情况
            net_io = psutil.net_io_counters()
            time_diff = time.time() - self.network_baseline['timestamp']
            
            if time_diff > 0:
                network_sent_mb = (net_io.bytes_sent - self.network_baseline['bytes_sent']) / (1024**2) / time_diff
                network_recv_mb = (net_io.bytes_recv - self.network_baseline['bytes_recv']) / (1024**2) / time_diff
            else:
                network_sent_mb = 0
                network_recv_mb = 0
                
            # 进程数量
            process_count = len(psutil.pids())
            
            # 系统负载
            try:
                load_average = list(psutil.getloadavg())
            except AttributeError:
                # Windows系统不支持getloadavg
                load_average = [0.0, 0.0, 0.0]
                
            return SystemMetrics(
                timestamp=datetime.now().isoformat(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used_gb=round(memory_used_gb, 2),
                memory_total_gb=round(memory_total_gb, 2),
                disk_percent=disk.percent,
                disk_used_gb=round(disk_used_gb, 2),
                disk_total_gb=round(disk_total_gb, 2),
                network_sent_mb=round(network_sent_mb, 2),
                network_recv_mb=round(network_recv_mb, 2),
                process_count=process_count,
                load_average=load_average
            )
            
        except Exception as e:
            self.logger.error(f"收集系统指标失败: {e}")
            return None
            
    def check_dependency_status(self) -> Dict[str, DependencyStatus]:
        """检查依赖状态
        
        Returns:
            依赖状态字典
        """
        self.logger.info("检查依赖状态...")
        
        dependency_status = {}
        
        for dep_name in self.config['dependencies_to_monitor']:
            try:
                # 检查当前版本
                result = subprocess.run(
                    ['pip', 'show', dep_name],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    # 解析版本信息
                    lines = result.stdout.split('\n')
                    version = None
                    for line in lines:
                        if line.startswith('Version:'):
                            version = line.split(':', 1)[1].strip()
                            break
                            
                    if version:
                        # 检查最新版本
                        latest_version = self._get_latest_version(dep_name)
                        
                        # 检查安全漏洞
                        vulnerabilities = self._check_vulnerabilities(dep_name, version)
                        
                        # 确定状态
                        if vulnerabilities:
                            status = 'vulnerable'
                        elif latest_version and version != latest_version:
                            status = 'outdated'
                        else:
                            status = 'ok'
                            
                        dependency_status[dep_name] = DependencyStatus(
                            name=dep_name,
                            version=version,
                            status=status,
                            latest_version=latest_version,
                            vulnerabilities=vulnerabilities,
                            last_checked=datetime.now().isoformat()
                        )
                    else:
                        dependency_status[dep_name] = DependencyStatus(
                            name=dep_name,
                            version='unknown',
                            status='error',
                            last_checked=datetime.now().isoformat()
                        )
                else:
                    dependency_status[dep_name] = DependencyStatus(
                        name=dep_name,
                        version='not_installed',
                        status='missing',
                        last_checked=datetime.now().isoformat()
                    )
                    
            except Exception as e:
                self.logger.error(f"检查依赖 {dep_name} 失败: {e}")
                dependency_status[dep_name] = DependencyStatus(
                    name=dep_name,
                    version='error',
                    status='error',
                    last_checked=datetime.now().isoformat()
                )
                
        self.dependency_status = dependency_status
        return dependency_status
        
    def _get_latest_version(self, package_name: str) -> Optional[str]:
        """获取包的最新版本
        
        Args:
            package_name: 包名
            
        Returns:
            最新版本号
        """
        try:
            result = subprocess.run(
                ['pip', 'index', 'versions', package_name],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # 解析输出获取最新版本
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'Available versions:' in line:
                        versions = line.split(':', 1)[1].strip().split(', ')
                        if versions and versions[0]:
                            return versions[0]
                            
        except Exception as e:
            self.logger.debug(f"获取 {package_name} 最新版本失败: {e}")
            
        return None
        
    def _check_vulnerabilities(self, package_name: str, version: str) -> List[str]:
        """检查包的安全漏洞
        
        Args:
            package_name: 包名
            version: 版本号
            
        Returns:
            漏洞列表
        """
        try:
            # 使用safety检查漏洞
            result = subprocess.run(
                ['safety', 'check', '--json'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                try:
                    safety_data = json.loads(result.stdout)
                    vulnerabilities = []
                    
                    for vuln in safety_data:
                        if vuln.get('package_name', '').lower() == package_name.lower():
                            vulnerabilities.append(vuln.get('advisory', 'Unknown vulnerability'))
                            
                    return vulnerabilities
                except json.JSONDecodeError:
                    pass
                    
        except Exception as e:
            self.logger.debug(f"检查 {package_name} 漏洞失败: {e}")
            
        return []
        
    def check_service_health(self) -> Dict[str, ServiceHealth]:
        """检查服务健康状态
        
        Returns:
            服务健康状态字典
        """
        self.logger.info("检查服务健康状态...")
        
        service_health = {}
        
        for service_config in self.config['services_to_monitor']:
            service_name = service_config['name']
            
            try:
                if service_config['type'] == 'http':
                    health = self._check_http_service(service_config)
                elif service_config['type'] == 'process':
                    health = self._check_process_service(service_config)
                else:
                    health = ServiceHealth(
                        service_name=service_name,
                        status='error',
                        error_message=f"不支持的服务类型: {service_config['type']}",
                        last_check=datetime.now().isoformat()
                    )
                    
                service_health[service_name] = health
                
            except Exception as e:
                self.logger.error(f"检查服务 {service_name} 失败: {e}")
                service_health[service_name] = ServiceHealth(
                    service_name=service_name,
                    status='error',
                    error_message=str(e),
                    last_check=datetime.now().isoformat()
                )
                
        self.service_health = service_health
        return service_health
        
    def _check_http_service(self, service_config: Dict) -> ServiceHealth:
        """检查HTTP服务
        
        Args:
            service_config: 服务配置
            
        Returns:
            服务健康状态
        """
        import requests
        
        service_name = service_config['name']
        url = service_config['url']
        timeout = service_config.get('timeout', 5)
        
        try:
            start_time = time.time()
            response = requests.get(url, timeout=timeout)
            response_time_ms = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                status = 'running'
                error_message = None
            else:
                status = 'error'
                error_message = f"HTTP {response.status_code}"
                
            return ServiceHealth(
                service_name=service_name,
                status=status,
                response_time_ms=round(response_time_ms, 2),
                error_message=error_message,
                last_check=datetime.now().isoformat()
            )
            
        except requests.exceptions.RequestException as e:
            return ServiceHealth(
                service_name=service_name,
                status='stopped',
                error_message=str(e),
                last_check=datetime.now().isoformat()
            )
            
    def _check_process_service(self, service_config: Dict) -> ServiceHealth:
        """检查进程服务
        
        Args:
            service_config: 服务配置
            
        Returns:
            服务健康状态
        """
        service_name = service_config['name']
        process_name = service_config.get('process_name', service_name)
        
        try:
            # 查找进程
            for proc in psutil.process_iter(['pid', 'name', 'create_time']):
                if process_name.lower() in proc.info['name'].lower():
                    uptime_seconds = time.time() - proc.info['create_time']
                    
                    return ServiceHealth(
                        service_name=service_name,
                        status='running',
                        uptime_seconds=round(uptime_seconds, 2),
                        last_check=datetime.now().isoformat()
                    )
                    
            # 进程未找到
            return ServiceHealth(
                service_name=service_name,
                status='stopped',
                error_message="进程未运行",
                last_check=datetime.now().isoformat()
            )
            
        except Exception as e:
            return ServiceHealth(
                service_name=service_name,
                status='error',
                error_message=str(e),
                last_check=datetime.now().isoformat()
            )
            
    def check_alerts(self, metrics: SystemMetrics) -> List[Dict]:
        """检查告警条件
        
        Args:
            metrics: 系统指标
            
        Returns:
            告警列表
        """
        alerts = []
        thresholds = self.config['alert_thresholds']
        
        # CPU告警
        if metrics.cpu_percent > thresholds['cpu_percent']:
            alerts.append({
                'type': 'cpu_high',
                'message': f"CPU使用率过高: {metrics.cpu_percent}%",
                'severity': 'warning',
                'timestamp': metrics.timestamp
            })
            
        # 内存告警
        if metrics.memory_percent > thresholds['memory_percent']:
            alerts.append({
                'type': 'memory_high',
                'message': f"内存使用率过高: {metrics.memory_percent}%",
                'severity': 'warning',
                'timestamp': metrics.timestamp
            })
            
        # 磁盘告警
        if metrics.disk_percent > thresholds['disk_percent']:
            alerts.append({
                'type': 'disk_high',
                'message': f"磁盘使用率过高: {metrics.disk_percent}%",
                'severity': 'critical',
                'timestamp': metrics.timestamp
            })
            
        # 服务响应时间告警
        for service_name, health in self.service_health.items():
            if health.response_time_ms and health.response_time_ms > thresholds['response_time_ms']:
                alerts.append({
                    'type': 'service_slow',
                    'message': f"服务 {service_name} 响应时间过长: {health.response_time_ms}ms",
                    'severity': 'warning',
                    'timestamp': health.last_check
                })
                
        # 依赖漏洞告警
        for dep_name, status in self.dependency_status.items():
            if status.status == 'vulnerable':
                alerts.append({
                    'type': 'dependency_vulnerable',
                    'message': f"依赖 {dep_name} 存在安全漏洞",
                    'severity': 'critical',
                    'timestamp': status.last_checked
                })
                
        return alerts
        
    def start_monitoring(self):
        """开始监控"""
        if self.is_monitoring:
            self.logger.warning("监控已在运行中")
            return
            
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        
        self.logger.info("监控系统已启动")
        
    def stop_monitoring(self):
        """停止监控"""
        self.is_monitoring = False
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
            
        self.logger.info("监控系统已停止")
        
    def _monitoring_loop(self):
        """监控主循环"""
        last_dependency_check = 0
        last_service_check = 0
        
        while self.is_monitoring:
            try:
                current_time = time.time()
                
                # 收集系统指标
                metrics = self.collect_system_metrics()
                if metrics:
                    self.metrics_history.append(metrics)
                    
                    # 清理旧数据
                    self._cleanup_old_metrics()
                    
                    # 检查告警
                    alerts = self.check_alerts(metrics)
                    if alerts:
                        self._handle_alerts(alerts)
                        
                # 定期检查依赖状态
                if current_time - last_dependency_check > self.config['dependency_check_interval']:
                    self.check_dependency_status()
                    last_dependency_check = current_time
                    
                # 定期检查服务健康状态
                if current_time - last_service_check > self.config['service_check_interval']:
                    self.check_service_health()
                    last_service_check = current_time
                    
                # 等待下次检查
                time.sleep(self.config['monitoring_interval'])
                
            except Exception as e:
                self.logger.error(f"监控循环出错: {e}")
                time.sleep(10)  # 出错时等待更长时间
                
    def _cleanup_old_metrics(self):
        """清理旧的指标数据"""
        retention_hours = self.config['metrics_retention_hours']
        cutoff_time = datetime.now() - timedelta(hours=retention_hours)
        
        self.metrics_history = [
            metrics for metrics in self.metrics_history
            if datetime.fromisoformat(metrics.timestamp) > cutoff_time
        ]
        
    def _handle_alerts(self, alerts: List[Dict]):
        """处理告警
        
        Args:
            alerts: 告警列表
        """
        for alert in alerts:
            self.logger.warning(f"告警: {alert['message']}")
            
            # 这里可以添加更多告警处理逻辑，如发送邮件、Slack通知等
            
    def get_monitoring_status(self) -> Dict:
        """获取监控状态
        
        Returns:
            监控状态字典
        """
        latest_metrics = self.metrics_history[-1] if self.metrics_history else None
        
        return {
            'is_monitoring': self.is_monitoring,
            'latest_metrics': asdict(latest_metrics) if latest_metrics else None,
            'dependency_status': {name: asdict(status) for name, status in self.dependency_status.items()},
            'service_health': {name: asdict(health) for name, health in self.service_health.items()},
            'metrics_count': len(self.metrics_history),
            'last_update': datetime.now().isoformat()
        }
        
    def generate_monitoring_report(self) -> str:
        """生成监控报告
        
        Returns:
            监控报告内容
        """
        status = self.get_monitoring_status()
        
        report = f"""
# 系统监控报告

生成时间: {status['last_update']}
监控状态: {'运行中' if status['is_monitoring'] else '已停止'}
指标数据点: {status['metrics_count']} 个

## 系统指标概览
"""
        
        if status['latest_metrics']:
            metrics = status['latest_metrics']
            report += f"""
- **CPU使用率**: {metrics['cpu_percent']}%
- **内存使用率**: {metrics['memory_percent']}% ({metrics['memory_used_gb']:.1f}GB / {metrics['memory_total_gb']:.1f}GB)
- **磁盘使用率**: {metrics['disk_percent']}% ({metrics['disk_used_gb']:.1f}GB / {metrics['disk_total_gb']:.1f}GB)
- **网络流量**: 发送 {metrics['network_sent_mb']:.2f}MB/s, 接收 {metrics['network_recv_mb']:.2f}MB/s
- **进程数量**: {metrics['process_count']}
- **系统负载**: {', '.join(map(str, metrics['load_average']))}

"""
        
        report += "## 依赖状态\n\n"
        
        for name, dep_status in status['dependency_status'].items():
            status_emoji = {
                'ok': '✅',
                'outdated': '⚠️',
                'vulnerable': '🚨',
                'missing': '❌',
                'error': '💥'
            }.get(dep_status['status'], '❓')
            
            report += f"- {status_emoji} **{name}**: {dep_status['version']} ({dep_status['status']})\n"
            
            if dep_status['vulnerabilities']:
                report += f"  - 漏洞: {', '.join(dep_status['vulnerabilities'])}\n"
                
        report += "\n## 服务健康状态\n\n"
        
        for name, health in status['service_health'].items():
            status_emoji = {
                'running': '✅',
                'stopped': '❌',
                'error': '💥'
            }.get(health['status'], '❓')
            
            report += f"- {status_emoji} **{name}**: {health['status']}\n"
            
            if health['response_time_ms']:
                report += f"  - 响应时间: {health['response_time_ms']}ms\n"
                
            if health['uptime_seconds']:
                uptime_hours = health['uptime_seconds'] / 3600
                report += f"  - 运行时间: {uptime_hours:.1f}小时\n"
                
            if health['error_message']:
                report += f"  - 错误: {health['error_message']}\n"
                
        return report
        
    def save_monitoring_report(self, output_file: str = None):
        """保存监控报告
        
        Args:
            output_file: 输出文件路径
        """
        if output_file is None:
            output_file = self.project_root / "monitoring_report.md"
            
        report = self.generate_monitoring_report()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
            
        self.logger.info(f"监控报告已保存到: {output_file}")
        
        # 同时保存JSON格式的详细数据
        status = self.get_monitoring_status()
        json_file = str(output_file).replace('.md', '.json')
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2, ensure_ascii=False)
            
        self.logger.info(f"详细数据已保存到: {json_file}")

def main():
    """主函数"""
    project_root = Path.cwd()
    
    print("🚀 启动增强监控系统...")
    monitor = EnhancedMonitor(str(project_root))
    
    try:
        # 执行一次完整检查
        print("📊 执行系统指标收集...")
        metrics = monitor.collect_system_metrics()
        
        print("🔍 检查依赖状态...")
        monitor.check_dependency_status()
        
        print("🏥 检查服务健康状态...")
        monitor.check_service_health()
        
        # 生成并保存报告
        print("📝 生成监控报告...")
        monitor.save_monitoring_report()
        
        # 显示状态摘要
        status = monitor.get_monitoring_status()
        
        print("\n📊 监控状态摘要:")
        if status['latest_metrics']:
            m = status['latest_metrics']
            print(f"- CPU: {m['cpu_percent']}%")
            print(f"- 内存: {m['memory_percent']}%")
            print(f"- 磁盘: {m['disk_percent']}%")
            
        print(f"\n🔗 依赖状态:")
        for name, dep in status['dependency_status'].items():
            print(f"- {name}: {dep['status']}")
            
        print(f"\n🏥 服务状态:")
        for name, health in status['service_health'].items():
            print(f"- {name}: {health['status']}")
            
        print("\n✅ 监控检查完成！")
        
    except KeyboardInterrupt:
        print("\n⏹️ 监控已停止")
    except Exception as e:
        print(f"❌ 监控出错: {e}")
        
if __name__ == "__main__":
    main()