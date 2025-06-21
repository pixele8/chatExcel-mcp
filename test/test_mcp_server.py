#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 MCP 服务器功能
"""

import json
import sys
import os
import asyncio

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_mcp_server():
    """测试 MCP 服务器的基本功能"""
    try:
        # 导入服务器模块
        import server
        
        print("✓ 成功导入服务器模块")
        
        # 检查 mcp 对象是否存在
        if hasattr(server, 'mcp'):
            mcp_app = server.mcp
            print("✓ 成功获取 FastMCP 应用对象")
            
            # 测试工具列表（异步调用）
            tools = await mcp_app.list_tools()
            print(f"✓ 服务器提供 {len(tools)} 个工具")
            
            # 打印工具名称
            tool_names = [tool.name for tool in tools]
            print(f"可用工具: {', '.join(tool_names)}")
            
            # 打印前几个工具的详细信息
            for i, tool in enumerate(tools[:3]):
                print(f"  工具 {i+1}: {tool.name} - {tool.description[:100]}..." if len(tool.description) > 100 else f"  工具 {i+1}: {tool.name} - {tool.description}")
            
            return True
        else:
            print("✗ 未找到 mcp 应用对象")
            return False
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("开始测试 MCP 服务器...")
    success = await test_mcp_server()
    if success:
        print("\n✓ MCP 服务器测试通过")
    else:
        print("\n✗ MCP 服务器测试失败")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())