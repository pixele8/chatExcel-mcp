# -*- coding: utf-8 -*-
"""
统一错误码标准 v1.0
实现改进.md中提出的标准化错误码体系

错误码分类：
- 文件访问错误：E001-E099
- 编码检测错误：E100-E199
- 列头解析错误：E200-E299
- 代码执行错误：E300-E399
- 性能优化错误：E400-E499
- 配置管理错误：E500-E599
- MCP工具错误：E600-E699
- 系统级错误：E700-E799

作者: AI Assistant
更新时间: 2024-12-19
版本: 1.0.0
"""

from enum import Enum
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import json
from datetime import datetime


class ErrorCode(Enum):
    """统一错误码枚举"""
    
    # 文件访问错误 E001-E099
    E001_FILE_NOT_FOUND = "E001"
    E002_FILE_PERMISSION_DENIED = "E002"
    E003_FILE_TOO_LARGE = "E003"
    E004_FILE_CORRUPTED = "E004"
    E005_FILE_LOCKED = "E005"
    E006_INVALID_FILE_PATH = "E006"
    E007_FILE_READ_ERROR = "E007"
    E008_FILE_WRITE_ERROR = "E008"
    E009_DIRECTORY_NOT_FOUND = "E009"
    E010_INSUFFICIENT_DISK_SPACE = "E010"
    
    # 编码检测错误 E100-E199
    E100_ENCODING_DETECTION_FAILED = "E100"
    E101_UNSUPPORTED_ENCODING = "E101"
    E102_ENCODING_CONVERSION_ERROR = "E102"
    E103_CHARSET_MISMATCH = "E103"
    E104_BOM_DETECTION_ERROR = "E104"
    E105_ENCODING_CACHE_ERROR = "E105"
    E106_FALLBACK_ENCODING_FAILED = "E106"
    E107_CHARDET_LIBRARY_ERROR = "E107"
    E108_ENCODING_VALIDATION_FAILED = "E108"
    E109_MIXED_ENCODING_DETECTED = "E109"
    
    # 列头解析错误 E200-E299
    E200_HEADER_NOT_FOUND = "E200"
    E201_MULTIHEADER_DETECTION_FAILED = "E201"
    E202_COLUMN_MAPPING_ERROR = "E202"
    E203_HEADER_STRUCTURE_INVALID = "E203"
    E204_COLUMN_NAME_CONFLICT = "E204"
    E205_HEADER_ROW_DETECTION_FAILED = "E205"
    E206_SEMANTIC_ANALYSIS_ERROR = "E206"
    E207_TABLE_PATTERN_MISMATCH = "E207"
    E208_COLUMN_TYPE_INFERENCE_FAILED = "E208"
    E209_HEADER_CACHE_CORRUPTION = "E209"
    
    # 代码执行错误 E300-E399
    E300_CODE_SYNTAX_ERROR = "E300"
    E301_CODE_EXECUTION_FAILED = "E301"
    E302_VARIABLE_NOT_DEFINED = "E302"
    E303_FUNCTION_NOT_FOUND = "E303"
    E304_IMPORT_ERROR = "E304"
    E305_SECURITY_VIOLATION = "E305"
    E306_TIMEOUT_ERROR = "E306"
    E307_MEMORY_LIMIT_EXCEEDED = "E307"
    E308_PANDAS_OPERATION_ERROR = "E308"
    E309_DATA_TYPE_ERROR = "E309"
    
    # 性能优化错误 E400-E499
    E400_PERFORMANCE_MONITORING_FAILED = "E400"
    E401_MEMORY_OPTIMIZATION_ERROR = "E401"
    E402_CACHE_OPERATION_FAILED = "E402"
    E403_CONCURRENT_PROCESSING_ERROR = "E403"
    E404_CHUNK_PROCESSING_FAILED = "E404"
    E405_PROFILING_ERROR = "E405"
    E406_RESOURCE_EXHAUSTION = "E406"
    E407_OPTIMIZATION_STRATEGY_FAILED = "E407"
    E408_PERFORMANCE_DEGRADATION = "E408"
    E409_PARALLEL_EXECUTION_ERROR = "E409"
    
    # 配置管理错误 E500-E599
    E500_CONFIG_FILE_NOT_FOUND = "E500"
    E501_CONFIG_PARSE_ERROR = "E501"
    E502_CONFIG_VALIDATION_FAILED = "E502"
    E503_CONFIG_WRITE_ERROR = "E503"
    E504_CONFIG_SCHEMA_MISMATCH = "E504"
    E505_CONFIG_MIGRATION_FAILED = "E505"
    E506_CONFIG_BACKUP_ERROR = "E506"
    E507_CONFIG_LOCK_ERROR = "E507"
    E508_CONFIG_PERMISSION_ERROR = "E508"
    E509_CONFIG_VERSION_CONFLICT = "E509"
    
    # MCP工具错误 E600-E699
    E600_MCP_TOOL_NOT_FOUND = "E600"
    E601_MCP_TOOL_REGISTRATION_FAILED = "E601"
    E602_MCP_TOOL_EXECUTION_ERROR = "E602"
    E603_MCP_PARAMETER_VALIDATION_FAILED = "E603"
    E604_MCP_RESPONSE_FORMAT_ERROR = "E604"
    E605_MCP_DEPENDENCY_MISSING = "E605"
    E606_MCP_VERSION_INCOMPATIBLE = "E606"
    E607_MCP_COMMUNICATION_ERROR = "E607"
    E608_MCP_TIMEOUT_ERROR = "E608"
    E609_MCP_AUTHENTICATION_FAILED = "E609"
    
    # 系统级错误 E700-E799
    E700_SYSTEM_ERROR = "E700"
    E701_DEPENDENCY_MISSING = "E701"
    E702_VERSION_INCOMPATIBLE = "E702"
    E703_ENVIRONMENT_ERROR = "E703"
    E704_NETWORK_ERROR = "E704"
    E705_DATABASE_ERROR = "E705"
    E706_AUTHENTICATION_ERROR = "E706"
    E707_AUTHORIZATION_ERROR = "E707"
    E708_SERVICE_UNAVAILABLE = "E708"
    E709_INTERNAL_SERVER_ERROR = "E709"


