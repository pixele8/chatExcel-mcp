"""Alert Manager Module.

Provides comprehensive alert management for the ChatExcel MCP server,
including alert rules, notifications, and alert lifecycle management.
"""

import time
import threading
import smtplib
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import logging

try:
    from core.config import get_config
    from core.exceptions import AlertError
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    def get_config():
        return {'monitoring': {'alert_cooldown': 300}}
    
    # 如果core不可用，创建简单的AlertError类
    class AlertError(Exception):
        def __init__(self, alert_type: str, error_details: str):
            super().__init__(f"Alert error in {alert_type}: {error_details}")


class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class AlertStatus(Enum):
    """Alert status."""
    ACTIVE = "active"
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"
    ACKNOWLEDGED = "acknowledged"


@dataclass
class Alert:
    """Alert data structure."""
    id: str
    name: str
    severity: AlertSeverity
    message: str
    source: str
    timestamp: float
    status: AlertStatus = AlertStatus.ACTIVE
    details: Dict[str, Any] = field(default_factory=dict)
    labels: Dict[str, str] = field(default_factory=dict)
    resolved_at: Optional[float] = None
    acknowledged_at: Optional[float] = None
    acknowledged_by: Optional[str] = None
    suppressed_until: Optional[float] = None
    notification_sent: bool = False
    last_notification: Optional[float] = None


@dataclass
class AlertRule:
    """Alert rule configuration."""
    name: str
    condition: Callable[[], bool]
    severity: AlertSeverity
    message_template: str
    source: str
    enabled: bool = True
    cooldown: int = 300  # 5 minutes default
    max_alerts: int = 10
    labels: Dict[str, str] = field(default_factory=dict)
    notification_channels: List[str] = field(default_factory=list)
    auto_resolve: bool = False
    resolve_condition: Optional[Callable[[], bool]] = None


@dataclass
class NotificationChannel:
    """Notification channel configuration."""
    name: str
    type: str  # email, webhook, log, etc.
    config: Dict[str, Any]
    enabled: bool = True
    rate_limit: int = 60  # seconds between notifications
    last_notification: Optional[float] = None


