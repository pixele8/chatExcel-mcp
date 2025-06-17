#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化套件
整合所有强化工具，提供统一的执行入口和自动化流程
"""

import json
import sys
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging
import time

class AutomationSuite:
    """自动化套件主类"""
    
    def __init__(self, project_root: str):
        """初始化自动化套件
        
        Args:
            project_root: 项目根目录
        """
        self.project_root = Path(project_root)
        self.scripts_dir = self.project_root / "scripts"
        self.reports_dir = self.project_root / "reports"
        self.reports_dir.mkdir(exist_ok=True)
        
        # 设置日志
        self._setup_logging()
        
        # 可用的工具脚本
        self.available_tools = {
            'dependency_audit': {
                'script': 'dependency_audit.py',
                'description': '依赖审计和清理',
                'category': 'dependency'
            },
            'security_enhancer': {
                'script': 'security_enhancer.py',
                'description': '安全强化扫描',
                'category': 'security'
            },
            'structure_optimizer': {
                'script': 'structure_optimizer.py',
                'description': '项目结构优化',
                'category': 'structure'
            },
            'enhanced_monitor': {
                'script': 'enhanced_monitor.py',
                'description': '增强监控系统',
                'category': 'monitoring'
            }
        }
        
        # 预定义的执行套件
        self.execution_suites = {
            'full_audit': {
                'name': '完整审计',
                'description': '执行完整的项目审计和优化',
                'tools': ['dependency_audit', 'security_enhancer', 'structure_optimizer'],
                'parallel': False
            },
            'security_check': {
                'name': '安全检查',
                'description': '专注于安全相关的检查和强化',
                'tools': ['dependency_audit', 'security_enhancer'],
                'parallel': True
            },
            'maintenance': {
                'name': '维护优化',
                'description': '项目维护和结构优化',
                'tools': ['structure_optimizer', 'dependency_audit'],
                'parallel': False
            },
            'monitoring_setup': {
                'name': '监控设置',
                'description': '设置和启动监控系统',
                'tools': ['enhanced_monitor'],
                'parallel': False
            }
        }
        
    def _setup_logging(self):
        """设置日志系统"""
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "automation_suite.log"),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("AutomationSuite")
        
    def list_available_tools(self):
        """列出可用的工具"""
        print("\n🛠️ 可用工具:")
        
        categories = {}
        for tool_name, tool_info in self.available_tools.items():
            category = tool_info['category']
            if category not in categories:
                categories[category] = []
            categories[category].append((tool_name, tool_info))
            
        for category, tools in categories.items():
            print(f"\n📂 {category.upper()}:")
            for tool_name, tool_info in tools:
                print(f"  - {tool_name}: {tool_info['description']}")
                
    def list_execution_suites(self):
        """列出执行套件"""
        print("\n📦 执行套件:")
        
        for suite_name, suite_info in self.execution_suites.items():
            print(f"\n🎯 {suite_name}: {suite_info['name']}")
            print(f"   描述: {suite_info['description']}")
            print(f"   工具: {', '.join(suite_info['tools'])}")
            print(f"   并行执行: {'是' if suite_info['parallel'] else '否'}")
            
    def validate_tool(self, tool_name: str) -> bool:
        """验证工具是否可用
        
        Args:
            tool_name: 工具名称
            
        Returns:
            是否可用
        """
        if tool_name not in self.available_tools:
            self.logger.error(f"未知工具: {tool_name}")
            return False
            
        script_path = self.scripts_dir / self.available_tools[tool_name]['script']
        if not script_path.exists():
            self.logger.error(f"工具脚本不存在: {script_path}")
            return False
            
        return True
        
    def execute_tool(self, tool_name: str, args: List[str] = None) -> Dict:
        """执行单个工具
        
        Args:
            tool_name: 工具名称
            args: 额外参数
            
        Returns:
            执行结果
        """
        if not self.validate_tool(tool_name):
            return {
                'success': False,
                'error': f'工具验证失败: {tool_name}'
            }
            
        script_path = self.scripts_dir / self.available_tools[tool_name]['script']
        
        self.logger.info(f"执行工具: {tool_name}")
        print(f"\n🚀 执行 {tool_name}...")
        
        try:
            # 构建命令
            cmd = [sys.executable, str(script_path)]
            if args:
                cmd.extend(args)
                
            # 执行命令
            start_time = time.time()
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=600  # 10分钟超时
            )
            
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                self.logger.info(f"工具 {tool_name} 执行成功，耗时 {execution_time:.2f}秒")
                print(f"✅ {tool_name} 执行成功")
                
                return {
                    'success': True,
                    'tool_name': tool_name,
                    'execution_time': execution_time,
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }
            else:
                self.logger.error(f"工具 {tool_name} 执行失败，返回码: {result.returncode}")
                print(f"❌ {tool_name} 执行失败")
                
                return {
                    'success': False,
                    'tool_name': tool_name,
                    'execution_time': execution_time,
                    'return_code': result.returncode,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'error': f'执行失败，返回码: {result.returncode}'
                }
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"工具 {tool_name} 执行超时")
            print(f"⏰ {tool_name} 执行超时")
            
            return {
                'success': False,
                'tool_name': tool_name,
                'error': '执行超时'
            }
            
        except Exception as e:
            self.logger.error(f"工具 {tool_name} 执行异常: {e}")
            print(f"💥 {tool_name} 执行异常: {e}")
            
            return {
                'success': False,
                'tool_name': tool_name,
                'error': str(e)
            }
            
    def execute_suite(self, suite_name: str) -> Dict:
        """执行工具套件
        
        Args:
            suite_name: 套件名称
            
        Returns:
            执行结果
        """
        if suite_name not in self.execution_suites:
            return {
                'success': False,
                'error': f'未知套件: {suite_name}'
            }
            
        suite_info = self.execution_suites[suite_name]
        tools = suite_info['tools']
        parallel = suite_info['parallel']
        
        self.logger.info(f"执行套件: {suite_name} ({suite_info['name']})")
        print(f"\n🎯 执行套件: {suite_info['name']}")
        print(f"📝 描述: {suite_info['description']}")
        print(f"🛠️ 工具: {', '.join(tools)}")
        print(f"⚡ 并行执行: {'是' if parallel else '否'}")
        
        start_time = time.time()
        results = []
        
        if parallel:
            # 并行执行（简化版，实际可以使用threading或multiprocessing）
            print("\n⚡ 并行执行模式")
            for tool_name in tools:
                result = self.execute_tool(tool_name)
                results.append(result)
        else:
            # 顺序执行
            print("\n📋 顺序执行模式")
            for i, tool_name in enumerate(tools, 1):
                print(f"\n[{i}/{len(tools)}] 执行 {tool_name}")
                result = self.execute_tool(tool_name)
                results.append(result)
                
                # 如果工具执行失败，询问是否继续
                if not result['success']:
                    print(f"\n⚠️ 工具 {tool_name} 执行失败")
                    print(f"错误: {result.get('error', '未知错误')}")
                    
                    if i < len(tools):
                        response = input("是否继续执行剩余工具？(y/N): ").strip().lower()
                        if response not in ['y', 'yes']:
                            print("🛑 用户选择停止执行")
                            break
                            
        total_time = time.time() - start_time
        
        # 统计结果
        successful_tools = [r for r in results if r['success']]
        failed_tools = [r for r in results if not r['success']]
        
        suite_result = {
            'success': len(failed_tools) == 0,
            'suite_name': suite_name,
            'suite_info': suite_info,
            'total_time': total_time,
            'total_tools': len(tools),
            'successful_tools': len(successful_tools),
            'failed_tools': len(failed_tools),
            'results': results
        }
        
        # 打印摘要
        print(f"\n📊 套件执行摘要:")
        print(f"- 总耗时: {total_time:.2f}秒")
        print(f"- 成功工具: {len(successful_tools)}/{len(tools)}")
        print(f"- 失败工具: {len(failed_tools)}/{len(tools)}")
        
        if failed_tools:
            print(f"\n❌ 失败的工具:")
            for result in failed_tools:
                print(f"  - {result['tool_name']}: {result.get('error', '未知错误')}")
                
        if successful_tools:
            print(f"\n✅ 成功的工具:")
            for result in successful_tools:
                exec_time = result.get('execution_time', 0)
                print(f"  - {result['tool_name']}: {exec_time:.2f}秒")
                
        return suite_result
        
    def generate_execution_report(self, results: List[Dict]) -> str:
        """生成执行报告
        
        Args:
            results: 执行结果列表
            
        Returns:
            报告内容
        """
        report = f"""
