#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Excel Tools with Go Service Integration

集成 Go excelize 库的增强 Excel 工具，提供高性能的 Excel 操作能力。
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import pandas as pd
from excel_go_client import ExcelGoClient, read_excel_fast, write_excel_fast, create_chart_fast, get_file_info_fast

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExcelEnhancedProcessor:
    """增强的 Excel 处理器，集成 Go 服务"""
    
    def __init__(self, use_go_service: bool = True, fallback_to_pandas: bool = True):
        """
        初始化增强的 Excel 处理器
        
        Args:
            use_go_service: 是否使用 Go 服务（默认启用）
            fallback_to_pandas: 当 Go 服务不可用时是否回退到 pandas（默认启用）
        """
        self.use_go_service = use_go_service
        self.fallback_to_pandas = fallback_to_pandas
        self.go_client = None
        
        if use_go_service:
            try:
                self.go_client = ExcelGoClient(auto_start=True)
                # 测试连接
                health = self.go_client.health_check()
                if not health.get('success', False):
                    logger.warning("Go service health check failed, will use fallback")
                    self.go_client = None
                else:
                    logger.info("Go service initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Go service: {e}")
                self.go_client = None
    
    def _should_use_go_service(self, file_path: str) -> bool:
        """判断是否应该使用 Go 服务"""
        if not self.use_go_service or not self.go_client:
            return False
        
        # 检查文件大小，大文件优先使用 Go 服务
        try:
            file_size = os.path.getsize(file_path)
            # 超过 10MB 的文件优先使用 Go 服务
            if file_size > 10 * 1024 * 1024:
                return True
        except:
            pass
        
        return True
    
    def _get_server_functions(self):
        """动态导入server模块的函数，避免循环导入"""
        try:
            from server import validate_file_access, create_success_response, create_error_response
            return validate_file_access, create_success_response, create_error_response
        except ImportError:
            # 如果无法导入，提供简单的替代实现
            def simple_validate_file_access(file_path):
                if os.path.exists(file_path):
                    return {"status": "SUCCESS", "message": "File exists"}
                else:
                    return {"status": "ERROR", "message": "File not found"}
            
            def simple_create_success_response(data, message="Success"):
                return {"status": "SUCCESS", "data": data, "message": message}
            
            def simple_create_error_response(error_type, error_message, user_message):
                return {"status": "ERROR", "error_type": error_type, "error_message": error_message, "user_message": user_message}
            
            return simple_validate_file_access, simple_create_success_response, simple_create_error_response
    
    def read_excel_enhanced(self, 
                           file_path: str, 
                           sheet_name: Optional[str] = None,
                           start_row: Optional[int] = None,
                           end_row: Optional[int] = None,
                           start_col: Optional[str] = None,
                           end_col: Optional[str] = None,
                           use_go: Optional[bool] = None) -> Dict[str, Any]:
        """
        增强的 Excel 读取功能
        
        Args:
            file_path: Excel 文件路径
            sheet_name: 工作表名称
            start_row: 起始行
            end_row: 结束行
            start_col: 起始列
            end_col: 结束列
            use_go: 强制指定是否使用 Go 服务
            
        Returns:
            Dict: 读取结果
        """
        # 获取server函数
        validate_file_access, create_success_response, create_error_response = self._get_server_functions()
        
        # 验证文件访问
        validation_result = validate_file_access(file_path)
        if validation_result["status"] != "SUCCESS":
            return create_error_response(
                "FILE_ACCESS_ERROR",
                validation_result["message"],
                "请确保文件路径正确且文件存在。"
            )
        
        # 决定使用哪种方法
        should_use_go = use_go if use_go is not None else self._should_use_go_service(file_path)
        
        if should_use_go and self.go_client:
            try:
                logger.info(f"Using Go service to read Excel file: {file_path}")
                result = self.go_client.read_excel(
                    file_path=file_path,
                    sheet_name=sheet_name,
                    start_row=start_row,
                    end_row=end_row,
                    start_col=start_col,
                    end_col=end_col
                )
                
                if result.get('success', False):
                    return create_success_response({
                        "method": "go_service",
                        "data": result.get('data', {}),
                        "performance": "high"
                    }, "Excel file read successfully using Go service")
                else:
                    logger.warning(f"Go service failed: {result.get('error', 'Unknown error')}")
                    if not self.fallback_to_pandas:
                        return create_error_response(
                            "GO_SERVICE_ERROR",
                            result.get('error', 'Go service failed'),
                            "Go 服务处理失败"
                        )
            except Exception as e:
                logger.warning(f"Go service exception: {e}")
                if not self.fallback_to_pandas:
                    return create_error_response(
                        "GO_SERVICE_EXCEPTION",
                        str(e),
                        "Go 服务异常"
                    )
        
        # 回退到 pandas
        if self.fallback_to_pandas:
            try:
                logger.info(f"Using pandas to read Excel file: {file_path}")
                
                # 首先获取所有工作表名称
                try:
                    excel_file = pd.ExcelFile(file_path)
                    available_sheets = excel_file.sheet_names
                    logger.info(f"Available sheets: {available_sheets}")
                    
                    # 如果指定了工作表名称但不存在，提供建议
                    if sheet_name and sheet_name not in available_sheets:
                        return create_error_response(
                            "SHEET_NOT_FOUND",
                            f"Worksheet named '{sheet_name}' not found. Available sheets: {', '.join(available_sheets)}",
                            f"找不到名为 '{sheet_name}' 的工作表。可用工作表: {', '.join(available_sheets)}"
                        )
                    
                    # 如果没有指定工作表名称，使用第一个工作表
                    if not sheet_name:
                        sheet_name = available_sheets[0]
                        logger.info(f"No sheet specified, using first sheet: {sheet_name}")
                        
                except Exception as e:
                    logger.warning(f"Failed to get sheet names: {e}")
                    # 如果无法获取工作表名称，继续使用原有逻辑
                
                # 构建 pandas 参数
                kwargs = {}
                if sheet_name:
                    kwargs['sheet_name'] = sheet_name
                if start_row is not None:
                    kwargs['skiprows'] = start_row - 1 if start_row > 0 else 0
                if end_row is not None and start_row is not None:
                    kwargs['nrows'] = end_row - start_row + 1
                
                df = pd.read_excel(file_path, **kwargs)
                
                # 应用列范围过滤
                if start_col or end_col:
                    if start_col and end_col:
                        # 简单的列范围处理
                        start_idx = ord(start_col.upper()) - ord('A')
                        end_idx = ord(end_col.upper()) - ord('A')
                        df = df.iloc[:, start_idx:end_idx+1]
                
                # 转换为与 Go 服务兼容的格式
                rows = []
                if not df.empty:
                    # 添加表头
                    rows.append(df.columns.tolist())
                    # 添加数据行
                    for _, row in df.iterrows():
                        rows.append(row.fillna('').astype(str).tolist())
                
                return create_success_response({
                    "method": "pandas_fallback",
                    "data": {
                        "rows": rows,
                        "sheet_name": sheet_name or "Sheet1",
                        "total_rows": len(rows),
                        "available_sheets": available_sheets if 'available_sheets' in locals() else []
                    },
                    "performance": "standard"
                }, "Excel file read successfully using pandas")
                
            except Exception as e:
                error_msg = str(e)
                # 提供更具体的错误信息
                if "Worksheet named" in error_msg and "not found" in error_msg:
                    return create_error_response(
                        "SHEET_NOT_FOUND",
                        error_msg,
                        "指定的工作表不存在，请检查工作表名称"
                    )
                else:
                    return create_error_response(
                        "PANDAS_READ_ERROR",
                        error_msg,
                        "pandas 读取 Excel 文件失败"
                    )
        
        return create_error_response(
            "NO_AVAILABLE_METHOD",
            "Both Go service and pandas fallback failed",
            "所有读取方法都失败了"
        )
    
    def write_excel_enhanced(self, 
                            file_path: str, 
                            data: Union[List[Dict[str, str]], pd.DataFrame], 
                            sheet_name: Optional[str] = None,
                            start_row: Optional[int] = None,
                            start_col: Optional[str] = None,
                            use_go: Optional[bool] = None) -> Dict[str, Any]:
        """
        增强的 Excel 写入功能
        
        Args:
            file_path: Excel 文件路径
            data: 要写入的数据（字典列表或 DataFrame）
            sheet_name: 工作表名称
            start_row: 起始行
            start_col: 起始列
            use_go: 强制指定是否使用 Go 服务
            
        Returns:
            Dict: 写入结果
        """
        # 获取server函数
        validate_file_access, create_success_response, create_error_response = self._get_server_functions()
        
        # 数据格式转换
        if isinstance(data, pd.DataFrame):
            # 将 DataFrame 转换为字典列表
            data_list = data.fillna('').astype(str).to_dict('records')
        elif isinstance(data, list):
            data_list = data
        else:
            return create_error_response(
                "INVALID_DATA_FORMAT",
                "Data must be a list of dictionaries or pandas DataFrame",
                "数据格式必须是字典列表或 pandas DataFrame"
            )
        
        # 决定使用哪种方法
        should_use_go = use_go if use_go is not None else (self.go_client is not None)
        
        if should_use_go and self.go_client:
            try:
                logger.info(f"Using Go service to write Excel file: {file_path}")
                result = self.go_client.write_excel(
                    file_path=file_path,
                    data=data_list,
                    sheet_name=sheet_name,
                    start_row=start_row,
                    start_col=start_col
                )
                
                if result.get('success', False):
                    return create_success_response({
                        "method": "go_service",
                        "data": result.get('data', {}),
                        "performance": "high"
                    }, "Excel file written successfully using Go service")
                else:
                    logger.warning(f"Go service failed: {result.get('error', 'Unknown error')}")
                    if not self.fallback_to_pandas:
                        return create_error_response(
                            "GO_SERVICE_ERROR",
                            result.get('error', 'Go service failed'),
                            "Go 服务写入失败"
                        )
            except Exception as e:
                logger.warning(f"Go service exception: {e}")
                if not self.fallback_to_pandas:
                    return create_error_response(
                        "GO_SERVICE_EXCEPTION",
                        str(e),
                        "Go 服务异常"
                    )
        
        # 回退到 pandas
        if self.fallback_to_pandas:
            try:
                logger.info(f"Using pandas to write Excel file: {file_path}")
                
                # 创建 DataFrame
                if isinstance(data, list) and data:
                    df = pd.DataFrame(data)
                else:
                    df = data
                
                # 写入 Excel
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    df.to_excel(
                        writer, 
                        sheet_name=sheet_name or 'Sheet1',
                        index=False,
                        startrow=start_row - 1 if start_row and start_row > 0 else 0,
                        startcol=ord(start_col.upper()) - ord('A') if start_col else 0
                    )
                
                return create_success_response({
                    "method": "pandas_fallback",
                    "data": {
                        "file_path": file_path,
                        "rows_written": len(df),
                        "sheet_name": sheet_name or 'Sheet1'
                    },
                    "performance": "standard"
                }, "Excel file written successfully using pandas")
                
            except Exception as e:
                return create_error_response(
                    "PANDAS_WRITE_ERROR",
                    str(e),
                    "pandas 写入 Excel 文件失败"
                )
        
        return create_error_response(
            "NO_AVAILABLE_METHOD",
            "Both Go service and pandas fallback failed",
            "所有写入方法都失败了"
        )
    
    def create_chart_enhanced(self, 
                             file_path: str, 
                             chart_type: str,
                             data_range: str,
                             chart_title: Optional[str] = None,
                             sheet_name: Optional[str] = None,
                             x_axis_title: Optional[str] = None,
                             y_axis_title: Optional[str] = None,
                             use_go: Optional[bool] = None) -> Dict[str, Any]:
        """
        增强的图表创建功能
        
        Args:
            file_path: Excel 文件路径
            chart_type: 图表类型（line, bar, pie 等）
            data_range: 数据范围（如 "A1:C10"）
            chart_title: 图表标题
            sheet_name: 工作表名称
            x_axis_title: X轴标题
            y_axis_title: Y轴标题
            use_go: 强制指定是否使用 Go 服务
            
        Returns:
            Dict: 创建结果
        """
        # 获取server函数
        validate_file_access, create_success_response, create_error_response = self._get_server_functions()
        
        # 验证文件访问
        validation_result = validate_file_access(file_path)
        if validation_result["status"] != "SUCCESS":
            return create_error_response(
                "FILE_ACCESS_ERROR",
                validation_result["message"],
                "请确保文件路径正确且文件存在。"
            )
        
        # 决定使用哪种方法
        should_use_go = use_go if use_go is not None else (self.go_client is not None)
        
        if should_use_go and self.go_client:
            try:
                logger.info(f"Using Go service to create chart in: {file_path}")
                result = self.go_client.create_chart(
                    file_path=file_path,
                    chart_type=chart_type,
                    data_range=data_range,
                    title=chart_title,
                    sheet_name=sheet_name,
                    x_axis_title=x_axis_title,
                    y_axis_title=y_axis_title
                )
                
                if result.get('success', False):
                    return create_success_response({
                        "method": "go_service",
                        "data": result.get('data', {}),
                        "performance": "high"
                    }, "Chart created successfully using Go service")
                else:
                    logger.warning(f"Go service failed: {result.get('error', 'Unknown error')}")
                    return create_error_response(
                        "GO_SERVICE_ERROR",
                        result.get('error', 'Go service failed'),
                        "Go 服务创建图表失败"
                    )
            except Exception as e:
                logger.warning(f"Go service exception: {e}")
                return create_error_response(
                    "GO_SERVICE_EXCEPTION",
                    str(e),
                    "Go 服务异常"
                )
        
        # 目前没有 pandas 的图表创建回退
        return create_error_response(
            "CHART_NOT_SUPPORTED",
            "Chart creation requires Go service",
            "图表创建功能需要 Go 服务支持"
        )
    
    def get_file_info_enhanced(self, file_path: str, use_go: Optional[bool] = None) -> Dict[str, Any]:
        """
        增强的文件信息获取功能
        
        Args:
            file_path: Excel 文件路径
            use_go: 强制指定是否使用 Go 服务
            
        Returns:
            Dict: 文件信息
        """
        # 获取server函数
        validate_file_access, create_success_response, create_error_response = self._get_server_functions()
        
        # 验证文件访问
        validation_result = validate_file_access(file_path)
        if validation_result["status"] != "SUCCESS":
            return create_error_response(
                "FILE_ACCESS_ERROR",
                validation_result["message"],
                "请确保文件路径正确且文件存在。"
            )
        
        # 决定使用哪种方法
        should_use_go = use_go if use_go is not None else (self.go_client is not None)
        
        if should_use_go and self.go_client:
            try:
                logger.info(f"Using Go service to get file info: {file_path}")
                result = self.go_client.get_file_info(file_path)
                
                if result.get('success', False):
                    return create_success_response({
                        "method": "go_service",
                        "data": result.get('data', {}),
                        "performance": "high"
                    }, "File info retrieved successfully using Go service")
                else:
                    logger.warning(f"Go service failed: {result.get('error', 'Unknown error')}")
                    if not self.fallback_to_pandas:
                        return create_error_response(
                            "GO_SERVICE_ERROR",
                            result.get('error', 'Go service failed'),
                            "Go 服务获取文件信息失败"
                        )
            except Exception as e:
                logger.warning(f"Go service exception: {e}")
                if not self.fallback_to_pandas:
                    return create_error_response(
                        "GO_SERVICE_EXCEPTION",
                        str(e),
                        "Go 服务异常"
                    )
        
        # 回退到基本文件信息
        if self.fallback_to_pandas:
            try:
                logger.info(f"Using basic method to get file info: {file_path}")
                
                # 获取基本文件信息
                file_stat = os.stat(file_path)
                file_size = file_stat.st_size
                
                # 尝试读取 Excel 文件获取工作表信息
                try:
                    excel_file = pd.ExcelFile(file_path)
                    sheet_names = excel_file.sheet_names
                    
                    # 获取每个工作表的详细信息
                    sheets_info = {}
                    for sheet in sheet_names:
                        try:
                            # 读取完整数据以获取行数
                            df = pd.read_excel(file_path, sheet_name=sheet)
                            
                            # 使用多级表头检测器获取详细结构信息
                            try:
                                from enhanced_multiheader_detector import EnhancedMultiHeaderDetector
                                with EnhancedMultiHeaderDetector(file_path, sheet) as detector:
                                    structure_analysis = detector.suggest_optimal_parameters()
                                    merged_cells_info = detector.analyze_merged_cells()
                                    
                                    # 构建完整的工作表信息
                                    sheets_info[sheet] = {
                                        "row_count": len(df),
                                        "col_count": len(df.columns),
                                        "column_names": df.columns.tolist(),
                                        "has_data": len(df) > 0,
                                        # 新增：多级表头和合并单元格信息
                                        "multi_level_header": {
                                            "detected": structure_analysis['analysis']['multi_level_header_detected'],
                                            "structure_type": structure_analysis['analysis']['structure_type'],
                                            "confidence": structure_analysis['analysis']['confidence'],
                                            "header_candidates": structure_analysis['analysis']['header_candidates']
                                        },
                                        "merged_cells": {
                                            "count": len(merged_cells_info),
                                            "ranges": [{
                                                "range": cell_info['range'],
                                                "start_row": cell_info['min_row'],
                                                "end_row": cell_info['max_row'],
                                                "start_col": cell_info['min_col'],
                                                "end_col": cell_info['max_col'],
                                                "span_rows": cell_info['span_rows'],
                                                "span_cols": cell_info['span_cols']
                                            } for cell_info in merged_cells_info[:10]]  # 限制返回前10个合并单元格
                                        },
                                        "empty_rows": structure_analysis['analysis']['empty_rows'][:5],  # 限制返回前5个空行
                                        "structure_warnings": structure_analysis.get('warnings', []),
                                        "read_suggestions": structure_analysis.get('tips', [])
                                    }
                            except Exception as detector_error:
                                logger.warning(f"Multi-header detector failed for sheet {sheet}: {detector_error}")
                                # 回退到基本信息
                                sheets_info[sheet] = {
                                    "row_count": len(df),
                                    "col_count": len(df.columns),
                                    "column_names": df.columns.tolist(),
                                    "has_data": len(df) > 0,
                                    "multi_level_header": {
                                        "detected": False,
                                        "error": str(detector_error)
                                    },
                                    "merged_cells": {
                                        "count": 0,
                                        "error": "检测失败"
                                    }
                                }
                                
                        except Exception as e:
                            sheets_info[sheet] = {
                                "error": f"Could not read sheet: {str(e)}",
                                "row_count": 0,
                                "col_count": 0,
                                "has_data": False,
                                "multi_level_header": {"detected": False, "error": "读取失败"},
                                "merged_cells": {"count": 0, "error": "读取失败"}
                            }
                    
                    # 修复：添加文件修改时间和更完整的信息结构
                    import datetime
                    return create_success_response({
                        "method": "pandas_fallback_enhanced",
                        "data": {
                            "file_name": os.path.basename(file_path),
                            "file_size": file_size,
                            "modified_time": datetime.datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                            "sheet_count": len(sheet_names),
                            "sheets": sheets_info,
                            # 新增：整体文件结构分析
                            "file_structure_summary": {
                                "total_merged_cells": sum(sheet.get('merged_cells', {}).get('count', 0) for sheet in sheets_info.values() if isinstance(sheet, dict)),
                                "sheets_with_multi_headers": sum(1 for sheet in sheets_info.values() if isinstance(sheet, dict) and sheet.get('multi_level_header', {}).get('detected', False)),
                                "complex_structure_detected": any(sheet.get('multi_level_header', {}).get('detected', False) or sheet.get('merged_cells', {}).get('count', 0) > 0 for sheet in sheets_info.values() if isinstance(sheet, dict))
                            }
                        },
                        "performance": "enhanced"
                    }, "Enhanced file info retrieved successfully using pandas with structure analysis")
                    
                except Exception as e:
                    return create_error_response(
                        "PANDAS_INFO_ERROR",
                        str(e),
                        "pandas 获取文件信息失败"
                    )
                    
            except Exception as e:
                return create_error_response(
                    "FILE_STAT_ERROR",
                    str(e),
                    "获取文件基本信息失败"
                )
        
        return create_error_response(
            "NO_AVAILABLE_METHOD",
            "All methods failed",
            "所有获取文件信息的方法都失败了"
        )


