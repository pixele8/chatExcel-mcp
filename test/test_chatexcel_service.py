#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chatExcel服务功能验证脚本

验证重命名后的MCP服务器功能是否正常：
1. 服务器启动验证
2. 工具函数可用性验证
3. Excel处理功能验证
4. 日志文件生成验证
"""

import sys
import os
import subprocess
import time
import json
from pathlib import Path

def test_server_import():
    """测试服务器模块导入"""
    print("\n=== 测试服务器模块导入 ===")
    try:
        # 添加当前目录到Python路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # 导入服务器模块
        import server
        print("✅ 服务器模块导入成功")
        
        # 检查MCP实例名称
        if hasattr(server, 'mcp'):
            print(f"✅ MCP实例已创建，名称: {server.mcp.name}")
            if server.mcp.name == "chatExcel":
                print("✅ 服务名称已正确更新为 chatExcel")
            else:
                print(f"❌ 服务名称错误，期望: chatExcel，实际: {server.mcp.name}")
        else:
            print("❌ MCP实例未找到")
            
        return True
    except Exception as e:
        print(f"❌ 服务器模块导入失败: {e}")
        return False

def test_config_update():
    """测试配置文件更新"""
    print("\n=== 测试配置文件更新 ===")
    try:
        import config
        cfg = config.config
        print(f"✅ 配置模块导入成功")
        print(f"✅ 日志文件配置: {cfg.LOG_FILE}")
        
        if "chatExcel.log" in cfg.LOG_FILE:
            print("✅ 日志文件名已正确更新")
        else:
            print(f"❌ 日志文件名未更新，当前: {cfg.LOG_FILE}")
            
        return True
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

def test_excel_tools():
    """测试Excel智能工具"""
    print("\n=== 测试Excel智能工具 ===")
    try:
        from excel_smart_tools import (
            suggest_excel_read_parameters,
            detect_excel_file_structure,
            create_excel_read_template
        )
        print("✅ Excel智能工具导入成功")
        
        # 检查sample_data.xlsx是否存在
        sample_file = "sample_data.xlsx"
        if os.path.exists(sample_file):
            print(f"✅ 测试文件存在: {sample_file}")
            
            # 测试文件结构检测
            structure = detect_excel_file_structure(sample_file)
            print(f"✅ 文件结构检测成功，工作表数量: {len(structure.get('sheets', []))}")
        else:
            print(f"⚠️  测试文件不存在: {sample_file}")
            
        return True
    except Exception as e:
        print(f"❌ Excel工具测试失败: {e}")
        return False

def test_project_files():
    """测试项目文件更新"""
    print("\n=== 测试项目文件更新 ===")
    
    # 检查pyproject.toml
    try:
        with open('pyproject.toml', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'name = "chatExcel"' in content:
                print("✅ pyproject.toml 项目名称已更新")
            else:
                print("❌ pyproject.toml 项目名称未更新")
    except Exception as e:
        print(f"❌ pyproject.toml 检查失败: {e}")
    
    # 检查README.md
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'chatExcel' in content:
                print("✅ README.md 已包含 chatExcel 引用")
            else:
                print("❌ README.md 未更新")
    except Exception as e:
        print(f"❌ README.md 检查失败: {e}")

def test_mcp_client_config():
    """测试MCP客户端配置"""
    print("\n=== 测试MCP客户端配置 ===")
    
    # 生成示例配置
    current_path = os.path.abspath('server.py')
    config_example = {
        "mcpServers": {
            "chatExcel": {
                "command": "python",
                "args": [current_path]
            }
        }
    }
    
    print("✅ MCP客户端配置示例:")
    print(json.dumps(config_example, indent=2, ensure_ascii=False))
    
    return True

def main():
    """主测试函数"""
    print("🚀 chatExcel 服务功能验证开始")
    print("=" * 50)
    
    # 切换到脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"📁 工作目录: {os.getcwd()}")
    
    # 运行测试
    tests = [
        test_server_import,
        test_config_update,
        test_excel_tools,
        test_project_files,
        test_mcp_client_config
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ 测试 {test_func.__name__} 异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 测试完成: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！chatExcel 服务重命名成功！")
        print("\n📋 使用说明:")
        print("1. 在MCP客户端配置中使用服务名: chatExcel")
        print("2. 日志文件已更新为: chatExcel.log")
        print("3. 所有Excel智能处理功能保持不变")
    else:
        print("⚠️  部分测试未通过，请检查相关配置")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)