#!/usr/bin/env python3
"""
ChatExcel MCP设置诊断工具
检查和修复常见的MCP配置问题
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple

class MCPDiagnostic:
    """MCP诊断工具类"""
    
    def __init__(self, project_root: str = None):
        """初始化诊断工具
        
        Args:
            project_root: 项目根目录，如果为None则自动检测
        """
        if project_root:
            self.project_root = Path(project_root)
        else:
            self.project_root = self._detect_project_root()
        
        self.issues = []
        self.fixes = []
    
    def _detect_project_root(self) -> Path:
        """自动检测项目根目录"""
        current_dir = Path(__file__).parent.absolute()
        
        # 检查当前目录
        if (current_dir / "server.py").exists():
            return current_dir
        
        # 向上查找
        for parent in current_dir.parents:
            if (parent / "server.py").exists():
                return parent
        
        return current_dir
    
    def check_file_exists(self, file_path: Path, description: str) -> bool:
        """检查文件是否存在"""
        if file_path.exists():
            print(f"✓ {description}: {file_path}")
            return True
        else:
            print(f"✗ {description}不存在: {file_path}")
            self.issues.append(f"{description}不存在")
            return False
    
    def check_directory_exists(self, dir_path: Path, description: str) -> bool:
        """检查目录是否存在"""
        if dir_path.exists() and dir_path.is_dir():
            print(f"✓ {description}: {dir_path}")
            return True
        else:
            print(f"✗ {description}不存在: {dir_path}")
            self.issues.append(f"{description}不存在")
            return False
    
    def check_python_executable(self, python_path: Path) -> bool:
        """检查Python可执行文件"""
        if python_path.exists() and os.access(python_path, os.X_OK):
            try:
                result = subprocess.run([str(python_path), "--version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✓ Python可执行文件: {python_path} ({result.stdout.strip()})")
                    return True
            except Exception as e:
                print(f"✗ Python可执行文件测试失败: {e}")
        
        print(f"✗ Python可执行文件无效: {python_path}")
        self.issues.append("Python可执行文件无效")
        return False
    
    def check_mcp_package(self, python_path: Path) -> bool:
        """检查MCP包是否安装"""
        try:
            result = subprocess.run([str(python_path), "-c", "import mcp; print(mcp.__version__)"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✓ MCP包已安装: 版本 {version}")
                return True
            else:
                print(f"✗ MCP包未安装或导入失败: {result.stderr}")
                self.issues.append("MCP包未安装")
                self.fixes.append(f"安装MCP包: {python_path} -m pip install mcp")
                return False
        except Exception as e:
            print(f"✗ 检查MCP包时出错: {e}")
            self.issues.append("无法检查MCP包")
            return False
    
    def check_server_syntax(self, server_path: Path, python_path: Path) -> bool:
        """检查服务器文件语法"""
        try:
            result = subprocess.run([str(python_path), "-m", "py_compile", str(server_path)], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✓ 服务器文件语法正确: {server_path}")
                return True
            else:
                print(f"✗ 服务器文件语法错误: {result.stderr}")
                self.issues.append("服务器文件语法错误")
                return False
        except Exception as e:
            print(f"✗ 检查服务器文件语法时出错: {e}")
            return False
    
    def validate_config(self, config_path: Path) -> bool:
        """验证MCP配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 检查基本结构
            if "mcpServers" not in config:
                print(f"✗ 配置文件缺少mcpServers字段: {config_path}")
                return False
            
            if "chatExcel" not in config["mcpServers"]:
                print(f"✗ 配置文件缺少chatExcel服务器配置: {config_path}")
                return False
            
            server_config = config["mcpServers"]["chatExcel"]
            
            # 检查必要字段
            if "command" not in server_config:
                print(f"✗ 配置文件缺少command字段: {config_path}")
                return False
            
            if "args" not in server_config:
                print(f"✗ 配置文件缺少args字段: {config_path}")
                return False
            
            print(f"✓ 配置文件格式正确: {config_path}")
            return True
            
        except json.JSONDecodeError as e:
            print(f"✗ 配置文件JSON格式错误: {e}")
            self.issues.append("配置文件JSON格式错误")
            return False
        except Exception as e:
            print(f"✗ 验证配置文件时出错: {e}")
            return False
    
    def run_full_diagnostic(self) -> Dict[str, bool]:
        """运行完整诊断"""
        print(f"开始诊断ChatExcel MCP设置...")
        print(f"项目根目录: {self.project_root}")
        print("=" * 60)
        
        results = {}
        
        # 1. 检查项目文件
        print("\n1. 检查项目文件:")
        server_file = self.project_root / "server.py"
        results['server_file'] = self.check_file_exists(server_file, "服务器文件")
        
        # 2. 检查虚拟环境
        print("\n2. 检查虚拟环境:")
        venv_dir = self.project_root / "venv"
        results['venv_dir'] = self.check_directory_exists(venv_dir, "虚拟环境目录")
        
        if results['venv_dir']:
            python_exe = venv_dir / "bin" / "python"
            results['python_exe'] = self.check_python_executable(python_exe)
            
            if results['python_exe']:
                results['mcp_package'] = self.check_mcp_package(python_exe)
                
                if results['server_file']:
                    results['server_syntax'] = self.check_server_syntax(server_file, python_exe)
        else:
            results['python_exe'] = False
            results['mcp_package'] = False
            results['server_syntax'] = False
            self.fixes.append(f"创建虚拟环境: cd {self.project_root} && python3.11 -m venv venv")
            self.fixes.append(f"激活虚拟环境: source {venv_dir}/bin/activate")
            self.fixes.append(f"安装依赖: pip install -r requirements.txt")
        
        # 3. 检查配置文件
        print("\n3. 检查配置文件:")
        config_files = [
            "mcp_config_flexible.json",
            "mcp_config_absolute.json", 
            "mcp_config_relative.json"
        ]
        
        results['config_files'] = []
        for config_file in config_files:
            config_path = self.project_root / config_file
            if config_path.exists():
                valid = self.validate_config(config_path)
                results['config_files'].append((config_file, valid))
            else:
                print(f"- {config_file}: 不存在")
                results['config_files'].append((config_file, False))
        
        # 4. 生成修复建议
        print("\n4. 诊断结果:")
        if self.issues:
            print("发现的问题:")
            for i, issue in enumerate(self.issues, 1):
                print(f"  {i}. {issue}")
        else:
            print("✓ 未发现明显问题")
        
        if self.fixes:
            print("\n建议的修复步骤:")
            for i, fix in enumerate(self.fixes, 1):
                print(f"  {i}. {fix}")
        
        return results
    
    def generate_working_config(self) -> str:
        """生成一个可工作的配置"""
        venv_python = self.project_root / "venv" / "bin" / "python"
        server_file = self.project_root / "server.py"
        
        if venv_python.exists() and server_file.exists():
            config = {
                "mcpServers": {
                    "chatExcel": {
                        "command": str(venv_python),
                        "args": [str(server_file)]
                    }
                }
            }
            return json.dumps(config, indent=2, ensure_ascii=False)
        else:
            return "无法生成配置：缺少必要文件"

def main():
    """主函数"""
    diagnostic = MCPDiagnostic()
    results = diagnostic.run_full_diagnostic()
    
    print("\n" + "=" * 60)
    print("推荐的MCP配置:")
    print(diagnostic.generate_working_config())
    
    print("\n使用说明:")
    print("1. 将上述配置复制到你的MCP客户端配置文件中")
    print("2. 如果仍有问题，请按照修复建议逐步解决")
    print("3. 可以使用 ./start_mcp_server.sh 测试服务器启动")

if __name__ == "__main__":
    main()