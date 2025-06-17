#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置优化器
统一管理和优化项目的各种配置文件
"""

import json
import toml
import yaml
import configparser
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import shutil
import re

class ConfigOptimizer:
    """配置优化器主类"""
    
    def __init__(self, project_root: str):
        """初始化配置优化器
        
        Args:
            project_root: 项目根目录
        """
        self.project_root = Path(project_root)
        self.backup_dir = self.project_root / "config_backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # 配置文件模式
        self.config_patterns = {
            'python': {
                'pyproject.toml': 'toml',
                'setup.py': 'python',
                'setup.cfg': 'ini',
                'requirements.txt': 'text',
                'requirements-dev.txt': 'text',
                'Pipfile': 'toml',
                'poetry.lock': 'toml',
                'uv.lock': 'toml'
            },
            'javascript': {
                'package.json': 'json',
                'package-lock.json': 'json',
                'yarn.lock': 'text',
                'tsconfig.json': 'json',
                '.eslintrc.json': 'json',
                '.prettierrc': 'json'
            },
            'docker': {
                'Dockerfile': 'text',
                'docker-compose.yml': 'yaml',
                'docker-compose.yaml': 'yaml',
                '.dockerignore': 'text'
            },
            'ci_cd': {
                '.github/workflows/*.yml': 'yaml',
                '.github/workflows/*.yaml': 'yaml',
                '.gitlab-ci.yml': 'yaml',
                'Jenkinsfile': 'text'
            },
            'editor': {
                '.vscode/settings.json': 'json',
                '.vscode/launch.json': 'json',
                '.editorconfig': 'ini'
            },
            'git': {
                '.gitignore': 'text',
                '.gitattributes': 'text'
            },
            'other': {
                'Makefile': 'text',
                'README.md': 'text',
                'LICENSE': 'text'
            }
        }
        
        # 优化规则
        self.optimization_rules = {
            'pyproject.toml': self._optimize_pyproject_toml,
            'requirements.txt': self._optimize_requirements_txt,
            'package.json': self._optimize_package_json,
            '.gitignore': self._optimize_gitignore,
            'docker-compose.yml': self._optimize_docker_compose
        }
        
    def scan_config_files(self) -> Dict[str, List[Path]]:
        """扫描项目中的配置文件
        
        Returns:
            按类别分组的配置文件列表
        """
        found_configs = {}
        
        for category, patterns in self.config_patterns.items():
            found_configs[category] = []
            
            for pattern, file_type in patterns.items():
                if '*' in pattern:
                    # 通配符模式
                    for file_path in self.project_root.rglob(pattern):
                        if file_path.is_file():
                            found_configs[category].append(file_path)
                else:
                    # 精确匹配
                    file_path = self.project_root / pattern
                    if file_path.exists() and file_path.is_file():
                        found_configs[category].append(file_path)
                        
        return found_configs
        
    def analyze_config_file(self, file_path: Path) -> Dict[str, Any]:
        """分析单个配置文件
        
        Args:
            file_path: 配置文件路径
            
        Returns:
            分析结果
        """
        analysis = {
            'file_path': str(file_path),
            'file_name': file_path.name,
            'file_size': file_path.stat().st_size,
            'last_modified': datetime.fromtimestamp(file_path.stat().st_mtime),
            'file_type': self._detect_file_type(file_path),
            'issues': [],
            'suggestions': [],
            'content_summary': {}
        }
        
        try:
            # 读取文件内容
            content = file_path.read_text(encoding='utf-8')
            analysis['line_count'] = len(content.splitlines())
            analysis['char_count'] = len(content)
            
            # 根据文件类型进行特定分析
            if file_path.name == 'pyproject.toml':
                analysis.update(self._analyze_pyproject_toml(file_path, content))
            elif file_path.name == 'requirements.txt':
                analysis.update(self._analyze_requirements_txt(file_path, content))
            elif file_path.name == 'package.json':
                analysis.update(self._analyze_package_json(file_path, content))
            elif file_path.name == '.gitignore':
                analysis.update(self._analyze_gitignore(file_path, content))
            elif file_path.name in ['docker-compose.yml', 'docker-compose.yaml']:
                analysis.update(self._analyze_docker_compose(file_path, content))
                
        except Exception as e:
            analysis['issues'].append(f"读取文件失败: {e}")
            
        return analysis
        
    def _detect_file_type(self, file_path: Path) -> str:
        """检测文件类型"""
        name = file_path.name.lower()
        suffix = file_path.suffix.lower()
        
        if suffix in ['.json']:
            return 'json'
        elif suffix in ['.toml']:
            return 'toml'
        elif suffix in ['.yml', '.yaml']:
            return 'yaml'
        elif suffix in ['.ini', '.cfg']:
            return 'ini'
        elif suffix in ['.py']:
            return 'python'
        elif suffix in ['.md']:
            return 'markdown'
        elif name in ['dockerfile', '.dockerignore', '.gitignore', '.gitattributes']:
            return 'text'
        else:
            return 'unknown'
            
    def _analyze_pyproject_toml(self, file_path: Path, content: str) -> Dict[str, Any]:
        """分析 pyproject.toml 文件"""
        analysis = {'content_summary': {}, 'issues': [], 'suggestions': []}
        
        try:
            data = toml.loads(content)
            
            # 基本信息
            if 'project' in data:
                project = data['project']
                analysis['content_summary']['project_name'] = project.get('name', 'Unknown')
                analysis['content_summary']['version'] = project.get('version', 'Unknown')
                analysis['content_summary']['python_requires'] = project.get('requires-python', 'Unknown')
                
                # 依赖分析
                dependencies = project.get('dependencies', [])
                analysis['content_summary']['dependency_count'] = len(dependencies)
                
                optional_deps = project.get('optional-dependencies', {})
                analysis['content_summary']['optional_dependency_groups'] = len(optional_deps)
                
                # 检查常见问题
                if not project.get('description'):
                    analysis['issues'].append("缺少项目描述")
                    
                if not project.get('authors'):
                    analysis['issues'].append("缺少作者信息")
                    
                if not project.get('license'):
                    analysis['suggestions'].append("建议添加许可证信息")
                    
            # 构建系统分析
            if 'build-system' in data:
                build_system = data['build-system']
                analysis['content_summary']['build_backend'] = build_system.get('build-backend', 'Unknown')
                
            # 工具配置分析
            tool_configs = []
            for key in data.keys():
                if key.startswith('tool.'):
                    tool_configs.append(key[5:])  # 移除 'tool.' 前缀
                    
            analysis['content_summary']['configured_tools'] = tool_configs
            
            # 检查重复依赖
            all_deps = set()
            for dep in dependencies:
                dep_name = dep.split('[')[0].split('>=')[0].split('==')[0].split('~=')[0].strip()
                if dep_name in all_deps:
                    analysis['issues'].append(f"重复依赖: {dep_name}")
                all_deps.add(dep_name)
                
        except Exception as e:
            analysis['issues'].append(f"解析 TOML 失败: {e}")
            
        return analysis
        
    def _analyze_requirements_txt(self, file_path: Path, content: str) -> Dict[str, Any]:
        """分析 requirements.txt 文件"""
        analysis = {'content_summary': {}, 'issues': [], 'suggestions': []}
        
        lines = content.splitlines()
        dependencies = []
        comments = 0
        empty_lines = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                empty_lines += 1
            elif line.startswith('#'):
                comments += 1
            elif line.startswith('-'):
                # pip 选项
                if line.startswith('-r'):
                    analysis['suggestions'].append(f"引用其他文件: {line}")
            else:
                dependencies.append(line)
                
        analysis['content_summary']['dependency_count'] = len(dependencies)
        analysis['content_summary']['comment_lines'] = comments
        analysis['content_summary']['empty_lines'] = empty_lines
        
        # 检查版本固定
        pinned_versions = 0
        range_versions = 0
        no_versions = 0
        
        for dep in dependencies:
            if '==' in dep:
                pinned_versions += 1
            elif any(op in dep for op in ['>=', '<=', '>', '<', '~=', '!=']):
                range_versions += 1
            else:
                no_versions += 1
                
        analysis['content_summary']['pinned_versions'] = pinned_versions
        analysis['content_summary']['range_versions'] = range_versions
        analysis['content_summary']['no_versions'] = no_versions
        
        if no_versions > 0:
            analysis['issues'].append(f"{no_versions} 个依赖没有指定版本")
            
        # 检查重复依赖
        dep_names = set()
        for dep in dependencies:
            name = dep.split('[')[0].split('>=')[0].split('==')[0].split('~=')[0].strip()
            if name in dep_names:
                analysis['issues'].append(f"重复依赖: {name}")
            dep_names.add(name)
            
        return analysis
        
    def _analyze_package_json(self, file_path: Path, content: str) -> Dict[str, Any]:
        """分析 package.json 文件"""
        analysis = {'content_summary': {}, 'issues': [], 'suggestions': []}
        
        try:
            data = json.loads(content)
            
            # 基本信息
            analysis['content_summary']['name'] = data.get('name', 'Unknown')
            analysis['content_summary']['version'] = data.get('version', 'Unknown')
            analysis['content_summary']['description'] = data.get('description', '')
            
            # 依赖分析
            deps = data.get('dependencies', {})
            dev_deps = data.get('devDependencies', {})
            peer_deps = data.get('peerDependencies', {})
            
            analysis['content_summary']['dependency_count'] = len(deps)
            analysis['content_summary']['dev_dependency_count'] = len(dev_deps)
            analysis['content_summary']['peer_dependency_count'] = len(peer_deps)
            
            # 脚本分析
            scripts = data.get('scripts', {})
            analysis['content_summary']['script_count'] = len(scripts)
            
            # 检查常见问题
            if not data.get('description'):
                analysis['issues'].append("缺少项目描述")
                
            if not data.get('author'):
                analysis['issues'].append("缺少作者信息")
                
            if not data.get('license'):
                analysis['suggestions'].append("建议添加许可证信息")
                
            # 检查重复依赖
            all_deps = set(deps.keys()) | set(dev_deps.keys()) | set(peer_deps.keys())
            if len(all_deps) < len(deps) + len(dev_deps) + len(peer_deps):
                analysis['issues'].append("存在重复依赖")
                
        except Exception as e:
            analysis['issues'].append(f"解析 JSON 失败: {e}")
            
        return analysis
        
    def _analyze_gitignore(self, file_path: Path, content: str) -> Dict[str, Any]:
        """分析 .gitignore 文件"""
        analysis = {'content_summary': {}, 'issues': [], 'suggestions': []}
        
        lines = content.splitlines()
        patterns = []
        comments = 0
        empty_lines = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                empty_lines += 1
            elif line.startswith('#'):
                comments += 1
            else:
                patterns.append(line)
                
        analysis['content_summary']['pattern_count'] = len(patterns)
        analysis['content_summary']['comment_lines'] = comments
        analysis['content_summary']['empty_lines'] = empty_lines
        
        # 检查常见模式
        common_patterns = {
            '__pycache__/': 'Python 缓存',
            '*.pyc': 'Python 字节码',
            '.env': '环境变量',
            'node_modules/': 'Node.js 模块',
            '.DS_Store': 'macOS 系统文件',
            '*.log': '日志文件',
            '.vscode/': 'VS Code 配置',
            '.idea/': 'IntelliJ IDEA 配置'
        }
        
        missing_patterns = []
        for pattern, description in common_patterns.items():
            if not any(p.strip() == pattern for p in patterns):
                missing_patterns.append(f"{pattern} ({description})")
                
        if missing_patterns:
            analysis['suggestions'].append(f"建议添加常见忽略模式: {', '.join(missing_patterns)}")
            
        # 检查重复模式
        unique_patterns = set(patterns)
        if len(unique_patterns) < len(patterns):
            analysis['issues'].append("存在重复的忽略模式")
            
        return analysis
        
    def _analyze_docker_compose(self, file_path: Path, content: str) -> Dict[str, Any]:
        """分析 docker-compose.yml 文件"""
        analysis = {'content_summary': {}, 'issues': [], 'suggestions': []}
        
        try:
            data = yaml.safe_load(content)
            
            # 基本信息
            version = data.get('version', 'Unknown')
            analysis['content_summary']['compose_version'] = version
            
            # 服务分析
            services = data.get('services', {})
            analysis['content_summary']['service_count'] = len(services)
            
            service_info = []
            for service_name, service_config in services.items():
                info = {'name': service_name}
                
                if 'image' in service_config:
                    info['image'] = service_config['image']
                elif 'build' in service_config:
                    info['build'] = True
                    
                if 'ports' in service_config:
                    info['ports'] = len(service_config['ports'])
                    
                if 'volumes' in service_config:
                    info['volumes'] = len(service_config['volumes'])
                    
                service_info.append(info)
                
            analysis['content_summary']['services'] = service_info
            
            # 网络分析
            networks = data.get('networks', {})
            analysis['content_summary']['network_count'] = len(networks)
            
            # 卷分析
            volumes = data.get('volumes', {})
            analysis['content_summary']['volume_count'] = len(volumes)
            
            # 检查常见问题
            if version and version.startswith('2'):
                analysis['suggestions'].append("建议升级到 Compose 文件格式版本 3.x")
                
            for service_name, service_config in services.items():
                if 'restart' not in service_config:
                    analysis['suggestions'].append(f"服务 {service_name} 建议添加重启策略")
                    
                if 'image' in service_config and ':latest' in service_config['image']:
                    analysis['issues'].append(f"服务 {service_name} 使用 latest 标签，建议指定具体版本")
                    
        except Exception as e:
            analysis['issues'].append(f"解析 YAML 失败: {e}")
            
        return analysis
        
    def backup_config_file(self, file_path: Path) -> Path:
        """备份配置文件
        
        Args:
            file_path: 要备份的文件路径
            
        Returns:
            备份文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.{timestamp}.backup"
        backup_path = self.backup_dir / backup_name
        
        shutil.copy2(file_path, backup_path)
        return backup_path
        
    def optimize_config_file(self, file_path: Path) -> Dict[str, Any]:
        """优化单个配置文件
        
        Args:
            file_path: 配置文件路径
            
        Returns:
            优化结果
        """
        result = {
            'file_path': str(file_path),
            'optimized': False,
            'backup_path': None,
            'changes': [],
            'errors': []
        }
        
        try:
            # 备份原文件
            backup_path = self.backup_config_file(file_path)
            result['backup_path'] = str(backup_path)
            
            # 根据文件名选择优化规则
            file_name = file_path.name
            if file_name in self.optimization_rules:
                optimizer = self.optimization_rules[file_name]
                changes = optimizer(file_path)
                
                if changes:
                    result['optimized'] = True
                    result['changes'] = changes
                else:
                    result['changes'] = ['无需优化']
                    
            else:
                result['changes'] = ['暂无优化规则']
                
        except Exception as e:
            result['errors'].append(str(e))
            
        return result
        
    def _optimize_pyproject_toml(self, file_path: Path) -> List[str]:
        """优化 pyproject.toml 文件"""
        changes = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            data = toml.loads(content)
            
            # 排序依赖
            if 'project' in data and 'dependencies' in data['project']:
                original_deps = data['project']['dependencies']
                sorted_deps = sorted(original_deps, key=lambda x: x.lower())
                
                if original_deps != sorted_deps:
                    data['project']['dependencies'] = sorted_deps
                    changes.append("依赖列表已排序")
                    
            # 排序可选依赖
            if 'project' in data and 'optional-dependencies' in data['project']:
                optional_deps = data['project']['optional-dependencies']
                for group_name, deps in optional_deps.items():
                    sorted_deps = sorted(deps, key=lambda x: x.lower())
                    if deps != sorted_deps:
                        optional_deps[group_name] = sorted_deps
                        changes.append(f"可选依赖组 {group_name} 已排序")
                        
            # 保存修改
            if changes:
                with open(file_path, 'w', encoding='utf-8') as f:
                    toml.dump(data, f)
                    
        except Exception as e:
            changes.append(f"优化失败: {e}")
            
        return changes
        
    def _optimize_requirements_txt(self, file_path: Path) -> List[str]:
        """优化 requirements.txt 文件"""
        changes = []
        
        try:
            lines = file_path.read_text(encoding='utf-8').splitlines()
            
            # 分离依赖和其他内容
            dependencies = []
            other_lines = []
            
            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith('#') and not stripped.startswith('-'):
                    dependencies.append(line)
                else:
                    other_lines.append(line)
                    
            # 排序依赖
            original_deps = dependencies.copy()
            dependencies.sort(key=lambda x: x.lower())
            
            if original_deps != dependencies:
                changes.append("依赖列表已排序")
                
            # 重新组合内容
            new_content = []
            
            # 添加注释和选项
            for line in other_lines:
                if line.strip():
                    new_content.append(line)
                    
            # 添加空行分隔
            if new_content and dependencies:
                new_content.append('')
                
            # 添加排序后的依赖
            new_content.extend(dependencies)
            
            # 保存修改
            if changes:
                file_path.write_text('\n'.join(new_content) + '\n', encoding='utf-8')
                
        except Exception as e:
            changes.append(f"优化失败: {e}")
            
        return changes
        
    def _optimize_package_json(self, file_path: Path) -> List[str]:
        """优化 package.json 文件"""
        changes = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            data = json.loads(content)
            
            # 排序依赖
            for dep_type in ['dependencies', 'devDependencies', 'peerDependencies']:
                if dep_type in data:
                    original_deps = data[dep_type]
                    sorted_deps = dict(sorted(original_deps.items()))
                    
                    if original_deps != sorted_deps:
                        data[dep_type] = sorted_deps
                        changes.append(f"{dep_type} 已排序")
                        
            # 排序脚本
            if 'scripts' in data:
                original_scripts = data['scripts']
                sorted_scripts = dict(sorted(original_scripts.items()))
                
                if original_scripts != sorted_scripts:
                    data['scripts'] = sorted_scripts
                    changes.append("脚本已排序")
                    
            # 保存修改
            if changes:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    
        except Exception as e:
            changes.append(f"优化失败: {e}")
            
        return changes
        
    def _optimize_gitignore(self, file_path: Path) -> List[str]:
        """优化 .gitignore 文件"""
        changes = []
        
        try:
            lines = file_path.read_text(encoding='utf-8').splitlines()
            
            # 分离模式和注释
            patterns = []
            comments = []
            
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#'):
                    comments.append(line)
                elif stripped:
                    patterns.append(line)
                    
            # 去重并排序模式
            unique_patterns = list(dict.fromkeys(patterns))  # 保持顺序的去重
            
            if len(unique_patterns) < len(patterns):
                changes.append("移除重复模式")
                
            # 重新组合内容
            new_content = []
            
            # 添加注释
            if comments:
                new_content.extend(comments)
                new_content.append('')
                
            # 添加模式
            new_content.extend(unique_patterns)
            
            # 保存修改
            if changes:
                file_path.write_text('\n'.join(new_content) + '\n', encoding='utf-8')
                
        except Exception as e:
            changes.append(f"优化失败: {e}")
            
        return changes
        
    def _optimize_docker_compose(self, file_path: Path) -> List[str]:
        """优化 docker-compose.yml 文件"""
        changes = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            data = yaml.safe_load(content)
            
            # 检查并更新版本
            if 'version' in data and data['version'].startswith('2'):
                data['version'] = '3.8'
                changes.append("升级 Compose 文件格式版本到 3.8")
                
            # 为服务添加重启策略
            if 'services' in data:
                for service_name, service_config in data['services'].items():
                    if 'restart' not in service_config:
                        service_config['restart'] = 'unless-stopped'
                        changes.append(f"为服务 {service_name} 添加重启策略")
                        
            # 保存修改
            if changes:
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
                    
        except Exception as e:
            changes.append(f"优化失败: {e}")
            
        return changes
        
    def generate_config_report(self, analyses: List[Dict[str, Any]]) -> str:
        """生成配置分析报告
        
        Args:
            analyses: 分析结果列表
            
        Returns:
            报告内容
        """
        report = f"""
# 配置文件分析报告

生成时间: {datetime.now().isoformat()}

## 概览

"""
        
        total_files = len(analyses)
        total_issues = sum(len(a.get('issues', [])) for a in analyses)
        total_suggestions = sum(len(a.get('suggestions', [])) for a in analyses)
        
        report += f"""
- 总配置文件数: {total_files}
- 发现问题数: {total_issues}
- 优化建议数: {total_suggestions}

## 详细分析

"""
        
        # 按类别分组
        categories = {}
        for analysis in analyses:
            file_path = Path(analysis['file_path'])
            category = 'other'
            
            for cat, patterns in self.config_patterns.items():
                for pattern in patterns.keys():
                    if '*' in pattern:
                        if file_path.match(pattern):
                            category = cat
                            break
                    else:
                        if file_path.name == pattern or str(file_path).endswith(pattern):
                            category = cat
                            break
                if category != 'other':
                    break
                    
            if category not in categories:
                categories[category] = []
            categories[category].append(analysis)
            
        for category, files in categories.items():
            report += f"\n### {category.upper()} 配置\n\n"
            
            for analysis in files:
                file_name = Path(analysis['file_path']).name
                issues = analysis.get('issues', [])
                suggestions = analysis.get('suggestions', [])
                
                status_emoji = "❌" if issues else "✅"
                report += f"#### {status_emoji} {file_name}\n\n"
                
                # 基本信息
                report += f"- **路径**: `{analysis['file_path']}`\n"
                report += f"- **大小**: {analysis.get('file_size', 0)} 字节\n"
                report += f"- **行数**: {analysis.get('line_count', 0)}\n"
                report += f"- **最后修改**: {analysis.get('last_modified', 'Unknown')}\n"
                
                # 内容摘要
                if 'content_summary' in analysis:
                    summary = analysis['content_summary']
                    if summary:
                        report += "\n**内容摘要**:\n"
                        for key, value in summary.items():
                            report += f"- {key}: {value}\n"
                            
                # 问题
                if issues:
                    report += "\n**问题**:\n"
                    for issue in issues:
                        report += f"- ❌ {issue}\n"
                        
                # 建议
                if suggestions:
                    report += "\n**建议**:\n"
                    for suggestion in suggestions:
                        report += f"- 💡 {suggestion}\n"
                        
                report += "\n"
                
        return report
        
    def run_full_analysis(self) -> Dict[str, Any]:
        """运行完整的配置分析
        
        Returns:
            分析结果
        """
        print("🔍 扫描配置文件...")
        config_files = self.scan_config_files()
        
        all_files = []
        for category, files in config_files.items():
            all_files.extend(files)
            
        print(f"📁 发现 {len(all_files)} 个配置文件")
        
        analyses = []
        for i, file_path in enumerate(all_files, 1):
            print(f"[{i}/{len(all_files)}] 分析 {file_path.name}...")
            analysis = self.analyze_config_file(file_path)
            analyses.append(analysis)
            
        return {
            'config_files': config_files,
            'analyses': analyses,
            'summary': {
                'total_files': len(all_files),
                'total_issues': sum(len(a.get('issues', [])) for a in analyses),
                'total_suggestions': sum(len(a.get('suggestions', [])) for a in analyses)
            }
        }
        
    def run_optimization(self, file_patterns: List[str] = None) -> Dict[str, Any]:
        """运行配置优化
        
        Args:
            file_patterns: 要优化的文件模式列表
            
        Returns:
            优化结果
        """
        config_files = self.scan_config_files()
        
        # 确定要优化的文件
        files_to_optimize = []
        
        if file_patterns:
            # 根据模式筛选文件
            for pattern in file_patterns:
                for category, files in config_files.items():
                    for file_path in files:
                        if pattern in file_path.name or pattern in str(file_path):
                            files_to_optimize.append(file_path)
        else:
            # 优化所有支持的文件
            for category, files in config_files.items():
                for file_path in files:
                    if file_path.name in self.optimization_rules:
                        files_to_optimize.append(file_path)
                        
        # 去重
        files_to_optimize = list(set(files_to_optimize))
        
        print(f"🔧 准备优化 {len(files_to_optimize)} 个配置文件")
        
        results = []
        for i, file_path in enumerate(files_to_optimize, 1):
            print(f"[{i}/{len(files_to_optimize)}] 优化 {file_path.name}...")
            result = self.optimize_config_file(file_path)
            results.append(result)
            
        return {
            'optimized_files': len(files_to_optimize),
            'results': results,
            'summary': {
                'successful': len([r for r in results if r['optimized']]),
                'failed': len([r for r in results if r['errors']]),
                'no_changes': len([r for r in results if not r['optimized'] and not r['errors']])
            }
        }

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="配置文件优化器",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--project-root',
        default='.',
        help='项目根目录路径（默认: 当前目录）'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 分析命令
    analyze_parser = subparsers.add_parser('analyze', help='分析配置文件')
    analyze_parser.add_argument('--output', help='输出报告文件路径')
    
    # 优化命令
    optimize_parser = subparsers.add_parser('optimize', help='优化配置文件')
    optimize_parser.add_argument('--files', nargs='*', help='要优化的文件模式')
    optimize_parser.add_argument('--output', help='输出报告文件路径')
    
    args = parser.parse_args()
    
    optimizer = ConfigOptimizer(args.project_root)
    
    if args.command == 'analyze':
        result = optimizer.run_full_analysis()
        
        # 生成报告
        report = optimizer.generate_config_report(result['analyses'])
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"📊 分析报告已保存到: {args.output}")
        else:
            print(report)
            
    elif args.command == 'optimize':
        result = optimizer.run_optimization(args.files)
        
        print(f"\n📊 优化摘要:")
        print(f"- 成功优化: {result['summary']['successful']} 个文件")
        print(f"- 优化失败: {result['summary']['failed']} 个文件")
        print(f"- 无需优化: {result['summary']['no_changes']} 个文件")
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False, default=str)
            print(f"📊 优化结果已保存到: {args.output}")
            
    else:
        print("🔧 配置文件优化器")
        print("\n使用 --help 查看详细帮助信息")
        print("\n示例:")
        print("  python config_optimizer.py analyze")
        print("  python config_optimizer.py optimize --files pyproject.toml")
        
if __name__ == "__main__":
    main()