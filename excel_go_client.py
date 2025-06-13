#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel Go Service Client

提供与 Go Excel 服务通信的 Python 客户端，实现高性能 Excel 操作。
"""

import json
import requests
import subprocess
import time
import os
import signal
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExcelGoClient:
    """Excel Go 服务客户端"""
    
    def __init__(self, service_url: str = "http://localhost:8080", auto_start: bool = True):
        """
        初始化 Excel Go 客户端
        
        Args:
            service_url: Go 服务的 URL
            auto_start: 是否自动启动 Go 服务
        """
        self.service_url = service_url.rstrip('/')
        self.api_base = f"{self.service_url}/api/v1"
        self.process = None
        self.auto_start = auto_start
        
        if auto_start:
            self._ensure_service_running()
    
    def _ensure_service_running(self) -> bool:
        """确保 Go 服务正在运行"""
        try:
            # 检查服务是否已经运行
            response = requests.get(f"{self.api_base}/health", timeout=2)
            if response.status_code == 200:
                logger.info("Excel Go service is already running")
                return True
        except requests.exceptions.RequestException:
            pass
        
        # 启动 Go 服务
        return self._start_service()
    
    def _start_service(self) -> bool:
        """启动 Go 服务"""
        try:
            # 获取当前脚本所在目录
            current_dir = Path(__file__).parent
            service_dir = current_dir / "excel-service"
            
            if not service_dir.exists():
                logger.error(f"Excel service directory not found: {service_dir}")
                return False
            
            # 构建 Go 服务（如果需要）
            go_mod_path = service_dir / "go.mod"
            if go_mod_path.exists():
                logger.info("Building Go service...")
                build_result = subprocess.run(
                    ["go", "build", "-o", "excel-service", "."],
                    cwd=service_dir,
                    capture_output=True,
                    text=True
                )
                
                if build_result.returncode != 0:
                    logger.error(f"Failed to build Go service: {build_result.stderr}")
                    return False
            
            # 启动服务
            logger.info("Starting Excel Go service...")
            self.process = subprocess.Popen(
                ["./excel-service"],
                cwd=service_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, "PORT": "8080"}
            )
            
            # 等待服务启动
            for _ in range(30):  # 最多等待30秒
                try:
                    response = requests.get(f"{self.api_base}/health", timeout=1)
                    if response.status_code == 200:
                        logger.info("Excel Go service started successfully")
                        return True
                except requests.exceptions.RequestException:
                    pass
                time.sleep(1)
            
            logger.error("Failed to start Excel Go service")
            return False
            
        except Exception as e:
            logger.error(f"Error starting Go service: {e}")
            return False
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict[str, Any]:
        """发送 HTTP 请求"""
        url = f"{self.api_base}/{endpoint.lstrip('/')}"
        
        # 绕过系统代理设置，直接访问本地服务
        proxies = {
            'http': None,
            'https': None
        }
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, params=params, timeout=30, proxies=proxies)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, timeout=30, proxies=proxies)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
    
    def read_excel(self, 
                   file_path: str, 
                   sheet_name: Optional[str] = None,
                   start_row: Optional[int] = None,
                   end_row: Optional[int] = None,
                   start_col: Optional[str] = None,
                   end_col: Optional[str] = None) -> Dict[str, Any]:
        """
        读取 Excel 文件
        
        Args:
            file_path: Excel 文件路径
            sheet_name: 工作表名称（可选）
            start_row: 起始行（可选）
            end_row: 结束行（可选）
            start_col: 起始列（可选）
            end_col: 结束列（可选）
            
        Returns:
            Dict: 包含读取结果的字典
        """
        data = {
            "file_path": file_path
        }
        
        if sheet_name:
            data["sheet_name"] = sheet_name
        if start_row is not None:
            data["start_row"] = start_row
        if end_row is not None:
            data["end_row"] = end_row
        if start_col:
            data["start_col"] = start_col
        if end_col:
            data["end_col"] = end_col
        
        return self._make_request("POST", "/read", data)
    
    def write_excel(self, 
                    file_path: str, 
                    data: List[Dict[str, str]], 
                    sheet_name: Optional[str] = None,
                    start_row: Optional[int] = None,
                    start_col: Optional[str] = None) -> Dict[str, Any]:
        """
        写入 Excel 文件
        
        Args:
            file_path: Excel 文件路径
            data: 要写入的数据
            sheet_name: 工作表名称（可选）
            start_row: 起始行（可选）
            start_col: 起始列（可选）
            
        Returns:
            Dict: 包含写入结果的字典
        """
        request_data = {
            "file_path": file_path,
            "data": data
        }
        
        if sheet_name:
            request_data["sheet_name"] = sheet_name
        if start_row is not None:
            request_data["start_row"] = start_row
        if start_col:
            request_data["start_col"] = start_col
        
        return self._make_request("POST", "/write", request_data)
    
    def create_chart(self, 
                     file_path: str, 
                     chart_type: str, 
                     data_range: str,
                     sheet_name: Optional[str] = None,
                     title: Optional[str] = None,
                     x_axis_title: Optional[str] = None,
                     y_axis_title: Optional[str] = None) -> Dict[str, Any]:
        """
        创建图表
        
        Args:
            file_path: Excel 文件路径
            chart_type: 图表类型（如 'col', 'line', 'pie' 等）
            data_range: 数据范围（如 'A1:B10'）
            sheet_name: 工作表名称（可选）
            title: 图表标题（可选）
            x_axis_title: X轴标题（可选）
            y_axis_title: Y轴标题（可选）
            
        Returns:
            Dict: 包含创建结果的字典
        """
        data = {
            "file_path": file_path,
            "chart_type": chart_type,
            "data_range": data_range
        }
        
        if sheet_name:
            data["sheet_name"] = sheet_name
        if title:
            data["title"] = title
        if x_axis_title:
            data["x_axis_title"] = x_axis_title
        if y_axis_title:
            data["y_axis_title"] = y_axis_title
        
        return self._make_request("POST", "/chart", data)
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        获取 Excel 文件信息
        
        Args:
            file_path: Excel 文件路径
            
        Returns:
            Dict: 包含文件信息的字典
        """
        return self._make_request("GET", "/file-info", params={"file_path": file_path})
    
    def health_check(self) -> Dict[str, Any]:
        """
        健康检查
        
        Returns:
            Dict: 包含服务状态的字典
        """
        return self._make_request("GET", "/health")
    
    def stop_service(self):
        """停止 Go 服务"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                logger.info("Excel Go service stopped")
            except subprocess.TimeoutExpired:
                self.process.kill()
                logger.warning("Excel Go service force killed")
            except Exception as e:
                logger.error(f"Error stopping service: {e}")
            finally:
                self.process = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_service()


# 便捷函数
def read_excel_fast(file_path: str, **kwargs) -> Dict[str, Any]:
    """快速读取 Excel 文件"""
    with ExcelGoClient() as client:
        return client.read_excel(file_path, **kwargs)

def write_excel_fast(file_path: str, data: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
    """快速写入 Excel 文件"""
    with ExcelGoClient() as client:
        return client.write_excel(file_path, data, **kwargs)

def create_chart_fast(file_path: str, chart_type: str, data_range: str, **kwargs) -> Dict[str, Any]:
    """快速创建图表"""
    with ExcelGoClient() as client:
        return client.create_chart(file_path, chart_type, data_range, **kwargs)

def get_file_info_fast(file_path: str) -> Dict[str, Any]:
    """快速获取文件信息"""
    with ExcelGoClient() as client:
        return client.get_file_info(file_path)


if __name__ == "__main__":
    # 测试代码
    client = ExcelGoClient()
    
    # 健康检查
    health = client.health_check()
    print(f"Health check: {health}")
    
    # 停止服务
    client.stop_service()