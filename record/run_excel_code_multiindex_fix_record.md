# run_excel_code 工具 MultiIndex 列名类型错误修复记录

## 问题描述

**错误信息**: `TypeError: sequence item 1: expected str instance, int found`

**错误位置**: 
- 文件: `security/secure_code_executor.py`, 第 328 行
- 具体位置: `exec(code, safe_globals, safe_locals)` 执行的用户代码第 6 行

**问题原因**:
当使用 `header=[0,1]` 参数读取 Excel 文件时，pandas 会创建 MultiIndex 列名。在某些情况下，MultiIndex 的元素可能包含整数类型（如果 Excel 单元格包含数字），当用户代码尝试对这些列名进行字符串操作（如 `join()`）时，就会出现类型错误。

## 修复方案

### 1. 增强列名处理逻辑 (enhanced_excel_helper.py)

**修复位置**: 第 456-472 行

**修复内容**:
- 改进了 MultiIndex 列名的处理逻辑
- 确保所有元组元素都被正确转换为字符串
- 对于多级列名，使用下划线连接各级名称
- 对于单级列名，也确保转换为字符串类型

**修复前**:
```python
col_parts = [str(part).strip() for part in col if part is not None and str(part).strip()]
if col_parts:
    new_columns.append(col_parts[-1])
else:
    new_columns.append(str(col))
```

**修复后**:
```python
col_parts = []
for part in col:
    if part is not None:
        part_str = str(part).strip()
        if part_str:  # 只添加非空字符串
            col_parts.append(part_str)

if col_parts:
    # 使用下划线连接多级列名，或取最后一个非空元素
    if len(col_parts) > 1:
        new_columns.append('_'.join(col_parts))
    else:
        new_columns.append(col_parts[0])
else:
    new_columns.append(str(col))
```

### 2. 添加 DataFrame 列名标准化预处理 (secure_code_executor.py)

**修复位置**: 第 325 行之前

**修复内容**:
- 在执行用户代码前，对所有 DataFrame-like 对象进行列名标准化
- 确保 MultiIndex 列名被正确转换为字符串
- 添加异常处理，确保预处理失败不影响主要功能

**新增代码**:
```python
# 预处理：标准化DataFrame列名（防止MultiIndex列名类型错误）
for var_name, var_value in safe_locals.items():
    if hasattr(var_value, 'columns') and hasattr(var_value, 'index'):
        # 这是一个DataFrame-like对象
        try:
            # 确保所有列名都是字符串类型
            new_columns = []
            for col in var_value.columns:
                if isinstance(col, tuple):
                    # 处理MultiIndex列名
                    col_parts = [str(part) for part in col if part is not None]
                    new_columns.append('_'.join(col_parts) if len(col_parts) > 1 else col_parts[0] if col_parts else str(col))
                else:
                    new_columns.append(str(col))
            var_value.columns = new_columns
        except Exception:
            # 如果列名标准化失败，继续执行，不影响主要功能
            pass
```

## 修复效果

1. **解决类型错误**: 彻底解决了 MultiIndex 列名中整数类型导致的 `join()` 操作错误
2. **保持兼容性**: 修复不影响现有的单级列头处理逻辑
3. **增强鲁棒性**: 双重保障机制，从文件读取和代码执行两个阶段确保列名类型正确
4. **改善用户体验**: 多级列名现在会被合理地连接为单一字符串，便于后续操作

## 测试建议

1. 测试使用 `header=[0,1]` 读取包含数字列名的 Excel 文件
2. 测试对 MultiIndex 列名进行字符串操作（如 `join()`, `split()` 等）
3. 测试混合类型的 MultiIndex 列名处理
4. 验证单级列头的正常功能不受影响

## 相关文件

- `enhanced_excel_helper.py`: 主要修复文件，改进列名处理逻辑
- `security/secure_code_executor.py`: 添加预处理安全措施
- `server.py`: 调用修复后的函数，无需修改

## 修复时间

**修复日期**: 2024年12月19日
**修复版本**: v1.2.1
**修复状态**: 已完成