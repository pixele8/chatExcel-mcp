#!/usr/bin/env python3
"""
测试行数统计逻辑的脚本
"""

import pandas as pd
import os

def test_row_count_logic():
    """测试行数统计逻辑"""
    print("Testing row count logic...")
    
    # 创建测试数据
    df = pd.DataFrame({
        'A': range(150), 
        'B': range(150, 300),
        'C': ['test'] * 150
    })
    
    test_file = 'test_data.csv'
    df.to_csv(test_file, index=False)
    print(f"Created test file with {len(df)} rows")
    
    # 方法1：通过文件行数统计（不包括header）
    with open(test_file, 'r') as f:
        total_lines = sum(1 for _ in f) - 1  # 减去header行
    print(f"File line count (excluding header): {total_lines}")
    
    # 方法2：使用pandas读取样本数据
    sample_df = pd.read_csv(test_file, nrows=100)
    print(f"Sample rows loaded: {len(sample_df)}")
    
    # 方法3：使用pandas获取总行数（高效方式）
    # 注意：usecols=[] 在某些pandas版本中可能返回0行，改用读取第一列
    total_df = pd.read_csv(test_file, usecols=[0])
    print(f"Total rows via pandas (usecols=[0]): {len(total_df)}")
    
    # 验证结果
    assert total_lines == 150, f"Expected 150 rows, got {total_lines}"
    assert len(sample_df) == 100, f"Expected 100 sample rows, got {len(sample_df)}"
    assert len(total_df) == 150, f"Expected 150 total rows, got {len(total_df)}"
    
    # 清理
    os.remove(test_file)
    print("✅ All tests passed! Row count logic is working correctly.")
    
    return {
        'total_rows': total_lines,
        'sample_rows': len(sample_df)
    }

if __name__ == '__main__':
    result = test_row_count_logic()
    print(f"\nResult: {result}")