# 全局处理器实例
_global_processor = None

def get_excel_processor(use_go_service: bool = True, fallback_to_pandas: bool = True) -> ExcelEnhancedProcessor:
    """
    获取全局 Excel 处理器实例
    
    Args:
        use_go_service: 是否使用 Go 服务
        fallback_to_pandas: 是否回退到 pandas
        
    Returns:
        ExcelEnhancedProcessor: 处理器实例
    """
    global _global_processor
    if _global_processor is None:
        _global_processor = ExcelEnhancedProcessor(use_go_service, fallback_to_pandas)
    return _global_processor


# 便捷函数
def read_excel_enhanced(file_path: str, **kwargs) -> Dict[str, Any]:
    """便捷的增强 Excel 读取函数"""
    processor = get_excel_processor()
    return processor.read_excel_enhanced(file_path, **kwargs)

def write_excel_enhanced(file_path: str, data: Union[List[Dict[str, str]], pd.DataFrame], **kwargs) -> Dict[str, Any]:
    """便捷的增强 Excel 写入函数"""
    processor = get_excel_processor()
    return processor.write_excel_enhanced(file_path, data, **kwargs)

def create_chart_enhanced(file_path: str, chart_type: str, data_range: str, **kwargs) -> Dict[str, Any]:
    """便捷的增强图表创建函数"""
    processor = get_excel_processor()
    return processor.create_chart_enhanced(file_path, chart_type, data_range, **kwargs)

def get_file_info_enhanced(file_path: str, **kwargs) -> Dict[str, Any]:
    """便捷的增强文件信息获取函数"""
    processor = get_excel_processor()
    return processor.get_file_info_enhanced(file_path, **kwargs)