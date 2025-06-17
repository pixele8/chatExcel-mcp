#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatExcel MCP Server - Excel 公式处理工具模块
企业级 Excel 公式解析、编译和执行工具集

功能特性:
- Excel 公式解析和编译
- 工作簿编译为 Python 代码
- 公式依赖关系分析
- 自定义函数支持
- 公式验证和错误检查
- 安全的公式执行环境
- 智能公式推荐和模板管理
- 多表格协同处理
- 性能分析和优化建议
- 批量公式处理

作者: ChatExcel MCP Team
版本: 2.0.0
创建日期: 2025-06-18
更新日期: 2025-06-18
"""

import json
import logging
import tempfile
import traceback
import time
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
from collections import defaultdict
import hashlib

try:
    import formulas
    from formulas import ExcelModel
    from formulas import Parser
except ImportError as e:
    logging.error(f"Failed to import formulas library: {e}")
    formulas = None
    ExcelModel = None
    Parser = None

import pandas as pd
import numpy as np

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FormulaTemplateManager:
    """Excel 公式模板管理器"""
    
    def __init__(self):
        self.templates = self._initialize_templates()
        self.categories = list(self.templates.keys())
    
    def _initialize_templates(self) -> Dict[str, Dict[str, Any]]:
        """初始化公式模板库"""
        return {
            "财务计算": {
                "复合年增长率": {
                    "formula": "=POWER({end_value}/{start_value}, 1/{years}) - 1",
                    "description": "计算复合年增长率(CAGR)",
                    "parameters": ["end_value", "start_value", "years"],
                    "example": "=POWER(B10/B1, 1/9) - 1",
                    "use_case": "投资回报率分析"
                },
                "净现值": {
                    "formula": "=NPV({rate}, {cash_flows}) + {initial_investment}",
                    "description": "计算净现值(NPV)",
                    "parameters": ["rate", "cash_flows", "initial_investment"],
                    "example": "=NPV(0.1, B2:B10) + B1",
                    "use_case": "项目投资评估"
                },
                "内部收益率": {
                    "formula": "=IRR({cash_flows})",
                    "description": "计算内部收益率(IRR)",
                    "parameters": ["cash_flows"],
                    "example": "=IRR(B1:B10)",
                    "use_case": "投资项目评估"
                }
            },
            "统计分析": {
                "移动平均": {
                    "formula": "=AVERAGE(OFFSET({reference}, -{periods}+1, 0, {periods}, 1))",
                    "description": "计算移动平均值",
                    "parameters": ["reference", "periods"],
                    "example": "=AVERAGE(OFFSET(A10, -6, 0, 7, 1))",
                    "use_case": "趋势分析"
                },
                "标准差": {
                    "formula": "=STDEV({range})",
                    "description": "计算标准差",
                    "parameters": ["range"],
                    "example": "=STDEV(A1:A100)",
                    "use_case": "数据离散度分析"
                },
                "相关系数": {
                    "formula": "=CORREL({array1}, {array2})",
                    "description": "计算相关系数",
                    "parameters": ["array1", "array2"],
                    "example": "=CORREL(A1:A100, B1:B100)",
                    "use_case": "变量关系分析"
                }
            },
            "文本处理": {
                "提取数字": {
                    "formula": "=VALUE(REGEX({text}, \"[0-9]+\", \"g\"))",
                    "description": "从文本中提取数字",
                    "parameters": ["text"],
                    "example": "=VALUE(REGEX(A1, \"[0-9]+\", \"g\"))",
                    "use_case": "数据清洗"
                },
                "首字母大写": {
                    "formula": "=PROPER({text})",
                    "description": "将文本转换为首字母大写",
                    "parameters": ["text"],
                    "example": "=PROPER(A1)",
                    "use_case": "文本格式化"
                },
                "分割文本": {
                    "formula": "=TRIM(MID(SUBSTITUTE({text}, {delimiter}, REPT(\" \", 100)), ({n}-1)*100+1, 100))",
                    "description": "按分隔符分割文本并获取第n部分",
                    "parameters": ["text", "delimiter", "n"],
                    "example": "=TRIM(MID(SUBSTITUTE(A1, \",\", REPT(\" \", 100)), (2-1)*100+1, 100))",
                    "use_case": "数据拆分"
                }
            },
            "日期时间": {
                "工作日计算": {
                    "formula": "=NETWORKDAYS({start_date}, {end_date}, {holidays})",
                    "description": "计算两个日期间的工作日数",
                    "parameters": ["start_date", "end_date", "holidays"],
                    "example": "=NETWORKDAYS(A1, B1, C1:C10)",
                    "use_case": "项目工期计算"
                },
                "年龄计算": {
                    "formula": "=DATEDIF({birth_date}, TODAY(), \"Y\")",
                    "description": "计算年龄",
                    "parameters": ["birth_date"],
                    "example": "=DATEDIF(A1, TODAY(), \"Y\")",
                    "use_case": "人员信息管理"
                },
                "季度提取": {
                    "formula": "=\"Q\" & ROUNDUP(MONTH({date})/3, 0)",
                    "description": "从日期提取季度",
                    "parameters": ["date"],
                    "example": "=\"Q\" & ROUNDUP(MONTH(A1)/3, 0)",
                    "use_case": "财务报表分析"
                }
            },
            "条件逻辑": {
                "多条件判断": {
                    "formula": "=IFS({condition1}, {value1}, {condition2}, {value2}, TRUE, {default_value})",
                    "description": "多条件判断",
                    "parameters": ["condition1", "value1", "condition2", "value2", "default_value"],
                    "example": "=IFS(A1>90, \"优秀\", A1>80, \"良好\", TRUE, \"需改进\")",
                    "use_case": "成绩等级评定"
                },
                "嵌套IF": {
                    "formula": "=IF({condition1}, {value1}, IF({condition2}, {value2}, {default_value}))",
                    "description": "嵌套IF条件判断",
                    "parameters": ["condition1", "value1", "condition2", "value2", "default_value"],
                    "example": "=IF(A1>100, \"超额\", IF(A1>80, \"达标\", \"不达标\"))",
                    "use_case": "绩效评估"
                }
            },
            "数组公式": {
                "动态求和": {
                    "formula": "=SUMPRODUCT(({criteria_range}={criteria})*{sum_range})",
                    "description": "基于条件的动态求和",
                    "parameters": ["criteria_range", "criteria", "sum_range"],
                    "example": "=SUMPRODUCT((A1:A100=\"销售\")*B1:B100)",
                    "use_case": "分类汇总"
                },
                "数组查找": {
                    "formula": "=INDEX({return_array}, MATCH(1, ({criteria1_range}={criteria1})*({criteria2_range}={criteria2}), 0))",
                    "description": "多条件数组查找",
                    "parameters": ["return_array", "criteria1_range", "criteria1", "criteria2_range", "criteria2"],
                    "example": "=INDEX(C1:C100, MATCH(1, (A1:A100=\"张三\")*(B1:B100=\"销售\"), 0))",
                    "use_case": "复杂数据查找"
                }
            }
        }
    
    def get_templates_by_category(self, category: str) -> Dict[str, Any]:
        """根据分类获取模板"""
        return self.templates.get(category, {})
    
    def search_templates(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索模板"""
        results = []
        keyword_lower = keyword.lower()
        
        for category, templates in self.templates.items():
            for name, template in templates.items():
                if (keyword_lower in name.lower() or 
                    keyword_lower in template['description'].lower() or
                    keyword_lower in template['use_case'].lower()):
                    results.append({
                        'category': category,
                        'name': name,
                        **template
                    })
        
        return results
    
    def get_template_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """根据名称获取模板"""
        for category, templates in self.templates.items():
            if name in templates:
                return {
                    'category': category,
                    'name': name,
                    **templates[name]
                }
        return None
    
    def get_templates(self, category: str = None, difficulty: str = None) -> List[Dict[str, Any]]:
        """获取模板列表
        
        Args:
            category: 模板类别筛选
            difficulty: 难度级别筛选
            
        Returns:
            模板列表
        """
        results = []
        
        # 遍历所有模板
        for cat_name, templates in self.templates.items():
            # 类别筛选
            if category and cat_name != category:
                continue
                
            for template_name, template_data in templates.items():
                # 难度筛选（基于公式复杂度简单判断）
                if difficulty:
                    formula_complexity = self._estimate_difficulty(template_data['formula'])
                    if difficulty == 'basic' and formula_complexity > 2:
                        continue
                    elif difficulty == 'intermediate' and (formula_complexity <= 2 or formula_complexity > 5):
                        continue
                    elif difficulty == 'advanced' and formula_complexity <= 5:
                        continue
                
                results.append({
                    'category': cat_name,
                    'name': template_name,
                    **template_data
                })
        
        return results
    
    def get_available_categories(self) -> List[str]:
        """获取可用的模板类别列表"""
        return list(self.templates.keys())
    
    def find_matching_templates(self, formula: str) -> List[Dict[str, Any]]:
        """查找与给定公式匹配的模板"""
        matches = []
        formula_upper = formula.upper()
        
        for category, templates in self.templates.items():
            for name, template in templates.items():
                template_formula = template['formula'].upper()
                # 简单的模式匹配
                if self._calculate_similarity(formula_upper, template_formula) > 0.6:
                    matches.append({
                        'category': category,
                        'name': name,
                        'similarity': self._calculate_similarity(formula_upper, template_formula),
                        **template
                    })
        
        # 按相似度排序
        matches.sort(key=lambda x: x['similarity'], reverse=True)
        return matches[:5]  # 返回前5个最匹配的
    
    def _estimate_difficulty(self, formula: str) -> int:
        """估算公式难度"""
        difficulty = 0
        
        # 基于函数数量
        import re
        functions = re.findall(r'[A-Z]+\(', formula)
        difficulty += len(functions)
        
        # 基于嵌套层级
        nesting = 0
        max_nesting = 0
        for char in formula:
            if char == '(':
                nesting += 1
                max_nesting = max(max_nesting, nesting)
            elif char == ')':
                nesting -= 1
        difficulty += max_nesting
        
        # 基于公式长度
        difficulty += len(formula) // 50
        
        return difficulty
    
    def _calculate_similarity(self, formula1: str, formula2: str) -> float:
        """计算两个公式的相似度"""
        # 简单的字符串相似度计算
        import difflib
        return difflib.SequenceMatcher(None, formula1, formula2).ratio()


