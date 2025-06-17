from mcp.server.fastmcp import FastMCP
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import base64
import os
from chardet import detect
import traceback
from io import StringIO
import sys
import time
from textwrap import wrap
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
from excel_helper import _suggest_excel_read_parameters, detect_excel_structure
# 导入Excel智能工具
from excel_smart_tools import suggest_excel_read_parameters, detect_excel_file_structure, create_excel_read_template
from enhanced_excel_helper import smart_read_excel, detect_file_encoding, validate_excel_data_integrity
from comprehensive_data_verification import ComprehensiveDataVerifier
from data_verification import verify_data_processing_result, DataVerificationEngine
from excel_enhanced_tools import ExcelEnhancedProcessor, get_excel_processor
# 导入 Excel 公式处理工具
from formulas_tools import (
    parse_excel_formula,
    compile_excel_workbook,
    execute_excel_formula,
    analyze_excel_dependencies,
    validate_excel_formula
)
# 导入 Excel 数据质量工具
from excel_data_quality_tools import (
    ExcelDataQualityController,
    ExcelCellContentExtractor,
    ExcelCharacterConverter,
    ExcelMultiConditionExtractor,
    ExcelMultiTableMerger,
    ExcelDataCleaner,
    ExcelBatchProcessor
)

# 统一常量定义 - 降低安全限制
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB
BLACKLIST = ['subprocess.']  # 大幅减少黑名单，完全解除tabulate库限制
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
CHARTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")

# 初始化数据质量工具实例
data_quality_controller = ExcelDataQualityController()
cell_content_extractor = ExcelCellContentExtractor()
character_converter = ExcelCharacterConverter()
multi_condition_extractor = ExcelMultiConditionExtractor()
multi_table_merger = ExcelMultiTableMerger()
data_cleaner = ExcelDataCleaner()
batch_processor = ExcelBatchProcessor()

# 错误类型常量
ERROR_TYPES = {
    "FILE_NOT_FOUND": "指定的文件未找到",
    "FILE_TOO_LARGE": "文件大小超过最大限制",
    "TEMPLATE_ERROR": "模板处理失败",
    "SECURITY_VIOLATION": "操作因安全原因被阻止",
    "VALIDATION_ERROR": "输入验证失败",
    "PROCESSING_ERROR": "数据处理失败"
}

mcp = FastMCP("chatExcel")

# 工具函数
def create_error_response(error_type: str, message: str, details: dict = None, solutions: list = None) -> dict:
    """创建统一格式的错误响应
    
    Args:
        error_type: 错误类型
        message: 错误消息
        details: 错误详情
        solutions: 解决方案建议
        
    Returns:
        dict: 标准化错误响应
    """
    response = {
        "status": "ERROR",
        "error_type": error_type,
        "message": message,
        "timestamp": time.time()
    }
    
    if details:
        response["details"] = details
    if solutions:
        response["solutions"] = solutions
        
    return response

def create_success_response(data: dict, message: str = "操作成功完成") -> dict:
    """创建统一格式的成功响应
    
    Args:
        data: 响应数据
        message: 成功消息
        
    Returns:
        dict: 标准化成功响应
    """
    return {
        "status": "SUCCESS",
        "message": message,
        "data": data,
        "timestamp": time.time()
    }

def get_template_path(template_name: str) -> str:
    """获取模板文件的绝对路径
    
    Args:
        template_name: 模板文件名
        
    Returns:
        str: 模板文件绝对路径
        
    Raises:
        FileNotFoundError: 模板文件不存在
    """
    template_path = os.path.join(TEMPLATE_DIR, template_name)
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"模板文件未找到: {template_path}")
    
    return template_path

def validate_file_access(file_path: str) -> dict:
    """验证文件访问权限和大小
    
    Args:
        file_path: 文件路径
        
    Returns:
        dict: 验证结果，包含status和相关信息
    """
    if not os.path.exists(file_path):
        return create_error_response(
            "FILE_NOT_FOUND", 
            f"文件不存在: {file_path}",
            solutions=["检查文件路径是否正确", "确保文件存在且可访问"]
        )

    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE:
        return create_error_response(
            "FILE_TOO_LARGE",
            f"文件过大: {file_size / (1024*1024):.1f}MB (最大: {MAX_FILE_SIZE / (1024*1024)}MB)",
            details={"actual_size": file_size, "max_size": MAX_FILE_SIZE},
            solutions=["使用较小的文件", "分块处理数据"]
        )
    
    return {"status": "SUCCESS", "file_size": file_size}

import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatExcel.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@mcp.tool()
def read_metadata(file_path: str) -> dict:
    """读取CSV文件元数据并返回MCP兼容格式
    
    Args:
        file_path: CSV文件的绝对路径
        
    Returns:
        dict: 包含列信息、文件信息和状态的结构化元数据
    """
    logger.info(f"开始读取文件元数据: {file_path}")
    
    try:
        # 验证文件访问
        validation_result = validate_file_access(file_path)
        if validation_result["status"] != "SUCCESS":
            return validation_result
        
        # Detect encoding and delimiter
        with open(file_path, 'rb') as f:
            rawdata = f.read(50000)
            enc = detect(rawdata)['encoding'] or 'utf-8'

        with open(file_path, 'r', encoding=enc) as f:
            first_line = f.readline()
            delimiter = ',' if ',' in first_line else '\t' if '\t' in first_line else ';'

        # 获取文件大小
        file_size = validation_result["file_size"]
        
        # Get actual row count efficiently
        try:
            # Count total rows without loading data
            total_rows = sum(1 for _ in open(file_path, 'r', encoding=enc)) - 1  # -1 for header
        except Exception:
            # Fallback: use pandas to count rows
            # Read only first column to count rows efficiently
            temp_df = pd.read_csv(file_path, encoding=enc, delimiter=delimiter, usecols=[0])
            total_rows = len(temp_df)
        
        # Check file size limit
        if file_size > MAX_FILE_SIZE:
            return {
                "status": "ERROR",
                "error": "FILE_TOO_LARGE",
                "max_size": f"{MAX_FILE_SIZE / 1024 / 1024}MB",
                "actual_size": f"{file_size / 1024 / 1024:.1f}MB"
            }
        
        # Read sample data for metadata analysis
        sample_size = min(100, total_rows)
        df = pd.read_csv(file_path, encoding=enc, delimiter=delimiter, nrows=sample_size)

        # Calculate additional metadata
        columns_metadata = []
        for col in df.columns:
            col_meta = {
                "name": col,
                "type": str(df[col].dtype),
                "sample": df[col].dropna().iloc[:2].tolist(),
                "stats": {
                    "null_count": df[col].isnull().sum(),
                    "unique_count": df[col].nunique(),
                    "is_numeric": pd.api.types.is_numeric_dtype(df[col])
                },
                "warnings": [],
                "suggested_operations": []
            }
            
            # Add numeric stats if applicable
            if pd.api.types.is_numeric_dtype(df[col]):
                col_meta["stats"].update({
                    "min": df[col].min(),
                    "max": df[col].max(),
                    "mean": df[col].mean(),
                    "std": df[col].std()
                })
                col_meta["suggested_operations"].extend([
                    "normalize", "scale", "log_transform"
                ])
            
            # Add categorical stats if applicable
            if pd.api.types.is_string_dtype(df[col]):
                col_meta["suggested_operations"].extend([
                    "one_hot_encode", "label_encode", "text_processing"
                ])
            
            # Add datetime detection
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                col_meta["suggested_operations"].extend([
                    "extract_year", "extract_month", "time_delta"
                ])
            
            # Add warnings
            if df[col].isnull().sum() > 0:
                col_meta["warnings"].append(f"{df[col].isnull().sum()} null values found")
            if df[col].nunique() == 1:
                col_meta["warnings"].append("Column contains only one unique value")
            if pd.api.types.is_numeric_dtype(df[col]) and df[col].abs().max() > 1e6:
                col_meta["warnings"].append("Large numeric values detected - consider scaling")
            
            columns_metadata.append(col_meta)

        from pandas.api.types import infer_dtype
        
        # Format concise response
        summary = {
            "status": "SUCCESS",
            "file_info": {
                "size": f"{file_size / 1024:.1f}KB",
                "encoding": enc,
                "delimiter": delimiter
            },
            "dataset": {
                "total_rows": total_rows,
                "sample_rows": len(df),
                "columns": len(df.columns),
                "column_types": {
                    col: infer_dtype(df[col])
                    for col in df.columns
                }
            },
            "warnings": {
                "message": "Data quality issues detected" if (
                    df.isnull().any().any() or 
                    df.duplicated().any() or
                    (df.nunique() == 1).any()
                ) else "No significant data quality issues found",
                **({
                    "null_columns": {
                        "count": sum(df.isnull().any()),
                        "columns": [col for col in df.columns if df[col].isnull().any()]
                    }
                } if sum(df.isnull().any()) > 0 else {}),
                **({
                    "total_nulls": df.isnull().sum().sum()
                } if df.isnull().sum().sum() > 0 else {}),
                **({
                    "duplicate_rows": {
                        "count": df.duplicated().sum(),
                        "rows": df[df.duplicated()].index.tolist()
                    }
                } if df.duplicated().sum() > 0 else {}),
                **({
                    "single_value_columns": {
                        "count": sum(df.nunique() == 1),
                        "columns": [col for col in df.columns if df[col].nunique() == 1]
                    }
                } if sum(df.nunique() == 1) > 0 else {})
            }
        }
            
        return summary

    except Exception as e:
        return {
            "status": "ERROR",
            "error_type": type(e).__name__,
            "message": str(e),
            "solution": [
                "Check if the file is being used by another program",
                "Try saving the file as UTF-8 encoded CSV",
                "Contact the administrator to check MCP file access permissions"
            ],
            "traceback": traceback.format_exc()
        }




