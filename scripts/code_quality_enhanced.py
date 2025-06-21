#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强的代码质量检查脚本

集成多种静态分析工具，提供全面的代码质量评估。
支持生成详细报告和修复建议，集成 pre-commit 钩子。

使用方法:
    python scripts/code_quality_enhanced.py [选项]

选项:
    --fix: 自动修复可修复的问题
    --report: 生成详细报告
    --config: 指定配置文件路径
    --exclude: 排除特定目录或文件
    --install-hooks: 安装 pre-commit 钩子
    --run-hooks: 运行 pre-commit 钩子
"""

import os
import sys
import subprocess
import json
import time
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class QualityResult:
    """质量检查结果"""
    tool: str
    status: str  # 'success', 'warning', 'error', 'skipped'
    score: Optional[float] = None
    issues: List[Dict[str, Any]] = None
    execution_time: float = 0.0
    output: str = ""
    error: str = ""


class CodeQualityChecker:
    """代码质量检查器"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.results: List[QualityResult] = []
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置"""
        config_file = self.project_root / "pyproject.toml"
        if config_file.exists():
            try:
                import toml
                with open(config_file, 'r', encoding='utf-8') as f:
                    return toml.load(f)
            except ImportError:
                print("警告: 未安装 toml 库，使用默认配置")
            except Exception as e:
                print(f"警告: 读取配置文件失败: {e}")
        
        return {
            "tool": {
                "black": {"line-length": 88, "target-version": ["py311"]},
                "isort": {"profile": "black", "line_length": 88},
                "flake8": {"max-line-length": 88, "ignore": ["E203", "W503"]},
                "mypy": {"python_version": "3.11", "strict": True},
                "bandit": {"exclude_dirs": ["tests", "venv", ".venv"]}
            }
        }
    
    def _run_command(self, cmd: List[str], cwd: Optional[Path] = None) -> tuple[int, str, str]:
        """运行命令并返回结果"""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "命令执行超时"
        except Exception as e:
            return -1, "", str(e)
    
    def _check_tool_available(self, tool: str) -> bool:
        """检查工具是否可用"""
        try:
            result = subprocess.run(
                [tool, "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def check_black(self) -> QualityResult:
        """检查代码格式化 (Black)"""
        start_time = time.time()
        
        if not self._check_tool_available("black"):
            return QualityResult(
                tool="black",
                status="skipped",
                error="Black 未安装",
                execution_time=time.time() - start_time
            )
        
        # 检查格式化
        cmd = ["black", "--check", "--diff", "--color", "."]
        returncode, stdout, stderr = self._run_command(cmd)
        
        if returncode == 0:
            status = "success"
            score = 100.0
        else:
            status = "warning"
            score = 70.0  # 需要格式化但不是错误
        
        return QualityResult(
            tool="black",
            status=status,
            score=score,
            output=stdout,
            error=stderr,
            execution_time=time.time() - start_time
        )
    
    def check_isort(self) -> QualityResult:
        """检查导入排序 (isort)"""
        start_time = time.time()
        
        if not self._check_tool_available("isort"):
            return QualityResult(
                tool="isort",
                status="skipped",
                error="isort 未安装",
                execution_time=time.time() - start_time
            )
        
        cmd = ["isort", "--check-only", "--diff", "."]
        returncode, stdout, stderr = self._run_command(cmd)
        
        if returncode == 0:
            status = "success"
            score = 100.0
        else:
            status = "warning"
            score = 80.0
        
        return QualityResult(
            tool="isort",
            status=status,
            score=score,
            output=stdout,
            error=stderr,
            execution_time=time.time() - start_time
        )
    
    def check_flake8(self) -> QualityResult:
        """检查代码风格 (Flake8)"""
        start_time = time.time()
        
        if not self._check_tool_available("flake8"):
            return QualityResult(
                tool="flake8",
                status="skipped",
                error="flake8 未安装",
                execution_time=time.time() - start_time
            )
        
        cmd = ["flake8", "--format=json", "."]
        returncode, stdout, stderr = self._run_command(cmd)
        
        issues = []
        if stdout:
            try:
                # Flake8 JSON 格式输出
                for line in stdout.strip().split('\n'):
                    if line:
                        issue = json.loads(line)
                        issues.append(issue)
            except json.JSONDecodeError:
                # 如果不是 JSON 格式，按行解析
                issues = [{'message': line} for line in stdout.strip().split('\n') if line]
        
        # 计算分数
        if len(issues) == 0:
            status = "success"
            score = 100.0
        elif len(issues) <= 10:
            status = "warning"
            score = max(70.0, 100.0 - len(issues) * 3)
        else:
            status = "error"
            score = max(30.0, 100.0 - len(issues) * 2)
        
        return QualityResult(
            tool="flake8",
            status=status,
            score=score,
            issues=issues,
            output=stdout,
            error=stderr,
            execution_time=time.time() - start_time
        )
    
    def check_mypy(self) -> QualityResult:
        """检查类型注解 (MyPy)"""
        start_time = time.time()
        
        if not self._check_tool_available("mypy"):
            return QualityResult(
                tool="mypy",
                status="skipped",
                error="mypy 未安装",
                execution_time=time.time() - start_time
            )
        
        cmd = ["mypy", "--json-report", "/tmp/mypy_report", "."]
        returncode, stdout, stderr = self._run_command(cmd)
        
        issues = []
        # 解析 MyPy 输出
        if stderr:
            for line in stderr.strip().split('\n'):
                if line and ':' in line:
                    parts = line.split(':', 3)
                    if len(parts) >= 4:
                        issues.append({
                            'file': parts[0],
                            'line': parts[1],
                            'column': parts[2] if parts[2].isdigit() else '0',
                            'message': parts[3].strip()
                        })
        
        # 计算分数
        if len(issues) == 0:
            status = "success"
            score = 100.0
        elif len(issues) <= 5:
            status = "warning"
            score = max(80.0, 100.0 - len(issues) * 4)
        else:
            status = "error"
            score = max(50.0, 100.0 - len(issues) * 3)
        
        return QualityResult(
            tool="mypy",
            status=status,
            score=score,
            issues=issues,
            output=stdout,
            error=stderr,
            execution_time=time.time() - start_time
        )
    
    def check_bandit(self) -> QualityResult:
        """检查安全问题 (Bandit)"""
        start_time = time.time()
        
        if not self._check_tool_available("bandit"):
            return QualityResult(
                tool="bandit",
                status="skipped",
                error="bandit 未安装",
                execution_time=time.time() - start_time
            )
        
        cmd = ["bandit", "-r", ".", "-f", "json", "-x", "tests,venv,.venv"]
        returncode, stdout, stderr = self._run_command(cmd)
        
        issues = []
        if stdout:
            try:
                data = json.loads(stdout)
                issues = data.get('results', [])
            except json.JSONDecodeError:
                pass
        
        # 计算分数 - 安全问题更严重
        high_severity = len([i for i in issues if i.get('issue_severity') == 'HIGH'])
        medium_severity = len([i for i in issues if i.get('issue_severity') == 'MEDIUM'])
        low_severity = len([i for i in issues if i.get('issue_severity') == 'LOW'])
        
        if high_severity > 0:
            status = "error"
            score = max(20.0, 100.0 - high_severity * 20 - medium_severity * 10 - low_severity * 5)
        elif medium_severity > 0:
            status = "warning"
            score = max(60.0, 100.0 - medium_severity * 10 - low_severity * 5)
        elif low_severity > 0:
            status = "warning"
            score = max(80.0, 100.0 - low_severity * 5)
        else:
            status = "success"
            score = 100.0
        
        return QualityResult(
            tool="bandit",
            status=status,
            score=score,
            issues=issues,
            output=stdout,
            error=stderr,
            execution_time=time.time() - start_time
        )
    
    def check_pytest(self) -> QualityResult:
        """运行测试 (Pytest)"""
        start_time = time.time()
        
        if not self._check_tool_available("pytest"):
            return QualityResult(
                tool="pytest",
                status="skipped",
                error="pytest 未安装",
                execution_time=time.time() - start_time
            )
        
        cmd = ["pytest", "--tb=short", "-v", "--json-report", "--json-report-file=/tmp/pytest_report.json"]
        returncode, stdout, stderr = self._run_command(cmd)
        
        # 解析测试结果
        test_results = {}
        try:
            with open('/tmp/pytest_report.json', 'r') as f:
                test_results = json.load(f)
        except:
            pass
        
        total_tests = test_results.get('summary', {}).get('total', 0)
        passed_tests = test_results.get('summary', {}).get('passed', 0)
        failed_tests = test_results.get('summary', {}).get('failed', 0)
        
        if total_tests == 0:
            status = "warning"
            score = 50.0  # 没有测试
        elif failed_tests == 0:
            status = "success"
            score = 100.0
        else:
            status = "error"
            score = max(30.0, (passed_tests / total_tests) * 100)
        
        return QualityResult(
            tool="pytest",
            status=status,
            score=score,
            issues=[],
            output=stdout,
            error=stderr,
            execution_time=time.time() - start_time
        )
    
    def run_all_checks(self) -> List[QualityResult]:
        """运行所有检查"""
        print("🔍 开始代码质量检查...")
        
        checks = [
            ("代码格式化", self.check_black),
            ("导入排序", self.check_isort),
            ("代码风格", self.check_flake8),
            ("类型检查", self.check_mypy),
            ("安全检查", self.check_bandit),
            ("单元测试", self.check_pytest)
        ]
        
        for name, check_func in checks:
            print(f"  ⏳ 检查 {name}...")
            result = check_func()
            self.results.append(result)
            
            # 显示结果
            if result.status == "success":
                print(f"  ✅ {name}: 通过 (分数: {result.score:.1f})")
            elif result.status == "warning":
                print(f"  ⚠️  {name}: 警告 (分数: {result.score:.1f})")
            elif result.status == "error":
                print(f"  ❌ {name}: 错误 (分数: {result.score:.1f})")
            else:
                print(f"  ⏭️  {name}: 跳过 ({result.error})")
        
        return self.results
    
    def generate_report(self) -> Dict[str, Any]:
        """生成报告"""
        total_score = 0.0
        valid_scores = 0
        
        for result in self.results:
            if result.score is not None:
                total_score += result.score
                valid_scores += 1
        
        average_score = total_score / valid_scores if valid_scores > 0 else 0.0
        
        # 确定总体状态
        if average_score >= 90:
            overall_status = "excellent"
        elif average_score >= 80:
            overall_status = "good"
        elif average_score >= 70:
            overall_status = "fair"
        else:
            overall_status = "poor"
        
        return {
            "timestamp": datetime.now().isoformat(),
            "overall_score": average_score,
            "overall_status": overall_status,
            "total_checks": len(self.results),
            "passed_checks": len([r for r in self.results if r.status == "success"]),
            "warning_checks": len([r for r in self.results if r.status == "warning"]),
            "failed_checks": len([r for r in self.results if r.status == "error"]),
            "skipped_checks": len([r for r in self.results if r.status == "skipped"]),
            "results": [
                {
                    "tool": r.tool,
                    "status": r.status,
                    "score": r.score,
                    "execution_time": r.execution_time,
                    "issues_count": len(r.issues) if r.issues else 0,
                    "error": r.error if r.error else None
                }
                for r in self.results
            ]
        }
    
    def save_report(self, report: Dict[str, Any], output_file: Path):
        """保存报告"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"📊 报告已保存到: {output_file}")


