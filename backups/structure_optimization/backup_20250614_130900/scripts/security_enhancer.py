#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全强化工具
用于扫描和修复项目中的安全漏洞
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
import re
from datetime import datetime

class SecurityEnhancer:
    """安全强化器"""
    
    def __init__(self, project_root: str):
        """初始化安全强化器
        
        Args:
            project_root: 项目根目录路径
        """
        self.project_root = Path(project_root)
        self.security_config = self.project_root / "config" / "security.json"
        
    def scan_vulnerabilities(self) -> Dict:
        """扫描安全漏洞
        
        Returns:
            漏洞扫描结果
        """
        print("🔒 开始安全漏洞扫描...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "dependency_vulnerabilities": self._scan_dependency_vulnerabilities(),
            "code_vulnerabilities": self._scan_code_vulnerabilities(),
            "configuration_issues": self._scan_configuration_issues(),
            "file_permissions": self._check_file_permissions()
        }
        
        return results
    
    def _scan_dependency_vulnerabilities(self) -> List[Dict]:
        """扫描依赖漏洞
        
        Returns:
            依赖漏洞列表
        """
        vulnerabilities = []
        
        try:
            # 使用safety扫描
            result = subprocess.run(
                ['safety', 'check', '--json', '--full-report'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.stdout:
                try:
                    safety_data = json.loads(result.stdout)
                    for vuln in safety_data:
                        vulnerabilities.append({
                            'type': 'dependency',
                            'package': vuln.get('package'),
                            'version': vuln.get('installed_version'),
                            'vulnerability_id': vuln.get('vulnerability_id'),
                            'advisory': vuln.get('advisory'),
                            'cve': vuln.get('cve'),
                            'severity': self._get_severity_from_cve(vuln.get('cve')),
                            'fix_suggestion': f"升级到安全版本: {vuln.get('spec', 'latest')}"
                        })
                except json.JSONDecodeError:
                    pass
                    
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("⚠️ 无法运行safety扫描，请安装safety包")
            
        # 使用bandit扫描Python代码
        try:
            result = subprocess.run(
                ['bandit', '-r', str(self.project_root), '-f', 'json'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.stdout:
                try:
                    bandit_data = json.loads(result.stdout)
                    for issue in bandit_data.get('results', []):
                        vulnerabilities.append({
                            'type': 'code',
                            'file': issue.get('filename'),
                            'line': issue.get('line_number'),
                            'test_id': issue.get('test_id'),
                            'test_name': issue.get('test_name'),
                            'issue_severity': issue.get('issue_severity'),
                            'issue_confidence': issue.get('issue_confidence'),
                            'issue_text': issue.get('issue_text'),
                            'fix_suggestion': self._get_bandit_fix_suggestion(issue.get('test_id'))
                        })
                except json.JSONDecodeError:
                    pass
                    
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("⚠️ 无法运行bandit扫描，请安装bandit包")
            
        return vulnerabilities
    
    def _scan_code_vulnerabilities(self) -> List[Dict]:
        """扫描代码漏洞
        
        Returns:
            代码漏洞列表
        """
        vulnerabilities = []
        
        # 扫描常见的不安全模式
        patterns = {
            'hardcoded_password': r'password\s*=\s*["\'][^"\'
]+["\']',
            'hardcoded_secret': r'secret\s*=\s*["\'][^"\'
]+["\']',
            'hardcoded_api_key': r'api_key\s*=\s*["\'][^"\'
]+["\']',
            'sql_injection': r'execute\s*\(\s*["\'].*%.*["\']',
            'eval_usage': r'eval\s*\(',
            'exec_usage': r'exec\s*\(',
            'pickle_load': r'pickle\.loads?\s*\(',
            'yaml_unsafe_load': r'yaml\.load\s*\(',
            'shell_injection': r'os\.system\s*\(|subprocess\.call\s*\(',
        }
        
        for py_file in self.project_root.rglob('*.py'):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                for pattern_name, pattern in patterns.items():
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        vulnerabilities.append({
                            'type': 'code_pattern',
                            'file': str(py_file.relative_to(self.project_root)),
                            'line': line_num,
                            'pattern': pattern_name,
                            'matched_text': match.group(),
                            'severity': self._get_pattern_severity(pattern_name),
                            'fix_suggestion': self._get_pattern_fix_suggestion(pattern_name)
                        })
                        
            except Exception:
                continue
                
        return vulnerabilities
    
    def _scan_configuration_issues(self) -> List[Dict]:
        """扫描配置问题
        
        Returns:
            配置问题列表
        """
        issues = []
        
        # 检查敏感文件权限
        sensitive_files = [
            'config/security.json',
            'config/system.json',
            '.env',
            'secrets.json'
        ]
        
        for file_path in sensitive_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                # 检查文件权限
                import stat
                file_stat = full_path.stat()
                permissions = oct(file_stat.st_mode)[-3:]
                
                if permissions != '600':  # 应该只有所有者可读写
                    issues.append({
                        'type': 'file_permission',
                        'file': file_path,
                        'current_permission': permissions,
                        'recommended_permission': '600',
                        'severity': 'medium',
                        'fix_suggestion': f'chmod 600 {file_path}'
                    })
                    
        # 检查配置文件中的敏感信息
        config_files = list(self.project_root.rglob('*.json')) + list(self.project_root.rglob('*.yaml')) + list(self.project_root.rglob('*.yml'))
        
        for config_file in config_files:
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 检查是否包含敏感信息
                sensitive_patterns = {
                    'password': r'"password"\s*:\s*"[^"]+"',
                    'secret': r'"secret"\s*:\s*"[^"]+"',
                    'api_key': r'"api_key"\s*:\s*"[^"]+"',
                    'token': r'"token"\s*:\s*"[^"]+"'
                }
                
                for pattern_name, pattern in sensitive_patterns.items():
                    if re.search(pattern, content, re.IGNORECASE):
                        issues.append({
                            'type': 'sensitive_config',
                            'file': str(config_file.relative_to(self.project_root)),
                            'pattern': pattern_name,
                            'severity': 'high',
                            'fix_suggestion': f'将{pattern_name}移动到环境变量或安全的密钥管理系统'
                        })
                        
            except Exception:
                continue
                
        return issues
    
    def _check_file_permissions(self) -> List[Dict]:
        """检查文件权限
        
        Returns:
            文件权限问题列表
        """
        issues = []
        
        # 检查脚本文件权限
        script_files = list(self.project_root.rglob('*.sh')) + list(self.project_root.rglob('*.py'))
        
        for script_file in script_files:
            try:
                import stat
                file_stat = script_file.stat()
                
                # 检查是否有执行权限但不应该有
                if script_file.suffix == '.py' and file_stat.st_mode & stat.S_IXUSR:
                    # Python文件通常不需要执行权限
                    if not script_file.name.startswith('start_') and not script_file.name.startswith('run_'):
                        issues.append({
                            'type': 'unnecessary_execute_permission',
                            'file': str(script_file.relative_to(self.project_root)),
                            'severity': 'low',
                            'fix_suggestion': f'chmod -x {script_file.relative_to(self.project_root)}'
                        })
                        
                # 检查shell脚本是否有执行权限
                if script_file.suffix == '.sh' and not (file_stat.st_mode & stat.S_IXUSR):
                    issues.append({
                        'type': 'missing_execute_permission',
                        'file': str(script_file.relative_to(self.project_root)),
                        'severity': 'medium',
                        'fix_suggestion': f'chmod +x {script_file.relative_to(self.project_root)}'
                    })
                    
            except Exception:
                continue
                
        return issues
    
    def _get_severity_from_cve(self, cve: str) -> str:
        """从CVE获取严重程度
        
        Args:
            cve: CVE编号
            
        Returns:
            严重程度
        """
        # 这里可以集成CVE数据库查询
        # 简化版本，返回默认值
        return 'medium'
    
    def _get_bandit_fix_suggestion(self, test_id: str) -> str:
        """获取bandit测试的修复建议
        
        Args:
            test_id: bandit测试ID
            
        Returns:
            修复建议
        """
        suggestions = {
            'B101': '不要使用assert语句进行安全检查',
            'B102': '避免使用exec_used',
            'B103': '设置适当的文件权限',
            'B104': '绑定到所有接口可能不安全',
            'B105': '硬编码密码字符串',
            'B106': '硬编码密码函数参数',
            'B107': '硬编码密码默认参数',
            'B108': '临时文件创建不安全',
            'B110': 'try/except/pass可能隐藏错误',
            'B112': 'try/except/continue可能隐藏错误',
            'B201': 'Flask应用调试模式',
            'B301': 'pickle和相关模块不安全',
            'B302': 'marshal.loads不安全',
            'B303': 'MD5哈希算法不安全',
            'B304': '不安全的密码学算法',
            'B305': '不安全的密码学算法',
            'B306': 'mktemp不安全',
            'B307': 'eval使用不安全',
            'B308': 'mark_safe可能不安全',
            'B309': 'HTTPSConnection不验证证书',
            'B310': 'urllib.urlopen不安全',
            'B311': '随机数生成器不安全',
            'B312': 'telnetlib使用不安全',
            'B313': 'XML解析器不安全',
            'B314': 'XML解析器不安全',
            'B315': 'XML解析器不安全',
            'B316': 'XML解析器不安全',
            'B317': 'XML解析器不安全',
            'B318': 'XML解析器不安全',
            'B319': 'XML解析器不安全',
            'B320': 'XML解析器不安全',
            'B321': 'FTP相关安全问题',
            'B322': 'input()函数使用',
            'B323': '不安全的随机数生成',
            'B324': 'hashlib.new不安全参数',
            'B325': 'tempfile.mktemp不安全',
            'B401': 'import telnetlib',
            'B402': 'import ftplib',
            'B403': 'import pickle',
            'B404': 'import subprocess',
            'B405': 'import xml.etree',
            'B406': 'import xml.sax',
            'B407': 'import xml.dom',
            'B408': 'import xml.minidom',
            'B409': 'import xml.pulldom',
            'B410': 'import lxml',
            'B411': 'import xmlrpclib',
            'B412': 'import httpoxy',
            'B413': 'import pycrypto',
            'B501': 'SSL证书验证禁用',
            'B502': 'SSL证书验证禁用',
            'B503': 'SSL证书验证禁用',
            'B504': 'SSL证书验证禁用',
            'B505': 'SSL证书验证禁用',
            'B506': 'YAML不安全加载',
            'B507': 'SSH主机密钥验证禁用',
            'B601': 'shell注入风险',
            'B602': 'subprocess shell注入',
            'B603': 'subprocess不安全',
            'B604': 'shell调用不安全',
            'B605': 'shell调用不安全',
            'B606': 'shell调用不安全',
            'B607': 'shell调用不安全',
            'B608': 'SQL注入风险',
            'B609': 'Linux命令通配符注入',
            'B610': 'Django SQL注入',
            'B611': 'Django SQL注入',
            'B701': 'jinja2自动转义禁用',
            'B702': 'Mako模板自动转义禁用',
            'B703': 'Django标记安全',
        }
        
        return suggestions.get(test_id, '请查阅bandit文档获取详细修复建议')
    
    def _get_pattern_severity(self, pattern_name: str) -> str:
        """获取模式的严重程度
        
        Args:
            pattern_name: 模式名称
            
        Returns:
            严重程度
        """
        severity_map = {
            'hardcoded_password': 'high',
            'hardcoded_secret': 'high',
            'hardcoded_api_key': 'high',
            'sql_injection': 'high',
            'eval_usage': 'high',
            'exec_usage': 'high',
            'pickle_load': 'medium',
            'yaml_unsafe_load': 'medium',
            'shell_injection': 'high'
        }
        
        return severity_map.get(pattern_name, 'medium')
    
    def _get_pattern_fix_suggestion(self, pattern_name: str) -> str:
        """获取模式的修复建议
        
        Args:
            pattern_name: 模式名称
            
        Returns:
            修复建议
        """
        suggestions = {
            'hardcoded_password': '使用环境变量或安全的密钥管理系统存储密码',
            'hardcoded_secret': '使用环境变量或安全的密钥管理系统存储密钥',
            'hardcoded_api_key': '使用环境变量或安全的密钥管理系统存储API密钥',
            'sql_injection': '使用参数化查询或ORM防止SQL注入',
            'eval_usage': '避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案',
            'exec_usage': '避免使用exec()，重新设计代码逻辑',
            'pickle_load': '避免反序列化不可信数据，考虑使用JSON或其他安全格式',
            'yaml_unsafe_load': '使用yaml.safe_load()代替yaml.load()',
            'shell_injection': '使用subprocess的列表参数形式，避免shell=True'
        }
        
        return suggestions.get(pattern_name, '请查阅安全编码最佳实践')
    
    def generate_security_report(self, scan_results: Dict) -> str:
        """生成安全报告
        
        Args:
            scan_results: 扫描结果
            
        Returns:
            安全报告内容
        """
        report = f"""
# 安全扫描报告

生成时间: {scan_results['timestamp']}

## 概览
- 依赖漏洞: {len(scan_results['dependency_vulnerabilities'])} 个
- 代码漏洞: {len(scan_results['code_vulnerabilities'])} 个
- 配置问题: {len(scan_results['configuration_issues'])} 个
- 文件权限问题: {len(scan_results['file_permissions'])} 个

## 依赖漏洞详情
"""
        
        for vuln in scan_results['dependency_vulnerabilities']:
            if vuln.get('type') == 'dependency':
                report += f"""
### {vuln['package']} {vuln['version']}
- **漏洞ID**: {vuln['vulnerability_id']}
- **CVE**: {vuln.get('cve', 'N/A')}
- **严重程度**: {vuln.get('severity', 'unknown')}
- **描述**: {vuln['advisory']}
- **修复建议**: {vuln['fix_suggestion']}

"""
            
        report += "\n## 代码安全问题\n"
        
        for vuln in scan_results['code_vulnerabilities']:
            report += f"""
### {vuln.get('file', 'unknown')}:{vuln.get('line', 'unknown')}
- **问题类型**: {vuln.get('pattern', vuln.get('test_name', 'unknown'))}
- **严重程度**: {vuln.get('severity', vuln.get('issue_severity', 'unknown'))}
- **描述**: {vuln.get('matched_text', vuln.get('issue_text', 'N/A'))}
- **修复建议**: {vuln['fix_suggestion']}

"""
            
        report += "\n## 配置安全问题\n"
        
        for issue in scan_results['configuration_issues']:
            report += f"""
### {issue['file']}
- **问题类型**: {issue['type']}
- **严重程度**: {issue['severity']}
- **修复建议**: {issue['fix_suggestion']}

"""
            
        report += "\n## 文件权限问题\n"
        
        for issue in scan_results['file_permissions']:
            report += f"""
### {issue['file']}
- **问题类型**: {issue['type']}
- **严重程度**: {issue['severity']}
- **修复建议**: {issue['fix_suggestion']}

"""
            
        return report
    
    def apply_security_fixes(self, scan_results: Dict) -> Dict:
        """应用安全修复
        
        Args:
            scan_results: 扫描结果
            
        Returns:
            修复结果
        """
        print("🔧 开始应用安全修复...")
        
        fixes_applied = {
            'file_permissions': [],
            'configuration_updates': [],
            'dependency_updates': []
        }
        
        # 修复文件权限问题
        for issue in scan_results['file_permissions']:
            if issue['type'] == 'missing_execute_permission':
                try:
                    file_path = self.project_root / issue['file']
                    file_path.chmod(file_path.stat().st_mode | 0o111)
                    fixes_applied['file_permissions'].append(f"添加执行权限: {issue['file']}")
                except Exception as e:
                    print(f"⚠️ 无法修复权限 {issue['file']}: {e}")
                    
        # 修复配置问题
        for issue in scan_results['configuration_issues']:
            if issue['type'] == 'file_permission':
                try:
                    file_path = self.project_root / issue['file']
                    file_path.chmod(0o600)
                    fixes_applied['file_permissions'].append(f"设置安全权限: {issue['file']}")
                except Exception as e:
                    print(f"⚠️ 无法修复权限 {issue['file']}: {e}")
                    
        return fixes_applied
    
    def save_security_report(self, scan_results: Dict, output_file: str = None):
        """保存安全报告
        
        Args:
            scan_results: 扫描结果
            output_file: 输出文件路径
        """
        if output_file is None:
            output_file = self.project_root / "security_scan_report.md"
            
        report = self.generate_security_report(scan_results)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
            
        print(f"🔒 安全报告已保存到: {output_file}")
        
        # 同时保存JSON格式的详细数据
        json_file = str(output_file).replace('.md', '.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(scan_results, f, indent=2, ensure_ascii=False)
            
        print(f"🔒 详细数据已保存到: {json_file}")

def main():
    """主函数"""
    project_root = Path.cwd()
    
    print("🚀 开始安全扫描...")
    enhancer = SecurityEnhancer(str(project_root))
    
    # 执行扫描
    scan_results = enhancer.scan_vulnerabilities()
    
    # 生成并保存报告
    enhancer.save_security_report(scan_results)
    
    # 应用自动修复
    fixes = enhancer.apply_security_fixes(scan_results)
    
    # 打印摘要
    print("\n🔒 安全扫描摘要:")
    print(f"- 依赖漏洞: {len(scan_results['dependency_vulnerabilities'])} 个")
    print(f"- 代码漏洞: {len(scan_results['code_vulnerabilities'])} 个")
    print(f"- 配置问题: {len(scan_results['configuration_issues'])} 个")
    print(f"- 文件权限问题: {len(scan_results['file_permissions'])} 个")
    
    print("\n🔧 自动修复摘要:")
    print(f"- 权限修复: {len(fixes['file_permissions'])} 个")
    print(f"- 配置更新: {len(fixes['configuration_updates'])} 个")
    print(f"- 依赖更新: {len(fixes['dependency_updates'])} 个")
    
if __name__ == "__main__":
    main()