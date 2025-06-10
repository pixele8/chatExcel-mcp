#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NumPy功能完备性和稳定性测试脚本

本脚本全面测试NumPy在当前项目环境中的：
1. 导入和版本检查
2. 基本数组操作
3. 数学运算功能
4. 数据类型支持
5. 与pandas的兼容性
6. 内存管理和性能
7. 错误处理机制
"""

import sys
import traceback
import time
import gc
from typing import Any, Dict, List

def test_numpy_import():
    """测试NumPy导入和基本信息"""
    print("\n=== NumPy导入和版本测试 ===")
    try:
        import numpy as np
        print(f"✅ NumPy导入成功")
        print(f"📦 NumPy版本: {np.__version__}")
        print(f"📍 安装路径: {np.__file__}")
        print(f"🏗️  构建信息: {np.version.full_version}")
        
        # 检查关键模块
        modules_to_check = [
            'numpy.linalg', 'numpy.random', 'numpy.fft', 
            'numpy.ma', 'numpy.polynomial', 'numpy.testing'
        ]
        
        for module_name in modules_to_check:
            try:
                __import__(module_name)
                print(f"✅ {module_name} 可用")
            except ImportError as e:
                print(f"❌ {module_name} 不可用: {e}")
                
        return True, np
    except Exception as e:
        print(f"❌ NumPy导入失败: {e}")
        traceback.print_exc()
        return False, None

def test_basic_array_operations(np):
    """测试基本数组操作"""
    print("\n=== 基本数组操作测试 ===")
    try:
        # 创建不同类型的数组
        arr1 = np.array([1, 2, 3, 4, 5])
        arr2 = np.zeros((3, 3))
        arr3 = np.ones((2, 4))
        arr4 = np.arange(10)
        arr5 = np.linspace(0, 1, 11)
        arr6 = np.random.rand(5, 5)
        
        print(f"✅ 基本数组创建成功")
        print(f"   - 整数数组: {arr1.shape}, dtype: {arr1.dtype}")
        print(f"   - 零数组: {arr2.shape}, dtype: {arr2.dtype}")
        print(f"   - 单位数组: {arr3.shape}, dtype: {arr3.dtype}")
        print(f"   - 范围数组: {arr4.shape}, dtype: {arr4.dtype}")
        print(f"   - 线性空间: {arr5.shape}, dtype: {arr5.dtype}")
        print(f"   - 随机数组: {arr6.shape}, dtype: {arr6.dtype}")
        
        # 数组操作
        reshaped = arr4.reshape(2, 5)
        transposed = arr6.T
        sliced = arr6[1:3, 2:4]
        
        print(f"✅ 数组变形操作成功")
        print(f"   - 重塑: {reshaped.shape}")
        print(f"   - 转置: {transposed.shape}")
        print(f"   - 切片: {sliced.shape}")
        
        return True
    except Exception as e:
        print(f"❌ 基本数组操作失败: {e}")
        traceback.print_exc()
        return False

def test_mathematical_operations(np):
    """测试数学运算功能"""
    print("\n=== 数学运算功能测试 ===")
    try:
        # 基本运算
        a = np.array([1, 2, 3, 4, 5])
        b = np.array([2, 3, 4, 5, 6])
        
        # 算术运算
        add_result = a + b
        sub_result = a - b
        mul_result = a * b
        div_result = a / b
        pow_result = a ** 2
        
        print(f"✅ 基本算术运算成功")
        print(f"   - 加法: {add_result}")
        print(f"   - 减法: {sub_result}")
        print(f"   - 乘法: {mul_result}")
        print(f"   - 除法: {div_result}")
        print(f"   - 幂运算: {pow_result}")
        
        # 统计函数
        data = np.random.randn(100)
        mean_val = np.mean(data)
        std_val = np.std(data)
        min_val = np.min(data)
        max_val = np.max(data)
        sum_val = np.sum(data)
        
        print(f"✅ 统计函数运算成功")
        print(f"   - 均值: {mean_val:.4f}")
        print(f"   - 标准差: {std_val:.4f}")
        print(f"   - 最小值: {min_val:.4f}")
        print(f"   - 最大值: {max_val:.4f}")
        print(f"   - 总和: {sum_val:.4f}")
        
        # 线性代数
        matrix_a = np.random.rand(3, 3)
        matrix_b = np.random.rand(3, 3)
        
        dot_product = np.dot(matrix_a, matrix_b)
        determinant = np.linalg.det(matrix_a)
        eigenvals = np.linalg.eigvals(matrix_a)
        
        print(f"✅ 线性代数运算成功")
        print(f"   - 矩阵乘法: {dot_product.shape}")
        print(f"   - 行列式: {determinant:.4f}")
        print(f"   - 特征值数量: {len(eigenvals)}")
        
        return True
    except Exception as e:
        print(f"❌ 数学运算功能失败: {e}")
        traceback.print_exc()
        return False

def test_data_types(np):
    """测试数据类型支持"""
    print("\n=== 数据类型支持测试 ===")
    try:
        # 测试各种数据类型
        dtypes_to_test = [
            np.int8, np.int16, np.int32, np.int64,
            np.uint8, np.uint16, np.uint32, np.uint64,
            np.float16, np.float32, np.float64,
            np.complex64, np.complex128,
            np.bool_, np.object_
        ]
        
        successful_dtypes = []
        failed_dtypes = []
        
        for dtype in dtypes_to_test:
            try:
                arr = np.array([1, 2, 3], dtype=dtype)
                successful_dtypes.append(dtype.__name__)
            except Exception as e:
                failed_dtypes.append((dtype.__name__, str(e)))
        
        print(f"✅ 支持的数据类型 ({len(successful_dtypes)})个):")
        for dtype_name in successful_dtypes:
            print(f"   - {dtype_name}")
            
        if failed_dtypes:
            print(f"❌ 不支持的数据类型 ({len(failed_dtypes)}个):")
            for dtype_name, error in failed_dtypes:
                print(f"   - {dtype_name}: {error}")
        
        # 测试类型转换
        int_arr = np.array([1, 2, 3], dtype=np.int32)
        float_arr = int_arr.astype(np.float64)
        bool_arr = int_arr.astype(np.bool_)
        
        print(f"✅ 类型转换成功")
        print(f"   - int32 -> float64: {float_arr.dtype}")
        print(f"   - int32 -> bool: {bool_arr.dtype}")
        
        return True
    except Exception as e:
        print(f"❌ 数据类型测试失败: {e}")
        traceback.print_exc()
        return False

def test_pandas_compatibility(np):
    """测试与pandas的兼容性"""
    print("\n=== Pandas兼容性测试 ===")
    try:
        import pandas as pd
        
        # 创建numpy数组
        np_array = np.random.randn(100, 4)
        np_dates = np.datetime64('2024-01-01') + np.arange(100)
        
        # 转换为pandas对象
        df = pd.DataFrame(np_array, columns=['A', 'B', 'C', 'D'])
        series = pd.Series(np_array[:, 0])
        date_index = pd.DatetimeIndex(np_dates)
        
        print(f"✅ NumPy到Pandas转换成功")
        print(f"   - DataFrame: {df.shape}")
        print(f"   - Series: {series.shape}")
        print(f"   - DatetimeIndex: {len(date_index)}")
        
        # 从pandas转回numpy
        back_to_numpy = df.values
        series_to_numpy = series.values
        
        print(f"✅ Pandas到NumPy转换成功")
        print(f"   - DataFrame.values: {back_to_numpy.shape}")
        print(f"   - Series.values: {series_to_numpy.shape}")
        
        # 测试数据一致性
        is_equal = np.allclose(np_array, back_to_numpy)
        print(f"✅ 数据一致性检查: {'通过' if is_equal else '失败'}")
        
        return True
    except Exception as e:
        print(f"❌ Pandas兼容性测试失败: {e}")
        traceback.print_exc()
        return False

def test_memory_performance(np):
    """测试内存管理和性能"""
    print("\n=== 内存管理和性能测试 ===")
    try:
        # 内存使用测试
        large_array = np.random.rand(1000, 1000)
        memory_usage = large_array.nbytes / (1024 * 1024)  # MB
        
        print(f"✅ 大数组创建成功")
        print(f"   - 数组大小: {large_array.shape}")
        print(f"   - 内存使用: {memory_usage:.2f} MB")
        
        # 性能测试
        start_time = time.time()
        result = np.dot(large_array, large_array.T)
        end_time = time.time()
        
        print(f"✅ 矩阵运算性能测试")
        print(f"   - 运算时间: {end_time - start_time:.4f} 秒")
        print(f"   - 结果形状: {result.shape}")
        
        # 内存清理
        del large_array, result
        gc.collect()
        
        print(f"✅ 内存清理完成")
        
        return True
    except Exception as e:
        print(f"❌ 内存管理和性能测试失败: {e}")
        traceback.print_exc()
        return False

def test_error_handling(np):
    """测试错误处理机制"""
    print("\n=== 错误处理机制测试 ===")
    try:
        error_cases = [
            ("除零错误", lambda: np.array([1, 2, 3]) / np.array([1, 0, 1])),
            ("形状不匹配", lambda: np.dot(np.array([[1, 2]]), np.array([1, 2, 3]))),
            ("索引越界", lambda: np.array([1, 2, 3])[10]),
            ("无效数据类型", lambda: np.array([1, 2, 3], dtype='invalid_type'))
        ]
        
        handled_errors = 0
        for error_name, error_func in error_cases:
            try:
                with np.errstate(divide='ignore', invalid='ignore'):
                    result = error_func()
                    if np.any(np.isnan(result)) or np.any(np.isinf(result)):
                        print(f"✅ {error_name}: 正确处理(产生NaN/Inf)")
                        handled_errors += 1
                    else:
                        print(f"⚠️  {error_name}: 未产生预期错误")
            except Exception as e:
                print(f"✅ {error_name}: 正确抛出异常 - {type(e).__name__}")
                handled_errors += 1
        
        print(f"✅ 错误处理测试完成: {handled_errors}/{len(error_cases)} 个错误被正确处理")
        
        return True
    except Exception as e:
        print(f"❌ 错误处理测试失败: {e}")
        traceback.print_exc()
        return False

def test_advanced_features(np):
    """测试高级功能"""
    print("\n=== 高级功能测试 ===")
    try:
        # 广播机制
        a = np.array([[1, 2, 3]])
        b = np.array([[1], [2], [3]])
        broadcast_result = a + b
        
        print(f"✅ 广播机制测试成功")
        print(f"   - 结果形状: {broadcast_result.shape}")
        
        # 掩码数组
        data = np.array([1, 2, -999, 4, 5])
        masked_array = np.ma.masked_where(data == -999, data)
        
        print(f"✅ 掩码数组测试成功")
        print(f"   - 掩码数量: {masked_array.mask.sum()}")
        
        # FFT变换
        signal = np.sin(2 * np.pi * np.arange(100) / 10)
        fft_result = np.fft.fft(signal)
        
        print(f"✅ FFT变换测试成功")
        print(f"   - 变换结果长度: {len(fft_result)}")
        
        # 随机数生成
        rng = np.random.default_rng(42)
        random_data = rng.normal(0, 1, 1000)
        
        print(f"✅ 随机数生成测试成功")
        print(f"   - 随机数据形状: {random_data.shape}")
        print(f"   - 均值: {np.mean(random_data):.4f}")
        
        return True
    except Exception as e:
        print(f"❌ 高级功能测试失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🔬 NumPy功能完备性和稳定性测试")
    print("=" * 50)
    
    # 测试结果统计
    test_results = {}
    
    # 1. 导入测试
    success, np_module = test_numpy_import()
    test_results['导入测试'] = success
    
    if not success:
        print("\n❌ NumPy导入失败，无法继续测试")
        return
    
    # 2. 基本数组操作测试
    test_results['基本数组操作'] = test_basic_array_operations(np_module)
    
    # 3. 数学运算功能测试
    test_results['数学运算功能'] = test_mathematical_operations(np_module)
    
    # 4. 数据类型支持测试
    test_results['数据类型支持'] = test_data_types(np_module)
    
    # 5. Pandas兼容性测试
    test_results['Pandas兼容性'] = test_pandas_compatibility(np_module)
    
    # 6. 内存管理和性能测试
    test_results['内存管理和性能'] = test_memory_performance(np_module)
    
    # 7. 错误处理机制测试
    test_results['错误处理机制'] = test_error_handling(np_module)
    
    # 8. 高级功能测试
    test_results['高级功能'] = test_advanced_features(np_module)
    
    # 输出测试总结
    print("\n" + "=" * 50)
    print("📊 测试结果总结")
    print("=" * 50)
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n总体结果: {passed_tests}/{total_tests} 项测试通过")
    
    if passed_tests == total_tests:
        print("🎉 所有测试通过！NumPy功能完备且稳定。")
    elif passed_tests >= total_tests * 0.8:
        print("⚠️  大部分测试通过，NumPy基本功能正常。")
    else:
        print("❌ 多项测试失败，NumPy可能存在问题。")
    
    return test_results

if __name__ == "__main__":
    main()