@mcp.tool()
def verify_data_integrity(original_file: str, processed_data: Optional[str] = None, 
                         comparison_file: Optional[str] = None, verification_type: str = "basic") -> dict:
    """数据完整性验证和比对核准工具。
    
    Args:
        original_file: 原始Excel文件路径
        processed_data: 处理后的数据（JSON字符串格式）或文件路径
        comparison_file: 用于比较的另一个Excel文件路径（可选）
        verification_type: 验证类型 ("basic", "detailed", "statistical")
    
    Returns:
        dict: 验证结果报告
    """
    try:
        from data_verification import DataVerificationEngine, verify_data_processing_result
        
        # 验证原始文件访问
        validation_result = validate_file_access(original_file)
        if validation_result["status"] != "SUCCESS":
            return {
                "success": False,
                "error": validation_result["message"],
                "suggestion": "请确保原始文件路径正确且文件存在。"
            }
        
        # 创建验证引擎
        verifier = DataVerificationEngine()
        
        if comparison_file:
            # 文件对比模式
            validation_result2 = validate_file_access(comparison_file)
            if validation_result2["status"] != "SUCCESS":
                return {
                    "success": False,
                    "error": f"比较文件访问失败: {validation_result2['message']}",
                    "suggestion": "请确保比较文件路径正确且文件存在。"
                }
            
            # 读取两个文件进行比较
            df1 = pd.read_excel(original_file)
            df2 = pd.read_excel(comparison_file)
            
            comparison_result = verifier.compare_dataframes(
                df1, df2, 
                name1=os.path.basename(original_file),
                name2=os.path.basename(comparison_file)
            )
            
            # 添加增强的数据质量检查
            quality_result1 = data_quality_controller.comprehensive_quality_check(
                original_file, "comprehensive"
            )
            quality_result2 = data_quality_controller.comprehensive_quality_check(
                comparison_file, "comprehensive"
            )
            
            comparison_result["enhanced_quality_analysis"] = {
                "original_file_quality": quality_result1,
                "comparison_file_quality": quality_result2,
                "quality_comparison": {
                    "score_difference": quality_result1.get("overall_score", 0) - quality_result2.get("overall_score", 0),
                    "better_quality_file": "original" if quality_result1.get("overall_score", 0) > quality_result2.get("overall_score", 0) else "comparison"
                }
            }
            
            return {
                "success": True,
                "verification_type": "file_comparison",
                "comparison_result": comparison_result,
                "summary": {
                    "files_compared": [original_file, comparison_file],
                    "match_score": comparison_result.get("match_score", 0),
                    "has_differences": comparison_result.get("has_differences", True)
                }
            }
        
        elif processed_data:
            # 数据处理结果验证模式
            try:
                # 尝试解析处理后的数据
                if isinstance(processed_data, str):
                    if processed_data.endswith(('.xlsx', '.xls', '.csv')):
                        # 如果是文件路径
                        if processed_data.endswith('.csv'):
                            processed_df = pd.read_csv(processed_data)
                        else:
                            processed_df = pd.read_excel(processed_data)
                    else:
                        # 如果是JSON字符串
                        import json
                        data_dict = json.loads(processed_data)
                        processed_df = pd.DataFrame(data_dict)
                else:
                    return {
                        "success": False,
                        "error": "处理后数据格式不支持",
                        "suggestion": "请提供JSON字符串、CSV或Excel文件路径。"
                    }
                
                # 执行验证
                verification_result = verify_data_processing_result(
                    original_file, processed_df, verification_type
                )
                
                return {
                    "success": True,
                    "verification_type": "processing_verification",
                    "verification_result": verification_result
                }
                
            except Exception as parse_error:
                return {
                    "success": False,
                    "error": f"数据解析失败: {str(parse_error)}",
                    "suggestion": "请检查处理后数据的格式是否正确。"
                }
        
        else:
            # 基础完整性检查模式
            df = pd.read_excel(original_file)
            
            # 执行基础完整性检查
            integrity_report = {
                "file_info": {
                    "path": original_file,
                    "shape": df.shape,
                    "columns": list(df.columns),
                    "dtypes": df.dtypes.to_dict()
                },
                "data_quality": {
                    "total_rows": len(df),
                    "total_columns": len(df.columns),
                    "null_counts": df.isnull().sum().to_dict(),
                    "null_percentage": (df.isnull().sum() / len(df) * 100).to_dict(),
                    "duplicate_rows": df.duplicated().sum(),
                    "memory_usage": df.memory_usage(deep=True).to_dict()
                },
                "column_analysis": {}
            }
            
            # 详细列分析
            for col in df.columns:
                col_info = {
                    "dtype": str(df[col].dtype),
                    "null_count": df[col].isnull().sum(),
                    "unique_count": df[col].nunique(),
                    "sample_values": df[col].dropna().head(3).tolist()
                }
                
                if df[col].dtype in ['int64', 'float64']:
                    col_info.update({
                        "min": df[col].min(),
                        "max": df[col].max(),
                        "mean": df[col].mean(),
                        "std": df[col].std()
                    })
                
                integrity_report["column_analysis"][col] = col_info
            
            return {
                "success": True,
                "verification_type": "integrity_check",
                "integrity_report": integrity_report
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": type(e).__name__,
                "message": str(e),
                "traceback": traceback.format_exc()
            },
            "suggestion": "请检查输入参数和文件格式是否正确。"
        }

@mcp.tool()
def read_excel_metadata(file_path: str) -> dict:
    """增强版Excel文件元数据读取，支持智能编码检测和完整性验证。
    
    Args:
        file_path: Excel文件路径
    
    Returns:
        dict: 包含文件元数据、编码信息、完整性验证结果的字典
    """
    try:
        # 验证文件访问
        validation_result = validate_file_access(file_path)
        if validation_result["status"] != "SUCCESS":
            return validation_result

        # 智能编码检测
        encoding_info = detect_file_encoding(file_path)
        
        # 使用智能读取功能
        read_result = smart_read_excel(file_path, sample_size=100)
        if not read_result['success']:
            return {
                "status": "ERROR",
                "error": "SMART_READ_FAILED",
                "message": read_result.get('error', '智能读取失败'),
                "encoding_info": encoding_info
            }
        
        df = read_result['dataframe']  # 修复：使用正确的键名
        read_params = read_result.get('info', {}).get('read_params', {})  # 修复：获取正确的参数信息
        
        # 数据完整性验证
        integrity_result = validate_excel_data_integrity(file_path, df)
        
        # 增强的数据质量检查
        quality_result = data_quality_controller.comprehensive_quality_check(
            file_path, "comprehensive"
        )
        
        # 高级单元格内容分析
        cell_analysis = cell_content_extractor.extract_cell_content_advanced(
            file_path, extract_type="all"
        )
        
        # 获取所有工作表信息
        workbook = openpyxl.load_workbook(file_path, read_only=True)
        sheet_names = workbook.sheetnames
        sheets_info = {}
        
        for sheet_name in sheet_names:
            sheet_obj = workbook[sheet_name]
            sheets_info[sheet_name] = {
                'max_row': sheet_obj.max_row,
                'max_column': sheet_obj.max_column,
                'has_data': sheet_obj.max_row > 1
            }
        workbook.close()
        
        # 智能参数推荐（使用增强版）
        suggested_params = _suggest_excel_read_parameters(file_path, read_params.get('sheet_name'))

        columns_metadata = []
        for col in df.columns:
            col_meta = {
                "name": col,
                "type": str(df[col].dtype),
                "sample": df[col].dropna().iloc[:2].tolist(),
                "stats": {
                    "null_count": df[col].isnull().sum(),
                    "unique_count": df[col].nunique(),
                    "is_numeric": pd.api.types.is_numeric_dtype(df[col])
                },
                "warnings": [],
                "suggested_operations": []
            }
            if pd.api.types.is_numeric_dtype(df[col]):
                col_meta["stats"].update({
                    "min": df[col].min(),
                    "max": df[col].max(),
                    "mean": df[col].mean(),
                    "std": df[col].std()
                })
                col_meta["suggested_operations"].extend([
                    "normalize", "scale", "log_transform"
                ])
            if pd.api.types.is_string_dtype(df[col]):
                col_meta["suggested_operations"].extend([
                    "one_hot_encode", "label_encode", "text_processing"
                ])
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                col_meta["suggested_operations"].extend([
                    "extract_year", "extract_month", "time_delta"
                ])
            if df[col].isnull().sum() > 0:
                col_meta["warnings"].append(f"{df[col].isnull().sum()} null values found")
            if df[col].nunique() == 1:
                col_meta["warnings"].append("Column contains only one unique value")
            if pd.api.types.is_numeric_dtype(df[col]) and df[col].abs().max() > 1e6:
                col_meta["warnings"].append("Large numeric values detected - consider scaling")
            columns_metadata.append(col_meta)

        summary = {
            "status": "SUCCESS",
            "file_info": {
                "size": f"{validation_result['file_size'] / 1024:.1f}KB",
                "sheets": sheet_names,
                "sheets_info": sheets_info,
                "encoding": encoding_info
            },
            "dataset": {
                "total_rows": read_result.get('total_rows', len(df)),
                "sample_rows": len(df),
                "columns": len(df.columns),
                "column_types": {
                    col: str(df[col].dtype)
                    for col in df.columns
                }
            },
            "read_params": read_params,
            "suggested_params": suggested_params,
            "columns_metadata": columns_metadata,
            "integrity_check": integrity_result,
            "enhanced_quality_analysis": quality_result,
            "cell_content_analysis": cell_analysis,
            "warnings": {
                "message": "Data quality issues detected" if (
                    df.isnull().any().any() or 
                    df.duplicated().any() or
                    (df.nunique() == 1).any()
                ) else "No significant data quality issues found",
                **({
                    "null_columns": {
                        "count": sum(df.isnull().any()),
                        "columns": [col for col in df.columns if df[col].isnull().any()]
                    }
                } if sum(df.isnull().any()) > 0 else {}),
                **({
                    "total_nulls": df.isnull().sum().sum()
                } if df.isnull().sum().sum() > 0 else {}),
                **({
                    "duplicate_rows": {
                        "count": df.duplicated().sum(),
                        "rows": df[df.duplicated()].index.tolist()
                    }
                } if df.duplicated().sum() > 0 else {}),
                **({
                    "single_value_columns": {
                        "count": sum(df.nunique() == 1),
                        "columns": [col for col in df.columns if df[col].nunique() == 1]
                    }
                } if sum(df.nunique() == 1) > 0 else {})
            }
        }
        return summary

    except Exception as e:
        return {
            "status": "ERROR",
            "error_type": type(e).__name__,
            "message": str(e),
            "solution": [
                "Ensure the file is a valid Excel file (.xlsx)",
                "Check if the file is being used by another program",
                "Contact the administrator to check MCP file access permissions"
            ],
            "traceback": traceback.format_exc()
        }



