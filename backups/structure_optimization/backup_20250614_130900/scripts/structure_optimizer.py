#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目结构优化工具
用于清理冗余文件、优化目录结构和提升项目组织性
"""

import json
import shutil
import hashlib
from pathlib import Path
from typing import Dict, List, Set, Tuple
from datetime import datetime
import re

class StructureOptimizer:
    """项目结构优化器"""
    
    def __init__(self, project_root: str):
        """初始化结构优化器
        
        Args:
            project_root: 项目根目录路径
        """
        self.project_root = Path(project_root)
        self.backup_dir = self.project_root / "backups" / "structure_optimization"
        
    def analyze_structure(self) -> Dict:
        """分析项目结构
        
        Returns:
            结构分析结果
        """
        print("📊 开始项目结构分析...")
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "duplicate_files": self._find_duplicate_files(),
            "empty_directories": self._find_empty_directories(),
            "large_files": self._find_large_files(),
            "temporary_files": self._find_temporary_files(),
            "redundant_configs": self._find_redundant_configs(),
            "unused_assets": self._find_unused_assets(),
            "structure_suggestions": self._analyze_structure_patterns()
        }
        
        return analysis
    
    def _find_duplicate_files(self) -> List[Dict]:
        """查找重复文件
        
        Returns:
            重复文件列表
        """
        print("🔍 查找重复文件...")
        
        file_hashes = {}
        duplicates = []
        
        # 排除的目录
        exclude_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'cache', 'logs'}
        
        for file_path in self.project_root.rglob('*'):
            if file_path.is_file() and not any(part in exclude_dirs for part in file_path.parts):
                try:
                    # 计算文件哈希
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                    
                    if file_hash in file_hashes:
                        # 找到重复文件
                        duplicates.append({
                            'hash': file_hash,
                            'original': str(file_hashes[file_hash].relative_to(self.project_root)),
                            'duplicate': str(file_path.relative_to(self.project_root)),
                            'size': file_path.stat().st_size
                        })
                    else:
                        file_hashes[file_hash] = file_path
                        
                except Exception:
                    continue
                    
        return duplicates
    
    def _find_empty_directories(self) -> List[str]:
        """查找空目录
        
        Returns:
            空目录列表
        """
        print("📁 查找空目录...")
        
        empty_dirs = []
        
        for dir_path in self.project_root.rglob('*'):
            if dir_path.is_dir():
                try:
                    # 检查目录是否为空（忽略隐藏文件）
                    contents = [item for item in dir_path.iterdir() if not item.name.startswith('.')]
                    if not contents:
                        empty_dirs.append(str(dir_path.relative_to(self.project_root)))
                except Exception:
                    continue
                    
        return empty_dirs
    
    def _find_large_files(self, size_threshold: int = 10 * 1024 * 1024) -> List[Dict]:
        """查找大文件
        
        Args:
            size_threshold: 大小阈值（字节），默认10MB
            
        Returns:
            大文件列表
        """
        print("📏 查找大文件...")
        
        large_files = []
        
        for file_path in self.project_root.rglob('*'):
            if file_path.is_file():
                try:
                    size = file_path.stat().st_size
                    if size > size_threshold:
                        large_files.append({
                            'file': str(file_path.relative_to(self.project_root)),
                            'size': size,
                            'size_mb': round(size / (1024 * 1024), 2),
                            'type': file_path.suffix or 'no_extension'
                        })
                except Exception:
                    continue
                    
        # 按大小排序
        large_files.sort(key=lambda x: x['size'], reverse=True)
        return large_files
    
    def _find_temporary_files(self) -> List[str]:
        """查找临时文件
        
        Returns:
            临时文件列表
        """
        print("🗑️ 查找临时文件...")
        
        temp_patterns = [
            r'.*\.tmp$',
            r'.*\.temp$',
            r'.*\.bak$',
            r'.*\.backup$',
            r'.*~$',
            r'.*\.swp$',
            r'.*\.swo$',
            r'.*\.log$',
            r'.*\.cache$',
            r'.*\.pid$',
            r'.*\.lock$',
            r'.*\.orig$',
            r'.*\.rej$',
            r'.*\.pyc$',
            r'.*\.pyo$',
            r'.*\.pyd$',
            r'.*__pycache__.*',
            r'.*\.DS_Store$',
            r'.*Thumbs\.db$',
            r'.*\.coverage$',
            r'.*\.pytest_cache.*',
            r'.*\.mypy_cache.*',
            r'.*\.tox.*',
            r'.*\.nox.*'
        ]
        
        temp_files = []
        
        for file_path in self.project_root.rglob('*'):
            if file_path.is_file():
                file_str = str(file_path.relative_to(self.project_root))
                for pattern in temp_patterns:
                    if re.match(pattern, file_str, re.IGNORECASE):
                        temp_files.append(file_str)
                        break
                        
        return temp_files
    
    def _find_redundant_configs(self) -> List[Dict]:
        """查找冗余配置文件
        
        Returns:
            冗余配置文件列表
        """
        print("⚙️ 查找冗余配置文件...")
        
        config_files = {
            'mcp_config': [],
            'server_config': [],
            'test_config': [],
            'requirements': []
        }
        
        # 查找各类配置文件
        for file_path in self.project_root.rglob('*'):
            if file_path.is_file():
                name = file_path.name.lower()
                
                if 'mcp_config' in name and name.endswith('.json'):
                    config_files['mcp_config'].append(str(file_path.relative_to(self.project_root)))
                elif 'server' in name and (name.endswith('.py') or name.endswith('.json')):
                    config_files['server_config'].append(str(file_path.relative_to(self.project_root)))
                elif 'test' in name and name.endswith('.py'):
                    config_files['test_config'].append(str(file_path.relative_to(self.project_root)))
                elif 'requirements' in name and name.endswith('.txt'):
                    config_files['requirements'].append(str(file_path.relative_to(self.project_root)))
                    
        # 识别冗余
        redundant = []
        for config_type, files in config_files.items():
            if len(files) > 1:
                redundant.append({
                    'type': config_type,
                    'files': files,
                    'count': len(files),
                    'suggestion': self._get_config_consolidation_suggestion(config_type, files)
                })
                
        return redundant
    
    def _find_unused_assets(self) -> List[str]:
        """查找未使用的资源文件
        
        Returns:
            未使用资源文件列表
        """
        print("🖼️ 查找未使用的资源文件...")
        
        # 查找所有资源文件
        asset_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.css', '.js', '.html'}
        assets = []
        
        for file_path in self.project_root.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in asset_extensions:
                assets.append(file_path)
                
        # 查找代码文件中的引用
        referenced_assets = set()
        code_extensions = {'.py', '.html', '.css', '.js', '.md', '.json', '.yaml', '.yml'}
        
        for code_file in self.project_root.rglob('*'):
            if code_file.is_file() and code_file.suffix.lower() in code_extensions:
                try:
                    with open(code_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    # 查找资源文件引用
                    for asset in assets:
                        asset_name = asset.name
                        if asset_name in content:
                            referenced_assets.add(asset)
                            
                except Exception:
                    continue
                    
        # 找出未引用的资源
        unused_assets = []
        for asset in assets:
            if asset not in referenced_assets:
                # 排除一些特殊文件
                if asset.name not in ['favicon.ico', 'robots.txt', 'sitemap.xml']:
                    unused_assets.append(str(asset.relative_to(self.project_root)))
                    
        return unused_assets
    
    def _analyze_structure_patterns(self) -> List[Dict]:
        """分析结构模式并提供建议
        
        Returns:
            结构建议列表
        """
        print("🏗️ 分析项目结构模式...")
        
        suggestions = []
        
        # 检查是否有合适的目录结构
        expected_dirs = ['src', 'tests', 'docs', 'config', 'scripts']
        missing_dirs = []
        
        for expected_dir in expected_dirs:
            if not (self.project_root / expected_dir).exists():
                missing_dirs.append(expected_dir)
                
        if missing_dirs:
            suggestions.append({
                'type': 'missing_directories',
                'description': '缺少标准目录结构',
                'missing': missing_dirs,
                'suggestion': '考虑创建标准的项目目录结构'
            })
            
        # 检查文件分布
        root_py_files = [f for f in self.project_root.glob('*.py') if f.is_file()]
        if len(root_py_files) > 5:
            suggestions.append({
                'type': 'too_many_root_files',
                'description': '根目录下Python文件过多',
                'count': len(root_py_files),
                'files': [f.name for f in root_py_files],
                'suggestion': '考虑将Python文件移动到src/或适当的子目录中'
            })
            
        # 检查测试文件组织
        test_files = list(self.project_root.rglob('test_*.py')) + list(self.project_root.rglob('*_test.py'))
        test_dir_files = list((self.project_root / 'tests').rglob('*.py')) if (self.project_root / 'tests').exists() else []
        test_dir_files += list((self.project_root / 'test').rglob('*.py')) if (self.project_root / 'test').exists() else []
        
        scattered_tests = [f for f in test_files if not any(part in ['tests', 'test'] for part in f.parts)]
        
        if scattered_tests:
            suggestions.append({
                'type': 'scattered_test_files',
                'description': '测试文件分散在项目中',
                'count': len(scattered_tests),
                'files': [str(f.relative_to(self.project_root)) for f in scattered_tests],
                'suggestion': '考虑将所有测试文件移动到tests/目录中'
            })
            
        # 检查配置文件组织
        config_files = []
        for pattern in ['*.json', '*.yaml', '*.yml', '*.toml', '*.ini', '*.cfg']:
            config_files.extend(self.project_root.glob(pattern))
            
        root_config_files = [f for f in config_files if f.parent == self.project_root]
        
        if len(root_config_files) > 3:
            suggestions.append({
                'type': 'too_many_root_configs',
                'description': '根目录下配置文件过多',
                'count': len(root_config_files),
                'files': [f.name for f in root_config_files],
                'suggestion': '考虑将配置文件移动到config/目录中'
            })
            
        return suggestions
    
    def _get_config_consolidation_suggestion(self, config_type: str, files: List[str]) -> str:
        """获取配置文件整合建议
        
        Args:
            config_type: 配置类型
            files: 文件列表
            
        Returns:
            整合建议
        """
        suggestions = {
            'mcp_config': '保留一个主要的MCP配置文件，将其他配置合并或移动到config/目录',
            'server_config': '整合服务器配置，保留一个主服务器文件',
            'test_config': '将测试文件移动到tests/目录并整合重复的测试',
            'requirements': '保留requirements.txt，将其他依赖文件整合到pyproject.toml'
        }
        
        return suggestions.get(config_type, '考虑整合重复的配置文件')
    
    def optimize_structure(self, analysis: Dict, auto_fix: bool = False) -> Dict:
        """优化项目结构
        
        Args:
            analysis: 结构分析结果
            auto_fix: 是否自动修复
            
        Returns:
            优化结果
        """
        print("🔧 开始结构优化...")
        
        optimization_results = {
            'timestamp': datetime.now().isoformat(),
            'actions_taken': [],
            'manual_actions_needed': [],
            'backup_created': False
        }
        
        if auto_fix:
            # 创建备份
            self._create_backup()
            optimization_results['backup_created'] = True
            
            # 删除临时文件
            for temp_file in analysis['temporary_files']:
                try:
                    file_path = self.project_root / temp_file
                    if file_path.exists():
                        file_path.unlink()
                        optimization_results['actions_taken'].append(f"删除临时文件: {temp_file}")
                except Exception as e:
                    print(f"⚠️ 无法删除临时文件 {temp_file}: {e}")
                    
            # 删除空目录
            for empty_dir in analysis['empty_directories']:
                try:
                    dir_path = self.project_root / empty_dir
                    if dir_path.exists() and dir_path.is_dir():
                        dir_path.rmdir()
                        optimization_results['actions_taken'].append(f"删除空目录: {empty_dir}")
                except Exception as e:
                    print(f"⚠️ 无法删除空目录 {empty_dir}: {e}")
                    
            # 创建建议的目录结构
            for suggestion in analysis['structure_suggestions']:
                if suggestion['type'] == 'missing_directories':
                    for missing_dir in suggestion['missing']:
                        try:
                            dir_path = self.project_root / missing_dir
                            dir_path.mkdir(exist_ok=True)
                            optimization_results['actions_taken'].append(f"创建目录: {missing_dir}")
                        except Exception as e:
                            print(f"⚠️ 无法创建目录 {missing_dir}: {e}")
                            
        # 添加需要手动处理的项目
        for duplicate in analysis['duplicate_files']:
            optimization_results['manual_actions_needed'].append(
                f"手动检查重复文件: {duplicate['original']} vs {duplicate['duplicate']}"
            )
            
        for large_file in analysis['large_files'][:5]:  # 只显示前5个最大的文件
            optimization_results['manual_actions_needed'].append(
                f"检查大文件: {large_file['file']} ({large_file['size_mb']} MB)"
            )
            
        for redundant in analysis['redundant_configs']:
            optimization_results['manual_actions_needed'].append(
                f"整合冗余配置: {redundant['type']} - {redundant['suggestion']}"
            )
            
        return optimization_results
    
    def _create_backup(self):
        """创建项目备份"""
        print("💾 创建项目备份...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"backup_{timestamp}"
        
        # 创建备份目录
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # 备份重要文件
        important_files = [
            'requirements.txt',
            'pyproject.toml',
            'README.md',
            'config/',
            'scripts/'
        ]
        
        for item in important_files:
            source = self.project_root / item
            if source.exists():
                dest = backup_path / item
                try:
                    if source.is_file():
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source, dest)
                    elif source.is_dir():
                        shutil.copytree(source, dest, dirs_exist_ok=True)
                except Exception as e:
                    print(f"⚠️ 备份失败 {item}: {e}")
                    
        print(f"✅ 备份已创建: {backup_path}")
    
    def generate_optimization_report(self, analysis: Dict, optimization_results: Dict = None) -> str:
        """生成优化报告
        
        Args:
            analysis: 分析结果
            optimization_results: 优化结果
            
        Returns:
            优化报告内容
        """
        report = f"""
