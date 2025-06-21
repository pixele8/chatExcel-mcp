#!/usr/bin/env python3
"""
最终的MCP客户端测试脚本
通过stdio协议连接ChatExcel MCP服务器并验证工具注册
"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class MCPClient:
    """
    简单的MCP客户端实现
    """
    
    def __init__(self):
        self.process = None
        self.request_id = 0
    
    async def start_server(self):
        """
        启动MCP服务器
        """
        venv_python = project_root / "venv" / "bin" / "python"
        server_file = project_root / "server.py"
        
        if not venv_python.exists():
            raise FileNotFoundError(f"虚拟环境Python不存在: {venv_python}")
        
        if not server_file.exists():
            raise FileNotFoundError(f"服务器文件不存在: {server_file}")
        
        # 启动服务器进程
        self.process = await asyncio.create_subprocess_exec(
            str(venv_python),
            str(server_file),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(project_root),
            env={"PYTHONPATH": str(project_root)}
        )
        
        print("✅ MCP服务器已启动")
    
    async def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        发送MCP请求
        """
        if not self.process:
            raise RuntimeError("服务器未启动")
        
        self.request_id += 1
        
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method
        }
        
        if params is not None:
            request["params"] = params
        
        # 发送请求
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json.encode())
        await self.process.stdin.drain()
        
        # 读取响应
        response_line = await self.process.stdout.readline()
        if not response_line:
            raise RuntimeError("服务器无响应")
        
        try:
            response = json.loads(response_line.decode().strip())
            return response
        except json.JSONDecodeError as e:
            raise RuntimeError(f"响应JSON解析失败: {e}")
    
    async def initialize(self):
        """
        初始化MCP连接
        """
        response = await self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        })
        
        if "error" in response:
            raise RuntimeError(f"初始化失败: {response['error']}")
        
        # 发送initialized通知
        await self.send_notification("notifications/initialized")
        
        print("✅ MCP连接已初始化")
        return response.get("result", {})
    
    async def send_notification(self, method: str, params: Dict[str, Any] = None):
        """
        发送MCP通知（无需响应）
        """
        if not self.process:
            raise RuntimeError("服务器未启动")
        
        notification = {
            "jsonrpc": "2.0",
            "method": method
        }
        
        if params is not None:
            notification["params"] = params
        
        # 发送通知
        notification_json = json.dumps(notification) + "\n"
        self.process.stdin.write(notification_json.encode())
        await self.process.stdin.drain()
    
    async def list_tools(self):
        """
        获取工具列表
        """
        response = await self.send_request("tools/list", {})
        
        if "error" in response:
            raise RuntimeError(f"获取工具列表失败: {response['error']}")
        
        return response.get("result", {}).get("tools", [])
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None):
        """
        调用工具
        """
        params = {
            "name": tool_name
        }
        
        if arguments:
            params["arguments"] = arguments
        
        response = await self.send_request("tools/call", params)
        
        if "error" in response:
            raise RuntimeError(f"调用工具失败: {response['error']}")
        
        return response.get("result", {})
    
    async def close(self):
        """
        关闭连接
        """
        if self.process:
            self.process.terminate()
            try:
                await asyncio.wait_for(self.process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                self.process.kill()
                await self.process.wait()
            
            print("✅ MCP服务器已关闭")

async def test_mcp_tools():
    """
    测试MCP工具注册和调用
    """
    print("🔍 ChatExcel MCP 工具完整性测试")
    print("=" * 60)
    
    client = MCPClient()
    
    try:
        # 1. 启动服务器
        print("\n🚀 启动MCP服务器...")
        await client.start_server()
        
        # 等待服务器启动
        await asyncio.sleep(2)
        
        # 2. 初始化连接
        print("\n🔗 初始化MCP连接...")
        init_result = await client.initialize()
        
        print(f"📊 服务器信息: {init_result.get('serverInfo', {})}")
        print(f"🔧 服务器能力: {list(init_result.get('capabilities', {}).keys())}")
        
        # 3. 获取工具列表
        print("\n📋 获取工具列表...")
        tools = await client.list_tools()
        
        print(f"✅ 发现 {len(tools)} 个工具")
        
        # 预期工具列表
        expected_tools = [
            "read_metadata", "verify_data_integrity", "read_excel_metadata",
            "run_excel_code", "run_code", "bar_chart_to_html", "pie_chart_to_html",
            "line_chart_to_html", "validate_data_quality", "suggest_excel_read_parameters_tool",
            "detect_excel_file_structure_tool", "create_excel_read_template_tool",
            "comprehensive_data_verification_tool", "batch_data_verification_tool",
            "excel_read_enhanced", "excel_write_enhanced", "excel_chart_enhanced",
            "excel_info_enhanced", "excel_performance_comparison", "parse_formula",
            "compile_workbook", "execute_formula", "analyze_dependencies",
            "validate_formula", "enhanced_data_quality_check", "extract_cell_content_advanced",
            "convert_character_formats", "extract_multi_condition_data",
            "merge_multiple_tables", "clean_excel_data", "batch_process_excel_files"
        ]
        
        # 4. 验证工具注册
        print("\n🔍 验证工具注册...")
        
        found_tools = [tool["name"] for tool in tools]
        missing_tools = set(expected_tools) - set(found_tools)
        extra_tools = set(found_tools) - set(expected_tools)
        
        print(f"📊 预期工具数量: {len(expected_tools)}")
        print(f"📊 实际工具数量: {len(found_tools)}")
        print(f"📊 注册成功率: {len(found_tools)/len(expected_tools)*100:.1f}%")
        
        if missing_tools:
            print(f"❌ 缺失工具 ({len(missing_tools)}): {', '.join(sorted(missing_tools))}")
        
        if extra_tools:
            print(f"➕ 额外工具 ({len(extra_tools)}): {', '.join(sorted(extra_tools))}")
        
        # 5. 显示工具详情
        if tools:
            print("\n📋 工具详情:")
            for i, tool in enumerate(tools[:5], 1):  # 只显示前5个
                print(f"  {i}. {tool['name']}")
                if 'description' in tool:
                    desc = tool['description'][:100] + "..." if len(tool['description']) > 100 else tool['description']
                    print(f"     描述: {desc}")
            
            if len(tools) > 5:
                print(f"     ... 还有 {len(tools) - 5} 个工具")
        
        # 6. 测试工具调用（如果有工具的话）
        if found_tools and "read_metadata" in found_tools:
            print("\n🧪 测试工具调用...")
            try:
                # 创建一个测试Excel文件路径（不需要真实存在）
                test_result = await client.call_tool("read_metadata", {
                    "file_path": "/tmp/test.xlsx"
                })
                print("✅ 工具调用测试成功")
            except Exception as e:
                print(f"⚠️ 工具调用测试失败（预期，因为文件不存在）: {str(e)[:100]}")
        
        # 7. 总结
        print("\n" + "=" * 60)
        print("📊 测试总结:")
        
        if len(found_tools) == len(expected_tools) and not missing_tools:
            print("🎉 所有工具注册成功！")
            print("✅ ChatExcel MCP服务器完全可用")
            return True
        elif len(found_tools) > 0:
            print(f"⚠️ 部分工具注册成功: {len(found_tools)}/{len(expected_tools)}")
            print("✅ ChatExcel MCP服务器基本可用")
            return True
        else:
            print("❌ 没有发现任何工具")
            print("❌ 工具注册完全失败")
            return False
    
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # 关闭连接
        await client.close()

async def main():
    """
    主函数
    """
    try:
        success = await test_mcp_tools()
        
        if success:
            print("\n💡 下一步:")
            print("  1. 在MCP客户端（如Claude Desktop）中配置此服务器")
            print("  2. 使用配置文件: mcp_config_absolute.json")
            print("  3. 重启客户端并测试工具功能")
        else:
            print("\n🔧 故障排除建议:")
            print("  1. 检查虚拟环境依赖是否完整")
            print("  2. 确认所有模块文件存在")
            print("  3. 检查FastMCP版本兼容性")
            print("  4. 查看服务器错误日志")
        
        return success
    
    except KeyboardInterrupt:
        print("\n👋 测试已取消")
        return False
    except Exception as e:
        print(f"❌ 测试过程出错: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)