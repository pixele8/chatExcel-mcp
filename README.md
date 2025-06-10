# chatExcel - Excel智能处理与数据分析MCP服务器

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![MCP Protocol](https://img.shields.io/badge/MCP-2024--11--05-green.svg)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![NumPy](https://img.shields.io/badge/NumPy-1.26.4-orange.svg)](https://numpy.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.3.0-blue.svg)](https://pandas.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-5.17.0-red.svg)](https://plotly.com)
[![功能验证](https://img.shields.io/badge/功能验证-通过-green.svg)](#功能验证)

## 📋 项目概述

chatExcel 是一个基于 Model Context Protocol (MCP) 的智能 Excel 处理与数据分析服务器，专为复杂 Excel 文件的智能解析、数据处理和可视化设计。提供 14 个专业 MCP 工具，支持智能读取、数据验证、代码执行和交互式图表生成。

**🎉 最新更新 (2025-01-27)**:  
- ✅ 增强多级列头检测系统  
- ✅ 优化参数推荐算法  
- ✅ 完善数据验证功能  
- ✅ 提升缓存性能  
- ✅ 增强安全特性  

## ✨ 核心特性

- **智能Excel处理**: 自动检测编码、多级表头识别、参数推荐  
- **安全代码执行**: 沙箱环境支持 pandas/numpy 代码  
- **交互式可视化**: 基于 Plotly 的柱状图、饼图、折线图  
- **数据质量验证**: 完整性检查、质量评估、批量处理  
- **缓存优化**: 智能编码检测缓存，提升性能  
- **复杂格式支持**: 处理多级标题、合并单元格、不规则格式  

## 🛠️ MCP工具列表 (14个)

| 工具名称 | 功能描述 | 支持格式 |
|----------|----------|----------|
| `read_metadata` | CSV 元数据读取与分析 | CSV |
| `read_excel_metadata` | Excel 元数据读取与编码检测 | Excel |
| `suggest_excel_read_parameters_tool` | 智能推荐 Excel 读取参数 | Excel |
| `detect_excel_file_structure_tool` | Excel 文件结构检测 | Excel |
| `create_excel_read_template_tool` | 生成 Excel 读取代码模板 | Excel |
| `run_excel_code` | Excel 代码执行引擎 | Excel |
| `run_code` | CSV 代码执行引擎 | CSV |
| `bar_chart_to_html` | 交互式柱状图生成 | 数据数组 |
| `pie_chart_to_html` | 交互式饼图生成 | 数据数组 |
| `line_chart_to_html` | 交互式折线图生成 | 数据数组 |
| `verify_data_integrity` | 数据完整性验证 | Excel, CSV |
| `validate_data_quality` | 数据质量验证与建议 | Excel, CSV |
| `comprehensive_data_verification_tool` | 综合数据验证 | Excel, CSV |
| `batch_data_verification_tool` | 批量数据验证 | Excel, CSV |

## 🚀 编码缓存优化

### 核心功能
- **智能缓存**: 缓存文件编码检测结果  
- **自动清理**: 定期清除过期缓存  
- **大小监控**: 实时监控缓存大小  
- **自动备份**: 定期备份缓存数据  
- **配置驱动**: JSON 配置灵活控制参数  

### 配置文件 (`cache_config.json`)

```json
{
  "cache_settings": {
    "max_cache_size_mb": 10,
    "cache_expiry_days": 7,
    "auto_cleanup_interval": 10,
    "enable_auto_backup": true
  },
  "monitoring": {
    "enable_size_monitoring": true,
    "size_warning_threshold_mb": 8,
    "enable_performance_logging": false,
    "log_level": "INFO"
  },
  "maintenance": {
    "auto_reduce_cache_percentage": 50,
    "enable_startup_cleanup": true,
    "enable_periodic_optimization": true,
    "optimization_frequency": "weekly"
  },
  "paths": {
    "cache_directory": ".encoding_cache",
    "backup_directory": ".encoding_cache",
    "log_file": "cache_maintenance.log"
  }
}
```

### 使用方法

#### 命令行工具
```bash
# 查看缓存统计
python cache_manager.py stats
# 清理过期缓存
python cache_manager.py cleanup
# 监控缓存大小
python cache_manager.py monitor
# 创建备份
python cache_manager.py backup
# 从备份恢复
python cache_manager.py restore
```

#### 程序集成
```python
from enhanced_excel_helper import EncodingCache
cache = EncodingCache(config_file="cache_config.json")
encoding = cache.get("/path/to/file.xlsx")
if not encoding:
    detected_encoding = detect_file_encoding("/path/to/file.xlsx")
    cache.set("/path/to/file.xlsx", detected_encoding)
```

## 📊 系统要求

- **Python**: 3.11+  
- **操作系统**: macOS, Linux, Windows  
- **内存**: 建议 4GB+  
- **存储**: 至少 500MB  

## 🛠️ 安装部署

### 快速安装
```bash
git clone <repository-url>
cd chatExcel-mcp
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/health_check.py
python server.py
```

### 验证安装
```bash
python -c "import pandas as pd; print(f'Pandas {pd.__version__}')"
python -c "import numpy as np; print(f'NumPy {np.__version__}')"
python -c "import plotly; print(f'Plotly {plotly.__version__}')"
python test_complete_functionality.py
```

## 🔧 MCP配置

### 推荐配置 (`mcp_config_flexible.json`)
```json
{
  "mcpServers": {
    "chatExcel": {
      "command": "python3",
      "args": ["server.py"],
      "cwd": "/path/to/chatExcel-mcp",
      "env": {
        "PATH": "/path/to/venv/bin:/usr/local/bin:/usr/bin:/bin",
        "VIRTUAL_ENV": "/path/to/venv",
        "PYTHONPATH": "/path/to/chatExcel-mcp"
      }
    }
  }
}
```

### 测试配置
```bash
cd /path/to/chatExcel-mcp
source venv/bin/activate
python server.py
python -c "import mcp; print('MCP包正常')"
```

## 📚 API功能

### 数据元数据读取
- **`read_metadata`**: CSV 元数据读取  
- **`read_excel_metadata`**: Excel 元数据读取，支持复杂参数  

### 代码执行
- **`run_code`**: CSV 数据处理代码执行  
- **`run_excel_code`**: Excel 数据处理代码执行  

### 图表生成
- **`bar_chart_to_html`**: 交互式柱状图  
- **`pie_chart_to_html`**: 交互式饼图  
- **`line_chart_to_html`**: 交互式折线图  

### 数据质量验证
- **`validate_data_quality`**: 数据质量分析与建议  
- **`comprehensive_data_verification_tool`**: 综合数据验证  
- **`batch_data_verification_tool`**: 批量数据验证  

## 🧪 测试验证

```bash
python test_complete_functionality.py
python test_enhanced_excel.py
python demo_excel_features.py
pytest tests/
```

## 🛡️ 安全特性

- **代码沙箱**: 阻止危险操作  
- **资源限制**: 100MB 文件大小，30秒执行超时，1GB 内存限制  
- **输入验证**: 严格参数检查  

## 🔧 故障排除

### 常见问题
- **模块导入失败**: 激活虚拟环境，重新安装依赖  
- **文件编码问题**: 清理缓存或手动指定编码  
- **MCP服务器启动失败**: 检查路径、权限、Python版本  

### 诊断工具
```bash
python scripts/health_check.py
python -c "import sys, pandas, numpy, plotly; print(f'Python: {sys.version}, Pandas: {pandas.__version__}, NumPy: {numpy.__version__}, Plotly: {plotly.__version__}')"
```

## 📄 许可证

MIT 许可证，详见 [LICENSE](LICENSE)。

## 🤝 贡献指南

1. Fork 仓库  
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)  
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)  
4. 推送分支 (`git push origin feature/AmazingFeature`)  
5. 开启 Pull Request  

## 📞 联系方式

- 项目主页: [GitHub Repository](https://github.com/your-username/chatExcel-mcp-server)  
- 问题反馈: [Issues](https://github.com/your-username/chatExcel-mcp-server/issues)  
- 文档: [Wiki](https://github.com/your-username/chatExcel-mcp-server/wiki)  

**chatExcel** - 智能高效的 Excel 数据处理！ 🚀
