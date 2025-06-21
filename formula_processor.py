#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公式处理模块
提供Excel公式解析、验证和执行功能
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
import re
import ast
import operator
from datetime import datetime, date, timedelta
import math
import warnings
from dataclasses import dataclass
from enum import Enum

class FormulaType(Enum):
    """公式类型"""
    ARITHMETIC = "arithmetic"  # 算术公式
    LOGICAL = "logical"       # 逻辑公式
    TEXT = "text"             # 文本公式
    DATE = "date"             # 日期公式
    LOOKUP = "lookup"         # 查找公式
    STATISTICAL = "statistical"  # 统计公式
    FINANCIAL = "financial"   # 财务公式
    CUSTOM = "custom"         # 自定义公式

@dataclass
class FormulaResult:
    """公式执行结果"""
    success: bool
    result: Any
    formula: str
    formula_type: FormulaType
    execution_time: float
    error_message: Optional[str] = None
    warnings: Optional[List[str]] = None
    dependencies: Optional[List[str]] = None

class FormulaProcessor:
    """公式处理器"""
    
    def __init__(self, df: Optional[pd.DataFrame] = None):
        self.df = df
        self.variables = {}
        self.functions = {}
        self._register_builtin_functions()
        self._operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '//': operator.floordiv,
            '%': operator.mod,
            '**': operator.pow,
            '==': operator.eq,
            '!=': operator.ne,
            '<': operator.lt,
            '<=': operator.le,
            '>': operator.gt,
            '>=': operator.ge,
            '&': operator.and_,
            '|': operator.or_,
            '^': operator.xor
        }
    
    def set_dataframe(self, df: pd.DataFrame) -> None:
        """设置DataFrame"""
        self.df = df
        # 自动将列名添加到变量中
        for col in df.columns:
            self.variables[str(col)] = df[col]
    
    def _register_builtin_functions(self) -> None:
        """注册内置函数"""
        # 数学函数
        self.functions.update({
            'SUM': self._sum,
            'AVERAGE': self._average,
            'COUNT': self._count,
            'MAX': self._max,
            'MIN': self._min,
            'ROUND': self._round,
            'ABS': self._abs,
            'SQRT': self._sqrt,
            'POWER': self._power,
            'LOG': self._log,
            'EXP': self._exp,
            'SIN': self._sin,
            'COS': self._cos,
            'TAN': self._tan
        })
        
        # 逻辑函数
        self.functions.update({
            'IF': self._if,
            'AND': self._and,
            'OR': self._or,
            'NOT': self._not,
            'ISNULL': self._isnull,
            'ISNA': self._isna,
            'ISNUMBER': self._isnumber,
            'ISTEXT': self._istext
        })
        
        # 文本函数
        self.functions.update({
            'LEN': self._len,
            'LEFT': self._left,
            'RIGHT': self._right,
            'MID': self._mid,
            'UPPER': self._upper,
            'LOWER': self._lower,
            'TRIM': self._trim,
            'CONCATENATE': self._concatenate,
            'FIND': self._find,
            'SUBSTITUTE': self._substitute
        })
        
        # 日期函数
        self.functions.update({
            'TODAY': self._today,
            'NOW': self._now,
            'YEAR': self._year,
            'MONTH': self._month,
            'DAY': self._day,
            'HOUR': self._hour,
            'MINUTE': self._minute,
            'SECOND': self._second,
            'DATE': self._date,
            'DATEDIF': self._datedif
        })
        
        # 查找函数
        self.functions.update({
            'VLOOKUP': self._vlookup,
            'HLOOKUP': self._hlookup,
            'INDEX': self._index,
            'MATCH': self._match
        })
        
        # 统计函数
        self.functions.update({
            'MEDIAN': self._median,
            'MODE': self._mode,
            'STDEV': self._stdev,
            'VAR': self._var,
            'PERCENTILE': self._percentile,
            'QUARTILE': self._quartile,
            'CORREL': self._correl
        })
    
    def parse_formula(self, formula: str) -> Dict[str, Any]:
        """解析公式"""
        try:
            # 清理公式
            formula = formula.strip()
            if formula.startswith('='):
                formula = formula[1:]
            
            # 检测公式类型
            formula_type = self._detect_formula_type(formula)
            
            # 提取依赖项
            dependencies = self._extract_dependencies(formula)
            
            # 验证公式语法
            validation_result = self._validate_formula_syntax(formula)
            
            return {
                'success': True,
                'formula': formula,
                'formula_type': formula_type,
                'dependencies': dependencies,
                'validation': validation_result,
                'message': '公式解析成功'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'公式解析失败: {str(e)}',
                'formula': formula
            }
    
    def execute_formula(self, formula: str, context: Optional[Dict[str, Any]] = None) -> FormulaResult:
        """执行公式"""
        start_time = datetime.now()
        
        try:
            # 解析公式
            parse_result = self.parse_formula(formula)
            if not parse_result['success']:
                return FormulaResult(
                    success=False,
                    result=None,
                    formula=formula,
                    formula_type=FormulaType.CUSTOM,
                    execution_time=0,
                    error_message=parse_result['error']
                )
            
            # 设置执行上下文
            if context:
                self.variables.update(context)
            
            # 执行公式
            result = self._evaluate_expression(formula)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return FormulaResult(
                success=True,
                result=result,
                formula=formula,
                formula_type=parse_result['formula_type'],
                execution_time=execution_time,
                dependencies=parse_result['dependencies']
            )
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return FormulaResult(
                success=False,
                result=None,
                formula=formula,
                formula_type=FormulaType.CUSTOM,
                execution_time=execution_time,
                error_message=str(e)
            )
    
    def _detect_formula_type(self, formula: str) -> FormulaType:
        """检测公式类型"""
        formula_upper = formula.upper()
        
        # 统计函数
        if any(func in formula_upper for func in ['SUM', 'AVERAGE', 'COUNT', 'MAX', 'MIN', 'MEDIAN', 'STDEV']):
            return FormulaType.STATISTICAL
        
        # 逻辑函数
        if any(func in formula_upper for func in ['IF', 'AND', 'OR', 'NOT']):
            return FormulaType.LOGICAL
        
        # 文本函数
        if any(func in formula_upper for func in ['LEN', 'LEFT', 'RIGHT', 'UPPER', 'LOWER', 'CONCATENATE']):
            return FormulaType.TEXT
        
        # 日期函数
        if any(func in formula_upper for func in ['TODAY', 'NOW', 'YEAR', 'MONTH', 'DAY', 'DATE']):
            return FormulaType.DATE
        
        # 查找函数
        if any(func in formula_upper for func in ['VLOOKUP', 'HLOOKUP', 'INDEX', 'MATCH']):
            return FormulaType.LOOKUP
        
        # 算术运算
        if any(op in formula for op in ['+', '-', '*', '/', '**']):
            return FormulaType.ARITHMETIC
        
        return FormulaType.CUSTOM
    
    def _extract_dependencies(self, formula: str) -> List[str]:
        """提取公式依赖项"""
        dependencies = []
        
        # 提取列名引用
        if self.df is not None:
            for col in self.df.columns:
                if str(col) in formula:
                    dependencies.append(str(col))
        
        # 提取单元格引用（如A1, B2等）
        cell_pattern = r'\b[A-Z]+\d+\b'
        cell_refs = re.findall(cell_pattern, formula)
        dependencies.extend(cell_refs)
        
        # 提取范围引用（如A1:B10）
        range_pattern = r'\b[A-Z]+\d+:[A-Z]+\d+\b'
        range_refs = re.findall(range_pattern, formula)
        dependencies.extend(range_refs)
        
        return list(set(dependencies))
    
    def _validate_formula_syntax(self, formula: str) -> Dict[str, Any]:
        """验证公式语法"""
        errors = []
        warnings = []
        
        # 检查括号匹配
        if formula.count('(') != formula.count(')'):
            errors.append("括号不匹配")
        
        # 检查引号匹配
        if formula.count('"') % 2 != 0:
            errors.append("引号不匹配")
        
        # 检查函数名
        function_pattern = r'\b([A-Z]+)\s*\('
        functions_used = re.findall(function_pattern, formula.upper())
        
        for func in functions_used:
            if func not in self.functions:
                warnings.append(f"未知函数: {func}")
        
        # 检查除零
        if '/0' in formula.replace(' ', ''):
            warnings.append("可能存在除零错误")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def _evaluate_expression(self, expression: str) -> Any:
        """评估表达式"""
        # 替换函数调用
        expression = self._replace_function_calls(expression)
        
        # 替换变量
        expression = self._replace_variables(expression)
        
        # 安全评估
        try:
            # 使用ast.literal_eval进行安全评估
            return ast.literal_eval(expression)
        except (ValueError, SyntaxError):
            # 如果literal_eval失败，尝试使用eval（需要更多安全检查）
            return self._safe_eval(expression)
    
    def _replace_function_calls(self, expression: str) -> str:
        """替换函数调用"""
        # 这里需要实现函数调用的替换逻辑
        # 简化实现，实际需要更复杂的解析
        for func_name, func in self.functions.items():
            pattern = rf'\b{func_name}\s*\(([^)]+)\)'
            matches = re.finditer(pattern, expression, re.IGNORECASE)
            
            for match in reversed(list(matches)):
                args_str = match.group(1)
                args = [arg.strip() for arg in args_str.split(',')]
                
                try:
                    result = func(*args)
                    expression = expression[:match.start()] + str(result) + expression[match.end():]
                except Exception as e:
                    raise ValueError(f"函数 {func_name} 执行失败: {str(e)}")
        
        return expression
    
    def _replace_variables(self, expression: str) -> str:
        """替换变量"""
        for var_name, var_value in self.variables.items():
            if var_name in expression:
                # 简化实现，实际需要更精确的替换
                if isinstance(var_value, pd.Series):
                    # 对于Series，可能需要特殊处理
                    continue
                else:
                    expression = expression.replace(var_name, str(var_value))
        
        return expression
    
    def _safe_eval(self, expression: str) -> Any:
        """安全的表达式评估"""
        # 创建安全的命名空间
        safe_dict = {
            '__builtins__': {},
            'abs': abs,
            'max': max,
            'min': min,
            'sum': sum,
            'len': len,
            'round': round,
            'int': int,
            'float': float,
            'str': str,
            'bool': bool
        }
        
        # 添加数学函数
        safe_dict.update({
            'sqrt': math.sqrt,
            'pow': math.pow,
            'log': math.log,
            'exp': math.exp,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'pi': math.pi,
            'e': math.e
        })
        
        return eval(expression, safe_dict)
    
    # 内置函数实现
    def _sum(self, *args) -> float:
        """SUM函数"""
        values = []
        for arg in args:
            if isinstance(arg, str) and arg in self.variables:
                var = self.variables[arg]
                if isinstance(var, pd.Series):
                    values.extend(var.dropna().tolist())
                else:
                    values.append(float(var))
            else:
                values.append(float(arg))
        return sum(values)
    
    def _average(self, *args) -> float:
        """AVERAGE函数"""
        total = self._sum(*args)
        count = self._count(*args)
        return total / count if count > 0 else 0
    
    def _count(self, *args) -> int:
        """COUNT函数"""
        count = 0
        for arg in args:
            if isinstance(arg, str) and arg in self.variables:
                var = self.variables[arg]
                if isinstance(var, pd.Series):
                    count += var.notna().sum()
                else:
                    count += 1
            else:
                count += 1
        return count
    
    def _max(self, *args) -> float:
        """MAX函数"""
        values = []
        for arg in args:
            if isinstance(arg, str) and arg in self.variables:
                var = self.variables[arg]
                if isinstance(var, pd.Series):
                    values.extend(var.dropna().tolist())
                else:
                    values.append(float(var))
            else:
                values.append(float(arg))
        return max(values) if values else 0
    
    def _min(self, *args) -> float:
        """MIN函数"""
        values = []
        for arg in args:
            if isinstance(arg, str) and arg in self.variables:
                var = self.variables[arg]
                if isinstance(var, pd.Series):
                    values.extend(var.dropna().tolist())
                else:
                    values.append(float(var))
            else:
                values.append(float(arg))
        return min(values) if values else 0
    
    def _round(self, value, digits=0) -> float:
        """ROUND函数"""
        return round(float(value), int(digits))
    
    def _abs(self, value) -> float:
        """ABS函数"""
        return abs(float(value))
    
    def _sqrt(self, value) -> float:
        """SQRT函数"""
        return math.sqrt(float(value))
    
    def _power(self, base, exponent) -> float:
        """POWER函数"""
        return math.pow(float(base), float(exponent))
    
    def _log(self, value, base=math.e) -> float:
        """LOG函数"""
        if base == math.e:
            return math.log(float(value))
        else:
            return math.log(float(value), float(base))
    
    def _exp(self, value) -> float:
        """EXP函数"""
        return math.exp(float(value))
    
    def _sin(self, value) -> float:
        """SIN函数"""
        return math.sin(float(value))
    
    def _cos(self, value) -> float:
        """COS函数"""
        return math.cos(float(value))
    
    def _tan(self, value) -> float:
        """TAN函数"""
        return math.tan(float(value))
    
    def _if(self, condition, true_value, false_value) -> Any:
        """IF函数"""
        # 简化实现
        if str(condition).lower() in ['true', '1', 'yes']:
            return true_value
        else:
            return false_value
    
    def _and(self, *args) -> bool:
        """AND函数"""
        return all(str(arg).lower() in ['true', '1', 'yes'] for arg in args)
    
    def _or(self, *args) -> bool:
        """OR函数"""
        return any(str(arg).lower() in ['true', '1', 'yes'] for arg in args)
    
    def _not(self, value) -> bool:
        """NOT函数"""
        return not (str(value).lower() in ['true', '1', 'yes'])
    
    def _isnull(self, value) -> bool:
        """ISNULL函数"""
        return pd.isna(value)
    
    def _isna(self, value) -> bool:
        """ISNA函数"""
        return pd.isna(value)
    
    def _isnumber(self, value) -> bool:
        """ISNUMBER函数"""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False
    
    def _istext(self, value) -> bool:
        """ISTEXT函数"""
        return isinstance(value, str)
    
    def _len(self, text) -> int:
        """LEN函数"""
        return len(str(text))
    
    def _left(self, text, num_chars) -> str:
        """LEFT函数"""
        return str(text)[:int(num_chars)]
    
    def _right(self, text, num_chars) -> str:
        """RIGHT函数"""
        return str(text)[-int(num_chars):]
    
    def _mid(self, text, start_pos, num_chars) -> str:
        """MID函数"""
        start = int(start_pos) - 1  # Excel使用1基索引
        return str(text)[start:start + int(num_chars)]
    
    def _upper(self, text) -> str:
        """UPPER函数"""
        return str(text).upper()
    
    def _lower(self, text) -> str:
        """LOWER函数"""
        return str(text).lower()
    
    def _trim(self, text) -> str:
        """TRIM函数"""
        return str(text).strip()
    
    def _concatenate(self, *args) -> str:
        """CONCATENATE函数"""
        return ''.join(str(arg) for arg in args)
    
    def _find(self, find_text, within_text, start_pos=1) -> int:
        """FIND函数"""
        start = int(start_pos) - 1
        result = str(within_text).find(str(find_text), start)
        return result + 1 if result != -1 else -1  # Excel使用1基索引
    
    def _substitute(self, text, old_text, new_text, instance_num=None) -> str:
        """SUBSTITUTE函数"""
        text_str = str(text)
        old_str = str(old_text)
        new_str = str(new_text)
        
        if instance_num is None:
            return text_str.replace(old_str, new_str)
        else:
            # 替换指定的实例
            parts = text_str.split(old_str)
            if len(parts) > int(instance_num):
                parts[int(instance_num)] = new_str
                return old_str.join(parts[:int(instance_num)]) + new_str + old_str.join(parts[int(instance_num)+1:])
            return text_str
    
    def _today(self) -> date:
        """TODAY函数"""
        return date.today()
    
    def _now(self) -> datetime:
        """NOW函数"""
        return datetime.now()
    
    def _year(self, date_value) -> int:
        """YEAR函数"""
        if isinstance(date_value, (date, datetime)):
            return date_value.year
        else:
            dt = pd.to_datetime(date_value)
            return dt.year
    
    def _month(self, date_value) -> int:
        """MONTH函数"""
        if isinstance(date_value, (date, datetime)):
            return date_value.month
        else:
            dt = pd.to_datetime(date_value)
            return dt.month
    
    def _day(self, date_value) -> int:
        """DAY函数"""
        if isinstance(date_value, (date, datetime)):
            return date_value.day
        else:
            dt = pd.to_datetime(date_value)
            return dt.day
    
    def _hour(self, time_value) -> int:
        """HOUR函数"""
        if isinstance(time_value, datetime):
            return time_value.hour
        else:
            dt = pd.to_datetime(time_value)
            return dt.hour
    
    def _minute(self, time_value) -> int:
        """MINUTE函数"""
        if isinstance(time_value, datetime):
            return time_value.minute
        else:
            dt = pd.to_datetime(time_value)
            return dt.minute
    
    def _second(self, time_value) -> int:
        """SECOND函数"""
        if isinstance(time_value, datetime):
            return time_value.second
        else:
            dt = pd.to_datetime(time_value)
            return dt.second
    
    def _date(self, year, month, day) -> date:
        """DATE函数"""
        return date(int(year), int(month), int(day))
    
    def _datedif(self, start_date, end_date, unit) -> int:
        """DATEDIF函数"""
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        
        if unit.upper() == 'D':
            return (end - start).days
        elif unit.upper() == 'M':
            return (end.year - start.year) * 12 + (end.month - start.month)
        elif unit.upper() == 'Y':
            return end.year - start.year
        else:
            raise ValueError(f"不支持的日期单位: {unit}")
    
    def _vlookup(self, lookup_value, table_array, col_index, range_lookup=True):
        """VLOOKUP函数（简化实现）"""
        # 这里需要更复杂的实现
        raise NotImplementedError("VLOOKUP函数需要进一步实现")
    
    def _hlookup(self, lookup_value, table_array, row_index, range_lookup=True):
        """HLOOKUP函数（简化实现）"""
        # 这里需要更复杂的实现
        raise NotImplementedError("HLOOKUP函数需要进一步实现")
    
    def _index(self, array, row_num, col_num=None):
        """INDEX函数（简化实现）"""
        # 这里需要更复杂的实现
        raise NotImplementedError("INDEX函数需要进一步实现")
    
    def _match(self, lookup_value, lookup_array, match_type=1):
        """MATCH函数（简化实现）"""
        # 这里需要更复杂的实现
        raise NotImplementedError("MATCH函数需要进一步实现")
    
    def _median(self, *args) -> float:
        """MEDIAN函数"""
        values = []
        for arg in args:
            if isinstance(arg, str) and arg in self.variables:
                var = self.variables[arg]
                if isinstance(var, pd.Series):
                    values.extend(var.dropna().tolist())
                else:
                    values.append(float(var))
            else:
                values.append(float(arg))
        return np.median(values) if values else 0
    
    def _mode(self, *args) -> float:
        """MODE函数"""
        values = []
        for arg in args:
            if isinstance(arg, str) and arg in self.variables:
                var = self.variables[arg]
                if isinstance(var, pd.Series):
                    values.extend(var.dropna().tolist())
                else:
                    values.append(float(var))
            else:
                values.append(float(arg))
        
        if values:
            from scipy import stats
            mode_result = stats.mode(values)
            return mode_result.mode[0] if len(mode_result.mode) > 0 else 0
        return 0
    
    def _stdev(self, *args) -> float:
        """STDEV函数"""
        values = []
        for arg in args:
            if isinstance(arg, str) and arg in self.variables:
                var = self.variables[arg]
                if isinstance(var, pd.Series):
                    values.extend(var.dropna().tolist())
                else:
                    values.append(float(var))
            else:
                values.append(float(arg))
        return np.std(values, ddof=1) if len(values) > 1 else 0
    
    def _var(self, *args) -> float:
        """VAR函数"""
        values = []
        for arg in args:
            if isinstance(arg, str) and arg in self.variables:
                var = self.variables[arg]
                if isinstance(var, pd.Series):
                    values.extend(var.dropna().tolist())
                else:
                    values.append(float(var))
            else:
                values.append(float(arg))
        return np.var(values, ddof=1) if len(values) > 1 else 0
    
    def _percentile(self, array, k) -> float:
        """PERCENTILE函数"""
        if isinstance(array, str) and array in self.variables:
            var = self.variables[array]
            if isinstance(var, pd.Series):
                values = var.dropna().tolist()
            else:
                values = [float(var)]
        else:
            values = [float(array)]
        
        return np.percentile(values, float(k)) if values else 0
    
    def _quartile(self, array, quart) -> float:
        """QUARTILE函数"""
        quartile_map = {0: 0, 1: 25, 2: 50, 3: 75, 4: 100}
        percentile = quartile_map.get(int(quart), 50)
        return self._percentile(array, percentile)
    
    def _correl(self, array1, array2) -> float:
        """CORREL函数"""
        # 简化实现
        if (isinstance(array1, str) and array1 in self.variables and 
            isinstance(array2, str) and array2 in self.variables):
            var1 = self.variables[array1]
            var2 = self.variables[array2]
            if isinstance(var1, pd.Series) and isinstance(var2, pd.Series):
                return var1.corr(var2)
        return 0

def create_formula_processor(df: Optional[pd.DataFrame] = None) -> FormulaProcessor:
    """创建公式处理器实例"""
    return FormulaProcessor(df)