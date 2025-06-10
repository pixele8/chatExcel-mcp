#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pandas NameError 问题修复补丁
将增强的错误处理集成到 server.py 中
"""

import os
import shutil
from datetime import datetime

def backup_original_server():
    """备份原始 server.py 文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"server_backup_{timestamp}.py"
    
    if os.path.exists('server.py'):
        shutil.copy2('server.py', backup_name)
        print(f"✅ 已备份原始文件为: {backup_name}")
        return backup_name
    else:
        print("❌ 未找到 server.py 文件")
        return None

def create_enhanced_server():
    """创建增强版的 server.py"""
    
    # 读取原始文件
    with open('server.py', 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    # 查找 run_excel_code 函数的位置
    start_marker = "@mcp.tool()\ndef run_excel_code("
    end_marker = "@mcp.tool()\ndef run_code("
    
    start_pos = original_content.find(start_marker)
    end_pos = original_content.find(end_marker)
    
    if start_pos == -1 or end_pos == -1:
        print("❌ 无法找到 run_excel_code 函数")
        return False
    
    # 增强的 run_excel_code 函数
    enhanced_function = '''
@mcp.tool()
def run_excel_code(
    code: str, 
    file_path: str, 
    sheet_name: str = None, 
    skiprows: int = None, 
    header: int = None, 
    usecols: str = None, 
    encoding: str = None,
    auto_detect: bool = True
) -> dict:
    """增强版Excel代码执行工具，具备强化的pandas导入和错误处理机制。
    
    Args:
        code: 要执行的数据处理代码字符串
        file_path: Excel文件路径
        sheet_name: 可选，工作表名称
        skiprows: 可选，跳过的行数
        header: 可选，用作列名的行号。可以是整数、整数列表或None
        usecols: 可选，要解析的列。可以是列名列表、列索引列表或字符串
        encoding: 指定编码（可选，自动检测时忽略）
        auto_detect: 是否启用智能检测和参数优化
        
    Returns:
        dict: 执行结果或错误信息
    """
    
    # 增强的安全检查
    for forbidden in BLACKLIST:
        if forbidden in code:
            return {
                "error": {
                    "type": "SECURITY_VIOLATION",
                    "message": f"Forbidden operation detected: {forbidden}",
                    "solution": "Remove restricted operations from your code"
                }
            }

    # 验证文件访问
    validation_result = validate_file_access(file_path)
    if validation_result["status"] != "SUCCESS":
        return {
            "error": {
                "type": "FILE_ACCESS_ERROR",
                "message": validation_result["message"],
                "solution": "请确保文件路径正确且文件存在。"
            }
        }

    # 增强的模块导入机制
    def safe_import_pandas():
        """安全导入 pandas 模块"""
        try:
            import pandas as pd_local
            return pd_local, None
        except ImportError as e:
            error_msg = f"pandas 导入失败: {str(e)}"
            # 尝试重新导入
            try:
                import importlib
                importlib.invalidate_caches()
                import pandas as pd_local
                return pd_local, None
            except Exception as e2:
                return None, f"{error_msg}. 重试失败: {str(e2)}"
    
    def safe_import_numpy():
        """安全导入 numpy 模块"""
        try:
            import numpy as np_local
            return np_local, None
        except ImportError as e:
            error_msg = f"numpy 导入失败: {str(e)}"
            try:
                import importlib
                importlib.invalidate_caches()
                import numpy as np_local
                return np_local, None
            except Exception as e2:
                return None, f"{error_msg}. 重试失败: {str(e2)}"
    
    # 导入关键模块
    pd_module, pd_error = safe_import_pandas()
    np_module, np_error = safe_import_numpy()
    
    if pd_module is None:
        return {
            "error": {
                "type": "IMPORT_ERROR",
                "message": "Failed to import pandas",
                "details": pd_error,
                "solution": "请确保 pandas 已正确安装: pip install pandas"
            }
        }

    # 使用智能读取功能
    if auto_detect:
        # 智能编码检测
        encoding_info = detect_file_encoding(file_path)
        
        # 构建读取参数
        read_kwargs = {}
        if sheet_name is not None:
            read_kwargs['sheet_name'] = sheet_name
        if skiprows is not None:
            read_kwargs['skiprows'] = skiprows
        if header is not None:
            read_kwargs['header'] = header
        if encoding is not None:
            read_kwargs['encoding'] = encoding
        elif encoding_info.get('encoding'):
            read_kwargs['encoding'] = encoding_info['encoding']
        if usecols is not None:
            read_kwargs['usecols'] = usecols
        
        # 使用智能读取
        read_result = smart_read_excel(file_path, auto_detect_params=True, **read_kwargs)
        
        if not read_result['success']:
            return {
                "error": {
                    "type": "SMART_READ_ERROR",
                    "message": "智能读取失败: " + "; ".join(read_result.get('errors', [])),
                    "warnings": read_result.get('warnings', []),
                    "solution": "尝试手动指定参数或检查文件格式。"
                }
            }
        
        df = read_result['dataframe']
        read_info = read_result['info']
    else:
        # 传统读取方式
        read_params = {}
        if sheet_name:
            read_params['sheet_name'] = sheet_name
        if skiprows is not None:
            read_params['skiprows'] = skiprows
        if header is not None:
            read_params['header'] = header
        if usecols is not None:
            read_params['usecols'] = usecols
        
        try:
            df = pd_module.read_excel(file_path, **read_params)
            read_info = {'read_params': read_params, 'method': 'traditional'}
        except Exception as e:
            return {
                "error": {
                    "type": "READ_ERROR",
                    "message": f"读取Excel文件失败: {str(e)}",
                    "solution": "请检查文件格式和参数设置"
                }
            }
    
    # 增强的执行环境准备
    local_vars = {
        'pd': pd_module, 
        'file_path': file_path, 
        'sheet_name': sheet_name,
        'df': df,
        'read_info': read_info
    }
    
    # 添加 numpy（如果可用）
    if np_module is not None:
        local_vars['np'] = np_module
    
    # 添加常用内置函数
    local_vars.update({
        'len': len, 'str': str, 'int': int, 'float': float,
        'list': list, 'dict': dict, 'print': print,
        'range': range, 'enumerate': enumerate, 'zip': zip,
        'sum': sum, 'max': max, 'min': min, 'abs': abs, 'round': round
    })
    
    # 创建安全的全局环境
    global_vars = {
        '__builtins__': {
            'len': len, 'str': str, 'int': int, 'float': float,
            'list': list, 'dict': dict, 'print': print,
            'range': range, 'enumerate': enumerate, 'zip': zip,
            'sum': sum, 'max': max, 'min': min, 'abs': abs, 'round': round
        }
    }

    stdout_capture = StringIO()
    old_stdout = sys.stdout
    sys.stdout = stdout_capture

    try:
        # 执行用户代码（使用增强的环境）
        exec(code, global_vars, local_vars)
        result = local_vars.get('result', None)

        if result is None:
            return {
                "output": stdout_capture.getvalue(),
                "warning": "No 'result' variable found in code",
                "read_info": read_info if auto_detect else None
            }

        # 处理返回结果
        if isinstance(result, (pd_module.DataFrame, pd_module.Series)):
            response = {
                "result": {
                    "type": "dataframe" if isinstance(result, pd_module.DataFrame) else "series",
                    "shape": result.shape,
                    "dtypes": str(result.dtypes),
                    "data": result.head().to_dict() if isinstance(result, pd_module.DataFrame) else result.to_dict()
                },
                "output": stdout_capture.getvalue()
            }
        else:
            response = {
                "result": str(result),
                "output": stdout_capture.getvalue()
            }
        
        # 添加读取信息
        if auto_detect:
            response["read_info"] = read_info
            if read_result.get('warnings'):
                response["warnings"] = read_result['warnings']

        return response
        
    except NameError as e:
        error_msg = str(e)
        suggestions = []
        
        if "'pd'" in error_msg or "pandas" in error_msg.lower():
            suggestions.extend([
                "pandas 模块可能未正确导入，请检查安装: pip install pandas",
                "尝试重启 MCP 服务器",
                "检查虚拟环境是否正确激活",
                "尝试在代码中显式导入: import pandas as pd"
            ])
        
        if "'np'" in error_msg or "numpy" in error_msg.lower():
            suggestions.extend([
                "numpy 模块可能未正确导入，请检查安装: pip install numpy",
                "尝试在代码中显式导入: import numpy as np"
            ])
        
        if "'df'" in error_msg:
            suggestions.extend([
                "DataFrame 未正确加载，请检查文件路径和格式",
                "尝试使用 pd.read_excel() 手动读取文件"
            ])
        
        return {
            "error": {
                "type": "NameError",
                "message": f"变量未定义错误: {error_msg}",
                "traceback": traceback.format_exc(),
                "output": stdout_capture.getvalue(),
                "suggestions": suggestions,
                "pandas_available": pd_module is not None,
                "numpy_available": np_module is not None
            }
        }
        
    except Exception as e:
        error_msg = str(e)
        suggestions = []

        if "No such file or directory" in error_msg:
            suggestions.append("Use raw strings for paths: r'path\\to\\file.xlsx'")
        if "Worksheet named" in error_msg and "not found" in error_msg:
            suggestions.append("Check the sheet_name parameter. Ensure the sheet name exists in the Excel file.")
        if "could not convert string to float" in error_msg:
            suggestions.append("Try: pd.to_numeric(df['col'], errors='coerce')")
        if "AttributeError" in error_msg and "str" in error_msg:
            suggestions.append("Try: df['col'].astype(str).str.strip()")
        if "encoding" in error_msg.lower():
            suggestions.append("Try specifying encoding parameter or disable auto_detect")

        return {
            "error": {
                "type": type(e).__name__,
                "message": error_msg,
                "traceback": traceback.format_exc(),
                "output": stdout_capture.getvalue(),
                "suggestions": suggestions if suggestions else None,
                "read_info": read_info if auto_detect else None
            }
        }
    finally:
        sys.stdout = old_stdout


'''
    
    # 替换原始函数
    new_content = (
        original_content[:start_pos] + 
        enhanced_function + 
        original_content[end_pos:]
    )
    
    # 写入新文件
    with open('server_enhanced.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ 已创建增强版 server_enhanced.py")
    return True

def apply_patch():
    """应用补丁"""
    print("🔧 应用 pandas NameError 修复补丁")
    print("=" * 50)
    
    # 备份原始文件
    backup_file = backup_original_server()
    if not backup_file:
        return False
    
    # 创建增强版
    if create_enhanced_server():
        # 替换原始文件
        if os.path.exists('server_enhanced.py'):
            shutil.move('server.py', 'server_original.py')
            shutil.move('server_enhanced.py', 'server.py')
            print("✅ 补丁应用成功")
            print("📁 原始文件已保存为: server_original.py")
            print("📁 备份文件: " + backup_file)
            return True
    
    print("❌ 补丁应用失败")
    return False

def create_usage_guide():
    """创建使用指南"""
    guide_content = '''
# pandas NameError 问题解决方案

## 问题描述
在使用 `run_excel_code` 工具时可能遇到 `NameError: name 'pd' is not defined` 错误。

## 解决方案

### 1. 应用修复补丁
```bash
python3 pandas_fix_patch.py
```

### 2. 重启 MCP 服务器
```bash
python3 server.py
```

### 3. 使用增强的错误处理
修复后的 `run_excel_code` 工具包含：
- 增强的 pandas/numpy 导入机制
- 更详细的错误信息和建议
- 安全的执行环境
- 自动重试机制

### 4. 最佳实践

#### 推荐的代码写法：
```python
# 基本操作
print(f"数据形状: {df.shape}")
print(f"列名: {list(df.columns)}")

# 数据处理
result = df.groupby('列名').sum()
```

#### 如果仍然遇到问题，可以显式导入：
```python
import pandas as pd
import numpy as np

# 然后进行操作
result = df.describe()
```

### 5. 故障排除

如果问题仍然存在：

1. **检查环境**：
   ```bash
   python3 enhanced_run_excel_code.py
   ```

2. **检查依赖**：
   ```bash
   pip install pandas numpy openpyxl xlrd
   ```

3. **重新安装依赖**：
   ```bash
   pip uninstall pandas numpy
   pip install pandas numpy
   ```

4. **检查虚拟环境**：
   确保在正确的虚拟环境中运行

### 6. 错误信息解读

- `NameError: name 'pd' is not defined`：pandas 导入失败
- `NameError: name 'np' is not defined`：numpy 导入失败
- `NameError: name 'df' is not defined`：DataFrame 加载失败

每种错误都会提供具体的解决建议。

### 7. 联系支持

如果问题仍然无法解决，请提供：
- 错误的完整信息
- 使用的代码
- 环境诊断结果
'''
    
    with open('PANDAS_FIX_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("📖 已创建使用指南: PANDAS_FIX_GUIDE.md")

def main():
    """主函数"""
    try:
        if apply_patch():
            create_usage_guide()
            print("\n🎉 修复完成！")
            print("\n📋 下一步：")
            print("1. 重启 MCP 服务器")
            print("2. 测试 run_excel_code 工具")
            print("3. 查看 PANDAS_FIX_GUIDE.md 了解详细信息")
        else:
            print("\n❌ 修复失败，请检查错误信息")
    except Exception as e:
        print(f"\n❌ 修复过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()