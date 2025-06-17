import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp_server():
    try:
        # 创建服务器参数
        server_params = StdioServerParameters(
            command="python",
            args=["server.py"],
            env=None
        )
        
        # 连接到服务器
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # 初始化
                await session.initialize()
                
                # 列出可用工具
                tools = await session.list_tools()
                print(f"Available tools: {len(tools.tools)}")
                for tool in tools.tools[:5]:  # 显示前5个工具
                    print(f"- {tool.name}: {tool.description[:100]}...")
                
                return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_mcp_server())
    print(f"Test result: {'SUCCESS' if result else 'FAILED'}")