# 项目结构优化报告

生成时间: {analysis['timestamp']}

## 分析概览
- 重复文件: {len(analysis['duplicate_files'])} 组
- 空目录: {len(analysis['empty_directories'])} 个
- 大文件: {len(analysis['large_files'])} 个
- 临时文件: {len(analysis['temporary_files'])} 个
- 冗余配置: {len(analysis['redundant_configs'])} 组
- 未使用资源: {len(analysis['unused_assets'])} 个
- 结构建议: {len(analysis['structure_suggestions'])} 项

## 重复文件详情
"""
        
        for duplicate in analysis['duplicate_files']:
            report += f"""
### 重复文件组 (大小: {duplicate['size']} 字节)
- 原文件: {duplicate['original']}
- 重复文件: {duplicate['duplicate']}

"""
            
        report += "\n## 大文件列表\n"
        
        for large_file in analysis['large_files'][:10]:  # 只显示前10个
            report += f"- {large_file['file']}: {large_file['size_mb']} MB\n"
            
        report += "\n## 临时文件列表\n"
        
        for temp_file in analysis['temporary_files'][:20]:  # 只显示前20个
            report += f"- {temp_file}\n"
            
        if len(analysis['temporary_files']) > 20:
            report += f"... 还有 {len(analysis['temporary_files']) - 20} 个临时文件\n"
            
        report += "\n## 冗余配置详情\n"
        
        for redundant in analysis['redundant_configs']:
            report += f"""
