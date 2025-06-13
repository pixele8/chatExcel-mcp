#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版 ChatExcel MCP 服务器
集成安全机制、依赖管理和健康监控
"""

import os
import sys
import asyncio
import signal
import logging
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
import traceback
from contextlib import asynccontextmanager

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 导入自定义模块
try:
    from service_management.config_manager import get_config_manager, ConfigManager
    from service_management.health_manager import HealthManager
    from service_management.dependency_manager import DependencyManager
    from security.secure_code_executor import SecureCodeExecutor
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保所有依赖模块都已正确安装")
    sys.exit(1)

# 导入 MCP 相关模块
try:
    from fastmcp import FastMCP
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(f"导入 MCP 依赖失败: {e}")
    print("请运行: pip install fastmcp pandas numpy")
    sys.exit(1)

# 导入原有的服务器模块
try:
    from server import (
        read_metadata, read_excel, write_excel, create_chart,
        get_file_info, run_excel_code, bar_chart_to_html,
        pie_chart_to_html, line_chart_to_html, scatter_chart_to_html,
        create_pivot_table, merge_excel_files, filter_data,
        sort_data, calculate_statistics, validate_data,
        export_to_csv, import_from_csv, create_excel_template,
        batch_process_files, compare_excel_files
    )
except ImportError as e:
    print(f"导入原有服务器模块失败: {e}")
    print("请确保 server.py 文件存在且可导入")
    sys.exit(1)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/enhanced_server.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class EnhancedChatExcelServer:
    """增强版 ChatExcel MCP 服务器"""
    
    def __init__(self):
        self.config_manager: Optional[ConfigManager] = None
        self.health_manager: Optional[HealthManager] = None
        self.dependency_manager: Optional[DependencyManager] = None
        self.secure_executor: Optional[SecureCodeExecutor] = None
        self.mcp_server: Optional[FastMCP] = None
        self.running = False
        self.startup_time = None
        
        # 创建必要的目录
        self._create_directories()
    
    def _create_directories(self):
        """创建必要的目录"""
        directories = [
            'logs',
            'temp',
            'uploads',
            'backups',
            'config',
            'security',
            'service_management'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    async def initialize(self):
        """初始化服务器组件"""
        logger.info("初始化增强版 ChatExcel MCP 服务器...")
        
        try:
            # 初始化配置管理器
            self.config_manager = get_config_manager()
            logger.info("配置管理器初始化完成")
            
            # 获取配置
            security_config = self.config_manager.get_security_config()
            service_config = self.config_manager.get_service_config()
            runtime_config = self.config_manager.get_runtime_config()
            
            # 初始化健康管理器
            self.health_manager = HealthManager()
            await self.health_manager.initialize()
            logger.info("健康管理器初始化完成")
            
            # 初始化依赖管理器
            self.dependency_manager = DependencyManager()
            await self.dependency_manager.initialize()
            logger.info("依赖管理器初始化完成")
            
            # 初始化安全代码执行器
            self.secure_executor = SecureCodeExecutor(
                timeout=security_config.code_execution_timeout,
                memory_limit=security_config.code_execution_memory_limit,
                blacklisted_modules=security_config.blacklisted_modules
            )
            logger.info("安全代码执行器初始化完成")
            
            # 初始化 MCP 服务器
            self.mcp_server = FastMCP("Enhanced ChatExcel MCP")
            self._register_tools()
            logger.info("MCP 服务器初始化完成")
            
            # 注册信号处理器
            self._register_signal_handlers()
            
            # 启动健康检查
            if service_config.health_check_enabled:
                await self.health_manager.start_monitoring()
                logger.info("健康监控已启动")
            
            # 检查依赖
            dependency_status = await self.dependency_manager.check_all_dependencies()
            if not dependency_status['all_healthy']:
                logger.warning(f"部分依赖不健康: {dependency_status}")
            
            self.startup_time = time.time()
            logger.info("服务器初始化完成")
            
        except Exception as e:
            logger.error(f"服务器初始化失败: {e}")
            logger.error(traceback.format_exc())
            raise
    
    def _register_tools(self):
        """注册 MCP 工具"""
        if not self.mcp_server:
            return
        
        # 注册原有工具（包装为安全版本）
        tools = [
            ("read_metadata", self._secure_read_metadata),
            ("read_excel", self._secure_read_excel),
            ("write_excel", self._secure_write_excel),
            ("create_chart", self._secure_create_chart),
            ("get_file_info", self._secure_get_file_info),
            ("run_excel_code", self._secure_run_excel_code),
            ("bar_chart_to_html", self._secure_bar_chart_to_html),
            ("pie_chart_to_html", self._secure_pie_chart_to_html),
            ("line_chart_to_html", self._secure_line_chart_to_html),
            ("scatter_chart_to_html", self._secure_scatter_chart_to_html),
            ("create_pivot_table", self._secure_create_pivot_table),
            ("merge_excel_files", self._secure_merge_excel_files),
            ("filter_data", self._secure_filter_data),
            ("sort_data", self._secure_sort_data),
            ("calculate_statistics", self._secure_calculate_statistics),
            ("validate_data", self._secure_validate_data),
            ("export_to_csv", self._secure_export_to_csv),
            ("import_from_csv", self._secure_import_from_csv),
            ("create_excel_template", self._secure_create_excel_template),
            ("batch_process_files", self._secure_batch_process_files),
            ("compare_excel_files", self._secure_compare_excel_files)
        ]
        
        # 注册新的管理工具
        management_tools = [
            ("get_server_status", self._get_server_status),
            ("get_health_status", self._get_health_status),
            ("get_dependency_status", self._get_dependency_status),
            ("get_security_status", self._get_security_status),
            ("restart_service", self._restart_service),
            ("update_config", self._update_config),
            ("create_backup", self._create_backup),
            ("get_metrics", self._get_metrics)
        ]
        
        # 注册所有工具
        for tool_name, tool_func in tools + management_tools:
            self.mcp_server.tool()(tool_func)
            logger.debug(f"注册工具: {tool_name}")
    
    def _register_signal_handlers(self):
        """注册信号处理器"""
        def signal_handler(signum, frame):
            logger.info(f"收到信号 {signum}，开始优雅关闭...")
            asyncio.create_task(self.shutdown())
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def _validate_request(self, **kwargs) -> bool:
        """验证请求"""
        try:
            security_config = self.config_manager.get_security_config()
            
            # 检查文件大小
            if 'file_path' in kwargs:
                file_path = Path(kwargs['file_path'])
                if file_path.exists():
                    file_size = file_path.stat().st_size
                    if file_size > security_config.max_file_size:
                        logger.warning(f"文件大小超限: {file_size} > {security_config.max_file_size}")
                        return False
            
            # 检查文件类型
            if 'file_path' in kwargs:
                file_path = Path(kwargs['file_path'])
                if file_path.suffix.lower() not in security_config.allowed_file_types:
                    logger.warning(f"不允许的文件类型: {file_path.suffix}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"请求验证失败: {e}")
            return False
    
    async def _log_request(self, tool_name: str, **kwargs):
        """记录请求日志"""
        try:
            security_config = self.config_manager.get_security_config()
            
            if security_config.audit_log_enabled:
                # 过滤敏感信息
                safe_kwargs = {}
                for key, value in kwargs.items():
                    if key in ['password', 'token', 'secret', 'key']:
                        safe_kwargs[key] = "[REDACTED]"
                    else:
                        safe_kwargs[key] = str(value)[:100]  # 限制长度
                
                audit_log = logging.getLogger('audit')
                audit_log.info(f"工具调用: {tool_name}, 参数: {safe_kwargs}")
        
        except Exception as e:
            logger.error(f"记录请求日志失败: {e}")
    
    # 安全包装器方法
    async def _secure_read_metadata(self, **kwargs):
        """安全的读取元数据"""
        await self._log_request("read_metadata", **kwargs)
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        return await read_metadata(**kwargs)
    
    async def _secure_read_excel(self, **kwargs):
        """安全的读取 Excel"""
        await self._log_request("read_excel", **kwargs)
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        return await read_excel(**kwargs)
    
    async def _secure_write_excel(self, **kwargs):
        """安全的写入 Excel"""
        await self._log_request("write_excel", **kwargs)
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        return await write_excel(**kwargs)
    
    async def _secure_create_chart(self, **kwargs):
        """安全的创建图表"""
        await self._log_request("create_chart", **kwargs)
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        return await create_chart(**kwargs)
    
    async def _secure_get_file_info(self, **kwargs):
        """安全的获取文件信息"""
        await self._log_request("get_file_info", **kwargs)
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        return await get_file_info(**kwargs)
    
    async def _secure_run_excel_code(self, **kwargs):
        """安全的运行 Excel 代码"""
        await self._log_request("run_excel_code", **kwargs)
        
        security_config = self.config_manager.get_security_config()
        if not security_config.code_execution_enabled:
            return {"error": "代码执行功能已禁用"}
        
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        
        # 使用安全执行器
        try:
            code = kwargs.get('code', '')
            context = kwargs.get('context', {})
            
            result = await self.secure_executor.execute_code(code, context)
            return {"success": True, "result": result}
            
        except Exception as e:
            logger.error(f"安全代码执行失败: {e}")
            return {"error": f"代码执行失败: {str(e)}"}
    
    async def _secure_bar_chart_to_html(self, **kwargs):
        """安全的柱状图生成"""
        await self._log_request("bar_chart_to_html", **kwargs)
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        return await bar_chart_to_html(**kwargs)
    
    async def _secure_pie_chart_to_html(self, **kwargs):
        """安全的饼图生成"""
        await self._log_request("pie_chart_to_html", **kwargs)
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        return await pie_chart_to_html(**kwargs)
    
    async def _secure_line_chart_to_html(self, **kwargs):
        """安全的折线图生成"""
        await self._log_request("line_chart_to_html", **kwargs)
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        return await line_chart_to_html(**kwargs)
    
    async def _secure_scatter_chart_to_html(self, **kwargs):
        """安全的散点图生成"""
        await self._log_request("scatter_chart_to_html", **kwargs)
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        return await scatter_chart_to_html(**kwargs)
    
    async def _secure_create_pivot_table(self, **kwargs):
        """安全的数据透视表创建"""
        await self._log_request("create_pivot_table", **kwargs)
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        return await create_pivot_table(**kwargs)
    
    async def _secure_merge_excel_files(self, **kwargs):
        """安全的 Excel 文件合并"""
        await self._log_request("merge_excel_files", **kwargs)
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        return await merge_excel_files(**kwargs)
    
    async def _secure_filter_data(self, **kwargs):
        """安全的数据过滤"""
        await self._log_request("filter_data", **kwargs)
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        return await filter_data(**kwargs)
    
    async def _secure_sort_data(self, **kwargs):
        """安全的数据排序"""
        await self._log_request("sort_data", **kwargs)
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        return await sort_data(**kwargs)
    
    async def _secure_calculate_statistics(self, **kwargs):
        """安全的统计计算"""
        await self._log_request("calculate_statistics", **kwargs)
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        return await calculate_statistics(**kwargs)
    
    async def _secure_validate_data(self, **kwargs):
        """安全的数据验证"""
        await self._log_request("validate_data", **kwargs)
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        return await validate_data(**kwargs)
    
    async def _secure_export_to_csv(self, **kwargs):
        """安全的 CSV 导出"""
        await self._log_request("export_to_csv", **kwargs)
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        return await export_to_csv(**kwargs)
    
    async def _secure_import_from_csv(self, **kwargs):
        """安全的 CSV 导入"""
        await self._log_request("import_from_csv", **kwargs)
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        return await import_from_csv(**kwargs)
    
    async def _secure_create_excel_template(self, **kwargs):
        """安全的 Excel 模板创建"""
        await self._log_request("create_excel_template", **kwargs)
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        return await create_excel_template(**kwargs)
    
    async def _secure_batch_process_files(self, **kwargs):
        """安全的批量文件处理"""
        await self._log_request("batch_process_files", **kwargs)
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        return await batch_process_files(**kwargs)
    
    async def _secure_compare_excel_files(self, **kwargs):
        """安全的 Excel 文件比较"""
        await self._log_request("compare_excel_files", **kwargs)
        if not await self._validate_request(**kwargs):
            return {"error": "请求验证失败"}
        return await compare_excel_files(**kwargs)
    
    # 管理工具
    async def _get_server_status(self):
        """获取服务器状态"""
        uptime = time.time() - self.startup_time if self.startup_time else 0
        
        return {
            "status": "running" if self.running else "stopped",
            "uptime": uptime,
            "startup_time": self.startup_time,
            "version": "1.0.0-enhanced",
            "components": {
                "config_manager": self.config_manager is not None,
                "health_manager": self.health_manager is not None,
                "dependency_manager": self.dependency_manager is not None,
                "secure_executor": self.secure_executor is not None
            }
        }
    
    async def _get_health_status(self):
        """获取健康状态"""
        if not self.health_manager:
            return {"error": "健康管理器未初始化"}
        
        return await self.health_manager.get_health_status()
    
    async def _get_dependency_status(self):
        """获取依赖状态"""
        if not self.dependency_manager:
            return {"error": "依赖管理器未初始化"}
        
        return await self.dependency_manager.check_all_dependencies()
    
    async def _get_security_status(self):
        """获取安全状态"""
        if not self.config_manager:
            return {"error": "配置管理器未初始化"}
        
        security_config = self.config_manager.get_security_config()
        
        return {
            "api_key_required": security_config.api_key_required,
            "rate_limit_enabled": security_config.rate_limit_enabled,
            "code_execution_enabled": security_config.code_execution_enabled,
            "ssl_enabled": security_config.ssl_enabled,
            "audit_log_enabled": security_config.audit_log_enabled,
            "max_file_size": security_config.max_file_size,
            "allowed_file_types": security_config.allowed_file_types
        }
    
    async def _restart_service(self, service_name: str):
        """重启服务"""
        if not self.health_manager:
            return {"error": "健康管理器未初始化"}
        
        try:
            result = await self.health_manager.restart_service(service_name)
            return {"success": True, "result": result}
        except Exception as e:
            return {"error": f"重启服务失败: {str(e)}"}
    
    async def _update_config(self, path: str, value: Any, persist: bool = False):
        """更新配置"""
        if not self.config_manager:
            return {"error": "配置管理器未初始化"}
        
        try:
            self.config_manager.set(path, value, persist)
            return {"success": True, "message": f"配置 {path} 已更新"}
        except Exception as e:
            return {"error": f"更新配置失败: {str(e)}"}
    
    async def _create_backup(self):
        """创建备份"""
        if not self.config_manager:
            return {"error": "配置管理器未初始化"}
        
        try:
            backup_file = self.config_manager.create_backup()
            return {"success": True, "backup_file": str(backup_file)}
        except Exception as e:
            return {"error": f"创建备份失败: {str(e)}"}
    
    async def _get_metrics(self):
        """获取指标"""
        metrics = {
            "timestamp": time.time(),
            "uptime": time.time() - self.startup_time if self.startup_time else 0
        }
        
        # 添加健康指标
        if self.health_manager:
            health_status = await self.health_manager.get_health_status()
            metrics["health"] = health_status
        
        # 添加依赖指标
        if self.dependency_manager:
            dependency_status = await self.dependency_manager.check_all_dependencies()
            metrics["dependencies"] = dependency_status
        
        return metrics
    
    async def run(self):
        """运行服务器"""
        try:
            await self.initialize()
            
            self.running = True
            logger.info("增强版 ChatExcel MCP 服务器启动成功")
            
            # 运行 MCP 服务器
            if self.mcp_server:
                await self.mcp_server.run()
            
        except Exception as e:
            logger.error(f"服务器运行失败: {e}")
            logger.error(traceback.format_exc())
            raise
        finally:
            await self.shutdown()
    
    async def shutdown(self):
        """关闭服务器"""
        logger.info("开始关闭服务器...")
        
        self.running = False
        
        try:
            # 停止健康监控
            if self.health_manager:
                await self.health_manager.stop_monitoring()
                logger.info("健康监控已停止")
            
            # 关闭配置管理器
            if self.config_manager:
                self.config_manager.shutdown()
                logger.info("配置管理器已关闭")
            
            # 停止 MCP 服务器
            if self.mcp_server:
                # FastMCP 可能没有显式的停止方法
                logger.info("MCP 服务器已停止")
            
            logger.info("服务器已优雅关闭")
            
        except Exception as e:
            logger.error(f"关闭服务器时出错: {e}")

async def main():
    """主函数"""
    server = EnhancedChatExcelServer()
    
    try:
        await server.run()
    except KeyboardInterrupt:
        logger.info("收到中断信号")
    except Exception as e:
        logger.error(f"服务器异常: {e}")
        logger.error(traceback.format_exc())
    finally:
        await server.shutdown()

if __name__ == "__main__":
    # 确保事件循环策略兼容
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"启动失败: {e}")
        sys.exit(1)