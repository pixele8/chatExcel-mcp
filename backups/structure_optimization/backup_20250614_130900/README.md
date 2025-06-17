# ChatExcel MCP Server

> 🚀 **企业级Excel智能处理与数据分析MCP服务器** - 基于FastMCP构建的高性能数据处理解决方案

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://python.org)
[![FastMCP](https://img.shields.io/badge/FastMCP-0.3.0-green.svg)](https://github.com/jlowin/fastmcp)
[![Go Version](https://img.shields.io/badge/go-1.24%2B-00ADD8.svg)](https://golang.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.4.0-orange.svg)](pyproject.toml)
[![Formulas](https://img.shields.io/badge/formulas-1.2.10-blue.svg)](https://pypi.org/project/formulas/)
[![Security](https://img.shields.io/badge/security-enhanced-green.svg)](#-安全考虑)
[![Performance](https://img.shields.io/badge/performance-optimized-brightgreen.svg)](#-性能优化)
[![Health Check](https://img.shields.io/badge/health-monitoring-blue.svg)](#-运维工具)

## 📋 项目概述

ChatExcel MCP Server 是一个功能强大的模型上下文协议(MCP)服务器，专门为Excel文件处理、数据分析和可视化而设计。项目集成了Python生态系统的最佳数据处理库，并通过Go excelize库提供高性能Excel操作能力。

### 🎯 核心特性

- **24个专业MCP工具** - 覆盖数据读取、处理、验证、可视化、公式计算全流程
- **双引擎架构** - Python pandas + Go excelize 混合处理引擎
- **Excel公式引擎** - 基于formulas库的完整Excel公式解析、编译和执行系统
- **智能参数推荐** - 自动检测Excel文件结构并推荐最佳读取参数
- **企业级安全** - 多层安全机制，代码沙箱执行环境，公式安全验证
- **性能优化** - 缓存机制、并发处理、内存优化
- **健康监控** - 完整的服务监控、日志记录和错误追踪
- **可视化支持** - 交互式图表生成(Chart.js、Plotly、Matplotlib)

## 🛠️ MCP工具列表

本项目提供 **24个专业MCP工具**，覆盖Excel数据处理、分析、验证和公式计算的完整生命周期。

### 📊 数据读取与元数据工具 (4个)
| 工具名称 | 功能描述 | 主要特性 |
|---------|----------|----------|
| `read_metadata` | CSV文件元数据读取和智能分析 | 编码检测、分隔符识别、数据统计 |
| `read_excel_metadata` | Excel文件元数据读取和完整性验证 | 多工作表分析、智能编码检测 |
| `excel_read_enhanced` | 增强版Excel读取工具 | Go excelize集成、智能参数推荐 |
| `excel_info_enhanced` | 增强版Excel文件信息获取 | 详细文件分析、工作表统计 |

### 🔧 数据处理与执行工具 (6个)
| 工具名称 | 功能描述 | 主要特性 |
|---------|----------|----------|
| `run_excel_code` | Excel代码执行引擎 | 安全沙箱、复杂格式参数支持 |
| `run_code` | CSV代码执行引擎 | 安全环境、pandas集成 |
| `excel_write_enhanced` | 增强版Excel写入工具 | 格式优化、样式支持 |
| `excel_chart_enhanced` | 增强版Excel图表生成 | 多种图表类型、自定义样式 |
| `excel_performance_comparison` | Excel性能对比分析 | Go vs Python性能测试 |
| `batch_data_verification_tool` | 批量数据验证工具 | 并发处理、批量报告 |

### 📈 数据可视化工具 (3个)
| 工具名称 | 功能描述 | 主要特性 |
|---------|----------|----------|
| `bar_chart_to_html` | 交互式柱状图生成 | Chart.js、响应式设计 |
| `pie_chart_to_html` | 交互式饼图生成 | 动画效果、数据标签 |
| `line_chart_to_html` | 交互式折线图生成 | 多维数据、趋势分析 |

### 🔍 数据验证与质量工具 (3个)
| 工具名称 | 功能描述 | 主要特性 |
|---------|----------|----------|
| `verify_data_integrity` | 数据完整性验证和比对核准 | 多种验证模式、详细报告 |
| `validate_data_quality` | 数据质量验证和改进建议 | 质量评分、优化建议 |
| `comprehensive_data_verification_tool` | 综合数据验证和核准工具 | 全面验证、质量评估、比对核准 |

### 🤖 智能辅助工具 (3个)
| 工具名称 | 功能描述 | 主要特性 |
|---------|----------|----------|
| `suggest_excel_read_parameters_tool` | Excel读取参数智能推荐 | 结构分析、参数优化 |
| `detect_excel_file_structure_tool` | Excel文件结构检测 | 多级表头、数据区域识别 |
| `create_excel_read_template_tool` | Excel读取代码模板生成 | 智能模板、参数配置 |

### 🧮 Excel公式处理工具 (5个) - **新增**
| 工具名称 | 功能描述 | 主要特性 |
|---------|----------|----------|
| `parse_formula` | Excel公式解析器 | AST解析、语法分析、安全验证 |
| `compile_workbook` | Excel工作簿编译器 | 公式编译、代码生成、依赖分析 |
| `execute_formula` | Excel公式执行引擎 | 安全执行、上下文支持、结果验证 |
| `analyze_dependencies` | Excel公式依赖分析 | 依赖图生成、循环检测、影响分析 |
| `validate_formula` | Excel公式验证器 | 安全检查、语法验证、风险评估 |

---

## 🧮 Excel公式处理功能详解

### 功能概述

基于 `formulas==1.2.10` 库构建的完整Excel公式处理系统，提供从解析到执行的全流程支持。

### 核心工具详解

#### 1. `parse_formula` - 公式解析器
```python
# 解析Excel公式并获取AST结构
result = parse_formula("=SUM(A1:A10)*2", validate_security=True)
# 返回: 语法树、函数列表、引用单元格、安全状态
```

#### 2. `compile_workbook` - 工作簿编译器
```python
# 将Excel文件编译为Python代码或JSON结构
result = compile_workbook("/path/to/file.xlsx", output_format="python")
# 支持格式: 'python', 'json'
```

#### 3. `execute_formula` - 公式执行引擎
```python
# 在指定上下文中执行Excel公式
context = '{"A1": 10, "A2": 20}'
result = execute_formula("=A1+A2", context)
# 返回: 计算结果、执行状态、性能指标
```

#### 4. `analyze_dependencies` - 依赖分析器
```python
# 分析Excel文件中的公式依赖关系
result = analyze_dependencies("/path/to/file.xlsx")
# 返回: 依赖图、循环检测、影响分析
```

#### 5. `validate_formula` - 公式验证器
```python
# 验证公式的安全性和有效性
result = validate_formula("=SUM(A1:A10)")
# 返回: 安全评估、语法检查、风险等级
```

### 安全特性

- **AST安全分析**: 检测潜在的恶意代码模式
- **函数白名单**: 仅允许安全的Excel函数
- **引用验证**: 验证单元格引用的合法性
- **执行沙箱**: 隔离的公式执行环境

### 性能优化

- **缓存机制**: 解析结果智能缓存
- **并发支持**: 多公式并行处理
- **内存管理**: 大文件分块处理
- **错误恢复**: 优雅的异常处理

---

## 🚀 快速开始

### 环境要求

- **Python**: 3.11+
- **操作系统**: macOS, Linux, Windows
- **内存**: 建议4GB+
- **磁盘空间**: 500MB+

### 一键部署

```bash
# 克隆项目
git clone <repository-url>
cd chatExcel-mcp

# 一键部署（推荐）
./start.sh --deploy

# 启动增强版服务器
./start.sh
```

### 手动安装

```bash
# 1. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务器
python3 server.py
```

### Docker部署

```bash
# 构建镜像
docker build -t chatexcel-mcp .

# 运行容器
docker run -p 8080:8080 -v $(pwd)/data:/app/data chatexcel-mcp
```

## 📖 使用示例

### 基础Excel读取

```python
# 使用MCP工具读取Excel文件
result = await mcp_client.call_tool(
    "read_excel_metadata",
    {"file_path": "/path/to/your/file.xlsx"}
)

print(f"工作表数量: {result['sheets_count']}")
print(f"数据行数: {result['total_rows']}")
```

### 智能参数推荐

```python
# 获取最佳读取参数
params = await mcp_client.call_tool(
    "suggest_excel_read_parameters",
    {"file_path": "/path/to/complex.xlsx"}
)

# 使用推荐参数读取
data = await mcp_client.call_tool(
    "excel_read_enhanced",
    {
        "file_path": "/path/to/complex.xlsx",
        **params["recommended_params"]
    }
)
```

### 数据处理与分析

```python
# 执行数据分析代码
analysis = await mcp_client.call_tool(
    "run_excel_code",
    {
        "file_path": "/path/to/data.xlsx",
        "code": """
        # 数据清洗和分析
        df_clean = df.dropna()
        summary = df_clean.describe()
        correlation = df_clean.corr()
        
        print("数据摘要:")
        print(summary)
        """
    }
)
```

### 可视化图表生成

```python
# 生成交互式柱状图
chart = await mcp_client.call_tool(
    "bar_chart_to_html",
    {
        "labels": ["Q1", "Q2", "Q3", "Q4"],
        "datasets": [
            {
                "label": "销售额",
                "data": [120, 150, 180, 200]
            }
        ],
        "title": "季度销售报告"
    }
)

print(f"图表已生成: {chart['filepath']}")
```

## 🏗️ 项目架构

### 系统架构图

```mermaid
graph TB
    A[MCP Client] --> B[FastMCP Server]
    B --> C[Tool Router]
    C --> D[Excel Engine]
    C --> E[Data Engine]
    C --> F[Chart Engine]
    
    D --> G[Python pandas]
    D --> H[Go excelize]
    D --> I[openpyxl]
    
    E --> J[Data Validator]
    E --> K[Code Executor]
    E --> L[Cache Manager]
    
    F --> M[Chart.js]
    F --> N[Plotly]
    F --> O[Matplotlib]
    
    P[Security Layer] --> C
    Q[Monitoring] --> B
    R[Logging] --> B
```

### 核心模块

#### 📁 主要文件结构

```
chatExcel-mcp/
├── server.py                 # 主服务器文件（19个MCP工具）
├── enhanced_server.py        # 增强版服务器
├── config.py                 # 配置管理
├── excel_enhanced_tools.py   # Excel增强工具
├── excel_smart_tools.py      # Excel智能工具
├── data_verification.py      # 数据验证引擎
├── comprehensive_data_verification.py  # 综合数据验证
├── excel-service/           # Go excelize服务
│   ├── main.go
│   ├── go.mod
│   └── go.sum
├── templates/               # 图表模板
│   ├── barchart_template.html
│   ├── linechart_template.html
│   └── piechart_template.html
├── scripts/                 # 运维脚本
│   ├── deploy.py
│   ├── health_check.py
│   └── maintenance.sh
├── config/                  # 配置文件
│   ├── runtime.yaml
│   ├── security.json
│   └── system.json
└── tests/                   # 测试套件
    ├── unit/
    ├── integration/
    └── performance/
```

#### 🔧 引擎类设计

- **ExcelEnhancedProcessor**: 高性能Excel处理引擎
- **DataVerificationEngine**: 数据验证和质量检查引擎
- **ComprehensiveDataVerifier**: 综合数据验证器
- **SecureCodeExecutor**: 安全代码执行器

### 数据流架构

#### Excel处理流程

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant E as Excel Engine
    participant G as Go Service
    participant P as Python Engine
    
    C->>S: 调用excel_read_enhanced
    S->>E: 路由到Excel引擎
    E->>G: 尝试Go excelize
    alt Go服务可用
        G-->>E: 返回高性能结果
    else Go服务不可用
        E->>P: 降级到pandas
        P-->>E: 返回标准结果
    end
    E-->>S: 返回处理结果
    S-->>C: 返回最终结果
```

#### 数据验证流程

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant V as Validator
    participant R as Reporter
    
    C->>S: 调用verify_data_integrity
    S->>V: 启动验证引擎
    V->>V: 结构验证
    V->>V: 数据类型检查
    V->>V: 完整性验证
    V->>V: 统计分析
    V->>R: 生成验证报告
    R-->>S: 返回详细报告
    S-->>C: 返回验证结果
```

#### 代码执行流程

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant SE as Security Engine
    participant EX as Executor
    participant M as Monitor
    
    C->>S: 调用run_excel_code
    S->>SE: 安全检查
    SE->>SE: 黑名单过滤
    SE->>SE: 语法验证
    SE-->>S: 安全通过
    S->>EX: 沙箱执行
    EX->>M: 监控执行
    M->>M: 资源监控
    M->>M: 超时检查
    EX-->>S: 返回执行结果
    S-->>C: 返回最终结果
```

### 性能优化架构

#### 缓存机制

```mermaid
graph LR
    A[请求] --> B{缓存检查}
    B -->|命中| C[返回缓存]
    B -->|未命中| D[处理请求]
    D --> E[更新缓存]
    E --> F[返回结果]
    
    G[缓存策略]
    G --> H[LRU淘汰]
    G --> I[TTL过期]
    G --> J[内存限制]
```

#### 并发处理

```python
# 并发处理示例
class ConcurrentProcessor:
    def __init__(self, max_workers=4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.semaphore = asyncio.Semaphore(max_workers)
    
    async def process_batch(self, tasks):
        async with self.semaphore:
            futures = [self.executor.submit(task) for task in tasks]
            results = await asyncio.gather(*futures)
            return results
```

### 安全架构设计

#### 多层安全防护

```mermaid
graph TB
    A[用户请求] --> B[输入验证层]
    B --> C[权限检查层]
    C --> D[代码安全层]
    D --> E[执行沙箱层]
    E --> F[输出过滤层]
    F --> G[审计日志层]
    
    H[安全策略]
    H --> I[黑名单过滤]
    H --> J[白名单验证]
    H --> K[资源限制]
    H --> L[超时控制]
```

#### 错误处理机制

```mermaid
graph LR
    A[异常发生] --> B{异常类型}
    B -->|安全异常| C[安全日志]
    B -->|业务异常| D[业务日志]
    B -->|系统异常| E[系统日志]
    
    C --> F[告警通知]
    D --> G[用户反馈]
    E --> H[运维通知]
    
    F --> I[安全响应]
    G --> J[错误恢复]
    H --> K[系统修复]
```

### 扩展性设计

#### 插件架构

```python
# 插件接口定义
class MCPToolPlugin:
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
    
    def register_tools(self, mcp_server):
        """注册MCP工具"""
        raise NotImplementedError
    
    def initialize(self, config: dict):
        """初始化插件"""
        pass
    
    def cleanup(self):
        """清理资源"""
        pass

# 插件管理器
class PluginManager:
    def __init__(self):
        self.plugins = {}
    
    def load_plugin(self, plugin_class, config=None):
        plugin = plugin_class()
        plugin.initialize(config or {})
        self.plugins[plugin.name] = plugin
        return plugin
```

#### 配置管理

```python
# 动态配置示例
class ConfigManager:
    def __init__(self, config_path="config/"):
        self.config_path = Path(config_path)
        self.configs = {}
        self.watchers = {}
    
    def load_config(self, name: str) -> dict:
        config_file = self.config_path / f"{name}.yaml"
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        self.configs[name] = config
        return config
    
    def watch_config(self, name: str, callback):
        """监控配置文件变化"""
        self.watchers[name] = callback
```

### 监控与运维架构

#### 健康检查

```python
# 健康检查示例
class HealthChecker:
    def __init__(self):
        self.checks = {
            "database": self.check_database,
            "cache": self.check_cache,
            "disk_space": self.check_disk_space,
            "memory": self.check_memory
        }
    
    async def run_health_check(self) -> dict:
        results = {}
        for name, check_func in self.checks.items():
            try:
                results[name] = await check_func()
            except Exception as e:
                results[name] = {"status": "error", "error": str(e)}
        
        overall_status = "healthy" if all(
            r.get("status") == "healthy" for r in results.values()
        ) else "unhealthy"
        
        return {
            "status": overall_status,
            "checks": results,
            "timestamp": datetime.utcnow().isoformat()
        }
```

#### 日志与监控

```mermaid
graph TB
    A[应用日志] --> B[日志收集器]
    C[性能指标] --> D[指标收集器]
    E[错误追踪] --> F[错误收集器]
    
    B --> G[日志存储]
    D --> H[指标存储]
    F --> I[错误存储]
    
    G --> J[日志分析]
    H --> K[监控告警]
    I --> L[错误分析]
    
    J --> M[运维仪表板]
    K --> M
    L --> M
```

## 🧪 测试与验证

### 运行测试套件

```bash
# 运行所有测试
python3 -m pytest tests/ -v

# 运行特定测试
python3 comprehensive_mcp_test.py
python3 final_verification.py

# 性能测试
python3 test/performance/benchmark.py
```

### 健康检查

```bash
# 服务健康检查
curl http://localhost:8080/health

# 详细诊断
python3 diagnose_mcp_setup.py

# Excel功能验证
python3 demo_excel_features.py
```

### 核心依赖验证

```bash
# NumPy和Pandas功能验证
python3 -c "import numpy as np; import pandas as pd; print('✅ 核心依赖正常')"

# Excel智能处理功能测试
python3 test_excel_smart_features.py

# Go服务连接测试
python3 excel_go_client.py --test
```

## 🔒 安全考虑

### 代码执行安全

- **黑名单过滤**: 禁止危险操作（os, sys, subprocess等）
- **沙箱环境**: 隔离代码执行环境
- **资源限制**: 内存、CPU、执行时间限制
- **输入验证**: 严格的参数验证和类型检查

### 文件访问安全

- **路径验证**: 防止目录遍历攻击
- **文件大小限制**: 防止大文件攻击
- **格式验证**: 确保文件格式正确性
- **权限检查**: 文件读写权限验证

### 网络安全

- **HTTPS支持**: 加密传输
- **认证机制**: API密钥验证
- **速率限制**: 防止DDoS攻击
- **审计日志**: 完整的操作记录

## 🛠️ 运维工具

### 自动化脚本

```bash
# 部署脚本
./scripts/deploy.py --env production

# 健康检查
./scripts/health_check.py --detailed

# 维护脚本
./scripts/maintenance.sh --clean-cache

# 依赖更新
./scripts/update_dependencies.sh
```

### 缓存管理

```bash
# 清理缓存
python3 cache_manager.py --clean

# 缓存统计
python3 cache_manager.py --stats

# 缓存配置
vim cache_config.json
```

### 日志管理

```bash
# 查看实时日志
tail -f logs/chatExcel.log

# 日志分析
python3 scripts/log_analyzer.py --date today

# 日志轮转
logrotate config/logrotate.conf
```

## ⚡ 性能优化

### 内存优化

- **分块读取**: 大文件分块处理
- **内存池**: 对象重用机制
- **垃圾回收**: 主动内存清理
- **缓存策略**: LRU缓存淘汰

### 并发优化

- **异步处理**: asyncio并发模型
- **线程池**: CPU密集型任务并行
- **连接池**: 数据库连接复用
- **队列机制**: 任务队列管理

### I/O优化

- **批量操作**: 减少I/O次数
- **压缩传输**: 数据压缩传输
- **预读取**: 智能数据预加载
- **缓存命中**: 提高缓存命中率

## 🐛 故障排除

### 常见问题

#### 1. 服务启动失败

```bash
# 检查端口占用
lsof -i :8080

# 检查依赖
pip check

# 查看详细错误
python3 server.py --debug
```

#### 2. Excel读取失败

```bash
# 检查文件权限
ls -la /path/to/file.xlsx

# 验证文件格式
file /path/to/file.xlsx

# 测试读取
python3 simple_test.py /path/to/file.xlsx
```

#### 3. Go服务连接失败

```bash
# 检查Go服务状态
ps aux | grep excel-service

# 重启Go服务
cd excel-service && ./excel-service

# 测试连接
curl http://localhost:8081/health
```

### 调试工具

```bash
# 简单调试
python3 simple_debug.py

# 全面诊断
python3 diagnose_mcp_setup.py

# 性能分析
python3 -m cProfile server.py
```

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

## 🤝 贡献指南

我们欢迎社区贡献！请遵循以下步骤：

1. **Fork** 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 **Pull Request**

### 开发规范

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 代码风格
- 添加适当的测试用例
- 更新相关文档
- 确保所有测试通过

### 代码质量检查

```bash
# 代码格式化
black .

# 代码检查
flake8 .

# 类型检查
mypy .

# 安全检查
bandit -r .
```

## 📞 联系方式

- **项目维护者**: ChatExcel Team
- **问题反馈**: [GitHub Issues](https://github.com/your-repo/chatExcel-mcp/issues)
- **功能建议**: [GitHub Discussions](https://github.com/your-repo/chatExcel-mcp/discussions)
- **技术支持**: support@chatexcel.com

## 🙏 致谢

感谢以下开源项目的支持：

- [FastMCP](https://github.com/jlowin/fastmcp) - MCP服务器框架
- [pandas](https://pandas.pydata.org/) - 数据分析库
- [openpyxl](https://openpyxl.readthedocs.io/) - Excel文件处理
- [excelize](https://github.com/qax-os/excelize) - Go Excel库
- [Chart.js](https://www.chartjs.org/) - 图表可视化
- [Plotly](https://plotly.com/) - 交互式图表

---

## 🎯 Excel数据处理工作流程 - 结构化提示词指南

### 📋 概述

基于ChatExcel MCP Server的31个专业工具，本指南提供了一套完整的结构化提示词体系，帮助用户高效完成Excel文件的数据统计、分析和操作任务。通过链式思维和工具组合，实现从数据探索到深度分析的全流程自动化。

### 🔄 核心工作流程架构

```mermaid
graph TB
    A[文件探索阶段] --> B[数据质量评估]
    B --> C[智能参数优化]
    C --> D[数据读取与预处理]
    D --> E[数据分析与计算]
    E --> F[可视化与报告]
    F --> G[结果验证与输出]
    
    A1[文件结构检测] --> A
    A2[元数据分析] --> A
    
    B1[质量检查] --> B
    B2[完整性验证] --> B
    
    C1[参数推荐] --> C
    C2[模板生成] --> C
    
    D1[增强读取] --> D
    D2[数据清洗] --> D
    
    E1[代码执行] --> E
    E2[公式计算] --> E
    
    F1[图表生成] --> F
    F2[报告输出] --> F
```

### 🚀 阶段一：文件探索与结构分析

#### 1.1 初始文件探索提示词

```markdown
# Excel文件智能探索分析

请按以下步骤对Excel文件进行全面探索：

## 第一步：基础信息获取
使用 `excel_info_enhanced` 工具获取文件基本信息：
- 文件大小和创建时间
- 工作表数量和名称
- 总体数据规模评估

## 第二步：结构深度检测
使用 `detect_excel_file_structure_tool` 进行结构分析：
- 识别多级表头结构
- 定位数据区域边界
- 检测合并单元格分布
- 分析数据类型分布

## 第三步：元数据详细分析
使用 `read_excel_metadata` 获取详细元数据：
- 每个工作表的行列统计
- 数据类型分布分析
- 编码格式检测
- 潜在问题识别

**输出要求：**
生成结构化的文件探索报告，包含：
- 文件概览摘要
- 各工作表详细信息
- 数据质量初步评估
- 后续处理建议
```

#### 1.2 多文件批量探索提示词

```markdown
# 批量Excel文件结构分析

对于多个Excel文件的批量分析场景：

## 批量处理策略
使用 `batch_process_excel_files` 工具：
- 并行处理多个文件
- 统一的结构检测标准
- 生成对比分析报告

## 处理流程
1. 文件清单生成和验证
2. 并发结构检测
3. 数据格式标准化评估
4. 异常文件识别和处理建议

**期望输出：**
- 批量文件处理摘要
- 结构一致性分析
- 数据质量对比矩阵
- 标准化处理方案
```

### 🔍 阶段二：数据质量评估与优化

#### 2.1 综合质量检查提示词

```markdown
# Excel数据质量全面评估

执行多层次数据质量检查：

## 基础质量检查
使用 `enhanced_data_quality_check` 进行：
- 缺失值分布分析
- 重复数据检测
- 数据类型一致性验证
- 异常值识别和统计

## 深度质量验证
使用 `comprehensive_data_verification_tool` 执行：
- 数据完整性验证
- 业务逻辑一致性检查
- 跨表关联性验证
- 数据范围合理性分析

## 质量改进建议
使用 `validate_data_quality` 生成：
- 具体的数据清洗建议
- 质量提升优先级排序
- 自动化修复方案
- 人工干预需求评估

**交付成果：**
- 数据质量评估报告
- 问题分类和优先级
- 清洗策略和实施计划
- 质量监控指标建议
```

#### 2.2 数据清洗与标准化提示词

```markdown
# 智能数据清洗与格式标准化

## 自动化清洗流程
使用 `clean_excel_data` 工具：
- 去除重复记录
- 标准化数据格式
- 填充缺失值
- 修正数据类型

## 格式转换优化
使用 `convert_character_formats` 进行：
- 字符编码统一
- 数值格式标准化
- 日期时间格式统一
- 文本内容规范化

## 高级内容提取
使用 `extract_cell_content_advanced` 实现：
- 复杂格式内容解析
- 嵌套数据结构提取
- 格式化内容保留
- 元数据信息提取

**预期结果：**
- 清洗后的标准化数据集
- 数据转换日志
- 质量提升对比报告
- 后续处理优化建议
```

### ⚙️ 阶段三：智能参数优化与模板生成

#### 3.1 读取参数智能推荐提示词

```markdown
# Excel读取参数智能优化

## 参数自动推荐
使用 `suggest_excel_read_parameters_tool` 获取：
- 最优的header行设置
- 数据区域自动识别
- 列名处理策略
- 数据类型推断配置

## 模板代码生成
使用 `create_excel_read_template_tool` 创建：
- 定制化读取代码模板
- 参数配置最佳实践
- 错误处理机制
- 性能优化建议

## 参数验证与调优
- 对比不同参数组合的效果
- 评估读取性能和准确性
- 生成参数调优报告
- 提供最终推荐方案

**输出内容：**
- 优化后的读取参数配置
- 可执行的代码模板
- 参数选择理由说明
- 性能基准测试结果
```

### 📊 阶段四：数据读取与高级处理

#### 4.1 增强数据读取提示词

```markdown
# 高性能Excel数据读取

## 增强读取策略
使用 `excel_read_enhanced` 工具：
- Go excelize引擎优先
- 大文件分块处理
- 内存优化读取
- 并发处理支持

## 性能对比分析
使用 `excel_performance_comparison` 评估：
- Go vs Python引擎性能
- 不同文件大小的处理效率
- 内存使用情况对比
- 最优引擎选择建议

## 多条件数据提取
使用 `extract_multi_condition_data` 实现：
- 复杂筛选条件设置
- 多维度数据切片
- 动态条件组合
- 结果集优化

**期望产出：**
- 高效的数据读取方案
- 性能基准测试报告
- 优化后的数据集
- 处理效率提升建议
```

#### 4.2 多表数据整合提示词

```markdown
# 多表格数据智能合并

## 表格合并策略
使用 `merge_multiple_tables` 工具：
- 自动识别关联字段
- 智能合并策略选择
- 数据一致性保证
- 合并结果验证

## 合并配置优化
- 关联字段匹配规则
- 重复数据处理策略
- 缺失值填充方案
- 数据类型统一处理

## 结果质量验证
- 合并完整性检查
- 数据逻辑一致性验证
- 业务规则符合性检查
- 异常情况处理记录

**交付成果：**
- 整合后的统一数据表
- 合并过程详细日志
- 数据质量验证报告
- 后续优化建议
```

### 🧮 阶段五：公式计算与数据分析

#### 5.1 Excel公式处理提示词

```markdown
# Excel公式智能处理与计算

## 公式解析与验证
使用 `parse_formula` 和 `validate_formula`：
- 公式语法结构分析
- 安全性风险评估
- 依赖关系识别
- 计算复杂度评估

## 工作簿编译优化
使用 `compile_workbook` 工具：
- 公式编译为Python代码
- 依赖关系图生成
- 计算顺序优化
- 性能瓶颈识别

## 公式执行与分析
使用 `execute_formula` 和 `analyze_dependencies`：
- 安全沙箱环境执行
- 循环依赖检测
- 影响分析报告
- 计算结果验证

**预期输出：**
- 公式处理完整报告
- 优化后的计算方案
- 依赖关系可视化图
- 性能提升建议
```

#### 5.2 数据分析代码执行提示词

```markdown
# 安全数据分析代码执行

## Excel数据分析
使用 `run_excel_code` 执行：
- 描述性统计分析
- 相关性分析
- 趋势分析
- 异常值检测

## 分析代码模板
```python
# 数据概览分析
print("=== 数据基本信息 ===")
print(f"数据形状: {df.shape}")
print(f"列名: {list(df.columns)}")
print(f"数据类型:\n{df.dtypes}")

# 描述性统计
print("\n=== 描述性统计 ===")
print(df.describe())

# 缺失值分析
print("\n=== 缺失值分析 ===")
missing_data = df.isnull().sum()
print(missing_data[missing_data > 0])

# 相关性分析
print("\n=== 数值列相关性分析 ===")
numeric_cols = df.select_dtypes(include=[np.number]).columns
if len(numeric_cols) > 1:
    correlation_matrix = df[numeric_cols].corr()
    print(correlation_matrix)
```

**分析维度：**
- 数据分布特征
- 业务指标计算
- 异常模式识别
- 趋势变化分析
```

### 📈 阶段六：数据可视化与报告生成

#### 6.1 交互式图表生成提示词

```markdown
# 专业数据可视化方案

## 柱状图分析展示
使用 `bar_chart_to_html` 创建：
- 分类数据对比分析
- 时间序列趋势展示
- 多维度数据对比
- 交互式数据探索

## 饼图比例分析
使用 `pie_chart_to_html` 生成：
- 构成比例分析
- 市场份额展示
- 分类占比可视化
- 动态数据标签

## 折线图趋势分析
使用 `line_chart_to_html` 制作：
- 时间序列变化趋势
- 多指标对比分析
- 预测趋势展示
- 关键节点标注

## Excel内嵌图表
使用 `excel_chart_enhanced` 创建：
- 原生Excel图表格式
- 多种图表类型支持
- 自定义样式配置
- 数据源动态链接

**可视化策略：**
- 根据数据特征选择图表类型
- 优化视觉设计和用户体验
- 确保图表的可读性和准确性
- 提供交互式数据探索功能
```

#### 6.2 综合报告生成提示词

```markdown
# 数据分析综合报告生成

## 报告结构设计
1. **执行摘要**
   - 关键发现总结
   - 主要指标概览
   - 重要结论提炼

2. **数据质量评估**
   - 数据完整性报告
   - 质量问题识别
   - 改进措施建议

3. **统计分析结果**
   - 描述性统计
   - 相关性分析
   - 趋势分析
   - 异常值分析

4. **可视化展示**
   - 关键指标图表
   - 趋势变化图
   - 对比分析图
   - 分布特征图

5. **结论与建议**
   - 数据洞察总结
   - 业务建议
   - 后续行动计划

## 报告输出格式
- HTML交互式报告
- Excel格式数据表
- PDF打印版本
- 图表文件集合
```

### 🔄 阶段七：结果验证与质量保证

#### 7.1 数据完整性验证提示词

```markdown
# 分析结果验证与质量保证

## 数据完整性验证
使用 `verify_data_integrity` 工具：
- 原始数据与处理结果对比
- 数据变换过程验证
- 计算结果准确性检查
- 业务逻辑一致性验证

## 批量验证处理
使用 `batch_data_verification_tool`：
- 多文件处理结果验证
- 批量质量检查
- 一致性标准验证
- 异常结果识别

## 验证报告生成
- 验证通过率统计
- 问题分类和严重程度
- 修复建议和优先级
- 质量保证认证

**质量标准：**
- 数据准确性 ≥ 99.5%
- 完整性检查通过率 100%
- 业务逻辑一致性验证通过
- 性能指标达到预期
```

### 🎯 高级应用场景提示词

#### 场景1：财务数据分析

```markdown
# 财务Excel数据智能分析

## 分析目标
对财务报表进行全面分析，生成财务健康度评估报告

## 工具组合策略
1. `detect_excel_file_structure_tool` - 识别财务报表结构
2. `enhanced_data_quality_check` - 财务数据质量验证
3. `extract_multi_condition_data` - 按条件提取关键财务指标
4. `run_excel_code` - 执行财务比率计算
5. `bar_chart_to_html` - 生成财务指标对比图
6. `verify_data_integrity` - 验证计算结果准确性

## 分析维度
- 盈利能力分析
- 偿债能力评估
- 运营效率指标
- 成长性分析
- 风险评估指标
```

#### 场景2：销售数据挖掘

```markdown
# 销售业绩数据深度挖掘

## 分析框架
构建销售数据的多维度分析体系

## 工具链设计
1. `batch_process_excel_files` - 批量处理销售数据文件
2. `merge_multiple_tables` - 整合多渠道销售数据
3. `clean_excel_data` - 清洗和标准化销售记录
4. `execute_formula` - 计算销售KPI指标
5. `line_chart_to_html` - 生成销售趋势图
6. `pie_chart_to_html` - 展示市场份额分布

## 洞察维度
- 销售趋势分析
- 产品性能评估
- 客户行为分析
- 渠道效果对比
- 预测模型构建
```

#### 场景3：运营数据监控

```markdown
# 运营数据实时监控分析

## 监控体系
建立运营数据的实时监控和预警机制

## 技术实现
1. `excel_performance_comparison` - 优化数据处理性能
2. `comprehensive_data_verification_tool` - 全面数据质量监控
3. `convert_character_formats` - 标准化数据格式
4. `excel_chart_enhanced` - 生成运营仪表板
5. `validate_data_quality` - 持续质量监控

## 监控指标
- 业务关键指标KPI
- 数据质量健康度
- 系统性能指标
- 异常预警机制
- 趋势预测分析
```

### 📚 最佳实践指南

#### 工具组合原则

1. **渐进式处理**：从简单到复杂，逐步深入分析
2. **质量优先**：每个阶段都要进行质量检查和验证
3. **性能优化**：根据数据规模选择最优的工具和参数
4. **结果验证**：关键计算结果必须进行独立验证
5. **文档记录**：完整记录处理过程和决策依据

#### 错误处理策略

1. **预防性检查**：使用质量检查工具提前发现问题
2. **降级处理**：Go服务不可用时自动切换到Python引擎
3. **异常恢复**：建立数据备份和恢复机制
4. **日志记录**：详细记录处理过程和异常信息

#### 性能优化建议

1. **批量处理**：对于大量文件使用批量处理工具
2. **并发执行**：利用多核处理能力提升效率
3. **缓存机制**：重复计算结果进行缓存
4. **内存管理**：大文件采用分块处理策略

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给我们一个星标！**

[⬆ 回到顶部](#chatexcel-mcp-server)

</div>