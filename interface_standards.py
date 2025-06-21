#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
接口标准化模块

定义Excel处理系统的标准接口：
- 统一的数据格式
- 标准化的API接口
- 输入输出规范
- 错误码标准
- 兼容性接口

作者: AI Assistant
创建时间: 2024-12-19
版本: 1.0.0
"""

import json
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union, Tuple, Protocol
from dataclasses import dataclass, asdict, field
from enum import Enum, IntEnum
from pathlib import Path

import pandas as pd
import numpy as np


class ProcessingStatus(Enum):
    """处理状态枚举"""
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class ErrorSeverity(IntEnum):
    """错误严重程度"""
    INFO = 0
    WARNING = 1
    ERROR = 2
    CRITICAL = 3
    FATAL = 4


class DataType(Enum):
    """数据类型枚举"""
    DATAFRAME = "dataframe"
    SERIES = "series"
    DICT = "dict"
    LIST = "list"
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    NULL = "null"


@dataclass
class ErrorInfo:
    """标准错误信息"""
    code: str
    message: str
    severity: ErrorSeverity = ErrorSeverity.ERROR
    details: Optional[Dict[str, Any]] = None
    timestamp: float = field(default_factory=time.time)
    traceback: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_exception(cls, error: Exception, code: str = "E999", severity: ErrorSeverity = ErrorSeverity.ERROR) -> 'ErrorInfo':
        """从异常创建错误信息"""
        import traceback
        return cls(
            code=code,
            message=str(error),
            severity=severity,
            details={'error_type': type(error).__name__},
            traceback=traceback.format_exc()
        )


@dataclass
class WarningInfo:
    """标准警告信息"""
    message: str
    category: str = "general"
    details: Optional[Dict[str, Any]] = None
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


@dataclass
class MetadataInfo:
    """标准元数据信息"""
    source_file: Optional[str] = None
    sheet_name: Optional[Union[str, int]] = None
    data_shape: Optional[Tuple[int, int]] = None
    column_count: Optional[int] = None
    row_count: Optional[int] = None
    data_types: Optional[Dict[str, str]] = None
    encoding: Optional[str] = None
    file_size: Optional[int] = None
    processing_time: Optional[float] = None
    memory_usage: Optional[float] = None
    has_multiheader: Optional[bool] = None
    header_rows: Optional[List[int]] = None
    data_quality_score: Optional[float] = None
    custom_metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {k: v for k, v in asdict(self).items() if v is not None}
    
    def update_from_dataframe(self, df: pd.DataFrame) -> None:
        """从DataFrame更新元数据"""
        self.data_shape = df.shape
        self.column_count = len(df.columns)
        self.row_count = len(df)
        self.data_types = {str(col): str(dtype) for col, dtype in df.dtypes.items()}
        self.memory_usage = df.memory_usage(deep=True).sum() / 1024 / 1024  # MB


@dataclass
class PerformanceMetrics:
    """标准性能指标"""
    operation_name: str
    start_time: float
    end_time: float
    duration: float
    memory_before: Optional[float] = None
    memory_after: Optional[float] = None
    memory_peak: Optional[float] = None
    cpu_usage: Optional[float] = None
    data_size: Optional[int] = None
    throughput: Optional[float] = None
    cache_hits: Optional[int] = None
    cache_misses: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {k: v for k, v in asdict(self).items() if v is not None}
    
    @property
    def memory_delta(self) -> Optional[float]:
        """内存变化量"""
        if self.memory_before is not None and self.memory_after is not None:
            return self.memory_after - self.memory_before
        return None


@dataclass
class StandardResponse:
    """标准响应格式"""
    success: bool
    status: ProcessingStatus
    data: Optional[Any] = None
    metadata: Optional[MetadataInfo] = None
    errors: List[ErrorInfo] = field(default_factory=list)
    warnings: List[WarningInfo] = field(default_factory=list)
    performance: Optional[PerformanceMetrics] = None
    request_id: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
    version: str = "1.0.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            'success': self.success,
            'status': self.status.value,
            'timestamp': self.timestamp,
            'version': self.version
        }
        
        if self.data is not None:
            if isinstance(self.data, pd.DataFrame):
                result['data'] = {
                    'type': DataType.DATAFRAME.value,
                    'shape': self.data.shape,
                    'columns': self.data.columns.tolist(),
                    'dtypes': {str(col): str(dtype) for col, dtype in self.data.dtypes.items()},
                    'sample_data': self.data.head().to_dict('records') if len(self.data) > 0 else [],
                    'memory_usage_mb': self.data.memory_usage(deep=True).sum() / 1024 / 1024
                }
            else:
                result['data'] = {
                    'type': self._detect_data_type(self.data).value,
                    'value': self.data
                }
        
        if self.metadata:
            result['metadata'] = self.metadata.to_dict()
        
        if self.errors:
            result['errors'] = [error.to_dict() for error in self.errors]
        
        if self.warnings:
            result['warnings'] = [warning.to_dict() for warning in self.warnings]
        
        if self.performance:
            result['performance'] = self.performance.to_dict()
        
        if self.request_id:
            result['request_id'] = self.request_id
        
        return result
    
    def _detect_data_type(self, data: Any) -> DataType:
        """检测数据类型"""
        if isinstance(data, pd.DataFrame):
            return DataType.DATAFRAME
        elif isinstance(data, pd.Series):
            return DataType.SERIES
        elif isinstance(data, dict):
            return DataType.DICT
        elif isinstance(data, list):
            return DataType.LIST
        elif isinstance(data, str):
            return DataType.STRING
        elif isinstance(data, (int, float)):
            return DataType.NUMBER
        elif isinstance(data, bool):
            return DataType.BOOLEAN
        elif data is None:
            return DataType.NULL
        else:
            return DataType.STRING  # 默认转为字符串
    
    def add_error(self, code: str, message: str, severity: ErrorSeverity = ErrorSeverity.ERROR, **kwargs) -> None:
        """添加错误"""
        error = ErrorInfo(code=code, message=message, severity=severity, details=kwargs)
        self.errors.append(error)
        if severity >= ErrorSeverity.ERROR:
            self.success = False
            if self.status == ProcessingStatus.PROCESSING:
                self.status = ProcessingStatus.FAILED
    
    def add_warning(self, message: str, category: str = "general", **kwargs) -> None:
        """添加警告"""
        warning = WarningInfo(message=message, category=category, details=kwargs)
        self.warnings.append(warning)
    
    def has_errors(self) -> bool:
        """是否有错误"""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """是否有警告"""
        return len(self.warnings) > 0
    
    def get_error_summary(self) -> str:
        """获取错误摘要"""
        if not self.errors:
            return "无错误"
        
        error_counts = {}
        for error in self.errors:
            severity = error.severity.name
            error_counts[severity] = error_counts.get(severity, 0) + 1
        
        return ", ".join([f"{severity}: {count}" for severity, count in error_counts.items()])


class ExcelProcessorInterface(Protocol):
    """Excel处理器接口协议"""
    
    def process_file(self, 
                    file_path: str, 
                    **kwargs) -> StandardResponse:
        """处理Excel文件"""
        ...
    
    def execute_code(self, 
                    data: pd.DataFrame, 
                    code: str, 
                    **kwargs) -> StandardResponse:
        """执行代码"""
        ...
    
    def detect_headers(self, 
                      file_path: str, 
                      **kwargs) -> StandardResponse:
        """检测列头"""
        ...
    
    def get_status(self) -> Dict[str, Any]:
        """获取状态"""
        ...


class BaseExcelProcessor(ABC):
    """Excel处理器基类"""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.request_counter = 0
    
    def _generate_request_id(self) -> str:
        """生成请求ID"""
        self.request_counter += 1
        return f"{self.name}_{int(time.time())}_{self.request_counter}"
    
    def _create_response(self, success: bool = True, status: ProcessingStatus = ProcessingStatus.SUCCESS) -> StandardResponse:
        """创建标准响应"""
        return StandardResponse(
            success=success,
            status=status,
            request_id=self._generate_request_id(),
            version=self.version
        )
    
    @abstractmethod
    def process_file(self, file_path: str, **kwargs) -> StandardResponse:
        """处理Excel文件"""
        pass
    
    def validate_file_path(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """验证文件路径"""
        if not file_path:
            return False, "文件路径不能为空"
        
        path = Path(file_path)
        if not path.exists():
            return False, f"文件不存在: {file_path}"
        
        if not path.is_file():
            return False, f"路径不是文件: {file_path}"
        
        valid_extensions = {'.xlsx', '.xls', '.csv', '.tsv'}
        if path.suffix.lower() not in valid_extensions:
            return False, f"不支持的文件格式: {path.suffix}"
        
        return True, None
    
    def validate_dataframe(self, df: pd.DataFrame) -> Tuple[bool, Optional[str]]:
        """验证DataFrame"""
        if df is None:
            return False, "DataFrame不能为None"
        
        if df.empty:
            return False, "DataFrame不能为空"
        
        return True, None


class CompatibilityAdapter:
    """兼容性适配器"""
    
    def __init__(self):
        self.legacy_mappings = {
            # 旧版本字段映射
            'dataframe': 'data',
            'info': 'metadata',
            'execution_time': 'performance.duration',
            'data_shape': 'metadata.data_shape'
        }
    
    def adapt_legacy_response(self, legacy_response: Dict[str, Any]) -> StandardResponse:
        """适配旧版本响应格式"""
        response = StandardResponse(
            success=legacy_response.get('success', False),
            status=ProcessingStatus.SUCCESS if legacy_response.get('success', False) else ProcessingStatus.FAILED
        )
        
        # 适配数据
        if 'dataframe' in legacy_response:
            response.data = legacy_response['dataframe']
        elif 'data' in legacy_response:
            response.data = legacy_response['data']
        
        # 适配元数据
        metadata = MetadataInfo()
        if 'info' in legacy_response:
            info = legacy_response['info']
            if isinstance(info, dict):
                for key, value in info.items():
                    if hasattr(metadata, key):
                        setattr(metadata, key, value)
        response.metadata = metadata
        
        # 适配错误和警告
        if 'errors' in legacy_response:
            errors = legacy_response['errors']
            if isinstance(errors, list):
                for error in errors:
                    if isinstance(error, str):
                        response.add_error("E999", error)
                    elif isinstance(error, dict):
                        response.add_error(
                            error.get('code', 'E999'),
                            error.get('message', str(error))
                        )
        
        if 'warnings' in legacy_response:
            warnings = legacy_response['warnings']
            if isinstance(warnings, list):
                for warning in warnings:
                    if isinstance(warning, str):
                        response.add_warning(warning)
                    elif isinstance(warning, dict):
                        response.add_warning(
                            warning.get('message', str(warning)),
                            warning.get('category', 'general')
                        )
        
        return response
    
    def adapt_to_legacy_format(self, response: StandardResponse) -> Dict[str, Any]:
        """适配为旧版本格式"""
        legacy_response = {
            'success': response.success,
            'dataframe': response.data if isinstance(response.data, pd.DataFrame) else None,
            'info': response.metadata.to_dict() if response.metadata else {},
            'errors': [error.message for error in response.errors],
            'warnings': [warning.message for warning in response.warnings]
        }
        
        # 添加性能信息
        if response.performance:
            legacy_response['execution_time'] = response.performance.duration
        
        return legacy_response


class APIValidator:
    """API验证器"""
    
    @staticmethod
    def validate_process_file_params(file_path: str, **kwargs) -> Tuple[bool, List[str]]:
        """验证处理文件参数"""
        errors = []
        
        # 验证文件路径
        if not isinstance(file_path, str):
            errors.append("file_path必须是字符串类型")
        elif not file_path.strip():
            errors.append("file_path不能为空")
        
        # 验证可选参数
        valid_params = {
            'sheet_name': (str, int, type(None)),
            'header': (int, list, type(None)),
            'skiprows': (int, list, type(None)),
            'nrows': (int, type(None)),
            'usecols': (str, list, type(None)),
            'dtype': (dict, type(None)),
            'na_values': (list, str, type(None)),
            'encoding': (str, type(None))
        }
        
        for param, value in kwargs.items():
            if param in valid_params:
                expected_types = valid_params[param]
                if not isinstance(value, expected_types):
                    errors.append(f"参数 {param} 类型错误，期望 {expected_types}，实际 {type(value)}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_execute_code_params(data: Any, code: str, **kwargs) -> Tuple[bool, List[str]]:
        """验证执行代码参数"""
        errors = []
        
        # 验证数据
        if not isinstance(data, pd.DataFrame):
            errors.append("data必须是pandas.DataFrame类型")
        
        # 验证代码
        if not isinstance(code, str):
            errors.append("code必须是字符串类型")
        elif not code.strip():
            errors.append("code不能为空")
        
        return len(errors) == 0, errors


class ResponseFormatter:
    """响应格式化器"""
    
    @staticmethod
    def format_json(response: StandardResponse, indent: int = 2) -> str:
        """格式化为JSON字符串"""
        return json.dumps(response.to_dict(), ensure_ascii=False, indent=indent, default=str)
    
    @staticmethod
    def format_summary(response: StandardResponse) -> str:
        """格式化为摘要字符串"""
        lines = [
            f"处理结果: {'成功' if response.success else '失败'}",
            f"状态: {response.status.value}",
            f"时间戳: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(response.timestamp))}"
        ]
        
        if response.metadata:
            if response.metadata.data_shape:
                lines.append(f"数据形状: {response.metadata.data_shape}")
            if response.metadata.processing_time:
                lines.append(f"处理时间: {response.metadata.processing_time:.2f}秒")
        
        if response.errors:
            lines.append(f"错误数量: {len(response.errors)}")
            for error in response.errors[:3]:  # 只显示前3个错误
                lines.append(f"  - {error.code}: {error.message}")
        
        if response.warnings:
            lines.append(f"警告数量: {len(response.warnings)}")
            for warning in response.warnings[:3]:  # 只显示前3个警告
                lines.append(f"  - {warning.message}")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_table(response: StandardResponse, max_rows: int = 10) -> str:
        """格式化为表格字符串"""
        if not isinstance(response.data, pd.DataFrame):
            return "数据不是DataFrame格式"
        
        df = response.data
        if len(df) > max_rows:
            return f"DataFrame形状: {df.shape}\n\n{df.head(max_rows).to_string()}\n\n... (显示前{max_rows}行，共{len(df)}行)"
        else:
            return f"DataFrame形状: {df.shape}\n\n{df.to_string()}"


# 标准错误码定义
class StandardErrorCodes:
    """标准错误码"""
    
    # 文件相关错误 (E001-E099)
    FILE_NOT_FOUND = "E001"
    FILE_ACCESS_DENIED = "E002"
    FILE_CORRUPTED = "E003"
    FILE_FORMAT_UNSUPPORTED = "E004"
    FILE_TOO_LARGE = "E005"
    
    # 编码相关错误 (E100-E199)
    ENCODING_DETECTION_FAILED = "E100"
    ENCODING_UNSUPPORTED = "E101"
    ENCODING_CONVERSION_ERROR = "E102"
    
    # 数据解析错误 (E200-E299)
    HEADER_DETECTION_FAILED = "E200"
    MULTIHEADER_PARSING_ERROR = "E201"
    COLUMN_MAPPING_ERROR = "E202"
    DATA_TYPE_ERROR = "E203"
    DATA_VALIDATION_ERROR = "E204"
    
    # 代码执行错误 (E300-E399)
    CODE_EXECUTION_ERROR = "E300"
    SYNTAX_ERROR = "E301"
    RUNTIME_ERROR = "E302"
    IMPORT_ERROR = "E303"
    VARIABLE_ERROR = "E304"
    
    # 系统错误 (E400-E499)
    MEMORY_ERROR = "E400"
    TIMEOUT_ERROR = "E401"
    PERMISSION_ERROR = "E402"
    RESOURCE_EXHAUSTED = "E403"
    
    # 参数错误 (E500-E599)
    INVALID_PARAMETER = "E500"
    MISSING_PARAMETER = "E501"
    PARAMETER_TYPE_ERROR = "E502"
    PARAMETER_VALUE_ERROR = "E503"
    
    # 未知错误 (E999)
    UNKNOWN_ERROR = "E999"


if __name__ == "__main__":
    # 测试标准接口
    response = StandardResponse(
        success=True,
        status=ProcessingStatus.SUCCESS,
        data=pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    )
    
    response.add_warning("这是一个测试警告")
    response.metadata = MetadataInfo(source_file="test.xlsx")
    response.metadata.update_from_dataframe(response.data)
    
    print("标准响应JSON格式:")
    print(ResponseFormatter.format_json(response))
    
    print("\n标准响应摘要格式:")
    print(ResponseFormatter.format_summary(response))
    
    print("\n接口标准化模块测试完成")