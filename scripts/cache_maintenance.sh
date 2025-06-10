#!/bin/bash
# 编码缓存自动维护脚本
# 建议通过 crontab 定期执行

# 设置脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
CACHE_MANAGER="$PROJECT_DIR/cache_manager.py"

# 日志文件
LOG_FILE="$PROJECT_DIR/cache_maintenance.log"

# 记录日志的函数
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查 Python 环境
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        log_message "错误: 未找到 Python 解释器"
        exit 1
    fi
}

# 执行缓存维护
maintain_cache() {
    log_message "开始缓存维护任务"
    
    # 切换到项目目录
    cd "$PROJECT_DIR" || {
        log_message "错误: 无法切换到项目目录 $PROJECT_DIR"
        exit 1
    }
    
    # 检查缓存管理器是否存在
    if [[ ! -f "$CACHE_MANAGER" ]]; then
        log_message "错误: 缓存管理器不存在 $CACHE_MANAGER"
        exit 1
    fi
    
    # 显示当前缓存状态
    log_message "当前缓存状态:"
    $PYTHON_CMD "$CACHE_MANAGER" stats 2>&1 | tee -a "$LOG_FILE"
    
    # 执行缓存优化
    log_message "执行缓存优化:"
    $PYTHON_CMD "$CACHE_MANAGER" optimize 2>&1 | tee -a "$LOG_FILE"
    
    # 显示优化后状态
    log_message "优化后缓存状态:"
    $PYTHON_CMD "$CACHE_MANAGER" stats 2>&1 | tee -a "$LOG_FILE"
    
    log_message "缓存维护任务完成"
}

# 清理旧日志（保留最近30天）
cleanup_logs() {
    if [[ -f "$LOG_FILE" ]]; then
        # 创建临时文件保存最近30天的日志
        TEMP_LOG="${LOG_FILE}.tmp"
        
        # 计算30天前的日期
        if [[ "$(uname)" == "Darwin" ]]; then
            # macOS
            CUTOFF_DATE=$(date -v-30d '+%Y-%m-%d')
        else
            # Linux
            CUTOFF_DATE=$(date -d '30 days ago' '+%Y-%m-%d')
        fi
        
        # 过滤日志，只保留最近30天的记录
        grep -E "\[$CUTOFF_DATE|$(date '+%Y-%m-%d')" "$LOG_FILE" > "$TEMP_LOG" 2>/dev/null || true
        
        # 如果临时文件不为空，替换原日志文件
        if [[ -s "$TEMP_LOG" ]]; then
            mv "$TEMP_LOG" "$LOG_FILE"
            log_message "日志清理完成，保留最近30天记录"
        else
            rm -f "$TEMP_LOG"
        fi
    fi
}

# 主函数
main() {
    # 检查参数
    case "${1:-maintain}" in
        "maintain")
            check_python
            maintain_cache
            cleanup_logs
            ;;
        "stats")
            check_python
            cd "$PROJECT_DIR" && $PYTHON_CMD "$CACHE_MANAGER" stats
            ;;
        "cleanup")
            check_python
            cd "$PROJECT_DIR" && $PYTHON_CMD "$CACHE_MANAGER" cleanup
            ;;
        "backup")
            check_python
            cd "$PROJECT_DIR" && $PYTHON_CMD "$CACHE_MANAGER" backup
            ;;
        "help")
            echo "用法: $0 [maintain|stats|cleanup|backup|help]"
            echo "  maintain  - 执行完整的缓存维护（默认）"
            echo "  stats     - 显示缓存统计信息"
            echo "  cleanup   - 清理过期缓存"
            echo "  backup    - 创建缓存备份"
            echo "  help      - 显示此帮助信息"
            ;;
        *)
            echo "未知参数: $1"
            echo "使用 '$0 help' 查看帮助信息"
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"