@mcp.tool()
def run_excel_code(
    file_path: str,
    code: str, 
    sheet_name: str = None, 
    skiprows: int = None, 
    header: int = None, 
    usecols: str = None, 
    encoding: str = None,
    auto_detect: bool = True,
    allow_file_write: bool = False
) -> dict:
    """增强版Excel代码执行工具，具备强化的pandas导入和错误处理机制。
    
    Args:
        code: 要执行的数据处理代码字符串
        file_path: Excel文件路径
        sheet_name: 可选，工作表名称
        skiprows: 可选，跳过的行数
        header: 可选，用作列名的行号。可以是整数、整数列表或None
        usecols: 可选，要解析的列。可以是列名列表、列索引列表或字符串
        encoding: 指定编码（可选，自动检测时忽略）
        auto_detect: 是否启用智能检测和参数优化
        allow_file_write: 是否允许在代码中写入文件
        
    Returns:
        dict: 执行结果或错误信息
    """
    
    # 增强的安全检查
    security_blacklist = BLACKLIST.copy()
    if not allow_file_write:
        # 如果不允许文件写入，添加更多限制
        security_blacklist.extend([
            'to_excel(', 'to_csv(', 'to_json(', 'to_pickle(',
            '.save(', '.write(', 'open(', 'with open('
        ])
    
    for forbidden in security_blacklist:
        if forbidden in code:
            return {
                "error": {
                    "type": "SECURITY_VIOLATION",
                    "message": f"Forbidden operation detected: {forbidden}",
                    "solution": "Remove restricted operations from your code" + 
                               (" or set allow_file_write=True" if not allow_file_write and 
                                forbidden in ['to_excel(', 'to_csv(', 'to_json(', 'to_pickle(', '.save(', '.write(', 'open(', 'with open('] else "")
                }
            }

    # 验证文件访问
    validation_result = validate_file_access(file_path)
    if validation_result["status"] != "SUCCESS":
        return {
            "error": {
                "type": "FILE_ACCESS_ERROR",
                "message": validation_result["message"],
                "solution": "请确保文件路径正确且文件存在。"
            }
        }

    # 增强的模块导入机制
    def safe_import_pandas():
        """安全导入 pandas 模块"""
        try:
            import pandas as pd_local
            return pd_local, None
        except ImportError as e:
            error_msg = f"pandas 导入失败: {str(e)}"
            # 尝试重新导入
            try:
                import importlib
                importlib.invalidate_caches()
                import pandas as pd_local
                return pd_local, None
            except Exception as e2:
                return None, f"{error_msg}. 重试失败: {str(e2)}"
    
    def safe_import_numpy():
        """安全导入 numpy 模块"""
        try:
            import numpy as np_local
            return np_local, None
        except ImportError as e:
            error_msg = f"numpy 导入失败: {str(e)}"
            try:
                import importlib
                importlib.invalidate_caches()
                import numpy as np_local
                return np_local, None
            except Exception as e2:
                return None, f"{error_msg}. 重试失败: {str(e2)}"
    
    # 导入关键模块
    pd_module, pd_error = safe_import_pandas()
    np_module, np_error = safe_import_numpy()
    
    if pd_module is None:
        return {
            "error": {
                "type": "IMPORT_ERROR",
                "message": "Failed to import pandas",
                "details": pd_error,
                "solution": "请确保 pandas 已正确安装: pip install pandas"
            }
        }

    # 使用智能读取功能
    if auto_detect:
        # 智能编码检测
        encoding_info = detect_file_encoding(file_path)
        
        # 数据质量预检查
        quality_precheck = data_quality_controller.comprehensive_quality_check(
            file_path, "basic"
        )
        
        # 构建读取参数
        read_kwargs = {}
        if sheet_name is not None:
            read_kwargs['sheet_name'] = sheet_name
        if skiprows is not None:
            read_kwargs['skiprows'] = skiprows
        if header is not None:
            read_kwargs['header'] = header
        if encoding is not None:
            read_kwargs['encoding'] = encoding
        elif encoding_info.get('encoding'):
            read_kwargs['encoding'] = encoding_info['encoding']
        if usecols is not None:
            read_kwargs['usecols'] = usecols
        
        # 使用智能读取，禁用自动检测并明确指定header=0
        # 改进的智能Excel读取逻辑
        try:
            from excel_helper import _suggest_excel_read_parameters
            
            # 1. 获取参数建议
            suggestions = _suggest_excel_read_parameters(file_path)
            recommended_params = suggestions.get('recommended_params', {})
            
            # 2. 检查是否检测到多级列头
            is_multi_level = suggestions.get('analysis', {}).get('multi_level_header_detected', False)
            
            # 3. 智能参数选择 - 用户参数优先
            if header is not None:
                # 用户明确指定了header参数，优先使用用户设置
                final_params = read_kwargs.copy()
                # 不覆盖用户的header设置
            elif is_multi_level:
                # 多级列头且用户未指定header：使用建议参数
                final_params = recommended_params.copy()
                final_params.update(read_kwargs)
            else:
                # 简单列头且用户未指定header：使用header=0
                final_params = read_kwargs.copy()
                final_params['header'] = 0
            
            # 4. 执行读取
            read_result = smart_read_excel(file_path, auto_detect_params=False, **final_params)
            
            # 5. 验证并可能回退
            if read_result['success']:
                df = read_result['dataframe']
                unnamed_cols = [col for col in df.columns if 'Unnamed' in str(col)]
                if len(unnamed_cols) > len(df.columns) * 0.5:
                    # 回退到header=0
                    fallback_params = read_kwargs.copy()
                    fallback_params['header'] = 0
                    read_result = smart_read_excel(file_path, auto_detect_params=False, **fallback_params)
                    
        except Exception as e:
            # 出错时回退到简单的header=0
            fallback_params = read_kwargs.copy()
            fallback_params['header'] = 0
            read_result = smart_read_excel(file_path, auto_detect_params=False, **fallback_params)
        
        if not read_result['success']:
            return {
                "error": {
                    "type": "SMART_READ_ERROR",
                    "message": "智能读取失败: " + "; ".join(read_result.get('errors', [])),
                    "warnings": read_result.get('warnings', []),
                    "solution": "尝试手动指定参数或检查文件格式。"
                }
            }
        
        df = read_result['dataframe']
        read_info = read_result['info']
    else:
        # 传统读取方式
        read_params = {}
        if sheet_name:
            read_params['sheet_name'] = sheet_name
        if skiprows is not None:
            read_params['skiprows'] = skiprows
        if header is not None:
            read_params['header'] = header
        if usecols is not None:
            read_params['usecols'] = usecols
        
        try:
            df = pd_module.read_excel(file_path, **read_params)
            read_info = {'read_params': read_params, 'method': 'traditional'}
        except Exception as e:
            return {
                "error": {
                    "type": "READ_ERROR",
                    "message": f"读取Excel文件失败: {str(e)}",
                    "solution": "请检查文件格式和参数设置"
                }
            }
    
    # 增强的执行环境准备
    local_vars = {
        'pd': pd_module, 
        'file_path': file_path, 
        'sheet_name': sheet_name,
        'df': df,
        'read_info': read_info
    }
    
    # 添加 numpy（如果可用）
    if np_module is not None:
        local_vars['np'] = np_module
    
    # 添加常用内置函数
    local_vars.update({
        'len': len, 'str': str, 'int': int, 'float': float,
        'list': list, 'dict': dict, 'print': print,
        'range': range, 'enumerate': enumerate, 'zip': zip,
        'sum': sum, 'max': max, 'min': min, 'abs': abs, 'round': round
    })
    
    # 如果允许文件写入，添加文件操作函数
    if allow_file_write:
        local_vars.update({
            'open': open,
            'os': __import__('os'),
            'pathlib': __import__('pathlib')
        })
    
    # 创建安全的全局环境
    builtins_dict = {
        'len': len, 'str': str, 'int': int, 'float': float,
        'list': list, 'dict': dict, 'print': print,
        'range': range, 'enumerate': enumerate, 'zip': zip,
        'sum': sum, 'max': max, 'min': min, 'abs': abs, 'round': round,
        'locals': locals, 'globals': globals, 'isinstance': isinstance,
        'type': type, 'hasattr': hasattr, 'getattr': getattr,
        'NameError': NameError, 'ValueError': ValueError, 'TypeError': TypeError,
        'KeyError': KeyError, 'IndexError': IndexError, 'Exception': Exception,
        '__import__': __import__
    }
    
    # 如果允许文件写入，添加文件操作到全局环境
    if allow_file_write:
        builtins_dict.update({
            'open': open
        })
    
    global_vars = {
        '__builtins__': builtins_dict
    }

    stdout_capture = StringIO()
    old_stdout = sys.stdout
    sys.stdout = stdout_capture

    try:
        # 使用安全代码执行器执行用户代码
        from security.secure_code_executor import SecureCodeExecutor
        secure_executor = SecureCodeExecutor(
            max_memory_mb=256,
            max_execution_time=30,
            enable_ast_analysis=False  # 禁用 AST 分析以提高成功率
        )
        
        # 准备执行上下文
        context = local_vars.copy()
        context.update(global_vars)
        
        # 执行代码并获取结果
        execution_result = secure_executor.execute_code(code, context)
        
        # 如果执行成功，进行数据质量后检查
        if execution_result.get('success', False):
            # 检查执行后的数据框是否存在
            if 'df' in execution_result.get('variables', {}):
                processed_df = execution_result['variables']['df']
                
                # 数据质量后检查
                post_quality_check = {
                    "data_shape": processed_df.shape if hasattr(processed_df, 'shape') else None,
                    "null_values": processed_df.isnull().sum().to_dict() if hasattr(processed_df, 'isnull') else None,
                    "data_types": processed_df.dtypes.to_dict() if hasattr(processed_df, 'dtypes') else None,
                    "memory_usage": processed_df.memory_usage(deep=True).sum() if hasattr(processed_df, 'memory_usage') else None
                }
                
                # 添加数据清洗建议
                cleaning_suggestions = data_cleaner.suggest_cleaning_operations(
                    processed_df if hasattr(processed_df, 'shape') else df
                )
                
                execution_result["data_quality_analysis"] = {
                    "pre_execution_quality": quality_precheck if auto_detect else None,
                    "post_execution_check": post_quality_check,
                    "cleaning_suggestions": cleaning_suggestions
                }
        
        if not execution_result['success']:
            return {
                "error": execution_result.get('error', '代码执行失败'),
                "output": execution_result.get('output', stdout_capture.getvalue()),
                "suggestion": execution_result.get('suggestion', '请检查代码语法和逻辑错误'),
                "details": execution_result.get('message', ''),
                "traceback": execution_result.get('traceback', '')
            }
        
        # 从执行结果中获取result
        result = execution_result.get('result', None)
        
        # 检查局部变量中是否有 result
        if result is None and 'result' in local_vars:
            result = local_vars['result']
        
        # 如果仍然没有 result，从安全执行器的上下文中获取
        if result is None:
            execution_context = execution_result.get('context', {})
            if 'result' in execution_context:
                result = execution_context['result']
            elif 'locals' in execution_result and 'result' in execution_result['locals']:
                result = execution_result['locals']['result']

        if result is None:
            return {
                "output": stdout_capture.getvalue(),
                "warning": "No 'result' variable found in code",
                "read_info": read_info if auto_detect else None
            }

        # 处理返回结果
        if isinstance(result, (pd_module.DataFrame, pd_module.Series)):
            response = {
                "result": {
                    "type": "dataframe" if isinstance(result, pd_module.DataFrame) else "series",
                    "shape": result.shape,
                    "dtypes": str(result.dtypes),
                    "data": result.head().to_dict() if isinstance(result, pd_module.DataFrame) else result.to_dict()
                },
                "output": stdout_capture.getvalue()
            }
        else:
            response = {
                "result": str(result),
                "output": stdout_capture.getvalue()
            }
        
        # 添加读取信息
        if auto_detect:
            response["read_info"] = read_info
            if read_result.get('warnings'):
                response["warnings"] = read_result['warnings']

        return response
        
    except NameError as e:
        error_msg = str(e)
        suggestions = []
        
        if "'pd'" in error_msg or "pandas" in error_msg.lower():
            suggestions.extend([
                "pandas 模块可能未正确导入，请检查安装: pip install pandas",
                "尝试重启 MCP 服务器",
                "检查虚拟环境是否正确激活",
                "尝试在代码中显式导入: import pandas as pd"
            ])
        
        if "'np'" in error_msg or "numpy" in error_msg.lower():
            suggestions.extend([
                "numpy 模块可能未正确导入，请检查安装: pip install numpy",
                "尝试在代码中显式导入: import numpy as np"
            ])
        
        if "'df'" in error_msg:
            suggestions.extend([
                "DataFrame 未正确加载，请检查文件路径和格式",
                "尝试使用 pd.read_excel() 手动读取文件"
            ])
        
        return {
            "error": {
                "type": "NameError",
                "message": f"变量未定义错误: {error_msg}",
                "traceback": traceback.format_exc(),
                "output": stdout_capture.getvalue(),
                "suggestions": suggestions,
                "pandas_available": pd_module is not None,
                "numpy_available": np_module is not None
            }
        }
        
    except Exception as e:
        error_msg = str(e)
        suggestions = []

        if "No such file or directory" in error_msg:
            suggestions.append("Use raw strings for paths: r'path\to\file.xlsx'")
        if "Worksheet named" in error_msg and "not found" in error_msg:
            suggestions.append("Check the sheet_name parameter. Ensure the sheet name exists in the Excel file.")
        if "could not convert string to float" in error_msg:
            suggestions.append("Try: pd.to_numeric(df['col'], errors='coerce')")
        if "AttributeError" in error_msg and "str" in error_msg:
            suggestions.append("Try: df['col'].astype(str).str.strip()")
        if "encoding" in error_msg.lower():
            suggestions.append("Try specifying encoding parameter or disable auto_detect")

        return {
            "error": {
                "type": type(e).__name__,
                "message": error_msg,
                "traceback": traceback.format_exc(),
                "output": stdout_capture.getvalue(),
                "suggestions": suggestions if suggestions else None,
                "read_info": read_info if auto_detect else None
            }
        }
    finally:
        sys.stdout = old_stdout


