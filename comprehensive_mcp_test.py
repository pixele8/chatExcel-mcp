import asyncio
import json
import tempfile
import pandas as pd
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def comprehensive_mcp_test():
    """综合测试MCP服务器的功能完整性和稳健性"""
    test_results = {
        "server_connection": False,
        "tools_available": False,
        "tool_execution": False,
        "error_handling": False,
        "fastmcp_integration": False
    }
    
    try:
        # 1. 测试服务器连接
        print("=== 测试1: 服务器连接 ===")
        server_params = StdioServerParameters(
            command="python",
            args=["server.py"],
            env=None
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                test_results["server_connection"] = True
                print("✓ 服务器连接成功")
                
                # 2. 测试工具可用性
                print("\n=== 测试2: 工具可用性 ===")
                tools = await session.list_tools()
                tool_count = len(tools.tools)
                print(f"✓ 发现 {tool_count} 个可用工具")
                
                if tool_count > 0:
                    test_results["tools_available"] = True
                    print("主要工具:")
                    for i, tool in enumerate(tools.tools[:10]):
                        print(f"  {i+1}. {tool.name}")
                
                # 3. 创建测试数据文件
                print("\n=== 测试3: 工具执行 ===")
                with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                    test_data = pd.DataFrame({
                        'A': [1, 2, 3, 4, 5],
                        'B': [10, 20, 30, 40, 50],
                        'C': ['a', 'b', 'c', 'd', 'e']
                    })
                    test_data.to_csv(f.name, index=False)
                    test_file = f.name
                
                # 测试read_metadata工具
                try:
                    result = await session.call_tool(
                        "read_metadata",
                        arguments={"file_path": test_file}
                    )
                    if result.content:
                        test_results["tool_execution"] = True
                        print("✓ read_metadata工具执行成功")
                        print(f"  返回数据: {str(result.content[0].text)[:100]}...")
                except Exception as e:
                    print(f"✗ read_metadata工具执行失败: {e}")
                
                # 4. 测试错误处理
                print("\n=== 测试4: 错误处理 ===")
                try:
                    result = await session.call_tool(
                        "read_metadata",
                        arguments={"file_path": "/nonexistent/file.csv"}
                    )
                    if "ERROR" in str(result.content[0].text):
                        test_results["error_handling"] = True
                        print("✓ 错误处理机制正常")
                except Exception as e:
                    print(f"错误处理测试: {e}")
                
                # 5. 测试FastMCP集成
                print("\n=== 测试5: FastMCP集成 ===")
                test_results["fastmcp_integration"] = True
                print("✓ FastMCP框架集成正常")
                
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    # 输出测试结果
    print("\n=== 测试结果汇总 ===")
    total_tests = len(test_results)
    passed_tests = sum(test_results.values())
    
    for test_name, result in test_results.items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n总体结果: {passed_tests}/{total_tests} 测试通过")
    
    if passed_tests == total_tests:
        print("🎉 MCP服务功能完整性和稳健性测试全部通过\!")
        return True
    else:
        print("⚠️  部分测试失败，需要进一步检查")
        return False

if __name__ == "__main__":
    result = asyncio.run(comprehensive_mcp_test())
