#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastMCP工具注册诊断脚本
深入分析FastMCP的工具注册机制和状态
"""

import sys
import os
import inspect
from typing import Dict, List, Any

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def analyze_fastmcp_instance():
    """分析FastMCP实例的详细状态"""
    print("🔍 FastMCP实例深度诊断")
    print("=" * 50)
    
    try:
        # 导入FastMCP
        from fastmcp import FastMCP
        print(f"✅ FastMCP导入成功")
        
        # 导入服务器模块
        import server
        print(f"✅ 服务器模块导入成功")
        
        # 获取MCP实例
        mcp_instance = getattr(server, 'mcp', None)
        if not mcp_instance:
            print("❌ MCP实例未找到")
            return False
        
        print(f"✅ MCP实例: {type(mcp_instance)}")
        print(f"✅ 实例名称: {getattr(mcp_instance, 'name', 'N/A')}")
        
        # 检查FastMCP版本
        import fastmcp
        print(f"✅ FastMCP版本: {fastmcp.__version__}")
        
        # 深度检查实例属性
        print("\n📋 MCP实例所有属性:")
        all_attrs = [attr for attr in dir(mcp_instance) if not attr.startswith('__')]
        for attr in sorted(all_attrs):
            try:
                value = getattr(mcp_instance, attr)
                attr_type = type(value).__name__
                
                if callable(value):
                    print(f"  🔧 {attr}: {attr_type} (方法)")
                elif hasattr(value, '__len__') and not isinstance(value, str):
                    print(f"  📦 {attr}: {attr_type} (长度: {len(value)})")
                else:
                    print(f"  📄 {attr}: {attr_type} = {repr(value)[:50]}")
            except Exception as e:
                print(f"  ❌ {attr}: 访问失败 - {e}")
        
        # 检查工具相关的属性
        print("\n🔧 工具相关属性详细检查:")
        tool_attrs = ['_tools', 'tools', '_handlers', 'registry', '_registry', 
                     '_tool_registry', '_resource_registry', '_prompt_registry']
        
        for attr in tool_attrs:
            if hasattr(mcp_instance, attr):
                try:
                    value = getattr(mcp_instance, attr)
                    print(f"  ✅ {attr}: {type(value)}")
                    
                    if hasattr(value, 'keys'):
                        keys = list(value.keys())
                        print(f"    - 键数量: {len(keys)}")
                        if keys:
                            print(f"    - 前5个键: {keys[:5]}")
                    
                    elif hasattr(value, '__len__') and not isinstance(value, str):
                        print(f"    - 长度: {len(value)}")
                        if hasattr(value, '__iter__'):
                            items = list(value)[:5]
                            print(f"    - 前5个项: {items}")
                    
                    elif hasattr(value, '__dict__'):
                        attrs = [a for a in dir(value) if not a.startswith('_')]
                        print(f"    - 子属性: {attrs[:5]}")
                        
                except Exception as e:
                    print(f"  ❌ {attr}: 检查失败 - {e}")
            else:
                print(f"  ❌ {attr}: 不存在")
        
        # 检查工具装饰器函数
        print("\n🎯 检查@mcp.tool装饰的函数:")
        
        # 获取服务器模块中的所有函数
        server_functions = []
        for name, obj in inspect.getmembers(server, inspect.isfunction):
            server_functions.append((name, obj))
        
        print(f"  📊 服务器模块函数总数: {len(server_functions)}")
        
        # 查找可能的工具函数
        potential_tools = []
        for name, func in server_functions:
            # 检查函数的各种可能的工具标记
            markers = [
                hasattr(func, '__mcp_tool__'),
                hasattr(func, '_mcp_tool'),
                hasattr(func, '__wrapped__'),
                'mcp.tool' in str(func),
                getattr(func, '__name__', '').endswith('_tool')
            ]
            
            if any(markers):
                potential_tools.append(name)
        
        print(f"  🎯 潜在工具函数: {len(potential_tools)}")
        for tool in potential_tools:
            print(f"    - {tool}")
        
        # 尝试手动调用工具注册方法
        print("\n🔨 尝试手动工具注册测试:")
        
        if hasattr(mcp_instance, 'tool'):
            tool_decorator = getattr(mcp_instance, 'tool')
            print(f"  ✅ tool装饰器可用: {type(tool_decorator)}")
            
            # 创建一个测试函数
            @tool_decorator()
            def test_tool_function():
                """测试工具函数"""
                return "测试成功"
            
            print(f"  ✅ 测试函数创建成功")
            
            # 再次检查工具注册状态
            print("\n🔍 重新检查工具注册状态:")
            for attr in ['_tools', 'tools', '_handlers']:
                if hasattr(mcp_instance, attr):
                    value = getattr(mcp_instance, attr)
                    if hasattr(value, '__len__'):
                        print(f"    {attr}: {len(value)} 项")
                        if hasattr(value, 'keys'):
                            keys = list(value.keys())
                            if 'test_tool_function' in keys:
                                print(f"      ✅ 测试函数已注册")
                            else:
                                print(f"      ❌ 测试函数未找到")
                            print(f"      所有键: {keys}")
        
        # 检查FastMCP的内部结构
        print("\n🏗️  FastMCP内部结构分析:")
        
        # 检查是否有server属性
        if hasattr(mcp_instance, 'server'):
            server_obj = getattr(mcp_instance, 'server')
            print(f"  ✅ server对象: {type(server_obj)}")
            
            # 检查server对象的属性
            server_attrs = [attr for attr in dir(server_obj) if not attr.startswith('_')]
            print(f"  📋 server属性: {server_attrs[:10]}")
        
        # 检查是否有app属性
        if hasattr(mcp_instance, 'app'):
            app_obj = getattr(mcp_instance, 'app')
            print(f"  ✅ app对象: {type(app_obj)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 诊断过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    success = analyze_fastmcp_instance()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 FastMCP诊断完成")
        print("\n💡 建议:")
        print("  1. 检查FastMCP版本兼容性")
        print("  2. 确认工具装饰器语法正确")
        print("  3. 验证模块导入顺序")
        print("  4. 检查是否需要显式调用工具注册")
    else:
        print("❌ FastMCP诊断失败")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())