# 自动化执行报告

生成时间: {datetime.now().isoformat()}

## 执行概览

"""
        
        total_executions = len(results)
        successful_executions = len([r for r in results if r.get('success', False)])
        failed_executions = total_executions - successful_executions
        
        report += f"""
- 总执行次数: {total_executions}
- 成功执行: {successful_executions}
- 失败执行: {failed_executions}
- 成功率: {(successful_executions/total_executions*100):.1f}%

## 详细结果

"""
        
        for i, result in enumerate(results, 1):
            status_emoji = "✅" if result.get('success', False) else "❌"
            
            if 'suite_name' in result:
                # 套件执行结果
                report += f"""
### {i}. {status_emoji} 套件: {result['suite_name']}

- **名称**: {result['suite_info']['name']}
- **描述**: {result['suite_info']['description']}
- **总耗时**: {result.get('total_time', 0):.2f}秒
- **成功工具**: {result.get('successful_tools', 0)}/{result.get('total_tools', 0)}
- **失败工具**: {result.get('failed_tools', 0)}/{result.get('total_tools', 0)}

#### 工具执行详情

"""
                
                for tool_result in result.get('results', []):
                    tool_status = "✅" if tool_result['success'] else "❌"
                    exec_time = tool_result.get('execution_time', 0)
                    
                    report += f"- {tool_status} **{tool_result['tool_name']}**: {exec_time:.2f}秒\n"
                    
                    if not tool_result['success']:
                        error = tool_result.get('error', '未知错误')
                        report += f"  - 错误: {error}\n"
                        
            else:
                # 单个工具执行结果
                tool_name = result.get('tool_name', '未知工具')
                exec_time = result.get('execution_time', 0)
                
                report += f"""
