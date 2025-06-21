# 更新日志 (CHANGELOG)

## [2.1.1] - 2025-06-19

### 🔧 修复 (Fixed)
- **pandas导入问题完全修复**: 解决了MCP服务器中pandas导入失败的问题
  - 增强了`fallback_enhanced_run_excel_code`函数的执行环境
  - 添加了多种pandas和numpy引用方式支持 (`pd`, `pandas`, `np`, `numpy`)
  - 完善了内置函数和常用模块的导入
  - 改进了错误处理和返回格式

### 🆕 新增 (Added)
- **enhanced_globals_config.py**: 增强的全局配置模块
- **pandas_fix_patch.py**: pandas导入修复补丁
- **mcp_pandas_integration.py**: MCP服务器集成修复模块
- **test_pandas_fix.py**: pandas修复验证测试脚本
- **test_final_fix.py**: 最终修复验证测试脚本

### 🔄 更新 (Changed)
- 版本号从 v2.1.0 升级到 v2.1.1
- 更新了项目描述，标注为"pandas导入修复版"
- 增加了新的关键词: `pandas-fix`, `import-fix`, `execution-environment`
- 更新了README.md中的工具特性说明
- 更新了requirements.txt中的版本信息和修复状态

### ✅ 测试 (Testing)
- 所有pandas相关功能测试通过
- 基本数据查看、pandas函数调用、numpy函数调用测试通过
- 数据分析和复杂操作测试通过
- MCP服务器集成测试通过

### 📋 技术细节
- **执行环境增强**: 使用`safe_globals`替代`local_vars`
- **多重引用支持**: 支持`pd`, `pandas`, `np`, `numpy`等多种引用方式
- **内置函数完善**: 添加了`len`, `sum`, `max`, `min`, `abs`, `round`等常用函数
- **模块导入优化**: 预导入了`math`, `datetime`, `json`等常用模块
- **错误处理改进**: 更详细的错误信息和调试支持

---

## [2.1.0] - 2025-06-18

### 🆕 主要功能
- tabulate库集成完成，解决ImportError问题
- NumPy和Pandas功能完备性验证通过
- 增强多级列头检测系统已修复并正常运行
- 新增Excel公式处理引擎 (formulas==1.2.10)
- 新增7个数据质量控制工具，完善企业级功能
- 新增安全机制、健康监控、依赖管理等企业级功能
- 虚拟环境兼容性和依赖检查机制完善

### 🛠️ 技术改进
- 31个专业MCP工具覆盖完整数据处理流程
- 双引擎架构 (Python + Go)
- 企业级安全和性能优化
- 完整的健康监控和错误追踪

---

## 版本说明

- **主版本号**: 重大架构变更或不兼容更新
- **次版本号**: 新功能添加或重要改进
- **修订版本号**: Bug修复和小幅改进

## 贡献指南

如果您发现问题或有改进建议，请：
1. 查看现有的Issues
2. 创建新的Issue描述问题
3. 提交Pull Request

## 支持

- 📧 邮箱: support@chatexcel.com
- 📖 文档: README.md
- 🐛 问题反馈: GitHub Issues