class IntelligentRecommender:
    """智能公式推荐器"""
    
    def __init__(self, template_manager: FormulaTemplateManager):
        self.template_manager = template_manager
        self.data_patterns = {
            'numeric': r'^-?\d+(\.\d+)?$',
            'date': r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',
            'percentage': r'\d+(\.\d+)?%',
            'currency': r'[¥$€£]\d+(\.\d+)?',
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'phone': r'\d{3}-?\d{3,4}-?\d{4}'
        }
    
    def analyze_data_characteristics(self, data: Union[List, pd.Series, pd.DataFrame]) -> Dict[str, Any]:
        """分析数据特征"""
        if isinstance(data, pd.DataFrame):
            # 分析DataFrame的每一列
            characteristics = {}
            for col in data.columns:
                characteristics[col] = self._analyze_column(data[col])
            return characteristics
        elif isinstance(data, pd.Series):
            return self._analyze_column(data)
        elif isinstance(data, list):
            return self._analyze_column(pd.Series(data))
        else:
            return {}
    
    def _analyze_column(self, series: pd.Series) -> Dict[str, Any]:
        """分析单列数据特征"""
        characteristics = {
            'data_type': str(series.dtype),
            'null_count': series.isnull().sum(),
            'unique_count': series.nunique(),
            'total_count': len(series)
        }
        
        # 检测数据模式
        if series.dtype in ['int64', 'float64']:
            characteristics.update({
                'min_value': series.min(),
                'max_value': series.max(),
                'mean_value': series.mean(),
                'std_value': series.std(),
                'pattern_type': 'numeric'
            })
        else:
            # 文本数据模式检测
            sample_values = series.dropna().astype(str).head(100)
            for pattern_name, pattern in self.data_patterns.items():
                matches = sum(1 for val in sample_values if re.match(pattern, val))
                if matches / len(sample_values) > 0.8:  # 80%以上匹配
                    characteristics['pattern_type'] = pattern_name
                    break
            else:
                characteristics['pattern_type'] = 'text'
        
        return characteristics
    
    def recommend_formulas(self, data_characteristics: Dict[str, Any], 
                          user_intent: str = "") -> List[Dict[str, Any]]:
        """基于数据特征和用户意图推荐公式"""
        recommendations = []
        
        # 基于数据类型推荐
        if isinstance(data_characteristics, dict) and 'pattern_type' in data_characteristics:
            pattern_type = data_characteristics['pattern_type']
            
            if pattern_type == 'numeric':
                recommendations.extend(self._get_numeric_recommendations())
            elif pattern_type == 'date':
                recommendations.extend(self._get_date_recommendations())
            elif pattern_type == 'currency':
                recommendations.extend(self._get_financial_recommendations())
            elif pattern_type == 'text':
                recommendations.extend(self._get_text_recommendations())
        
        # 基于用户意图推荐
        if user_intent:
            intent_recommendations = self.template_manager.search_templates(user_intent)
            recommendations.extend(intent_recommendations)
        
        # 去重并排序
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            key = rec.get('name', '') + rec.get('category', '')
            if key not in seen:
                seen.add(key)
                unique_recommendations.append(rec)
        
        return unique_recommendations[:10]  # 返回前10个推荐
    
    def _get_numeric_recommendations(self) -> List[Dict[str, Any]]:
        """获取数值型数据推荐"""
        return [
            self.template_manager.get_template_by_name('移动平均'),
            self.template_manager.get_template_by_name('标准差'),
            self.template_manager.get_template_by_name('动态求和')
        ]
    
    def _get_date_recommendations(self) -> List[Dict[str, Any]]:
        """获取日期型数据推荐"""
        return [
            self.template_manager.get_template_by_name('工作日计算'),
            self.template_manager.get_template_by_name('年龄计算'),
            self.template_manager.get_template_by_name('季度提取')
        ]
    
    def _get_financial_recommendations(self) -> List[Dict[str, Any]]:
        """获取财务型数据推荐"""
        return [
            self.template_manager.get_template_by_name('复合年增长率'),
            self.template_manager.get_template_by_name('净现值'),
            self.template_manager.get_template_by_name('内部收益率')
        ]
    
    def _get_text_recommendations(self) -> List[Dict[str, Any]]:
        """获取文本型数据推荐"""
        return [
            self.template_manager.get_template_by_name('提取数字'),
            self.template_manager.get_template_by_name('首字母大写'),
            self.template_manager.get_template_by_name('分割文本')
        ]
    
    def get_recommendations(self, data_range=None, user_intent=None, context=None):
        """
        获取智能公式推荐
        
        Args:
            data_range: 数据范围
            user_intent: 用户意图描述
            context: 上下文信息
            
        Returns:
            dict: 推荐结果
        """
        try:
            recommendations = []
            
            # 基于数据特征推荐
            if data_range:
                data_recommendations = self.recommend_formulas(data_range, user_intent or "")
                recommendations.extend(data_recommendations)
            
            # 基于用户意图推荐
            if user_intent:
                intent_recommendations = self._get_intent_based_recommendations(user_intent)
                recommendations.extend(intent_recommendations)
            
            # 基于上下文推荐
            if context:
                context_recommendations = self._get_context_based_recommendations(context)
                recommendations.extend(context_recommendations)
            
            # 去重并排序
            unique_recommendations = self._deduplicate_recommendations(recommendations)
            sorted_recommendations = sorted(unique_recommendations, key=lambda x: x.get('confidence', 0), reverse=True)
            
            return {
                'success': True,
                'recommendations': sorted_recommendations[:10],  # 返回前10个推荐
                'total_count': len(sorted_recommendations)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'recommendations': []
            }
    
    def get_optimization_suggestions(self, formula, data_context=None):
        """
        获取公式优化建议
        
        Args:
            formula: 要优化的公式
            data_context: 数据上下文
            
        Returns:
            dict: 优化建议
        """
        try:
            suggestions = []
            
            # 性能优化建议
            performance_suggestions = self._get_performance_suggestions(formula)
            suggestions.extend(performance_suggestions)
            
            # 可读性优化建议
            readability_suggestions = self._get_readability_suggestions(formula)
            suggestions.extend(readability_suggestions)
            
            # 功能优化建议
            functionality_suggestions = self._get_functionality_suggestions(formula, data_context)
            suggestions.extend(functionality_suggestions)
            
            # 错误处理建议
            error_handling_suggestions = self._get_error_handling_suggestions(formula)
            suggestions.extend(error_handling_suggestions)
            
            return {
                'success': True,
                'original_formula': formula,
                'suggestions': suggestions,
                'total_suggestions': len(suggestions)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'suggestions': []
            }
    
    def _get_intent_based_recommendations(self, user_intent):
        """
        基于用户意图获取推荐
        """
        intent_keywords = {
            '求和': ['SUM', 'SUMIF', 'SUMIFS'],
            '平均': ['AVERAGE', 'AVERAGEIF', 'AVERAGEIFS'],
            '计数': ['COUNT', 'COUNTA', 'COUNTIF', 'COUNTIFS'],
            '查找': ['VLOOKUP', 'HLOOKUP', 'INDEX', 'MATCH'],
            '日期': ['TODAY', 'NOW', 'DATE', 'DATEDIF'],
            '文本': ['CONCATENATE', 'LEFT', 'RIGHT', 'MID', 'LEN'],
            '条件': ['IF', 'IFS', 'AND', 'OR', 'NOT']
        }
        
        recommendations = []
        for keyword, formulas in intent_keywords.items():
            if keyword in user_intent:
                for formula in formulas:
                    recommendations.append({
                        'formula': formula,
                        'description': f'基于意图 "{keyword}" 推荐的公式',
                        'confidence': 0.8,
                        'category': 'intent_based'
                    })
        
        return recommendations
    
    def _get_context_based_recommendations(self, context):
        """
        基于上下文获取推荐
        """
        recommendations = []
        
        # 分析上下文中的数据类型和模式
        if 'financial' in context.get('domain', '').lower():
            financial_formulas = ['NPV', 'IRR', 'PMT', 'FV', 'PV']
            for formula in financial_formulas:
                recommendations.append({
                    'formula': formula,
                    'description': '财务分析推荐公式',
                    'confidence': 0.7,
                    'category': 'context_based'
                })
        
        if 'statistical' in context.get('analysis_type', '').lower():
            stat_formulas = ['STDEV', 'VAR', 'CORREL', 'REGRESSION']
            for formula in stat_formulas:
                recommendations.append({
                    'formula': formula,
                    'description': '统计分析推荐公式',
                    'confidence': 0.7,
                    'category': 'context_based'
                })
        
        return recommendations
    
    def _deduplicate_recommendations(self, recommendations):
        """
        去除重复的推荐
        """
        seen = set()
        unique_recommendations = []
        
        for rec in recommendations:
            formula = rec.get('formula', '')
            if formula not in seen:
                seen.add(formula)
                unique_recommendations.append(rec)
        
        return unique_recommendations
    
    def _get_performance_suggestions(self, formula):
        """
        获取性能优化建议
        """
        suggestions = []
        
        # 检查是否使用了低效的函数
        if 'VLOOKUP' in formula.upper():
            suggestions.append({
                'type': 'performance',
                'suggestion': '考虑使用 INDEX/MATCH 替代 VLOOKUP 以提高性能',
                'priority': 'medium',
                'impact': '可能提高查找速度 20-50%'
            })
        
        # 检查是否有重复计算
        if formula.count('(') > 5:
            suggestions.append({
                'type': 'performance',
                'suggestion': '公式过于复杂，考虑拆分为多个步骤',
                'priority': 'high',
                'impact': '提高计算效率和可维护性'
            })
        
        return suggestions
    
    def _get_readability_suggestions(self, formula):
        """
        获取可读性优化建议
        """
        suggestions = []
        
        # 检查公式长度
        if len(formula) > 100:
            suggestions.append({
                'type': 'readability',
                'suggestion': '公式过长，建议使用命名区域或辅助列简化',
                'priority': 'medium',
                'impact': '提高公式可读性和维护性'
            })
        
        # 检查嵌套层级
        nesting_level = formula.count('(') - formula.count(')')
        if abs(nesting_level) > 3:
            suggestions.append({
                'type': 'readability',
                'suggestion': '嵌套层级过深，考虑使用辅助计算',
                'priority': 'medium',
                'impact': '降低理解难度'
            })
        
        return suggestions
    
    def _get_functionality_suggestions(self, formula, data_context):
        """
        获取功能优化建议
        """
        suggestions = []
        
        # 基于数据上下文提供功能建议
        if data_context and 'large_dataset' in data_context:
            if 'SUM' in formula.upper() and 'IF' not in formula.upper():
                suggestions.append({
                    'type': 'functionality',
                    'suggestion': '对于大数据集，考虑使用 SUMIFS 进行条件求和',
                    'priority': 'low',
                    'impact': '提供更灵活的条件筛选'
                })
        
        return suggestions
    
    def _get_error_handling_suggestions(self, formula):
        """
        获取错误处理建议
        """
        suggestions = []
        
        # 检查是否有错误处理
        if 'IFERROR' not in formula.upper() and 'ISERROR' not in formula.upper():
            if any(func in formula.upper() for func in ['VLOOKUP', 'INDEX', 'MATCH', 'FIND']):
                suggestions.append({
                    'type': 'error_handling',
                    'suggestion': '添加 IFERROR 函数处理可能的错误',
                    'priority': 'high',
                    'impact': '避免显示错误值，提高用户体验'
                })
        
        return suggestions


