#!/bin/bash

# ChatExcel MCP 项目维护定时任务设置脚本
# 此脚本帮助用户设置自动化的项目维护任务

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}🔧 ChatExcel MCP 项目维护定时任务设置${NC}"
echo -e "${BLUE}📁 项目路径: $PROJECT_ROOT${NC}"
echo "================================================"

# 检查 Python 环境
check_python() {
    echo -e "${YELLOW}🐍 检查 Python 环境...${NC}"
    
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python3 未安装${NC}"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    echo -e "${GREEN}✅ Python 版本: $PYTHON_VERSION${NC}"
    
    # 检查虚拟环境
    if [ -d "$PROJECT_ROOT/venv" ]; then
        echo -e "${GREEN}✅ 发现虚拟环境: $PROJECT_ROOT/venv${NC}"
        PYTHON_CMD="$PROJECT_ROOT/venv/bin/python3"
    else
        echo -e "${YELLOW}⚠️ 未发现虚拟环境，使用系统 Python${NC}"
        PYTHON_CMD="python3"
    fi
}

# 检查脚本文件
check_scripts() {
    echo -e "${YELLOW}📋 检查增强脚本...${NC}"
    
    local scripts=(
        "quick_enhancement.py"
        "dependency_audit.py"
        "security_enhancer.py"
        "structure_optimizer.py"
        "enhanced_monitor.py"
        "automation_suite.py"
    )
    
    for script in "${scripts[@]}"; do
        if [ -f "$SCRIPT_DIR/$script" ]; then
            echo -e "${GREEN}✅ $script${NC}"
        else
            echo -e "${RED}❌ $script 不存在${NC}"
        fi
    done
}

# 生成 crontab 条目
generate_crontab() {
    echo -e "${YELLOW}⏰ 生成定时任务配置...${NC}"
    
    local crontab_file="$SCRIPT_DIR/maintenance_crontab.txt"
    
    cat > "$crontab_file" << EOF
# ChatExcel MCP 项目自动维护定时任务
# 生成时间: $(date)
# 项目路径: $PROJECT_ROOT

# 设置环境变量
PATH=/usr/local/bin:/usr/bin:/bin
SHELL=/bin/bash

# 每天凌晨 2:00 运行快速检查
0 2 * * * cd "$PROJECT_ROOT" && "$PYTHON_CMD" scripts/quick_enhancement.py --check >> logs/maintenance.log 2>&1

# 每周一凌晨 3:00 运行完整的安全扫描
0 3 * * 1 cd "$PROJECT_ROOT" && "$PYTHON_CMD" scripts/security_enhancer.py --scan --report >> logs/security.log 2>&1

# 每周三凌晨 3:30 运行依赖审计
30 3 * * 3 cd "$PROJECT_ROOT" && "$PYTHON_CMD" scripts/dependency_audit.py --analyze --report >> logs/dependency.log 2>&1

# 每周五凌晨 4:00 运行结构优化
0 4 * * 5 cd "$PROJECT_ROOT" && "$PYTHON_CMD" scripts/structure_optimizer.py --analyze --report >> logs/structure.log 2>&1

# 每月第一个周日凌晨 5:00 运行完整的自动化套件
0 5 1-7 * 0 cd "$PROJECT_ROOT" && "$PYTHON_CMD" scripts/automation_suite.py --suite full >> logs/full_maintenance.log 2>&1

# 每小时检查监控状态（工作时间 9:00-18:00）
0 9-18 * * 1-5 cd "$PROJECT_ROOT" && "$PYTHON_CMD" scripts/enhanced_monitor.py --status >> logs/monitor_status.log 2>&1

# 每天晚上 23:00 清理临时文件
0 23 * * * find "$PROJECT_ROOT/temp" -type f -mtime +7 -delete 2>/dev/null || true

# 每周日凌晨 1:00 清理旧日志文件（保留30天）
0 1 * * 0 find "$PROJECT_ROOT/logs" -name "*.log" -mtime +30 -delete 2>/dev/null || true

EOF

    echo -e "${GREEN}✅ 定时任务配置已生成: $crontab_file${NC}"
}

# 创建日志目录
setup_log_directories() {
    echo -e "${YELLOW}📁 设置日志目录...${NC}"
    
    local log_dirs=(
        "$PROJECT_ROOT/logs"
        "$PROJECT_ROOT/logs/maintenance"
        "$PROJECT_ROOT/logs/security"
        "$PROJECT_ROOT/logs/dependency"
        "$PROJECT_ROOT/logs/structure"
        "$PROJECT_ROOT/logs/monitor"
    )
    
    for dir in "${log_dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            echo -e "${GREEN}✅ 创建目录: $dir${NC}"
        else
            echo -e "${GREEN}✅ 目录已存在: $dir${NC}"
        fi
    done
}

# 创建日志轮转配置
setup_log_rotation() {
    echo -e "${YELLOW}🔄 设置日志轮转...${NC}"
    
    local logrotate_config="$PROJECT_ROOT/logs/logrotate.conf"
    
    cat > "$logrotate_config" << EOF
# ChatExcel MCP 项目日志轮转配置

$PROJECT_ROOT/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 $(whoami) $(id -gn)
    postrotate
        # 可以在这里添加日志轮转后的操作
    endscript
}

