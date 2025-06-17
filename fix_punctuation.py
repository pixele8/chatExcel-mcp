#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

file_path = '/Users/wangdada/Downloads/mcp/chatExcel-mcp/utils/string_escape_handler.py'

# 读取文件内容
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换中文标点符号
content = content.replace('，', ',')
content = content.replace('：', ':')

# 写回文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("已修复中文标点符号问题")