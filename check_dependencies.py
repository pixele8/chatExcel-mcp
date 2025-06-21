#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖检查脚本 - 验证虚拟环境中的关键依赖
"""

import sys
import importlib
from typing import Dict, List, Tuple

def check_dependency(module_name: str, package_name: str = None) -> Tuple[bool, str]:
    """检查单个依赖的可用性
    
    Args:
        module_name: 模块名称
        package_name: 包名称（如果与模块名不同）
        
    Returns:
        Tuple[bool, str]: (是否可用, 版本信息或错误信息)
    """
    try:
        module = importlib.import_module(module_name)
        version = getattr(module, '__version__', 'Unknown')
        return True, version
    except ImportError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    """主检查函数"""
    print("🔍 ChatExcel MCP服务器依赖检查")
    print("=" * 50)
    
    # 核心依赖列表
    core_dependencies = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('fastmcp', 'fastmcp'),
        ('openpyxl', 'openpyxl'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn'),
        ('plotly', 'plotly'),
        ('chardet', 'chardet'),
        ('formulas', 'formulas'),
        ('tabulate', 'tabulate')
    ]
    
    # 可选依赖列表
    optional_dependencies = [
        ('xlrd', 'xlrd'),
        ('xlsxwriter', 'xlsxwriter'),
        ('scipy', 'scipy'),
        ('scikit-learn', 'sklearn'),
        ('requests', 'requests')
    ]
    
    success_count = 0
    total_count = 0
    
    print("\n📦 核心依赖检查:")
    for module_name, package_name in core_dependencies:
        total_count += 1
        is_available, info = check_dependency(module_name)
        if is_available:
            success_count += 1
            print(f"  ✅ {package_name}: {info}")
        else:
            print(f"  ❌ {package_name}: {info}")
    
    print("\n📦 可选依赖检查:")
    for module_name, package_name in optional_dependencies:
        is_available, info = check_dependency(module_name)
        if is_available:
            print(f"  ✅ {package_name}: {info}")
        else:
            print(f"  ⚠️  {package_name}: {info}")
    
    print("\n" + "=" * 50)
    print(f"📊 核心依赖状态: {success_count}/{total_count} 可用")
    
    if success_count == total_count:
        print("🎉 所有核心依赖都已正确安装!")
        return 0
    else:
        print("⚠️  部分核心依赖缺失，请检查虚拟环境配置")
        return 1

if __name__ == "__main__":
    sys.exit(main())