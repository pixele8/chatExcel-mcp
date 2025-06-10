# chatExcel - Excel智能处理与数据分析MCP服务器

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![MCP Protocol](https://img.shields.io/badge/MCP-2024--11--05-green.svg)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![NumPy](https://img.shields.io/badge/NumPy-1.26.4-orange.svg)](https://numpy.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.3.0-blue.svg)](https://pandas.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-5.17.0-red.svg)](https://plotly.com)
[![功能验证](https://img.shields.io/badge/功能验证-通过-green.svg)](#功能验证)

chatExcel - 基于模型上下文协议（MCP）的Excel智能处理与数据分析服务器，专为Excel文件智能解析、数据处理、代码执行以及交互式图表生成而设计。支持复杂Excel格式处理、智能参数推荐、代码模板生成和高级数据可视化。

**🎉 最新更新 (2025-01-27)**: 
- ✅ NumPy和Pandas功能完备性验证通过
- ✅ Plotly交互式图表库集成完成
- ✅ Excel智能处理功能全面优化
- ✅ 增强多级列头检测系统已修复并正常运行
- ✅ 所有核心数据处理功能稳定运行
- ✅ MCP服务器安全沙箱环境优化完成

## ✨ 核心特性

### 🛠️ MCP工具总览 (14个专业工具)

本项目提供**14个专业MCP工具**，涵盖Excel智能处理、数据分析、代码执行和可视化的完整工作流：

#### 📊 数据读取与元数据分析工具
1. **`read_metadata`** - CSV文件元数据读取和智能分析
   - 依赖库: `pandas`, `numpy`, `chardet`
   - 功能: 智能编码检测、分隔符识别、数据质量预警

2. **`read_excel_metadata`** - Excel文件元数据读取和智能编码检测
   - 依赖库: `pandas`, `openpyxl`, `xlrd`, `chardet`
   - 功能: 多工作表分析、复杂格式处理、参数推荐

#### 🔧 Excel智能处理工具
3. **`suggest_excel_read_parameters_tool`** - Excel读取参数智能推荐
   - 依赖库: `openpyxl`, `pandas`
   - 功能: 自动检测最佳读取参数、多级标题处理

4. **`detect_excel_file_structure_tool`** - Excel文件结构检测
   - 依赖库: `openpyxl`, `pandas`
   - 功能: 工作表结构分析、数据区域识别

5. **`create_excel_read_template_tool`** - Excel读取代码模板生成
   - 依赖库: `pandas`, `openpyxl`
   - 功能: 基于文件结构自动生成读取代码

#### ⚡ 代码执行引擎
6. **`run_excel_code`** - Excel代码执行引擎(支持复杂格式参数)
   - 依赖库: `pandas`, `numpy`, `openpyxl`, `xlrd`
   - 功能: 安全沙箱执行、智能参数检测、错误诊断

7. **`run_code`** - CSV代码执行引擎(安全沙箱环境)
   - 依赖库: `pandas`, `numpy`
   - 功能: 代码安全检查、结果格式化、性能优化

#### 📈 交互式图表生成工具
8. **`bar_chart_to_html`** - 交互式柱状图生成(Chart.js)
   - 依赖库: `plotly` (Chart.js模板)
   - 功能: 动态柱状图、自定义样式、HTML输出

9. **`pie_chart_to_html`** - 交互式饼图生成(Chart.js)
   - 依赖库: `plotly` (Chart.js模板)
   - 功能: 动态饼图、颜色配置、数据标签

10. **`line_chart_to_html`** - 交互式折线图生成(Chart.js)
    - 依赖库: `plotly` (Chart.js模板)
    - 功能: 多数据集支持、趋势分析、交互式缩放

#### 🔍 数据质量与验证工具
11. **`verify_data_integrity`** - 数据完整性验证和比对核准
    - 依赖库: `pandas`, `numpy`, `scipy`
    - 功能: 数据一致性检查、文件比较、完整性报告

12. **`validate_data_quality`** - 数据质量验证和改进建议
    - 依赖库: `pandas`, `numpy`
    - 功能: 质量评分、缺失值分析、优化建议

13. **`comprehensive_data_verification_tool`** - 综合数据验证和核准
    - 依赖库: `pandas`, `numpy`, `scipy`, `chardet`
    - 功能: 多层次验证、异常检测、质量报告生成

14. **`batch_data_verification_tool`** - 批量数据验证工具
    - 依赖库: `pandas`, `numpy`, `scipy`
    - 功能: 批量文件处理、质量排名、批量建议

### 📊 数据处理能力
- **智能文件解析**: 自动检测 CSV 文件编码和分隔符
- **Excel 智能处理**: 🆕 智能分析Excel结构，自动推荐最佳读取参数
- **Excel 多表格支持**: 完整的 Excel 工作簿处理能力
- **复杂格式支持**: 🆕 处理多级标题、合并单元格、不规则格式的Excel文件
- **代码模板生成**: 🆕 基于文件结构自动生成Excel读取代码
- **元数据分析**: 快速获取数据结构、类型和统计信息
- **安全代码执行**: 沙箱环境下的数据处理代码执行
- **大文件支持**: 最大支持 100MB 文件处理

### 📈 可视化功能
- **交互式图表**: 基于 Chart.js 的动态图表生成
- **多种图表类型**: 柱状图、饼图、折线图
- **HTML 输出**: 可在浏览器中直接查看的图表文件
- **自定义样式**: 支持标题、轴标签等个性化配置

### 🔒 安全特性
- **代码沙箱**: 阻止危险操作（文件系统、系统调用等）
- **输入验证**: 严格的参数验证和类型检查
- **错误处理**: 详细的错误信息和解决方案建议
- **资源限制**: 文件大小和处理时间限制

### 🚀 性能优化
- **Python 3.11**: 利用最新 Python 版本的性能提升
- **异步处理**: 支持并发请求处理
- **内存优化**: 智能内存管理和垃圾回收
- **缓存机制**: 元数据缓存提升响应速度

## 📋 系统要求

- **Python**: 3.11 或更高版本
- **操作系统**: macOS, Linux, Windows
- **内存**: 建议 4GB 以上
- **存储**: 至少 500MB 可用空间

## 🛠️ 安装部署

### 环境要求

- **Python**: 3.11 或更高版本
- **操作系统**: macOS, Linux, Windows
- **内存**: 建议 4GB 以上
- **存储**: 至少 500MB 可用空间

### 快速安装

```bash
# 1. 克隆项目到本地
git clone <repository-url>
cd chatExcel-mcp-server

# 2. 创建Python 3.11虚拟环境
python3.11 -m venv venv

# 3. 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或 Windows: venv\Scripts\activate

# 4. 升级pip到最新版本
pip install --upgrade pip

# 5. 安装项目依赖
pip install -r requirements.txt

# 6. 运行健康检查
python scripts/health_check.py

# 7. 启动MCP服务器
python server.py
```

### 详细安装步骤

#### 步骤1: 环境准备

**macOS用户**:
```bash
# 安装Python 3.11（如果未安装）
brew install python@3.11

# 验证Python版本
python3.11 --version
```

**Linux用户**:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# CentOS/RHEL
sudo yum install python3.11 python3.11-venv
```

**Windows用户**:
- 从 [Python官网](https://www.python.org/downloads/) 下载并安装Python 3.11+
- 确保在安装时勾选"Add Python to PATH"

#### 步骤2: 项目设置

```bash
# 克隆项目
git clone <repository-url>
cd chatExcel-mcp-server

# 创建虚拟环境
python3.11 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 验证虚拟环境
which python  # 应该显示venv路径
python --version  # 应该显示Python 3.11.x
```

#### 步骤3: 依赖安装

```bash
# 升级pip
pip install --upgrade pip

# 安装核心依赖
pip install -r requirements.txt

# 验证关键依赖
python -c "import fastmcp; print('FastMCP安装成功')"
python -c "import pandas as pd; print(f'Pandas {pd.__version__} 安装成功')"
python -c "import numpy as np; print(f'NumPy {np.__version__} 安装成功')"
python -c "import plotly; print(f'Plotly {plotly.__version__} 安装成功')"
python -c "import openpyxl; print('OpenPyXL安装成功')"
```

#### 步骤4: 功能验证

```bash
# 运行健康检查
python scripts/health_check.py

# 运行完整功能测试
python test_complete_functionality.py

# 测试增强多级列头检测
python test_enhanced_multiheader.py

# 验证MCP工具导入
python -c "from server import *; print('所有MCP工具导入成功')"
```

### 使用启动脚本（推荐）

```bash
# 给启动脚本添加执行权限
chmod +x start_py311.sh

# 使用启动脚本（自动激活环境并运行健康检查）
./start_py311.sh

# 然后启动服务器
python server.py
```

### 验证安装

```bash
# 验证核心依赖
python -c "import pandas as pd; print(f'Pandas {pd.__version__} 安装成功')"
python -c "import numpy as np; print(f'NumPy {np.__version__} 安装成功')"
python -c "import plotly; print(f'Plotly {plotly.__version__} 安装成功')"

# 验证Excel处理功能
python -c "from excel_smart_tools import *; print('Excel智能工具导入成功')"

# 运行功能测试
python test_complete_functionality.py
```

### 🔧 故障排除

#### 常见问题及解决方案

**问题1: Python版本不兼容**
```bash
# 错误: Python版本低于3.11
# 解决方案: 安装Python 3.11+
python3.11 --version  # 验证版本
```

**问题2: 依赖安装失败**
```bash
# 错误: pip install失败
# 解决方案: 升级pip并清理缓存
pip install --upgrade pip
pip cache purge
pip install -r requirements.txt --no-cache-dir
```

**问题3: 模块导入错误**
```bash
# 错误: ModuleNotFoundError
# 解决方案: 确认虚拟环境激活
source venv/bin/activate  # 重新激活
which python  # 确认使用venv中的python
pip list  # 查看已安装包
```

**问题4: Excel文件处理错误**
```bash
# 错误: openpyxl或xlrd相关错误
# 解决方案: 重新安装Excel处理库
pip uninstall openpyxl xlrd xlsxwriter -y
pip install openpyxl>=3.1.0 xlrd>=2.0.1 xlsxwriter>=3.1.9
```

**问题5: MCP服务器启动失败**
```bash
# 错误: FastMCP相关错误
# 解决方案: 检查MCP框架安装
pip install fastmcp>=2.5.0 mcp>=1.9.0 --upgrade
python -c "from mcp.server.fastmcp import FastMCP; print('MCP框架正常')"
```

#### 环境诊断脚本

```bash
# 运行完整环境诊断
python -c "
import sys
print(f'Python版本: {sys.version}')
print(f'Python路径: {sys.executable}')

try:
    import pandas as pd
    import numpy as np
    import plotly
    import openpyxl
    import fastmcp
    print('✅ 所有核心依赖正常')
except ImportError as e:
    print(f'❌ 依赖缺失: {e}')
"
```

### 📋 MCP配置验证

#### 验证MCP服务器功能

```bash
# 测试MCP服务器基本功能
python test_mcp_config.py

# 预期输出:
# ✅ Plotly导入成功: 5.17.0
# ✅ 服务器导入成功
# 📋 MCP服务器配置示例已生成
```

#### 验证所有14个MCP工具

```bash
# 验证所有MCP工具可用性
python -c "
from server import (
    read_metadata, read_excel_metadata, run_excel_code, run_code,
    bar_chart_to_html, pie_chart_to_html, line_chart_to_html,
    verify_data_integrity, validate_data_quality,
    suggest_excel_read_parameters_tool, detect_excel_file_structure_tool,
    create_excel_read_template_tool, comprehensive_data_verification_tool,
    batch_data_verification_tool
)
print('✅ 所有14个MCP工具导入成功')
"
```

#### Claude Desktop配置验证

1. **检查配置文件位置**:
   ```bash
   # macOS
   ls -la ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # 如果文件不存在，创建目录
   mkdir -p ~/Library/Application\ Support/Claude/
   ```

2. **验证配置格式**:
   ```bash
   # 验证JSON格式
   python -c "import json; print(json.load(open('~/Library/Application Support/Claude/claude_desktop_config.json')))"
   ```

3. **测试MCP连接**:
    ```bash
    # 启动服务器并测试连接
    python server.py &
    sleep 2
    python test_mcp_client.py
    ```

### 🚀 部署后验证

#### 完整功能测试套件

```bash
# 1. 基础功能测试
python test_complete_functionality.py

# 2. Excel智能处理测试
python test_enhanced_excel.py

# 3. 多级列头检测测试
python test_enhanced_multiheader.py

# 4. 数据验证功能测试
python test_enhanced_features.py

# 5. 图表生成测试
python test_charts.py

# 6. MCP服务器配置测试
python test_mcp_config.py
```

#### 性能基准测试

```bash
# 创建测试数据
python create_test_excel.py

# 运行性能测试
python -c "
import time
from server import read_excel_metadata, run_excel_code

# 测试元数据读取性能
start = time.time()
result = read_excel_metadata('sample_data.xlsx')
print(f'元数据读取耗时: {time.time() - start:.2f}秒')

# 测试代码执行性能
start = time.time()
code = 'df.describe()'
result = run_excel_code('sample_data.xlsx', code)
print(f'代码执行耗时: {time.time() - start:.2f}秒')
"
```

#### 内存使用监控

```bash
# 安装内存监控工具（可选）
pip install psutil

# 监控内存使用
python -c "
import psutil
import os
from server import read_excel_metadata

process = psutil.Process(os.getpid())
print(f'启动时内存使用: {process.memory_info().rss / 1024 / 1024:.1f} MB')

# 执行操作
result = read_excel_metadata('sample_data.xlsx')
print(f'处理后内存使用: {process.memory_info().rss / 1024 / 1024:.1f} MB')
"
```

### 🔧 生产环境优化

#### 环境变量配置

```bash
# 创建环境配置文件
cat > .env << EOF
# MCP服务器配置
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=3000
MCP_LOG_LEVEL=INFO

# 数据处理配置
MAX_FILE_SIZE=104857600  # 100MB
MAX_PROCESSING_TIME=300  # 5分钟
ENABLE_CACHE=true

# 安全配置
ENABLE_SANDBOX=true
ALLOW_FILE_OPERATIONS=false
EOF
```

#### 日志配置

```bash
# 配置日志轮转
cat > logging.conf << EOF
[loggers]
keys=root,chatexcel

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=INFO
handlers=consoleHandler

[logger_chatexcel]
level=DEBUG
handlers=consoleHandler,fileHandler
qualname=chatexcel
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=simpleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=handlers.RotatingFileHandler
level=DEBUG
formatter=simpleFormatter
args=('chatExcel.log', 'a', 10485760, 5)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
EOF
```

#### 系统服务配置（Linux）

```bash
# 创建systemd服务文件
sudo cat > /etc/systemd/system/chatexcel-mcp.service << EOF
[Unit]
Description=ChatExcel MCP Server
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/chatExcel-mcp-server
Environment=PATH=/path/to/chatExcel-mcp-server/venv/bin
ExecStart=/path/to/chatExcel-mcp-server/venv/bin/python server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 启用并启动服务
sudo systemctl enable chatexcel-mcp
sudo systemctl start chatexcel-mcp
sudo systemctl status chatexcel-mcp
```

#### Docker部署（推荐）

```bash
# 创建Dockerfile
cat > Dockerfile << EOF
FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建非root用户
RUN useradd -m -u 1000 chatexcel && chown -R chatexcel:chatexcel /app
USER chatexcel

# 暴露端口
EXPOSE 3000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:3000/health')"

# 启动命令
CMD ["python", "server.py"]
EOF

# 创建docker-compose.yml
cat > docker-compose.yml << EOF
version: '3.8'

services:
  chatexcel-mcp:
    build: .
    ports:
      - "3000:3000"
    environment:
      - MCP_SERVER_HOST=0.0.0.0
      - MCP_SERVER_PORT=3000
      - MCP_LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:3000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # 可选：添加监控服务
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-storage:/var/lib/grafana

volumes:
  grafana-storage:
EOF

# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f chatexcel-mcp

# 停止服务
docker-compose down
```

#### 监控和告警配置

```bash
# 创建监控目录
mkdir -p monitoring

# 创建Prometheus配置
cat > monitoring/prometheus.yml << EOF
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'chatexcel-mcp'
    static_configs:
      - targets: ['chatexcel-mcp:3000']
    metrics_path: '/metrics'
    scrape_interval: 5s
EOF

# 创建健康检查脚本
cat > health_check.py << EOF
#!/usr/bin/env python3
import requests
import sys
import time

def check_health():
    try:
        response = requests.get('http://localhost:3000/health', timeout=10)
        if response.status_code == 200:
            print("✅ ChatExcel MCP服务器运行正常")
            return True
        else:
            print(f"❌ 健康检查失败: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 连接失败: {e}")
        return False

if __name__ == "__main__":
    if check_health():
        sys.exit(0)
    else:
        sys.exit(1)
EOF

chmod +x health_check.py

# 创建性能监控脚本
cat > monitor_performance.py << EOF
#!/usr/bin/env python3
import psutil
import time
import json
from datetime import datetime

def monitor_system():
    while True:
        stats = {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'network_io': psutil.net_io_counters()._asdict()
        }
        
        print(json.dumps(stats, indent=2))
        time.sleep(60)  # 每分钟记录一次

if __name__ == "__main__":
    monitor_system()
EOF

chmod +x monitor_performance.py
```

## 🔧 MCP 客户端配置

### Claude Desktop 配置

在 Claude Desktop 的配置文件中添加以下配置：

**macOS 配置文件位置**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "chatExcel": {
      "name": "chatExcel",
      "type": "stdio",
      "description": "Excel智能处理与数据分析服务器",
      "isActive": true,
      "command": "python",
      "args": [
        "/Users/wangdada/Downloads/mcp/excel-mcp/chatExcel-mcp-server/server.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/wangdada/Downloads/mcp/excel-mcp/chatExcel-mcp-server",
        "PATH": "/Users/wangdada/Downloads/mcp/excel-mcp/chatExcel-mcp-server/venv/bin:/usr/local/bin:/usr/bin:/bin"
      }
    }
  }
}
```

### 配置验证

```bash
# 测试MCP服务器配置
python test_mcp_config.py

# 预期输出
✅ Plotly导入成功: 5.17.0
✅ 服务器导入成功
📋 MCP服务器配置示例已生成
```

### 其他MCP客户端配置

对于其他MCP客户端，请参考以下通用配置模板：

```json
{
  "mcpServers": {
    "chatexcel-mcp-server": {
      "command": "python",
      "args": ["/Users/wangdada/Downloads/mcp/excel-mcp/chatExcel-mcp-server/server.py"],
      "env": {
        "PYTHONPATH": "/Users/wangdada/Downloads/mcp/excel-mcp/chatExcel-mcp-server"
      }
    }
  }
}
```

### 配置验证

```bash
# 测试MCP服务器配置
python test_mcp_config.py

# 预期输出
✅ Plotly导入成功: 5.17.0
✅ 服务器导入成功
📋 MCP服务器配置示例已生成
```

## 📚 API 功能详解

### 🆕 Excel智能处理功能

#### `suggest_excel_read_parameters_tool`
智能分析Excel文件结构并推荐最佳读取参数

**参数**:
- `file_path` (string): Excel文件路径

**返回**:
```json
{
  "recommended_params": {
    "skiprows": 3,
    "header": 0,
    "usecols": "A:E"
  },
  "analysis": {
    "detected_header_row": 3,
    "empty_rows": [0, 1, 2],
    "data_start_row": 4
  },
  "warnings": ["检测到合并单元格"],
  "tips": ["建议跳过前3行空行"]
}
```

#### `detect_excel_file_structure_tool`
深度分析Excel文件的详细结构信息

**参数**:
- `file_path` (string): Excel文件路径

**返回**:
```json
{
  "sheets": [
    {
      "name": "Sheet1",
      "max_row": 100,
      "max_column": 10,
      "merged_cells": [["A1:C1"]],
      "data_range": "A4:J100"
    }
  ],
  "file_info": {
    "size": 51200,
    "sheet_count": 3
  }
}
```

### 配置验证

```bash
# 测试MCP服务器配置
python test_mcp_config.py

# 预期输出
✅ Plotly导入成功: 5.17.0
✅ 服务器导入成功
📋 MCP服务器配置示例已生成
```

#### `create_excel_read_template_tool` 🆕 优化版
基于智能分析生成Excel读取代码模板，支持用户参数优先级

**参数**:
- `file_path` (string): Excel文件路径
- `sheet_name` (string, 可选): 工作表名称
- `skiprows` (int, 可选): 跳过行数（用户指定优先）
- `header` (int, 可选): 标题行位置（用户指定优先）
- `usecols` (string, 可选): 使用的列范围（用户指定优先）

**功能特性**:
- **智能参数融合**: 结合智能推荐参数和用户自定义参数
- **用户参数优先**: 用户提供的参数将覆盖智能推荐的参数
- **完整参数传递**: 确保所有参数正确传递到生成的代码中
- **参数验证**: 自动验证参数的有效性和兼容性

**返回**:
```json
{
  "status": "SUCCESS",
  "template_code": "import pandas as pd\n\ndf = pd.read_excel('file.xlsx', sheet_name='Sheet1', skiprows=3, header=0, usecols='A:E')\nprint(df.head())",
  "explanation": "代码说明和使用提示",
  "recommended_params": {
    "sheet_name": "Sheet1",
    "skiprows": 3,
    "header": 0,
    "usecols": "A:E"
  },
  "user_overrides": {
    "skiprows": "用户指定: 3",
    "header": "用户指定: 0"
  }
}
```

### 配置验证

```bash
# 测试MCP服务器配置
python test_mcp_config.py

# 预期输出
✅ Plotly导入成功: 5.17.0
✅ 服务器导入成功
📋 MCP服务器配置示例已生成
```

### 1. 数据元数据读取

#### `read_metadata`
读取 CSV 文件的元数据信息

**参数**:
- `file_path` (string): CSV 文件路径

**返回**:
```json
{
  "status": "SUCCESS",
  "columns": [
    {
      "name": "column_name",
      "type": "data_type",
      "sample": "sample_value",
      "statistics": {...}
    }
  ],
  "file_info": {
    "size": 1024,
    "encoding": "utf-8",
    "delimiter": ",",
    "row_count": 1000
  }
}
```

### 配置验证

```bash
# 测试MCP服务器配置
python test_mcp_config.py

# 预期输出
✅ Plotly导入成功: 5.17.0
✅ 服务器导入成功
📋 MCP服务器配置示例已生成
```

#### `read_excel_metadata` 🆕 增强版
读取 Excel 文件的元数据信息（支持复杂读取参数）

**参数**:
- `file_path` (string): Excel 文件路径
- `sheet_name` (string, 可选): 🆕 工作表名称
- `skiprows` (int, 可选): 🆕 跳过的行数
- `header` (int, 可选): 🆕 标题行位置
- `usecols` (string, 可选): 🆕 使用的列范围

**返回**:
```json
{
  "status": "SUCCESS",
  "sheets": ["Sheet1", "Sheet2"],
  "columns_metadata": [
    {
      "name": "column_name",
      "type": "data_type",
      "sample": "sample_value",
      "statistics": {...}
    }
  ],
  "file_info": {
    "size": 51200,
    "encoding": "utf-8",
    "sheet_count": 2
  },
  "read_params": {
    "skiprows": 3,
    "header": 0,
    "usecols": "A:E"
  }
}
```

### 配置验证

```bash
# 测试MCP服务器配置
python test_mcp_config.py

# 预期输出
✅ Plotly导入成功: 5.17.0
✅ 服务器导入成功
📋 MCP服务器配置示例已生成
```

### 2. 代码执行

#### `run_code`
在 CSV 数据上执行数据处理代码

**参数**:
- `code` (string): 要执行的数据处理代码
- `file_path` (string): CSV 文件路径

**示例**:
```json
{
  "code": "df.groupby('category').agg({'sales': 'sum', 'quantity': 'mean'})",
  "file_path": "/path/to/data.csv"
}
```

#### `run_excel_code` 🆕 增强版
在 Excel 数据上执行数据处理代码（支持复杂读取参数）

**参数**:
- `code` (string): 要执行的数据处理代码
- `file_path` (string): Excel 文件路径
- `sheet_name` (string, 可选): 工作表名称
- `skiprows` (int, 可选): 🆕 跳过的行数
- `header` (int, 可选): 🆕 标题行位置
- `usecols` (string, 可选): 🆕 使用的列范围

**示例**:
```json
{
  "code": "df.groupby('category').agg({'sales': 'sum', 'quantity': 'mean'})",
  "file_path": "/path/to/complex_excel.xlsx",
  "sheet_name": "Sales_Data",
  "skiprows": 3,
  "header": 0,
  "usecols": "A:F"
}
```

### 3. 图表生成

#### `bar_chart_to_html`
生成交互式柱状图

**参数**:
- `categories` (array): X轴分类标签
- `values` (array): Y轴数值
- `title` (string, 可选): 图表标题

**示例**:
```json
{
  "categories": ["Q1", "Q2", "Q3", "Q4"],
  "values": [120000, 150000, 180000, 200000],
  "title": "季度销售额"
}
```

#### `pie_chart_to_html`
生成交互式饼图

**参数**:
- `labels` (array): 扇形标签
- `values` (array): 扇形数值
- `title` (string, 可选): 图表标题

#### `line_chart_to_html`
生成交互式折线图

**参数**:
- `labels` (array): X轴标签
- `datasets` (array): 数据集列表
- `title` (string, 可选): 图表标题

**数据集格式**:
```json
{
  "label": "数据系列名称",
  "data": [10, 20, 30, 40]
}
```

### 4. 数据质量验证

#### `validate_data_quality`
分析数据质量并提供改进建议

**参数**:
- `file_path` (string): 数据文件路径

**返回**:
```json
{
  "status": "SUCCESS",
  "missing_data": {...},
  "duplicates": {...},
  "data_types": {...},
  "recommendations": [...]
}
```

## 🎯 使用场景

### 🆕 Excel智能处理场景
```
用户: "这个Excel文件格式很复杂，有很多空行和合并单元格，怎么读取？"
→ 调用 suggest_excel_read_parameters_tool 智能分析并推荐参数
→ 调用 create_excel_read_template_tool 生成标准读取代码
```

```
用户: "分析这个Excel文件的结构，看看有哪些工作表和数据范围"
→ 调用 detect_excel_file_structure_tool 获取详细结构信息
```

```
用户: "读取Excel文件，但要跳过前3行，只要A到E列的数据"
→ 调用 read_excel_metadata 使用 skiprows=3, usecols="A:E" 参数
→ 调用 run_excel_code 执行复杂参数的数据分析
```

```
用户: "生成读取代码，我要自定义跳过行数为1，标题行为0"
→ 调用 create_excel_read_template_tool 传入用户参数 skiprows=1, header=0
→ 系统智能融合用户参数和推荐参数，用户参数优先
→ 生成包含用户指定参数的完整Excel读取代码模板
```

```
用户: "这个Excel文件我只想要部分参数自定义，其他的用智能推荐"
→ 调用 create_excel_read_template_tool 仅传入部分用户参数
→ 系统自动融合：用户参数 + 智能推荐参数
→ 确保参数传递的完整性和准确性
```

### 数据探索分析
```
用户: "读取 sales_data.csv 的元数据，显示列结构"
→ 调用 read_metadata 获取数据概览
```

### 数据处理操作
```
用户: "按产品类别分组，计算总销售额"
→ 调用 run_code 执行分组聚合操作
```

### 数据可视化
```
用户: "创建一个显示各类别销售额的柱状图"
→ 调用 bar_chart_to_html 生成交互式图表
```

### Excel 数据处理
```
用户: "分析 Excel 文件中的第二个工作表"
→ 调用 run_excel_code 指定工作表处理
```

## 🔍 项目结构

```
chatExcel/
├── server.py              # 主服务器文件
├── config.py              # 配置文件
├── requirements.txt       # 依赖包列表
├── pyproject.toml         # 项目配置
├── start_py311.sh         # 启动脚本
├── README.md              # 项目文档
├── EXCEL_FEATURES.md      # 🆕 Excel智能处理功能详细文档
├── PYTHON311_UPGRADE.md   # 升级说明
│
├── excel_smart_tools.py   # 🆕 Excel智能处理工具
├── excel_helper.py        # 🆕 Excel分析辅助函数
├── demo_excel_features.py # 🆕 Excel功能演示脚本
│
├── scripts/               # 工具脚本
│   ├── health_check.py    # 健康检查
│   ├── maintenance.sh     # 维护脚本
│   ├── update_dependencies.sh
│   └── code_quality_check.sh
│
├── templates/             # HTML 模板
│   ├── barchart_template.html
│   ├── piechart_template.html
│   └── linechart_template.html
│
├── charts/                # 生成的图表文件
├── tests/                 # 测试文件
│   ├── test_complete_functionality.py  # 🆕 完整功能测试
│   ├── test_enhanced_excel.py          # 🆕 Excel增强功能测试
│   ├── test_metadata_functions.py     # 元数据功能测试
│   ├── test_parameter_passing.py      # 🆕 参数传递测试
│   ├── debug_parameter_passing.py     # 🆕 参数传递调试脚本
│   ├── test_pandas_import.py           # 🆕 Pandas导入功能测试
│   ├── test_numpy_functionality.py    # 🆕 NumPy功能完备性测试
│   └── test_numpy_mcp_integration.py  # 🆕 NumPy-MCP集成测试
├── static/                # 静态资源
└── venv/                  # Python 虚拟环境
```

## 🧪 测试验证

### 🎯 功能验证

#### NumPy 功能完备性验证 ✅
- **版本**: NumPy 1.26.4
- **安装状态**: 已在虚拟环境中正确安装
- **基础功能**: 数组操作、数学运算、数据类型支持 - 全部通过
- **高级功能**: 线性代数、随机数生成、统计分析 - 全部通过
- **Pandas集成**: 与Pandas协同工作 - 完美兼容
- **MCP集成**: 在MCP服务环境中稳定运行 - 验证通过
- **性能表现**: 大数组操作和内存管理 - 符合预期

#### Pandas 功能完备性验证 ✅
- **版本**: Pandas 2.3.0
- **安装状态**: 已在虚拟环境中正确安装
- **核心功能**: DataFrame/Series操作、数据读写 - 全部通过
- **Excel支持**: Excel文件读取、写入、格式处理 - 完美支持
- **数据处理**: 清洗、转换、聚合、分析 - 功能完备
- **可视化集成**: 与matplotlib/seaborn协同 - 无缝集成
- **代码执行**: 在run_excel_code中稳定运行 - 验证通过

### 🆕 Excel智能处理功能测试
```bash
# Excel智能处理完整功能测试
python test_complete_functionality.py

# Excel增强功能专项测试
python test_enhanced_excel.py

# Excel功能演示（包含所有新功能）
python demo_excel_features.py

# 🆕 参数传递功能测试
python test_parameter_passing.py

# 🆕 参数传递调试分析
python debug_parameter_passing.py
```

### 🔬 核心依赖功能测试
```bash
# 🆕 Pandas导入和基础功能测试
python test_pandas_import.py

# 🆕 NumPy功能完备性测试
python test_numpy_functionality.py

# 🆕 NumPy与MCP服务集成测试
python test_numpy_mcp_integration.py
```

### 运行测试套件
```bash
# 元数据功能测试
python test_metadata_functions.py

# 图表生成测试
python test_charts.py

# 行数统计测试
python test_row_count.py

# 完整测试套件
pytest tests/
```

### 健康检查
```bash
# 运行系统健康检查
python scripts/health_check.py

# 预期输出
✅ Python版本: Python 3.11.3
✅ 虚拟环境: 虚拟环境存在
✅ 依赖包: 依赖包完整性检查通过
✅ 文件结构: 文件结构完整
✅ 服务器模块: 服务器模块导入成功
✅ Excel智能工具: Excel智能处理模块正常
🎯 总体状态: HEALTHY
```

### 🆕 Excel功能验证
```bash
# 验证Excel智能处理功能
python -c "from excel_smart_tools import *; print('Excel智能工具导入成功')"

# 验证Excel辅助函数
python -c "from excel_helper import *; print('Excel辅助函数导入成功')"

# 🆕 验证NumPy功能
python -c "import numpy as np; print(f'NumPy {np.__version__} 导入成功')"

# 🆕 验证Pandas功能
python -c "import pandas as pd; print(f'Pandas {pd.__version__} 导入成功')"

# 🆕 验证核心数据处理功能
python -c "import numpy as np, pandas as pd; df = pd.DataFrame(np.random.rand(5,3)); print('NumPy+Pandas集成验证成功')"

# 运行功能演示
python demo_excel_features.py
```

## 🛡️ 安全注意事项

### 代码执行限制
以下操作被严格禁止：
- 文件系统操作 (`os.`, `open()`)
- 系统调用 (`sys.`, `subprocess.`)
- 代码注入 (`exec()`, `eval()`)
- 模块导入 (`import os`, `import sys`)

### 资源限制
- 最大文件大小: 100MB
- 代码执行超时: 30秒
- 内存使用限制: 1GB

## 🔧 维护工具

### 日常维护命令
```bash
# 依赖包更新
./scripts/update_dependencies.sh

# 代码质量检查
./scripts/code_quality_check.sh

# 系统维护
./scripts/maintenance.sh
```

### 日志管理
```bash
# 查看服务器日志
tail -f chatExcel.log

# 查看健康检查报告
cat health_report.json
```

## 🚀 性能优化

### Python 3.11 性能提升
- 整体性能提升: 10-60%
- 启动时间减少: 10-20%
- 内存使用优化: 15-25%
- 错误追踪改进: 更清晰的错误信息

### 最佳实践
1. **虚拟环境**: 始终在虚拟环境中运行
2. **内存管理**: 处理大文件时监控内存使用
3. **错误处理**: 利用详细的错误信息进行调试
4. **缓存利用**: 重复操作时利用元数据缓存

## 🐛 故障排除

### 常见问题

#### 1. 模块导入失败
```bash
# 解决方案
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. 文件编码问题
```bash
# 检查文件编码
file -I your_file.csv
# 或使用 chardet 自动检测
```

#### 3. 权限问题
```bash
# 添加执行权限
chmod +x start_py311.sh
chmod +x scripts/*.sh
```

#### 4. 端口占用
```bash
# 检查端口使用
lsof -i :8000
# 终止占用进程
kill -9 <PID>
```

### 获取帮助

如果遇到问题，请按以下步骤操作：

1. 运行健康检查: `python scripts/health_check.py`
2. 查看日志文件: `chatExcel.log`
3. 检查依赖版本: `pip list`
4. 验证 Python 版本: `python --version`

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📞 联系方式

- 项目主页: [GitHub Repository](https://github.com/your-username/chatExcel-mcp-server)
- 问题反馈: [Issues](https://github.com/your-username/chatExcel-mcp-server/issues)
- 文档: [Wiki](https://github.com/your-username/chatExcel-mcp-server/wiki)

---

**chatExcel** - 让Excel数据分析更智能、更高效！ 🚀