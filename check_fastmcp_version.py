#!/usr/bin/env python3
"""
检查 FastMCP 版本和属性
"""

try:
    import fastmcp
    print(f"FastMCP 版本: {getattr(fastmcp, '__version__', '未知')}")
    print(f"FastMCP 路径: {fastmcp.__file__}")
    print(f"FastMCP 主要属性: {[attr for attr in dir(fastmcp) if not attr.startswith('_')]}")
    
    # 检查 FastMCP 类
    if hasattr(fastmcp, 'FastMCP'):
        FastMCP = fastmcp.FastMCP
        print(f"\nFastMCP 类属性: {[attr for attr in dir(FastMCP) if not attr.startswith('_')]}")
        
        # 创建一个测试实例
        test_mcp = FastMCP("test")
        print(f"\nFastMCP 实例属性: {[attr for attr in dir(test_mcp) if not attr.startswith('_')]}")
        
        # 检查 tool 方法
        if hasattr(test_mcp, 'tool'):
            print(f"\ntool 方法类型: {type(test_mcp.tool)}")
            print(f"tool 方法属性: {dir(test_mcp.tool)}")
        
except ImportError as e:
    print(f"导入 FastMCP 失败: {e}")
except Exception as e:
    print(f"检查 FastMCP 时出错: {e}")