#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖包完整性检查脚本
检查虚拟环境中是否安装了requirements.txt中要求的所有依赖包
"""

import pkg_resources
import re
import sys
from pathlib import Path

def parse_requirements(file_path):
    """解析requirements.txt文件"""
    requirements = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            # 跳过注释和空行
            if not line or line.startswith('#'):
                continue
            
            # 提取包名和版本
            if '==' in line:
                # 处理行内注释
                if '#' in line:
                    line = line.split('#')[0].strip()
                requirements.append(line)
    
    except Exception as e:
        print(f"读取requirements.txt失败: {e}")
        return []
    
    return requirements

def get_installed_packages():
    """获取已安装的包列表"""
    installed = {}
    try:
        for pkg in pkg_resources.working_set:
            # 统一转换为小写进行比较
            installed[pkg.project_name.lower()] = pkg.version
    except Exception as e:
        print(f"获取已安装包列表失败: {e}")
    
    return installed

def normalize_package_name(name):
    """标准化包名（处理下划线和连字符的差异）"""
    return name.lower().replace('_', '-').replace('.', '-')

def check_dependencies():
    """检查依赖包完整性"""
    print("=" * 60)
    print("ChatExcel MCP Server - 依赖包完整性检查")
    print("=" * 60)
    
    # 解析requirements.txt
    requirements = parse_requirements('requirements.txt')
    print(f"requirements.txt中定义的包数量: {len(requirements)}")
    
    # 获取已安装的包
    installed = get_installed_packages()
    print(f"虚拟环境中已安装的包数量: {len(installed)}")
    print()
    
    # 分析缺失和版本不匹配的包
    missing_packages = []
    version_mismatch = []
    correct_packages = []
    
    for req in requirements:
        if '==' not in req:
            continue
            
        try:
            name, version = req.split('==')
            name = name.strip()
            version = version.strip()
            
            # 标准化包名进行比较
            normalized_name = normalize_package_name(name)
            
            # 检查是否安装
            found = False
            installed_version = None
            
            # 尝试多种包名格式
            possible_names = [
                name.lower(),
                normalized_name,
                name.lower().replace('-', '_'),
                name.lower().replace('_', '-')
            ]
            
            for possible_name in possible_names:
                if possible_name in installed:
                    found = True
                    installed_version = installed[possible_name]
                    break
            
            if not found:
                missing_packages.append(req)
            elif installed_version != version:
                version_mismatch.append({
                    'name': name,
                    'required': version,
                    'installed': installed_version
                })
            else:
                correct_packages.append(req)
                
        except ValueError:
            print(f"无法解析依赖: {req}")
    
    # 输出结果
    print("📊 检查结果统计:")
    print(f"✅ 正确安装的包: {len(correct_packages)}")
    print(f"❌ 缺失的包: {len(missing_packages)}")
    print(f"⚠️  版本不匹配的包: {len(version_mismatch)}")
    print()
    
    if missing_packages:
        print("❌ 缺失的依赖包:")
        print("-" * 40)
        for pkg in missing_packages:
            print(f"  {pkg}")
        print()
    
    if version_mismatch:
        print("⚠️  版本不匹配的包:")
        print("-" * 40)
        for pkg in version_mismatch:
            print(f"  {pkg['name']}: 要求 {pkg['required']}, 已安装 {pkg['installed']}")
        print()
    
    # 核心MCP工具依赖检查
    print("🔍 核心MCP工具依赖检查:")
    print("-" * 40)
    
    core_dependencies = {
        'fastmcp': '0.3.0',
        'mcp': '1.1.0',
        'pandas': '2.2.3',
        'numpy': '2.2.1',
        'openpyxl': '3.1.5',
        'plotly': '5.24.1',
        'matplotlib': '3.10.0',
        'formulas': '1.2.10'
    }
    
    core_status = {}
    for name, required_version in core_dependencies.items():
        normalized_name = normalize_package_name(name)
        possible_names = [
            name.lower(),
            normalized_name,
            name.lower().replace('-', '_'),
            name.lower().replace('_', '-')
        ]
        
        found = False
        installed_version = None
        
        for possible_name in possible_names:
            if possible_name in installed:
                found = True
                installed_version = installed[possible_name]
                break
        
        if found:
            if installed_version == required_version:
                status = "✅ 正确"
            else:
                status = f"⚠️  版本不匹配 (已安装: {installed_version})"
        else:
            status = "❌ 缺失"
        
        core_status[name] = status
        print(f"  {name:12} {required_version:8} {status}")
    
    print()
    
    # 安全和监控工具依赖检查
    security_deps = {
        'RestrictedPython': '7.4',
        'psutil': '6.1.0',
        'cryptography': '44.0.0',
        'pydantic': '2.11.5'
    }
    
    print("🔒 安全和监控工具依赖:")
    print("-" * 40)
    
    for name, required_version in security_deps.items():
        normalized_name = normalize_package_name(name)
        possible_names = [
            name.lower(),
            normalized_name,
            name.lower().replace('-', '_'),
            name.lower().replace('_', '-')
        ]
        
        found = False
        installed_version = None
        
        for possible_name in possible_names:
            if possible_name in installed:
                found = True
                installed_version = installed[possible_name]
                break
        
        if found:
            if installed_version == required_version:
                status = "✅ 正确"
            else:
                status = f"⚠️  版本不匹配 (已安装: {installed_version})"
        else:
            status = "❌ 缺失"
        
        print(f"  {name:18} {required_version:8} {status}")
    
    print()
    
    # 总结和建议
    print("📋 总结和建议:")
    print("-" * 40)
    
    if not missing_packages and not version_mismatch:
        print("🎉 恭喜！所有依赖包都已正确安装，MCP服务器可以正常运行。")
    else:
        print("⚠️  发现依赖问题，建议执行以下操作:")
        
        if missing_packages:
            print("\n1. 安装缺失的包:")
            for pkg in missing_packages[:5]:  # 只显示前5个
                print(f"   pip install {pkg}")
            if len(missing_packages) > 5:
                print(f"   ... 还有 {len(missing_packages) - 5} 个包")
        
        if version_mismatch:
            print("\n2. 更新版本不匹配的包:")
            for pkg in version_mismatch[:5]:  # 只显示前5个
                print(f"   pip install {pkg['name']}=={pkg['required']}")
            if len(version_mismatch) > 5:
                print(f"   ... 还有 {len(version_mismatch) - 5} 个包")
        
        print("\n3. 或者直接重新安装所有依赖:")
        print("   pip install -r requirements.txt")
    
    print("\n" + "=" * 60)
    return len(missing_packages) == 0 and len(version_mismatch) == 0

if __name__ == "__main__":
    success = check_dependencies()
    sys.exit(0 if success else 1)