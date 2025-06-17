#!/usr/bin/env python3
"""
ChatExcel MCP Server 自动部署脚本
企业级增强版自动化部署工具
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path
import platform
import time
from typing import Dict, List, Optional

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

class DeploymentManager:
    """部署管理器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.system_info = self._get_system_info()
        self.errors = []
        self.warnings = []
        
    def _get_system_info(self) -> Dict:
        """获取系统信息"""
        return {
            'platform': platform.system(),
            'architecture': platform.machine(),
            'python_version': sys.version,
            'python_executable': sys.executable
        }
    
    def print_header(self):
        """打印部署头信息"""
        print(f"{Colors.CYAN}{Colors.BOLD}" + "="*60)
        print("    ChatExcel MCP Server - 企业级增强版")
        print("    自动化部署工具")
        print("="*60 + f"{Colors.END}")
        print(f"{Colors.BLUE}系统信息:{Colors.END}")
        print(f"  平台: {self.system_info['platform']}")
        print(f"  架构: {self.system_info['architecture']}")
        print(f"  Python: {sys.version.split()[0]}")
        print()
    
    def check_prerequisites(self) -> bool:
        """检查系统先决条件"""
        print(f"{Colors.YELLOW}🔍 检查系统先决条件...{Colors.END}")
        
        # 检查Python版本
        if sys.version_info < (3, 11):
            self.errors.append("Python 3.11+ 是必需的")
            return False
        
        # 检查Go是否安装
        try:
            result = subprocess.run(['go', 'version'], capture_output=True, text=True)
            if result.returncode != 0:
                self.warnings.append("Go 未安装，Excel服务将不可用")
        except FileNotFoundError:
            self.warnings.append("Go 未安装，Excel服务将不可用")
        
        # 检查pip
        try:
            subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                         capture_output=True, check=True)
        except subprocess.CalledProcessError:
            self.errors.append("pip 不可用")
            return False
        
        print(f"{Colors.GREEN}✅ 系统先决条件检查完成{Colors.END}")
        return True
    
    def create_virtual_environment(self) -> bool:
        """创建虚拟环境"""
        venv_path = self.project_root / 'venv'
        
        if venv_path.exists():
            print(f"{Colors.YELLOW}📦 虚拟环境已存在，跳过创建{Colors.END}")
            return True
        
        print(f"{Colors.YELLOW}📦 创建虚拟环境...{Colors.END}")
        try:
            subprocess.run([sys.executable, '-m', 'venv', str(venv_path)], 
                         check=True)
            print(f"{Colors.GREEN}✅ 虚拟环境创建成功{Colors.END}")
            return True
        except subprocess.CalledProcessError as e:
            self.errors.append(f"虚拟环境创建失败: {e}")
            return False
    
    def install_dependencies(self) -> bool:
        """安装Python依赖"""
        print(f"{Colors.YELLOW}📚 安装Python依赖...{Colors.END}")
        
        requirements_file = self.project_root / 'requirements.txt'
        if not requirements_file.exists():
            self.errors.append("requirements.txt 文件不存在")
            return False
        
        try:
            # 升级pip
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                         check=True)
            
            # 安装依赖
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 
                          str(requirements_file)], check=True)
            
            print(f"{Colors.GREEN}✅ Python依赖安装成功{Colors.END}")
            return True
        except subprocess.CalledProcessError as e:
            self.errors.append(f"依赖安装失败: {e}")
            return False
    
    def build_go_service(self) -> bool:
        """构建Go服务"""
        go_service_dir = self.project_root / 'excel-service'
        
        if not go_service_dir.exists():
            self.warnings.append("Go服务目录不存在，跳过构建")
            return True
        
        print(f"{Colors.YELLOW}🔨 构建Go Excel服务...{Colors.END}")
        
        try:
            # 检查Go是否可用
            subprocess.run(['go', 'version'], capture_output=True, check=True)
            
            # 进入Go服务目录
            os.chdir(go_service_dir)
            
            # 下载依赖
            subprocess.run(['go', 'mod', 'tidy'], check=True)
            
            # 构建服务
            subprocess.run(['go', 'build', '-o', 'excel_service', 'main.go'], 
                         check=True)
            
            # 返回项目根目录
            os.chdir(self.project_root)
            
            print(f"{Colors.GREEN}✅ Go服务构建成功{Colors.END}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            self.warnings.append(f"Go服务构建失败: {e}")
            return True  # 不阻止部署继续
    
    def setup_configuration(self) -> bool:
        """设置配置文件"""
        print(f"{Colors.YELLOW}⚙️ 设置配置文件...{Colors.END}")
        
        config_dir = self.project_root / 'config'
        config_dir.mkdir(exist_ok=True)
        
        # 创建系统配置
        system_config = {
            "service": {
                "name": "chatexcel-mcp",
                "host": "localhost",
                "port": 8080,
                "debug": False,
                "workers": 1,
                "max_connections": 1000,
                "timeout": 30,
                "health_check_enabled": True,
                "auto_restart": True,
                "dependencies": ["go-excel-service"]
            },
            "go_service": {
                "name": "go-excel-service",
                "host": "localhost",
                "port": 8081,
                "timeout": 30,
                "health_check_enabled": True,
                "auto_restart": True
            }
        }
        
        # 创建安全配置
        security_config = {
            "code_execution": {
                "enabled": True,
                "timeout": 30,
                "memory_limit": "256MB",
                "allowed_modules": ["pandas", "numpy", "matplotlib", "seaborn"],
                "blocked_functions": ["exec", "eval", "__import__", "open"]
            },
            "api_security": {
                "rate_limiting": {
                    "enabled": True,
                    "requests_per_minute": 60
                },
                "authentication": {
                    "enabled": False
                }
            },
            "audit": {
                "enabled": True,
                "log_file": "logs/audit.log"
            }
        }
        
        # 创建健康检查配置
        health_config = {
            "health_checks": {
                "interval": 30,
                "timeout": 10,
                "retries": 3
            },
            "monitoring": {
                "cpu_threshold": 80,
                "memory_threshold": 85,
                "disk_threshold": 90
            },
            "recovery": {
                "auto_restart": True,
                "max_restarts": 3,
                "restart_delay": 5
            }
        }
        
        try:
            # 写入配置文件
            with open(config_dir / 'system.json', 'w', encoding='utf-8') as f:
                json.dump(system_config, f, indent=2, ensure_ascii=False)
            
            with open(config_dir / 'security.json', 'w', encoding='utf-8') as f:
                json.dump(security_config, f, indent=2, ensure_ascii=False)
            
            with open(config_dir / 'health.json', 'w', encoding='utf-8') as f:
                json.dump(health_config, f, indent=2, ensure_ascii=False)
            
            print(f"{Colors.GREEN}✅ 配置文件设置完成{Colors.END}")
            return True
        except Exception as e:
            self.errors.append(f"配置文件设置失败: {e}")
            return False
    
    def create_directories(self) -> bool:
        """创建必要的目录"""
        print(f"{Colors.YELLOW}📁 创建项目目录...{Colors.END}")
        
        directories = [
            'logs',
            'temp',
            'static',
            'backups',
            'charts'
        ]
        
        try:
            for directory in directories:
                dir_path = self.project_root / directory
                dir_path.mkdir(exist_ok=True)
            
            print(f"{Colors.GREEN}✅ 项目目录创建完成{Colors.END}")
            return True
        except Exception as e:
            self.errors.append(f"目录创建失败: {e}")
            return False
    
    def run_health_check(self) -> bool:
        """运行健康检查"""
        print(f"{Colors.YELLOW}🏥 运行健康检查...{Colors.END}")
        
        try:
            # 运行基本的导入测试
            test_imports = [
                'pandas',
                'numpy',
                'matplotlib',
                'plotly',
                'fastmcp',
                'mcp'
            ]
            
            for module in test_imports:
                try:
                    __import__(module)
                    print(f"  ✅ {module}")
                except ImportError:
                    print(f"  ❌ {module}")
                    self.warnings.append(f"模块 {module} 导入失败")
            
            print(f"{Colors.GREEN}✅ 健康检查完成{Colors.END}")
            return True
        except Exception as e:
            self.warnings.append(f"健康检查失败: {e}")
            return True  # 不阻止部署
    
    def print_summary(self):
        """打印部署摘要"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}" + "="*60)
        print("    部署摘要")
        print("="*60 + f"{Colors.END}")
        
        if self.errors:
            print(f"{Colors.RED}❌ 错误:{Colors.END}")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print(f"{Colors.YELLOW}⚠️ 警告:{Colors.END}")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if not self.errors:
            print(f"{Colors.GREEN}🎉 部署成功完成!{Colors.END}")
            print(f"\n{Colors.BLUE}下一步:{Colors.END}")
            print("1. 启动增强版服务器: python enhanced_server.py")
            print("2. 或启动原始服务器: python server.py")
            print("3. 查看使用指南: cat ENHANCED_USAGE_GUIDE.md")
            print("4. 运行测试: python -m pytest tests/")
        else:
            print(f"{Colors.RED}❌ 部署失败，请解决上述错误后重试{Colors.END}")
    
    def deploy(self) -> bool:
        """执行完整部署"""
        self.print_header()
        
        steps = [
            ("检查先决条件", self.check_prerequisites),
            ("创建目录", self.create_directories),
            ("安装依赖", self.install_dependencies),
            ("构建Go服务", self.build_go_service),
            ("设置配置", self.setup_configuration),
            ("健康检查", self.run_health_check)
        ]
        
        for step_name, step_func in steps:
            print(f"\n{Colors.BLUE}📋 {step_name}...{Colors.END}")
            if not step_func():
                print(f"{Colors.RED}❌ {step_name} 失败{Colors.END}")
                break
            time.sleep(0.5)  # 短暂延迟以便观察
        
        self.print_summary()
        return len(self.errors) == 0

def main():
    """主函数"""
    try:
        deployer = DeploymentManager()
        success = deployer.deploy()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️ 部署被用户中断{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}❌ 部署过程中发生未预期的错误: {e}{Colors.END}")
        sys.exit(1)

if __name__ == '__main__':
    main()