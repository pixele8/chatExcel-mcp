#!/usr/bin/env python3
"""
项目健康检查脚本
检查项目的各个方面是否正常运行
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    return False, f"Python版本过低: {version.major}.{version.minor}.{version.micro}"

def check_virtual_environment():
    """检查虚拟环境"""
    venv_path = Path("venv")
    if venv_path.exists() and venv_path.is_dir():
        return True, "虚拟环境存在"
    return False, "虚拟环境不存在"

def check_dependencies():
    """检查依赖包"""
    try:
        result = subprocess.run(["pip", "check"], capture_output=True, text=True)
        if result.returncode == 0:
            return True, "依赖包完整性检查通过"
        return False, f"依赖包问题: {result.stdout}"
    except Exception as e:
        return False, f"依赖检查失败: {str(e)}"

def check_file_structure():
    """检查文件结构"""
    required_files = [
        "server.py",
        "config.py", 
        "pyproject.toml",
        "README.md"
    ]
    
    required_dirs = [
        "templates",
        "tests",
        "charts"
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            missing_dirs.append(dir_name)
    
    if not missing_files and not missing_dirs:
        return True, "文件结构完整"
    
    issues = []
    if missing_files:
        issues.append(f"缺失文件: {', '.join(missing_files)}")
    if missing_dirs:
        issues.append(f"缺失目录: {', '.join(missing_dirs)}")
    
    return False, "; ".join(issues)

def check_server_import():
    """检查服务器模块导入"""
    try:
        # 添加项目根目录到Python路径
        project_root = Path(__file__).parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        
        import server
        return True, "服务器模块导入成功"
    except Exception as e:
        return False, f"服务器模块导入失败: {str(e)}"

def generate_health_report():
    """生成健康检查报告"""
    checks = [
        ("Python版本", check_python_version),
        ("虚拟环境", check_virtual_environment),
        ("依赖包", check_dependencies),
        ("文件结构", check_file_structure),
        ("服务器模块", check_server_import)
    ]
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "checks": [],
        "overall_status": "HEALTHY"
    }
    
    print("🏥 项目健康检查报告")
    print("=" * 50)
    
    for check_name, check_func in checks:
        try:
            status, message = check_func()
            check_result = {
                "name": check_name,
                "status": "PASS" if status else "FAIL",
                "message": message
            }
            report["checks"].append(check_result)
            
            status_icon = "✅" if status else "❌"
            print(f"{status_icon} {check_name}: {message}")
            
            if not status:
                report["overall_status"] = "UNHEALTHY"
                
        except Exception as e:
            check_result = {
                "name": check_name,
                "status": "ERROR",
                "message": f"检查失败: {str(e)}"
            }
            report["checks"].append(check_result)
            print(f"❌ {check_name}: 检查失败 - {str(e)}")
            report["overall_status"] = "UNHEALTHY"
    
    print("=" * 50)
    print(f"🎯 总体状态: {report['overall_status']}")
    
    # 保存报告
    with open("health_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    return report["overall_status"] == "HEALTHY"

if __name__ == "__main__":
    success = generate_health_report()
    sys.exit(0 if success else 1)