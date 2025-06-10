#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的调试脚本
"""

import pandas as pd
import os
import sys
import traceback

def create_test_file():
    """创建测试文件"""
    data = {
        '姓名': ['张三', '李四'],
        '年龄': [25, 30],
        '薪资': [8000, 12000]
    }
    df = pd.DataFrame(data)
    file_path = 'simple_test.xlsx'
    df.to_excel(file_path, index=False)
    return file_path

def test_import():
    """测试导入"""
    print("🧪 测试模块导入")
    try:
        from server import run_excel_code
        print("✅ server.run_excel_code 导入成功")
        return True
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        traceback.print_exc()
        return False

def test_function_call():
    """测试函数调用"""
    print("\n🧪 测试函数调用")
    
    file_path = create_test_file()
    
    try:
        from server import run_excel_code
        
        # 简单的代码
        code = "print(f'数据形状: {df.shape}')"
        
        print(f"调用 run_excel_code('{file_path}', '{code}')")
        result = run_excel_code(file_path, code)
        
        print(f"返回结果类型: {type(result)}")
        print(f"返回结果: {result}")
        
        # 判断是否成功：有输出且没有错误
        if isinstance(result, dict):
            has_output = 'output' in result and result['output']
            has_error = 'error' in result
            return has_output and not has_error
        return False
        
    except Exception as e:
        print(f"❌ 函数调用失败: {e}")
        traceback.print_exc()
        return False
        
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"🧹 已清理: {file_path}")

def main():
    """主函数"""
    print("🔍 简单调试测试")
    print("=" * 40)
    
    # 测试导入
    import_ok = test_import()
    if not import_ok:
        print("❌ 导入失败，无法继续测试")
        return
    
    # 测试函数调用
    call_ok = test_function_call()
    
    print(f"\n{'='*40}")
    print(f"导入测试: {'✅' if import_ok else '❌'}")
    print(f"调用测试: {'✅' if call_ok else '❌'}")

if __name__ == "__main__":
    main()