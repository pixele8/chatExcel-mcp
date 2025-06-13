# ChatExcel MCP Server - 增强版

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![MCP Protocol](https://img.shields.io/badge/MCP-2024--11--05-green.svg)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![NumPy](https://img.shields.io/badge/NumPy-2.2.1-orange.svg)](https://numpy.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.2.3-blue.svg)](https://pandas.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-5.24.1-red.svg)](https://plotly.com)
[![FastMCP](https://img.shields.io/badge/FastMCP-0.3.0-green.svg)](https://github.com/jlowin/fastmcp)
[![安全增强](https://img.shields.io/badge/安全增强-已启用-red.svg)](#)
[![功能验证](https://img.shields.io/badge/功能验证-通过-brightgreen.svg)](#)

## 📋 项目概述

chatExcel 是一个基于 Model Context Protocol (MCP) 的企业级 Excel 数据处理服务器，集成了 Python pandas 和 Go excelize 库，提供强大的 Excel 文件读取、处理、分析和图表生成功能。增强版新增了安全机制、服务管理、健康监控和依赖管理等企业级特性。

### 🚀 核心特性

#### 🏗️ 双引擎架构
- **Python pandas 引擎**: 强大的数据分析和处理能力
- **Go excelize 引擎**: 高性能 Excel 文件操作
- **智能路由**: 根据任务类型自动选择最优引擎

#### 🧠 智能处理能力
- **智能编码检测**: 自动检测和处理各种文件编码问题
- **多级表头识别**: 智能识别复杂的 Excel 表头结构
- **参数智能推荐**: 基于文件结构自动推荐最佳读取参数
- **缓存优化**: 智能缓存机制提升重复操作性能

#### ✅ 数据验证与质量保证
- **综合数据验证**: 全面的数据完整性和质量检查
- **批量处理**: 支持多文件批量验证和处理
- **错误诊断**: 详细的错误分析和修复建议

#### 📊 可视化与图表
- **交互式图表**: 基于 Chart.js 的动态图表生成
- **多种图表类型**: 支持柱状图、饼图、折线图等
- **Go 图表引擎**: 高性能图表生成和嵌入

#### 🔒 安全增强功能 (新增)
- **安全代码执行**: 沙箱环境中执行用户代码，防止恶意操作
- **权限控制**: 细粒度的操作权限管理
- **输入验证**: 严格的输入参数验证和过滤
- **审计日志**: 完整的操作审计和日志记录

#### 🏥 健康监控系统 (新增)
- **服务健康检查**: 实时监控服务状态和性能
- **自动恢复**: 服务异常时自动重启和恢复
- **性能监控**: CPU、内存、磁盘使用率监控
- **告警机制**: 异常情况自动告警和通知

#### 📦 依赖管理系统 (新增)
- **智能依赖分析**: 自动检测和分析项目依赖
- **版本冲突检测**: 识别和解决依赖版本冲突
- **安全扫描**: 检测依赖包中的安全漏洞
- **自动更新**: 智能更新依赖包到安全版本

#### ⚙️ 配置管理系统 (新增)
- **统一配置**: 集中管理所有服务配置
- **环境隔离**: 支持开发、测试、生产环境配置
- **动态配置**: 运行时动态更新配置
- **配置验证**: 自动验证配置文件的正确性

### 🛠️ MCP 工具列表 (20个)

#### 基础元数据工具
| 工具名称 | 功能描述 | 支持格式 |
|---------|---------|----------|
| `read_metadata` | CSV文件元数据读取和智能分析 | CSV |
| `read_excel_metadata` | Excel文件元数据读取和智能编码检测 | Excel |
| `excel_info_enhanced` | 增强版Excel文件信息获取（Go服务） | Excel |

#### 数据处理工具
| 工具名称 | 功能描述 | 支持格式 |
|---------|---------|----------|
| `run_code` | CSV代码执行引擎（安全沙箱环境） | CSV |
| `run_excel_code` | Excel代码执行引擎（支持复杂格式参数） | Excel |
| `excel_read_enhanced` | 增强版Excel读取（集成Go服务） | Excel |
| `excel_write_enhanced` | 增强版Excel写入（集成Go服务） | Excel |

#### 数据验证工具
| 工具名称 | 功能描述 | 支持格式 |
|---------|---------|----------|
| `verify_data_integrity` | 数据完整性验证和比对核准 | Excel, CSV |
| `validate_data_quality` | 数据质量验证和改进建议 | Excel, CSV |
| `comprehensive_data_verification_tool` | 综合数据验证和核准 | Excel, CSV |
| `batch_data_verification_tool` | 批量数据验证工具 | Excel, CSV |

#### 智能分析工具
| 工具名称 | 功能描述 | 支持格式 |
|---------|---------|----------|
| `suggest_excel_read_parameters_tool` | Excel读取参数智能推荐 | Excel |
| `detect_excel_file_structure_tool` | Excel文件结构检测 | Excel |
| `create_excel_read_template_tool` | Excel读取代码模板生成 | Excel |

#### 图表和可视化工具
| 工具名称 | 功能描述 | 支持格式 |
|---------|---------|----------|
| `excel_chart_enhanced` | 增强版Excel图表创建（Go服务） | Excel |
| `bar_chart_to_html` | 交互式柱状图生成（Chart.js） | 数据数组 |
| `pie_chart_to_html` | 交互式饼图生成（Chart.js） | 数据数组 |
| `line_chart_to_html` | 交互式折线图生成（Chart.js） | 数据数组 |

#### 性能和监控工具
| 工具名称 | 功能描述 | 支持格式 |
|---------|---------|----------|
| `excel_performance_comparison` | Excel性能对比工具 | Excel |
| `your_new_tool_name` | 请填写工具描述 | 请填写支持格式 |

## 🏗️ 架构设计

### 系统架构
```
┌─────────────────┐    ┌─────────────────┐
│   MCP Client    │    │   Go Service    │
│   (Claude等)    │    │   (excelize)    │
└─────────┬───────┘    └─────────┬───────┘
          │                      │
          │ MCP Protocol         │ HTTP API
          │                      │
┌─────────▼──────────────────────▼───────┐
│         Python MCP Server              │
│  ┌─────────────┐  ┌─────────────────┐  │
│  │   pandas    │  │  Excel Go Client │  │
│  │   Engine    │  │     Wrapper     │  │
│  └─────────────┘  └─────────────────┘  │
│  ┌─────────────────────────────────────┐ │
│  │        Cache & Validation           │ │
│  └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### 项目结构

```
chatExcel-mcp/
├── server.py                    # 原始服务器文件
├── enhanced_server.py           # 增强版服务器 (推荐使用)
├── excel-service/               # Go 服务目录
│   ├── main.go                 # Go 服务主文件
│   ├── go.mod                  # Go 模块定义
│   └── go.sum                  # Go 依赖锁定
├── security/                    # 安全模块 (新增)
│   ├── __init__.py
│   ├── secure_executor.py      # 安全代码执行器
│   ├── input_validator.py      # 输入验证器
│   └── audit_logger.py         # 审计日志
├── service_management/          # 服务管理模块 (新增)
│   ├── __init__.py
│   ├── health_manager.py       # 健康监控管理器
│   ├── dependency_manager.py   # 依赖管理器
│   └── config_manager.py       # 配置管理器
├── config/                      # 配置文件目录 (新增)
│   ├── system.json             # 系统配置
│   ├── security.json           # 安全配置
│   └── health.json             # 健康检查配置
├── test/                        # 测试文件目录
│   ├── debug_*.py              # 调试脚本
│   └── test_*.py               # 测试脚本
├── tests/                       # 单元测试目录
│   ├── test_enhanced_features.py # 增强功能测试
│   └── test_*.py               # 其他测试文件
├── static/                      # 静态文件
│   ├── chart.html              # 图表模板
│   └── chart.js                # 图表脚本
├── temp/                        # 临时文件目录
├── logs/                        # 日志文件目录
├── record/                      # 记录文件目录
│   └── record.md               # 开发记录
├── requirements.txt             # Python 依赖
├── pyproject.toml              # 项目配置
├── ENHANCED_USAGE_GUIDE.md     # 增强版使用指南
└── README.md                   # 项目文档
```

### 核心组件

1. **MCP Server Core** (`server.py` / `enhanced_server.py`)
   - 工具注册和路由
   - 请求处理和响应格式化
   - 错误处理和日志记录
   - 安全增强功能 (增强版)

2. **Excel Processing Engines**
   - **pandas Engine**: 复杂数据分析和处理
   - **Go excelize Engine**: 高性能文件操作
   - **智能路由**: 自动选择最优处理引擎

3. **Data Verification System**
   - `comprehensive_data_verification.py`: 综合验证引擎
   - `data_verification.py`: 基础验证工具
   - 批量处理和报告生成

4. **Cache Management**
   - `cache_manager.py`: 智能缓存管理
   - `cache_config.json`: 缓存配置
   - 自动清理和优化

5. **Security Module** (新增)
   - 安全代码执行沙箱
   - 输入验证和过滤
   - 审计日志记录

6. **Service Management** (新增)
   - 健康监控系统
   - 依赖管理器
   - 配置管理器

## 🚀 快速开始

### 环境要求

- Python 3.11+
- Go 1.21+ (用于 Excel 服务)
- 操作系统: macOS, Linux, Windows
- 内存: 建议 4GB+
- 磁盘空间: 建议 2GB+

### 安装步骤

#### 方式一: 自动部署 (推荐)

**一键启动脚本（推荐）**

```bash
# 克隆项目
git clone <repository-url>
cd chatExcel-mcp

# 快速启动增强版服务器
./start.sh

# 或者指定服务器类型
./start.sh --type enhanced    # 增强版（默认）
./start.sh --type standard    # 标准版

# 首次使用，运行部署脚本
./start.sh --deploy

# 查看服务状态
./start.sh --status

# 停止所有服务
./start.sh --stop

# 查看帮助
./start.sh --help
```

**Python脚本启动**

```bash
# 运行自动部署脚本
python scripts/deploy.py

# 启动增强版服务器
python scripts/start_server.py --type enhanced

# 启动标准版服务器
python scripts/start_server.py --type standard
```

自动部署脚本将:
- 检查系统环境
- 安装 Python 依赖
- 构建 Go 服务
- 配置安全设置
- 启动所有服务
- 运行健康检查

**直接启动**

```bash
# 启动增强版服务器
python enhanced_server.py

# 启动标准版服务器
python server.py
```

#### 方式二: 手动安装

1. **克隆项目**
```bash
git clone <repository-url>
cd chatExcel-mcp
```

2. **安装 Python 依赖**
```bash
# 创建虚拟环境 (推荐)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

3. **构建 Go 服务**
```bash
cd excel-service
go mod tidy
go build -o excel_service main.go
cd ..
```

4. **配置系统**
```bash
# 复制配置模板
cp config/system.json.template config/system.json
cp config/security.json.template config/security.json

# 编辑配置文件 (可选)
vim config/system.json
```

5. **启动服务**

**增强版服务器 (推荐)**
```bash
python enhanced_server.py
```

**原始服务器**
```bash
python server.py
```

6. **验证部署**
```bash
# 检查服务状态
curl http://localhost:8080/health
curl http://localhost:8081/health

# 运行测试套件
python -m pytest tests/
```

### 配置文件

#### MCP 配置文件

项目提供了多个预配置的 MCP 配置文件：

- `mcp_config_absolute.json`: 绝对路径配置（推荐生产环境）
- `mcp_config_relative.json`: 相对路径配置（开发环境）
- `mcp_config_flexible.json`: 灵活配置
- `mcp_config_optimized.json`: 性能优化配置

#### 系统配置 (`config/system.json`)

```json
{
  "services": {
    "main_service": {
      "host": "localhost",
      "port": 8000,
      "debug": false,
      "dependencies": ["excel_service"],
      "environment": "production"
    },
    "excel_service": {
      "host": "localhost",
      "port": 8080,
      "timeout": 30,
      "max_retries": 3
    }
  },
  "cache": {
    "enabled": true,
    "max_size": 100,
    "ttl": 3600
  },
  "logging": {
    "level": "INFO",
    "file": "logs/chatexcel.log",
    "max_size": "10MB",
    "backup_count": 5
  }
}
```

#### 安全配置 (`config/security.json`)

```json
{
  "code_execution": {
    "enabled": true,
    "timeout": 30,
    "memory_limit": "256MB",
    "allowed_modules": ["pandas", "numpy", "matplotlib"],
    "blocked_functions": ["exec", "eval", "__import__"]
  },
  "api_security": {
    "rate_limiting": {
      "enabled": true,
      "requests_per_minute": 60
    },
    "authentication": {
      "enabled": false,
      "method": "token"
    }
  },
  "audit": {
    "enabled": true,
    "log_file": "logs/audit.log",
    "log_level": "INFO"
  }
}
```

#### 健康检查配置 (`config/health.json`)

```json
{
  "health_checks": {
    "interval": 30,
    "timeout": 10,
    "retries": 3
  },
  "monitoring": {
    "cpu_threshold": 80,
    "memory_threshold": 85,
    "disk_threshold": 90
  },
  "recovery": {
    "auto_restart": true,
    "max_restarts": 3,
    "restart_delay": 5
  }
}
```

## 📊 使用示例

### 基础 Excel 读取
```python
# 使用 MCP 工具读取 Excel 文件
result = await mcp_client.call_tool(
    "read_excel_metadata",
    {"file_path": "/path/to/your/file.xlsx"}
)
```

### 数据处理代码执行
```python
# 执行数据处理代码
result = await mcp_client.call_tool(
    "run_excel_code",
    {
        "file_path": "/path/to/your/file.xlsx",
        "code": "df.groupby('category').sum()",
        "sheet_name": "Sheet1"
    }
)
```

### 图表生成
```python
# 创建交互式图表
result = await mcp_client.call_tool(
    "excel_chart_enhanced",
    {
        "file_path": "/path/to/your/file.xlsx",
        "chart_type": "col",
        "data_range": "A1:D10",
        "title": "销售数据分析"
    }
)
```

### 批量数据验证
```python
# 批量验证多个文件
result = await mcp_client.call_tool(
    "batch_data_verification_tool",
    {
        "file_paths": [
            "/path/to/file1.xlsx",
            "/path/to/file2.xlsx"
        ],
        "verification_level": "comprehensive"
    }
)
```

### 增强版功能示例

#### 安全代码执行
```python
# 安全执行数据处理代码
result = await mcp_client.call_tool(
    "execute_safe_code",
    {
        "code": "df.groupby('category').sum()",
        "context": {"df": "your_dataframe_reference"}
    }
)
```

#### 健康监控
```python
# 检查服务健康状态
result = await mcp_client.call_tool(
    "check_service_health",
    {}
)

# 获取系统性能指标
result = await mcp_client.call_tool(
    "get_system_metrics",
    {
        "metrics": ["cpu", "memory", "disk"]
    }
)
```

#### 依赖管理
```python
# 分析项目依赖
result = await mcp_client.call_tool(
    "analyze_dependencies",
    {
        "check_security": true,
        "check_updates": true
    }
)

# 更新依赖包
result = await mcp_client.call_tool(
    "update_dependencies",
    {
        "packages": ["pandas", "numpy"],
        "auto_approve": false
    }
)
```

## 🔧 高级配置

### 性能优化

1. **缓存配置**
   - 调整缓存大小和 TTL
   - 启用智能缓存策略
   - 配置分布式缓存 (Redis)

2. **并发处理**
   - 配置工作线程数
   - 调整请求队列大小
   - 启用异步处理

3. **内存管理**
   - 设置内存限制
   - 启用垃圾回收优化
   - 配置内存监控阈值

### 安全配置

1. **访问控制**
   - 配置 IP 白名单
   - 设置 API 密钥验证
   - 启用 OAuth2 认证

2. **数据保护**
   - 启用数据加密
   - 配置敏感数据脱敏
   - 设置数据访问审计

3. **代码执行安全**
   - 配置沙箱环境
   - 设置执行超时
   - 限制可用模块和函数

### 监控和告警

1. **健康监控**
   - 配置健康检查间隔
   - 设置性能阈值
   - 启用自动恢复

2. **告警配置**
   - 配置邮件告警
   - 设置 Webhook 通知
   - 集成监控系统 (Prometheus)

### 缓存配置

编辑 `cache_config.json` 来自定义缓存行为：

```json
{
  "cache_settings": {
    "max_cache_size_mb": 10,
    "cache_expiry_days": 7,
    "auto_cleanup_interval": 10
  },
  "monitoring": {
    "enable_size_monitoring": true,
    "size_warning_threshold_mb": 8
  }
}
```

### Go 服务配置

Go 服务默认运行在 `localhost:8080`，可以通过环境变量配置：

```bash
export EXCEL_SERVICE_HOST=localhost
export EXCEL_SERVICE_PORT=8080
```

## 🧪 测试

### 运行测试套件

```bash
# 运行所有测试
python -m pytest test/

# 运行特定测试
python test/comprehensive_mcp_test.py

# 运行性能测试
python test/demo_excel_features.py
```

### 测试文件说明

- `test/comprehensive_mcp_test.py`: 完整功能测试
- `test/demo_excel_features.py`: 功能演示和性能测试
- `test/create_test_excel.py`: 测试数据生成
- `test/simple_test.py`: 基础功能测试

## 📈 性能优化

### 缓存策略

1. **编码检测缓存**: 避免重复检测文件编码
2. **元数据缓存**: 缓存文件结构信息
3. **自动清理**: 定期清理过期缓存

### 双引擎优势

| 操作类型 | pandas 引擎 | Go excelize 引擎 | 推荐场景 |
|---------|-------------|------------------|----------|
| 数据分析 | ✅ 优秀 | ❌ 不支持 | 复杂数据处理 |
| 文件读写 | ⚠️ 中等 | ✅ 优秀 | 大文件操作 |
| 图表生成 | ⚠️ 基础 | ✅ 优秀 | 专业图表 |
| 内存使用 | ⚠️ 较高 | ✅ 较低 | 资源受限环境 |

## 🛠️ 维护和监控

### 自动维护脚本

```bash
# 缓存维护
./scripts/cache_maintenance.sh

# 健康检查
python scripts/health_check.py

# 依赖更新
./scripts/update_dependencies.sh
```

### 日志和监控

- **应用日志**: 记录在 `logs/` 目录
- **缓存日志**: `cache_maintenance.log`
- **性能监控**: 内置性能对比工具

## 🤝 贡献指南

我们欢迎社区贡献！请遵循以下步骤：

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发规范

- 遵循 PEP 8 代码风格
- 添加适当的测试用例
- 更新相关文档
- 确保所有测试通过
- 安全功能需要额外的安全审查
- 新增功能需要更新配置文件模板

### 测试要求

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行增强功能测试
python -m pytest tests/test_enhanced_features.py -v

# 运行安全测试
python -m pytest tests/test_security.py -v

# 检查代码覆盖率
python -m pytest --cov=. tests/
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP 协议支持
- [FastMCP](https://github.com/jlowin/fastmcp) - 快速 MCP 开发框架
- [pandas](https://pandas.pydata.org/) - 强大的数据分析库
- [excelize](https://github.com/qax-os/excelize) - Go Excel 库
- [Chart.js](https://www.chartjs.org/) - 图表可视化库
- [psutil](https://github.com/giampaolo/psutil) - 系统监控库

## 📚 相关文档

- **[快速开始指南](QUICK_START.md)** - 一分钟快速上手 🚀
- [增强版使用指南](ENHANCED_USAGE_GUIDE.md) - 详细的增强功能使用说明
- [开发记录](record/record.md) - 项目开发历程和问题解决记录
- [更新日志](CHANGELOG.md) - 版本更新历史

## 📞 支持

如果您遇到问题或有建议，请：

1. 查看 [增强版使用指南](ENHANCED_USAGE_GUIDE.md)
2. 查看 [FAQ](#常见问题)
3. 搜索现有 [Issues](../../issues)
4. 创建新的 Issue
5. 联系维护者

### 紧急安全问题

如果发现安全漏洞，请通过私有渠道联系维护者，不要公开披露。

## 🆘 故障排除

### 常见问题

1. **Go 服务连接失败**
   - 检查 Go 服务是否正常运行
   - 验证端口 8080 是否被占用
   - 检查防火墙设置
   - 检查服务依赖状态

2. **编码检测错误**
   - 清理编码缓存：`rm -rf .encoding_cache`
   - 检查文件权限
   - 验证文件格式
   - 检查编码问题

3. **内存使用过高**
   - 调整缓存大小配置
   - 使用 Go 引擎处理大文件
   - 启用自动清理
   - 启用内存监控

4. **安全模块问题**
   - 检查沙箱环境配置
   - 验证权限设置
   - 查看审计日志
   - 检查代码执行限制

5. **健康监控异常**
   - 检查监控配置
   - 验证阈值设置
   - 查看系统资源使用
   - 检查自动恢复机制

### 日志分析

查看不同类型的日志文件：

```bash
# 主服务日志
tail -f logs/chatexcel.log

# 安全审计日志
tail -f logs/audit.log

# 健康监控日志
tail -f logs/health.log

# 错误日志
tail -f logs/error.log

# 性能监控日志
tail -f logs/performance.log
```

### 调试模式

启用调试模式获取更详细的信息：

```bash
# 启用调试模式
export DEBUG=true
python enhanced_server.py

# 或修改配置文件
# config/system.json -> services.main_service.debug = true
```

### 获取帮助

- 查看 [Issues](../../issues) 页面
- 阅读 `record.md` 了解已知问题和解决方案
- 运行诊断工具：`python test/diagnose_mcp_setup.py`

## 📚 更新日志

查看 `record.md` 文件了解详细的更新历史和问题解决记录。

---

**开发团队**: ChatExcel MCP 开发组  
**最后更新**: 2025年1月  
**版本**: 2.0.0