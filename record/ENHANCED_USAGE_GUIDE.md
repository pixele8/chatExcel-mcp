# ChatExcel MCP 增强版使用指南

## 概述

本指南介绍 ChatExcel MCP 增强版的新功能，包括安全机制、服务依赖管理和健康监控等改进。增强版在保持原有功能的基础上，大幅提升了系统的安全性、可靠性和可维护性。

## 🚀 快速开始

### 1. 自动部署

使用自动部署脚本快速设置增强版服务器：

```bash
# 基本部署
python3 deploy_enhanced.py

# 详细输出
python3 deploy_enhanced.py --verbose

# 升级现有依赖
python3 deploy_enhanced.py --upgrade-deps

# 跳过测试（快速部署）
python3 deploy_enhanced.py --skip-tests
```

### 2. 手动启动

```bash
# 使用增强版服务器
python3 enhanced_server.py

# 或使用启动脚本
./start_server.sh  # Unix/Linux/macOS
start_server.bat   # Windows
```

### 3. 验证部署

```bash
# 运行测试套件
python3 test_enhanced_features.py

# 检查服务健康状态
curl http://localhost:8080/health
```

## 🔒 安全功能

### 安全代码执行

增强版提供了安全的代码执行环境，防止恶意代码执行：

#### 支持的安全特性：

- **代码黑名单检查**：阻止危险函数调用
- **AST 语法分析**：深度分析代码结构
- **资源限制**：内存和 CPU 使用限制
- **执行超时**：防止无限循环
- **沙箱环境**：隔离代码执行

#### 使用示例：

```python
from security.secure_code_executor import SecureCodeExecutor

executor = SecureCodeExecutor()

# 安全的代码执行
safe_code = """
import pandas as pd
data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
df = pd.DataFrame(data)
result = df.sum()
"""

result = executor.execute_code(safe_code, {})
if result['success']:
    print("执行成功:", result['result'])
else:
    print("执行失败:", result['error'])
```

#### 被阻止的危险操作：

- 文件系统操作：`open()`, `os.system()`, `subprocess`
- 代码执行：`exec()`, `eval()`, `compile()`
- 网络操作：`socket`, `urllib`, `requests`
- 系统调用：`__import__()`, `getattr()`, `setattr()`

### API 安全

#### 认证和授权：

```python
# 配置 API 密钥
API_KEYS = {
    "admin": "your-admin-key",
    "user": "your-user-key"
}

# 请求头中包含认证信息
headers = {
    "Authorization": "Bearer your-api-key",
    "Content-Type": "application/json"
}
```

#### 速率限制：

- 每个 IP 每分钟最多 60 次请求
- 每个 API 密钥每小时最多 1000 次请求
- 超出限制将返回 429 状态码

## 🏥 健康监控

### 服务健康管理

增强版提供了完整的服务健康监控和自动恢复功能：

#### 使用健康管理器：

```python
from service_management.health_manager import HealthManager

health_manager = HealthManager()

# 注册服务
service_config = {
    'name': 'excel_service',
    'host': 'localhost',
    'port': 8081,
    'health_check': {
        'endpoint': '/health',
        'interval': 30,  # 30秒检查一次
        'timeout': 5,    # 5秒超时
        'retries': 3     # 失败重试3次
    },
    'auto_recovery': {
        'enabled': True,
        'max_attempts': 3,
        'restart_command': ['./restart_service.sh']
    }
}

health_manager.register_service('excel_service', service_config)

# 启动监控
health_manager.start_monitoring()
```

#### 健康检查端点：

```bash
# 检查主服务健康状态
curl http://localhost:8080/health

# 检查特定服务状态
curl http://localhost:8080/health/excel_service

# 获取详细健康报告
curl http://localhost:8080/health/detailed
```

#### 响应格式：

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "services": {
    "excel_service": {
      "status": "healthy",
      "last_check": "2024-01-15T10:29:45Z",
      "response_time": 0.05,
      "uptime": 3600
    }
  },
  "system": {
    "cpu_usage": 15.2,
    "memory_usage": 45.8,
    "disk_usage": 67.3
  }
}
```

### 自动恢复

当服务出现故障时，系统会自动尝试恢复：

1. **检测故障**：健康检查失败
2. **记录日志**：记录故障详情
3. **尝试恢复**：执行恢复命令
4. **验证恢复**：检查服务是否恢复正常
5. **通知管理员**：发送故障和恢复通知

## 📦 依赖管理

### 智能依赖分析

增强版提供了强大的依赖管理功能：

#### 使用依赖管理器：

```python
from service_management.dependency_manager import DependencyManager

