# -*- coding: utf-8 -*-
"""
数据验证引擎模块
提供数据处理结果验证和数据验证引擎功能
"""

from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import pandas as pd
import numpy as np
from enum import Enum

class VerificationLevel(Enum):
    """验证级别枚举"""
    BASIC = "basic"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"
    STRICT = "strict"

class VerificationStatus(Enum):
    """验证状态枚举"""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"

@dataclass
class VerificationResult:
    """验证结果数据类"""
    status: VerificationStatus
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "status": self.status.value,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat()
        }

class DataVerificationEngine:
    """数据验证引擎"""
    
    def __init__(self, level: VerificationLevel = VerificationLevel.STANDARD):
        """初始化验证引擎
        
        Args:
            level: 验证级别
        """
        self.level = level
        self.rules = []
        self.results = []
        
    def add_rule(self, rule_name: str, rule_func, **kwargs):
        """添加验证规则
        
        Args:
            rule_name: 规则名称
            rule_func: 规则函数
            **kwargs: 规则参数
        """
        self.rules.append({
            "name": rule_name,
            "function": rule_func,
            "params": kwargs
        })
    
    def verify_data_structure(self, data: pd.DataFrame) -> VerificationResult:
        """验证数据结构
        
        Args:
            data: 待验证的DataFrame
            
        Returns:
            验证结果
        """
        try:
            if data is None or data.empty:
                return VerificationResult(
                    status=VerificationStatus.FAILED,
                    message="数据为空或None",
                    details={"row_count": 0, "column_count": 0}
                )
            
            details = {
                "row_count": len(data),
                "column_count": len(data.columns),
                "columns": list(data.columns),
                "dtypes": data.dtypes.to_dict(),
                "memory_usage": data.memory_usage(deep=True).sum()
            }
            
            return VerificationResult(
                status=VerificationStatus.PASSED,
                message="数据结构验证通过",
                details=details
            )
            
        except Exception as e:
            return VerificationResult(
                status=VerificationStatus.FAILED,
                message=f"数据结构验证失败: {str(e)}",
                details={"error": str(e)}
            )
    
    def verify_data_quality(self, data: pd.DataFrame) -> VerificationResult:
        """验证数据质量
        
        Args:
            data: 待验证的DataFrame
            
        Returns:
            验证结果
        """
        try:
            issues = []
            
            # 检查缺失值
            missing_counts = data.isnull().sum()
            if missing_counts.sum() > 0:
                issues.append({
                    "type": "missing_values",
                    "count": int(missing_counts.sum()),
                    "columns": missing_counts[missing_counts > 0].to_dict()
                })
            
            # 检查重复行
            duplicate_count = data.duplicated().sum()
            if duplicate_count > 0:
                issues.append({
                    "type": "duplicate_rows",
                    "count": int(duplicate_count)
                })
            
            # 检查数据类型一致性
            for col in data.columns:
                if data[col].dtype == 'object':
                    unique_types = set(type(x).__name__ for x in data[col].dropna())
                    if len(unique_types) > 1:
                        issues.append({
                            "type": "mixed_types",
                            "column": col,
                            "types": list(unique_types)
                        })
            
            status = VerificationStatus.PASSED if not issues else VerificationStatus.WARNING
            message = "数据质量验证通过" if not issues else f"发现 {len(issues)} 个质量问题"
            
            return VerificationResult(
                status=status,
                message=message,
                details={"issues": issues, "total_issues": len(issues)}
            )
            
        except Exception as e:
            return VerificationResult(
                status=VerificationStatus.FAILED,
                message=f"数据质量验证失败: {str(e)}",
                details={"error": str(e)}
            )
    
    def verify_data_integrity(self, data: pd.DataFrame, constraints: Dict[str, Any] = None) -> VerificationResult:
        """验证数据完整性
        
        Args:
            data: 待验证的DataFrame
            constraints: 约束条件
            
        Returns:
            验证结果
        """
        try:
            violations = []
            constraints = constraints or {}
            
            # 检查必需列
            required_columns = constraints.get('required_columns', [])
            missing_columns = [col for col in required_columns if col not in data.columns]
            if missing_columns:
                violations.append({
                    "type": "missing_required_columns",
                    "columns": missing_columns
                })
            
            # 检查数据范围
            range_constraints = constraints.get('ranges', {})
            for col, (min_val, max_val) in range_constraints.items():
                if col in data.columns and pd.api.types.is_numeric_dtype(data[col]):
                    out_of_range = ((data[col] < min_val) | (data[col] > max_val)).sum()
                    if out_of_range > 0:
                        violations.append({
                            "type": "out_of_range",
                            "column": col,
                            "count": int(out_of_range),
                            "range": [min_val, max_val]
                        })
            
            status = VerificationStatus.PASSED if not violations else VerificationStatus.FAILED
            message = "数据完整性验证通过" if not violations else f"发现 {len(violations)} 个完整性违规"
            
            return VerificationResult(
                status=status,
                message=message,
                details={"violations": violations, "total_violations": len(violations)}
            )
            
        except Exception as e:
            return VerificationResult(
                status=VerificationStatus.FAILED,
                message=f"数据完整性验证失败: {str(e)}",
                details={"error": str(e)}
            )
    
    def run_verification(self, data: pd.DataFrame, constraints: Dict[str, Any] = None) -> Dict[str, Any]:
        """运行完整验证流程
        
        Args:
            data: 待验证的DataFrame
            constraints: 约束条件
            
        Returns:
            完整验证结果
        """
        results = {
            "structure": self.verify_data_structure(data),
            "quality": self.verify_data_quality(data),
            "integrity": self.verify_data_integrity(data, constraints)
        }
        
        # 运行自定义规则
        custom_results = {}
        for rule in self.rules:
            try:
                result = rule["function"](data, **rule["params"])
                custom_results[rule["name"]] = result
            except Exception as e:
                custom_results[rule["name"]] = VerificationResult(
                    status=VerificationStatus.FAILED,
                    message=f"规则执行失败: {str(e)}",
                    details={"error": str(e)}
                )
        
        if custom_results:
            results["custom_rules"] = custom_results
        
        # 计算总体状态
        all_results = list(results.values())
        if isinstance(results.get("custom_rules"), dict):
            all_results.extend(results["custom_rules"].values())
        
        failed_count = sum(1 for r in all_results if r.status == VerificationStatus.FAILED)
        warning_count = sum(1 for r in all_results if r.status == VerificationStatus.WARNING)
        
        if failed_count > 0:
            overall_status = VerificationStatus.FAILED
        elif warning_count > 0:
            overall_status = VerificationStatus.WARNING
        else:
            overall_status = VerificationStatus.PASSED
        
        return {
            "overall_status": overall_status.value,
            "summary": {
                "total_checks": len(all_results),
                "passed": sum(1 for r in all_results if r.status == VerificationStatus.PASSED),
                "failed": failed_count,
                "warnings": warning_count
            },
            "results": {k: v.to_dict() for k, v in results.items() if not isinstance(v, dict)},
            "custom_results": {k: v.to_dict() for k, v in results.get("custom_rules", {}).items()},
            "timestamp": datetime.now().isoformat()
        }

