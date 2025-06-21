# ChatExcel MCP 项目 Makefile
# 简化常用开发任务的执行

.PHONY: help install dev-install clean test test-cov lint format type-check security quality pre-commit docs build release health-check

# 默认目标
help:
	@echo "ChatExcel MCP 项目开发工具"
	@echo ""
	@echo "可用命令:"
	@echo "  install        - 安装生产依赖"
	@echo "  dev-install    - 安装开发依赖"
	@echo "  clean          - 清理临时文件和缓存"
	@echo "  test           - 运行单元测试"
	@echo "  test-cov       - 运行测试并生成覆盖率报告"
	@echo "  lint           - 运行代码风格检查"
	@echo "  format         - 格式化代码"
	@echo "  type-check     - 运行类型检查"
	@echo "  security       - 运行安全检查"
	@echo "  quality        - 运行完整的代码质量检查"
	@echo "  pre-commit     - 安装并运行 pre-commit 钩子"
	@echo "  docs           - 生成文档"
	@echo "  build          - 构建包"
	@echo "  release        - 发布新版本"
	@echo "  health-check   - 运行健康检查"
	@echo "  server         - 启动 MCP 服务器"
	@echo ""

# 安装依赖
install:
	@echo "📦 安装生产依赖..."
	pip install -r requirements.txt

dev-install:
	@echo "🔧 安装开发依赖..."
	pip install -r requirements.txt
	pip install pytest pytest-cov pytest-xdist black isort flake8 mypy bandit safety pre-commit
	pip install sphinx sphinx-rtd-theme myst-parser

# 清理
clean:
	@echo "🧹 清理临时文件和缓存..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/
	rm -rf reports/ *.log

# 测试
test:
	@echo "🧪 运行单元测试..."
	pytest tests/ -v

test-cov:
	@echo "📊 运行测试并生成覆盖率报告..."
	pytest tests/ --cov=. --cov-report=html --cov-report=term-missing --cov-report=xml -v
	@echo "📈 覆盖率报告已生成: htmlcov/index.html"

# 代码质量
lint:
	@echo "🔍 运行代码风格检查..."
	flake8 . --max-line-length=88 --extend-ignore=E203,W503 --exclude=.venv,build,dist

format:
	@echo "✨ 格式化代码..."
	black . --line-length=88
	isort . --profile=black --line-length=88

type-check:
	@echo "🔎 运行类型检查..."
	mypy . --config-file=mypy.ini

security:
	@echo "🔒 运行安全检查..."
	bandit -r . -f txt
	safety check
	pip-audit

quality:
	@echo "🎯 运行完整的代码质量检查..."
	python scripts/code_quality_enhanced.py --report

# Pre-commit
pre-commit:
	@echo "🪝 安装并运行 pre-commit 钩子..."
	python scripts/code_quality_enhanced.py --install-hooks
	python scripts/code_quality_enhanced.py --run-hooks

# 文档
docs:
	@echo "📚 生成文档..."
	@if [ -d "docs" ]; then \
		cd docs && make html; \
		echo "📖 文档已生成: docs/_build/html/index.html"; \
	else \
		echo "⚠️ docs 目录不存在，跳过文档生成"; \
	fi

# 构建和发布
build:
	@echo "🏗️ 构建包..."
	python -m build
	twine check dist/*

release: clean test-cov quality build
	@echo "🚀 准备发布..."
	@echo "请确认版本号并运行: twine upload dist/*"

# 健康检查
health-check:
	@echo "💊 运行健康检查..."
	python scripts/health_check.py

# 启动服务
server:
	@echo "🚀 启动 MCP 服务器..."
	python server.py

# 开发环境设置
setup-dev: dev-install pre-commit
	@echo "✅ 开发环境设置完成！"
	@echo ""
	@echo "下一步:"
	@echo "  1. 运行 'make test' 确保测试通过"
	@echo "  2. 运行 'make quality' 检查代码质量"
	@echo "  3. 运行 'make server' 启动服务"

# 快速检查（提交前）
check: format lint type-check test
	@echo "✅ 快速检查完成！代码已准备好提交。"

# 完整检查
full-check: clean format lint type-check security test-cov quality
	@echo "✅ 完整检查完成！"

# CI 模拟
ci: full-check health-check
	@echo "✅ CI 模拟完成！"

# 性能测试
perf:
	@echo "⚡ 运行性能测试..."
	pytest tests/ -k "benchmark" --benchmark-only || echo "⚠️ 没有找到性能测试"

# 依赖更新检查
dep-check:
	@echo "🔍 检查依赖更新..."
	pip list --outdated
	safety check
	pip-audit

# 项目统计
stats:
	@echo "📊 项目统计信息:"
	@echo "代码行数:"
	@find . -name "*.py" -not -path "./.venv/*" -not -path "./build/*" -not -path "./dist/*" | xargs wc -l | tail -1
	@echo ""
	@echo "文件数量:"
	@find . -name "*.py" -not -path "./.venv/*" -not -path "./build/*" -not -path "./dist/*" | wc -l
	@echo ""
	@echo "测试覆盖率:"
	@pytest tests/ --cov=. --cov-report=term-missing -q 2>/dev/null | grep "TOTAL" || echo "运行 'make test-cov' 获取详细覆盖率"

# 环境信息
env-info:
	@echo "🔧 环境信息:"
	@echo "Python 版本: $$(python --version)"
	@echo "Pip 版本: $$(pip --version)"
	@echo "工作目录: $$(pwd)"
	@echo "虚拟环境: $${VIRTUAL_ENV:-未激活}"
	@echo ""
	@echo "已安装的关键包:"
	@pip list | grep -E "(pytest|black|flake8|mypy|bandit)" || echo "开发依赖未安装"

# 快速启动指南
quickstart:
	@echo "🚀 ChatExcel MCP 快速启动指南"
	@echo ""
	@echo "1. 设置开发环境:"
	@echo "   make setup-dev"
	@echo ""
	@echo "2. 运行测试:"
	@echo "   make test"
	@echo ""
	@echo "3. 检查代码质量:"
	@echo "   make quality"
	@echo ""
	@echo "4. 启动服务:"
	@echo "   make server"
	@echo ""
	@echo "5. 提交前检查:"
	@echo "   make check"
	@echo ""
	@echo "更多命令请运行: make help"