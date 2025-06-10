#!/bin/bash

# ChatExcel MCP服务器启动脚本
# 自动检测项目路径和虚拟环境

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"

# 检查虚拟环境
VENV_DIR="$PROJECT_DIR/venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "错误: 虚拟环境不存在于 $VENV_DIR"
    echo "请先创建虚拟环境: python3.11 -m venv venv"
    exit 1
fi

# 检查server.py文件
SERVER_FILE="$PROJECT_DIR/server.py"
if [ ! -f "$SERVER_FILE" ]; then
    echo "错误: server.py文件不存在于 $SERVER_FILE"
    exit 1
fi

# 激活虚拟环境
source "$VENV_DIR/bin/activate"

# 检查Python版本
PYTHON_VERSION=$(python --version 2>&1)
echo "使用Python版本: $PYTHON_VERSION"

# 检查必要的包
echo "检查MCP包..."
if ! python -c "import mcp" 2>/dev/null; then
    echo "警告: MCP包未安装，正在安装..."
    pip install mcp
fi

# 设置环境变量
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"
export MCP_SERVER_ROOT="$PROJECT_DIR"

# 启动服务器
echo "启动ChatExcel MCP服务器..."
echo "项目目录: $PROJECT_DIR"
echo "虚拟环境: $VENV_DIR"
echo "服务器文件: $SERVER_FILE"
echo "----------------------------------------"

cd "$PROJECT_DIR"
python "$SERVER_FILE" "$@"