def install_pre_commit_hooks():
    """安装 pre-commit 钩子"""
    print("🔧 安装 pre-commit 钩子...")
    
    try:
        # 检查 pre-commit 是否已安装
        result = subprocess.run(
            ["pre-commit", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            print("📦 安装 pre-commit...")
            subprocess.run(["pip", "install", "pre-commit"], check=True)
        
        # 安装钩子
        subprocess.run(["pre-commit", "install"], check=True)
        subprocess.run(["pre-commit", "install", "--hook-type", "commit-msg"], check=True)
        
        print("✅ Pre-commit 钩子安装成功！")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Pre-commit 钩子安装失败: {e}")
        return False
    except Exception as e:
        print(f"💥 安装过程中发生错误: {e}")
        return False


def run_pre_commit_hooks():
    """运行 pre-commit 钩子"""
    print("🚀 运行 pre-commit 钩子...")
    
    try:
        result = subprocess.run(
            ["pre-commit", "run", "--all-files"],
            capture_output=True,
            text=True,
            check=False
        )
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ 所有 pre-commit 钩子检查通过！")
            return True
        else:
            print("❌ Pre-commit 钩子检查发现问题。")
            return False
            
    except FileNotFoundError:
        print("❌ Pre-commit 未安装，请先运行 --install-hooks")
        return False
    except Exception as e:
        print(f"💥 运行钩子时发生错误: {e}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="ChatExcel MCP 项目代码质量检查工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python scripts/code_quality_enhanced.py --fix --report
    python scripts/code_quality_enhanced.py --exclude tests/ --config custom.ini
    python scripts/code_quality_enhanced.py --install-hooks
    python scripts/code_quality_enhanced.py --run-hooks
        """
    )
    
    parser.add_argument(
        "--fix", 
        action="store_true", 
        help="自动修复可修复的问题"
    )
    parser.add_argument(
        "--report", 
        action="store_true", 
        help="生成详细的质量报告"
    )
    parser.add_argument(
        "--config", 
        type=str, 
        help="指定配置文件路径"
    )
    parser.add_argument(
        "--exclude", 
        type=str, 
        nargs="*", 
        default=["build/", "dist/", ".venv/", "__pycache__/"],
        help="排除的目录或文件模式"
    )
    parser.add_argument(
        "--install-hooks",
        action="store_true",
        help="安装 pre-commit 钩子"
    )
    parser.add_argument(
        "--run-hooks",
        action="store_true",
        help="运行 pre-commit 钩子"
    )
    
    args = parser.parse_args()
    
    # 处理 pre-commit 相关操作
    if args.install_hooks:
        success = install_pre_commit_hooks()
        sys.exit(0 if success else 1)
    
    if args.run_hooks:
        success = run_pre_commit_hooks()
        sys.exit(0 if success else 1)
    
    # 原有的代码质量检查逻辑
    project_root = Path(__file__).parent.parent
    checker = CodeQualityChecker(project_root)
    
    # 运行检查
    results = checker.run_all_checks()
    
    # 生成报告
    report = checker.generate_report()
    
    # 保存报告
    reports_dir = project_root / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = reports_dir / f"code_quality_{timestamp}.json"
    checker.save_report(report, report_file)
    
    # 显示总结
    print("\n" + "="*50)
    print("📋 代码质量检查总结")
    print("="*50)
    print(f"总体分数: {report['overall_score']:.1f}/100")
    print(f"总体状态: {report['overall_status']}")
    print(f"通过检查: {report['passed_checks']}/{report['total_checks']}")
    
    if report['warning_checks'] > 0:
        print(f"警告检查: {report['warning_checks']}")
    if report['failed_checks'] > 0:
        print(f"失败检查: {report['failed_checks']}")
    if report['skipped_checks'] > 0:
        print(f"跳过检查: {report['skipped_checks']}")
    
    # 提示用户可以安装 pre-commit 钩子
    if report['overall_score'] >= 80:
        print("\n💡 提示: 可以运行 'python scripts/code_quality_enhanced.py --install-hooks' 安装 pre-commit 钩子")
    
    # 返回适当的退出码
    if report['failed_checks'] > 0:
        sys.exit(1)
    elif report['warning_checks'] > 0:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()