@mcp.tool()
def run_code(code: str, file_path: str) -> dict:
    """在CSV文件上执行数据处理代码，具备安全检查功能。
    
    Args:
        code: 要执行的数据处理代码字符串。
        file_path: CSV文件路径。
    
    Returns:
        dict: 执行结果，包含数据、输出或错误信息。
    """
    try:
        # Security check - 更精确的检查
        for forbidden in BLACKLIST:
            if forbidden in code:
                return {
                    "success": False,
                    "error": f"Forbidden operation detected: {forbidden}",
                    "suggestion": "请仅使用数据处理操作进行数据分析。"
                }
        
        # 验证文件访问
        validation_result = validate_file_access(file_path)
        if validation_result["status"] != "SUCCESS":
            return {
                "success": False,
                "error": validation_result["message"],
                "suggestion": "Please check the file path and ensure the file exists."
            }
        
        # Read CSV file with intelligent encoding detection
        try:
            # 首先尝试检测文件编码
            encoding_info = detect_file_encoding(file_path)
            detected_encoding = encoding_info.get('encoding', 'utf-8')
            
            # 尝试使用检测到的编码读取CSV文件
            try:
                df = pd.read_csv(file_path, encoding=detected_encoding)
            except UnicodeDecodeError:
                # 如果检测到的编码失败，尝试常见编码
                common_encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5', 'latin1', 'cp1252']
                df = None
                last_error = None
                
                for enc in common_encodings:
                    try:
                        df = pd.read_csv(file_path, encoding=enc)
                        break
                    except (UnicodeDecodeError, UnicodeError) as e:
                        last_error = e
                        continue
                
                if df is None:
                    return {
                        "success": False,
                        "error": f"Failed to read CSV file with any encoding. Last error: {str(last_error)}",
                        "suggestion": "Please check the file encoding. Try converting the file to UTF-8 format or specify the correct encoding."
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read CSV file: {str(e)}",
                "suggestion": "Please ensure the file is a valid CSV format and check the file encoding."
            }
        
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            # 使用安全代码执行器执行代码
            from security.secure_code_executor import SecureCodeExecutor
            secure_executor = SecureCodeExecutor(
                max_memory_mb=256,
                max_execution_time=30,
                enable_ast_analysis=False  # 禁用 AST 分析以提高成功率
            )
            
            # 准备执行上下文
            context = {'df': df, 'pd': pd}
            
            # 执行代码
            execution_result = secure_executor.execute_code(code, context)
            
            if not execution_result['success']:
                return {
                    "success": False,
                    "error": f"代码执行失败: {execution_result.get('error', '未知错误')}",
                    "output": execution_result.get('output', captured_output.getvalue()),
                    "suggestion": execution_result.get('suggestion', '')
                }
            
            # 从执行结果获取输出
            output = execution_result.get('output', '')
            
            # 检查是否有result变量
            result_data = None
            result = execution_result.get('result', None)
            if result is not None:
                if isinstance(result, pd.DataFrame):
                    result_data = {
                        "type": "DataFrame",
                        "shape": result.shape,
                        "columns": result.columns.tolist(),
                        "data": result.head(10).to_dict('records'),
                        "dtypes": result.dtypes.astype(str).to_dict()
                    }
                elif isinstance(result, pd.Series):
                    result_data = {
                        "type": "Series",
                        "name": result.name,
                        "length": len(result),
                        "data": result.head(10).tolist(),
                        "dtype": str(result.dtype)
                    }
                else:
                    result_data = {
                        "type": type(result).__name__,
                        "value": str(result)
                    }
            
            return {
                "success": True,
                "output": output,
                "result": result_data,
                "suggestion": "Code executed successfully. Use 'result' variable to store your final output."
            }
            
        finally:
            sys.stdout = old_stdout
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "suggestion": "请检查数据处理语法，确保操作对数据有效。"
        }


