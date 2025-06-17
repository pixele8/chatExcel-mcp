#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖审计和清理工具
用于分析项目依赖关系，识别冗余和安全风险
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
import pkg_resources
import requests
from datetime import datetime

class DependencyAuditor:
    """依赖审计器"""
    
    def __init__(self, project_root: str):
        """初始化审计器
        
        Args:
            project_root: 项目根目录路径
        """
        self.project_root = Path(project_root)
        self.requirements_file = self.project_root / "requirements.txt"
        self.pyproject_file = self.project_root / "pyproject.toml"
        self.uv_lock_file = self.project_root / "uv.lock"
        
    def analyze_dependencies(self) -> Dict:
        """分析项目依赖关系
        
        Returns:
            包含依赖分析结果的字典
        """
        print("🔍 开始依赖分析...")
        
        # 读取依赖文件
        requirements = self._read_requirements()
        pyproject_deps = self._read_pyproject_dependencies()
        installed_packages = self._get_installed_packages()
        
        # 分析结果
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "total_requirements": len(requirements),
            "total_pyproject_deps": len(pyproject_deps),
            "total_installed": len(installed_packages),
            "redundant_deps": self._find_redundant_dependencies(requirements, pyproject_deps),
            "unused_deps": self._find_unused_dependencies(installed_packages),
            "outdated_deps": self._find_outdated_dependencies(installed_packages),
            "security_vulnerabilities": self._check_security_vulnerabilities(installed_packages)
        }
        
        return analysis
    
    def _read_requirements(self) -> List[str]:
        """读取requirements.txt文件
        
        Returns:
            依赖包列表
        """
        if not self.requirements_file.exists():
            return []
            
        with open(self.requirements_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # 过滤注释和空行
        deps = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # 提取包名（去除版本号）
                pkg_name = line.split('==')[0].split('>=')[0].split('<=')[0].split('~=')[0]
                deps.append(pkg_name.strip())
                
        return deps
    
    def _read_pyproject_dependencies(self) -> List[str]:
        """读取pyproject.toml中的依赖
        
        Returns:
            依赖包列表
        """
        if not self.pyproject_file.exists():
            return []
            
        try:
            import tomli
        except ImportError:
            print("⚠️ 需要安装tomli包来解析pyproject.toml")
            return []
            
        with open(self.pyproject_file, 'rb') as f:
            data = tomli.load(f)
            
        deps = []
        if 'project' in data and 'dependencies' in data['project']:
            for dep in data['project']['dependencies']:
                pkg_name = dep.split('==')[0].split('>=')[0].split('<=')[0].split('~=')[0]
                deps.append(pkg_name.strip())
                
        return deps
    
    def _get_installed_packages(self) -> Dict[str, str]:
        """获取已安装的包列表
        
        Returns:
            包名到版本的映射
        """
        installed = {}
        for dist in pkg_resources.working_set:
            installed[dist.project_name.lower()] = dist.version
        return installed
    
    def _find_redundant_dependencies(self, req_deps: List[str], proj_deps: List[str]) -> List[str]:
        """查找冗余依赖
        
        Args:
            req_deps: requirements.txt中的依赖
            proj_deps: pyproject.toml中的依赖
            
        Returns:
            冗余依赖列表
        """
        req_set = set(dep.lower() for dep in req_deps)
        proj_set = set(dep.lower() for dep in proj_deps)
        
        # 在两个文件中都存在的依赖
        redundant = list(req_set.intersection(proj_set))
        return redundant
    
    def _find_unused_dependencies(self, installed: Dict[str, str]) -> List[str]:
        """查找未使用的依赖（简化版本）
        
        Args:
            installed: 已安装的包
            
        Returns:
            可能未使用的依赖列表
        """
        # 这里实现一个简化的未使用依赖检测
        # 实际项目中可以使用pipreqs或类似工具
        
        # 扫描Python文件中的import语句
        used_packages = set()
        for py_file in self.project_root.rglob('*.py'):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 简单的import检测
                import re
                imports = re.findall(r'^(?:from\s+(\w+)|import\s+(\w+))', content, re.MULTILINE)
                for imp in imports:
                    pkg = imp[0] or imp[1]
                    used_packages.add(pkg.lower())
                    
            except Exception:
                continue
                
        # 查找可能未使用的包
        unused = []
        for pkg in installed.keys():
            if pkg.lower() not in used_packages:
                # 排除一些常见的工具包
                if pkg.lower() not in ['pip', 'setuptools', 'wheel', 'pkg-resources']:
                    unused.append(pkg)
                    
        return unused
    
    def _find_outdated_dependencies(self, installed: Dict[str, str]) -> List[Dict]:
        """查找过时的依赖
        
        Args:
            installed: 已安装的包
            
        Returns:
            过时依赖信息列表
        """
        outdated = []
        
        for pkg_name, current_version in installed.items():
            try:
                # 查询PyPI获取最新版本
                response = requests.get(f"https://pypi.org/pypi/{pkg_name}/json", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    latest_version = data['info']['version']
                    
                    if current_version != latest_version:
                        outdated.append({
                            'package': pkg_name,
                            'current': current_version,
                            'latest': latest_version
                        })
                        
            except Exception:
                # 忽略网络错误或其他异常
                continue
                
        return outdated
    
    def _check_security_vulnerabilities(self, installed: Dict[str, str]) -> List[Dict]:
        """检查安全漏洞（使用safety数据库）
        
        Args:
            installed: 已安装的包
            
        Returns:
            安全漏洞信息列表
        """
        vulnerabilities = []
        
        try:
            # 运行safety check
            result = subprocess.run(
                ['safety', 'check', '--json'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # 没有发现漏洞
                return []
            else:
                # 解析safety输出
                try:
                    safety_data = json.loads(result.stdout)
                    for vuln in safety_data:
                        vulnerabilities.append({
                            'package': vuln.get('package'),
                            'version': vuln.get('installed_version'),
                            'vulnerability_id': vuln.get('vulnerability_id'),
                            'advisory': vuln.get('advisory'),
                            'cve': vuln.get('cve')
                        })
                except json.JSONDecodeError:
                    pass
                    
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("⚠️ 无法运行safety检查，请确保已安装safety包")
            
        return vulnerabilities
    
    def generate_report(self, analysis: Dict) -> str:
        """生成依赖审计报告
        
        Args:
            analysis: 分析结果
            
        Returns:
            报告内容
        """
        report = f"""
# 依赖审计报告

生成时间: {analysis['timestamp']}

## 概览
- 总依赖数量 (requirements.txt): {analysis['total_requirements']}
- 总依赖数量 (pyproject.toml): {analysis['total_pyproject_deps']}
- 已安装包数量: {analysis['total_installed']}

## 冗余依赖
{len(analysis['redundant_deps'])} 个包在多个配置文件中重复定义:
"""
        
        for dep in analysis['redundant_deps']:
            report += f"- {dep}\n"
            
        report += f"""

## 可能未使用的依赖
{len(analysis['unused_deps'])} 个包可能未被使用:
"""
        
        for dep in analysis['unused_deps'][:10]:  # 只显示前10个
            report += f"- {dep}\n"
            
        if len(analysis['unused_deps']) > 10:
            report += f"... 还有 {len(analysis['unused_deps']) - 10} 个\n"
            
        report += f"""

## 过时的依赖
{len(analysis['outdated_deps'])} 个包有更新版本:
"""
        
        for dep in analysis['outdated_deps'][:10]:  # 只显示前10个
            report += f"- {dep['package']}: {dep['current']} → {dep['latest']}\n"
            
        if len(analysis['outdated_deps']) > 10:
            report += f"... 还有 {len(analysis['outdated_deps']) - 10} 个\n"
            
        report += f"""

## 安全漏洞
{len(analysis['security_vulnerabilities'])} 个安全漏洞:
"""
        
        for vuln in analysis['security_vulnerabilities']:
            report += f"- {vuln['package']} {vuln['version']}: {vuln['advisory']}\n"
            
        return report
    
    def save_report(self, analysis: Dict, output_file: str = None):
        """保存审计报告
        
        Args:
            analysis: 分析结果
            output_file: 输出文件路径
        """
        if output_file is None:
            output_file = self.project_root / "dependency_audit_report.md"
            
        report = self.generate_report(analysis)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
            
        print(f"📊 审计报告已保存到: {output_file}")
        
        # 同时保存JSON格式的详细数据
        json_file = str(output_file).replace('.md', '.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
            
        print(f"📊 详细数据已保存到: {json_file}")

def main():
    """主函数"""
    project_root = Path.cwd()
    
    print("🚀 开始依赖审计...")
    auditor = DependencyAuditor(str(project_root))
    
    # 执行分析
    analysis = auditor.analyze_dependencies()
    
    # 生成并保存报告
    auditor.save_report(analysis)
    
    # 打印摘要
    print("\n📋 审计摘要:")
    print(f"- 冗余依赖: {len(analysis['redundant_deps'])} 个")
    print(f"- 可能未使用: {len(analysis['unused_deps'])} 个")
    print(f"- 过时依赖: {len(analysis['outdated_deps'])} 个")
    print(f"- 安全漏洞: {len(analysis['security_vulnerabilities'])} 个")
    
if __name__ == "__main__":
    main()