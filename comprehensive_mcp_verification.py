#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面的MCP工具验证脚本
验证所有31个MCP工具是否正确配置在虚拟环境中
"""

import sys
import os
import inspect
import re
from typing import List, Dict, Any

# 添加项目路径
project_path = '/Users/wangdada/Downloads/mcp/chatExcel-mcp'
sys.path.insert(0, project_path)
os.chdir(project_path)

def check_virtual_environment():
    """检查虚拟环境状态"""
    print("🔍 检查虚拟环境状态...")
    
    # 检查Python路径
    python_path = sys.executable
    print(f"Python路径: {python_path}")
    
    # 检查是否在虚拟环境中
    if 'venv' in python_path or 'virtualenv' in python_path:
        print("✅ 运行在虚拟环境中")
    else:
        print("⚠️  可能不在虚拟环境中")
    
    # 检查关键依赖
    dependencies = [
        'pandas', 'numpy', 'openpyxl', 'xlrd', 'XlsxWriter',
        'matplotlib', 'seaborn', 'plotly', 'chardet', 'scipy',
        'requests', 'pydantic', 'tabulate', 'formulas'
    ]
    
    missing_deps = []
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} - 已安装")
        except ImportError:
            print(f"❌ {dep} - 缺失")
            missing_deps.append(dep)
    
    return len(missing_deps) == 0

def check_server_import():
    """检查server.py导入"""
    print("\n🔍 检查server.py导入...")
    
    try:
        import server
        print("✅ server.py导入成功")
        
        # 检查MCP实例
        if hasattr(server, 'mcp'):
            print("✅ MCP实例存在")
            return server.mcp, server
        else:
            print("❌ MCP实例不存在")
            return None, server
            
    except Exception as e:
        print(f"❌ server.py导入失败: {e}")
        return None, None

def analyze_mcp_tools_from_source():
    """从源代码分析MCP工具"""
    print("\n🔍 从源代码分析MCP工具...")
    
    tools = []
    
    try:
        with open('server.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找所有@mcp.tool()装饰器
        tool_pattern = r'@mcp\.tool\(\)\s*\ndef\s+(\w+)\s*\('
        matches = re.findall(tool_pattern, content)
        
        print(f"✅ 发现 {len(matches)} 个MCP工具")
        
        for i, tool_name in enumerate(matches, 1):
            print(f"  {i:2d}. {tool_name}")
            tools.append({
                'name': tool_name,
                'source': 'server.py'
            })
        
        return tools
        
    except Exception as e:
        print(f"❌ 源代码分析失败: {e}")
        return []

def analyze_mcp_tools_from_instance(mcp_instance, server_module):
    """从MCP实例分析工具（安全方式）"""
    print("\n🔍 从MCP实例分析工具...")
    
    if not mcp_instance or not server_module:
        print("❌ 无法分析，MCP实例或server模块不存在")
        return []
    
    tools = []
    
    try:
        # 安全地获取工具信息，避免访问session_manager
        safe_attrs = ['name', '_tools', 'tools']
        
        for attr_name in safe_attrs:
            if hasattr(mcp_instance, attr_name):
                attr = getattr(mcp_instance, attr_name)
                print(f"✅ 找到属性: {attr_name} = {type(attr)}")
                
                if attr_name == '_tools' and isinstance(attr, dict):
                    for tool_name, tool_info in attr.items():
                        tools.append({
                            'name': tool_name,
                            'info': str(tool_info)[:100] + '...' if len(str(tool_info)) > 100 else str(tool_info)
                        })
        
        # 如果没有找到工具，尝试从server模块获取
        if not tools:
            print("⚠️  从实例未找到工具，尝试从模块获取...")
            
            for name in dir(server_module):
                obj = getattr(server_module, name)
                if callable(obj) and hasattr(obj, '__name__') and not name.startswith('_'):
                    # 检查是否可能是MCP工具
                    if hasattr(obj, '__wrapped__') or 'mcp' in str(type(obj)).lower():
                        tools.append({
                            'name': name,
                            'type': str(type(obj))
                        })
        
        print(f"✅ 从实例发现 {len(tools)} 个工具")
        
        for i, tool in enumerate(tools, 1):
            print(f"  {i:2d}. {tool['name']}")
        
        return tools
        
    except Exception as e:
        print(f"❌ 实例分析失败: {e}")
        return []

def check_tool_functions(server_module):
    """检查工具函数的可用性"""
    print("\n🔍 检查工具函数可用性...")
    
    if not server_module:
        print("❌ server模块不可用")
        return []
    
    issues = []
    tool_functions = []
    
    # 从源代码获取工具名称
    try:
        with open('server.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        tool_pattern = r'@mcp\.tool\(\)\s*\ndef\s+(\w+)\s*\('
        tool_names = re.findall(tool_pattern, content)
        
        for tool_name in tool_names:
            try:
                if hasattr(server_module, tool_name):
                    func = getattr(server_module, tool_name)
                    if callable(func):
                        sig = inspect.signature(func)
                        print(f"✅ {tool_name} - 函数可用，签名: {sig}")
                        tool_functions.append({
                            'name': tool_name,
                            'signature': str(sig),
                            'status': 'OK'
                        })
                    else:
                        print(f"❌ {tool_name} - 不可调用")
                        issues.append(f"{tool_name}: 不可调用")
                else:
                    print(f"❌ {tool_name} - 函数不存在")
                    issues.append(f"{tool_name}: 函数不存在")
                    
            except Exception as e:
                print(f"❌ {tool_name} - 检查失败: {e}")
                issues.append(f"{tool_name}: {str(e)}")
        
        return tool_functions, issues
        
    except Exception as e:
        print(f"❌ 工具函数检查失败: {e}")
        return [], [str(e)]

def generate_report(env_ok, source_tools, instance_tools, tool_functions, function_issues):
    """生成验证报告"""
    print("\n📊 生成验证报告...")
    
    report = {
        'virtual_environment': {
            'status': 'OK' if env_ok else 'ISSUES',
            'python_path': sys.executable
        },
        'mcp_tools_analysis': {
            'source_analysis': {
                'count': len(source_tools),
                'tools': [tool['name'] for tool in source_tools]
            },
            'instance_analysis': {
                'count': len(instance_tools),
                'tools': [tool['name'] for tool in instance_tools]
            },
            'function_analysis': {
                'count': len(tool_functions),
                'working_tools': [tool['name'] for tool in tool_functions if tool['status'] == 'OK'],
                'issues_count': len(function_issues),
                'issues': function_issues
            }
        },
        'summary': {
            'expected_tools': 31,
            'source_tools_found': len(source_tools),
            'working_functions': len([t for t in tool_functions if t['status'] == 'OK']),
            'overall_status': 'OK' if (len(source_tools) == 31 and len(function_issues) == 0) else 'ISSUES'
        }
    }
    
    # 保存报告
    import json
    with open('mcp_verification_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"📄 报告已保存到: mcp_verification_report.json")
    
    return report

def print_summary(report):
    """打印总结"""
    print("\n" + "="*60)
    print("📋 MCP工具验证总结")
    print("="*60)
    
    # 虚拟环境状态
    env_status = "✅ 正常" if report['virtual_environment']['status'] == 'OK' else "❌ 有问题"
    print(f"虚拟环境: {env_status}")
    
    # MCP工具状态
    expected = report['summary']['expected_tools']
    source_found = report['summary']['source_tools_found']
    working = report['summary']['working_functions']
    
    print(f"源代码工具数量: {source_found}/{expected} {'✅' if source_found == expected else '⚠️'}")
    print(f"可工作的工具: {working}/{source_found} {'✅' if working == source_found else '⚠️'}")
    
    # 问题统计
    issues_count = report['mcp_tools_analysis']['function_analysis']['issues_count']
    if issues_count > 0:
        print(f"函数问题: {issues_count}个")
        for issue in report['mcp_tools_analysis']['function_analysis']['issues'][:5]:  # 只显示前5个
            print(f"  - {issue}")
        if issues_count > 5:
            print(f"  ... 还有{issues_count - 5}个问题")
    
    # 总体状态
    overall_status = "✅ 全部正常" if report['summary']['overall_status'] == 'OK' else "⚠️  需要修复"
    print(f"\n总体状态: {overall_status}")
    
    if report['summary']['overall_status'] != 'OK':
        print("\n🔧 建议修复措施:")
        if report['virtual_environment']['status'] != 'OK':
            print("  - 检查虚拟环境配置和依赖安装")
        if source_found != expected:
            print(f"  - 检查server.py中的工具定义（期望{expected}个，找到{source_found}个）")
        if issues_count > 0:
            print("  - 修复工具函数的语法或导入问题")

def main():
    """主函数"""
    print("🚀 开始MCP工具全面验证...")
    print(f"项目路径: {project_path}")
    
    # 1. 检查虚拟环境
    env_ok = check_virtual_environment()
    
    # 2. 检查server.py导入
    mcp_instance, server_module = check_server_import()
    
    # 3. 从源代码分析MCP工具
    source_tools = analyze_mcp_tools_from_source()
    
    # 4. 从实例分析MCP工具（如果可能）
    instance_tools = analyze_mcp_tools_from_instance(mcp_instance, server_module)
    
    # 5. 检查工具函数
    tool_functions, function_issues = check_tool_functions(server_module)
    
    # 6. 生成报告
    report = generate_report(env_ok, source_tools, instance_tools, tool_functions, function_issues)
    
    # 7. 打印总结
    print_summary(report)
    
    return report

if __name__ == "__main__":
    try:
        report = main()
    except Exception as e:
        print(f"\n❌ 验证过程中出现错误: {e}")
        import traceback
        traceback.print_exc()