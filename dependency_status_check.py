#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖状态详细检查
专门检查XlsxWriter和其他关键依赖的安装状态
"""

import sys
import importlib
import pkg_resources
from typing import Dict, List, Tuple

def check_dependency_status() -> Dict[str, Dict]:
    """
    检查所有关键依赖的详细状态
    
    Returns:
        Dict: 包含每个依赖的详细状态信息
    """
    
    # 关键依赖列表
    critical_dependencies = [
        'pandas', 'numpy', 'openpyxl', 'xlrd', 'xlsxwriter',
        'matplotlib', 'seaborn', 'plotly', 'tabulate', 
        'formulas', 'fastmcp', 'mcp'
    ]
    
    results = {}
    
    print("🔍 详细依赖状态检查")
    print("=" * 60)
    
    for dep in critical_dependencies:
        status = {
            'installed': False,
            'version': None,
            'import_success': False,
            'location': None,
            'error': None
        }
        
        try:
            # 检查是否通过pip安装
            try:
                # 对于xlsxwriter，包名是XlsxWriter（大写）
                pkg_name = 'XlsxWriter' if dep == 'xlsxwriter' else dep
                dist = pkg_resources.get_distribution(pkg_name)
                status['installed'] = True
                status['version'] = dist.version
                status['location'] = dist.location
            except pkg_resources.DistributionNotFound:
                # 对于某些包，尝试不同的名称
                alt_names = {
                    'fastmcp': ['mcp', 'fastmcp'],
                    'mcp': ['mcp', 'fastmcp'],
                    'xlsxwriter': ['XlsxWriter', 'xlsxwriter']
                }
                
                if dep in alt_names:
                    for alt_name in alt_names[dep]:
                        try:
                            dist = pkg_resources.get_distribution(alt_name)
                            status['installed'] = True
                            status['version'] = dist.version
                            status['location'] = dist.location
                            break
                        except pkg_resources.DistributionNotFound:
                            continue
            
            # 检查是否可以导入
            try:
                if dep == 'fastmcp':
                    # 特殊处理FastMCP
                    from mcp.server.fastmcp import FastMCP
                    status['import_success'] = True
                elif dep == 'mcp':
                    import mcp
                    status['import_success'] = True
                elif dep == 'xlsxwriter':
                    # XlsxWriter包名是大写但导入时用小写
                    import xlsxwriter
                    status['import_success'] = True
                else:
                    importlib.import_module(dep)
                    status['import_success'] = True
            except ImportError as e:
                status['error'] = str(e)
                
        except Exception as e:
            status['error'] = str(e)
        
        results[dep] = status
        
        # 打印状态
        if status['installed'] and status['import_success']:
            print(f"✅ {dep:<15} v{status['version']:<10} - 正常")
        elif status['installed'] and not status['import_success']:
            print(f"⚠️  {dep:<15} v{status['version']:<10} - 已安装但导入失败")
            if status['error']:
                print(f"   错误: {status['error']}")
        elif not status['installed']:
            print(f"❌ {dep:<15} {'未安装':<10} - 缺失")
        else:
            print(f"❓ {dep:<15} {'未知状态':<10} - 检查失败")
            if status['error']:
                print(f"   错误: {status['error']}")
    
    return results

def check_virtual_environment() -> Dict[str, str]:
    """
    检查虚拟环境状态
    
    Returns:
        Dict: 虚拟环境信息
    """
    
    venv_info = {
        'python_path': sys.executable,
        'python_version': sys.version,
        'in_venv': False,
        'venv_path': None
    }
    
    # 检查是否在虚拟环境中
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        venv_info['in_venv'] = True
        venv_info['venv_path'] = sys.prefix
    
    # 额外检查路径中是否包含venv
    if 'venv' in sys.executable:
        venv_info['in_venv'] = True
        if not venv_info['venv_path']:
            venv_info['venv_path'] = sys.executable.split('/venv/')[0] + '/venv'
    
    return venv_info

def generate_summary(dep_results: Dict, venv_info: Dict) -> None:
    """
    生成检查总结
    
    Args:
        dep_results: 依赖检查结果
        venv_info: 虚拟环境信息
    """
    
    print("\n" + "=" * 60)
    print("📋 检查总结")
    print("=" * 60)
    
    # 虚拟环境状态
    if venv_info['in_venv']:
        print(f"✅ 虚拟环境: 正常 ({venv_info['venv_path']})")
    else:
        print("❌ 虚拟环境: 未检测到虚拟环境")
    
    # 依赖统计
    total_deps = len(dep_results)
    installed_deps = sum(1 for dep in dep_results.values() if dep['installed'])
    working_deps = sum(1 for dep in dep_results.values() if dep['installed'] and dep['import_success'])
    
    print(f"📦 依赖状态: {working_deps}/{total_deps} 正常工作")
    print(f"📦 安装状态: {installed_deps}/{total_deps} 已安装")
    
    # 问题依赖
    problem_deps = []
    for name, status in dep_results.items():
        if not status['installed']:
            problem_deps.append(f"{name} (未安装)")
        elif not status['import_success']:
            problem_deps.append(f"{name} (导入失败)")
    
    if problem_deps:
        print(f"⚠️  问题依赖: {', '.join(problem_deps)}")
    else:
        print("✅ 所有依赖正常")
    
    # 特别检查XlsxWriter
    xlsx_status = dep_results.get('xlsxwriter', {})
    if xlsx_status.get('installed') and xlsx_status.get('import_success'):
        print(f"✅ XlsxWriter: v{xlsx_status['version']} - 正常")
    elif xlsx_status.get('installed'):
        print(f"⚠️  XlsxWriter: v{xlsx_status['version']} - 已安装但有问题")
    else:
        print("❌ XlsxWriter: 未安装")

def main():
    """
    主函数
    """
    
    print("🔍 开始依赖状态详细检查...\n")
    
    # 检查虚拟环境
    print("1️⃣ 虚拟环境检查")
    print("-" * 30)
    venv_info = check_virtual_environment()
    print(f"Python路径: {venv_info['python_path']}")
    print(f"虚拟环境: {'是' if venv_info['in_venv'] else '否'}")
    if venv_info['venv_path']:
        print(f"环境路径: {venv_info['venv_path']}")
    
    print("\n2️⃣ 依赖检查")
    print("-" * 30)
    
    # 检查依赖
    dep_results = check_dependency_status()
    
    # 生成总结
    generate_summary(dep_results, venv_info)
    
    # 返回状态码
    all_working = all(dep['installed'] and dep['import_success'] for dep in dep_results.values())
    
    if all_working and venv_info['in_venv']:
        print("\n🎉 所有检查通过！")
        return 0
    else:
        print("\n⚠️  存在一些问题，请查看上述详情")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)