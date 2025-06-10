#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""
MCP服务器功能测试脚本
"""

import sys
import os
import pandas as pd
from pathlib import Path

# 添加服务器路径
sys.path.append('/Users/wangdada/Downloads/mcp/excel-mcp/chatExcel-mcp-server')

def test_mcp_imports():
    """测试MCP服务器模块导入"""
    print("=== 测试模块导入 ===")
    try:
        import server
        print("✓ server模块导入成功")
        
        from comprehensive_data_verification import ComprehensiveDataVerifier
        print("✓ ComprehensiveDataVerifier导入成功")
        
        from enhanced_excel_helper import smart_read_excel, detect_file_encoding
        print("✓ enhanced_excel_helper模块导入成功")
        
        from data_verification import DataVerificationEngine
        print("✓ DataVerificationEngine导入成功")
        
        return True
    except Exception as e:
        print(f"✗ 模块导入失败: {e}")
        return False

def create_test_excel_file():
    """创建测试Excel文件"""
    print("\n=== 创建测试Excel文件 ===")
    try:
        # 创建测试数据
        test_data = {
            '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
            '年龄': [25, 30, 35, 28, 32],
            '城市': ['北京', '上海', '广州', '深圳', '杭州'],
            '薪资': [8000, 12000, 15000, 9500, 11000],
            '部门': ['技术部', '销售部', '市场部', '技术部', '财务部']
        }
        
        df = pd.DataFrame(test_data)
        test_file = '/Users/wangdada/Downloads/mcp/excel-mcp/test_data.xlsx'
        df.to_excel(test_file, index=False)
        print(f"✓ 测试文件创建成功: {test_file}")
        return test_file
    except Exception as e:
        print(f"✗ 测试文件创建失败: {e}")
        return None

def test_comprehensive_verification(test_file):
    """测试综合数据验证功能"""
    print("\n=== 测试综合数据验证功能 ===")
    try:
        from comprehensive_data_verification import ComprehensiveDataVerifier
        
        verifier = ComprehensiveDataVerifier()
        result = verifier.comprehensive_excel_verification(
            file_path=test_file,
            verification_level="detailed",
            save_report=False
        )
        
        print(f"✓ 验证完成")
        print(f"  - 总体状态: {result.get('overall_status')}")
        print(f"  - 质量得分: {result.get('data_quality_score', 0):.1f}")
        print(f"  - 建议数量: {len(result.get('recommendations', []))}")
        
        return True
    except Exception as e:
        print(f"✗ 综合验证测试失败: {e}")
        return False

def test_mcp_tools(test_file):
    """测试MCP工具函数"""
    print("\n=== 测试MCP工具函数 ===")
    try:
        import server
        
        # 测试read_excel_metadata工具
        print("测试 read_excel_metadata...")
        metadata_result = server.read_excel_metadata(test_file)
        print(f"✓ read_excel_metadata成功，返回{len(metadata_result)}个字段")
        
        # 测试comprehensive_data_verification_tool
        print("测试 comprehensive_data_verification_tool...")
        verification_result = server.comprehensive_data_verification_tool(
            file_path=test_file,
            verification_level="detailed",
            save_report=False
        )
        print(f"✓ comprehensive_data_verification_tool成功")
        print(f"  - 成功状态: {verification_result.get('success')}")
        print(f"  - 总体状态: {verification_result.get('overall_status')}")
        
        return True
    except Exception as e:
        print(f"✗ MCP工具测试失败: {e}")
        return False

def test_encoding_detection(test_file):
    """测试编码检测功能"""
    print("\n=== 测试编码检测功能 ===")
    try:
        from enhanced_excel_helper import detect_file_encoding, smart_read_excel
        
        # 测试编码检测
        encoding_info = detect_file_encoding(test_file)
        print(f"✓ 编码检测成功: {encoding_info}")
        
        # 测试智能读取
        read_result = smart_read_excel(test_file)
        print(f"✓ 智能读取成功: {read_result.get('success')}")
        
        if not read_result.get('success'):
            print(f"✗ 智能读取失败: {read_result.get('error', '未知错误')}")
            return False
            
        if read_result.get('success'):
            df = read_result.get('dataframe')
            if df is None:
                df = read_result.get('data')
            
            if df is not None and hasattr(df, 'shape'):
                print(f"  - 数据形状: {df.shape}")
                print(f"  - 列名: {list(df.columns)}")
                return True
            else:
                print("✗ 无法获取数据框架")
                return False
        
        return True
    except Exception as e:
        print(f"✗ 编码检测测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    test_results = []
    test_names = []
    
    # 1. 测试模块导入
    result1 = test_mcp_imports()
    test_results.append(result1)
    test_names.append("模块导入")
    print(f"测试1结果: {result1}")
    
    # 2. 创建测试文件
    test_file = create_test_excel_file()
    if not test_file:
        print("无法创建测试文件，终止测试")
        return
    
    # 3. 测试编码检测
    result2 = test_encoding_detection(test_file)
    test_results.append(result2)
    test_names.append("编码检测")
    print(f"测试2结果: {result2}")
    
    # 4. 测试综合验证
    result3 = test_comprehensive_verification(test_file)
    test_results.append(result3)
    test_names.append("综合验证")
    print(f"测试3结果: {result3}")
    
    # 5. 测试MCP工具
    result4 = test_mcp_tools(test_file)
    test_results.append(result4)
    test_names.append("MCP工具")
    print(f"测试4结果: {result4}")
    
    # 清理测试文件
    try:
        os.remove(test_file)
        print(f"\n✓ 测试文件已清理: {test_file}")
    except:
        pass
    
    # 输出测试结果
    print("\n=== 测试结果汇总 ===")
    passed_tests = sum(test_results)
    total_tests = len(test_results)
    print(f"通过测试: {passed_tests}/{total_tests}")
    
    # 显示失败的测试
    for i, (name, result) in enumerate(zip(test_names, test_results)):
        status = "✓" if result else "✗"
        print(f"{status} {name}: {'通过' if result else '失败'}")
    
    if passed_tests == total_tests:
        print("🎉 所有测试通过！MCP服务器功能正常")
    else:
        print("⚠️  部分测试失败，请检查相关功能")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)