dep_manager = DependencyManager()

# 解析依赖文件
dependencies = dep_manager.parse_requirements_file('requirements.txt')

# 检测冲突
conflicts = dep_manager.detect_conflicts(dependencies)
if conflicts:
    print("发现依赖冲突:")
    for conflict in conflicts:
        print(f"  {conflict['package']}: {conflict['description']}")

# 构建依赖图
graph = dep_manager.build_dependency_graph(dependencies)

# 安全扫描
vulnerabilities = dep_manager.scan_vulnerabilities()
if vulnerabilities:
    print("发现安全漏洞:")
    for vuln in vulnerabilities:
        print(f"  {vuln['package']}: {vuln['advisory']}")
```

#### 依赖分析报告：

```bash
# 生成依赖分析报告
python3 -c "from service_management.dependency_manager import DependencyManager; DependencyManager().generate_analysis_report()"
```

报告包含：
- 依赖列表和版本信息
- 冲突检测结果
- 安全漏洞扫描
- 更新建议
- 依赖关系图

### 自动更新

```python
# 更新所有依赖到最新版本
dep_manager.update_dependencies()

# 更新特定包
dep_manager.update_package('pandas', '2.0.0')

# 安全更新（仅更新有漏洞的包）
dep_manager.security_update()
```

## ⚙️ 配置管理

### 集中配置管理

增强版提供了统一的配置管理系统：

#### 配置文件结构：

```
config/
├── system.json          # 系统配置
├── security.json        # 安全配置
├── runtime.yaml         # 运行时配置
├── logging.json         # 日志配置
└── deployment.json      # 部署配置
```

#### 使用配置管理器：

```python
from service_management.config_manager import ConfigManager

config_manager = ConfigManager('config/')

# 获取配置值
host = config_manager.get('server.host', 'localhost')
port = config_manager.get('server.port', 8080)
debug = config_manager.get('server.debug', False)

# 设置配置值
config_manager.set('server.max_workers', 4)

# 监听配置变化
def on_config_change(key, old_value, new_value):
    print(f"配置 {key} 从 {old_value} 变更为 {new_value}")

config_manager.watch('server.debug', on_config_change)
```

#### 配置验证：

```python
# 定义配置模式
schema = {
    "type": "object",
    "properties": {
        "host": {"type": "string"},
        "port": {"type": "integer", "minimum": 1, "maximum": 65535}
    },
    "required": ["host", "port"]
}

# 验证配置
config = {"host": "localhost", "port": 8080}
is_valid, errors = config_manager.validate_config(config, schema)
```

### 环境特定配置

支持不同环境的配置：

```bash
# 开发环境
export CHATEXCEL_ENV=development
python3 enhanced_server.py

# 生产环境
export CHATEXCEL_ENV=production
python3 enhanced_server.py

# 测试环境
export CHATEXCEL_ENV=testing
python3 enhanced_server.py
```

## 📊 监控和日志

### 日志系统

增强版提供了结构化的日志系统：

#### 日志级别：

- **DEBUG**：详细调试信息
- **INFO**：一般信息
- **WARNING**：警告信息
- **ERROR**：错误信息
- **CRITICAL**：严重错误

#### 日志文件：

```
logs/
├── app.log              # 应用日志
├── error/
│   └── error.log        # 错误日志
├── audit/
│   └── audit.log        # 审计日志
└── access/
    └── access.log       # 访问日志
```

#### 日志配置：

```python
import logging
from service_management.config_manager import ConfigManager

# 加载日志配置
config_manager = ConfigManager('config/')
logging_config = config_manager.get_config('logging')

# 配置日志
logging.config.dictConfig(logging_config)

# 使用日志
logger = logging.getLogger(__name__)
logger.info("服务启动")
logger.error("发生错误", exc_info=True)
```

### 性能监控

#### 系统指标：

```python
from service_management.health_manager import HealthManager

