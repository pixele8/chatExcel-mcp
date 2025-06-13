#!/bin/bash

# ChatExcel MCP Server 快速启动脚本
# 企业级增强版服务器启动工具

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 打印带颜色的消息
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# 打印标题
print_header() {
    echo -e "${CYAN}${BOLD}============================================================${NC}"
    echo -e "${CYAN}${BOLD}    ChatExcel MCP Server - 企业级增强版${NC}"
    echo -e "${CYAN}${BOLD}    快速启动脚本${NC}"
    echo -e "${CYAN}${BOLD}============================================================${NC}"
    echo
}

# 显示使用帮助
show_help() {
    print_header
    echo -e "${BLUE}使用方法:${NC}"
    echo "  $0 [选项]"
    echo
    echo -e "${BLUE}选项:${NC}"
    echo "  -h, --help          显示此帮助信息"
    echo "  -t, --type TYPE     服务器类型 (enhanced|standard，默认: enhanced)"
    echo "  -d, --deploy        运行部署脚本"
    echo "  -s, --status        显示服务状态"
    echo "  --stop              停止所有服务"
    echo "  --debug             启用调试模式"
    echo
    echo -e "${BLUE}示例:${NC}"
    echo "  $0                  # 启动增强版服务器"
    echo "  $0 -t standard      # 启动标准版服务器"
    echo "  $0 -d               # 运行部署脚本"
    echo "  $0 -s               # 显示服务状态"
    echo "  $0 --stop           # 停止所有服务"
    echo
}

# 检查Python环境
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_message "$RED" "❌ Python3 未安装或不在PATH中"
        exit 1
    fi
    
    local python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
    local major_version=$(echo $python_version | cut -d'.' -f1)
    local minor_version=$(echo $python_version | cut -d'.' -f2)
    
    if [[ $major_version -lt 3 ]] || [[ $major_version -eq 3 && $minor_version -lt 11 ]]; then
        print_message "$RED" "❌ 需要Python 3.11+，当前版本: $python_version"
        exit 1
    fi
    
    print_message "$GREEN" "✅ Python版本检查通过: $python_version"
}

# 检查项目文件
check_project_files() {
    local required_files=("enhanced_server.py" "server.py" "requirements.txt")
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$PROJECT_ROOT/$file" ]]; then
            print_message "$RED" "❌ 缺少必要文件: $file"
            exit 1
        fi
    done
    
    print_message "$GREEN" "✅ 项目文件检查通过"
}

# 运行部署脚本
run_deploy() {
    print_message "$YELLOW" "🚀 运行部署脚本..."
    
    if [[ -f "$PROJECT_ROOT/scripts/deploy.py" ]]; then
        cd "$PROJECT_ROOT"
        python3 scripts/deploy.py
    else
        print_message "$RED" "❌ 部署脚本不存在: scripts/deploy.py"
        exit 1
    fi
}

# 启动服务器
start_server() {
    local server_type=${1:-"enhanced"}
    local debug_mode=${2:-false}
    
    print_message "$YELLOW" "🚀 启动 $server_type 版本服务器..."
    
    local args=("--type" "$server_type")
    
    if [[ "$debug_mode" == "true" ]]; then
        args+=("--debug")
    fi
    
    if [[ -f "$PROJECT_ROOT/scripts/start_server.py" ]]; then
        cd "$PROJECT_ROOT"
        python3 scripts/start_server.py "${args[@]}"
    else
        print_message "$RED" "❌ 启动脚本不存在: scripts/start_server.py"
        exit 1
    fi
}

# 显示服务状态
show_status() {
    if [[ -f "$PROJECT_ROOT/scripts/start_server.py" ]]; then
        cd "$PROJECT_ROOT"
        python3 scripts/start_server.py --status
    else
        print_message "$RED" "❌ 启动脚本不存在: scripts/start_server.py"
        exit 1
    fi
}

# 停止服务
stop_services() {
    if [[ -f "$PROJECT_ROOT/scripts/start_server.py" ]]; then
        cd "$PROJECT_ROOT"
        python3 scripts/start_server.py --stop
    else
        print_message "$RED" "❌ 启动脚本不存在: scripts/start_server.py"
        exit 1
    fi
}

# 主函数
main() {
    local server_type="enhanced"
    local run_deploy=false
    local show_status_only=false
    local stop_services_only=false
    local debug_mode=false
    
    # 解析命令行参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -t|--type)
                server_type="$2"
                shift 2
                ;;
            -d|--deploy)
                run_deploy=true
                shift
                ;;
            -s|--status)
                show_status_only=true
                shift
                ;;
            --stop)
                stop_services_only=true
                shift
                ;;
            --debug)
                debug_mode=true
                shift
                ;;
            *)
                print_message "$RED" "❌ 未知选项: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 验证服务器类型
    if [[ "$server_type" != "enhanced" && "$server_type" != "standard" ]]; then
        print_message "$RED" "❌ 无效的服务器类型: $server_type (支持: enhanced, standard)"
        exit 1
    fi
    
    # 执行相应操作
    if [[ "$stop_services_only" == "true" ]]; then
        stop_services
    elif [[ "$show_status_only" == "true" ]]; then
        show_status
    elif [[ "$run_deploy" == "true" ]]; then
        check_python
        check_project_files
        run_deploy
    else
        print_header
        check_python
        check_project_files
        start_server "$server_type" "$debug_mode"
    fi
}

# 捕获中断信号
trap 'print_message "$YELLOW" "\n🛑 脚本被中断"; exit 1' INT TERM

# 运行主函数
main "$@"