class AlertManager:
    """Comprehensive alert management system."""
    
    def __init__(self):
        """Initialize alert manager."""
        self.config = get_config() if CORE_AVAILABLE else get_config()
        self.monitoring_config = self.config.get('monitoring', {})
        
        # Alert storage
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: deque = deque(
            maxlen=self.monitoring_config.get('max_alert_history', 1000)
        )
        
        # Rules and channels
        self.rules: Dict[str, AlertRule] = {}
        self.notification_channels: Dict[str, NotificationChannel] = {}
        
        # Alert tracking
        self.alert_counts: Dict[str, int] = defaultdict(int)
        self.last_alert_time: Dict[str, float] = {}
        
        # Monitoring thread
        self.monitoring_active = False
        self.monitoring_thread: Optional[threading.Thread] = None
        
        # Lock for thread safety
        self._lock = threading.Lock()
        
        # Initialize default channels
        self._initialize_default_channels()
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def _initialize_default_channels(self) -> None:
        """Initialize default notification channels."""
        # Log channel (always available)
        self.add_notification_channel(NotificationChannel(
            name="log",
            type="log",
            config={"level": "WARNING"},
            enabled=True
        ))
        
        # Email channel (if configured)
        email_config = self.monitoring_config.get('email', {})
        if email_config.get('enabled', False):
            self.add_notification_channel(NotificationChannel(
                name="email",
                type="email",
                config=email_config,
                enabled=True
            ))
        
        # Webhook channel (if configured)
        webhook_config = self.monitoring_config.get('webhook', {})
        if webhook_config.get('enabled', False):
            self.add_notification_channel(NotificationChannel(
                name="webhook",
                type="webhook",
                config=webhook_config,
                enabled=True
            ))
    
    def add_rule(self, rule: AlertRule) -> None:
        """Add an alert rule.
        
        Args:
            rule: Alert rule to add
        """
        with self._lock:
            self.rules[rule.name] = rule
    
    def remove_rule(self, name: str) -> None:
        """Remove an alert rule.
        
        Args:
            name: Rule name to remove
        """
        with self._lock:
            if name in self.rules:
                del self.rules[name]
    
    def add_notification_channel(self, channel: NotificationChannel) -> None:
        """Add a notification channel.
        
        Args:
            channel: Notification channel to add
        """
        with self._lock:
            self.notification_channels[channel.name] = channel
    
    def remove_notification_channel(self, name: str) -> None:
        """Remove a notification channel.
        
        Args:
            name: Channel name to remove
        """
        with self._lock:
            if name in self.notification_channels:
                del self.notification_channels[name]
    
    def create_alert(self, name: str, severity: AlertSeverity, message: str,
                    source: str, details: Optional[Dict[str, Any]] = None,
                    labels: Optional[Dict[str, str]] = None) -> Alert:
        """Create a new alert.
        
        Args:
            name: Alert name
            severity: Alert severity
            message: Alert message
            source: Alert source
            details: Additional alert details
            labels: Alert labels
            
        Returns:
            Created alert
        """
        alert_id = f"{source}:{name}:{int(time.time())}"
        
        alert = Alert(
            id=alert_id,
            name=name,
            severity=severity,
            message=message,
            source=source,
            timestamp=time.time(),
            details=details or {},
            labels=labels or {}
        )
        
        with self._lock:
            self.active_alerts[alert_id] = alert
            self.alert_history.append(alert)
            self.alert_counts[name] += 1
            self.last_alert_time[name] = alert.timestamp
        
        # Send notifications
        self._send_notifications(alert)
        
        return alert
    
    def resolve_alert(self, alert_id: str, resolved_by: Optional[str] = None) -> bool:
        """Resolve an alert.
        
        Args:
            alert_id: Alert ID to resolve
            resolved_by: Who resolved the alert
            
        Returns:
            True if alert was resolved, False if not found
        """
        with self._lock:
            if alert_id in self.active_alerts:
                alert = self.active_alerts[alert_id]
                alert.status = AlertStatus.RESOLVED
                alert.resolved_at = time.time()
                
                # Move to history
                del self.active_alerts[alert_id]
                
                # Send resolution notification
                self._send_resolution_notification(alert, resolved_by)
                
                return True
        
        return False
    
    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge an alert.
        
        Args:
            alert_id: Alert ID to acknowledge
            acknowledged_by: Who acknowledged the alert
            
        Returns:
            True if alert was acknowledged, False if not found
        """
        with self._lock:
            if alert_id in self.active_alerts:
                alert = self.active_alerts[alert_id]
                alert.status = AlertStatus.ACKNOWLEDGED
                alert.acknowledged_at = time.time()
                alert.acknowledged_by = acknowledged_by
                
                return True
        
        return False
    
    def suppress_alert(self, alert_id: str, duration: int) -> bool:
        """Suppress an alert for a specified duration.
        
        Args:
            alert_id: Alert ID to suppress
            duration: Suppression duration in seconds
            
        Returns:
            True if alert was suppressed, False if not found
        """
        with self._lock:
            if alert_id in self.active_alerts:
                alert = self.active_alerts[alert_id]
                alert.status = AlertStatus.SUPPRESSED
                alert.suppressed_until = time.time() + duration
                
                return True
        
        return False
    
    def get_alerts(self, status: Optional[AlertStatus] = None,
                  severity: Optional[AlertSeverity] = None,
                  source: Optional[str] = None,
                  limit: Optional[int] = None) -> List[Alert]:
        """Get alerts with optional filtering.
        
        Args:
            status: Filter by status
            severity: Filter by severity
            source: Filter by source
            limit: Maximum number of alerts to return
            
        Returns:
            List of alerts
        """
        with self._lock:
            alerts = list(self.active_alerts.values())
        
        # Apply filters
        if status:
            alerts = [a for a in alerts if a.status == status]
        
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        
        if source:
            alerts = [a for a in alerts if a.source == source]
        
        # Sort by timestamp (newest first)
        alerts.sort(key=lambda a: a.timestamp, reverse=True)
        
        # Apply limit
        if limit:
            alerts = alerts[:limit]
        
        return alerts
    
    def get_alert_stats(self) -> Dict[str, Any]:
        """Get alert statistics.
        
        Returns:
            Alert statistics dictionary
        """
        with self._lock:
            active_alerts = list(self.active_alerts.values())
            total_alerts = len(self.alert_history)
        
        # Count by severity
        severity_counts = defaultdict(int)
        for alert in active_alerts:
            severity_counts[alert.severity.value] += 1
        
        # Count by status
        status_counts = defaultdict(int)
        for alert in active_alerts:
            status_counts[alert.status.value] += 1
        
        # Count by source
        source_counts = defaultdict(int)
        for alert in active_alerts:
            source_counts[alert.source] += 1
        
        return {
            'active_alerts': len(active_alerts),
            'total_alerts': total_alerts,
            'severity_counts': dict(severity_counts),
            'status_counts': dict(status_counts),
            'source_counts': dict(source_counts),
            'rules_count': len(self.rules),
            'channels_count': len(self.notification_channels)
        }
    
    def check_rules(self) -> List[Alert]:
        """Check all alert rules and create alerts if conditions are met.
        
        Returns:
            List of newly created alerts
        """
        new_alerts = []
        current_time = time.time()
        
        for rule_name, rule in self.rules.items():
            if not rule.enabled:
                continue
            
            try:
                # Check cooldown
                last_alert = self.last_alert_time.get(rule_name, 0)
                if current_time - last_alert < rule.cooldown:
                    continue
                
                # Check max alerts
                if self.alert_counts[rule_name] >= rule.max_alerts:
                    continue
                
                # Check condition
                if rule.condition():
                    alert = self.create_alert(
                        name=rule_name,
                        severity=rule.severity,
                        message=rule.message_template,
                        source=rule.source,
                        labels=rule.labels.copy()
                    )
                    new_alerts.append(alert)
                
                # Check auto-resolve
                elif rule.auto_resolve and rule.resolve_condition:
                    if rule.resolve_condition():
                        # Find and resolve related alerts
                        for alert_id, alert in list(self.active_alerts.items()):
                            if (alert.name == rule_name and 
                                alert.source == rule.source and
                                alert.status == AlertStatus.ACTIVE):
                                self.resolve_alert(alert_id, "auto-resolve")
                
            except Exception as e:
                self.logger.error(f"Error checking rule {rule_name}: {e}")
        
        return new_alerts
    
    def _send_notifications(self, alert: Alert) -> None:
        """Send notifications for an alert.
        
        Args:
            alert: Alert to send notifications for
        """
        # Find applicable notification channels
        rule = self.rules.get(alert.name)
        channels_to_notify = []
        
        if rule and rule.notification_channels:
            channels_to_notify = rule.notification_channels
        else:
            # Use default channels based on severity
            if alert.severity in [AlertSeverity.CRITICAL, AlertSeverity.EMERGENCY]:
                channels_to_notify = list(self.notification_channels.keys())
            else:
                channels_to_notify = ["log"]
        
        # Send notifications
        for channel_name in channels_to_notify:
            if channel_name in self.notification_channels:
                channel = self.notification_channels[channel_name]
                self._send_notification(alert, channel)
    
    def _send_notification(self, alert: Alert, channel: NotificationChannel) -> None:
        """Send notification through a specific channel.
        
        Args:
            alert: Alert to notify about
            channel: Notification channel to use
        """
        if not channel.enabled:
            return
        
        # Check rate limiting
        current_time = time.time()
        if (channel.last_notification and 
            current_time - channel.last_notification < channel.rate_limit):
            return
        
        try:
            if channel.type == "log":
                self._send_log_notification(alert, channel)
            elif channel.type == "email":
                self._send_email_notification(alert, channel)
            elif channel.type == "webhook":
                self._send_webhook_notification(alert, channel)
            
            channel.last_notification = current_time
            alert.notification_sent = True
            alert.last_notification = current_time
            
        except Exception as e:
            self.logger.error(f"Failed to send notification via {channel.name}: {e}")
    
    def _send_log_notification(self, alert: Alert, channel: NotificationChannel) -> None:
        """Send log notification.
        
        Args:
            alert: Alert to log
            channel: Log channel configuration
        """
        log_level = getattr(logging, channel.config.get('level', 'WARNING'))
        message = f"[ALERT] {alert.severity.value.upper()}: {alert.message} (Source: {alert.source})"
        self.logger.log(log_level, message)
    
    def _send_email_notification(self, alert: Alert, channel: NotificationChannel) -> None:
        """Send email notification.
        
        Args:
            alert: Alert to email
            channel: Email channel configuration
        """
        config = channel.config
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = config['from']
        msg['To'] = ', '.join(config['to'])
        msg['Subject'] = f"[{alert.severity.value.upper()}] {alert.name}"
        
        # Create body
        body = f"""
        Alert: {alert.name}
        Severity: {alert.severity.value.upper()}
        Source: {alert.source}
        Message: {alert.message}
        Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(alert.timestamp))}
        
        Details:
        {json.dumps(alert.details, indent=2)}
        
        Labels:
        {json.dumps(alert.labels, indent=2)}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        with smtplib.SMTP(config['smtp_server'], config.get('smtp_port', 587)) as server:
            if config.get('use_tls', True):
                server.starttls()
            if config.get('username') and config.get('password'):
                server.login(config['username'], config['password'])
            server.send_message(msg)
    
    def _send_webhook_notification(self, alert: Alert, channel: NotificationChannel) -> None:
        """Send webhook notification.
        
        Args:
            alert: Alert to send
            channel: Webhook channel configuration
        """
        import requests
        
        config = channel.config
        
        payload = {
            'alert_id': alert.id,
            'name': alert.name,
            'severity': alert.severity.value,
            'message': alert.message,
            'source': alert.source,
            'timestamp': alert.timestamp,
            'status': alert.status.value,
            'details': alert.details,
            'labels': alert.labels
        }
        
        headers = config.get('headers', {'Content-Type': 'application/json'})
        
        response = requests.post(
            config['url'],
            json=payload,
            headers=headers,
            timeout=config.get('timeout', 30)
        )
        response.raise_for_status()
    
    def _send_resolution_notification(self, alert: Alert, resolved_by: Optional[str]) -> None:
        """Send notification when alert is resolved.
        
        Args:
            alert: Resolved alert
            resolved_by: Who resolved the alert
        """
        message = f"Alert resolved: {alert.name}"
        if resolved_by:
            message += f" (by {resolved_by})"
        
        self.logger.info(message)
    
    def start_monitoring(self, interval: int = 60) -> None:
        """Start continuous alert monitoring.
        
        Args:
            interval: Monitoring interval in seconds
        """
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        
        def monitor_loop():
            while self.monitoring_active:
                try:
                    # Check rules
                    self.check_rules()
                    
                    # Clean up suppressed alerts
                    current_time = time.time()
                    for alert_id, alert in list(self.active_alerts.items()):
                        if (alert.status == AlertStatus.SUPPRESSED and
                            alert.suppressed_until and
                            current_time > alert.suppressed_until):
                            alert.status = AlertStatus.ACTIVE
                            alert.suppressed_until = None
                    
                    time.sleep(interval)
                    
                except Exception as e:
                    self.logger.error(f"Alert monitoring error: {e}")
                    time.sleep(interval)
        
        self.monitoring_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitoring_thread.start()
    
    def stop_monitoring(self) -> None:
        """Stop continuous alert monitoring."""
        self.monitoring_active = False
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5)


# Global alert manager instance
_global_alert_manager = None


def get_alert_manager() -> AlertManager:
    """Get global alert manager instance.
    
    Returns:
        Global AlertManager instance
    """
    global _global_alert_manager
    if _global_alert_manager is None:
        _global_alert_manager = AlertManager()
    return _global_alert_manager