health_manager = HealthManager()
metrics = health_manager.get_system_metrics()

print(f"CPU 使用率: {metrics['cpu_percent']}%")
print(f"内存使用率: {metrics['memory_percent']}%")
print(f"磁盘使用率: {metrics['disk_percent']}%")
```

#### 应用指标：

- 请求处理时间
- 错误率
- 并发连接数
- 代码执行次数
- 文件处理量

## 🧪 测试

### 运行测试

```bash
# 运行完整测试套件
python3 test_enhanced_features.py

# 运行特定测试类
python3 -m unittest test_enhanced_features.TestSecureCodeExecutor

# 运行性能测试
python3 -c "from test_enhanced_features import run_performance_tests; run_performance_tests()"

# 运行压力测试
python3 -c "from test_enhanced_features import run_stress_tests; run_stress_tests()"
```

### 测试覆盖率

```bash
# 安装覆盖率工具
pip install coverage

# 运行覆盖率测试
coverage run test_enhanced_features.py
coverage report
coverage html  # 生成 HTML 报告
```

## 🔧 故障排除

### 常见问题

#### 1. 服务启动失败

**症状**：服务无法启动，出现端口占用错误

**解决方案**：
```bash
# 检查端口占用
lsof -i :8080

# 杀死占用进程
kill -9 <PID>

# 或更改端口
export CHATEXCEL_PORT=8081
python3 enhanced_server.py
```

#### 2. Go 服务构建失败

**症状**：部署时 Go 服务构建失败

**解决方案**：
```bash
# 检查 Go 版本
go version

# 更新 Go 模块
go mod tidy

# 手动构建
go build -o excel_service main.go
```

#### 3. 依赖冲突

**症状**：包安装失败或运行时导入错误

**解决方案**：
```bash
# 创建新的虚拟环境
python3 -m venv venv_new
source venv_new/bin/activate

# 重新安装依赖
pip install -r requirements.txt

# 或使用依赖管理器解决冲突
python3 -c "from service_management.dependency_manager import DependencyManager; DependencyManager().resolve_conflicts()"
```

#### 4. 内存不足

**症状**：处理大文件时内存不足

**解决方案**：
```yaml
# 在 runtime.yaml 中调整资源限制
resource_limits:
  memory_limit_mb: 2048  # 增加内存限制
  max_file_size_mb: 100  # 减少文件大小限制

processing:
  chunk_size: 1000       # 减少块大小
  use_streaming: true    # 启用流式处理
```

### 日志分析

#### 查看错误日志：

```bash
# 查看最新错误
tail -f logs/error/error.log

# 搜索特定错误
grep -i "error" logs/app.log

# 分析访问模式
awk '{print $1}' logs/access/access.log | sort | uniq -c | sort -nr
```

#### 性能分析：

```bash
# 分析响应时间
grep "response_time" logs/app.log | awk '{print $NF}' | sort -n

# 查看慢查询
grep "slow" logs/app.log
```

## 🚀 性能优化

### 系统优化

#### 1. 内存优化

```python
# 启用内存优化
config = {
    'memory_optimization': {
        'enable_gc': True,
        'gc_threshold': 1000,
        'use_memory_mapping': True
    }
}
```

#### 2. 并发优化

```python
# 调整工作进程数
config = {
    'server': {
        'workers': 4,  # CPU 核心数
        'max_connections': 1000,
        'connection_timeout': 30
    }
}
```

#### 3. 缓存优化

```python
# 启用缓存
config = {
    'cache': {
        'enabled': True,
        'type': 'memory',  # 或 'redis'
        'ttl': 3600,       # 1小时
        'max_size': 1000   # 最大条目数
    }
}
```

### 数据库优化

```python
# 连接池配置
config = {
    'database': {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30,
        'pool_recycle': 3600
    }
}
```

## 📈 扩展和定制

### 添加新的安全检查

```python
# 扩展安全检查器
from security.secure_code_executor import SecureCodeExecutor

class CustomSecureExecutor(SecureCodeExecutor):
    def __init__(self):
        super().__init__()
        # 添加自定义黑名单
        self.blacklist.extend([
            'custom_dangerous_function',
            'another_risky_operation'
        ])
    
    def custom_security_check(self, code):
        # 实现自定义安全检查
        if 'dangerous_pattern' in code:
            return False, "检测到危险模式"
        return True, None
