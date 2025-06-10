#!/usr/bin/env python3
"""
ChatExcel MCP配置生成器
自动检测环境并生成适合的MCP服务器配置
"""

import os
import json
import sys
from pathlib import Path

def detect_project_root():
    """检测项目根目录"""
    current_dir = Path(__file__).parent.absolute()
    
    # 检查当前目录是否包含server.py
    if (current_dir / "server.py").exists():
        return current_dir
    
    # 向上查找包含server.py的目录
    for parent in current_dir.parents:
        if (parent / "server.py").exists():
            return parent
    
    return current_dir

def detect_python_executable(project_root):
    """检测合适的Python可执行文件"""
    venv_dir = project_root / "venv"
    
    # 优先使用虚拟环境中的Python
    if venv_dir.exists():
        venv_python = venv_dir / "bin" / "python"
        if venv_python.exists():
            return str(venv_python)
        
        # 尝试python3
        venv_python3 = venv_dir / "bin" / "python3"
        if venv_python3.exists():
            return str(venv_python3)
    
    # 回退到系统Python
    for python_cmd in ["python3.11", "python3", "python"]:
        if os.system(f"which {python_cmd} > /dev/null 2>&1") == 0:
            return python_cmd
    
    return "python3"

def generate_mcp_config(project_root, config_type="flexible"):
    """生成MCP配置
    
    Args:
        project_root: 项目根目录
        config_type: 配置类型 ('flexible', 'absolute', 'relative')
    """
    project_root = Path(project_root)
    python_executable = detect_python_executable(project_root)
    
    if config_type == "flexible":
        # 灵活配置：使用工作目录和环境变量
        config = {
            "mcpServers": {
                "chatExcel": {
                    "command": "python3",
                    "args": ["server.py"],
                    "cwd": str(project_root),
                    "env": {
                        "PATH": f"{project_root}/venv/bin:/usr/local/bin:/usr/bin:/bin",
                        "VIRTUAL_ENV": str(project_root / "venv"),
                        "PYTHONPATH": str(project_root)
                    }
                }
            }
        }
    
    elif config_type == "absolute":
        # 绝对路径配置
        config = {
            "mcpServers": {
                "chatExcel": {
                    "command": python_executable,
                    "args": [str(project_root / "server.py")]
                }
            }
        }
    
    elif config_type == "relative":
        # 相对路径配置（需要在项目目录中运行）
        config = {
            "mcpServers": {
                "chatExcel": {
                    "command": "./venv/bin/python",
                    "args": ["./server.py"],
                    "cwd": str(project_root)
                }
            }
        }
    
    else:
        raise ValueError(f"不支持的配置类型: {config_type}")
    
    return config

def save_config(config, output_file):
    """保存配置到文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"配置已保存到: {output_file}")

def main():
    """主函数"""
    project_root = detect_project_root()
    print(f"检测到项目根目录: {project_root}")
    
    # 检查必要文件
    server_file = project_root / "server.py"
    if not server_file.exists():
        print(f"错误: 未找到server.py文件在 {server_file}")
        sys.exit(1)
    
    venv_dir = project_root / "venv"
    if not venv_dir.exists():
        print(f"警告: 未找到虚拟环境目录 {venv_dir}")
        print("建议先创建虚拟环境: python3.11 -m venv venv")
    
    # 生成不同类型的配置
    configs = {
        "flexible": "mcp_config_flexible.json",
        "absolute": "mcp_config_absolute.json",
        "relative": "mcp_config_relative.json"
    }
    
    for config_type, filename in configs.items():
        try:
            config = generate_mcp_config(project_root, config_type)
            output_file = project_root / filename
            save_config(config, output_file)
            print(f"✓ 生成 {config_type} 配置: {filename}")
        except Exception as e:
            print(f"✗ 生成 {config_type} 配置失败: {e}")
    
    print("\n推荐使用顺序:")
    print("1. mcp_config_flexible.json (最灵活，推荐)")
    print("2. mcp_config_absolute.json (绝对路径，兼容性好)")
    print("3. mcp_config_relative.json (相对路径，需要在项目目录运行)")
    
    print("\n使用方法:")
    print("将生成的配置内容复制到你的MCP客户端配置文件中")

if __name__ == "__main__":
    main()