@mcp.tool()
def bar_chart_to_html(
    categories: list,
    values: list,
    title: str = "Interactive Chart",
   
) -> dict:
    """Generate interactive HTML bar chart using Chart.js template.
    
    Args:
        categories: List of category names for x-axis
        values: List of numeric values for y-axis
        title: Chart title (default: "Interactive Chart")
        x_label: Label for X-axis (default: "Categories")
        y_label: Label for Y-axis (default: "Values")
        
    Returns:
        dict: Contains file path and status information
        
    Example:
        >>> bar_chart_to_html(
        ...     categories=['Electronics', 'Clothing', 'Home Goods', 'Sports Equipment'],
        ...     values=[120000, 85000, 95000, 60000],
        ...     title="Q1 Sales by Product Category"
        ... )
        {
            "status": "SUCCESS",
            "filepath": "/absolute/path/to/plotXXXXXX.html",
        }
    """
    # Validate input lengths
    if len(categories) != len(values):
        return {
            "status": "ERROR",
            "error": "MISMATCHED_LENGTHS",
            "message": f"Categories ({len(categories)}) and values ({len(values)}) must be same length"
        }

    # Read template file
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./templates/barchart_template.html")
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except Exception as e:
        return {
            "status": "ERROR",
            "error": "TEMPLATE_READ_ERROR",
            "message": str(e)
        }

    # Prepare data for Chart.js
    all_categories = categories
    all_values = values
    colors = [
        "#4e73df", "#1cc88a", "#36b9cc", "#f6c23e",
        "#e74a3b", "#858796", "#f8f9fc", "#5a5c69",
        "#6610f2", "#6f42c1", "#e83e8c", "#d63384",
        "#fd7e14", "#ffc107", "#28a745", "#20c997",
        "#17a2b8", "#007bff", "#6c757d", "#343a40",
        "#dc3545", "#ff6b6b", "#4ecdc4", "#1a535c"
    ][:len(all_categories)]

    # Inject data into template
    template = template.replace(
        'labels: ["Electronics", "Clothing", "Home Goods", "Sports Equipment"]',
        f'labels: {json.dumps(all_categories)}'
    ).replace(
        'data: [120000, 85000, 95000, 60000]',
        f'data: {json.dumps(all_values)}'
    ).replace(
        'backgroundColor: ["#4e73df", "#1cc88a", "#36b9cc", "#f6c23e"]',
        f'backgroundColor: {json.dumps(colors)}'
    ).replace(
        'Sales by Category (2023)',
        title
    ).replace(
        'legend: { position: \'top\' },',
        ''
    )

    # Save to plot directory as HTML
    charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
    os.makedirs(charts_dir, exist_ok=True)

    timestamp = str(int(time.time()))
    filename = f"chart_{timestamp}.html"
    filepath = os.path.join(charts_dir, filename)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(template)
    except Exception as e:
        return {
            "status": "ERROR",
            "error": "FILE_WRITE_ERROR",
            "message": str(e)
        }

    return {
        "status": "SUCCESS",
        "filepath": os.path.abspath(filepath)
    }


@mcp.tool()
def pie_chart_to_html(
    labels: list,
    values: list,
    title: str = "Interactive Pie Chart"
) -> dict:
    """Generate interactive HTML pie chart using Chart.js template.
    
    Args:
        labels: List of label names for each pie slice
        values: List of numeric values for each slice
        title: Chart title (default: "Interactive Pie Chart")
        
    Returns:
        dict: Contains file path and status information
        
    Example:
        >>> pie_chart_to_html(
        ...     labels=['Electronics', 'Clothing', 'Home Goods'],
        ...     values=[120000, 85000, 95000],
        ...     title="Q1 Sales Distribution"
        ... )
        {
            "status": "SUCCESS",
            "filepath": "/absolute/path/to/plotXXXXXX.html",
        }
    """
    # Validate input lengths
    if len(labels) != len(values):
        return {
            "status": "ERROR",
            "error": "MISMATCHED_LENGTHS",
            "message": f"Labels ({len(labels)}) and values ({len(values)}) must be same length"
        }

    # Read template file
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./templates/piechart_template.html")
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except Exception as e:
        return {
            "status": "ERROR",
            "error": "TEMPLATE_READ_ERROR",
            "message": str(e)
        }

    # Prepare data for Chart.js
    colors = [
        "#4e73df", "#1cc88a", "#36b9cc", "#f6c23e",
        "#e74a3b", "#858796", "#f8f9fc", "#5a5c69",
        "#6610f2", "#6f42c1", "#e83e8c", "#d63384",
        "#fd7e14", "#ffc107", "#28a745", "#20c997",
        "#17a2b8", "#007bff", "#6c757d", "#343a40",
        "#dc3545", "#ff6b6b", "#4ecdc4", "#1a535c"
    ][:len(labels)]

    # Inject data into template
    template = template.replace(
        'labels: ["Apple", "Samsung", "Huawei", "Xiaomi", "Others"]',
        f'labels: {json.dumps(labels)}'
    ).replace(
        'data: [45, 25, 12, 8, 10]',
        f'data: {json.dumps(values)}'
    ).replace(
        'backgroundColor: ["#4e73df", "#1cc88a", "#36b9cc", "#f6c23e", "#e74a3b"]',
        f'backgroundColor: {json.dumps(colors)}'
    ).replace(
        'Global Smartphone Market Share (2023)',
        title
    )

    # Save to plot directory as HTML
    charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
    os.makedirs(charts_dir, exist_ok=True)

    timestamp = str(int(time.time()))
    filename = f"chart_{timestamp}.html"
    filepath = os.path.join(charts_dir, filename)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(template)
    except Exception as e:
        return {
            "status": "ERROR",
            "error": "FILE_WRITE_ERROR",
            "message": str(e)
        }

    return {
        "status": "SUCCESS",
        "filepath": os.path.abspath(filepath)
    }

