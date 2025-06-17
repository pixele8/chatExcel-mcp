#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的 Excel 公式处理功能测试
"""

import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

print("开始测试 formulas 库基本功能...")

try:
    import formulas
    from formulas import Parser
    print("✓ formulas 库导入成功")
    
    # 测试基本公式解析
    parser = Parser()
    test_formula = "=SUM(A1:A10)"
    print(f"\n测试公式: {test_formula}")
    
    try:
        ast_nodes = parser.ast(test_formula)
        print(f"✓ 公式解析成功，AST 节点数: {len(ast_nodes)}")
        
        if len(ast_nodes) > 1:
            compiled_formula = ast_nodes[1].compile()
            print(f"✓ 公式编译成功: {compiled_formula}")
            
            if hasattr(compiled_formula, 'inputs'):
                print(f"✓ 公式输入: {list(compiled_formula.inputs)}")
        
    except Exception as e:
        print(f"✗ 公式处理失败: {e}")
    
    # 测试简单数学公式
    simple_formula = "=2+3*4"
    print(f"\n测试简单公式: {simple_formula}")
    
    try:
        ast_nodes = parser.ast(simple_formula)
        if len(ast_nodes) > 1:
            compiled_formula = ast_nodes[1].compile()
            result = compiled_formula()
            print(f"✓ 计算结果: {result}")
    except Exception as e:
        print(f"✗ 简单公式计算失败: {e}")
        
except ImportError as e:
    print(f"✗ formulas 库导入失败: {e}")
    sys.exit(1)

print("\n测试完成!")