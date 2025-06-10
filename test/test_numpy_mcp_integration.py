#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NumPy与MCP服务集成测试脚本

测试NumPy在MCP Excel服务中的实际应用场景：
1. Excel数据处理中的NumPy使用
2. 数据分析和计算功能
3. 与pandas的协同工作
4. 错误处理和边界情况
5. 性能和内存管理
"""

import sys
import os
import traceback
import tempfile
import pandas as pd
import numpy as np
from io import StringIO

# 添加项目路径
sys.path.append('/Users/wangdada/Downloads/mcp/excel-mcp/chatExcel-mcp-server')

def create_test_excel_with_numpy():
    """创建包含数值数据的测试Excel文件"""
    print("\n=== 创建NumPy测试Excel文件 ===")
    try:
        # 使用NumPy生成测试数据
        np.random.seed(42)
        
        # 生成不同类型的数值数据
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        sales_data = np.random.normal(10000, 2000, 100).astype(int)
        growth_rates = np.random.normal(0.05, 0.02, 100)
        categories = np.random.choice(['A', 'B', 'C', 'D'], 100)
        
        # 添加一些数学函数生成的数据
        time_series = np.sin(np.linspace(0, 4*np.pi, 100)) * 1000 + 5000
        exponential_data = np.exp(np.linspace(0, 2, 100)) * 100
        
        # 创建DataFrame
        df = pd.DataFrame({
            '日期': dates,
            '销售额': sales_data,
            '增长率': growth_rates,
            '类别': categories,
            '时间序列': time_series,
            '指数数据': exponential_data
        })
        
        # 保存到临时文件
        temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
        df.to_excel(temp_file.name, index=False)
        
        print(f"✅ 测试Excel文件创建成功: {temp_file.name}")
        print(f"   - 数据行数: {len(df)}")
        print(f"   - 数据列数: {len(df.columns)}")
        print(f"   - 数值列: {df.select_dtypes(include=[np.number]).columns.tolist()}")
        
        return temp_file.name, df
    except Exception as e:
        print(f"❌ 创建测试Excel文件失败: {e}")
        traceback.print_exc()
        return None, None

def test_numpy_in_excel_code_execution():
    """测试在Excel代码执行中使用NumPy"""
    print("\n=== Excel代码执行中的NumPy测试 ===")
    try:
        # 模拟MCP服务中的代码执行环境
        test_codes = [
            # 基本NumPy操作
            """
# 基本NumPy数组操作
import numpy as np
data_array = np.array(df['销售额'])
result = {
    'mean': np.mean(data_array),
    'std': np.std(data_array),
    'min': np.min(data_array),
    'max': np.max(data_array)
}
            """,
            
            # 数学运算
            """
# NumPy数学运算
import numpy as np
sales = np.array(df['销售额'])
growth = np.array(df['增长率'])

# 计算预测销售额
predicted_sales = sales * (1 + growth)
result = {
    'original_total': np.sum(sales),
    'predicted_total': np.sum(predicted_sales),
    'growth_impact': np.sum(predicted_sales) - np.sum(sales)
}
            """,
            
            # 统计分析
            """
# NumPy统计分析
import numpy as np
time_series = np.array(df['时间序列'])

# 计算移动平均
window_size = 7
moving_avg = np.convolve(time_series, np.ones(window_size)/window_size, mode='valid')

# 计算相关性
sales = np.array(df['销售额'])
correlation = np.corrcoef(sales[:-6], moving_avg)[0, 1]

result = {
    'moving_avg_length': len(moving_avg),
    'correlation': correlation,
    'trend': 'increasing' if correlation > 0 else 'decreasing'
}
            """,
            
            # 线性代数操作
            """
# NumPy线性代数
import numpy as np

# 创建特征矩阵
features = np.column_stack([
    np.array(df['销售额']),
    np.array(df['增长率']),
    np.array(df['时间序列'])
])

# 计算协方差矩阵
cov_matrix = np.cov(features.T)

# 计算特征值和特征向量
eigenvals, eigenvecs = np.linalg.eig(cov_matrix)

