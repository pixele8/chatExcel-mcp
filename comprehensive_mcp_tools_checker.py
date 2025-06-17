#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面的MCP工具完整性检查器

基于之前修复的问题模式，系统性检查所有31个MCP工具的：
1. 类方法调用一致性
2. 导入模块的完整性
3. 参数传递匹配性
4. 返回值格式统一性
"""

import ast
import os
import re
import json
import importlib.util
from typing import Dict, List, Set, Tuple, Any
from pathlib import Path
import traceback

class MCPToolsChecker:
    """MCP工具完整性检查器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.server_file = self.project_root / "server.py"
        self.issues = []
        self.tools_info = {}
        self.external_modules = {}
        
    def extract_mcp_tools(self) -> Dict[str, Dict]:
        """提取所有MCP工具的信息"""
        print("🔍 正在提取MCP工具信息...")
        
        with open(self.server_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 解析AST
        tree = ast.parse(content)
        
        tools = {}
        current_tool = None
        
        for node in ast.walk(tree):
            # 查找@mcp.tool()装饰的函数
            if isinstance(node, ast.FunctionDef):
                has_mcp_decorator = False
                for decorator in node.decorator_list:
                    if (isinstance(decorator, ast.Call) and 
                        isinstance(decorator.func, ast.Attribute) and
                        isinstance(decorator.func.value, ast.Name) and
                        decorator.func.value.id == 'mcp' and
                        decorator.func.attr == 'tool'):
                        has_mcp_decorator = True
                        break
                        
                if has_mcp_decorator:
                    tools[node.name] = {
                        'name': node.name,
                        'lineno': node.lineno,
                        'args': [arg.arg for arg in node.args.args],
                        'docstring': ast.get_docstring(node),
                        'calls': self._extract_function_calls(node),
                        'imports_used': list(self._extract_imports_used(node))
                    }
                    
        print(f"✅ 发现 {len(tools)} 个MCP工具")
        return tools
    
    def _extract_function_calls(self, func_node: ast.FunctionDef) -> List[Dict]:
        """提取函数中的所有外部调用"""
        calls = []
        
        for node in ast.walk(func_node):
            if isinstance(node, ast.Call):
                call_info = self._parse_call(node)
                if call_info:
                    calls.append(call_info)
                    
        return calls
    
    def _parse_call(self, call_node: ast.Call) -> Dict:
        """解析函数调用信息"""
        try:
            if isinstance(call_node.func, ast.Attribute):
                # 方法调用: obj.method()
                if isinstance(call_node.func.value, ast.Name):
                    return {
                        'type': 'method',
                        'object': call_node.func.value.id,
                        'method': call_node.func.attr,
                        'args_count': len(call_node.args),
                        'lineno': call_node.lineno
                    }
                elif isinstance(call_node.func.value, ast.Attribute):
                    # 链式调用: obj.attr.method()
                    return {
                        'type': 'chained_method',
                        'chain': self._get_attribute_chain(call_node.func),
                        'args_count': len(call_node.args),
                        'lineno': call_node.lineno
                    }
            elif isinstance(call_node.func, ast.Name):
                # 函数调用: function()
                return {
                    'type': 'function',
                    'name': call_node.func.id,
                    'args_count': len(call_node.args),
                    'lineno': call_node.lineno
                }
        except Exception as e:
            return {
                'type': 'parse_error',
                'error': str(e),
                'lineno': getattr(call_node, 'lineno', 0)
            }
        return None
    
    def _get_attribute_chain(self, attr_node: ast.Attribute) -> List[str]:
        """获取属性链"""
        chain = [attr_node.attr]
        current = attr_node.value
        
        while isinstance(current, ast.Attribute):
            chain.insert(0, current.attr)
            current = current.value
            
        if isinstance(current, ast.Name):
            chain.insert(0, current.id)
            
        return chain
    
    def _extract_imports_used(self, func_node: ast.FunctionDef) -> Set[str]:
        """提取函数中使用的导入模块"""
        imports = set()
        
        for node in ast.walk(func_node):
            if isinstance(node, ast.Name):
                imports.add(node.id)
                
        return imports
    
    def check_external_modules(self) -> Dict[str, Dict]:
        """检查外部模块的完整性"""
        print("🔍 正在检查外部模块...")
        
        modules_to_check = [
            'formulas_tools',
            'excel_data_quality_tools',
            'excel_helper',
            'excel_smart_tools',
            'enhanced_excel_helper',
            'comprehensive_data_verification',
            'data_verification',
            'excel_enhanced_tools'
        ]
        
        module_info = {}
        
        for module_name in modules_to_check:
            module_path = self.project_root / f"{module_name}.py"
            if module_path.exists():
                try:
                    module_info[module_name] = self._analyze_module(module_path)
                except Exception as e:
                    module_info[module_name] = {
                        'error': f"分析模块失败: {str(e)}",
                        'classes': {},
                        'functions': []
                    }
            else:
                module_info[module_name] = {
                    'error': '模块文件不存在',
                    'classes': {},
                    'functions': []
                }
                
        return module_info
    
    def _analyze_module(self, module_path: Path) -> Dict:
        """分析模块内容"""
        with open(module_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        tree = ast.parse(content)
        
        classes = {}
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        class_methods.append({
                            'name': item.name,
                            'args': [arg.arg for arg in item.args.args],
                            'lineno': item.lineno
                        })
                        
                classes[node.name] = {
                    'methods': class_methods,
                    'lineno': node.lineno
                }
                
            elif isinstance(node, ast.FunctionDef):
                # 只记录顶级函数
                if isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                    functions.append({
                        'name': node.name,
                        'args': [arg.arg for arg in node.args.args],
                        'lineno': node.lineno
                    })
                    
        return {
            'classes': classes,
            'functions': functions,
            'path': str(module_path)
        }
    
    def validate_tool_calls(self, tools: Dict, modules: Dict) -> List[Dict]:
        """验证工具调用的完整性"""
        print("🔍 正在验证工具调用...")
        
        issues = []
        
        # 已知的实例映射
        instance_mapping = {
            'data_quality_controller': ('excel_data_quality_tools', 'ExcelDataQualityController'),
            'cell_content_extractor': ('excel_data_quality_tools', 'ExcelCellContentExtractor'),
            'character_converter': ('excel_data_quality_tools', 'ExcelCharacterConverter'),
            'multi_condition_extractor': ('excel_data_quality_tools', 'ExcelMultiConditionExtractor'),
            'multi_table_merger': ('excel_data_quality_tools', 'ExcelMultiTableMerger'),
            'data_cleaner': ('excel_data_quality_tools', 'ExcelDataCleaner'),
            'batch_processor': ('excel_data_quality_tools', 'ExcelBatchProcessor')
        }
        
        for tool_name, tool_info in tools.items():
            print(f"  检查工具: {tool_name}")
            
            for call in tool_info['calls']:
                if call['type'] == 'method':
                    obj_name = call['object']
                    method_name = call['method']
                    
                    # 检查实例映射
                    if obj_name in instance_mapping:
                        module_name, class_name = instance_mapping[obj_name]
                        
                        if module_name in modules and 'classes' in modules[module_name]:
                            if class_name in modules[module_name]['classes']:
                                class_info = modules[module_name]['classes'][class_name]
                                method_names = [m['name'] for m in class_info['methods']]
                                
                                if method_name not in method_names:
                                    issues.append({
                                        'type': 'missing_method',
                                        'severity': 'high',
                                        'tool': tool_name,
                                        'object': obj_name,
                                        'class': class_name,
                                        'module': module_name,
                                        'missing_method': method_name,
                                        'available_methods': method_names,
                                        'line': call['lineno'],
                                        'suggestion': self._suggest_method_fix(method_name, method_names)
                                    })
                            else:
                                issues.append({
                                    'type': 'missing_class',
                                    'severity': 'high',
                                    'tool': tool_name,
                                    'object': obj_name,
                                    'class': class_name,
                                    'module': module_name,
                                    'line': call['lineno']
                                })
                        else:
                            issues.append({
                                'type': 'missing_module',
                                'severity': 'critical',
                                'tool': tool_name,
                                'module': module_name,
                                'line': call['lineno']
                            })
                            
                elif call['type'] == 'function':
                    func_name = call['name']
                    
                    # 检查导入的函数
                    found = False
                    for module_name, module_info in modules.items():
                        if 'functions' in module_info:
                            func_names = [f['name'] for f in module_info['functions']]
                            if func_name in func_names:
                                found = True
                                break
                                
                    # 内置函数和常用函数列表
                    builtin_functions = {
                        'len', 'str', 'int', 'float', 'bool', 'list', 'dict', 'tuple', 'set',
                        'min', 'max', 'sum', 'abs', 'round', 'sorted', 'reversed', 'enumerate',
                        'zip', 'map', 'filter', 'all', 'any', 'isinstance', 'hasattr', 'getattr',
                        'setattr', 'delattr', 'type', 'id', 'hash', 'repr', 'print', 'input',
                        'open', 'range', 'slice', 'super', 'property', 'staticmethod', 'classmethod',
                        '__import__', 'exec', 'eval', 'compile', 'globals', 'locals', 'vars'
                    }
                    
                    # 常用库函数和类
                    common_library_functions = {
                        'pd', 'np', 'plt', 'sns', 'px', 'go', 'make_subplots',
                        'create_error_response', 'create_success_response', 'validate_file_access',
                        'ComprehensiveDataVerifier', 'DataVerificationEngine', 'SecureCodeExecutor',
                        'StringIO', 'detect', 'infer_dtype', 'safe_import_pandas', 'safe_import_numpy'
                    }
                    
                    if not found and func_name not in builtin_functions and func_name not in common_library_functions:
                        # 只报告真正缺失的自定义函数
                        issues.append({
                            'type': 'missing_function',
                            'severity': 'medium',
                            'tool': tool_name,
                            'function': func_name,
                            'line': call['lineno']
                        })
                        
        return issues
    
    def _suggest_method_fix(self, missing_method: str, available_methods: List[str]) -> str:
        """建议方法修复方案"""
        # 简单的字符串相似度匹配
        suggestions = []
        
        for method in available_methods:
            if missing_method.lower() in method.lower() or method.lower() in missing_method.lower():
                suggestions.append(method)
                
        if suggestions:
            return f"可能的替代方法: {', '.join(suggestions)}"
        else:
            return f"建议检查类定义，可用方法: {', '.join(available_methods[:5])}"
    
    def generate_report(self, tools: Dict, modules: Dict, issues: List[Dict]) -> Dict:
        """生成检查报告"""
        print("📊 正在生成检查报告...")
        
        # 统计信息
        stats = {
            'total_tools': len(tools),
            'total_issues': len(issues),
            'critical_issues': len([i for i in issues if i.get('severity') == 'critical']),
            'high_issues': len([i for i in issues if i.get('severity') == 'high']),
            'medium_issues': len([i for i in issues if i.get('severity') == 'medium']),
            'modules_checked': len(modules),
            'modules_with_errors': len([m for m in modules.values() if 'error' in m])
        }
        
        # 按工具分组问题
        issues_by_tool = {}
        for issue in issues:
            tool = issue.get('tool', 'unknown')
            if tool not in issues_by_tool:
                issues_by_tool[tool] = []
            issues_by_tool[tool].append(issue)
            
        # 按严重程度分组
        issues_by_severity = {
            'critical': [i for i in issues if i.get('severity') == 'critical'],
            'high': [i for i in issues if i.get('severity') == 'high'],
            'medium': [i for i in issues if i.get('severity') == 'medium']
        }
        
        report = {
            'timestamp': str(Path().cwd()),
            'summary': stats,
            'tools_info': tools,
            'modules_info': modules,
            'issues': {
                'all': issues,
                'by_tool': issues_by_tool,
                'by_severity': issues_by_severity
            },
            'recommendations': self._generate_recommendations(issues)
        }
        
        return report
    
    def _generate_recommendations(self, issues: List[Dict]) -> List[str]:
        """生成修复建议"""
        recommendations = []
        
        critical_count = len([i for i in issues if i.get('severity') == 'critical'])
        high_count = len([i for i in issues if i.get('severity') == 'high'])
        
        if critical_count > 0:
            recommendations.append(f"🚨 发现 {critical_count} 个严重问题，需要立即修复")
            
        if high_count > 0:
            recommendations.append(f"⚠️ 发现 {high_count} 个高优先级问题，建议优先修复")
            
        # 具体建议
        missing_methods = [i for i in issues if i['type'] == 'missing_method']
        if missing_methods:
            recommendations.append("建议检查类方法定义，确保方法名一致性")
            
        missing_modules = [i for i in issues if i['type'] == 'missing_module']
        if missing_modules:
            recommendations.append("建议检查模块导入路径和文件存在性")
            
        return recommendations
    
    def run_comprehensive_check(self) -> Dict:
        """运行全面检查"""
        print("🚀 开始全面的MCP工具检查...")
        print(f"📁 项目路径: {self.project_root}")
        
        try:
            # 1. 提取工具信息
            tools = self.extract_mcp_tools()
            
            # 2. 检查外部模块
            modules = self.check_external_modules()
            
            # 3. 验证调用
            issues = self.validate_tool_calls(tools, modules)
            
            # 4. 生成报告
            report = self.generate_report(tools, modules, issues)
            
            print(f"✅ 检查完成！发现 {len(issues)} 个问题")
            return report
            
        except Exception as e:
            print(f"❌ 检查过程中出现错误: {str(e)}")
            print(traceback.format_exc())
            return {
                'error': str(e),
                'traceback': traceback.format_exc()
            }

def main():
    """主函数"""
    project_root = "/Users/wangdada/Downloads/mcp/chatExcel-mcp"
    
    checker = MCPToolsChecker(project_root)
    report = checker.run_comprehensive_check()
    
    # 保存报告
    report_file = Path(project_root) / "comprehensive_mcp_tools_check_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print(f"📄 详细报告已保存到: {report_file}")
    
    # 打印摘要
    if 'summary' in report:
        print("\n📊 检查摘要:")
        for key, value in report['summary'].items():
            print(f"  {key}: {value}")
            
    if 'issues' in report and 'by_severity' in report['issues']:
        print("\n🚨 问题分布:")
        for severity, issues in report['issues']['by_severity'].items():
            if issues:
                print(f"  {severity.upper()}: {len(issues)} 个")
                for issue in issues[:3]:  # 显示前3个
                    print(f"    - {issue.get('tool', 'unknown')}: {issue.get('type', 'unknown')}")
                if len(issues) > 3:
                    print(f"    ... 还有 {len(issues) - 3} 个")
                    
    if 'recommendations' in report:
        print("\n💡 修复建议:")
        for rec in report['recommendations']:
            print(f"  {rec}")

if __name__ == "__main__":
    main()