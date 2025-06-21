#!/usr/bin/env python3
"""
MCP 运行服务器工具验证脚本
连接到运行中的 ChatExcel MCP 服务器并验证工具注册状态
"""

import asyncio
import json
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print("❌ 无法导入 MCP 客户端库")
    print("请安装: pip install mcp")
    sys.exit(1)

async def verify_server_tools():
    """
    验证运行中的 MCP 服务器工具注册状态
    """
    print("🔍 验证运行中的 MCP 服务器工具...")
    print("=" * 60)
    
    # 服务器参数
    server_params = StdioServerParameters(
        command="python3",
        args=["server.py"],
        env={"PYTHONPATH": str(project_root)}
    )
    
    try:
        # 连接到服务器
        print("\n🔌 连接到 MCP 服务器...")
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                print("  ✅ 连接成功")
                
                # 初始化会话
                print("\n🚀 初始化会话...")
                await session.initialize()
                print("  ✅ 会话初始化成功")
                
                # 获取工具列表
                print("\n📋 获取工具列表...")
                tools_result = await session.list_tools()
                
                if tools_result and hasattr(tools_result, 'tools'):
                    tools = tools_result.tools
                    print(f"  📊 发现 {len(tools)} 个工具")
                    
                    if len(tools) > 0:
                        print("\n🔧 已注册的工具:")
                        for i, tool in enumerate(tools, 1):
                            print(f"  {i:2d}. {tool.name}")
                            if hasattr(tool, 'description') and tool.description:
                                print(f"      📝 {tool.description[:80]}{'...' if len(tool.description) > 80 else ''}")
                    
                    # 验证预期工具
                    expected_tools = [
                        'read_metadata', 'verify_data_integrity', 'read_excel_metadata',
                        'run_excel_code', 'run_code', 'bar_chart_to_html', 'pie_chart_to_html',
                        'line_chart_to_html', 'validate_data_quality', 'suggest_excel_read_parameters_tool',
                        'detect_excel_file_structure_tool', 'create_excel_read_template_tool',
                        'comprehensive_data_verification_tool', 'batch_data_verification_tool',
                        'excel_read_enhanced', 'excel_write_enhanced', 'excel_chart_enhanced',
                        'excel_info_enhanced', 'excel_performance_comparison', 'parse_formula',
                        'compile_workbook', 'execute_formula', 'analyze_dependencies',
                        'validate_formula', 'enhanced_data_quality_check', 'extract_cell_content_advanced',
                        'convert_character_formats', 'extract_multi_condition_data',
                        'merge_multiple_tables', 'clean_excel_data', 'batch_process_excel_files'
                    ]
                    
                    registered_tool_names = [tool.name for tool in tools]
                    
                    print("\n📊 工具验证结果:")
                    print(f"  🎯 预期工具数量: {len(expected_tools)}")
                    print(f"  📊 实际注册工具: {len(tools)}")
                    print(f"  📈 注册成功率: {len(tools)/len(expected_tools)*100:.1f}%")
                    
                    # 检查缺失的工具
                    missing_tools = [tool for tool in expected_tools if tool not in registered_tool_names]
                    if missing_tools:
                        print(f"\n⚠️  缺失的工具 ({len(missing_tools)} 个):")
                        for tool in missing_tools[:10]:  # 只显示前10个
                            print(f"    ❌ {tool}")
                        if len(missing_tools) > 10:
                            print(f"    ... 还有 {len(missing_tools) - 10} 个")
                    
                    # 检查额外的工具
                    extra_tools = [tool for tool in registered_tool_names if tool not in expected_tools]
                    if extra_tools:
                        print(f"\n➕ 额外的工具 ({len(extra_tools)} 个):")
                        for tool in extra_tools:
                            print(f"    ✨ {tool}")
                    
                    # 测试一个简单工具
                    if 'read_metadata' in registered_tool_names:
                        print("\n🧪 测试工具调用...")
                        try:
                            # 创建测试文件路径
                            test_file = project_root / "test_data.csv"
                            if not test_file.exists():
                                # 创建简单的测试CSV文件
                                test_file.write_text("name,age,city\nAlice,25,New York\nBob,30,London")
                            
                            # 调用工具
                            result = await session.call_tool(
                                "read_metadata",
                                {"file_path": str(test_file)}
                            )
                            
                            if result:
                                print("  ✅ 工具调用成功")
                                print(f"  📊 返回结果类型: {type(result)}")
                            else:
                                print("  ⚠️  工具调用返回空结果")
                                
                        except Exception as e:
                            print(f"  ❌ 工具调用失败: {e}")
                    
                    # 总结
                    print("\n" + "=" * 60)
                    if len(tools) == len(expected_tools):
                        print("🎉 所有工具注册成功! MCP 服务器运行正常")
                    elif len(tools) > 0:
                        print(f"⚠️  部分工具注册成功 ({len(tools)}/{len(expected_tools)})")
                    else:
                        print("❌ 工具注册失败")
                        
                else:
                    print("  ❌ 无法获取工具列表")
                    
    except Exception as e:
        print(f"❌ 连接服务器失败: {e}")
        print("\n💡 请确保:")
        print("  1. MCP 服务器正在运行")
        print("  2. 服务器配置正确")
        print("  3. 虚拟环境已激活")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(verify_server_tools())
    except KeyboardInterrupt:
        print("\n👋 验证已取消")
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        sys.exit(1)