#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP服务器配置验证脚本
测试plotly导入和MCP服务器配置
"""

import json
import sys
import os

def test_plotly_import():
    """测试plotly导入"""
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        print("✅ Plotly导入成功")
        print(f"   - plotly版本: {px.__version__ if hasattr(px, '__version__') else '未知'}")
        return True
    except ImportError as e:
        print(f"❌ Plotly导入失败: {e}")
        return False

def test_server_import():
    """测试服务器模块导入"""
    try:
        # 添加当前目录到路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        from server import mcp
        print("✅ MCP服务器模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ MCP服务器模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ MCP服务器模块导入异常: {e}")
        return False

def generate_mcp_config():
    """生成MCP配置"""
    server_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "server.py"))
    
    config = {
        "mcpServers": {
            "chatExcel": {
                "command": "python3.11",
                "args": [server_path]
            }
        }
    }
    
    print("\n📋 MCP服务器配置:")
    print(json.dumps(config, indent=2, ensure_ascii=False))
    return config

def main():
    """主函数"""
    print("🔍 MCP服务器配置验证")
    print("=" * 50)
    
    # 测试plotly导入
    plotly_ok = test_plotly_import()
    
    # 测试服务器导入
    server_ok = test_server_import()
    
    # 生成配置
    config = generate_mcp_config()
    
    # 总结
    print("\n📊 测试结果:")
    print(f"   - Plotly导入: {'✅ 成功' if plotly_ok else '❌ 失败'}")
    print(f"   - 服务器导入: {'✅ 成功' if server_ok else '❌ 失败'}")
    
    if plotly_ok and server_ok:
        print("\n🎉 所有测试通过！MCP服务器可以正常启动。")
        print("\n💡 使用方法:")
        print("   1. 将上述配置添加到你的MCP客户端配置文件中")
        print("   2. 重启MCP客户端")
        print("   3. 开始使用chatExcel MCP服务")
        return True
    else:
        print("\n❌ 存在问题，请检查依赖安装。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)