@mcp.tool()
def line_chart_to_html(
    labels: list,
    datasets: list,
    title: str = "Interactive Line Chart"
) -> dict:
    """Generate interactive HTML line chart using Chart.js template.
    
    Args:
        labels: List of label names for x-axis
        datasets: List of datasets, each containing:
            - label: Name of the dataset
            - data: List of numeric values (3 dimensions: [x, y, z])
        title: Chart title (default: "Interactive Line Chart")
        
    Returns:
        dict: Contains file path and status information
        
    Example:
        >>> line_chart_to_html(
        ...     labels=['Jan', 'Feb', 'Mar'],
        ...     datasets=[
        ...         {'label': 'Sales', 'data': [[100, 200, 300], [150, 250, 350], [200, 300, 400]]},
        ...         {'label': 'Expenses', 'data': [[50, 100, 150], [75, 125, 175], [100, 150, 200]]}
        ...     ],
        ...     title="Monthly Performance"
        ... )
        {
            "status": "SUCCESS",
            "filepath": "/absolute/path/to/plotXXXXXX.html",
        }
    """
    # Validate input
    if not all(len(d['data']) == len(labels) for d in datasets):
        return {
            "status": "ERROR",
            "error": "MISMATCHED_LENGTHS",
            "message": "All datasets must have same length as labels"
        }

    # Read template file
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./templates/linechart_template.html")
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except Exception as e:
        return {
            "status": "ERROR",
            "error": "TEMPLATE_READ_ERROR",
            "message": str(e)
        }

    # Prepare data for Chart.js
    chart_data = {
        "labels": labels,
        "datasets": []
    }
    
    # Create datasets using main labels
    for dataset in datasets:
            chart_data['datasets'].append({
                "label": dataset['label'],
                "data": dataset['data'],
                "borderColor": '#4e73df',  # Default color
                "backgroundColor": '#4e73df',
            "borderWidth": 2,
            "pointRadius": 5,
            "tension": 0,
            "fill": False
        })

    # Inject data into template
    template = template.replace(
        'labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]',
        f'labels: {json.dumps(labels)}'
    ).replace(
        'datasets: [\n' +
        '                {\n' +
        '                    label: "Electronics",\n' +
        '                    data: [6500, 5900, 8000, 8100, 8600, 8250, 9500, 10500, 12000, 11500, 13000, 15000],\n' +
        '                    borderColor: "#4e73df",\n' +
        '                    backgroundColor: "#4e73df",\n' +
        '                    borderWidth: 2,\n' +
        '                    pointRadius: 5,\n' +
        '                    tension: 0,\n' +
        '                    fill: false\n' +
        '                },\n' +
        '                {\n' +
        '                    label: "Clothing",\n' +
        '                    data: [12000, 11000, 12500, 10500, 11500, 13000, 14000, 12500, 11000, 9500, 10000, 12000],\n' +
        '                    borderColor: "#1cc88a",\n' +
        '                    backgroundColor: "#1cc88a",\n' +
        '                    borderWidth: 2,\n' +
        '                    pointRadius: 5,\n' +
        '                    tension: 0,\n' +
        '                    fill: false\n' +
        '                },\n' +
        '                {\n' +
        '                    label: "Home Goods",\n' +
        '                    data: [8000, 8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000, 12500, 13000, 13500],\n' +
        '                    borderColor: "#36b9cc",\n' +
        '                    backgroundColor: "#36b9cc",\n' +
        '                    borderWidth: 2,\n' +
        '                    pointRadius: 5,\n' +
        '                    tension: 0,\n' +
        '                    fill: false\n' +
        '                }\n' +
        '            ]',
        f'datasets: {json.dumps(chart_data["datasets"], indent=16)}'
    ).replace(
        'Interactive Sales Trend Dashboard',
        title
    ).replace(
        'Monthly Sales Trend (2023)',
        title
    )

    # Save to plot directory as HTML
    charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
    os.makedirs(charts_dir, exist_ok=True)

    timestamp = str(int(time.time()))
    filename = f"chart_{timestamp}.html"
    filepath = os.path.join(charts_dir, filename)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(template)
    except Exception as e:
        return {
            "status": "ERROR",
            "error": "FILE_WRITE_ERROR",
            "message": str(e)
        }

    return {
        "status": "SUCCESS",
        "filepath": os.path.abspath(filepath)
    }


@mcp.tool()
def validate_data_quality(file_path: str) -> dict:
    """验证数据质量并提供改进建议
    
    Args:
        file_path: 数据文件路径
        
    Returns:
        dict: 数据质量报告和改进建议
    """
    try:
        validation_result = validate_file_access(file_path)
        if validation_result["status"] != "SUCCESS":
            return validation_result
        
        df = pd.read_csv(file_path)
        
        quality_report = {
            "basic_info": {
                "total_rows": len(df),
                "columns": len(df.columns),
                "memory_usage": df.memory_usage(deep=True).sum()
            },
            "missing_data": {
                "total_missing": df.isnull().sum().sum(),
                "missing_by_column": df.isnull().sum().to_dict(),
                "missing_percentage": (df.isnull().sum() / len(df) * 100).to_dict()
            },
            "duplicates": {
                "duplicate_rows": df.duplicated().sum(),
                "duplicate_percentage": df.duplicated().sum() / len(df) * 100
            },
            "data_types": df.dtypes.astype(str).to_dict(),
            "recommendations": []
        }
        
        # 生成建议
        if quality_report["missing_data"]["total_missing"] > 0:
            quality_report["recommendations"].append("考虑处理缺失值：删除、填充或插值")
        
        if quality_report["duplicates"]["duplicate_rows"] > 0:
            quality_report["recommendations"].append("发现重复行，考虑去重处理")
        
        # 检查数据类型优化机会
        for col, dtype in quality_report["data_types"].items():
            if dtype == 'object':
                if df[col].nunique() / len(df) < 0.5:  # 低基数字符串
                    quality_report["recommendations"].append(f"列 '{col}' 可考虑转换为分类类型以节省内存")
        
        return create_success_response(quality_report, "数据质量分析完成")
        
    except Exception as e:
        return create_error_response(
            "PROCESSING_ERROR",
            f"数据质量验证失败: {str(e)}",
            details={"traceback": traceback.format_exc()}
        )


# 注册新的Excel智能工具
@mcp.tool()
def suggest_excel_read_parameters_tool(file_path: str) -> dict:
    """智能推荐Excel文件读取参数
    
    Args:
        file_path: Excel文件的绝对路径
        
    Returns:
        dict: 包含推荐参数的结构化响应
    """
    return suggest_excel_read_parameters(file_path)

@mcp.tool()
def detect_excel_file_structure_tool(file_path: str) -> dict:
    """检测Excel文件结构
    
    Args:
        file_path: Excel文件的绝对路径
        
    Returns:
        dict: 包含文件结构信息的响应
    """
    return detect_excel_file_structure(file_path)

@mcp.tool()
def create_excel_read_template_tool(file_path: str, sheet_name: Optional[str] = None, skiprows: Optional[int] = None, header: Optional[int] = None, usecols: Optional[str] = None) -> dict:
    """生成Excel读取代码模板
    
    Args:
        file_path: Excel文件的绝对路径
        sheet_name: 工作表名称
        skiprows: 跳过的行数
        header: 标题行位置
        usecols: 使用的列
        
    Returns:
        dict: 包含代码模板的响应
    """
    return create_excel_read_template(file_path, sheet_name, skiprows, header, usecols)

@mcp.tool()
def comprehensive_data_verification_tool(
    file_path: str,
    reference_file: str = None,
    verification_level: str = "detailed",
    save_report: bool = True
) -> dict:
    """
    综合数据验证和核准工具
    
    提供全面的Excel数据验证、质量评估和比对核准功能。
    支持单文件验证和双文件比较验证模式。
    
    Args:
        file_path: 要验证的Excel文件路径
        reference_file: 参考文件路径（可选，用于比较验证）
        verification_level: 验证级别
            - "basic": 基础验证（文件结构、基本统计）
            - "detailed": 详细验证（包含数据质量分析）
            - "comprehensive": 综合验证（包含异常检测和深度分析）
        save_report: 是否保存验证报告到本地
    
    Returns:
        dict: 包含以下字段的验证结果
            - overall_status: 总体状态 (EXCELLENT/GOOD/ACCEPTABLE/POOR/CRITICAL/FAILED)
            - data_quality_score: 数据质量得分 (0-100)
            - file_analysis: 文件结构分析结果
            - data_integrity: 数据完整性验证结果
            - comparison_results: 比较验证结果（如果提供了参考文件）
            - recommendations: 改进建议列表
            - detailed_report: 详细报告（详细和综合级别）
    
    功能特点:
    1. 多层次验证：支持基础、详细、综合三个验证级别
    2. 智能编码检测：自动检测文件编码并优化读取
    3. 数据质量评估：计算综合质量得分
    4. 异常检测：识别异常值和数据模式
    5. 比较验证：支持与参考文件的详细比较
    6. 报告生成：自动生成验证报告并可保存
    7. 建议系统：提供针对性的数据改进建议
    
    使用示例:
    - 基础验证: comprehensive_data_verification_tool("data.xlsx", verification_level="basic")
    - 详细验证: comprehensive_data_verification_tool("data.xlsx", verification_level="detailed")
    - 比较验证: comprehensive_data_verification_tool("data.xlsx", "reference.xlsx", "comprehensive")
    """
    try:
        # 验证文件路径
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"文件不存在: {file_path}",
                "overall_status": "FAILED"
            }
        
        if reference_file and not os.path.exists(reference_file):
            return {
                "success": False,
                "error": f"参考文件不存在: {reference_file}",
                "overall_status": "FAILED"
            }
        
        # 创建综合验证器
        verifier = ComprehensiveDataVerifier()
        
        # 执行综合验证
        verification_result = verifier.comprehensive_excel_verification(
            file_path=file_path,
            reference_file=reference_file,
            verification_level=verification_level,
            save_report=save_report
        )
        
        # 添加成功标志
        verification_result["success"] = True
        
        # 添加验证摘要
        verification_result["verification_summary"] = {
            "file_name": os.path.basename(file_path),
            "verification_time": verification_result.get("timestamp"),
            "quality_score": verification_result.get("data_quality_score", 0),
            "status": verification_result.get("overall_status", "UNKNOWN"),
            "has_reference": reference_file is not None,
            "level": verification_level,
            "recommendations_count": len(verification_result.get("recommendations", []))
        }
        
        return verification_result
        
    except Exception as e:
        return {
            "success": False,
            "error": f"综合验证过程中发生错误: {str(e)}",
            "overall_status": "ERROR",
            "file_path": file_path,
            "reference_file": reference_file,
            "verification_level": verification_level
        }


