# -*- coding: utf-8 -*-
"""
依赖管理器
实现智能的依赖解析、冲突检测、版本管理和安全扫描
"""

import os
import json
import hashlib
import subprocess
import threading
import time
import requests
from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from pathlib import Path
from packaging import version
from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
import logging
from enum import Enum
import tempfile
import shutil
from contextlib import contextmanager

# 配置日志
logger = logging.getLogger(__name__)

class DependencyType(Enum):
    """依赖类型"""
    PYTHON = "python"
    NODE = "node"
    GO = "go"
    SYSTEM = "system"

class SecurityLevel(Enum):
    """安全级别"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class Vulnerability:
    """漏洞信息"""
    id: str
    package: str
    version: str
    severity: SecurityLevel
    description: str
    fixed_version: Optional[str] = None
    cve_id: Optional[str] = None
    published_date: Optional[str] = None
    references: List[str] = field(default_factory=list)

@dataclass
class DependencyInfo:
    """依赖信息"""
    name: str
    version: str
    dep_type: DependencyType
    required_by: Set[str] = field(default_factory=set)
    dependencies: Set[str] = field(default_factory=set)
    is_dev: bool = False
    is_optional: bool = False
    license: Optional[str] = None
    description: Optional[str] = None
    homepage: Optional[str] = None
    vulnerabilities: List[Vulnerability] = field(default_factory=list)
    last_updated: Optional[str] = None
    size: Optional[int] = None

@dataclass
class ConflictInfo:
    """冲突信息"""
    package: str
    conflicting_versions: List[str]
    required_by: List[str]
    resolution_suggestion: Optional[str] = None
    severity: str = "medium"

class DependencyResolver:
    """依赖解析器"""
    
    def __init__(self):
        self.dependency_graph: Dict[str, DependencyInfo] = {}
        self.conflicts: List[ConflictInfo] = []
        self.lock = threading.Lock()
    
    def parse_requirements_file(self, file_path: Path, dep_type: DependencyType) -> List[DependencyInfo]:
        """解析依赖文件"""
        dependencies = []
        
        try:
            if dep_type == DependencyType.PYTHON:
                dependencies = self._parse_python_requirements(file_path)
            elif dep_type == DependencyType.NODE:
                dependencies = self._parse_package_json(file_path)
            elif dep_type == DependencyType.GO:
                dependencies = self._parse_go_mod(file_path)
            
            logger.info(f"解析 {file_path} 发现 {len(dependencies)} 个依赖")
            
        except Exception as e:
            logger.error(f"解析依赖文件 {file_path} 失败: {e}")
        
        return dependencies
    
    def _parse_python_requirements(self, file_path: Path) -> List[DependencyInfo]:
        """解析 Python requirements.txt"""
        dependencies = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                try:
                    req = Requirement(line)
                    dep_info = DependencyInfo(
                        name=req.name,
                        version=str(req.specifier) if req.specifier else "*",
                        dep_type=DependencyType.PYTHON
                    )
                    dependencies.append(dep_info)
                    
                except Exception as e:
                    logger.warning(f"解析第 {line_num} 行失败: {line} - {e}")
        
        return dependencies
    
    def _parse_package_json(self, file_path: Path) -> List[DependencyInfo]:
        """解析 Node.js package.json"""
        dependencies = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 生产依赖
        for name, version_spec in data.get('dependencies', {}).items():
            dep_info = DependencyInfo(
                name=name,
                version=version_spec,
                dep_type=DependencyType.NODE,
                is_dev=False
            )
            dependencies.append(dep_info)
        
        # 开发依赖
        for name, version_spec in data.get('devDependencies', {}).items():
            dep_info = DependencyInfo(
                name=name,
                version=version_spec,
                dep_type=DependencyType.NODE,
                is_dev=True
            )
            dependencies.append(dep_info)
        
        return dependencies
    
    def _parse_go_mod(self, file_path: Path) -> List[DependencyInfo]:
        """解析 Go go.mod"""
        dependencies = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 简单解析 go.mod（实际应该使用更复杂的解析器）
        lines = content.split('\n')
        in_require_block = False
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('require ('):
                in_require_block = True
                continue
            elif line == ')':
                in_require_block = False
                continue
            
            if in_require_block or line.startswith('require '):
                # 移除 require 前缀
                if line.startswith('require '):
                    line = line[8:]
                
                parts = line.split()
                if len(parts) >= 2:
                    name = parts[0]
                    version = parts[1]
                    
                    dep_info = DependencyInfo(
                        name=name,
                        version=version,
                        dep_type=DependencyType.GO
                    )
                    dependencies.append(dep_info)
        
        return dependencies
    
    def detect_conflicts(self, dependencies: List[DependencyInfo]) -> List[ConflictInfo]:
        """检测依赖冲突"""
        conflicts = []
        package_versions = {}
        
        # 收集所有包的版本要求
        for dep in dependencies:
            if dep.name not in package_versions:
                package_versions[dep.name] = []
            package_versions[dep.name].append(dep)
        
        # 检测冲突
        for package_name, deps in package_versions.items():
            if len(deps) > 1:
                versions = [dep.version for dep in deps]
                required_by = [f"{dep.name} ({dep.version})" for dep in deps]
                
                # 检查版本是否兼容
                if not self._are_versions_compatible(versions, deps[0].dep_type):
                    conflict = ConflictInfo(
                        package=package_name,
                        conflicting_versions=versions,
                        required_by=required_by,
                        resolution_suggestion=self._suggest_resolution(package_name, versions, deps[0].dep_type)
                    )
                    conflicts.append(conflict)
        
        return conflicts
    
    def _are_versions_compatible(self, versions: List[str], dep_type: DependencyType) -> bool:
        """检查版本是否兼容"""
        if dep_type == DependencyType.PYTHON:
            try:
                # 尝试找到满足所有版本要求的版本
                combined_spec = SpecifierSet()
                for version_spec in versions:
                    if version_spec != "*":
                        combined_spec &= SpecifierSet(version_spec)
                return True  # 如果没有异常，说明可以合并
            except Exception:
                return False
        
        # 对于其他类型，简单检查是否完全相同
        return len(set(versions)) == 1
    
    def _suggest_resolution(self, package_name: str, versions: List[str], dep_type: DependencyType) -> str:
        """建议解决方案"""
        if dep_type == DependencyType.PYTHON:
            # 尝试找到最宽松的版本要求
            try:
                # 找到最高的最小版本
                min_versions = []
                for version_spec in versions:
                    if version_spec != "*" and ">" in version_spec:
                        # 提取最小版本
                        spec = SpecifierSet(version_spec)
                        for spec_item in spec:
                            if spec_item.operator in (">=", ">"):
                                min_versions.append(version.parse(spec_item.version))
                
                if min_versions:
                    suggested_version = max(min_versions)
                    return f"建议使用版本 >={suggested_version}"
            except Exception:
                pass
        
        return f"建议手动解决 {package_name} 的版本冲突"
    
    def build_dependency_graph(self, dependencies: List[DependencyInfo]) -> Dict[str, DependencyInfo]:
        """构建依赖图"""
        graph = {}
        
        for dep in dependencies:
            graph[dep.name] = dep
        
        # 解析传递依赖（这里简化处理）
        for dep in dependencies:
            self._resolve_transitive_dependencies(dep, graph)
        
        return graph
    
    def _resolve_transitive_dependencies(self, dep: DependencyInfo, graph: Dict[str, DependencyInfo]):
        """解析传递依赖"""
        # 这里应该实现实际的传递依赖解析
        # 由于复杂性，这里只是一个占位符
        pass

class SecurityScanner:
    """安全扫描器"""
    
    def __init__(self):
        self.vulnerability_db = {}
        self.last_update = None
        self.cache_dir = Path.home() / ".chatexcel" / "security_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def scan_dependencies(self, dependencies: List[DependencyInfo]) -> List[Vulnerability]:
        """扫描依赖漏洞"""
        vulnerabilities = []
        
        # 更新漏洞数据库
        self._update_vulnerability_db()
        
        for dep in dependencies:
            dep_vulns = self._check_package_vulnerabilities(dep)
            vulnerabilities.extend(dep_vulns)
            dep.vulnerabilities = dep_vulns
        
        return vulnerabilities
    
    def _update_vulnerability_db(self):
        """更新漏洞数据库"""
        try:
            # 检查是否需要更新（每天更新一次）
            cache_file = self.cache_dir / "vulnerability_db.json"
            
            if cache_file.exists():
                stat = cache_file.stat()
                if time.time() - stat.st_mtime < 24 * 3600:  # 24小时内不重复更新
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        self.vulnerability_db = json.load(f)
                    return
            
            # 从多个源获取漏洞数据
            self._fetch_python_vulnerabilities()
            self._fetch_node_vulnerabilities()
            
            # 保存到缓存
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.vulnerability_db, f, indent=2)
            
            self.last_update = time.time()
            logger.info("漏洞数据库更新完成")
            
        except Exception as e:
            logger.error(f"更新漏洞数据库失败: {e}")
    
    def _fetch_python_vulnerabilities(self):
        """获取 Python 包漏洞信息"""
        try:
            # 使用 PyUp.io 的安全数据库（示例）
            # 实际应该使用官方的安全数据源
            url = "https://pyup.io/api/v1/vulnerabilities/"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                for vuln in data.get('results', []):
                    package_name = vuln.get('package')
                    if package_name:
                        if package_name not in self.vulnerability_db:
                            self.vulnerability_db[package_name] = []
                        
                        vulnerability = {
                            'id': vuln.get('id'),
                            'severity': vuln.get('severity', 'medium'),
                            'description': vuln.get('advisory'),
                            'affected_versions': vuln.get('specs', []),
                            'fixed_version': vuln.get('fixed_in'),
                            'cve_id': vuln.get('cve')
                        }
                        self.vulnerability_db[package_name].append(vulnerability)
        
        except Exception as e:
            logger.warning(f"获取 Python 漏洞信息失败: {e}")
    
    def _fetch_node_vulnerabilities(self):
        """获取 Node.js 包漏洞信息"""
        try:
            # 使用 npm audit 的数据源（示例）
            # 实际应该使用 GitHub Advisory Database 等
            pass
        except Exception as e:
            logger.warning(f"获取 Node.js 漏洞信息失败: {e}")
    
    def _check_package_vulnerabilities(self, dep: DependencyInfo) -> List[Vulnerability]:
        """检查包的漏洞"""
        vulnerabilities = []
        
        package_vulns = self.vulnerability_db.get(dep.name, [])
        
        for vuln_data in package_vulns:
            # 检查版本是否受影响
            if self._is_version_affected(dep.version, vuln_data.get('affected_versions', [])):
                vulnerability = Vulnerability(
                    id=vuln_data.get('id', ''),
                    package=dep.name,
                    version=dep.version,
                    severity=SecurityLevel(vuln_data.get('severity', 'medium')),
                    description=vuln_data.get('description', ''),
                    fixed_version=vuln_data.get('fixed_version'),
                    cve_id=vuln_data.get('cve_id')
                )
                vulnerabilities.append(vulnerability)
        
        return vulnerabilities
    
    def _is_version_affected(self, package_version: str, affected_versions: List[str]) -> bool:
        """检查版本是否受影响"""
        try:
            pkg_version = version.parse(package_version)
            
            for affected_spec in affected_versions:
                spec = SpecifierSet(affected_spec)
                if pkg_version in spec:
                    return True
            
            return False
        except Exception:
            # 如果版本解析失败，保守地认为受影响
            return True

class DependencyManager:
    """依赖管理器主类"""
    
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.resolver = DependencyResolver()
        self.scanner = SecurityScanner()
        self.lock_file = self.project_root / "dependency_lock.json"
        self.config_file = self.project_root / "dependency_config.json"
        
        # 加载配置
        self.config = self._load_config()
        
        # 依赖信息
        self.dependencies: Dict[str, DependencyInfo] = {}
        self.conflicts: List[ConflictInfo] = []
        self.vulnerabilities: List[Vulnerability] = []
        
        # 锁
        self.lock = threading.Lock()
    
    def analyze_project(self) -> Dict[str, Any]:
        """分析项目依赖"""
        with self.lock:
            logger.info("开始分析项目依赖")
            
            # 查找依赖文件
            dependency_files = self._find_dependency_files()
            
            all_dependencies = []
            
            # 解析所有依赖文件
            for file_path, dep_type in dependency_files:
                deps = self.resolver.parse_requirements_file(file_path, dep_type)
                all_dependencies.extend(deps)
            
            # 构建依赖图
            self.dependencies = self.resolver.build_dependency_graph(all_dependencies)
            
            # 检测冲突
            self.conflicts = self.resolver.detect_conflicts(all_dependencies)
            
            # 安全扫描
            self.vulnerabilities = self.scanner.scan_dependencies(all_dependencies)
            
            # 生成报告
            report = self._generate_analysis_report()
            
            # 保存锁文件
            self._save_lock_file()
            
            logger.info("项目依赖分析完成")
            return report
    
    def _find_dependency_files(self) -> List[Tuple[Path, DependencyType]]:
        """查找依赖文件"""
        dependency_files = []
        
        # Python
        for pattern in ['requirements.txt', 'requirements/*.txt', 'Pipfile', 'pyproject.toml']:
            for file_path in self.project_root.glob(pattern):
                if file_path.is_file():
                    dependency_files.append((file_path, DependencyType.PYTHON))
        
        # Node.js
        package_json = self.project_root / 'package.json'
        if package_json.exists():
            dependency_files.append((package_json, DependencyType.NODE))
        
        # Go
        go_mod = self.project_root / 'go.mod'
        if go_mod.exists():
            dependency_files.append((go_mod, DependencyType.GO))
        
        return dependency_files
    
    def _generate_analysis_report(self) -> Dict[str, Any]:
        """生成分析报告"""
        # 统计信息
        total_deps = len(self.dependencies)
        dev_deps = sum(1 for dep in self.dependencies.values() if dep.is_dev)
        prod_deps = total_deps - dev_deps
        
        # 漏洞统计
        vuln_stats = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'info': 0
        }
        
        for vuln in self.vulnerabilities:
            vuln_stats[vuln.severity.value] += 1
        
        # 依赖类型统计
        type_stats = {}
        for dep in self.dependencies.values():
            dep_type = dep.dep_type.value
            type_stats[dep_type] = type_stats.get(dep_type, 0) + 1
        
        return {
            'summary': {
                'total_dependencies': total_deps,
                'production_dependencies': prod_deps,
                'development_dependencies': dev_deps,
                'conflicts': len(self.conflicts),
                'vulnerabilities': len(self.vulnerabilities)
            },
            'dependency_types': type_stats,
            'vulnerability_summary': vuln_stats,
            'conflicts': [
                {
                    'package': conflict.package,
                    'versions': conflict.conflicting_versions,
                    'required_by': conflict.required_by,
                    'suggestion': conflict.resolution_suggestion,
                    'severity': conflict.severity
                }
                for conflict in self.conflicts
            ],
            'vulnerabilities': [
                {
                    'id': vuln.id,
                    'package': vuln.package,
                    'version': vuln.version,
                    'severity': vuln.severity.value,
                    'description': vuln.description,
                    'fixed_version': vuln.fixed_version,
                    'cve_id': vuln.cve_id
                }
                for vuln in self.vulnerabilities
            ],
            'recommendations': self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 冲突建议
        if self.conflicts:
            recommendations.append(f"发现 {len(self.conflicts)} 个依赖冲突，建议解决后再部署")
        
        # 安全建议
        critical_vulns = [v for v in self.vulnerabilities if v.severity == SecurityLevel.CRITICAL]
        if critical_vulns:
            recommendations.append(f"发现 {len(critical_vulns)} 个严重安全漏洞，强烈建议立即更新")
        
        high_vulns = [v for v in self.vulnerabilities if v.severity == SecurityLevel.HIGH]
        if high_vulns:
            recommendations.append(f"发现 {len(high_vulns)} 个高危安全漏洞，建议尽快更新")
        
        # 版本建议
        outdated_count = 0
        for dep in self.dependencies.values():
            if self._is_dependency_outdated(dep):
                outdated_count += 1
        
        if outdated_count > 0:
            recommendations.append(f"发现 {outdated_count} 个过时的依赖，建议更新到最新版本")
        
        # 许可证建议
        unlicensed_count = sum(1 for dep in self.dependencies.values() if not dep.license)
        if unlicensed_count > 0:
            recommendations.append(f"有 {unlicensed_count} 个依赖缺少许可证信息，建议检查")
        
        return recommendations
    
    def _is_dependency_outdated(self, dep: DependencyInfo) -> bool:
        """检查依赖是否过时"""
        # 这里应该实现实际的版本检查逻辑
        # 简化处理，返回 False
        return False
    
    def update_dependencies(self, packages: Optional[List[str]] = None) -> Dict[str, Any]:
        """更新依赖"""
        with self.lock:
            logger.info("开始更新依赖")
            
            results = {
                'updated': [],
                'failed': [],
                'conflicts': [],
                'security_fixes': []
            }
            
            if packages:
                # 更新指定包
                for package in packages:
                    result = self._update_single_package(package)
                    if result['success']:
                        results['updated'].append(result)
                    else:
                        results['failed'].append(result)
            else:
                # 更新所有包
                for dep_name in self.dependencies:
                    result = self._update_single_package(dep_name)
                    if result['success']:
                        results['updated'].append(result)
                    else:
                        results['failed'].append(result)
            
            # 重新分析
            self.analyze_project()
            
            logger.info(f"依赖更新完成: 成功 {len(results['updated'])}, 失败 {len(results['failed'])}")
            return results
    
    def _update_single_package(self, package_name: str) -> Dict[str, Any]:
        """更新单个包"""
        try:
            dep = self.dependencies.get(package_name)
            if not dep:
                return {
                    'package': package_name,
                    'success': False,
                    'error': '包不存在'
                }
            
            # 根据依赖类型执行更新
            if dep.dep_type == DependencyType.PYTHON:
                return self._update_python_package(package_name)
            elif dep.dep_type == DependencyType.NODE:
                return self._update_node_package(package_name)
            elif dep.dep_type == DependencyType.GO:
                return self._update_go_package(package_name)
            else:
                return {
                    'package': package_name,
                    'success': False,
                    'error': '不支持的依赖类型'
                }
        
        except Exception as e:
            return {
                'package': package_name,
                'success': False,
                'error': str(e)
            }
    
    def _update_python_package(self, package_name: str) -> Dict[str, Any]:
        """更新 Python 包"""
        try:
            # 使用 pip 更新
            result = subprocess.run(
                ['pip', 'install', '--upgrade', package_name],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                return {
                    'package': package_name,
                    'success': True,
                    'output': result.stdout
                }
            else:
                return {
                    'package': package_name,
                    'success': False,
                    'error': result.stderr
                }
        
        except Exception as e:
            return {
                'package': package_name,
                'success': False,
                'error': str(e)
            }
    
    def _update_node_package(self, package_name: str) -> Dict[str, Any]:
        """更新 Node.js 包"""
        try:
            # 使用 npm 更新
            result = subprocess.run(
                ['npm', 'update', package_name],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                return {
                    'package': package_name,
                    'success': True,
                    'output': result.stdout
                }
            else:
                return {
                    'package': package_name,
                    'success': False,
                    'error': result.stderr
                }
        
        except Exception as e:
            return {
                'package': package_name,
                'success': False,
                'error': str(e)
            }
    
    def _update_go_package(self, package_name: str) -> Dict[str, Any]:
        """更新 Go 包"""
        try:
            # 使用 go get 更新
            result = subprocess.run(
                ['go', 'get', '-u', package_name],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                return {
                    'package': package_name,
                    'success': True,
                    'output': result.stdout
                }
            else:
                return {
                    'package': package_name,
                    'success': False,
                    'error': result.stderr
                }
        
        except Exception as e:
            return {
                'package': package_name,
                'success': False,
                'error': str(e)
            }
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置"""
        default_config = {
            'auto_update': False,
            'security_scan': True,
            'conflict_resolution': 'manual',
            'update_schedule': 'weekly',
            'excluded_packages': [],
            'security_level_threshold': 'medium'
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    default_config.update(config)
            except Exception as e:
                logger.error(f"加载配置文件失败: {e}")
        
        return default_config
    
    def _save_lock_file(self):
        """保存锁文件"""
        try:
            lock_data = {
                'generated_at': time.time(),
                'dependencies': {
                    name: {
                        'version': dep.version,
                        'type': dep.dep_type.value,
                        'is_dev': dep.is_dev,
                        'license': dep.license,
                        'vulnerabilities': len(dep.vulnerabilities)
                    }
                    for name, dep in self.dependencies.items()
                },
                'conflicts': [
                    {
                        'package': conflict.package,
                        'versions': conflict.conflicting_versions,
                        'severity': conflict.severity
                    }
                    for conflict in self.conflicts
                ],
                'security_summary': {
                    'total_vulnerabilities': len(self.vulnerabilities),
                    'critical': len([v for v in self.vulnerabilities if v.severity == SecurityLevel.CRITICAL]),
                    'high': len([v for v in self.vulnerabilities if v.severity == SecurityLevel.HIGH])
                }
            }
            
            with open(self.lock_file, 'w', encoding='utf-8') as f:
                json.dump(lock_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"锁文件已保存: {self.lock_file}")
            
        except Exception as e:
            logger.error(f"保存锁文件失败: {e}")
    
    def get_dependency_info(self, package_name: str) -> Optional[Dict[str, Any]]:
        """获取依赖信息"""
        dep = self.dependencies.get(package_name)
        if not dep:
            return None
        
        return {
            'name': dep.name,
            'version': dep.version,
            'type': dep.dep_type.value,
            'is_dev': dep.is_dev,
            'is_optional': dep.is_optional,
            'license': dep.license,
            'description': dep.description,
            'homepage': dep.homepage,
            'vulnerabilities': [
                {
                    'id': vuln.id,
                    'severity': vuln.severity.value,
                    'description': vuln.description,
                    'fixed_version': vuln.fixed_version
                }
                for vuln in dep.vulnerabilities
            ],
            'required_by': list(dep.required_by),
            'dependencies': list(dep.dependencies)
        }
    
    def generate_report(self, output_file: Optional[Path] = None) -> str:
        """生成详细报告"""
        report = self._generate_analysis_report()
        
        # 生成 Markdown 报告
        markdown_content = self._format_report_as_markdown(report)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            logger.info(f"报告已保存: {output_file}")
        
        return markdown_content
    
    def _format_report_as_markdown(self, report: Dict[str, Any]) -> str:
        """格式化报告为 Markdown"""
        lines = [
            "# 依赖分析报告",
            "",
            f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 概览",
            "",
            f"- 总依赖数: {report['summary']['total_dependencies']}",
            f"- 生产依赖: {report['summary']['production_dependencies']}",
            f"- 开发依赖: {report['summary']['development_dependencies']}",
            f"- 冲突数: {report['summary']['conflicts']}",
            f"- 漏洞数: {report['summary']['vulnerabilities']}",
            ""
        ]
        
        # 依赖类型统计
        if report['dependency_types']:
            lines.extend([
                "## 依赖类型分布",
                ""
            ])
            for dep_type, count in report['dependency_types'].items():
                lines.append(f"- {dep_type}: {count}")
            lines.append("")
        
        # 安全漏洞
        if report['vulnerabilities']:
            lines.extend([
                "## 安全漏洞",
                "",
                "| 包名 | 版本 | 严重程度 | 描述 | 修复版本 |",
                "|------|------|----------|------|----------|"
            ])
            
            for vuln in report['vulnerabilities']:
                lines.append(
                    f"| {vuln['package']} | {vuln['version']} | {vuln['severity']} | "
                    f"{vuln['description'][:50]}... | {vuln['fixed_version'] or 'N/A'} |"
                )
            lines.append("")
        
        # 依赖冲突
        if report['conflicts']:
            lines.extend([
                "## 依赖冲突",
                ""
            ])
            
            for conflict in report['conflicts']:
                lines.extend([
                    f"### {conflict['package']}",
                    "",
                    f"- 冲突版本: {', '.join(conflict['versions'])}",
                    f"- 需要方: {', '.join(conflict['required_by'])}",
                    f"- 建议: {conflict['suggestion']}",
                    ""
                ])
        
        # 改进建议
        if report['recommendations']:
            lines.extend([
                "## 改进建议",
                ""
            ])
            
            for i, rec in enumerate(report['recommendations'], 1):
                lines.append(f"{i}. {rec}")
            lines.append("")
        
        return "\n".join(lines)

# 便捷函数
def analyze_project_dependencies(project_root: str) -> Dict[str, Any]:
    """分析项目依赖的便捷函数"""
    manager = DependencyManager(Path(project_root))
    return manager.analyze_project()

if __name__ == "__main__":
    # 测试代码
    import sys
    
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = "."
    
    # 创建依赖管理器
    manager = DependencyManager(Path(project_path))
    
    # 分析项目
    report = manager.analyze_project()
    
    # 生成报告
    report_content = manager.generate_report()
    print(report_content)
    
    # 保存报告
    report_file = Path(project_path) / "dependency_report.md"
    manager.generate_report(report_file)
    
    print(f"\n详细报告已保存到: {report_file}")