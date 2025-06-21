"""ChatExcel MCP 核心模块"""

__version__ = "2.1.0"
__author__ = "ChatExcel Team"

from .config import (
    Config,
    get_config,
    load_config,
    save_config,
    validate_config
)
from .exceptions import (
    ChatExcelError,
    ConfigurationError,
    ValidationError,
    ExecutionError,
    SecurityError,
    FileAccessError,
    CodeExecutionError,
    HealthCheckError,
    PerformanceError,
    SystemMonitorError,
    AlertError,
    SecurityViolationError,
    ExecutionTimeoutError,
    MemoryLimitError
)
from .types import (
    ExcelFileInfo,
    SheetInfo,
    CellRange,
    ValidationResult,
    ExecutionResult,
    FileOperationResult,
    HealthStatus,
    PerformanceMetric,
    SystemEvent,
    Alert,
    FileInfo,
    ExcelMetadata,
    CodeAnalysis
)

__all__ = [
    # Configuration
    "Config",
    "get_config",
    "load_config",
    "save_config",
    "validate_config",
    
    # Exceptions
    "ChatExcelError",
    "ConfigurationError",
    "ValidationError",
    "ExecutionError",
    "SecurityError",
    "FileAccessError",
    "CodeExecutionError",
    "HealthCheckError",
    "PerformanceError",
    "SystemMonitorError",
    "AlertError",
    
    # Types
    "ExcelFileInfo",
    "SheetInfo",
    "CellRange",
    "ValidationResult",
    "ExecutionResult",
    "FileOperationResult",
    "HealthStatus",
    "PerformanceMetric",
    "SystemEvent",
    "Alert",
    "FileInfo",
    "ExcelMetadata",
    "CodeAnalysis"
]