@mcp.tool()
def batch_data_verification_tool(
    file_paths: list,
    verification_level: str = "detailed",
    save_reports: bool = True
) -> dict:
    """
    批量数据验证工具
    
    对多个Excel文件进行批量验证和质量评估。
    
    Args:
        file_paths: Excel文件路径列表
        verification_level: 验证级别 ("basic", "detailed", "comprehensive")
        save_reports: 是否保存验证报告
    
    Returns:
        dict: 批量验证结果
            - overall_summary: 总体摘要
            - individual_results: 各文件验证结果
            - quality_ranking: 质量排名
            - batch_recommendations: 批量建议
    """
    try:
        if not file_paths or not isinstance(file_paths, list):
            return {
                "success": False,
                "error": "请提供有效的文件路径列表"
            }
        
        verifier = ComprehensiveDataVerifier()
        batch_results = {
            "success": True,
            "total_files": len(file_paths),
            "processed_files": 0,
            "failed_files": 0,
            "overall_summary": {},
            "individual_results": {},
            "quality_ranking": [],
            "batch_recommendations": []
        }
        
        quality_scores = []
        
        # 逐个验证文件
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    result = verifier.comprehensive_excel_verification(
                        file_path=file_path,
                        verification_level=verification_level,
                        save_report=save_reports
                    )
                    
                    batch_results["individual_results"][file_path] = result
                    quality_scores.append({
                        "file": os.path.basename(file_path),
                        "path": file_path,
                        "score": result.get("data_quality_score", 0),
                        "status": result.get("overall_status", "UNKNOWN")
                    })
                    batch_results["processed_files"] += 1
                else:
                    batch_results["individual_results"][file_path] = {
                        "success": False,
                        "error": "文件不存在",
                        "overall_status": "FAILED"
                    }
                    batch_results["failed_files"] += 1
                    
            except Exception as e:
                batch_results["individual_results"][file_path] = {
                    "success": False,
                    "error": str(e),
                    "overall_status": "ERROR"
                }
                batch_results["failed_files"] += 1
        
        # 生成质量排名
        batch_results["quality_ranking"] = sorted(
            quality_scores, key=lambda x: x["score"], reverse=True
        )
        
        # 生成总体摘要
        if quality_scores:
            scores = [item["score"] for item in quality_scores]
            batch_results["overall_summary"] = {
                "average_quality_score": sum(scores) / len(scores),
                "highest_score": max(scores),
                "lowest_score": min(scores),
                "excellent_files": len([s for s in scores if s >= 90]),
                "good_files": len([s for s in scores if 80 <= s < 90]),
                "acceptable_files": len([s for s in scores if 70 <= s < 80]),
                "poor_files": len([s for s in scores if 60 <= s < 70]),
                "critical_files": len([s for s in scores if s < 60])
            }
        
        # 生成批量建议
        if batch_results["failed_files"] > 0:
            batch_results["batch_recommendations"].append(
                f"有{batch_results['failed_files']}个文件验证失败，请检查文件格式和路径"
            )
        
        if quality_scores:
            avg_score = sum([item["score"] for item in quality_scores]) / len(quality_scores)
            if avg_score < 70:
                batch_results["batch_recommendations"].append(
                    "整体数据质量偏低，建议进行数据清洗和质量改进"
                )
            elif avg_score >= 90:
                batch_results["batch_recommendations"].append(
                    "整体数据质量优秀，可以放心使用"
                )
        
        return batch_results
        
    except Exception as e:
        return {
            "success": False,
            "error": f"批量验证过程中发生错误: {str(e)}"
        }


@mcp.tool()
def excel_read_enhanced(
    file_path: str,
    sheet_name: str = None,
    start_row: int = None,
    end_row: int = None,
    start_col: str = None,
    end_col: str = None,
    use_go_service: bool = True
) -> dict:
    """
    增强版 Excel 读取工具，集成 Go excelize 库提供高性能处理
    
    Args:
        file_path: Excel 文件路径
        sheet_name: 工作表名称（可选）
        start_row: 起始行号（可选）
        end_row: 结束行号（可选）
        start_col: 起始列（如 'A'，可选）
        end_col: 结束列（如 'Z'，可选）
        use_go_service: 是否优先使用 Go 服务（默认 True）
        
    Returns:
        dict: 读取结果，包含数据和性能信息
    """
    try:
        processor = get_excel_processor()
        result = processor.read_excel_enhanced(
            file_path=file_path,
            sheet_name=sheet_name,
            start_row=start_row,
            end_row=end_row,
            start_col=start_col,
            end_col=end_col,
            use_go=use_go_service
        )
        return result
    except Exception as e:
        return {
            "success": False,
            "error": f"增强 Excel 读取失败: {str(e)}",
            "suggestion": "请检查文件路径和参数设置"
        }


@mcp.tool()
def excel_write_enhanced(
    file_path: str,
    data: list,
    sheet_name: str = None,
    start_row: int = None,
    start_col: str = None,
    use_go_service: bool = True
) -> dict:
    """
    增强版 Excel 写入工具，集成 Go excelize 库提供高性能处理
    
    Args:
        file_path: Excel 文件路径
        data: 要写入的数据（字典列表格式）
        sheet_name: 工作表名称（可选）
        start_row: 起始行号（可选）
        start_col: 起始列（如 'A'，可选）
        use_go_service: 是否优先使用 Go 服务（默认 True）
        
    Returns:
        dict: 写入结果，包含性能信息
    """
    try:
        if not isinstance(data, list):
            return {
                "success": False,
                "error": "数据格式错误，需要字典列表格式",
                "suggestion": "请提供 [{column1: value1, column2: value2}, ...] 格式的数据"
            }
        
        processor = get_excel_processor()
        result = processor.write_excel_enhanced(
            file_path=file_path,
            data=data,
            sheet_name=sheet_name,
            start_row=start_row,
            start_col=start_col,
            use_go=use_go_service
        )
        return result
    except Exception as e:
        return {
            "success": False,
            "error": f"增强 Excel 写入失败: {str(e)}",
            "suggestion": "请检查文件路径和数据格式"
        }


@mcp.tool()
def excel_chart_enhanced(
    file_path: str,
    chart_type: str,
    data_range: str,
    sheet_name: str = None,
    title: str = None,
    x_axis_title: str = None,
    y_axis_title: str = None
) -> dict:
    """
    增强版 Excel 图表创建工具，使用 Go excelize 库提供高性能图表生成
    
    Args:
        file_path: Excel 文件路径
        chart_type: 图表类型（'col', 'line', 'pie', 'bar', 'area', 'scatter' 等）
        data_range: 数据范围（如 'A1:B10'）
        sheet_name: 工作表名称（可选）
        title: 图表标题（可选）
        x_axis_title: X轴标题（可选）
        y_axis_title: Y轴标题（可选）
        
    Returns:
        dict: 图表创建结果
    """
    try:
        # 验证图表类型
        valid_chart_types = ['col', 'line', 'pie', 'bar', 'area', 'scatter', 'doughnut']
        if chart_type not in valid_chart_types:
            return {
                "success": False,
                "error": f"不支持的图表类型: {chart_type}",
                "suggestion": f"支持的图表类型: {', '.join(valid_chart_types)}"
            }
        
        processor = get_excel_processor()
        result = processor.create_chart_enhanced(
            file_path=file_path,
            chart_type=chart_type,
            data_range=data_range,
            sheet_name=sheet_name,
            chart_title=title,
            x_axis_title=x_axis_title,
            y_axis_title=y_axis_title
        )
        return result
    except Exception as e:
        return {
            "success": False,
            "error": f"增强图表创建失败: {str(e)}",
            "suggestion": "请检查文件路径、数据范围和图表参数"
        }


@mcp.tool()
def excel_info_enhanced(file_path: str) -> dict:
    """
    增强版 Excel 文件信息获取工具，使用 Go excelize 库提供详细文件分析
    
    Args:
        file_path: Excel 文件路径
        
    Returns:
        dict: 详细的文件信息，包括工作表、行列数等
    """
    try:
        processor = get_excel_processor()
        result = processor.get_file_info_enhanced(file_path)
        return result
    except Exception as e:
        return {
            "success": False,
            "error": f"获取文件信息失败: {str(e)}",
            "suggestion": "请检查文件路径是否正确"
        }


