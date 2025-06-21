# -*- coding: utf-8 -*-
"""
Excel Go Client
提供与 Go Excel 服务的客户端接口
"""

import os
import json
import logging
import subprocess
import time
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import pandas as pd
import requests
from dataclasses import dataclass

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class GoServiceConfig:
    """Go 服务配置"""
    host: str = "localhost"
    port: int = 8080
    timeout: int = 30
    max_retries: int = 3
    
    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"

class ExcelGoClient:
    """Excel Go 服务客户端"""
    
    def __init__(self, config: GoServiceConfig = None, auto_start: bool = False):
        """
        初始化 Go 客户端
        
        Args:
            config: 服务配置
            auto_start: 是否自动启动服务
        """
        self.config = config or GoServiceConfig()
        self.session = requests.Session()
        self.session.timeout = self.config.timeout
        self._service_process = None
        
        if auto_start:
            self.start_service()
    
    def start_service(self) -> bool:
        """
        启动 Go 服务
        
        Returns:
            是否启动成功
        """
        try:
            # 检查服务是否已经运行
            if self.health_check().get('success', False):
                logger.info("Go service is already running")
                return True
            
            # 查找 Go 服务可执行文件
            go_service_path = self._find_go_service()
            if not go_service_path:
                logger.warning("Go service executable not found")
                return False
            
            # 启动服务
            cmd = [go_service_path, f"--port={self.config.port}"]
            self._service_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=Path(__file__).parent
            )
            
            # 等待服务启动
            for _ in range(10):
                time.sleep(1)
                if self.health_check().get('success', False):
                    logger.info(f"Go service started successfully on port {self.config.port}")
                    return True
            
            logger.error("Go service failed to start within timeout")
            return False
            
        except Exception as e:
            logger.error(f"Failed to start Go service: {e}")
            return False
    
    def _find_go_service(self) -> Optional[str]:
        """
        查找 Go 服务可执行文件
        
        Returns:
            可执行文件路径
        """
        possible_paths = [
            "./excel-service/excel-service",
            "./excel-service/excel-service.exe",
            "./bin/excel-service",
            "./bin/excel-service.exe",
            "excel-service",
            "excel-service.exe"
        ]
        
        for path in possible_paths:
            full_path = Path(path).resolve()
            if full_path.exists() and full_path.is_file():
                return str(full_path)
        
        return None
    
    def health_check(self) -> Dict[str, Any]:
        """
        健康检查
        
        Returns:
            健康状态
        """
        try:
            response = self.session.get(f"{self.config.base_url}/health")
            if response.status_code == 200:
                return {"success": True, "status": "healthy"}
            else:
                return {"success": False, "status": "unhealthy", "code": response.status_code}
        except Exception as e:
            return {"success": False, "status": "unreachable", "error": str(e)}
    
    def read_excel(self, file_path: str, sheet_name: str = None, **kwargs) -> Dict[str, Any]:
        """
        读取 Excel 文件
        
        Args:
            file_path: 文件路径
            sheet_name: 工作表名称
            **kwargs: 其他参数
            
        Returns:
            读取结果
        """
        try:
            data = {
                "file_path": file_path,
                "sheet_name": sheet_name,
                **kwargs
            }
            
            response = self.session.post(
                f"{self.config.base_url}/read",
                json=data
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def write_excel(self, data: List[List], file_path: str, sheet_name: str = "Sheet1", **kwargs) -> Dict[str, Any]:
        """
        写入 Excel 文件
        
        Args:
            data: 数据
            file_path: 文件路径
            sheet_name: 工作表名称
            **kwargs: 其他参数
            
        Returns:
            写入结果
        """
        try:
            payload = {
                "data": data,
                "file_path": file_path,
                "sheet_name": sheet_name,
                **kwargs
            }
            
            response = self.session.post(
                f"{self.config.base_url}/write",
                json=payload
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_chart(self, file_path: str, chart_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建图表
        
        Args:
            file_path: 文件路径
            chart_config: 图表配置
            
        Returns:
            创建结果
        """
        try:
            data = {
                "file_path": file_path,
                "chart_config": chart_config
            }
            
            response = self.session.post(
                f"{self.config.base_url}/chart",
                json=data
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        获取文件信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件信息
        """
        try:
            response = self.session.get(
                f"{self.config.base_url}/info",
                params={"file_path": file_path}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def stop_service(self):
        """
        停止服务
        """
        if self._service_process:
            try:
                self._service_process.terminate()
                self._service_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._service_process.kill()
            finally:
                self._service_process = None
    
    def __del__(self):
        """析构函数"""
        self.stop_service()

# 全局客户端实例
_global_client = None

def get_global_client() -> ExcelGoClient:
    """获取全局客户端实例"""
    global _global_client
    if _global_client is None:
        _global_client = ExcelGoClient(auto_start=False)
    return _global_client

def read_excel_fast(file_path: str, sheet_name: str = None, **kwargs) -> pd.DataFrame:
    """
    快速读取 Excel 文件
    
    Args:
        file_path: 文件路径
        sheet_name: 工作表名称
        **kwargs: 其他参数
        
    Returns:
        DataFrame
    """
    try:
        client = get_global_client()
        result = client.read_excel(file_path, sheet_name, **kwargs)
        
        if result.get('success', False):
            # 将结果转换为 DataFrame
            data = result.get('data', [])
            if data:
                return pd.DataFrame(data[1:], columns=data[0])
            else:
                return pd.DataFrame()
        else:
            # 回退到 pandas
            logger.warning(f"Go service failed, falling back to pandas: {result.get('error')}")
            return pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
            
    except Exception as e:
        logger.warning(f"Fast read failed, falling back to pandas: {e}")
        return pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)

def write_excel_fast(df: pd.DataFrame, file_path: str, sheet_name: str = "Sheet1", **kwargs) -> bool:
    """
    快速写入 Excel 文件
    
    Args:
        df: DataFrame
        file_path: 文件路径
        sheet_name: 工作表名称
        **kwargs: 其他参数
        
    Returns:
        是否成功
    """
    try:
        client = get_global_client()
        
        # 转换 DataFrame 为列表格式
        data = [df.columns.tolist()] + df.values.tolist()
        
        result = client.write_excel(data, file_path, sheet_name, **kwargs)
        
        if result.get('success', False):
            return True
        else:
            # 回退到 pandas
            logger.warning(f"Go service failed, falling back to pandas: {result.get('error')}")
            df.to_excel(file_path, sheet_name=sheet_name, index=False, **kwargs)
            return True
            
    except Exception as e:
        logger.warning(f"Fast write failed, falling back to pandas: {e}")
        try:
            df.to_excel(file_path, sheet_name=sheet_name, index=False, **kwargs)
            return True
        except Exception as fallback_error:
            logger.error(f"Pandas fallback also failed: {fallback_error}")
            return False

def create_chart_fast(file_path: str, chart_config: Dict[str, Any]) -> bool:
    """
    快速创建图表
    
    Args:
        file_path: 文件路径
        chart_config: 图表配置
        
    Returns:
        是否成功
    """
    try:
        client = get_global_client()
        result = client.create_chart(file_path, chart_config)
        return result.get('success', False)
    except Exception as e:
        logger.error(f"Chart creation failed: {e}")
        return False

def get_file_info_fast(file_path: str) -> Dict[str, Any]:
    """
    快速获取文件信息
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件信息
    """
    try:
        client = get_global_client()
        result = client.get_file_info(file_path)
        
        if result.get('success', False):
            return result
        else:
            # 回退到基本信息
            path = Path(file_path)
            if path.exists():
                stat = path.stat()
                return {
                    "success": True,
                    "file_size": stat.st_size,
                    "modified_time": stat.st_mtime,
                    "exists": True
                }
            else:
                return {"success": False, "exists": False}
                
    except Exception as e:
        logger.error(f"Get file info failed: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # 测试代码
    import sys
    
    if "--test" in sys.argv:
        print("Testing Excel Go Client...")
        
        client = ExcelGoClient(auto_start=True)
        health = client.health_check()
        print(f"Health check: {health}")
        
        if health.get('success', False):
            print("Go service is running")
        else:
            print("Go service is not available, will use pandas fallback")
        
        client.stop_service()
        print("Test completed")