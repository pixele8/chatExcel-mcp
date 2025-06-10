
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
