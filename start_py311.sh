#!/bin/bash
# Python 3.11 项目启动脚本

echo "🚀 启动 chatExcel (Python 3.11)"
echo "======================================"

# 激活Python 3.11虚拟环境（使用根目录的venv）
source ../venv/bin/activate

# 显示Python版本
echo "📍 当前Python版本: $(python --version)"

# 运行健康检查
echo "🏥 运行健康检查..."
python scripts/health_check.py

echo ""
echo "✅ 项目已准备就绪！"
echo "💡 使用以下命令启动服务器:"
echo "   python server.py"
echo ""
echo "🔧 或运行其他功能:"
echo "   python test_metadata_functions.py  # 测试元数据功能"
echo "   python test_charts.py             # 测试图表功能"
