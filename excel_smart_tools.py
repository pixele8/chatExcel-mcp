"""Excel智能工具函数 - 作为MCP工具提供给用户"""
from excel_helper import _suggest_excel_read_parameters, detect_excel_structure

def suggest_excel_read_parameters(file_path: str, sheet_name: str = None) -> dict:
    """智能分析Excel文件并推荐最佳读取参数
    
    Args:
        file_path: Excel文件的绝对路径
        sheet_name: 可选，工作表名称。如果为None，分析第一个工作表
        
    Returns:
        dict: 包含推荐参数、分析结果、警告和提示的详细信息
    """
    try:
        return _suggest_excel_read_parameters(file_path, sheet_name)
    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e),
            "recommended_params": {"header": 0},  # 默认参数
            "tips": ["发生错误，建议使用默认参数"]
        }

def detect_excel_file_structure(file_path: str, sheet_name: str = None) -> dict:
    """检测Excel文件的详细结构信息
    
    Args:
        file_path: Excel文件的绝对路径
        sheet_name: 可选，工作表名称。如果为None，分析所有工作表
        
    Returns:
        dict: 详细的Excel文件结构信息，包括工作表、合并单元格、数据范围等
    """
    try:
        return detect_excel_structure(file_path, sheet_name)
    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e),
            "message": "无法分析Excel文件结构"
        }

def create_excel_read_template(file_path: str, sheet_name: str = None, skiprows: int = None, header: int = None, usecols: str = None) -> dict:
    """为Excel文件创建读取代码模板
    
    Args:
        file_path: Excel文件的绝对路径
        sheet_name: 可选，工作表名称
        skiprows: 可选，跳过的行数
        header: 可选，标题行位置
        usecols: 可选，使用的列
        
    Returns:
        dict: 包含推荐的Excel读取代码模板
    """
    try:
        suggestions = _suggest_excel_read_parameters(file_path, sheet_name)
        recommended_params = suggestions.get("recommended_params", {})
        
        # 合并用户提供的参数和智能推荐的参数，用户参数优先
        final_params = {}
        
        # 首先收集用户提供的参数
        user_params = {}
        if sheet_name is not None:
            user_params['sheet_name'] = sheet_name
        if skiprows is not None:
            user_params['skiprows'] = skiprows
        if header is not None:
            user_params['header'] = header
        if usecols is not None:
            user_params['usecols'] = usecols
        
        # 先添加智能推荐的参数
        final_params.update(recommended_params)
        
        # 然后用用户提供的参数覆盖（用户参数优先）
        final_params.update(user_params)
        
        # 构建代码模板
        code_lines = ["import pandas as pd", ""]
        
        # 基础读取代码
        params_str = ""
        if final_params:
            param_parts = []
            for key, value in final_params.items():
                if key == 'sheet_name':  # sheet_name在pd.read_excel中单独处理
                    continue
                if isinstance(value, str):
                    param_parts.append(f"{key}='{value}'")
                elif isinstance(value, list):
                    param_parts.append(f"{key}={value}")
                else:
                    param_parts.append(f"{key}={value}")
            
            # 添加sheet_name参数（如果有的话）
            if 'sheet_name' in final_params:
                param_parts.insert(0, f"sheet_name='{final_params['sheet_name']}'")
            
            if param_parts:
                params_str = ", " + ", ".join(param_parts)
        
        basic_code = f"df = pd.read_excel('{file_path}'{params_str})"
        code_lines.append(f"# 推荐的基础读取代码")
        code_lines.append(basic_code)
        code_lines.append("")
        
        # 添加数据检查代码
        code_lines.extend([
            "# 数据基本信息检查",
            "print('数据形状:', df.shape)",
            "print('列名:', df.columns.tolist())",
            "print('数据类型:')",
            "print(df.dtypes)",
            "print('\n前5行数据:')",
            "print(df.head())"
        ])
        
        # 如果有警告，添加处理建议
        if suggestions.get("warnings"):
            code_lines.append("")
            code_lines.append("# 注意事项:")
            for warning in suggestions["warnings"]:
                code_lines.append(f"# - {warning}")
        
        # 如果有提示，添加优化建议
        if suggestions.get("tips"):
            code_lines.append("")
            code_lines.append("# 优化提示:")
            for tip in suggestions["tips"]:
                code_lines.append(f"# - {tip}")
        
        return {
            "status": "SUCCESS",
            "code_template": "\n".join(code_lines),
            "recommended_params": final_params,
            "analysis": suggestions.get("analysis", {}),
            "tips": suggestions.get("tips", [])
        }
        
    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e),
            "code_template": f"# 基础读取代码\ndf = pd.read_excel('{file_path}')\nprint(df.head())"
        }