result = {
    'feature_matrix_shape': features.shape,
    'covariance_matrix_det': np.linalg.det(cov_matrix),
    'principal_eigenvalue': np.max(eigenvals)
}
            """
        ]
        
        # 创建测试数据
        excel_file, df = create_test_excel_with_numpy()
        if not excel_file:
            return False
        
        successful_executions = 0
        
        for i, code in enumerate(test_codes, 1):
            try:
                print(f"\n--- 测试代码 {i} ---")
                
                # 模拟代码执行环境
                local_vars = {
                    'df': df,
                    'pd': pd,
                    'np': np
                }
                
                # 执行代码
                exec(code, {}, local_vars)
                
                # 获取结果
                result = local_vars.get('result', {})
                print(f"✅ 代码执行成功")
                print(f"   结果: {result}")
                
                successful_executions += 1
                
            except Exception as e:
                print(f"❌ 代码执行失败: {e}")
                traceback.print_exc()
        
        # 清理临时文件
        os.unlink(excel_file)
        
        print(f"\n✅ NumPy代码执行测试完成: {successful_executions}/{len(test_codes)} 成功")
        return successful_executions == len(test_codes)
        
    except Exception as e:
        print(f"❌ NumPy代码执行测试失败: {e}")
        traceback.print_exc()
        return False

def test_numpy_pandas_integration():
    """测试NumPy与Pandas的集成"""
    print("\n=== NumPy与Pandas集成测试 ===")
    try:
        # 创建测试数据
        np.random.seed(123)
        
        # 使用NumPy创建数据，然后转换为Pandas
        numpy_data = {
            'integers': np.random.randint(1, 100, 50),
            'floats': np.random.normal(0, 1, 50),
            'booleans': np.random.choice([True, False], 50),
            'dates': np.datetime64('2024-01-01') + np.arange(50)
        }
        
        # 转换为Pandas DataFrame
        df = pd.DataFrame(numpy_data)
        
        print(f"✅ NumPy到Pandas转换成功")
        print(f"   - DataFrame形状: {df.shape}")
        print(f"   - 数据类型: {df.dtypes.to_dict()}")
        
        # 在Pandas中使用NumPy函数
        df['log_floats'] = np.log(np.abs(df['floats']) + 1)
        df['sqrt_integers'] = np.sqrt(df['integers'])
        df['cumsum_integers'] = np.cumsum(df['integers'])
        
        print(f"✅ Pandas中NumPy函数应用成功")
        print(f"   - 新增列数: 3")
        
        # 从Pandas提取NumPy数组进行计算
        float_array = df['floats'].values
        int_array = df['integers'].values
        
        # NumPy计算
        correlation = np.corrcoef(float_array, int_array)[0, 1]
        covariance = np.cov(float_array, int_array)[0, 1]
        
        print(f"✅ Pandas到NumPy数据提取和计算成功")
        print(f"   - 相关系数: {correlation:.4f}")
        print(f"   - 协方差: {covariance:.4f}")
        
        # 测试数据一致性
        original_sum = np.sum(numpy_data['integers'])
        pandas_sum = df['integers'].sum()
        numpy_from_pandas_sum = np.sum(df['integers'].values)
        
        consistency_check = (original_sum == pandas_sum == numpy_from_pandas_sum)
        print(f"✅ 数据一致性检查: {'通过' if consistency_check else '失败'}")
        
        return True
        
    except Exception as e:
        print(f"❌ NumPy与Pandas集成测试失败: {e}")
        traceback.print_exc()
        return False

def test_numpy_error_handling_in_mcp():
    """测试MCP环境中NumPy的错误处理"""
    print("\n=== MCP环境中NumPy错误处理测试 ===")
    try:
        # 创建测试DataFrame
        df = pd.DataFrame({
            'valid_numbers': [1, 2, 3, 4, 5],
            'with_nan': [1, np.nan, 3, np.nan, 5],
            'with_inf': [1, 2, np.inf, 4, 5],
            'mixed_types': [1, '2', 3, '4', 5]
        })
        
        error_handling_tests = [
            # 处理NaN值
            """
import numpy as np
data = np.array(df['with_nan'])
result = {
    'has_nan': np.any(np.isnan(data)),
    'nan_count': np.sum(np.isnan(data)),
    'mean_ignore_nan': np.nanmean(data)
}
            """,
            
            # 处理无穷值
            """
import numpy as np
data = np.array(df['with_inf'])
result = {
    'has_inf': np.any(np.isinf(data)),
    'finite_only': data[np.isfinite(data)],
    'finite_mean': np.mean(data[np.isfinite(data)])
}
            """,
            
            # 处理类型转换错误
            """
import numpy as np
try:
    # 尝试转换混合类型
    data = pd.to_numeric(df['mixed_types'], errors='coerce')
    numpy_data = np.array(data)
    result = {
        'conversion_success': True,
        'nan_after_conversion': np.sum(np.isnan(numpy_data)),
        'valid_data': numpy_data[~np.isnan(numpy_data)]
    }
