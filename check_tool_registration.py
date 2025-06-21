#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具注册检查脚本 - 验证FastMCP中31个工具的注册状态
"""

import sys
import os
import inspect
from typing import Dict, List, Any

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_tool_registration():
    """检查工具注册状态"""
    print("🔍 ChatExcel MCP工具注册检查")
    print("=" * 50)
    
    try:
        # 导入服务器模块
        import server
        print("✅ 服务器模块导入成功")
        
        # 获取MCP实例
        mcp_instance = getattr(server, 'mcp', None)
        if not mcp_instance:
            print("❌ MCP实例未找到")
            return False
        
        print(f"✅ MCP实例类型: {type(mcp_instance)}")
        
        # 检查MCP实例的属性
        print("\n📋 MCP实例属性:")
        for attr in dir(mcp_instance):
            if not attr.startswith('_'):
                print(f"  - {attr}")
        
        # 尝试不同的方式获取工具
        tools = []
        tool_source = "未知"
        
        # 方法1: 检查_tools属性
        if hasattr(mcp_instance, '_tools'):
            tools = list(mcp_instance._tools.keys())
            tool_source = "_tools属性"
        
        # 方法2: 检查tools属性
        elif hasattr(mcp_instance, 'tools'):
            tools = list(mcp_instance.tools.keys())
            tool_source = "tools属性"
        
        # 方法3: 检查_handlers属性
        elif hasattr(mcp_instance, '_handlers'):
            handlers = getattr(mcp_instance, '_handlers', {})
            if 'tools' in handlers:
                tools = list(handlers['tools'].keys())
                tool_source = "_handlers.tools"
        
        # 方法4: 检查registry属性
        elif hasattr(mcp_instance, 'registry'):
            registry = getattr(mcp_instance, 'registry', {})
            if hasattr(registry, 'tools'):
                tools = list(registry.tools.keys())
                tool_source = "registry.tools"
        
        print(f"\n📊 工具注册状态 (来源: {tool_source}):")
        print(f"  - 注册工具数量: {len(tools)}")
        
        if tools:
            print("\n📝 已注册工具列表:")
            for i, tool_name in enumerate(tools, 1):
                print(f"  {i:2d}. {tool_name}")
        else:
            print("\n⚠️  未检测到已注册的工具")
            
            # 尝试查找@mcp.tool装饰的函数
            print("\n🔍 搜索@mcp.tool装饰的函数:")
            decorated_functions = []
            
            for name, obj in inspect.getmembers(server):
                if inspect.isfunction(obj):
                    # 检查函数是否有MCP工具装饰器的标记
                    if hasattr(obj, '__mcp_tool__') or hasattr(obj, '_mcp_tool'):
                        decorated_functions.append(name)
            
            if decorated_functions:
                print(f"  找到 {len(decorated_functions)} 个装饰函数:")
                for func in decorated_functions:
                    print(f"    - {func}")
            else:
                print("  未找到装饰函数标记")
        
        # 检查MCP实例的内部状态
        print("\n🔧 MCP实例内部状态:")
        
        # 检查是否有工具注册方法
        registration_methods = ['tool', 'register_tool', 'add_tool']
        for method in registration_methods:
            if hasattr(mcp_instance, method):
                print(f"  ✅ 发现注册方法: {method}")
            else:
                print(f"  ❌ 未发现注册方法: {method}")
        
        # 检查FastMCP特有属性
        fastmcp_attrs = ['_tool_registry', '_resource_registry', '_prompt_registry']
        for attr in fastmcp_attrs:
            if hasattr(mcp_instance, attr):
                attr_value = getattr(mcp_instance, attr)
                print(f"  ✅ {attr}: {type(attr_value)} (长度: {len(attr_value) if hasattr(attr_value, '__len__') else 'N/A'})")
            else:
                print(f"  ❌ 未发现属性: {attr}")
        
        # 总结
        print("\n" + "=" * 50)
        expected_tools = 31
        actual_tools = len(tools)
        
        if actual_tools == expected_tools:
            print(f"🎉 工具注册完整! ({actual_tools}/{expected_tools})")
            return True
        elif actual_tools > 0:
            print(f"⚠️  工具部分注册 ({actual_tools}/{expected_tools})")
            return False
        else:
            print(f"❌ 工具未注册 (0/{expected_tools})")
            print("\n💡 可能的原因:")
            print("  1. FastMCP版本不兼容")
            print("  2. 工具装饰器未正确应用")
            print("  3. 模块导入时发生错误")
            print("  4. MCP实例初始化问题")
            return False
            
    except Exception as e:
        print(f"❌ 检查过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    success = check_tool_registration()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())