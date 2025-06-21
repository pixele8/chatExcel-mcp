始终注意当前项目是在虚拟环境中研发，注意环境依赖导入等相关事项不出错。虚拟环境运行脚本为：
{
  "mcpServers": {
    "chatExcel": {
      "command": "/Users/wangdada/Downloads/mcp/chatExcel-mcp/venv/bin/python",
      "args": [
        "/Users/wangdada/Downloads/mcp/chatExcel-mcp/server.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/wangdada/Downloads/mcp/chatExcel-mcp"
      },
      "description": "chatExcel MCP服务器 - 支持31个Excel智能处理与数据分析工具",
      "version": "2.0",
      "capabilities": [
        "Excel文件读写和分析，Excel函数公式解析/写入",
        "数据验证和完整性检查",
        "交互式图表生成",
        "代码执行和性能分析",
        "智能参数推荐",
        "批量数据处理"
      ],
      "tools_count": 31,
      "supported_formats": ["xlsx", "xls", "csv", "json", "html"]
    }
  }
}