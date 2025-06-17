#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面的MCP工具系统性分析和优化检测脚本
基于问题1-5的修复经验，对所有24个工具进行稳定性检测
"""

import ast
import inspect
import importlib.util
import sys
import os
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
import pandas as pd
import traceback

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class MCPToolsAnalyzer:
    """MCP工具系统性分析器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.server_file = self.project_root / "server.py"
        self.tools_info = []
        self.problem_categories = {
            "编码问题": [],
            "安全检查问题": [],
            "执行环境问题": [],
            "参数验证问题": [],
            "错误处理问题": [],
            "性能优化问题": [],
            "兼容性问题": []
        }
        
    def extract_tools_from_server(self) -> List[Dict[str, Any]]:
        """从server.py中提取所有MCP工具信息"""
        print("=== 提取MCP工具信息 ===")
        
        with open(self.server_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 解析AST
        tree = ast.parse(content)
        
        tools = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # 检查是否有@mcp.tool()装饰器
                has_mcp_decorator = any(
                    # 检查 @mcp.tool() 调用形式
                    (isinstance(decorator, ast.Call) and
                     isinstance(decorator.func, ast.Attribute) and
                     isinstance(decorator.func.value, ast.Name) and
                     decorator.func.value.id == 'mcp' and
                     decorator.func.attr == 'tool') or
                    # 检查 @mcp.tool 属性形式
                    (isinstance(decorator, ast.Attribute) and
                     isinstance(decorator.value, ast.Name) and
                     decorator.value.id == 'mcp' and
                     decorator.attr == 'tool')
                    for decorator in node.decorator_list
                )
                
                if has_mcp_decorator:
                    tool_info = self._analyze_tool_function(node, content)
                    tools.append(tool_info)
                    
        print(f"✓ 发现 {len(tools)} 个MCP工具")
        return tools
    
    def _analyze_tool_function(self, node: ast.FunctionDef, content: str) -> Dict[str, Any]:
        """分析单个工具函数"""
        # 获取函数基本信息
        func_name = node.name
        docstring = ast.get_docstring(node) or "无文档"
        
        # 分析参数
        args = []
        for arg in node.args.args:
            arg_info = {
                "name": arg.arg,
                "annotation": ast.unparse(arg.annotation) if arg.annotation else "Any"
            }
            args.append(arg_info)
            
        # 分析返回类型
        return_type = ast.unparse(node.returns) if node.returns else "Any"
        
        # 获取函数源码行数
        start_line = node.lineno
        end_line = node.end_lineno or start_line
        
        # 分析函数复杂度
        complexity = self._calculate_complexity(node)
        
        # 检测潜在问题
        potential_issues = self._detect_potential_issues(node, content)
        
        return {
            "name": func_name,
            "docstring": docstring,
            "args": args,
            "return_type": return_type,
            "start_line": start_line,
            "end_line": end_line,
            "complexity": complexity,
            "potential_issues": potential_issues,
            "category": self._categorize_tool(func_name, docstring)
        }
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> Dict[str, int]:
        """计算函数复杂度"""
        complexity = {
            "lines": (node.end_lineno or node.lineno) - node.lineno + 1,
            "branches": 0,
            "loops": 0,
            "try_blocks": 0,
            "nested_functions": 0
        }
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For)):
                complexity["branches" if isinstance(child, ast.If) else "loops"] += 1
            elif isinstance(child, ast.Try):
                complexity["try_blocks"] += 1
            elif isinstance(child, ast.FunctionDef) and child != node:
                complexity["nested_functions"] += 1
                
        return complexity
    
    def _detect_potential_issues(self, node: ast.FunctionDef, content: str) -> List[Dict[str, str]]:
        """检测潜在问题"""
        issues = []
        func_source = ast.unparse(node)
        
        # 1. 编码问题检测
        if "encoding" in func_source.lower() and "detect" not in func_source.lower():
            issues.append({
                "category": "编码问题",
                "type": "缺少编码检测",
                "description": "函数处理文件但可能缺少智能编码检测机制",
                "severity": "medium"
            })
            
        # 2. 安全检查问题
        if "exec" in func_source or "eval" in func_source:
            if "SecureCodeExecutor" not in func_source:
                issues.append({
                    "category": "安全检查问题",
                    "type": "不安全的代码执行",
                    "description": "使用exec/eval但未使用安全执行器",
                    "severity": "high"
                })
                
        # 3. 错误处理检测
        has_try_except = any(isinstance(child, ast.Try) for child in ast.walk(node))
        if not has_try_except and node.name not in ["read_metadata", "get_tool_info"]:
            issues.append({
                "category": "错误处理问题",
                "type": "缺少异常处理",
                "description": "函数缺少try-except错误处理机制",
                "severity": "medium"
            })
            
        # 4. 参数验证检测
        if not any("validate" in ast.unparse(child).lower() 
                  for child in ast.walk(node) if isinstance(child, ast.Call)):
            if len(node.args.args) > 2:  # 多参数函数需要验证
                issues.append({
                    "category": "参数验证问题",
                    "type": "缺少参数验证",
                    "description": "多参数函数缺少输入验证",
                    "severity": "medium"
                })
                
        # 5. 性能问题检测
        if "pandas" in func_source and "chunk" not in func_source.lower():
            if "read_excel" in node.name or "process" in node.name:
                issues.append({
                    "category": "性能优化问题",
                    "type": "缺少分块处理",
                    "description": "大文件处理可能需要分块机制",
                    "severity": "low"
                })
                
        return issues
    
    def _categorize_tool(self, func_name: str, docstring: str) -> str:
        """工具分类"""
        name_lower = func_name.lower()
        doc_lower = docstring.lower()
        
        if "read" in name_lower or "读取" in doc_lower:
            return "数据读取"
        elif "write" in name_lower or "写入" in doc_lower:
            return "数据写入"
        elif "chart" in name_lower or "图表" in doc_lower:
            return "图表生成"
        elif "code" in name_lower or "代码" in doc_lower:
            return "代码执行"
        elif "validate" in name_lower or "验证" in doc_lower:
            return "数据验证"
        elif "formula" in name_lower or "公式" in doc_lower:
            return "公式处理"
        elif "metadata" in name_lower or "元数据" in doc_lower:
            return "元数据分析"
        elif "batch" in name_lower or "批量" in doc_lower:
            return "批量处理"
        else:
            return "其他工具"
    
    def generate_optimization_plan(self, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成优化方案"""
        print("\n=== 生成系统优化方案 ===")
        
        # 统计问题分布
        issue_stats = {category: 0 for category in self.problem_categories.keys()}
        high_priority_tools = []
        
        for tool in tools:
            for issue in tool["potential_issues"]:
                issue_stats[issue["category"]] += 1
                if issue["severity"] == "high":
                    high_priority_tools.append({
                        "tool": tool["name"],
                        "issue": issue
                    })
        
        # 按类别统计工具
        category_stats = {}
        for tool in tools:
            category = tool["category"]
            if category not in category_stats:
                category_stats[category] = 0
            category_stats[category] += 1
            
        # 生成优化建议
        optimization_plan = {
            "总体统计": {
                "工具总数": len(tools),
                "问题总数": sum(len(tool["potential_issues"]) for tool in tools),
                "高优先级问题": len(high_priority_tools),
                "类别分布": category_stats
            },
            "问题分布": issue_stats,
            "高优先级修复": high_priority_tools,
            "优化建议": self._generate_specific_recommendations(tools, issue_stats)
        }
        
        return optimization_plan
    
    def _generate_specific_recommendations(self, tools: List[Dict[str, Any]], 
                                         issue_stats: Dict[str, int]) -> List[Dict[str, Any]]:
        """生成具体优化建议"""
        recommendations = []
        
        # 基于问题统计生成建议
        if issue_stats["编码问题"] > 0:
            recommendations.append({
                "类别": "编码问题",
                "优先级": "高",
                "建议": "统一集成智能编码检测机制到所有文件处理工具",
                "实施方案": [
                    "在所有文件读取工具中集成detect_file_encoding函数",
                    "添加多编码尝试机制和回退策略",
                    "统一编码错误处理和用户提示"
                ]
            })
            
        if issue_stats["安全检查问题"] > 0:
            recommendations.append({
                "类别": "安全检查问题",
                "优先级": "高",
                "建议": "强化所有代码执行工具的安全机制",
                "实施方案": [
                    "确保所有代码执行都使用SecureCodeExecutor",
                    "优化AST安全分析器的函数白名单",
                    "添加更细粒度的安全策略配置"
                ]
            })
            
        if issue_stats["错误处理问题"] > 5:
            recommendations.append({
                "类别": "错误处理问题",
                "优先级": "中",
                "建议": "标准化错误处理机制",
                "实施方案": [
                    "为所有工具添加统一的异常处理装饰器",
                    "实现分层错误处理和详细错误报告",
                    "添加错误恢复和重试机制"
                ]
            })
            
        if issue_stats["参数验证问题"] > 3:
            recommendations.append({
                "类别": "参数验证问题",
                "优先级": "中",
                "建议": "实现统一的参数验证框架",
                "实施方案": [
                    "创建参数验证装饰器",
                    "添加类型检查和范围验证",
                    "实现参数自动转换和清理"
                ]
            })
            
        if issue_stats["性能优化问题"] > 2:
            recommendations.append({
                "类别": "性能优化问题",
                "优先级": "低",
                "建议": "优化大数据处理性能",
                "实施方案": [
                    "为大文件处理添加分块机制",
                    "实现内存使用监控和优化",
                    "添加进度报告和取消机制"
                ]
            })
            
        return recommendations
    
    def run_analysis(self) -> Dict[str, Any]:
        """运行完整分析"""
        print("🔍 开始MCP工具系统性分析...")
        
        try:
            # 1. 提取工具信息
            tools = self.extract_tools_from_server()
            self.tools_info = tools
            
            # 2. 生成优化方案
            optimization_plan = self.generate_optimization_plan(tools)
            
            # 3. 生成详细报告
            report = {
                "分析时间": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                "工具详情": tools,
                "优化方案": optimization_plan,
                "分析总结": self._generate_summary(tools, optimization_plan)
            }
            
            return report
            
        except Exception as e:
            print(f"❌ 分析过程中发生错误: {e}")
            traceback.print_exc()
            return {"error": str(e), "traceback": traceback.format_exc()}
    
    def _generate_summary(self, tools: List[Dict[str, Any]], 
                         optimization_plan: Dict[str, Any]) -> Dict[str, Any]:
        """生成分析总结"""
        total_issues = sum(len(tool["potential_issues"]) for tool in tools)
        high_severity_issues = sum(
            1 for tool in tools 
            for issue in tool["potential_issues"] 
            if issue["severity"] == "high"
        )
        
        return {
            "工具健康度评分": max(0, 100 - (total_issues * 5) - (high_severity_issues * 10)),
            "关键发现": [
                f"发现 {len(tools)} 个MCP工具",
                f"检测到 {total_issues} 个潜在问题",
                f"其中 {high_severity_issues} 个高优先级问题需要立即修复",
                f"建议实施 {len(optimization_plan['优化建议'])} 项优化措施"
            ],
            "下一步行动": [
                "优先修复高优先级安全问题",
                "统一实施编码检测机制",
                "标准化错误处理流程",
                "建立持续监控机制"
            ]
        }

def main():
    """主函数"""
    analyzer = MCPToolsAnalyzer()
    report = analyzer.run_analysis()
    
    # 保存报告
    report_file = "comprehensive_tools_analysis_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n📊 分析报告已保存到: {report_file}")
    
    # 打印关键信息
    if "error" not in report:
        print("\n=== 分析总结 ===")
        summary = report["分析总结"]
        print(f"工具健康度评分: {summary['工具健康度评分']}/100")
        print("\n关键发现:")
        for finding in summary["关键发现"]:
            print(f"  • {finding}")
        print("\n下一步行动:")
        for action in summary["下一步行动"]:
            print(f"  • {action}")
    
    return report

if __name__ == "__main__":
    main()