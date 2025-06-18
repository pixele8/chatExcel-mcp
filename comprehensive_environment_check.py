#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面虚拟环境和MCP工具功能检查
验证所有31个MCP工具在当前环境中的完整功能支持
"""

import sys
import os
import importlib
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import traceback

# 添加项目路径
project_path = '/Users/wangdada/Downloads/mcp/chatExcel-mcp'
sys.path.insert(0, project_path)
os.chdir(project_path)

class EnvironmentChecker:
    """环境检查器类"""
    
    def __init__(self):
        self.results = {
            'environment': {},
            'dependencies': {},
            'mcp_tools': {},
            'functionality': {},
            'summary': {}
        }
        
        # 31个MCP工具列表
        self.mcp_tools = [
            'read_metadata', 'verify_data_integrity', 'read_excel_metadata',
            'run_excel_code', 'run_code', 'bar_chart_to_html', 'pie_chart_to_html',
            'line_chart_to_html', 'validate_data_quality', 'suggest_excel_read_parameters_tool',
            'detect_excel_file_structure_tool', 'create_excel_read_template_tool',
            'comprehensive_data_verification_tool', 'batch_data_verification_tool',
            'excel_read_enhanced', 'excel_write_enhanced', 'excel_chart_enhanced',
            'excel_info_enhanced', 'excel_performance_comparison', 'parse_formula',
            'compile_workbook', 'execute_formula', 'analyze_dependencies',
            'validate_formula', 'enhanced_data_quality_check', 'extract_cell_content_advanced',
            'convert_character_formats', 'extract_multi_condition_data',
            'merge_multiple_tables', 'clean_excel_data', 'batch_process_excel_files'
        ]
        
        # 关键依赖库
        self.critical_dependencies = {
            'pandas': '数据处理核心库',
            'numpy': '数值计算库',
            'openpyxl': 'Excel文件处理',
            'matplotlib': '基础绘图库',
            'seaborn': '统计绘图库',
            'plotly': '交互式图表库',
            'tabulate': '表格格式化',
            'formulas': 'Excel公式处理',
            'chardet': '字符编码检测',
            'fastmcp': 'MCP框架',
            'xlsxwriter': 'Excel写入库',
            'scipy': '科学计算库',
            'sklearn': '机器学习库',  # 修正：使用sklearn而不是scikit-learn
            'requests': 'HTTP请求库',
            'lxml': 'XML处理库'
        }
    
    def check_environment(self) -> Dict[str, Any]:
        """检查Python环境"""
        print("🔍 检查Python环境...")
        
        env_info = {
            'python_version': sys.version,
            'python_executable': sys.executable,
            'platform': sys.platform,
            'is_virtual_env': False,
            'virtual_env_path': None,
            'working_directory': os.getcwd(),
            'python_path': sys.path[:5]  # 只显示前5个路径
        }
        
        # 检查虚拟环境
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            env_info['is_virtual_env'] = True
            env_info['virtual_env_path'] = sys.prefix
        elif 'venv' in sys.executable or 'virtualenv' in sys.executable:
            env_info['is_virtual_env'] = True
            env_info['virtual_env_path'] = sys.executable
        
        self.results['environment'] = env_info
        
        print(f"✅ Python版本: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        print(f"{'✅' if env_info['is_virtual_env'] else '⚠️'} 虚拟环境: {'是' if env_info['is_virtual_env'] else '否'}")
        
        return env_info
    
    def check_dependencies(self) -> Dict[str, Any]:
        """检查依赖库"""
        print("\n📦 检查依赖库...")
        
        dep_results = {
            'installed': {},
            'missing': [],
            'versions': {},
            'total_checked': len(self.critical_dependencies),
            'installed_count': 0
        }
        
        for package, description in self.critical_dependencies.items():
            try:
                module = importlib.import_module(package)
                version = getattr(module, '__version__', 'unknown')
                dep_results['installed'][package] = {
                    'version': version,
                    'description': description,
                    'status': 'ok'
                }
                dep_results['installed_count'] += 1
                print(f"✅ {package} ({version}) - {description}")
            except ImportError as e:
                dep_results['missing'].append({
                    'package': package,
                    'description': description,
                    'error': str(e)
                })
                print(f"❌ {package} - 缺失: {description}")
            except Exception as e:
                dep_results['installed'][package] = {
                    'version': 'error',
                    'description': description,
                    'status': 'error',
                    'error': str(e)
                }
                print(f"⚠️ {package} - 错误: {str(e)}")
        
        self.results['dependencies'] = dep_results
        return dep_results
    
    def check_mcp_tools(self) -> Dict[str, Any]:
        """检查MCP工具"""
        print("\n🛠️ 检查MCP工具...")
        
        tool_results = {
            'available': {},
            'unavailable': [],
            'total_tools': len(self.mcp_tools),
            'available_count': 0,
            'server_import_status': False
        }
        
        # 尝试导入server模块
        try:
            import server
            tool_results['server_import_status'] = True
            print("✅ server.py导入成功")
            
            # 检查每个工具
            for tool_name in self.mcp_tools:
                try:
                    if hasattr(server, tool_name):
                        func = getattr(server, tool_name)
                        if callable(func):
                            tool_results['available'][tool_name] = {
                                'status': 'ok',
                                'callable': True,
                                'docstring': func.__doc__[:100] if func.__doc__ else 'No docstring'
                            }
                            tool_results['available_count'] += 1
                            print(f"✅ {tool_name} - 可用")
                        else:
                            tool_results['unavailable'].append({
                                'tool': tool_name,
                                'reason': 'not_callable',
                                'error': 'Function exists but not callable'
                            })
                            print(f"❌ {tool_name} - 不可调用")
                    else:
                        tool_results['unavailable'].append({
                            'tool': tool_name,
                            'reason': 'not_found',
                            'error': 'Function not found in server module'
                        })
                        print(f"❌ {tool_name} - 未找到")
                except Exception as e:
                    tool_results['unavailable'].append({
                        'tool': tool_name,
                        'reason': 'error',
                        'error': str(e)
                    })
                    print(f"❌ {tool_name} - 错误: {str(e)}")
                    
        except Exception as e:
            tool_results['server_import_error'] = str(e)
            print(f"❌ server.py导入失败: {e}")
            
            # 如果server导入失败，标记所有工具为不可用
            for tool_name in self.mcp_tools:
                tool_results['unavailable'].append({
                    'tool': tool_name,
                    'reason': 'server_import_failed',
                    'error': f'Server import failed: {str(e)}'
                })
        
        self.results['mcp_tools'] = tool_results
        return tool_results
    
    def check_functionality(self) -> Dict[str, Any]:
        """检查功能完整性"""
        print("\n🧪 检查功能完整性...")
        
        func_results = {
            'core_modules': {},
            'file_access': {},
            'chart_generation': {},
            'formula_processing': {},
            'data_quality': {}
        }
        
        # 检查核心模块
        core_modules = [
            'column_checker', 'excel_helper', 'excel_smart_tools',
            'enhanced_excel_helper', 'comprehensive_data_verification',
            'data_verification', 'excel_enhanced_tools', 'formulas_tools',
            'excel_data_quality_tools'
        ]
        
        for module_name in core_modules:
            try:
                module = importlib.import_module(module_name)
                func_results['core_modules'][module_name] = {
                    'status': 'ok',
                    'path': getattr(module, '__file__', 'unknown')
                }
                print(f"✅ {module_name} - 模块可用")
            except Exception as e:
                func_results['core_modules'][module_name] = {
                    'status': 'error',
                    'error': str(e)
                }
                print(f"❌ {module_name} - 模块错误: {str(e)}")
        
        # 检查文件访问
        test_dirs = ['templates', 'charts', 'test']
        for dir_name in test_dirs:
            dir_path = Path(dir_name)
            func_results['file_access'][dir_name] = {
                'exists': dir_path.exists(),
                'readable': dir_path.exists() and os.access(dir_path, os.R_OK),
                'writable': dir_path.exists() and os.access(dir_path, os.W_OK)
            }
            status = "✅" if dir_path.exists() else "❌"
            print(f"{status} {dir_name}目录 - {'存在' if dir_path.exists() else '不存在'}")
        
        self.results['functionality'] = func_results
        return func_results
    
    def generate_summary(self) -> Dict[str, Any]:
        """生成检查摘要"""
        print("\n📊 生成检查摘要...")
        
        env = self.results['environment']
        deps = self.results['dependencies']
        tools = self.results['mcp_tools']
        func = self.results['functionality']
        
        summary = {
            'overall_status': 'unknown',
            'environment_ok': env.get('is_virtual_env', False),
            'dependencies_ok': deps.get('installed_count', 0) >= len(self.critical_dependencies) * 0.8,
            'tools_ok': tools.get('available_count', 0) == len(self.mcp_tools),
            'functionality_ok': len(func.get('core_modules', {})) > 0,
            'scores': {
                'environment': 100 if env.get('is_virtual_env', False) else 70,
                'dependencies': int((deps.get('installed_count', 0) / len(self.critical_dependencies)) * 100),
                'tools': int((tools.get('available_count', 0) / len(self.mcp_tools)) * 100),
                'functionality': int((len([m for m in func.get('core_modules', {}).values() if m.get('status') == 'ok']) / len(func.get('core_modules', {}))) * 100) if func.get('core_modules') else 0
            },
            'recommendations': []
        }
        
        # 计算总体评分
        total_score = sum(summary['scores'].values()) / len(summary['scores'])
        summary['total_score'] = int(total_score)
        
        # 确定总体状态
        if total_score >= 90:
            summary['overall_status'] = 'excellent'
        elif total_score >= 75:
            summary['overall_status'] = 'good'
        elif total_score >= 60:
            summary['overall_status'] = 'fair'
        else:
            summary['overall_status'] = 'poor'
        
        # 生成建议
        if not summary['environment_ok']:
            summary['recommendations'].append("建议使用虚拟环境以获得更好的依赖隔离")
        
        if deps.get('missing'):
            summary['recommendations'].append(f"需要安装缺失的依赖库: {', '.join([m['package'] for m in deps['missing']])}")
        
        if tools.get('unavailable'):
            summary['recommendations'].append(f"需要修复不可用的MCP工具: {len(tools['unavailable'])}个")
        
        self.results['summary'] = summary
        return summary
    
    def run_full_check(self) -> Dict[str, Any]:
        """运行完整检查"""
        print("🚀 开始全面环境检查")
        print("=" * 60)
        
        try:
            self.check_environment()
            self.check_dependencies()
            self.check_mcp_tools()
            self.check_functionality()
            summary = self.generate_summary()
            
            print("\n" + "=" * 60)
            print("📋 检查结果摘要")
            print("=" * 60)
            
            print(f"总体评分: {summary['total_score']}/100 ({summary['overall_status'].upper()})")
            print(f"环境评分: {summary['scores']['environment']}/100")
            print(f"依赖评分: {summary['scores']['dependencies']}/100")
            print(f"工具评分: {summary['scores']['tools']}/100")
            print(f"功能评分: {summary['scores']['functionality']}/100")
            
            print(f"\n✅ MCP工具可用: {self.results['mcp_tools']['available_count']}/31")
            print(f"✅ 依赖库安装: {self.results['dependencies']['installed_count']}/{len(self.critical_dependencies)}")
            
            if summary['recommendations']:
                print("\n💡 改进建议:")
                for i, rec in enumerate(summary['recommendations'], 1):
                    print(f"  {i}. {rec}")
            
            # 保存详细报告
            report_file = 'comprehensive_environment_check_report.json'
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            
            print(f"\n📄 详细报告已保存到: {report_file}")
            
            return self.results
            
        except Exception as e:
            print(f"\n❌ 检查过程中发生错误: {e}")
            traceback.print_exc()
            return {'error': str(e), 'traceback': traceback.format_exc()}

def main():
    """主函数"""
    checker = EnvironmentChecker()
    results = checker.run_full_check()
    
    # 返回检查是否成功
    if 'error' not in results:
        summary = results.get('summary', {})
        return summary.get('total_score', 0) >= 75
    else:
        return False

if __name__ == "__main__":
    success = main()
    exit_code = 0 if success else 1
    print(f"\n🏁 检查完成 - {'成功' if success else '需要改进'}")
    sys.exit(exit_code)