### {i}. {status_emoji} 工具: {tool_name}

- **执行时间**: {exec_time:.2f}秒
"""
                
                if not result.get('success', False):
                    error = result.get('error', '未知错误')
                    report += f"- **错误**: {error}\n"
                    
                    if 'stderr' in result and result['stderr']:
                        report += f"- **错误输出**: \n```\n{result['stderr']}\n```\n"
                        
            report += "\n"
            
        return report
        
    def save_execution_report(self, results: List[Dict], output_file: str = None):
        """保存执行报告
        
        Args:
            results: 执行结果列表
            output_file: 输出文件路径
        """
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.reports_dir / f"automation_report_{timestamp}.md"
            
        report = self.generate_execution_report(results)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
            
        self.logger.info(f"执行报告已保存到: {output_file}")
        print(f"📊 执行报告已保存到: {output_file}")
        
        # 同时保存JSON格式的详细数据
        json_file = str(output_file).replace('.md', '.json')
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
            
        self.logger.info(f"详细数据已保存到: {json_file}")
        print(f"📊 详细数据已保存到: {json_file}")
        
    def interactive_mode(self):
        """交互模式"""
        print("\n🎮 进入交互模式")
        print("输入 'help' 查看可用命令")
        
        while True:
            try:
                command = input("\n> ").strip()
                
                if not command:
                    continue
                    
                if command.lower() in ['exit', 'quit', 'q']:
                    print("👋 退出交互模式")
                    break
                    
                elif command.lower() == 'help':
                    self._show_interactive_help()
                    
                elif command.lower() == 'list-tools':
                    self.list_available_tools()
                    
                elif command.lower() == 'list-suites':
                    self.list_execution_suites()
                    
                elif command.startswith('run-tool '):
                    tool_name = command[9:].strip()
                    if tool_name:
                        result = self.execute_tool(tool_name)
                        self.save_execution_report([result])
                    else:
                        print("❌ 请指定工具名称")
                        
                elif command.startswith('run-suite '):
                    suite_name = command[10:].strip()
                    if suite_name:
                        result = self.execute_suite(suite_name)
                        self.save_execution_report([result])
                    else:
                        print("❌ 请指定套件名称")
                        
                else:
                    print(f"❌ 未知命令: {command}")
                    print("输入 'help' 查看可用命令")
                    
            except KeyboardInterrupt:
                print("\n👋 退出交互模式")
                break
            except Exception as e:
                print(f"❌ 命令执行出错: {e}")
                
    def _show_interactive_help(self):
        """显示交互模式帮助"""
        print("""
📖 可用命令:

🛠️ 工具管理:
  list-tools          - 列出所有可用工具
  run-tool <name>     - 执行指定工具

📦 套件管理:
  list-suites         - 列出所有执行套件
  run-suite <name>    - 执行指定套件

📊 其他:
  help               - 显示此帮助信息
  exit/quit/q        - 退出交互模式

示例:
  run-tool dependency_audit
  run-suite full_audit
""")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="ChatExcel MCP 项目自动化套件",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--project-root',
        default='.',
        help='项目根目录路径（默认: 当前目录）'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 列出工具命令
    subparsers.add_parser('list-tools', help='列出所有可用工具')
    
    # 列出套件命令
    subparsers.add_parser('list-suites', help='列出所有执行套件')
    
    # 执行工具命令
    tool_parser = subparsers.add_parser('run-tool', help='执行指定工具')
    tool_parser.add_argument('tool_name', help='工具名称')
    tool_parser.add_argument('--args', nargs='*', help='额外参数')
    
    # 执行套件命令
    suite_parser = subparsers.add_parser('run-suite', help='执行指定套件')
    suite_parser.add_argument('suite_name', help='套件名称')
    
    # 交互模式命令
    subparsers.add_parser('interactive', help='进入交互模式')
    
    args = parser.parse_args()
    
    # 初始化自动化套件
    suite = AutomationSuite(args.project_root)
    
    if args.command == 'list-tools':
        suite.list_available_tools()
        
    elif args.command == 'list-suites':
        suite.list_execution_suites()
        
    elif args.command == 'run-tool':
        result = suite.execute_tool(args.tool_name, args.args)
        suite.save_execution_report([result])
        
    elif args.command == 'run-suite':
        result = suite.execute_suite(args.suite_name)
        suite.save_execution_report([result])
        
    elif args.command == 'interactive':
        suite.interactive_mode()
        
    else:
        # 默认显示帮助和进入交互模式
        print("🚀 ChatExcel MCP 项目自动化套件")
        print("\n使用 --help 查看详细帮助信息")
        
        suite.list_available_tools()
        suite.list_execution_suites()
        
        print("\n💡 提示: 使用 'python automation_suite.py interactive' 进入交互模式")
        
if __name__ == "__main__":
    main()