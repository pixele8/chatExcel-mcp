#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义异常类模块
定义ChatExcel MCP服务的所有异常类型
"""

from typing import Optional, Dict, Any, List

class ChatExcelError(Exception):
    """ChatExcel基础异常类"""
    
    def __init__(self, message: str, error_code: Optional[str] = None, 
                 details: Optional[Dict[str, Any]] = None, 
                 suggestions: Optional[List[str]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        self.suggestions = suggestions or []
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "error": self.error_code,
            "message": self.message,
            "details": self.details,
            "suggestions": self.suggestions,
            "type": self.__class__.__name__
        }

class FileAccessError(ChatExcelError):
    """文件访问异常"""
    
    def __init__(self, file_path: str, reason: str, **kwargs):
        message = f"文件访问失败: {file_path} - {reason}"
        details = {"file_path": file_path, "reason": reason}
        suggestions = [
            "检查文件路径是否正确",
            "确认文件是否存在",
            "验证文件访问权限"
        ]
        super().__init__(message, details=details, suggestions=suggestions, **kwargs)
        self.file_path = file_path
        self.reason = reason

class CodeExecutionError(ChatExcelError):
    """代码执行异常"""
    
    def __init__(self, code: str, error_details: str, **kwargs):
        message = f"代码执行失败: {error_details}"
        details = {"code": code, "error_details": error_details}
        suggestions = [
            "检查代码语法是否正确",
            "确认使用的变量和函数是否存在",
            "验证数据类型是否匹配"
        ]
        super().__init__(message, details=details, suggestions=suggestions, **kwargs)
        self.code = code
        self.error_details = error_details

class ValidationError(ChatExcelError):
    """参数验证异常"""
    
    def __init__(self, parameter: str, value: Any, expected: str, **kwargs):
        message = f"参数验证失败: {parameter} = {value}, 期望: {expected}"
        details = {
            "parameter": parameter,
            "value": str(value),
            "expected": expected
        }
        suggestions = [
            f"请提供有效的{parameter}参数",
            f"参数{parameter}应该{expected}"
        ]
        super().__init__(message, details=details, suggestions=suggestions, **kwargs)
        self.parameter = parameter
        self.value = value
        self.expected = expected

class SecurityError(ChatExcelError):
    """安全异常"""
    
    def __init__(self, operation: str, reason: str, **kwargs):
        message = f"安全检查失败: {operation} - {reason}"
        details = {"operation": operation, "reason": reason}
        suggestions = [
            "检查操作是否被允许",
            "确认安全策略配置",
            "联系管理员获取权限"
        ]
        super().__init__(message, details=details, suggestions=suggestions, **kwargs)
        self.operation = operation
        self.reason = reason

class ConfigurationError(ChatExcelError):
    """配置异常"""
    
    def __init__(self, config_key: str, issue: str, **kwargs):
        message = f"配置错误: {config_key} - {issue}"
        details = {"config_key": config_key, "issue": issue}
        suggestions = [
            "检查配置文件格式",
            "确认配置项是否正确",
            "参考默认配置示例"
        ]
        super().__init__(message, details=details, suggestions=suggestions, **kwargs)
        self.config_key = config_key
        self.issue = issue

class DataProcessingError(ChatExcelError):
    """数据处理异常"""
    
    def __init__(self, operation: str, data_info: str, error_details: str, **kwargs):
        message = f"数据处理失败: {operation} - {error_details}"
        details = {
            "operation": operation,
            "data_info": data_info,
            "error_details": error_details
        }
        suggestions = [
            "检查数据格式是否正确",
            "确认数据完整性",
            "尝试使用不同的处理参数"
        ]
        super().__init__(message, details=details, suggestions=suggestions, **kwargs)
        self.operation = operation
        self.data_info = data_info
        self.error_details = error_details

class ResourceError(ChatExcelError):
    """资源异常"""
    
    def __init__(self, resource_type: str, limit: str, current: str, **kwargs):
        message = f"资源限制: {resource_type} 超出限制 (当前: {current}, 限制: {limit})"
        details = {
            "resource_type": resource_type,
            "limit": limit,
            "current": current
        }
        suggestions = [
            "减少资源使用量",
            "优化处理策略",
            "联系管理员调整限制"
        ]
        super().__init__(message, details=details, suggestions=suggestions, **kwargs)
        self.resource_type = resource_type
        self.limit = limit
        self.current = current

class TimeoutError(ChatExcelError):
    """超时异常"""
    
    def __init__(self, operation: str, timeout: int, **kwargs):
        message = f"操作超时: {operation} (超时时间: {timeout}秒)"
        details = {"operation": operation, "timeout": timeout}
        suggestions = [
            "尝试减少数据量",
            "优化处理逻辑",
            "增加超时时间限制"
        ]
        super().__init__(message, details=details, suggestions=suggestions, **kwargs)
        self.operation = operation
        self.timeout = timeout

class CacheError(ChatExcelError):
    """缓存异常"""
    
    def __init__(self, cache_key: str, operation: str, reason: str, **kwargs):
        message = f"缓存操作失败: {operation} - {reason} (key: {cache_key})"
        details = {
            "cache_key": cache_key,
            "operation": operation,
            "reason": reason
        }
        suggestions = [
            "检查缓存配置",
            "清理缓存空间",
            "重试操作"
        ]
        super().__init__(message, details=details, suggestions=suggestions, **kwargs)
        self.cache_key = cache_key
        self.operation = operation
        self.reason = reason

class ServiceUnavailableError(ChatExcelError):
    """服务不可用异常"""
    
    def __init__(self, service_name: str, reason: str, **kwargs):
        message = f"服务不可用: {service_name} - {reason}"
        details = {"service_name": service_name, "reason": reason}
        suggestions = [
            "检查服务状态",
            "等待服务恢复",
            "联系技术支持"
        ]
        super().__init__(message, details=details, suggestions=suggestions, **kwargs)
        self.service_name = service_name
        self.reason = reason

class ExecutionError(ChatExcelError):
    """执行异常"""
    
    def __init__(self, operation: str, error_message: str, **kwargs):
        message = f"执行失败: {operation} - {error_message}"
        details = {"operation": operation, "error_message": error_message}
        suggestions = [
            "检查执行环境",
            "验证输入参数",
            "查看详细错误日志"
        ]
        super().__init__(message, details=details, suggestions=suggestions, **kwargs)
        self.operation = operation
        self.error_message = error_message

# 监控相关异常
class HealthCheckError(ChatExcelError):
    """健康检查异常"""
    
    def __init__(self, check_name: str, reason: str, **kwargs):
        message = f"健康检查失败: {check_name} - {reason}"
        details = {"check_name": check_name, "reason": reason}
        suggestions = [
            "检查系统资源",
            "验证服务状态",
            "查看监控日志"
        ]
        super().__init__(message, details=details, suggestions=suggestions, **kwargs)
        self.check_name = check_name
        self.reason = reason

class PerformanceError(ChatExcelError):
    """性能异常"""
    
    def __init__(self, metric: str, threshold: float, current: float, **kwargs):
        message = f"性能指标异常: {metric} 当前值 {current} 超过阈值 {threshold}"
        details = {"metric": metric, "threshold": threshold, "current": current}
        suggestions = [
            "优化系统性能",
            "调整性能阈值",
            "检查资源使用情况"
        ]
        super().__init__(message, details=details, suggestions=suggestions, **kwargs)
        self.metric = metric
        self.threshold = threshold
        self.current = current

class SystemMonitorError(ChatExcelError):
    """系统监控异常"""
    
    def __init__(self, monitor_type: str, error_details: str, **kwargs):
        message = f"系统监控异常: {monitor_type} - {error_details}"
        details = {"monitor_type": monitor_type, "error_details": error_details}
        suggestions = [
            "检查监控配置",
            "验证系统权限",
            "重启监控服务"
        ]
        super().__init__(message, details=details, suggestions=suggestions, **kwargs)
        self.monitor_type = monitor_type
        self.error_details = error_details

class AlertError(ChatExcelError):
    """Alert system error."""
    def __init__(self, alert_type: str, error_details: str):
        self.alert_type = alert_type
        self.error_details = error_details
        super().__init__(f"Alert error in {alert_type}: {error_details}")

class SecurityViolationError(ChatExcelError):
    """Security violation error."""
    def __init__(self, violation_type: str, details: str):
        self.violation_type = violation_type
        self.details = details
        super().__init__(f"Security violation ({violation_type}): {details}")

class ExecutionTimeoutError(ChatExcelError):
    """Execution timeout error."""
    def __init__(self, timeout_duration: int, operation: str):
        self.timeout_duration = timeout_duration
        self.operation = operation
        super().__init__(f"Operation '{operation}' timed out after {timeout_duration} seconds")

class MemoryLimitError(ChatExcelError):
    """Memory limit exceeded error."""
    def __init__(self, limit_mb: int, usage_mb: int):
        self.limit_mb = limit_mb
        self.usage_mb = usage_mb
        super().__init__(f"Memory limit exceeded: {usage_mb}MB used, limit is {limit_mb}MB")