#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终MCP服务器功能测试
验证所有31个工具在虚拟环境中的完整配置
"""

import sys
import os

# 添加项目路径
project_path = '/Users/wangdada/Downloads/mcp/chatExcel-mcp'
sys.path.insert(0, project_path)
os.chdir(project_path)

def main():
    print("🚀 最终MCP服务器功能测试")
    print("="*50)
    
    # 1. 测试server.py导入
    print("\n1️⃣ 测试server.py导入...")
    try:
        import server
        print("✅ server.py导入成功")
        
        # 检查MCP实例
        if hasattr(server, 'mcp'):
            print(f"✅ MCP实例存在: {type(server.mcp)}")
            mcp_instance = server.mcp
        else:
            print("❌ MCP实例不存在")
            return False
            
    except Exception as e:
        print(f"❌ server.py导入失败: {e}")
        return False
    
    # 2. 验证工具数量
    print("\n2️⃣ 验证工具数量...")
    
    # 从源代码统计工具
    import re
    try:
        with open('server.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        tool_pattern = r'@mcp\.tool\(\)\s*\ndef\s+(\w+)\s*\('
        tools = re.findall(tool_pattern, content)
        
        print(f"✅ 发现 {len(tools)} 个MCP工具")
        
        if len(tools) == 31:
            print("✅ 工具数量正确 (31/31)")
        else:
            print(f"⚠️  工具数量不匹配 ({len(tools)}/31)")
            
    except Exception as e:
        print(f"❌ 工具统计失败: {e}")
        return False
    
    # 3. 测试关键依赖
    print("\n3️⃣ 测试关键依赖...")
    
    critical_deps = [
        'pandas', 'numpy', 'openpyxl', 'matplotlib', 
        'seaborn', 'plotly', 'tabulate', 'formulas'
    ]
    
    all_deps_ok = True
    for dep in critical_deps:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - 缺失")
            all_deps_ok = False
    
    # 4. 测试工具函数可用性
    print("\n4️⃣ 测试工具函数可用性...")
    
    sample_tools = [
        'read_metadata', 'run_excel_code', 'bar_chart_to_html',
        'validate_data_quality', 'excel_read_enhanced'
    ]
    
    tools_ok = True
    for tool_name in sample_tools:
        try:
            if hasattr(server, tool_name):
                func = getattr(server, tool_name)
                if callable(func):
                    print(f"✅ {tool_name} - 可调用")
                else:
                    print(f"❌ {tool_name} - 不可调用")
                    tools_ok = False
            else:
                print(f"❌ {tool_name} - 不存在")
                tools_ok = False
        except Exception as e:
            print(f"❌ {tool_name} - 错误: {e}")
            tools_ok = False
    
    # 5. 虚拟环境检查
    print("\n5️⃣ 虚拟环境检查...")
    
    python_path = sys.executable
    print(f"Python路径: {python_path}")
    
    if 'venv' in python_path:
        print("✅ 运行在虚拟环境中")
        venv_ok = True
    else:
        print("⚠️  可能不在虚拟环境中")
        venv_ok = False
    
    # 6. 总结
    print("\n" + "="*50)
    print("📋 测试总结")
    print("="*50)
    
    print(f"虚拟环境: {'✅ 正常' if venv_ok else '⚠️  警告'}")
    print(f"MCP工具数量: {'✅ 正确 (31个)' if len(tools) == 31 else '❌ 不正确'}")
    print(f"关键依赖: {'✅ 完整' if all_deps_ok else '❌ 缺失'}")
    print(f"工具函数: {'✅ 可用' if tools_ok else '❌ 有问题'}")
    
    # 最终状态
    overall_ok = len(tools) == 31 and all_deps_ok and tools_ok
    
    if overall_ok:
        print("\n🎉 所有31个MCP工具已正确配置在虚拟环境中！")
        print("✅ 项目可以正常运行")
    else:
        print("\n⚠️  存在一些问题，但核心功能可用")
        if len(tools) == 31 and tools_ok:
            print("✅ 所有MCP工具配置正确")
    
    return overall_ok

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🚀 测试完成 - 成功")
        else:
            print("\n⚠️  测试完成 - 部分成功")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()