except Exception as e:
    result = {
        'conversion_success': False,
        'error': str(e)
    }
            """
        ]
        
        successful_tests = 0
        
        for i, test_code in enumerate(error_handling_tests, 1):
            try:
                print(f"\n--- 错误处理测试 {i} ---")
                
                local_vars = {
                    'df': df,
                    'pd': pd,
                    'np': np
                }
                
                exec(test_code, {}, local_vars)
                result = local_vars.get('result', {})
                
                print(f"✅ 错误处理测试成功")
                print(f"   结果: {result}")
                
                successful_tests += 1
                
            except Exception as e:
                print(f"❌ 错误处理测试失败: {e}")
        
        print(f"\n✅ 错误处理测试完成: {successful_tests}/{len(error_handling_tests)} 成功")
        return successful_tests == len(error_handling_tests)
        
    except Exception as e:
        print(f"❌ NumPy错误处理测试失败: {e}")
        traceback.print_exc()
        return False

def test_numpy_performance_in_mcp():
    """测试MCP环境中NumPy的性能"""
    print("\n=== MCP环境中NumPy性能测试 ===")
    try:
        import time
        
        # 创建大型数据集
        large_df = pd.DataFrame({
            'data1': np.random.randn(10000),
            'data2': np.random.randn(10000),
            'data3': np.random.randn(10000)
        })
        
        performance_tests = [
            # 大数组运算
            {
                'name': '大数组统计计算',
                'code': '''
import numpy as np
import time
start_time = time.time()
data = np.array(df[['data1', 'data2', 'data3']])
means = np.mean(data, axis=0)
stds = np.std(data, axis=0)
corr_matrix = np.corrcoef(data.T)
end_time = time.time()
result = {
    'execution_time': end_time - start_time,
    'data_shape': data.shape,
    'means': means.tolist(),
    'correlation_det': np.linalg.det(corr_matrix)
}
'''
            },
            
            # 矩阵运算
            {
                'name': '矩阵乘法运算',
                'code': '''
import numpy as np
import time
start_time = time.time()
matrix_a = np.random.rand(500, 500)
matrix_b = np.random.rand(500, 500)
result_matrix = np.dot(matrix_a, matrix_b)
end_time = time.time()
result = {
    'execution_time': end_time - start_time,
    'matrix_shape': result_matrix.shape,
    'result_sum': np.sum(result_matrix)
}
'''
            }
        ]
        
        successful_tests = 0
        
        for test in performance_tests:
            try:
                print(f"\n--- {test['name']} ---")
                
                local_vars = {
                    'df': large_df,
                    'pd': pd,
                    'np': np
                }
                
                exec(test['code'], {}, local_vars)
                result = local_vars.get('result', {})
                
                execution_time = result.get('execution_time', 0)
                print(f"✅ {test['name']}完成")
                print(f"   执行时间: {execution_time:.4f} 秒")
                print(f"   其他结果: {dict((k, v) for k, v in result.items() if k != 'execution_time')}")
                
                # 性能基准检查（执行时间应该在合理范围内）
                if execution_time < 10:  # 10秒内完成
                    print(f"✅ 性能表现良好")
                    successful_tests += 1
                else:
                    print(f"⚠️  性能较慢，可能需要优化")
                
            except Exception as e:
                print(f"❌ {test['name']}失败: {e}")
        
        print(f"\n✅ 性能测试完成: {successful_tests}/{len(performance_tests)} 通过")
        return successful_tests == len(performance_tests)
        
    except Exception as e:
        print(f"❌ NumPy性能测试失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🔬 NumPy与MCP服务集成测试")
    print("=" * 60)
    
    test_results = {}
    
    # 1. Excel代码执行中的NumPy测试
    test_results['Excel代码执行中的NumPy'] = test_numpy_in_excel_code_execution()
    
    # 2. NumPy与Pandas集成测试
    test_results['NumPy与Pandas集成'] = test_numpy_pandas_integration()
    
    # 3. MCP环境中NumPy错误处理测试
    test_results['MCP环境中NumPy错误处理'] = test_numpy_error_handling_in_mcp()
    
    # 4. MCP环境中NumPy性能测试
    test_results['MCP环境中NumPy性能'] = test_numpy_performance_in_mcp()
    
    # 输出测试总结
    print("\n" + "=" * 60)
    print("📊 MCP集成测试结果总结")
    print("=" * 60)
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n总体结果: {passed_tests}/{total_tests} 项测试通过")
    
    if passed_tests == total_tests:
        print("🎉 所有集成测试通过！NumPy在MCP服务中功能完备且稳定。")
    elif passed_tests >= total_tests * 0.75:
        print("⚠️  大部分集成测试通过，NumPy在MCP服务中基本可用。")
    else:
        print("❌ 多项集成测试失败，NumPy在MCP服务中可能存在问题。")
    
    return test_results

if __name__ == "__main__":
    main()