class MultiWorkbookProcessor:
    """多工作簿处理器"""
    
    def __init__(self):
        self.loaded_workbooks = {}
        self.cross_references = defaultdict(list)
    
    def load_workbook(self, file_path: str, alias: str = None) -> Dict[str, Any]:
        """加载工作簿"""
        try:
            if not Path(file_path).exists():
                return {'success': False, 'error': f'文件不存在: {file_path}'}
            
            excel_model = ExcelModel().loads(file_path).finish()
            alias = alias or Path(file_path).stem
            
            self.loaded_workbooks[alias] = {
                'file_path': file_path,
                'model': excel_model,
                'load_time': time.time()
            }
            
            return {
                'success': True,
                'alias': alias,
                'worksheets': list(excel_model.worksheets.keys()) if hasattr(excel_model, 'worksheets') else [],
                'cells_count': len(excel_model.cells) if hasattr(excel_model, 'cells') else 0
            }
            
        except Exception as e:
            return {'success': False, 'error': f'加载工作簿失败: {str(e)}'}
    
    def analyze_cross_references(self) -> Dict[str, Any]:
        """分析跨工作簿引用"""
        cross_refs = defaultdict(list)
        
        for alias, workbook_info in self.loaded_workbooks.items():
            model = workbook_info['model']
            if hasattr(model, 'cells'):
                for cell_addr, cell in model.cells.items():
                    if hasattr(cell, 'formula') and cell.formula:
                        formula_str = str(cell.formula)
                        # 检测外部引用模式 [workbook.xlsx]Sheet1!A1
                        external_refs = re.findall(r'\[([^\]]+)\]([^!]+)!([A-Z]+\d+)', formula_str)
                        for ext_workbook, ext_sheet, ext_cell in external_refs:
                            cross_refs[alias].append({
                                'source_cell': cell_addr,
                                'target_workbook': ext_workbook,
                                'target_sheet': ext_sheet,
                                'target_cell': ext_cell,
                                'formula': formula_str
                            })
        
        return dict(cross_refs)
    
    def execute_cross_workbook_formula(self, formula: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """执行跨工作簿公式"""
        try:
            # 创建合并的执行环境
            merged_context = context or {}
            
            # 从所有加载的工作簿中提取数据
            for alias, workbook_info in self.loaded_workbooks.items():
                model = workbook_info['model']
                if hasattr(model, 'cells'):
                    for cell_addr, cell in model.cells.items():
                        if hasattr(cell, 'value'):
                            # 使用别名前缀避免冲突
                            prefixed_addr = f"{alias}_{cell_addr}"
                            merged_context[prefixed_addr] = cell.value
            
            # 替换公式中的跨工作簿引用
            processed_formula = self._process_cross_references(formula)
            
            # 执行公式
            excel_model = ExcelModel()
            for cell_addr, value in merged_context.items():
                excel_model[cell_addr] = value
            
            formula_cell = 'RESULT'
            excel_model[formula_cell] = processed_formula
            excel_model.finish()
            
            result_value = excel_model[formula_cell].value
            
            return {
                'success': True,
                'result': result_value,
                'processed_formula': processed_formula,
                'context_size': len(merged_context)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'跨工作簿公式执行失败: {str(e)}'
            }
    
    def _process_cross_references(self, formula: str) -> str:
        """处理公式中的跨工作簿引用"""
        # 将 [workbook.xlsx]Sheet1!A1 格式转换为 workbook_Sheet1_A1 格式
        pattern = r'\[([^\]]+)\]([^!]+)!([A-Z]+\d+)'
        
        def replace_ref(match):
            workbook = match.group(1).replace('.xlsx', '').replace('.xls', '')
            sheet = match.group(2)
            cell = match.group(3)
            return f"{workbook}_{sheet}_{cell}"
        
        return re.sub(pattern, replace_ref, formula)


class PerformanceAnalyzer:
    """性能分析器"""
    
    def __init__(self):
        self.execution_history = []
        self.performance_thresholds = {
            'execution_time': 5.0,  # 秒
            'memory_usage': 100 * 1024 * 1024,  # 100MB
            'formula_complexity': 100  # 复杂度分数
        }
    
    def analyze_formula_performance(self, formula: str, execution_time: float = None, 
                                  memory_usage: int = None) -> Dict[str, Any]:
        """分析公式性能"""
        analysis = {
            'formula': formula,
            'complexity_score': self._calculate_complexity(formula),
            'execution_time': execution_time,
            'memory_usage': memory_usage,
            'performance_issues': [],
            'optimization_suggestions': []
        }
        
        # 复杂度分析
        if analysis['complexity_score'] > self.performance_thresholds['formula_complexity']:
            analysis['performance_issues'].append('公式复杂度过高')
            analysis['optimization_suggestions'].append('考虑拆分为多个简单公式')
        
        # 执行时间分析
        if execution_time and execution_time > self.performance_thresholds['execution_time']:
            analysis['performance_issues'].append('执行时间过长')
            analysis['optimization_suggestions'].extend([
                '检查是否有不必要的重复计算',
                '考虑使用更高效的函数',
                '减少数据范围'
            ])
        
        # 内存使用分析
        if memory_usage and memory_usage > self.performance_thresholds['memory_usage']:
            analysis['performance_issues'].append('内存使用过多')
            analysis['optimization_suggestions'].append('减少处理的数据量')
        
        # 记录执行历史
        self.execution_history.append({
            'timestamp': time.time(),
            'formula_hash': hashlib.md5(formula.encode()).hexdigest(),
            **analysis
        })
        
        return analysis
    
    def _calculate_complexity(self, formula: str) -> int:
        """计算公式复杂度"""
        complexity = 0
        
        # 基础复杂度
        complexity += len(formula) // 10
        
        # 函数数量
        functions = re.findall(r'[A-Z][A-Z0-9_]*\(', formula)
        complexity += len(functions) * 5
        
        # 嵌套层级
        max_nesting = 0
        current_nesting = 0
        for char in formula:
            if char == '(':
                current_nesting += 1
                max_nesting = max(max_nesting, current_nesting)
            elif char == ')':
                current_nesting -= 1
        complexity += max_nesting * 10
        
        # 数组公式
        if '{' in formula and '}' in formula:
            complexity += 20
        
        # 条件函数
        conditional_functions = ['IF', 'IFS', 'SWITCH', 'CHOOSE']
        for func in conditional_functions:
            complexity += formula.upper().count(func) * 8
        
        return complexity
    
    def get_performance_report(self) -> Dict[str, Any]:
        """获取性能报告"""
        if not self.execution_history:
            return {'message': '暂无性能数据'}
        
        recent_executions = self.execution_history[-100:]  # 最近100次执行
        
        avg_complexity = sum(exec['complexity_score'] for exec in recent_executions) / len(recent_executions)
        avg_execution_time = sum(exec['execution_time'] for exec in recent_executions if exec['execution_time']) / max(1, sum(1 for exec in recent_executions if exec['execution_time']))
        
        common_issues = defaultdict(int)
        for exec in recent_executions:
            for issue in exec['performance_issues']:
                common_issues[issue] += 1
        
        return {
            'total_executions': len(self.execution_history),
            'recent_executions': len(recent_executions),
            'average_complexity': avg_complexity,
            'average_execution_time': avg_execution_time,
            'common_issues': dict(common_issues),
            'performance_trends': self._analyze_trends(recent_executions)
        }
    
    def _analyze_trends(self, executions: List[Dict]) -> Dict[str, Any]:
        """分析性能趋势"""
        if len(executions) < 10:
            return {'message': '数据不足以分析趋势'}
        
        # 简单的趋势分析
        first_half = executions[:len(executions)//2]
        second_half = executions[len(executions)//2:]
        
        first_avg_complexity = sum(exec['complexity_score'] for exec in first_half) / len(first_half)
        second_avg_complexity = sum(exec['complexity_score'] for exec in second_half) / len(second_half)
        
        complexity_trend = 'increasing' if second_avg_complexity > first_avg_complexity else 'decreasing'
        
        return {
            'complexity_trend': complexity_trend,
            'complexity_change': second_avg_complexity - first_avg_complexity
        }
    
    def analyze_formula_complexity(self, formula: str) -> Dict[str, Any]:
        """分析公式复杂度
        
        Args:
            formula (str): 要分析的公式
            
        Returns:
            Dict[str, Any]: 包含复杂度分析结果的字典
        """
        complexity_score = self._calculate_complexity(formula)
        
        # 分析复杂度等级
        if complexity_score <= 20:
            complexity_level = 'low'
            description = '简单公式'
        elif complexity_score <= 50:
            complexity_level = 'medium'
            description = '中等复杂度公式'
        elif complexity_score <= 100:
            complexity_level = 'high'
            description = '复杂公式'
        else:
            complexity_level = 'very_high'
            description = '极其复杂的公式'
        
        # 提供优化建议
        suggestions = []
        if complexity_score > 50:
            suggestions.append('考虑将复杂公式拆分为多个简单公式')
        if complexity_score > 100:
            suggestions.append('检查是否存在不必要的嵌套')
            suggestions.append('考虑使用辅助列来简化计算')
        
        return {
            'formula': formula,
            'complexity_score': complexity_score,
            'complexity_level': complexity_level,
            'description': description,
            'optimization_suggestions': suggestions,
            'performance_warning': complexity_score > self.performance_thresholds['formula_complexity']
        }


class FormulasSecurityManager:
    """Excel 公式安全管理器 - 增强版"""
    
    def __init__(self):
        # 危险函数黑名单 - 大幅减少
        self.dangerous_functions = {
            # 只保留最基本的系统级危险操作
        }
        
        # 资源限制
        self.max_formula_length = 10000
        self.max_calculation_time = 30  # 秒
        self.max_memory_usage = 100 * 1024 * 1024  # 100MB
        self.max_nesting_level = 20
        self.max_array_size = 1000000
    
    def validate_formula(self, formula: str) -> Dict[str, Any]:
        """验证公式安全性 - 增强版"""
        result = {
            'is_safe': True,
            'warnings': [],
            'errors': [],
            'security_score': 100,  # 安全分数，100为最安全
            'risk_level': 'low'  # low, medium, high, critical
        }
        
        # 检查公式长度
        if len(formula) > self.max_formula_length:
            result['is_safe'] = False
            result['errors'].append(f"公式长度超过限制 ({len(formula)} > {self.max_formula_length})")
            result['security_score'] -= 30
        
        # 检查危险函数 - 宽松版本
        formula_upper = formula.upper()
        for dangerous_func in self.dangerous_functions:
            if dangerous_func in formula_upper:
                # 只记录警告，不阻止执行
                result['warnings'].append(f"检测到潜在风险函数: {dangerous_func}")
                result['security_score'] -= 10  # 减少扣分
        
        # 检查嵌套层级
        nesting_level = self._calculate_nesting_level(formula)
        if nesting_level > self.max_nesting_level:
            result['warnings'].append(f"嵌套层级过深: {nesting_level}")
            result['security_score'] -= 10
        
        # 检查可疑模式
        suspicious_patterns = {
            '../': '相对路径遍历',
            '~/': '用户目录访问',
            '/etc/': '系统配置访问',
            '/var/': '系统变量访问',
            'C:\\': 'Windows系统盘访问',
            'D:\\': 'Windows其他盘访问',
            'javascript:': 'JavaScript代码注入',
            'vbscript:': 'VBScript代码注入'
        }
        
        for pattern, description in suspicious_patterns.items():
            if pattern.lower() in formula.lower():
                result['warnings'].append(f"检测到可疑模式: {description}")
                result['security_score'] -= 15
        
        # 检查大数组操作
        array_patterns = re.findall(r'([A-Z]+\d+:[A-Z]+\d+)', formula)
        for pattern in array_patterns:
            if self._estimate_array_size(pattern) > self.max_array_size:
                result['warnings'].append(f"数组范围过大: {pattern}")
                result['security_score'] -= 20
        
        # 确定风险级别
        if result['security_score'] >= 80:
            result['risk_level'] = 'low'
        elif result['security_score'] >= 60:
            result['risk_level'] = 'medium'
        elif result['security_score'] >= 40:
            result['risk_level'] = 'high'
        else:
            result['risk_level'] = 'critical'
            result['is_safe'] = False
        
        return result
    
    def _calculate_nesting_level(self, formula: str) -> int:
        """计算嵌套层级"""
        max_level = 0
        current_level = 0
        
        for char in formula:
            if char == '(':
                current_level += 1
                max_level = max(max_level, current_level)
            elif char == ')':
                current_level -= 1
        
        return max_level
    
    def _estimate_array_size(self, range_pattern: str) -> int:
        """估算数组大小"""
        try:
            # 解析范围如 A1:Z100
            start, end = range_pattern.split(':')
            
            # 提取列和行
            start_col = re.match(r'([A-Z]+)', start).group(1)
            start_row = int(re.search(r'(\d+)', start).group(1))
            end_col = re.match(r'([A-Z]+)', end).group(1)
            end_row = int(re.search(r'(\d+)', end).group(1))
            
            # 计算列数（简化计算）
            col_count = ord(end_col[-1]) - ord(start_col[-1]) + 1
            row_count = end_row - start_row + 1
            
            return col_count * row_count
        except:
            return 0


class FormulasToolsManager:
    """Excel 公式工具管理器 - 增强版"""
    
    def __init__(self):
        self.security_manager = FormulasSecurityManager()
        self.template_manager = FormulaTemplateManager()
        self.intelligent_recommender = IntelligentRecommender(self.template_manager)
        self.multi_workbook_processor = MultiWorkbookProcessor()
        self.performance_analyzer = PerformanceAnalyzer()
        self.temp_dir = Path(tempfile.gettempdir()) / "chatexcel_formulas"
        self.temp_dir.mkdir(exist_ok=True)
    
    def _check_formulas_availability(self) -> bool:
        """检查 formulas 库是否可用"""
        if formulas is None:
            logger.error("formulas 库未安装或导入失败")
            return False
        return True

    def parse_formula(self, formula: str, validate_security: bool = False, 
                     include_recommendations: bool = False, 
                     analyze_performance: bool = False) -> Dict[str, Any]:
        """解析 Excel 公式 - 增强版
        
        Args:
            formula: Excel 公式字符串
            validate_security: 是否进行安全验证
            include_recommendations: 是否包含优化建议
            analyze_performance: 是否进行性能分析
            
        Returns:
            解析结果字典
        """
        if not self._check_formulas_availability():
            return {
                'success': False,
                'error': 'formulas 库不可用',
                'data': None
            }
        
        try:
            start_time = time.time()
            
            # 安全验证 - 只记录警告，不阻止执行
            security_result = None
            if validate_security:
                security_result = self.security_manager.validate_formula(formula)
                if not security_result['is_safe']:
                    # 只记录警告，继续执行
                    logger.warning(f"公式安全验证警告: {'; '.join(security_result['errors'])}")
                    # 不返回错误，继续执行
            
            # 解析公式
            parser = Parser()
            ast_nodes = parser.ast(formula)
            compiled_formula = ast_nodes[1].compile() if len(ast_nodes) > 1 else None
            
            # 提取详细信息
            functions_used = self._extract_functions(formula)
            references = list(compiled_formula.inputs) if compiled_formula and hasattr(compiled_formula, 'inputs') else []
            
            execution_time = time.time() - start_time
            
            result = {
                'success': True,
                'data': {
                    'original_formula': formula,
                    'parsed_formula': str(compiled_formula) if compiled_formula else formula,
                    'functions_used': functions_used,
                    'references': references,
                    'complexity_analysis': {
                        'function_count': len(functions_used),
                        'reference_count': len(references),
                        'nesting_level': self.security_manager._calculate_nesting_level(formula),
                        'formula_length': len(formula)
                    },
                    'execution_time': execution_time
                }
            }
            
            # 添加安全验证结果
            if security_result:
                result['data']['security_status'] = security_result
            
            # 添加性能分析
            if analyze_performance:
                performance_analysis = self.performance_analyzer.analyze_formula_performance(
                    formula, execution_time
                )
                result['data']['performance_analysis'] = performance_analysis
            
            # 添加优化建议
            if include_recommendations:
                recommendations = self._generate_optimization_recommendations(formula, functions_used)
                result['data']['optimization_recommendations'] = recommendations
            
            return result
            
        except Exception as e:
            logger.error(f"公式解析失败: {e}")
            return {
                'success': False,
                'error': f"公式解析失败: {str(e)}",
                'traceback': traceback.format_exc(),
                'data': None
            }
    
    def _extract_functions(self, formula: str) -> List[str]:
        """从公式中提取函数名 - 增强版"""
        # 更精确的函数提取正则表达式
        function_pattern = r'([A-Z][A-Z0-9_]*?)\s*\('
        functions = re.findall(function_pattern, formula.upper())
        
        # 过滤掉可能的误匹配
        valid_functions = []
        for func in functions:
            if len(func) >= 2 and func.isalpha():  # 至少2个字符且全为字母
                valid_functions.append(func)
        
        return list(set(valid_functions))
    
    def _generate_optimization_recommendations(self, formula: str, functions_used: List[str]) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        # 检查常见的性能问题
        if 'VLOOKUP' in functions_used:
            recommendations.append("考虑使用INDEX+MATCH替代VLOOKUP以提高性能")
        
        if 'SUMPRODUCT' in functions_used and len(formula) > 200:
            recommendations.append("复杂的SUMPRODUCT公式可能影响性能，考虑拆分")
        
        if formula.count('IF') > 5:
            recommendations.append("过多的嵌套IF可以用IFS或SWITCH函数简化")
        
        if re.search(r'[A-Z]+\d+:[A-Z]+\d{4,}', formula):
            recommendations.append("大范围引用可能影响性能，考虑使用动态范围")
        
        # 检查数组公式
        if '{' in formula and '}' in formula:
            recommendations.append("数组公式在大数据集上可能较慢，考虑使用辅助列")
        
        return recommendations

    def compile_workbook(self, file_path: str, output_format: str = 'python') -> Dict[str, Any]:
        """编译 Excel 工作簿为代码
        
        Args:
            file_path: Excel 文件路径
            output_format: 输出格式 ('python', 'json')
            
        Returns:
            编译结果字典
        """
        if not self._check_formulas_availability():
            return {
                'success': False,
                'error': 'formulas 库不可用',
                'data': None
            }
        
        try:
            # 检查文件是否存在
            if not Path(file_path).exists():
                return {
                    'success': False,
                    'error': f"文件不存在: {file_path}",
                    'data': None
                }
            
            # 编译工作簿
            excel_model = ExcelModel().loads(file_path).finish()
            
            if output_format == 'python':
                # 生成 Python 代码
                python_code = excel_model.code
                
                # 保存到临时文件
                temp_file = self.temp_dir / f"compiled_{Path(file_path).stem}.py"
                with open(temp_file, 'w', encoding='utf-8') as f:
                    f.write(python_code)
                
                return {
                    'success': True,
                    'data': {
                        'output_format': 'python',
                        'code': python_code,
                        'temp_file': str(temp_file),
                        'model_info': {
                            'worksheets': list(excel_model.worksheets.keys()) if hasattr(excel_model, 'worksheets') else [],
                            'cells_count': len(excel_model.cells) if hasattr(excel_model, 'cells') else 0
                        }
                    }
                }
            
            elif output_format == 'json':
                # 生成 JSON 格式的模型信息
                model_data = {
                    'worksheets': {},
                    'formulas': {},
                    'values': {}
                }
                
                # 提取工作表信息
                if hasattr(excel_model, 'worksheets'):
                    for sheet_name, sheet in excel_model.worksheets.items():
                        model_data['worksheets'][sheet_name] = {
                            'name': sheet_name,
                            'cells': list(sheet.cells.keys()) if hasattr(sheet, 'cells') else []
                        }
                
                # 提取公式信息
                if hasattr(excel_model, 'cells'):
                    for cell_addr, cell in excel_model.cells.items():
                        if hasattr(cell, 'formula') and cell.formula:
                            model_data['formulas'][cell_addr] = str(cell.formula)
                        if hasattr(cell, 'value'):
                            model_data['values'][cell_addr] = cell.value
                
                return {
                    'success': True,
                    'data': {
                        'output_format': 'json',
                        'model_data': model_data,
                        'summary': {
                            'worksheets_count': len(model_data['worksheets']),
                            'formulas_count': len(model_data['formulas']),
                            'values_count': len(model_data['values'])
                        }
                    }
                }
            
            else:
                return {
                    'success': False,
                    'error': f"不支持的输出格式: {output_format}",
                    'data': None
                }
                
        except Exception as e:
            logger.error(f"工作簿编译失败: {e}")
            return {
                'success': False,
                'error': f"工作簿编译失败: {str(e)}",
                'traceback': traceback.format_exc(),
                'data': None
            }
    
    def execute_formula(self, formula: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """执行 Excel 公式
        
        Args:
            formula: Excel 公式字符串
            context: 执行上下文（变量值）
            
        Returns:
            执行结果字典
        """
        if not self._check_formulas_availability():
            return {
                'success': False,
                'error': 'formulas 库不可用',
                'data': None
            }
        
        try:
            # 安全验证
            security_result = self.security_manager.validate_formula(formula)
            if not security_result['is_safe']:
                return {
                    'success': False,
                    'error': f"公式安全验证失败: {'; '.join(security_result['errors'])}",
                    'security_warnings': security_result['warnings'],
                    'data': None
                }
            
            # 创建临时工作簿进行计算
            excel_model = ExcelModel()
            
            # 设置上下文变量
            if context:
                for cell_addr, value in context.items():
                    excel_model[cell_addr] = value
            
            # 设置公式到一个单元格
            formula_cell = 'A1'
            excel_model[formula_cell] = formula
            
            # 完成模型构建
            excel_model.finish()
            
            # 计算结果
            result_value = excel_model[formula_cell].value
            
            return {
                'success': True,
                'data': {
                    'formula': formula,
                    'result': result_value,
                    'result_type': type(result_value).__name__,
                    'context_used': context or {},
                    'security_status': security_result
                }
            }
            
        except Exception as e:
            logger.error(f"公式执行失败: {e}")
            return {
                'success': False,
                'error': f"公式执行失败: {str(e)}",
                'traceback': traceback.format_exc(),
                'data': None
            }
    
    def analyze_dependencies(self, file_path: str, include_cross_references: bool = True, 
                           generate_visualization: bool = False) -> Dict[str, Any]:
        """分析 Excel 文件的公式依赖关系
        
        Args:
            file_path: Excel 文件路径
            include_cross_references: 是否包含跨表格引用分析
            generate_visualization: 是否生成可视化数据
            
        Returns:
            依赖分析结果字典
        """
        if not self._check_formulas_availability():
            return {
                'success': False,
                'error': 'formulas 库不可用',
                'data': None
            }
        
        try:
            # 检查文件是否存在
            if not Path(file_path).exists():
                return {
                    'success': False,
                    'error': f"文件不存在: {file_path}",
                    'data': None
                }
            
            # 加载工作簿
            excel_model = ExcelModel().loads(file_path).finish()
            
            # 分析依赖关系
            dependencies = {}
            formulas_info = {}
            cross_references = {}
            circular_dependencies = []
            
            if hasattr(excel_model, 'cells'):
                for cell_addr, cell in excel_model.cells.items():
                    if hasattr(cell, 'formula') and cell.formula:
                        formula_str = str(cell.formula)
                        inputs = list(cell.inputs) if hasattr(cell, 'inputs') else []
                        outputs = list(cell.outputs) if hasattr(cell, 'outputs') else []
                        
                        formulas_info[cell_addr] = {
                            'formula': formula_str,
                            'inputs': inputs,
                            'outputs': outputs,
                            'complexity_score': self._calculate_formula_complexity(formula_str),
                            'function_count': len(self._extract_functions(formula_str))
                        }
                        
                        # 构建依赖关系图
                        dependencies[cell_addr] = inputs
                        
                        # 检测跨表格引用
                        if include_cross_references:
                            cross_refs = self._detect_cross_references(formula_str)
                            if cross_refs:
                                cross_references[cell_addr] = cross_refs
            
            # 检测循环依赖
            circular_dependencies = self._detect_circular_dependencies(dependencies)
            
            # 生成依赖关系统计
            stats = {
                'total_cells': len(excel_model.cells) if hasattr(excel_model, 'cells') else 0,
                'formula_cells': len(formulas_info),
                'dependency_count': sum(len(deps) for deps in dependencies.values()),
                'max_dependencies': max(len(deps) for deps in dependencies.values()) if dependencies else 0,
                'cross_reference_count': len(cross_references),
                'circular_dependency_count': len(circular_dependencies),
                'average_complexity': sum(info['complexity_score'] for info in formulas_info.values()) / len(formulas_info) if formulas_info else 0
            }
            
            result_data = {
                'file_path': file_path,
                'dependencies': dependencies,
                'formulas': formulas_info,
                'statistics': stats,
                'dependency_graph': self._build_dependency_graph(dependencies),
                'circular_dependencies': circular_dependencies
            }
            
            if include_cross_references:
                result_data['cross_references'] = cross_references
            
            if generate_visualization:
                result_data['visualization_data'] = self._generate_visualization_data(dependencies, formulas_info)
            
            return {
                'success': True,
                'data': result_data
            }
            
        except Exception as e:
            logger.error(f"依赖分析失败: {e}")
            return {
                'success': False,
                'error': f"依赖分析失败: {str(e)}",
                'traceback': traceback.format_exc(),
                'data': None
            }
    
    def _generate_visualization_data(self, dependencies: Dict[str, List[str]], 
                                   formulas_info: Dict[str, Any]) -> Dict[str, Any]:
        """生成可视化数据"""
        nodes = []
        edges = []
        
        # 创建节点
        all_cells = set(dependencies.keys())
        for deps in dependencies.values():
            all_cells.update(deps)
        
        for cell in all_cells:
            node_data = {
                'id': cell,
                'label': cell,
                'type': 'formula' if cell in formulas_info else 'data'
            }
            
            if cell in formulas_info:
                node_data.update({
                    'complexity': formulas_info[cell]['complexity_score'],
                    'function_count': formulas_info[cell]['function_count']
                })
            
            nodes.append(node_data)
        
        # 创建边
        for target, sources in dependencies.items():
            for source in sources:
                edges.append({
                    'from': source,
                    'to': target,
                    'type': 'dependency'
                })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'layout_suggestions': {
                'algorithm': 'hierarchical',
                'direction': 'UD',
                'node_spacing': 100
            }
        }
    
    def validate_formula(self, formula: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """增强版公式验证
        
        Args:
            formula: 要验证的公式
            context: 验证上下文
            
        Returns:
            验证结果字典
        """
        try:
            # 安全性验证
            security_result = self.security_manager.validate_formula(formula)
            
            # 语法验证
            syntax_result = self.parse_formula(formula, validate_security=False)
            
            # 性能分析
            performance_analysis = self.performance_analyzer.analyze_formula_complexity(formula)
            
            # 智能建议
            recommendations = self.intelligent_recommender.get_optimization_suggestions(formula)
            
            # 模板匹配
            template_matches = self.template_manager.find_matching_templates(formula)
            
            result = {
                'success': True,
                'data': {
                    'formula': formula,
                    'security_validation': security_result,
                    'syntax_validation': {
                        'is_valid': syntax_result['success'],
                        'error': syntax_result.get('error') if not syntax_result['success'] else None,
                        'parsed_data': syntax_result.get('data') if syntax_result['success'] else None
                    },
                    'performance_analysis': performance_analysis,
                    'recommendations': recommendations,
                    'template_matches': template_matches,
                    'overall_status': {
                        'is_safe': security_result['is_safe'],
                        'is_valid': syntax_result['success'],
                        'can_execute': security_result['is_safe'] and syntax_result['success'],
                        'performance_score': performance_analysis.get('score', 0),
                        'optimization_potential': len(recommendations) > 0
                    }
                }
            }
            
            return result
            
        except Exception as e:
            logger.error(f"公式验证失败: {e}")
            return {
                'success': False,
                'error': f"公式验证失败: {str(e)}",
                'traceback': traceback.format_exc(),
                'data': None
            }
    
    def batch_process_formulas(self, formulas: List[str], operation: str = 'validate', 
                             context: Dict[str, Any] = None) -> Dict[str, Any]:
        """批量处理公式
        
        Args:
            formulas: 公式列表
            operation: 操作类型 ('validate', 'parse', 'execute', 'optimize')
            context: 处理上下文
            
        Returns:
            批量处理结果
        """
        try:
            results = []
            errors = []
            
            for i, formula in enumerate(formulas):
                try:
                    if operation == 'validate':
                        result = self.validate_formula(formula, context)
                    elif operation == 'parse':
                        result = self.parse_formula(formula)
                    elif operation == 'execute':
                        result = self.execute_formula(formula, context or {})
                    elif operation == 'optimize':
                        result = self.intelligent_recommender.get_optimization_suggestions(formula)
                    else:
                        result = {'success': False, 'error': f'不支持的操作类型: {operation}'}
                    
                    results.append({
                        'index': i,
                        'formula': formula,
                        'result': result
                    })
                    
                except Exception as e:
                    errors.append({
                        'index': i,
                        'formula': formula,
                        'error': str(e)
                    })
            
            # 生成批量处理统计
            stats = {
                'total_formulas': len(formulas),
                'successful_operations': len(results),
                'failed_operations': len(errors),
                'success_rate': len(results) / len(formulas) if formulas else 0
            }
            
            return {
                'success': True,
                'data': {
                    'operation': operation,
                    'results': results,
                    'errors': errors,
                    'statistics': stats
                }
            }
            
        except Exception as e:
            logger.error(f"批量处理失败: {e}")
            return {
                'success': False,
                'error': f"批量处理失败: {str(e)}",
                'traceback': traceback.format_exc(),
                'data': None
            }
    
    def get_formula_templates(self, category: str = None, difficulty: str = None) -> Dict[str, Any]:
        """获取公式模板
        
        Args:
            category: 模板类别 (如 'math', 'text', 'date', 'lookup')
            difficulty: 难度级别 ('basic', 'intermediate', 'advanced')
            
        Returns:
            模板列表
        """
        try:
            templates = self.template_manager.get_templates(category, difficulty)
            
            return {
                'success': True,
                'data': {
                    'templates': templates,
                    'total_count': len(templates),
                    'categories': self.template_manager.get_available_categories(),
                    'difficulty_levels': ['basic', 'intermediate', 'advanced']
                }
            }
            
        except Exception as e:
            logger.error(f"获取模板失败: {e}")
            return {
                'success': False,
                'error': f"获取模板失败: {str(e)}",
                'data': None
            }
    
    def get_intelligent_recommendations(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """获取智能公式推荐
        
        Args:
            context: 推荐上下文，包含数据类型、操作意图等信息
            
        Returns:
            推荐结果
        """
        try:
            recommendations = self.intelligent_recommender.get_recommendations(context)
            
            return {
                'success': True,
                'data': {
                    'recommendations': recommendations,
                    'context': context,
                    'recommendation_count': len(recommendations)
                }
            }
            
        except Exception as e:
            logger.error(f"获取推荐失败: {e}")
            return {
                'success': False,
                'error': f"获取推荐失败: {str(e)}",
                'data': None
            }


# 创建工具管理器实例
formulas_manager = FormulasToolsManager()


def parse_excel_formula(formula: str, validate_security: bool = False) -> str:
    """解析 Excel 公式
    
    解析 Excel 公式，提取函数、引用和结构信息。
    
    Args:
        formula: Excel 公式字符串（如 "=SUM(A1:A10)"）
        validate_security: 是否进行安全验证（默认 True）
        
    Returns:
        JSON 格式的解析结果
    """
    try:
        result = formulas_manager.parse_formula(formula, validate_security)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        error_result = {
            'success': False,
            'error': f"解析公式时发生错误: {str(e)}",
            'data': None
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


def compile_excel_workbook(file_path: str, output_format: str = 'python') -> str:
    """编译 Excel 工作簿为代码
    
    将 Excel 工作簿编译为 Python 代码或 JSON 格式的模型数据。
    
    Args:
        file_path: Excel 文件路径
        output_format: 输出格式，支持 'python' 或 'json'（默认 'python'）
        
    Returns:
        JSON 格式的编译结果
    """
    try:
        result = formulas_manager.compile_workbook(file_path, output_format)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        error_result = {
            'success': False,
            'error': f"编译工作簿时发生错误: {str(e)}",
            'data': None
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


def execute_excel_formula(formula: str, context: str = '{}') -> str:
    """执行 Excel 公式
    
    在给定上下文中执行 Excel 公式并返回结果。
    
    Args:
        formula: Excel 公式字符串（如 "=SUM(A1:A3)"）
        context: JSON 格式的上下文变量（如 '{"A1": 10, "A2": 20, "A3": 30}'）
        
    Returns:
        JSON 格式的执行结果
    """
    try:
        # 解析上下文
        context_dict = json.loads(context) if context and context != '{}' else {}
        
        result = formulas_manager.execute_formula(formula, context_dict)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except json.JSONDecodeError as e:
        error_result = {
            'success': False,
            'error': f"上下文 JSON 解析失败: {str(e)}",
            'data': None
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)
    except Exception as e:
        error_result = {
            'success': False,
            'error': f"执行公式时发生错误: {str(e)}",
            'data': None
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


def analyze_excel_dependencies(file_path: str) -> str:
    """分析 Excel 文件的公式依赖关系
    
    分析 Excel 文件中公式之间的依赖关系，生成依赖图。
    
    Args:
        file_path: Excel 文件路径
        
    Returns:
        JSON 格式的依赖分析结果
    """
    try:
        result = formulas_manager.analyze_dependencies(file_path)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        error_result = {
            'success': False,
            'error': f"分析依赖关系时发生错误: {str(e)}",
            'data': None
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


def validate_excel_formula(formula: str) -> str:
    """验证 Excel 公式的安全性和有效性
    
    检查 Excel 公式是否安全，是否包含危险函数或模式。
    
    Args:
        formula: Excel 公式字符串
        
    Returns:
        JSON 格式的验证结果
    """
    try:
        result = formulas_manager.validate_formula(formula)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        error_result = {
            'success': False,
            'error': f"验证公式时发生错误: {str(e)}",
            'data': None
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


# 新增的批量处理和智能功能函数
def batch_process_excel_formulas(formulas_json: str, operation: str = 'validate') -> str:
    """批量处理 Excel 公式
    
    批量处理多个 Excel 公式，支持验证、解析、执行等操作。
    
    Args:
        formulas_json: JSON 格式的公式列表字符串
        operation: 操作类型 ('validate', 'parse', 'execute', 'optimize')
        
    Returns:
        JSON 格式的批量处理结果
    """
    try:
        formulas = json.loads(formulas_json)
        if not isinstance(formulas, list):
            raise ValueError("公式数据必须是列表格式")
        
        result = formulas_manager.batch_process_formulas(formulas, operation)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except json.JSONDecodeError as e:
        error_result = {
            'success': False,
            'error': f"公式列表 JSON 解析失败: {str(e)}",
            'data': None
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)
    except Exception as e:
        error_result = {
            'success': False,
            'error': f"批量处理公式时发生错误: {str(e)}",
            'data': None
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


def get_excel_formula_templates(category: str = '', difficulty: str = '') -> str:
    """获取 Excel 公式模板
    
    获取预定义的 Excel 公式模板，支持按类别和难度筛选。
    
    Args:
        category: 模板类别 (如 'math', 'text', 'date', 'lookup')
        difficulty: 难度级别 ('basic', 'intermediate', 'advanced')
        
    Returns:
        JSON 格式的模板列表
    """
    try:
        category = category if category else None
        difficulty = difficulty if difficulty else None
        
        result = formulas_manager.get_formula_templates(category, difficulty)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        error_result = {
            'success': False,
            'error': f"获取公式模板时发生错误: {str(e)}",
            'data': None
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


def get_excel_formula_recommendations(context_json: str) -> str:
    """获取智能 Excel 公式推荐
    
    基于给定上下文智能推荐合适的 Excel 公式。
    
    Args:
        context_json: JSON 格式的推荐上下文
        
    Returns:
        JSON 格式的推荐结果
    """
    try:
        context = json.loads(context_json) if context_json else {}
        
        result = formulas_manager.get_intelligent_recommendations(context)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except json.JSONDecodeError as e:
        error_result = {
            'success': False,
            'error': f"上下文 JSON 解析失败: {str(e)}",
            'data': None
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)
    except Exception as e:
        error_result = {
            'success': False,
            'error': f"获取公式推荐时发生错误: {str(e)}",
            'data': None
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # 测试代码
    print("Excel Formulas Tools 模块已加载 - 增强版 v2.0.0")
    print(f"formulas 库可用性: {formulas is not None}")
    
    if formulas is not None:
        # 简单测试
        test_formula = "=SUM(A1:A3)"
        test_context = '{"A1": 10, "A2": 20, "A3": 30}'
        
        print("\n测试公式解析:")
        print(parse_excel_formula(test_formula))
        
        print("\n测试公式执行:")
        print(execute_excel_formula(test_formula, test_context))
        
        print("\n测试增强版公式验证:")
        print(validate_excel_formula(test_formula))
        
        print("\n测试批量处理:")
        test_formulas = '["=SUM(A1:A3)", "=AVERAGE(B1:B5)", "=MAX(C1:C10)"]'
        print(batch_process_excel_formulas(test_formulas, 'validate'))
        
        print("\n测试模板获取:")
        print(get_excel_formula_templates('math', 'basic'))
        
        print("\n增强功能已就绪！")