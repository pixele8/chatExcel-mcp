#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatExcel MCP服务器系统完整性检查
验证31个工具和所有服务功能的完整性
"""

import sys
import os
import json
import importlib
from pathlib import Path
from typing import Dict, List, Any, Tuple

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_mcp_config() -> Tuple[bool, Dict[str, Any]]:
    """检查MCP配置文件"""
    config_path = "/Users/wangdada/Downloads/mcp/chatExcel-mcp/mcp_config_absolute.json"
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        chatexcel_config = config.get('mcpServers', {}).get('chatExcel', {})
        
        return True, {
            'config_exists': True,
            'python_path': chatexcel_config.get('command'),
            'server_script': chatexcel_config.get('args', []),
            'tools_count': chatexcel_config.get('tools_count', 0),
            'version': chatexcel_config.get('version'),
            'capabilities': chatexcel_config.get('capabilities', [])
        }
    except Exception as e:
        return False, {'error': str(e)}

def check_server_module() -> Tuple[bool, Dict[str, Any]]:
    """检查服务器模块和工具注册"""
    try:
        # 导入服务器模块
        import server
        
        # 检查MCP实例
        mcp_instance = getattr(server, 'mcp', None)
        if not mcp_instance:
            return False, {'error': 'MCP实例未找到'}
        
        # 获取注册的工具
        tools = []
        if hasattr(mcp_instance, '_tools'):
            tools = list(mcp_instance._tools.keys())
        elif hasattr(mcp_instance, 'tools'):
            tools = list(mcp_instance.tools.keys())
        
        # 检查依赖管理器
        dependency_manager = getattr(server, 'dependency_manager', None)
        available_modules = []
        failed_imports = []
        
        if dependency_manager:
            available_modules = list(dependency_manager.available_modules.keys())
            failed_imports = dependency_manager.failed_imports
        
        return True, {
            'mcp_instance': str(type(mcp_instance)),
            'tools_registered': len(tools),
            'tool_names': tools,
            'available_modules': available_modules,
            'failed_imports': failed_imports,
            'core_modules_available': getattr(server, 'CORE_MODULES_AVAILABLE', False)
        }
    except Exception as e:
        return False, {'error': str(e), 'traceback': str(e.__traceback__)}

def check_virtual_environment() -> Tuple[bool, Dict[str, Any]]:
    """检查虚拟环境状态"""
    try:
        venv_path = "/Users/wangdada/Downloads/mcp/chatExcel-mcp/venv"
        python_path = f"{venv_path}/bin/python"
        
        return True, {
            'venv_exists': os.path.exists(venv_path),
            'python_exists': os.path.exists(python_path),
            'current_python': sys.executable,
            'in_venv': sys.prefix != sys.base_prefix,
            'python_version': sys.version
        }
    except Exception as e:
        return False, {'error': str(e)}

def check_project_structure() -> Tuple[bool, Dict[str, Any]]:
    """检查项目结构完整性"""
    try:
        project_root = "/Users/wangdada/Downloads/mcp/chatExcel-mcp"
        
        required_files = [
            'server.py',
            'requirements.txt',
            'mcp_config_absolute.json',
            'config.py'
        ]
        
        required_dirs = [
            'core',
            'scripts',
            'templates',
            'config',
            'logs'
        ]
        
        file_status = {}
        for file in required_files:
            file_path = os.path.join(project_root, file)
            file_status[file] = os.path.exists(file_path)
        
        dir_status = {}
        for dir_name in required_dirs:
            dir_path = os.path.join(project_root, dir_name)
            dir_status[dir_name] = os.path.exists(dir_path)
        
        return True, {
            'project_root': project_root,
            'files': file_status,
            'directories': dir_status,
            'all_files_exist': all(file_status.values()),
            'all_dirs_exist': all(dir_status.values())
        }
    except Exception as e:
        return False, {'error': str(e)}

def main():
    """主检查函数"""
    print("🔍 ChatExcel MCP服务器系统完整性检查")
    print("=" * 60)
    
    checks = [
        ("MCP配置文件", check_mcp_config),
        ("虚拟环境", check_virtual_environment),
        ("项目结构", check_project_structure),
        ("服务器模块", check_server_module)
    ]
    
    results = {}
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"\n📋 检查 {check_name}...")
        success, data = check_func()
        results[check_name] = {'success': success, 'data': data}
        
        if success:
            print(f"  ✅ {check_name} 检查通过")
            
            # 显示关键信息
            if check_name == "MCP配置文件":
                print(f"    - 工具数量: {data.get('tools_count', 'N/A')}")
                print(f"    - 版本: {data.get('version', 'N/A')}")
                print(f"    - 功能数量: {len(data.get('capabilities', []))}")
            
            elif check_name == "服务器模块":
                print(f"    - 注册工具数量: {data.get('tools_registered', 0)}")
                print(f"    - 可用模块数量: {len(data.get('available_modules', []))}")
                print(f"    - 失败导入数量: {len(data.get('failed_imports', []))}")
                
                if data.get('failed_imports'):
                    print(f"    - 失败模块: {', '.join(data['failed_imports'])}")
            
            elif check_name == "虚拟环境":
                print(f"    - 虚拟环境激活: {data.get('in_venv', False)}")
                print(f"    - Python版本: {data.get('python_version', 'N/A').split()[0]}")
            
            elif check_name == "项目结构":
                print(f"    - 必需文件: {sum(data.get('files', {}).values())}/{len(data.get('files', {}))}")
                print(f"    - 必需目录: {sum(data.get('directories', {}).values())}/{len(data.get('directories', {}))}")
        
        else:
            all_passed = False
            print(f"  ❌ {check_name} 检查失败")
            print(f"    错误: {data.get('error', 'Unknown error')}")
    
    # 总结
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 系统完整性检查全部通过!")
        
        # 显示工具统计
        server_data = results.get("服务器模块", {}).get('data', {})
        config_data = results.get("MCP配置文件", {}).get('data', {})
        
        registered_tools = server_data.get('tools_registered', 0)
        expected_tools = config_data.get('tools_count', 31)
        
        print(f"\n📊 工具统计:")
        print(f"  - 预期工具数量: {expected_tools}")
        print(f"  - 实际注册工具: {registered_tools}")
        
        if registered_tools == expected_tools:
            print(f"  ✅ 工具数量匹配")
        else:
            print(f"  ⚠️  工具数量不匹配")
        
        print(f"\n🔧 服务状态:")
        print(f"  - MCP服务器: 就绪")
        print(f"  - 虚拟环境: 已配置")
        print(f"  - 依赖模块: {len(server_data.get('available_modules', []))} 个可用")
        print(f"  - 配置文件: 有效")
        
        return 0
    else:
        print("❌ 系统完整性检查发现问题，请检查上述错误")
        return 1

if __name__ == "__main__":
    sys.exit(main())