### {redundant['type']} ({redundant['count']} 个文件)
文件列表:
"""
            for file in redundant['files']:
                report += f"- {file}\n"
            report += f"**建议**: {redundant['suggestion']}\n\n"
            
        report += "\n## 结构优化建议\n"
        
        for suggestion in analysis['structure_suggestions']:
            report += f"""
### {suggestion['description']}
- **类型**: {suggestion['type']}
- **建议**: {suggestion['suggestion']}

"""
            
        if optimization_results:
            report += f"""

## 优化执行结果

执行时间: {optimization_results['timestamp']}
备份创建: {'是' if optimization_results['backup_created'] else '否'}

### 已执行的操作
"""
            for action in optimization_results['actions_taken']:
                report += f"- {action}\n"
                
            report += "\n### 需要手动处理的项目\n"
            
            for action in optimization_results['manual_actions_needed']:
                report += f"- {action}\n"
                
        return report
    
    def save_optimization_report(self, analysis: Dict, optimization_results: Dict = None, output_file: str = None):
        """保存优化报告
        
        Args:
            analysis: 分析结果
            optimization_results: 优化结果
            output_file: 输出文件路径
        """
        if output_file is None:
            output_file = self.project_root / "structure_optimization_report.md"
            
        report = self.generate_optimization_report(analysis, optimization_results)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
            
        print(f"📊 优化报告已保存到: {output_file}")
        
        # 同时保存JSON格式的详细数据
        json_data = {
            'analysis': analysis,
            'optimization_results': optimization_results
        }
        
        json_file = str(output_file).replace('.md', '.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
            
        print(f"📊 详细数据已保存到: {json_file}")

def main():
    """主函数"""
    project_root = Path.cwd()
    
    print("🚀 开始项目结构优化...")
    optimizer = StructureOptimizer(str(project_root))
    
    # 执行分析
    analysis = optimizer.analyze_structure()
    
    # 执行优化（自动修复安全的操作）
    optimization_results = optimizer.optimize_structure(analysis, auto_fix=True)
    
    # 生成并保存报告
    optimizer.save_optimization_report(analysis, optimization_results)
    
    # 打印摘要
    print("\n📊 结构分析摘要:")
    print(f"- 重复文件: {len(analysis['duplicate_files'])} 组")
    print(f"- 空目录: {len(analysis['empty_directories'])} 个")
    print(f"- 大文件: {len(analysis['large_files'])} 个")
    print(f"- 临时文件: {len(analysis['temporary_files'])} 个")
    print(f"- 冗余配置: {len(analysis['redundant_configs'])} 组")
    print(f"- 未使用资源: {len(analysis['unused_assets'])} 个")
    
    print("\n🔧 优化执行摘要:")
    print(f"- 已执行操作: {len(optimization_results['actions_taken'])} 项")
    print(f"- 需手动处理: {len(optimization_results['manual_actions_needed'])} 项")
    print(f"- 备份已创建: {'是' if optimization_results['backup_created'] else '否'}")
    
if __name__ == "__main__":
    main()