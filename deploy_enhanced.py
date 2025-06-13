#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版 ChatExcel MCP 服务器部署脚本
自动化安装、配置和部署流程
"""

import os
import sys
import subprocess
import json
import shutil
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
import argparse
import tempfile
import platform

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('deploy.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class DeploymentManager:
    """部署管理器"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.python_executable = sys.executable
        self.platform = platform.system().lower()
        self.requirements_installed = False
        self.go_service_built = False
        
        # 部署配置
        self.config = {
            'python_version': '3.8+',
            'go_version': '1.19+',
            'required_packages': [
                'fastmcp>=0.1.0',
                'mcp>=1.0.0',
                'pandas>=1.5.0',
                'numpy>=1.21.0',
                'openpyxl>=3.0.0',
                'pyyaml>=6.0',
                'cryptography>=3.4.0',
                'psutil>=5.8.0',
                'aiofiles>=0.8.0',
                'aiohttp>=3.8.0',
                'click>=8.0.0'
            ],
            'directories': [
                'logs',
                'temp',
                'uploads',
                'backups',
                'config',
                'security',
                'service_management',
                'tests'
            ],
            'config_files': [
                'config/system.json',
                'config/security.json',
                'config/runtime.yaml'
            ]
        }
    
    def check_prerequisites(self) -> Dict[str, bool]:
        """检查部署前提条件"""
        logger.info("检查部署前提条件...")
        
        results = {
            'python_version': False,
            'go_installed': False,
            'git_available': False,
            'write_permissions': False,
            'disk_space': False
        }
        
        try:
            # 检查 Python 版本
            python_version = sys.version_info
            if python_version >= (3, 8):
                results['python_version'] = True
                logger.info(f"Python 版本检查通过: {python_version.major}.{python_version.minor}.{python_version.micro}")
            else:
                logger.error(f"Python 版本过低: {python_version.major}.{python_version.minor}.{python_version.micro}，需要 3.8+")
            
            # 检查 Go 是否安装
            try:
                result = subprocess.run(['go', 'version'], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    results['go_installed'] = True
                    logger.info(f"Go 版本检查通过: {result.stdout.strip()}")
                else:
                    logger.warning("Go 未安装或不在 PATH 中")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                logger.warning("Go 未安装或不在 PATH 中")
            
            # 检查 Git 是否可用
            try:
                result = subprocess.run(['git', '--version'], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    results['git_available'] = True
                    logger.info(f"Git 检查通过: {result.stdout.strip()}")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                logger.warning("Git 未安装或不在 PATH 中")
            
            # 检查写入权限
            try:
                test_file = self.project_root / 'test_write_permission.tmp'
                test_file.write_text('test')
                test_file.unlink()
                results['write_permissions'] = True
                logger.info("写入权限检查通过")
            except Exception as e:
                logger.error(f"写入权限检查失败: {e}")
            
            # 检查磁盘空间（至少需要 1GB）
            try:
                disk_usage = shutil.disk_usage(self.project_root)
                free_space_gb = disk_usage.free / (1024**3)
                if free_space_gb >= 1.0:
                    results['disk_space'] = True
                    logger.info(f"磁盘空间检查通过: {free_space_gb:.2f} GB 可用")
                else:
                    logger.error(f"磁盘空间不足: {free_space_gb:.2f} GB 可用，需要至少 1 GB")
            except Exception as e:
                logger.error(f"磁盘空间检查失败: {e}")
            
        except Exception as e:
            logger.error(f"前提条件检查异常: {e}")
        
        return results
    
    def create_directories(self) -> bool:
        """创建必要的目录"""
        logger.info("创建项目目录结构...")
        
        try:
            for directory in self.config['directories']:
                dir_path = self.project_root / directory
                dir_path.mkdir(parents=True, exist_ok=True)
                logger.debug(f"创建目录: {dir_path}")
            
            # 创建特殊目录的子目录
            special_dirs = {
                'logs': ['audit', 'error', 'access'],
                'temp': ['uploads', 'processing', 'cache'],
                'backups': ['config', 'data', 'logs'],
                'tests': ['unit', 'integration', 'performance']
            }
            
            for parent, subdirs in special_dirs.items():
                for subdir in subdirs:
                    dir_path = self.project_root / parent / subdir
                    dir_path.mkdir(parents=True, exist_ok=True)
                    logger.debug(f"创建子目录: {dir_path}")
            
            logger.info("目录结构创建完成")
            return True
            
        except Exception as e:
            logger.error(f"创建目录失败: {e}")
            return False
    
    def install_python_dependencies(self, upgrade: bool = False) -> bool:
        """安装 Python 依赖"""
        logger.info("安装 Python 依赖包...")
        
        try:
            # 检查是否在虚拟环境中
            in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
            if not in_venv:
                logger.warning("建议在虚拟环境中运行部署")
            
            # 升级 pip
            logger.info("升级 pip...")
            subprocess.run([
                self.python_executable, '-m', 'pip', 'install', '--upgrade', 'pip'
            ], check=True, capture_output=True)
            
            # 安装依赖
            install_cmd = [self.python_executable, '-m', 'pip', 'install']
            if upgrade:
                install_cmd.append('--upgrade')
            
            # 从 requirements.txt 安装
            requirements_file = self.project_root / 'requirements.txt'
            if requirements_file.exists():
                logger.info(f"从 {requirements_file} 安装依赖...")
                subprocess.run(install_cmd + ['-r', str(requirements_file)], check=True)
            else:
                # 安装基本依赖
                logger.info("安装基本依赖包...")
                for package in self.config['required_packages']:
                    logger.info(f"安装: {package}")
                    subprocess.run(install_cmd + [package], check=True)
            
            # 验证安装
            logger.info("验证依赖安装...")
            critical_packages = ['fastmcp', 'pandas', 'numpy', 'openpyxl']
            for package in critical_packages:
                try:
                    __import__(package)
                    logger.debug(f"验证通过: {package}")
                except ImportError:
                    logger.error(f"关键包 {package} 导入失败")
                    return False
            
            self.requirements_installed = True
            logger.info("Python 依赖安装完成")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"安装依赖失败: {e}")
            return False
        except Exception as e:
            logger.error(f"安装依赖异常: {e}")
            return False
    
    def build_go_service(self) -> bool:
        """构建 Go 服务"""
        logger.info("构建 Go Excel 服务...")
        
        try:
            go_main_file = self.project_root / 'main.go'
            if not go_main_file.exists():
                logger.warning("main.go 文件不存在，跳过 Go 服务构建")
                return True
            
            # 检查 Go 是否可用
            try:
                subprocess.run(['go', 'version'], check=True, capture_output=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                logger.error("Go 未安装或不可用，无法构建 Go 服务")
                return False
            
            # 初始化 Go 模块（如果需要）
            go_mod_file = self.project_root / 'go.mod'
            if not go_mod_file.exists():
                logger.info("初始化 Go 模块...")
                subprocess.run([
                    'go', 'mod', 'init', 'chatexcel-go-service'
                ], cwd=self.project_root, check=True)
                
                subprocess.run([
                    'go', 'mod', 'tidy'
                ], cwd=self.project_root, check=True)
            
            # 构建可执行文件
            executable_name = 'excel_service'
            if self.platform == 'windows':
                executable_name += '.exe'
            
            logger.info(f"构建可执行文件: {executable_name}")
            subprocess.run([
                'go', 'build', '-o', executable_name, 'main.go'
            ], cwd=self.project_root, check=True)
            
            # 验证构建结果
            executable_path = self.project_root / executable_name
            if executable_path.exists():
                logger.info(f"Go 服务构建成功: {executable_path}")
                # 设置执行权限（Unix 系统）
                if self.platform != 'windows':
                    os.chmod(executable_path, 0o755)
                
                self.go_service_built = True
                return True
            else:
                logger.error("Go 服务构建失败：可执行文件不存在")
                return False
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Go 服务构建失败: {e}")
            return False
        except Exception as e:
            logger.error(f"Go 服务构建异常: {e}")
            return False
    
    def setup_configuration(self) -> bool:
        """设置配置文件"""
        logger.info("设置配置文件...")
        
        try:
            # 检查配置文件是否存在
            missing_configs = []
            for config_file in self.config['config_files']:
                config_path = self.project_root / config_file
                if not config_path.exists():
                    missing_configs.append(config_file)
            
            if missing_configs:
                logger.warning(f"缺少配置文件: {missing_configs}")
                logger.info("将使用默认配置")
            
            # 创建环境特定的配置
            env_config = {
                'deployment': {
                    'timestamp': time.time(),
                    'platform': self.platform,
                    'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                    'project_root': str(self.project_root),
                    'requirements_installed': self.requirements_installed,
                    'go_service_built': self.go_service_built
                }
            }
            
            env_config_file = self.project_root / 'config' / 'deployment.json'
            with open(env_config_file, 'w', encoding='utf-8') as f:
                json.dump(env_config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"部署配置已保存: {env_config_file}")
            
            # 设置日志配置
            self._setup_logging_config()
            
            logger.info("配置设置完成")
            return True
            
        except Exception as e:
            logger.error(f"配置设置失败: {e}")
            return False
    
    def _setup_logging_config(self):
        """设置日志配置"""
        log_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                },
                'detailed': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO',
                    'formatter': 'standard',
                    'stream': 'ext://sys.stdout'
                },
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'DEBUG',
                    'formatter': 'detailed',
                    'filename': 'logs/app.log',
                    'maxBytes': 10485760,
                    'backupCount': 5,
                    'encoding': 'utf-8'
                },
                'error_file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'ERROR',
                    'formatter': 'detailed',
                    'filename': 'logs/error/error.log',
                    'maxBytes': 10485760,
                    'backupCount': 5,
                    'encoding': 'utf-8'
                }
            },
            'loggers': {
                '': {
                    'handlers': ['console', 'file'],
                    'level': 'DEBUG',
                    'propagate': False
                },
                'audit': {
                    'handlers': ['file'],
                    'level': 'INFO',
                    'propagate': False,
                    'filename': 'logs/audit/audit.log'
                }
            }
        }
        
        log_config_file = self.project_root / 'config' / 'logging.json'
        with open(log_config_file, 'w', encoding='utf-8') as f:
            json.dump(log_config, f, indent=2, ensure_ascii=False)
    
    def run_tests(self) -> bool:
        """运行测试"""
        logger.info("运行部署测试...")
        
        try:
            # 基本导入测试
            test_imports = [
                'fastmcp',
                'pandas',
                'numpy',
                'openpyxl',
                'yaml',
                'cryptography'
            ]
            
            for module in test_imports:
                try:
                    __import__(module)
                    logger.debug(f"导入测试通过: {module}")
                except ImportError as e:
                    logger.error(f"导入测试失败: {module} - {e}")
                    return False
            
            # 配置管理器测试
            try:
                sys.path.insert(0, str(self.project_root))
                from service_management.config_manager import ConfigManager
                
                # 创建临时配置目录进行测试
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_config_dir = Path(temp_dir) / 'config'
                    temp_config_dir.mkdir()
                    
                    # 创建测试配置
                    test_config = {'test': {'value': 'success'}}
                    with open(temp_config_dir / 'test.json', 'w') as f:
                        json.dump(test_config, f)
                    
                    # 测试配置管理器
                    config_manager = ConfigManager(temp_config_dir)
                    test_value = config_manager.get('test.value')
                    
                    if test_value == 'success':
                        logger.debug("配置管理器测试通过")
                    else:
                        logger.error("配置管理器测试失败")
                        return False
                    
                    config_manager.shutdown()
                    
            except Exception as e:
                logger.error(f"配置管理器测试失败: {e}")
                return False
            
            # Go 服务测试（如果已构建）
            if self.go_service_built:
                executable_name = 'excel_service'
                if self.platform == 'windows':
                    executable_name += '.exe'
                
                executable_path = self.project_root / executable_name
                if executable_path.exists():
                    logger.debug("Go 服务可执行文件存在")
                else:
                    logger.warning("Go 服务可执行文件不存在")
            
            logger.info("部署测试完成")
            return True
            
        except Exception as e:
            logger.error(f"部署测试异常: {e}")
            return False
    
    def create_startup_scripts(self) -> bool:
        """创建启动脚本"""
        logger.info("创建启动脚本...")
        
        try:
            # Python 启动脚本
            if self.platform == 'windows':
                startup_script = self.project_root / 'start_server.bat'
                script_content = f'''@echo off
echo Starting Enhanced ChatExcel MCP Server...
"{self.python_executable}" enhanced_server.py
pause
'''
            else:
                startup_script = self.project_root / 'start_server.sh'
                script_content = f'''#!/bin/bash
echo "Starting Enhanced ChatExcel MCP Server..."
"{self.python_executable}" enhanced_server.py
'''
            
            with open(startup_script, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            # 设置执行权限（Unix 系统）
            if self.platform != 'windows':
                os.chmod(startup_script, 0o755)
            
            logger.info(f"启动脚本已创建: {startup_script}")
            
            # 创建停止脚本
            if self.platform == 'windows':
                stop_script = self.project_root / 'stop_server.bat'
                script_content = '''@echo off
echo Stopping ChatExcel MCP Server...
taskkill /f /im python.exe /fi "WINDOWTITLE eq Enhanced ChatExcel MCP Server"
echo Server stopped.
pause
'''
            else:
                stop_script = self.project_root / 'stop_server.sh'
                script_content = '''#!/bin/bash
echo "Stopping ChatExcel MCP Server..."
pkill -f "enhanced_server.py"
echo "Server stopped."
'''
            
            with open(stop_script, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            if self.platform != 'windows':
                os.chmod(stop_script, 0o755)
            
            logger.info(f"停止脚本已创建: {stop_script}")
            
            return True
            
        except Exception as e:
            logger.error(f"创建启动脚本失败: {e}")
            return False
    
    def generate_deployment_report(self) -> Dict[str, any]:
        """生成部署报告"""
        logger.info("生成部署报告...")
        
        report = {
            'deployment_time': time.time(),
            'platform': self.platform,
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'project_root': str(self.project_root),
            'components': {
                'python_dependencies': self.requirements_installed,
                'go_service': self.go_service_built,
                'configuration': True,
                'startup_scripts': True
            },
            'files_created': [],
            'directories_created': self.config['directories'],
            'next_steps': [
                "运行 'python enhanced_server.py' 启动服务器",
                "或使用启动脚本 'start_server.sh' (Unix) 或 'start_server.bat' (Windows)",
                "检查 logs/app.log 查看运行日志",
                "访问健康检查端点验证服务状态"
            ]
        }
        
        # 检查创建的文件
        important_files = [
            'enhanced_server.py',
            'config/system.json',
            'config/security.json',
            'config/runtime.yaml',
            'service_management/config_manager.py',
            'service_management/health_manager.py',
            'service_management/dependency_manager.py',
            'security/secure_code_executor.py'
        ]
        
        for file_path in important_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                report['files_created'].append(file_path)
        
        # 保存报告
        report_file = self.project_root / 'deployment_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"部署报告已保存: {report_file}")
        return report
    
    def deploy(self, skip_tests: bool = False, upgrade_deps: bool = False) -> bool:
        """执行完整部署"""
        logger.info("开始部署增强版 ChatExcel MCP 服务器")
        
        try:
            # 1. 检查前提条件
            prerequisites = self.check_prerequisites()
            if not all(prerequisites.values()):
                failed_checks = [k for k, v in prerequisites.items() if not v]
                logger.error(f"前提条件检查失败: {failed_checks}")
                return False
            
            # 2. 创建目录结构
            if not self.create_directories():
                logger.error("创建目录结构失败")
                return False
            
            # 3. 安装 Python 依赖
            if not self.install_python_dependencies(upgrade=upgrade_deps):
                logger.error("安装 Python 依赖失败")
                return False
            
            # 4. 构建 Go 服务
            if not self.build_go_service():
                logger.warning("Go 服务构建失败，但继续部署")
            
            # 5. 设置配置
            if not self.setup_configuration():
                logger.error("配置设置失败")
                return False
            
            # 6. 运行测试
            if not skip_tests:
                if not self.run_tests():
                    logger.error("部署测试失败")
                    return False
            
            # 7. 创建启动脚本
            if not self.create_startup_scripts():
                logger.warning("创建启动脚本失败，但继续部署")
            
            # 8. 生成部署报告
            report = self.generate_deployment_report()
            
            logger.info("部署完成！")
            logger.info("下一步:")
            for step in report['next_steps']:
                logger.info(f"  - {step}")
            
            return True
            
        except Exception as e:
            logger.error(f"部署失败: {e}")
            return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='部署增强版 ChatExcel MCP 服务器')
    parser.add_argument('--project-root', type=Path, default=Path.cwd(),
                       help='项目根目录路径')
    parser.add_argument('--skip-tests', action='store_true',
                       help='跳过部署测试')
    parser.add_argument('--upgrade-deps', action='store_true',
                       help='升级现有依赖包')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='详细输出')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 确保项目根目录存在
    if not args.project_root.exists():
        logger.error(f"项目根目录不存在: {args.project_root}")
        sys.exit(1)
    
    # 创建部署管理器
    deployer = DeploymentManager(args.project_root)
    
    # 执行部署
    success = deployer.deploy(
        skip_tests=args.skip_tests,
        upgrade_deps=args.upgrade_deps
    )
    
    if success:
        logger.info("部署成功完成！")
        sys.exit(0)
    else:
        logger.error("部署失败！")
        sys.exit(1)

if __name__ == '__main__':
    main()