$PROJECT_ROOT/logs/*/*.log {
    weekly
    rotate 12
    compress
    delaycompress
    missingok
    notifempty
    create 644 $(whoami) $(id -gn)
}
EOF

    echo -e "${GREEN}✅ 日志轮转配置已创建: $logrotate_config${NC}"
}

# 安装定时任务
install_crontab() {
    local crontab_file="$SCRIPT_DIR/maintenance_crontab.txt"
    
    echo -e "${YELLOW}⚙️ 安装定时任务...${NC}"
    echo -e "${YELLOW}当前用户: $(whoami)${NC}"
    
    # 备份现有的 crontab
    if crontab -l > /dev/null 2>&1; then
        echo -e "${YELLOW}📋 备份现有 crontab...${NC}"
        crontab -l > "$SCRIPT_DIR/crontab_backup_$(date +%Y%m%d_%H%M%S).txt"
        echo -e "${GREEN}✅ 现有 crontab 已备份${NC}"
        
        # 询问是否要合并
        echo -e "${YELLOW}❓ 是否要将新的定时任务添加到现有 crontab？(y/n)${NC}"
        read -r response
        
        if [[ "$response" =~ ^[Yy]$ ]]; then
            # 合并 crontab
            {
                crontab -l
                echo ""
                echo "# === ChatExcel MCP 项目维护任务 ==="
                cat "$crontab_file"
            } | crontab -
            echo -e "${GREEN}✅ 定时任务已添加到现有 crontab${NC}"
        else
            echo -e "${YELLOW}⚠️ 跳过 crontab 安装${NC}"
            echo -e "${BLUE}💡 您可以手动将以下内容添加到 crontab:${NC}"
            echo -e "${BLUE}   crontab -e${NC}"
            echo -e "${BLUE}   然后复制 $crontab_file 的内容${NC}"
        fi
    else
        # 没有现有 crontab，直接安装
        echo -e "${YELLOW}📋 安装新的 crontab...${NC}"
        crontab "$crontab_file"
        echo -e "${GREEN}✅ 定时任务已安装${NC}"
    fi
}

# 显示安装后的信息
show_post_install_info() {
    echo ""
    echo -e "${GREEN}🎉 维护定时任务设置完成！${NC}"
    echo "================================================"
    echo -e "${BLUE}📋 已设置的定时任务:${NC}"
    echo "  • 每天 02:00 - 快速检查"
    echo "  • 每周一 03:00 - 安全扫描"
    echo "  • 每周三 03:30 - 依赖审计"
    echo "  • 每周五 04:00 - 结构优化"
    echo "  • 每月第一个周日 05:00 - 完整维护"
    echo "  • 工作日每小时 - 监控状态检查"
    echo "  • 每天 23:00 - 清理临时文件"
    echo "  • 每周日 01:00 - 清理旧日志"
    echo ""
    echo -e "${BLUE}📁 日志位置:${NC}"
    echo "  • 主日志: $PROJECT_ROOT/logs/"
    echo "  • 维护日志: $PROJECT_ROOT/logs/maintenance.log"
    echo "  • 安全日志: $PROJECT_ROOT/logs/security.log"
    echo ""
    echo -e "${BLUE}🔧 管理命令:${NC}"
    echo "  • 查看定时任务: crontab -l"
    echo "  • 编辑定时任务: crontab -e"
    echo "  • 删除定时任务: crontab -r"
    echo "  • 手动运行检查: python3 scripts/quick_enhancement.py --check"
    echo ""
    echo -e "${YELLOW}⚠️ 注意事项:${NC}"
    echo "  • 确保项目路径不会改变"
    echo "  • 定期检查日志文件"
    echo "  • 根据需要调整定时任务频率"
    echo "  • 监控磁盘空间使用情况"
}

# 主函数
main() {
    echo -e "${BLUE}开始设置维护定时任务...${NC}"
    echo ""
    
    check_python
    echo ""
    
    check_scripts
    echo ""
    
    setup_log_directories
    echo ""
    
    setup_log_rotation
    echo ""
    
    generate_crontab
    echo ""
    
    # 询问是否安装 crontab
    echo -e "${YELLOW}❓ 是否要立即安装定时任务到 crontab？(y/n)${NC}"
    read -r install_response
    
    if [[ "$install_response" =~ ^[Yy]$ ]]; then
        install_crontab
    else
        echo -e "${YELLOW}⚠️ 跳过 crontab 安装${NC}"
        echo -e "${BLUE}💡 定时任务配置已保存到: $SCRIPT_DIR/maintenance_crontab.txt${NC}"
        echo -e "${BLUE}   您可以稍后手动安装: crontab $SCRIPT_DIR/maintenance_crontab.txt${NC}"
    fi
    
    echo ""
    show_post_install_info
}

# 处理命令行参数
case "${1:-}" in
    --help|-h)
        echo "用法: $0 [选项]"
        echo ""
        echo "选项:"
        echo "  --help, -h     显示此帮助信息"
        echo "  --check        仅检查环境，不安装"
        echo "  --generate     仅生成配置文件，不安装"
        echo ""
        echo "此脚本将为 ChatExcel MCP 项目设置自动化维护定时任务。"
        exit 0
        ;;
    --check)
        check_python
        check_scripts
        echo -e "${GREEN}✅ 环境检查完成${NC}"
        exit 0
        ;;
    --generate)
        check_python
        setup_log_directories
        setup_log_rotation
        generate_crontab
        echo -e "${GREEN}✅ 配置文件生成完成${NC}"
        exit 0
        ;;
    "")
        main
        ;;
    *)
        echo -e "${RED}❌ 未知选项: $1${NC}"
        echo "使用 --help 查看帮助信息"
        exit 1
        ;;
esac