@mcp.tool()
def excel_performance_comparison(
    file_path: str,
    operation: str = "read",
    test_data: list = None
) -> dict:
    """
    Excel 性能对比工具，比较 Go 服务和 pandas 的性能差异
    
    Args:
        file_path: Excel 文件路径
        operation: 操作类型（'read' 或 'write'）
        test_data: 测试数据（写入操作时需要）
        
    Returns:
        dict: 性能对比结果
    """
    try:
        import time
        
        results = {
            "success": True,
            "operation": operation,
            "file_path": file_path,
            "performance_comparison": {},
            "recommendation": ""
        }
        
        processor = get_excel_processor()
        
        if operation == "read":
            # 测试 Go 服务性能
            start_time = time.time()
            go_result = processor.read_excel_enhanced(file_path, use_go=True)
            go_time = time.time() - start_time
            
            # 测试 pandas 性能
            start_time = time.time()
            pandas_result = processor.read_excel_enhanced(file_path, use_go=False)
            pandas_time = time.time() - start_time
            
            results["performance_comparison"] = {
                "go_service": {
                    "time_seconds": round(go_time, 4),
                    "success": go_result.get("success", False),
                    "method": go_result.get("data", {}).get("method", "unknown")
                },
                "pandas": {
                    "time_seconds": round(pandas_time, 4),
                    "success": pandas_result.get("success", False),
                    "method": pandas_result.get("data", {}).get("method", "unknown")
                }
            }
            
            # 性能提升计算
            if go_time > 0 and pandas_time > 0:
                speedup = pandas_time / go_time
                results["performance_comparison"]["speedup"] = round(speedup, 2)
                
                if speedup > 2:
                    results["recommendation"] = f"Go 服务比 pandas 快 {speedup:.1f} 倍，建议使用 Go 服务"
                elif speedup < 0.8:
                    results["recommendation"] = "pandas 性能更好，建议使用 pandas"
                else:
                    results["recommendation"] = "两种方法性能相近，可根据需要选择"
        
        elif operation == "write":
            if not test_data:
                return {
                    "success": False,
                    "error": "写入测试需要提供 test_data 参数",
                    "suggestion": "请提供测试数据列表"
                }
            
            # 创建临时文件进行测试
            import tempfile
            
            with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp1, \
                 tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp2:
                
                # 测试 Go 服务性能
                start_time = time.time()
                go_result = processor.write_excel_enhanced(tmp1.name, test_data, use_go=True)
                go_time = time.time() - start_time
                
                # 测试 pandas 性能
                start_time = time.time()
                pandas_result = processor.write_excel_enhanced(tmp2.name, test_data, use_go=False)
                pandas_time = time.time() - start_time
                
                # 清理临时文件
                try:
                    os.unlink(tmp1.name)
                    os.unlink(tmp2.name)
                except:
                    pass
                
                results["performance_comparison"] = {
                    "go_service": {
                        "time_seconds": round(go_time, 4),
                        "success": go_result.get("success", False),
                        "method": go_result.get("data", {}).get("method", "unknown")
                    },
                    "pandas": {
                        "time_seconds": round(pandas_time, 4),
                        "success": pandas_result.get("success", False),
                        "method": pandas_result.get("data", {}).get("method", "unknown")
                    }
                }
                
                # 性能提升计算
                if go_time > 0 and pandas_time > 0:
                    speedup = pandas_time / go_time
                    results["performance_comparison"]["speedup"] = round(speedup, 2)
                    
                    if speedup > 2:
                        results["recommendation"] = f"Go 服务比 pandas 快 {speedup:.1f} 倍，建议使用 Go 服务"
                    elif speedup < 0.8:
                        results["recommendation"] = "pandas 性能更好，建议使用 pandas"
                    else:
                        results["recommendation"] = "两种方法性能相近，可根据需要选择"
        
        else:
            return {
                "success": False,
                "error": f"不支持的操作类型: {operation}",
                "suggestion": "支持的操作类型: 'read', 'write'"
            }
        
        return results
        
    except Exception as e:
        return {
            "success": False,
            "error": f"性能对比测试失败: {str(e)}",
            "suggestion": "请检查文件路径和参数设置"
        }


# 注册 Excel 公式处理工具
@mcp.tool()
def parse_formula(formula: str, validate_security: bool = False) -> str:
    """解析 Excel 公式
    
    Args:
        formula: Excel 公式字符串
        validate_security: 是否进行安全验证
        
    Returns:
        str: JSON 格式的解析结果
    """
    return parse_excel_formula(formula, validate_security)

@mcp.tool()
def compile_workbook(file_path: str, output_format: str = 'python') -> str:
    """编译 Excel 工作簿为代码
    
    Args:
        file_path: Excel 文件路径
        output_format: 输出格式 ('python' 或 'json')
        
    Returns:
        str: JSON 格式的编译结果
    """
    return compile_excel_workbook(file_path, output_format)

@mcp.tool()
def execute_formula(formula: str, context: str = '{}') -> str:
    """执行 Excel 公式
    
    Args:
        formula: Excel 公式字符串
        context: JSON 格式的上下文数据
        
    Returns:
        str: JSON 格式的执行结果
    """
    return execute_excel_formula(formula, context)

@mcp.tool()
def analyze_dependencies(file_path: str) -> str:
    """分析 Excel 文件的公式依赖关系
    
    Args:
        file_path: Excel 文件路径
        
    Returns:
        str: JSON 格式的依赖分析结果
    """
    return analyze_excel_dependencies(file_path)

@mcp.tool()
def validate_formula(formula: str) -> str:
    """验证 Excel 公式的安全性和有效性
    
    Args:
        formula: Excel 公式字符串
        
    Returns:
        str: JSON 格式的验证结果
    """
    return validate_excel_formula(formula)


# 增强的Excel数据质量控制工具
@mcp.tool()
def enhanced_data_quality_check(file_path: str, quality_level: str = "comprehensive") -> dict:
    """增强的Excel数据质量检查工具
    
    Args:
        file_path: Excel文件路径
        quality_level: 质量检查级别 ("basic", "standard", "comprehensive")
        
    Returns:
        dict: 数据质量检查结果
    """
    try:
        return data_quality_controller.comprehensive_quality_check(file_path, quality_level)
    except Exception as e:
        return create_error_response("QUALITY_CHECK_ERROR", str(e))


@mcp.tool()
def extract_cell_content_advanced(file_path: str, cell_range: Optional[str] = None, sheet_name: Optional[str] = None, 
                                 extract_type: str = "all") -> dict:
    """高级单元格内容提取工具
    
    Args:
        file_path: Excel文件路径
        cell_range: 单元格范围 (如 "A1:C10")
        sheet_name: 工作表名称
        extract_type: 提取类型 ("all", "text", "numbers", "formulas", "formatted")
        
    Returns:
        dict: 提取的单元格内容
    """
    try:
        return cell_content_extractor.extract_cell_content_advanced(
            file_path, cell_range, sheet_name, extract_type
        )
    except Exception as e:
        return create_error_response("CELL_EXTRACTION_ERROR", str(e))


@mcp.tool()
def convert_character_formats(file_path: str, conversion_rules: dict, output_path: Optional[str] = None) -> dict:
    """字符格式自动化转换工具
    
    Args:
        file_path: Excel文件路径
        conversion_rules: 转换规则字典
        output_path: 输出文件路径
        
    Returns:
        dict: 转换结果
    """
    try:
        return character_converter.batch_character_conversion(
            file_path, conversion_rules, output_path
        )
    except Exception as e:
        return create_error_response("CHARACTER_CONVERSION_ERROR", str(e))


@mcp.tool()
def extract_multi_condition_data(file_path: str, conditions: list, sheet_name: Optional[str] = None) -> dict:
    """多条件数据提取工具
    
    Args:
        file_path: Excel文件路径
        conditions: 条件列表
        sheet_name: 工作表名称
        
    Returns:
        dict: 提取的数据
    """
    try:
        return multi_condition_extractor.extract_with_multiple_conditions(
            file_path, conditions, sheet_name
        )
    except Exception as e:
        return create_error_response("MULTI_CONDITION_EXTRACTION_ERROR", str(e))


@mcp.tool()
def merge_multiple_tables(file_paths: list, merge_config: dict, output_path: Optional[str] = None) -> dict:
    """多表格数据合并工具
    
    Args:
        file_paths: Excel文件路径列表
        merge_config: 合并配置
        output_path: 输出文件路径
        
    Returns:
        dict: 合并结果
    """
    try:
        return multi_table_merger.merge_multiple_excel_files(
            file_paths, merge_config, output_path
        )
    except Exception as e:
        return create_error_response("TABLE_MERGE_ERROR", str(e))


@mcp.tool()
def clean_excel_data(file_path: str, cleaning_options: dict, output_path: Optional[str] = None) -> dict:
    """Excel数据清洗工具
    
    Args:
        file_path: Excel文件路径
        cleaning_options: 清洗选项
        output_path: 输出文件路径
        
    Returns:
        dict: 清洗结果
    """
    try:
        return data_cleaner.clean_excel_data(
            file_path=file_path, 
            cleaning_config=cleaning_options, 
            output_file=output_path
        )
    except Exception as e:
        return create_error_response("DATA_CLEANING_ERROR", str(e))


@mcp.tool()
def batch_process_excel_files(file_paths: list, processing_config: dict) -> dict:
    """批量Excel文件处理工具
    
    Args:
        file_paths: Excel文件路径列表
        processing_config: 处理配置
        
    Returns:
        dict: 批量处理结果
    """
    try:
        return batch_processor.batch_process_files(
            file_paths, processing_config
        )
    except Exception as e:
        return create_error_response("BATCH_PROCESSING_ERROR", str(e))


if __name__ == "__main__":
    # 确保必要目录存在
    os.makedirs(CHARTS_DIR, exist_ok=True)
    mcp.run()

