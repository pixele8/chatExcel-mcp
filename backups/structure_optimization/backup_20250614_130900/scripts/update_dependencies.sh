#!/bin/bash
# 依赖更新和同步脚本

set -e

echo "🔄 开始依赖更新流程..."

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ 虚拟环境已激活"
else
    echo "❌ 虚拟环境不存在，请先创建虚拟环境"
    exit 1
fi

# 备份当前依赖
echo "📦 备份当前依赖列表..."
pip freeze > requirements_backup_$(date +%Y%m%d_%H%M%S).txt

# 更新pip
echo "⬆️ 更新pip..."
pip install --upgrade pip

# 检查过时的包
echo "🔍 检查过时的包..."
pip list --outdated

# 更新核心依赖
echo "📈 更新核心依赖..."
pip install --upgrade fastmcp pandas chardet openpyxl seaborn matplotlib numpy

# 更新开发依赖
echo "🛠️ 更新开发依赖..."
pip install --upgrade pytest black flake8

# 生成新的requirements.txt
echo "📝 生成新的requirements.txt..."
pip freeze > requirements.txt

# 运行测试确保兼容性
echo "🧪 运行测试确保兼容性..."
pytest tests/ -v

echo "✅ 依赖更新完成！"