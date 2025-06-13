from server import read_metadata

import os

# 使用相对路径或创建测试数据
file_path = os.path.join(os.path.dirname(__file__), 'test_data.csv')

# 或者使用用户主目录
file_path = os.path.expanduser('~/Desktop/test_file.csv')

# 或者检查文件是否存在
test_files = [
    'test_data.csv',
    os.path.expanduser('~/Desktop/DO280 21 April.csv'),
    '/path/to/sample/file.csv'
]

for file_path in test_files:
    if os.path.exists(file_path):
        break
else:
    print("No test file found, creating sample data...")
    # 创建示例数据进行测试

print("Reading metadata from file:", read_metadata(file_path))