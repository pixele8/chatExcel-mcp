#!/usr/bin/env python3
"""
ChatExcel MCP 项目快速增强脚本

这个脚本提供了一个简化的入口点来快速运行所有包和依赖管理增强工具的基本功能。
适合日常维护和快速检查使用。

作者: AI Assistant
创建时间: 2024
"""

import os
import sys
import subprocess
import argparse
import json
from datetime import datetime
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class QuickEnhancer:
    """快速增强工具类"""
    
    def __init__(self):
        """初始化快速增强工具"""
        self.project_root = project_root
        self.scripts_dir = self.project_root / "scripts"
        self.reports_dir = self.project_root / "reports" / "quick"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # 工具映射
        self.tools = {
            'dependency': 'dependency_audit.py',
            'security': 'security_enhancer.py',
            'structure': 'structure_optimizer.py',
            'monitor': 'enhanced_monitor.py',
            'config': 'config_optimizer.py'
        }
        
        self.results = {}
    
    def run_tool(self, tool_name, action='--help'):
        """运行指定工具
        
        Args:
            tool_name (str): 工具名称
            action (str): 执行的动作
            
        Returns:
            dict: 执行结果
        """
        if tool_name not in self.tools:
            return {'success': False, 'error': f'未知工具: {tool_name}'}
        
        script_path = self.scripts_dir / self.tools[tool_name]
        if not script_path.exists():
            return {'success': False, 'error': f'脚本不存在: {script_path}'}
        
        try:
            cmd = [sys.executable, str(script_path), action]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5分钟超时
                cwd=str(self.project_root)
            )
            
            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'command': ' '.join(cmd)
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': '执行超时'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def quick_check(self):
        """快速检查所有工具
        
        Returns:
            dict: 检查结果
        """
        print("🚀 开始快速检查...")
        
        checks = {
            'dependency': '依赖审计',
            'security': '安全扫描',
            'structure': '结构分析',
            'config': '配置检查'
        }
        
        results = {}
        
        for tool, description in checks.items():
            print(f"\n📋 正在执行 {description}...")
            
            # 根据工具类型选择合适的参数
            if tool == 'dependency':
                result = self.run_tool(tool, '--analyze')
            elif tool == 'security':
                result = self.run_tool(tool, '--scan')
            elif tool == 'structure':
                result = self.run_tool(tool, '--analyze')
            elif tool == 'config':
                result = self.run_tool(tool, '--analyze')
            else:
                result = self.run_tool(tool, '--help')
            
            results[tool] = {
                'description': description,
                'result': result,
                'timestamp': datetime.now().isoformat()
            }
            
            if result['success']:
                print(f"✅ {description} 完成")
            else:
                print(f"❌ {description} 失败: {result.get('error', '未知错误')}")
        
        self.results['quick_check'] = results
        return results
    
    def quick_fix(self):
        """快速修复常见问题
        
        Returns:
            dict: 修复结果
        """
        print("🔧 开始快速修复...")
        
        fixes = {
            'security': ('安全修复', '--fix'),
            'structure': ('结构优化', '--optimize')
        }
        
        results = {}
        
        for tool, (description, action) in fixes.items():
            print(f"\n🛠️ 正在执行 {description}...")
            
            result = self.run_tool(tool, action)
            
            results[tool] = {
                'description': description,
                'result': result,
                'timestamp': datetime.now().isoformat()
            }
            
            if result['success']:
                print(f"✅ {description} 完成")
            else:
                print(f"❌ {description} 失败: {result.get('error', '未知错误')}")
        
        self.results['quick_fix'] = results
        return results
    
    def monitor_status(self):
        """检查监控状态
        
        Returns:
            dict: 监控状态
        """
        print("📊 检查监控状态...")
        
        result = self.run_tool('monitor', '--status')
        
        self.results['monitor_status'] = {
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
        
        if result['success']:
            print("✅ 监控状态检查完成")
        else:
            print(f"❌ 监控状态检查失败: {result.get('error', '未知错误')}")
        
        return result
    
    def generate_summary_report(self):
        """生成汇总报告
        
        Returns:
            str: 报告文件路径
        """
        # 确保报告目录存在
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"quick_enhancement_report_{timestamp}.md"
        
        try:
            # 生成 Markdown 报告
            report_content = self._generate_markdown_report()
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            # 生成 JSON 报告
            json_file = self.reports_dir / f"quick_enhancement_report_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            
            print(f"\n📄 报告已生成:")
            print(f"   Markdown: {report_file}")
            print(f"   JSON: {json_file}")
            
            return str(report_file)
        except Exception as e:
            print(f"❌ 报告生成失败: {e}")
            # 创建一个简单的报告
            simple_report = f"# 快速增强报告\n\n生成时间: {datetime.now()}\n\n执行结果:\n{json.dumps(self.results, indent=2, ensure_ascii=False)}"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(simple_report)
            return str(report_file)
    
    def _generate_markdown_report(self):
        """生成 Markdown 格式的报告
        
        Returns:
            str: Markdown 内容
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        content = f"""# ChatExcel MCP 快速增强报告

**生成时间:** {timestamp}
**项目路径:** {self.project_root}

## 执行摘要

"""
        
        # 统计成功和失败的任务
        total_tasks = 0
        successful_tasks = 0
        
        for section_name, section_data in self.results.items():
            if isinstance(section_data, dict):
                if 'result' in section_data:  # 单个任务
                    total_tasks += 1
                    if section_data['result'].get('success', False):
                        successful_tasks += 1
                else:  # 多个任务
                    for task_name, task_data in section_data.items():
                        if isinstance(task_data, dict) and 'result' in task_data:
                            total_tasks += 1
                            if task_data['result'].get('success', False):
                                successful_tasks += 1
        
        success_rate = (successful_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        content += f"- **总任务数:** {total_tasks}\n"
        content += f"- **成功任务:** {successful_tasks}\n"
        content += f"- **失败任务:** {total_tasks - successful_tasks}\n"
        content += f"- **成功率:** {success_rate:.1f}%\n\n"
        
        # 详细结果
        for section_name, section_data in self.results.items():
            content += f"## {section_name.replace('_', ' ').title()}\n\n"
            
            if isinstance(section_data, dict):
                if 'result' in section_data:  # 单个任务
                    content += self._format_task_result(section_name, section_data)
                else:  # 多个任务
                    for task_name, task_data in section_data.items():
                        if isinstance(task_data, dict):
                            content += self._format_task_result(task_name, task_data)
            
            content += "\n"
        
        # 建议和后续步骤
        content += "## 建议和后续步骤\n\n"
        
        if successful_tasks < total_tasks:
            content += "### ⚠️ 需要关注的问题\n\n"
            for section_name, section_data in self.results.items():
                if isinstance(section_data, dict):
                    if 'result' in section_data and not section_data['result'].get('success', False):
                        content += f"- **{section_name}:** {section_data['result'].get('error', '执行失败')}\n"
                    else:
                        for task_name, task_data in section_data.items():
                            if isinstance(task_data, dict) and 'result' in task_data:
                                if not task_data['result'].get('success', False):
                                    content += f"- **{task_name}:** {task_data['result'].get('error', '执行失败')}\n"
            content += "\n"
        
        content += "### 📋 建议的后续操作\n\n"
        content += "1. 查看详细的工具输出日志\n"
        content += "2. 对失败的任务进行手动检查\n"
        content += "3. 根据报告结果调整项目配置\n"
        content += "4. 定期运行快速检查以保持项目健康\n\n"
        
        content += "### 🔗 相关文档\n\n"
        content += "- [完整增强指南](../PACKAGE_MANAGEMENT_ENHANCEMENT_GUIDE.md)\n"
        content += "- [项目文档](../README.md)\n"
        content += "- [变更日志](../CHANGELOG.md)\n"
        
        return content
    
    def _format_task_result(self, task_name, task_data):
        """格式化任务结果
        
        Args:
            task_name (str): 任务名称
            task_data (dict): 任务数据
            
        Returns:
            str: 格式化的结果
        """
        result = task_data.get('result', {})
        description = task_data.get('description', task_name)
        timestamp = task_data.get('timestamp', 'N/A')
        
        status = "✅ 成功" if result.get('success', False) else "❌ 失败"
        
        content = f"### {description}\n\n"
        content += f"- **状态:** {status}\n"
        content += f"- **时间:** {timestamp}\n"
        
        if not result.get('success', False):
            error = result.get('error', '未知错误')
            content += f"- **错误:** {error}\n"
        
        if result.get('stdout'):
            content += f"\n**输出:**\n```\n{result['stdout'][:500]}\n```\n"
        
        if result.get('stderr') and not result.get('success', False):
            content += f"\n**错误输出:**\n```\n{result['stderr'][:500]}\n```\n"
        
        return content + "\n"

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='ChatExcel MCP 项目快速增强工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python3 scripts/quick_enhancement.py --check          # 快速检查
  python3 scripts/quick_enhancement.py --fix            # 快速修复
  python3 scripts/quick_enhancement.py --all            # 检查和修复
  python3 scripts/quick_enhancement.py --monitor        # 检查监控状态
  python3 scripts/quick_enhancement.py --report         # 仅生成报告
        """
    )
    
    parser.add_argument('--check', action='store_true',
                       help='执行快速检查')
    parser.add_argument('--fix', action='store_true',
                       help='执行快速修复')
    parser.add_argument('--all', action='store_true',
                       help='执行检查和修复')
    parser.add_argument('--monitor', action='store_true',
                       help='检查监控状态')
    parser.add_argument('--report', action='store_true',
                       help='仅生成报告（基于之前的结果）')
    parser.add_argument('--version', action='version', version='1.0.0')
    
    args = parser.parse_args()
    
    # 如果没有指定参数，显示帮助
    if not any([args.check, args.fix, args.all, args.monitor, args.report]):
        parser.print_help()
        return
    
    enhancer = QuickEnhancer()
    
    print("🎯 ChatExcel MCP 快速增强工具")
    print(f"📁 项目路径: {enhancer.project_root}")
    print("=" * 50)
    
    try:
        if args.all or args.check:
            enhancer.quick_check()
        
        if args.all or args.fix:
            enhancer.quick_fix()
        
        if args.monitor:
            enhancer.monitor_status()
        
        # 生成报告
        if enhancer.results:  # 只有在有结果时才生成报告
            report_file = enhancer.generate_summary_report()
            print(f"\n🎉 快速增强完成！查看报告: {report_file}")
        elif args.report:
            print("⚠️ 没有可用的结果数据来生成报告。请先运行检查或修复操作。")
        
    except KeyboardInterrupt:
        print("\n⚠️ 操作被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 执行过程中发生错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()