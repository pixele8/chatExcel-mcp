#!/bin/bash
# 项目维护脚本

set -e

echo "🔧 开始项目维护..."

# 清理临时文件
echo "🧹 清理临时文件..."
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.log" -mtime +7 -delete
find charts/ -name "*.html" -mtime +30 -delete 2>/dev/null || true

# 清理过期的备份文件
echo "📦 清理过期备份..."
find . -name "requirements_backup_*.txt" -mtime +30 -delete 2>/dev/null || true

# 检查磁盘空间
echo "💾 检查磁盘空间..."
df -h .

# 更新.gitignore
echo "📝 更新.gitignore..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*.so
*.egg-info/
dist/
build/

# Virtual Environment
venv/
.env
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
chatExcel.log

# Charts (keep recent ones)
charts/*.html

# Backup files
requirements_backup_*.txt

# Test coverage
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
EOF

echo "✅ 项目维护完成！"