```

### 添加新的健康检查

```python
# 扩展健康检查
from service_management.health_manager import HealthManager

class CustomHealthManager(HealthManager):
    async def custom_health_check(self, service_name):
        # 实现自定义健康检查逻辑
        try:
            # 执行特定的健康检查
            result = await self.perform_custom_check(service_name)
            return {
                'healthy': result['status'] == 'ok',
                'details': result
            }
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e)
            }
```

### 添加新的配置源

```python
# 扩展配置管理器
from service_management.config_manager import ConfigManager

class DatabaseConfigManager(ConfigManager):
    def __init__(self, config_dir, db_connection):
        super().__init__(config_dir)
        self.db = db_connection
    
    def load_from_database(self):
        # 从数据库加载配置
        configs = self.db.execute("SELECT key, value FROM configs")
        for key, value in configs:
            self.set(key, value)
```

## 📚 API 参考

### 安全 API

#### SecureCodeExecutor

```python
class SecureCodeExecutor:
    def execute_code(self, code: str, context: dict) -> dict:
        """安全执行代码"""
        pass
    
    def validate_code(self, code: str) -> tuple[bool, str]:
        """验证代码安全性"""
        pass
    
    def set_resource_limits(self, memory_mb: int, timeout_sec: int):
        """设置资源限制"""
        pass
```

### 健康管理 API

#### HealthManager

```python
class HealthManager:
    def register_service(self, name: str, config: dict):
        """注册服务"""
        pass
    
    async def check_service_health(self, name: str) -> dict:
        """检查服务健康状态"""
        pass
    
    def start_monitoring(self):
        """启动监控"""
        pass
    
    def get_system_metrics(self) -> dict:
        """获取系统指标"""
        pass
```

### 配置管理 API

#### ConfigManager

```python
class ConfigManager:
    def get(self, key: str, default=None):
        """获取配置值"""
        pass
    
    def set(self, key: str, value):
        """设置配置值"""
        pass
    
    def watch(self, key: str, callback):
        """监听配置变化"""
        pass
    
    def validate_config(self, config: dict, schema: dict) -> tuple[bool, list]:
        """验证配置"""
        pass
```

## 🤝 贡献指南

### 开发环境设置

```bash
# 克隆仓库
git clone <repository-url>
cd chatExcel-mcp

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装开发依赖
pip install -r requirements-dev.txt

# 安装预提交钩子
pre-commit install
```

### 代码规范

- 使用 Black 进行代码格式化
- 使用 Pylint 进行代码检查
- 遵循 PEP 8 编码规范
- 编写单元测试
- 更新文档

### 提交流程

1. 创建功能分支
2. 编写代码和测试
3. 运行测试套件
4. 提交代码
5. 创建 Pull Request

## 📞 支持

### 获取帮助

- 查看日志文件：`logs/app.log`
- 运行诊断：`python3 -c "from enhanced_server import diagnose; diagnose()"`
- 检查配置：`python3 -c "from service_management.config_manager import ConfigManager; ConfigManager('config/').validate_all()"`

### 报告问题

请在报告问题时包含：

1. 错误信息和堆栈跟踪
2. 系统信息（操作系统、Python 版本）
3. 配置文件内容
4. 重现步骤
5. 相关日志

---

## 更新日志

### v2.0.0 (增强版)

#### 新功能
- ✅ 安全代码执行环境
- ✅ 服务健康监控和自动恢复
- ✅ 智能依赖管理
- ✅ 集中配置管理
- ✅ 结构化日志系统
- ✅ 性能监控
- ✅ 自动部署脚本
- ✅ 完整测试套件

#### 改进
- 🔧 提升系统安全性
- 🔧 增强错误处理
- 🔧 优化性能
- 🔧 改进用户体验
- 🔧 完善文档

#### 修复
- 🐛 修复内存泄漏问题
- 🐛 修复并发安全问题
- 🐛 修复配置加载问题
- 🐛 修复日志轮转问题

---

*本指南持续更新中，如有疑问请查看最新版本或联系开发团队。*