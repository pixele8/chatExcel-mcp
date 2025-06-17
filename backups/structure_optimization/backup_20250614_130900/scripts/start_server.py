#!/usr/bin/env python3
"""
ChatExcel MCP Server 启动脚本
企业级增强版服务器启动工具
"""

import os
import sys
import subprocess
import json
import signal
import time
from pathlib import Path
from typing import Dict, List, Optional
import argparse

class Colors:
    """终端颜色常量"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class ServerManager:
    """服务器管理器"""
    
    def __init__(self, server_type: str = 'enhanced'):
        self.project_root = Path(__file__).parent.parent
        self.server_type = server_type
        self.processes = []
        self.config = self._load_config()
        
        # 注册信号处理器
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        config_file = self.project_root / 'config' / 'system.json'
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"{Colors.YELLOW}⚠️ 配置文件加载失败，使用默认配置: {e}{Colors.END}")
        
        # 默认配置
        return {
            "service": {
                "name": "chatexcel-mcp",
                "host": "localhost",
                "port": 8080,
                "debug": False,
                "workers": 1
            },
            "go_service": {
                "name": "go-excel-service",
                "host": "localhost",
                "port": 8081
            }
        }
    
    def _signal_handler(self, signum, frame):
        """信号处理器"""
        print(f"\n{Colors.YELLOW}🛑 接收到停止信号，正在关闭服务...{Colors.END}")
        self.stop_all_services()
        sys.exit(0)
    
    def print_header(self):
        """打印启动头信息"""
        print(f"{Colors.CYAN}{Colors.BOLD}" + "="*60)
        print("    ChatExcel MCP Server - 企业级增强版")
        print(f"    服务器启动工具 ({self.server_type.upper()})")
        print("="*60 + f"{Colors.END}")
        print(f"{Colors.BLUE}配置信息:{Colors.END}")
        print(f"  服务类型: {self.server_type}")
        print(f"  主机地址: {self.config['service']['host']}")
        print(f"  端口号: {self.config['service']['port']}")
        print()
    
    def check_dependencies(self) -> bool:
        """检查依赖"""
        print(f"{Colors.YELLOW}🔍 检查依赖...{Colors.END}")
        
        # 检查Python模块
        required_modules = ['fastmcp', 'mcp', 'pandas', 'numpy']
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module)
                print(f"  ✅ {module}")
            except ImportError:
                missing_modules.append(module)
                print(f"  ❌ {module}")
        
        if missing_modules:
            print(f"{Colors.RED}❌ 缺少必要模块: {', '.join(missing_modules)}{Colors.END}")
            print(f"{Colors.BLUE}💡 请运行: pip install -r requirements.txt{Colors.END}")
            return False
        
        print(f"{Colors.GREEN}✅ 依赖检查完成{Colors.END}")
        return True
    
    def start_go_service(self) -> bool:
        """启动Go服务"""
        go_service_path = self.project_root / 'excel-service' / 'excel_service'
        
        if not go_service_path.exists():
            print(f"{Colors.YELLOW}⚠️ Go服务不存在，跳过启动{Colors.END}")
            return True
        
        print(f"{Colors.YELLOW}🚀 启动Go Excel服务...{Colors.END}")
        
        try:
            # 设置环境变量
            env = os.environ.copy()
            env['PORT'] = str(self.config['go_service']['port'])
            env['HOST'] = self.config['go_service']['host']
            
            # 启动Go服务
            process = subprocess.Popen(
                [str(go_service_path)],
                cwd=go_service_path.parent,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.processes.append(('go-service', process))
            
            # 等待服务启动
            time.sleep(2)
            
            if process.poll() is None:
                print(f"{Colors.GREEN}✅ Go服务启动成功 (PID: {process.pid}){Colors.END}")
                return True
            else:
                stdout, stderr = process.communicate()
                print(f"{Colors.RED}❌ Go服务启动失败{Colors.END}")
                if stderr:
                    print(f"错误: {stderr.decode()}")
                return False
        
        except Exception as e:
            print(f"{Colors.RED}❌ Go服务启动异常: {e}{Colors.END}")
            return False
    
    def start_python_service(self) -> bool:
        """启动Python MCP服务"""
        if self.server_type == 'enhanced':
            server_file = 'enhanced_server.py'
            service_name = '增强版MCP服务'
        else:
            server_file = 'server.py'
            service_name = '标准MCP服务'
        
        server_path = self.project_root / server_file
        
        if not server_path.exists():
            print(f"{Colors.RED}❌ 服务器文件不存在: {server_file}{Colors.END}")
            return False
        
        print(f"{Colors.YELLOW}🚀 启动{service_name}...{Colors.END}")
        
        try:
            # 设置环境变量
            env = os.environ.copy()
            env['PYTHONPATH'] = str(self.project_root)
            env['MCP_SERVER_HOST'] = self.config['service']['host']
            env['MCP_SERVER_PORT'] = str(self.config['service']['port'])
            
            # 启动Python服务
            process = subprocess.Popen(
                [sys.executable, str(server_path)],
                cwd=self.project_root,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            self.processes.append(('python-service', process))
            
            # 实时显示输出
            print(f"{Colors.BLUE}📋 服务器日志:{Colors.END}")
            print("-" * 50)
            
            try:
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        print(output.strip())
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}🛑 用户中断服务{Colors.END}")
                return False
            
            return process.poll() == 0
        
        except Exception as e:
            print(f"{Colors.RED}❌ Python服务启动异常: {e}{Colors.END}")
            return False
    
    def stop_all_services(self):
        """停止所有服务"""
        print(f"{Colors.YELLOW}🛑 停止所有服务...{Colors.END}")
        
        for service_name, process in self.processes:
            try:
                if process.poll() is None:
                    print(f"  停止 {service_name} (PID: {process.pid})")
                    process.terminate()
                    
                    # 等待进程结束
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        print(f"  强制终止 {service_name}")
                        process.kill()
                        process.wait()
                    
                    print(f"  ✅ {service_name} 已停止")
            except Exception as e:
                print(f"  ❌ 停止 {service_name} 失败: {e}")
        
        self.processes.clear()
    
    def show_status(self):
        """显示服务状态"""
        print(f"{Colors.BLUE}📊 服务状态:{Colors.END}")
        
        if not self.processes:
            print("  没有运行中的服务")
            return
        
        for service_name, process in self.processes:
            if process.poll() is None:
                print(f"  ✅ {service_name} (PID: {process.pid}) - 运行中")
            else:
                print(f"  ❌ {service_name} - 已停止")
    
    def start(self) -> bool:
        """启动所有服务"""
        self.print_header()
        
        # 检查依赖
        if not self.check_dependencies():
            return False
        
        # 启动Go服务（如果存在）
        if not self.start_go_service():
            print(f"{Colors.YELLOW}⚠️ Go服务启动失败，继续启动Python服务{Colors.END}")
        
        # 启动Python服务
        return self.start_python_service()

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='ChatExcel MCP Server 启动工具')
    parser.add_argument(
        '--type', 
        choices=['enhanced', 'standard'], 
        default='enhanced',
        help='服务器类型 (默认: enhanced)'
    )
    parser.add_argument(
        '--status', 
        action='store_true',
        help='显示服务状态'
    )
    parser.add_argument(
        '--stop', 
        action='store_true',
        help='停止所有服务'
    )
    
    args = parser.parse_args()
    
    try:
        manager = ServerManager(args.type)
        
        if args.status:
            manager.show_status()
        elif args.stop:
            manager.stop_all_services()
        else:
            success = manager.start()
            if not success:
                sys.exit(1)
    
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️ 启动被用户中断{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}❌ 启动过程中发生错误: {e}{Colors.END}")
        sys.exit(1)

if __name__ == '__main__':
    main()