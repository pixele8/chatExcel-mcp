# ChatExcel MCP Server 快速开始指南

## 🚀 一分钟快速启动

### 第一步：克隆项目
```bash
git clone <repository-url>
cd chatExcel-mcp
```

### 第二步：一键启动
```bash
# 首次使用，运行部署脚本
./start.sh --deploy

# 启动增强版服务器
./start.sh
```

就这么简单！🎉

## 📋 常用命令

### 启动服务器
```bash
# 启动增强版服务器（推荐）
./start.sh

# 启动标准版服务器
./start.sh --type standard

# 启用调试模式
./start.sh --debug
```

### 管理服务
```bash
# 查看服务状态
./start.sh --status

# 停止所有服务
./start.sh --stop

# 查看帮助
./start.sh --help
```

### 部署和维护
```bash
# 运行部署脚本
./start.sh --deploy

# 或直接运行Python脚本
python scripts/deploy.py
```

## 🔧 高级用法

### Python脚本方式
```bash
# 使用Python启动脚本
python scripts/start_server.py --type enhanced
python scripts/start_server.py --type standard
python scripts/start_server.py --status
python scripts/start_server.py --stop
```

### 直接启动
```bash
# 直接运行服务器文件
python enhanced_server.py  # 增强版
python server.py           # 标准版
```

## 🏥 健康检查

### 检查系统状态
```bash
# 运行健康检查脚本
python scripts/health_check.py

# 查看服务状态
./start.sh --status
```

### 查看日志
```bash
# 查看错误日志
tail -f logs/error/*.log

# 查看访问日志
tail -f logs/access/*.log

# 查看审计日志
tail -f logs/audit/*.log
```

## 🛠️ 故障排除

### 常见问题

#### 1. Python版本问题
```bash
# 检查Python版本（需要3.11+）
python3 --version

# 如果版本不够，请升级Python
```

#### 2. 依赖缺失
```bash
# 重新安装依赖
pip install -r requirements.txt

# 或运行部署脚本
./start.sh --deploy
```

#### 3. 端口被占用
```bash
# 检查端口占用（默认8080）
lsof -i :8080

# 停止占用端口的进程
kill -9 <PID>
```

#### 4. Go服务问题
```bash
# 检查Go是否安装
go version

# 重新构建Go服务
cd excel-service
go mod tidy
go build -o excel_service main.go
```

### 重置环境
```bash
# 停止所有服务
./start.sh --stop

# 清理临时文件
rm -rf temp/* logs/* charts/*

# 重新部署
./start.sh --deploy

# 重新启动
./start.sh
```

## 📊 性能监控

### 系统资源监控
```bash
# 查看CPU和内存使用
top -p $(pgrep -f "enhanced_server.py")

# 查看磁盘使用
df -h

# 查看网络连接
netstat -tulpn | grep :8080
```

### 服务性能
```bash
# 测试MCP工具响应
python test/simple_test.py

# 运行性能测试
python test/performance/benchmark.py
```

## 🔐 安全配置

### 查看安全配置
```bash
# 查看安全配置文件
cat config/security.json

# 查看审计日志
tail -f logs/audit/audit.log
```

### 更新安全设置
```bash
# 编辑安全配置
vim config/security.json

# 重启服务以应用更改
./start.sh --stop
./start.sh
```

## 📚 更多资源

- **详细文档**: [README.md](README.md)
- **增强功能指南**: [ENHANCED_USAGE_GUIDE.md](ENHANCED_USAGE_GUIDE.md)
- **更新日志**: [CHANGELOG.md](CHANGELOG.md)
- **问题记录**: [record.md](record.md)

## 💡 提示

1. **首次使用**：建议先运行 `./start.sh --deploy` 进行完整部署
2. **开发环境**：使用 `./start.sh --debug` 启用调试模式
3. **生产环境**：使用 `./start.sh --type enhanced` 启动增强版
4. **监控服务**：定期运行 `./start.sh --status` 检查服务状态
5. **日志管理**：定期清理 `logs/` 目录下的旧日志文件

## 🆘 获取帮助

如果遇到问题，请：

1. 查看 `./start.sh --help` 获取命令帮助
2. 检查 `logs/error/` 目录下的错误日志
3. 运行 `python scripts/health_check.py` 进行系统诊断
4. 查看 [故障排除](#🛠️-故障排除) 部分
5. 提交Issue到项目仓库

---

**祝您使用愉快！** 🎉