#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
类型定义模块
定义ChatExcel MCP服务使用的数据类型
"""

from typing import Dict, Any, Optional, List, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
import pandas as pd

class ExecutionStatus(Enum):
    """执行状态枚举"""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"

class FileType(Enum):
    """文件类型枚举"""
    EXCEL = "excel"
    CSV = "csv"
    JSON = "json"
    HTML = "html"
    XML = "xml"
    UNKNOWN = "unknown"

class DataType(Enum):
    """数据类型枚举"""
    NUMERIC = "numeric"
    TEXT = "text"
    DATE = "date"
    BOOLEAN = "boolean"
    MIXED = "mixed"
    UNKNOWN = "unknown"

class OperationType(Enum):
    """操作类型枚举"""
    READ = "read"
    WRITE = "write"
    ANALYZE = "analyze"
    TRANSFORM = "transform"
    VALIDATE = "validate"
    VISUALIZE = "visualize"

@dataclass
class ExecutionResult:
    """代码执行结果"""
    status: ExecutionStatus
    result: Optional[Any] = None
    error: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    execution_time: Optional[float] = None
    memory_usage: Optional[int] = None
    output: Optional[str] = None
    variables: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "warnings": self.warnings,
            "execution_time": self.execution_time,
            "memory_usage": self.memory_usage,
            "output": self.output,
            "variables": self.variables,
            "metadata": self.metadata
        }

@dataclass
class FileInfo:
    """文件信息"""
    path: str
    name: str
    size: int
    type: FileType
    encoding: Optional[str] = None
    created_time: Optional[datetime] = None
    modified_time: Optional[datetime] = None
    checksum: Optional[str] = None
    permissions: Dict[str, bool] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "path": self.path,
            "name": self.name,
            "size": self.size,
            "type": self.type.value,
            "encoding": self.encoding,
            "created_time": self.created_time.isoformat() if self.created_time else None,
            "modified_time": self.modified_time.isoformat() if self.modified_time else None,
            "checksum": self.checksum,
            "permissions": self.permissions,
            "metadata": self.metadata
        }

@dataclass
class ExcelFileInfo:
    """Excel文件信息"""
    file_path: str
    file_size: int
    sheet_count: int
    total_rows: int
    total_columns: int
    encoding: str = "utf-8"
    last_modified: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "file_path": self.file_path,
            "file_size": self.file_size,
            "sheet_count": self.sheet_count,
            "total_rows": self.total_rows,
            "total_columns": self.total_columns,
            "encoding": self.encoding,
            "last_modified": self.last_modified.isoformat() if self.last_modified else None
        }

@dataclass
class SheetInfo:
    """工作表信息"""
    name: str
    index: int
    rows: int
    columns: int
    has_header: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "name": self.name,
            "index": self.index,
            "rows": self.rows,
            "columns": self.columns,
            "has_header": self.has_header
        }

@dataclass
class CellRange:
    """单元格范围"""
    start_row: int
    start_col: int
    end_row: int
    end_col: int
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "start_row": self.start_row,
            "start_col": self.start_col,
            "end_row": self.end_row,
            "end_col": self.end_col
        }

@dataclass
class ColumnInfo:
    """列信息"""
    name: str
    data_type: DataType
    null_count: int
    unique_count: int
    sample_values: List[Any] = field(default_factory=list)
    statistics: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "name": self.name,
            "data_type": self.data_type.value,
            "null_count": self.null_count,
            "unique_count": self.unique_count,
            "sample_values": self.sample_values,
            "statistics": self.statistics,
            "warnings": self.warnings,
            "suggestions": self.suggestions
        }

@dataclass
class FileOperationResult:
    """文件操作结果"""
    success: bool
    message: str
    file_path: Optional[str] = None
    operation: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "success": self.success,
            "message": self.message,
            "file_path": self.file_path,
            "operation": self.operation,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "metadata": self.metadata
        }

@dataclass
class ExcelMetadata:
    """Excel文件元数据"""
    file_info: FileInfo
    sheet_names: List[str]
    total_rows: int
    total_columns: int
    columns: List[ColumnInfo]
    data_quality_score: Optional[float] = None
    processing_recommendations: List[str] = field(default_factory=list)
    detected_issues: List[str] = field(default_factory=list)
    suggested_parameters: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "file_info": self.file_info.to_dict(),
            "sheet_names": self.sheet_names,
            "total_rows": self.total_rows,
            "total_columns": self.total_columns,
            "columns": [col.to_dict() for col in self.columns],
            "data_quality_score": self.data_quality_score,
            "processing_recommendations": self.processing_recommendations,
            "detected_issues": self.detected_issues,
            "suggested_parameters": self.suggested_parameters
        }

@dataclass
class CodeAnalysis:
    """代码分析结果"""
    variables_used: List[str]
    functions_called: List[str]
    modules_imported: List[str]
    security_issues: List[str] = field(default_factory=list)
    performance_warnings: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    complexity_score: Optional[float] = None
    estimated_execution_time: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "variables_used": self.variables_used,
            "functions_called": self.functions_called,
            "modules_imported": self.modules_imported,
            "security_issues": self.security_issues,
            "performance_warnings": self.performance_warnings,
            "suggestions": self.suggestions,
            "complexity_score": self.complexity_score,
            "estimated_execution_time": self.estimated_execution_time
        }

@dataclass
class CacheEntry:
    """缓存条目"""
    key: str
    value: Any
    created_time: datetime
    last_accessed: datetime
    access_count: int = 0
    ttl: Optional[int] = None
    size: Optional[int] = None
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        if self.ttl is None:
            return False
        return (datetime.now() - self.created_time).total_seconds() > self.ttl
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "key": self.key,
            "created_time": self.created_time.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
            "access_count": self.access_count,
            "ttl": self.ttl,
            "size": self.size
        }

@dataclass
class HealthStatus:
    """健康状态"""
    service_name: str
    status: str  # healthy, unhealthy, degraded
    timestamp: datetime
    checks: Dict[str, bool] = field(default_factory=dict)
    metrics: Dict[str, float] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "service_name": self.service_name,
            "status": self.status,
            "timestamp": self.timestamp.isoformat(),
            "checks": self.checks,
            "metrics": self.metrics,
            "errors": self.errors,
            "warnings": self.warnings
        }

@dataclass
class ProcessingTask:
    """处理任务"""
    task_id: str
    operation: OperationType
    file_path: str
    parameters: Dict[str, Any]
    status: ExecutionStatus
    created_time: datetime
    started_time: Optional[datetime] = None
    completed_time: Optional[datetime] = None
    progress: float = 0.0
    result: Optional[ExecutionResult] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "task_id": self.task_id,
            "operation": self.operation.value,
            "file_path": self.file_path,
            "parameters": self.parameters,
            "status": self.status.value,
            "created_time": self.created_time.isoformat(),
            "started_time": self.started_time.isoformat() if self.started_time else None,
            "completed_time": self.completed_time.isoformat() if self.completed_time else None,
            "progress": self.progress,
            "result": self.result.to_dict() if self.result else None
        }

@dataclass
class PerformanceMetric:
    """Performance metric data structure."""
    name: str
    value: float
    unit: str
    timestamp: float
    tags: Dict[str, str] = field(default_factory=dict)

@dataclass
class SystemEvent:
    """System event data structure."""
    timestamp: float
    event_type: str
    severity: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

# Alert system types
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

# Type aliases for common patterns
DataFrameType = pd.DataFrame
SeriesType = pd.Series
PathType = Union[str, Path]
ConfigType = Dict[str, Any]
MetricsType = Dict[str, Union[int, float, str]]

# 类型别名
DataFrame = pd.DataFrame
Series = pd.Series
ExcelReadParams = Dict[str, Union[str, int, bool, List[str]]]
ProcessingConfig = Dict[str, Any]
ValidationResult = Dict[str, Any]
ChartConfig = Dict[str, Any]
SecurityContext = Dict[str, Any]