def verify_data_processing_result(
    original_data: pd.DataFrame,
    processed_data: pd.DataFrame,
    operation: str,
    expected_changes: Dict[str, Any] = None
) -> Dict[str, Any]:
    """验证数据处理结果
    
    Args:
        original_data: 原始数据
        processed_data: 处理后数据
        operation: 操作类型
        expected_changes: 预期变化
        
    Returns:
        验证结果字典
    """
    try:
        verification_results = {
            "operation": operation,
            "timestamp": datetime.now().isoformat(),
            "status": "success",
            "checks": {},
            "summary": {},
            "issues": []
        }
        
        # 基本数据检查
        if original_data is None or processed_data is None:
            verification_results["status"] = "failed"
            verification_results["issues"].append("原始数据或处理后数据为None")
            return verification_results
        
        # 数据形状检查
        orig_shape = original_data.shape
        proc_shape = processed_data.shape
        
        verification_results["checks"]["shape_change"] = {
            "original": orig_shape,
            "processed": proc_shape,
            "row_change": proc_shape[0] - orig_shape[0],
            "column_change": proc_shape[1] - orig_shape[1]
        }
        
        # 列名检查
        orig_columns = set(original_data.columns)
        proc_columns = set(processed_data.columns)
        
        verification_results["checks"]["columns"] = {
            "original_columns": list(orig_columns),
            "processed_columns": list(proc_columns),
            "added_columns": list(proc_columns - orig_columns),
            "removed_columns": list(orig_columns - proc_columns),
            "common_columns": list(orig_columns & proc_columns)
        }
        
        # 数据类型检查
        common_columns = orig_columns & proc_columns
        dtype_changes = {}
        for col in common_columns:
            orig_dtype = str(original_data[col].dtype)
            proc_dtype = str(processed_data[col].dtype)
            if orig_dtype != proc_dtype:
                dtype_changes[col] = {
                    "original": orig_dtype,
                    "processed": proc_dtype
                }
        
        verification_results["checks"]["dtype_changes"] = dtype_changes
        
        # 缺失值检查
        orig_nulls = original_data.isnull().sum().sum()
        proc_nulls = processed_data.isnull().sum().sum()
        
        verification_results["checks"]["null_values"] = {
            "original_nulls": int(orig_nulls),
            "processed_nulls": int(proc_nulls),
            "null_change": int(proc_nulls - orig_nulls)
        }
        
        # 重复行检查
        orig_duplicates = original_data.duplicated().sum()
        proc_duplicates = processed_data.duplicated().sum()
        
        verification_results["checks"]["duplicates"] = {
            "original_duplicates": int(orig_duplicates),
            "processed_duplicates": int(proc_duplicates),
            "duplicate_change": int(proc_duplicates - orig_duplicates)
        }
        
        # 预期变化验证
        if expected_changes:
            expected_results = {}
            for key, expected_value in expected_changes.items():
                if key in verification_results["checks"]:
                    actual_value = verification_results["checks"][key]
                    expected_results[key] = {
                        "expected": expected_value,
                        "actual": actual_value,
                        "matches": actual_value == expected_value
                    }
            verification_results["expected_validation"] = expected_results
        
        # 生成摘要
        verification_results["summary"] = {
            "data_preserved": len(common_columns) > 0,
            "structure_changed": orig_shape != proc_shape,
            "columns_modified": len(dtype_changes) > 0,
            "quality_improved": proc_nulls < orig_nulls or proc_duplicates < orig_duplicates
        }
        
        return verification_results
        
    except Exception as e:
        return {
            "operation": operation,
            "timestamp": datetime.now().isoformat(),
            "status": "error",
            "error": str(e),
            "checks": {},
            "summary": {},
            "issues": [f"验证过程出错: {str(e)}"]
        }