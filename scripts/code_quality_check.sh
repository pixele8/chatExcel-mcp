#!/bin/bash
# 代码质量检查脚本

set -e

echo "🔍 开始代码质量检查..."

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ 虚拟环境不存在"
    exit 1
fi

# 代码格式化检查
echo "🎨 检查代码格式..."
black --check --diff .
if [ $? -ne 0 ]; then
    echo "⚠️ 代码格式需要修复，运行: black ."
fi

# 代码风格检查
echo "📏 检查代码风格..."
flake8 --max-line-length=88 --extend-ignore=E203,W503 .

# 运行测试
echo "🧪 运行测试套件..."
pytest tests/ -v --cov=. --cov-report=html --cov-report=term

# 检查安全漏洞
echo "🔒 检查安全漏洞..."
pip install --upgrade safety
safety check

echo "✅ 代码质量检查完成！"