@dataclass
class ErrorDetail:
    """错误详情数据类"""
    code: str
    message: str
    description: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    category: str
    suggestions: List[str]
    timestamp: str
    context: Optional[Dict[str, Any]] = None
    traceback: Optional[str] = None


class ErrorCodeManager:
    """错误码管理器"""
    
    # 错误码详细信息映射
    ERROR_DETAILS = {
        # 文件访问错误
        ErrorCode.E001_FILE_NOT_FOUND: {
            "message": "文件未找到",
            "description": "指定的文件路径不存在或无法访问",
            "severity": "high",
            "category": "文件访问",
            "suggestions": ["检查文件路径是否正确", "确认文件是否存在", "检查文件权限"]
        },
        ErrorCode.E002_FILE_PERMISSION_DENIED: {
            "message": "文件权限被拒绝",
            "description": "没有足够的权限访问指定文件",
            "severity": "high",
            "category": "文件访问",
            "suggestions": ["检查文件权限设置", "以管理员身份运行", "联系系统管理员"]
        },
        ErrorCode.E003_FILE_TOO_LARGE: {
            "message": "文件过大",
            "description": "文件大小超过系统限制",
            "severity": "medium",
            "category": "文件访问",
            "suggestions": ["使用分块读取", "增加内存限制", "压缩文件"]
        },
        
        # 编码检测错误
        ErrorCode.E100_ENCODING_DETECTION_FAILED: {
            "message": "编码检测失败",
            "description": "无法自动检测文件编码格式",
            "severity": "medium",
            "category": "编码检测",
            "suggestions": ["手动指定编码格式", "使用UTF-8编码", "检查文件完整性"]
        },
        ErrorCode.E101_UNSUPPORTED_ENCODING: {
            "message": "不支持的编码格式",
            "description": "检测到的编码格式不被系统支持",
            "severity": "medium",
            "category": "编码检测",
            "suggestions": ["转换为UTF-8编码", "使用支持的编码格式", "安装额外的编码库"]
        },
        
        # 列头解析错误
        ErrorCode.E200_HEADER_NOT_FOUND: {
            "message": "列头未找到",
            "description": "无法在Excel文件中找到有效的列头",
            "severity": "high",
            "category": "列头解析",
            "suggestions": ["检查Excel文件格式", "手动指定列头行", "验证数据结构"]
        },
        ErrorCode.E201_MULTIHEADER_DETECTION_FAILED: {
            "message": "多级列头检测失败",
            "description": "无法正确识别多级列头结构",
            "severity": "medium",
            "category": "列头解析",
            "suggestions": ["简化列头结构", "手动指定列头参数", "使用单级列头"]
        },
        
        # 代码执行错误
        ErrorCode.E300_CODE_SYNTAX_ERROR: {
            "message": "代码语法错误",
            "description": "提供的代码包含语法错误",
            "severity": "high",
            "category": "代码执行",
            "suggestions": ["检查代码语法", "验证变量名", "确认函数调用正确"]
        },
        ErrorCode.E301_CODE_EXECUTION_FAILED: {
            "message": "代码执行失败",
            "description": "代码在运行时发生错误",
            "severity": "high",
            "category": "代码执行",
            "suggestions": ["检查数据类型", "验证变量是否存在", "添加异常处理"]
        },
        
        # MCP工具错误
        ErrorCode.E600_MCP_TOOL_NOT_FOUND: {
            "message": "MCP工具未找到",
            "description": "请求的MCP工具不存在或未注册",
            "severity": "high",
            "category": "MCP工具",
            "suggestions": ["检查工具名称", "确认工具已注册", "重启MCP服务"]
        },
        ErrorCode.E601_MCP_TOOL_REGISTRATION_FAILED: {
            "message": "MCP工具注册失败",
            "description": "工具注册到MCP服务器时发生错误",
            "severity": "critical",
            "category": "MCP工具",
            "suggestions": ["检查工具定义", "验证依赖项", "重启服务"]
        }
    }
    
    @classmethod
    def get_error_detail(cls, error_code: ErrorCode, 
                        context: Optional[Dict[str, Any]] = None,
                        custom_message: Optional[str] = None,
                        traceback_info: Optional[str] = None) -> ErrorDetail:
        """获取错误详情"""
        detail_info = cls.ERROR_DETAILS.get(error_code, {
            "message": "未知错误",
            "description": "发生了未定义的错误",
            "severity": "medium",
            "category": "未知",
            "suggestions": ["联系技术支持"]
        })
        
        return ErrorDetail(
            code=error_code.value,
            message=custom_message or detail_info["message"],
            description=detail_info["description"],
            severity=detail_info["severity"],
            category=detail_info["category"],
            suggestions=detail_info["suggestions"],
            timestamp=datetime.now().isoformat(),
            context=context,
            traceback=traceback_info
        )
    
    @classmethod
    def create_error_response(cls, error_code: ErrorCode, 
                            context: Optional[Dict[str, Any]] = None,
                            custom_message: Optional[str] = None,
                            traceback_info: Optional[str] = None) -> Dict[str, Any]:
        """创建标准化错误响应"""
        error_detail = cls.get_error_detail(error_code, context, custom_message, traceback_info)
        
        return {
            "success": False,
            "error": {
                "code": error_detail.code,
                "message": error_detail.message,
                "description": error_detail.description,
                "severity": error_detail.severity,
                "category": error_detail.category,
                "timestamp": error_detail.timestamp,
                "context": error_detail.context,
                "traceback": error_detail.traceback
            },
            "suggestions": error_detail.suggestions,
            "status": "ERROR"
        }
    
    @classmethod
    def get_error_by_category(cls, category: str) -> List[ErrorCode]:
        """根据类别获取错误码列表"""
        result = []
        for error_code, detail in cls.ERROR_DETAILS.items():
            if detail["category"] == category:
                result.append(error_code)
        return result
    
    @classmethod
    def get_error_statistics(cls) -> Dict[str, Any]:
        """获取错误码统计信息"""
        categories = {}
        severities = {}
        
        for error_code, detail in cls.ERROR_DETAILS.items():
            category = detail["category"]
            severity = detail["severity"]
            
            categories[category] = categories.get(category, 0) + 1
            severities[severity] = severities.get(severity, 0) + 1
        
        return {
            "total_errors": len(cls.ERROR_DETAILS),
            "categories": categories,
            "severities": severities,
            "coverage": {
                "file_access": "E001-E099",
                "encoding": "E100-E199", 
                "header_parsing": "E200-E299",
                "code_execution": "E300-E399",
                "performance": "E400-E499",
                "config": "E500-E599",
                "mcp_tools": "E600-E699",
                "system": "E700-E799"
            }
        }


# 便捷函数
def create_file_error(error_code: ErrorCode, file_path: str, 
                      additional_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """创建文件相关错误响应"""
    context = {"file_path": file_path}
    if additional_context:
        context.update(additional_context)
    return ErrorCodeManager.create_error_response(error_code, context)


def create_mcp_error(error_code: ErrorCode, tool_name: str, 
                     additional_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """创建MCP工具相关错误响应"""
    context = {"tool_name": tool_name}
    if additional_context:
        context.update(additional_context)
    return ErrorCodeManager.create_error_response(error_code, context)


def create_execution_error(error_code: ErrorCode, code_snippet: str,
                          error_message: str,
                          additional_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """创建代码执行相关错误响应"""
    context = {
        "code_snippet": code_snippet[:200] + "..." if len(code_snippet) > 200 else code_snippet,
        "error_message": error_message
    }
    if additional_context:
        context.update(additional_context)
    return ErrorCodeManager.create_error_response(error_code, context)