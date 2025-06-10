"""服务器功能测试"""
import pytest
import pandas as pd
import os
import tempfile
from server import (
    read_metadata, run_code, bar_chart_to_html, 
    create_error_response, create_success_response,
    validate_file_access
)

class TestChatExcelServer:
    """chatExcel服务器测试类"""
    
    @pytest.fixture
    def sample_csv(self):
        """创建测试用CSV文件"""
        # 创建临时文件但不自动删除
        fd, temp_path = tempfile.mkstemp(suffix='.csv')
        try:
            # 写入测试数据
            with os.fdopen(fd, 'w') as f:
                f.write("name,age,city\n")
                f.write("Alice,25,New York\n")
                f.write("Bob,30,London\n")
                f.write("Charlie,35,Tokyo\n")
            # 确保文件完全写入
            yield temp_path
        finally:
            # 清理临时文件
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_read_metadata_success(self, sample_csv):
        """测试成功读取元数据"""
        result = read_metadata(sample_csv)
        print(f"Debug - read_metadata result: {result}")  # 调试输出
        assert result["status"] == "SUCCESS"
        assert "dataset" in result
        assert result["dataset"]["rows"] == 3
        assert result["dataset"]["columns"] == 3
    
    def test_read_metadata_file_not_found(self):
        """测试文件不存在的情况"""
        result = read_metadata("/nonexistent/file.csv")
        assert result["status"] == "ERROR"
        assert result["error_type"] == "FILE_NOT_FOUND"
    
    def test_run_code_success(self, sample_csv):
        """测试成功执行代码"""
        code = "result = df.shape[0]"
        result = run_code(code, sample_csv)
        print(f"Debug - run_code result: {result}")  # 调试输出
        assert result["success"] is True
        assert result["result"]["value"] == "3"
    
    def test_run_code_security_violation(self, sample_csv):
        """测试安全违规检测"""
        code = "import os; result = os.listdir('.')"
        result = run_code(code, sample_csv)
        assert result["success"] is False
        assert "Forbidden operation" in result["error"]
    
    def test_bar_chart_generation(self):
        """测试柱状图生成"""
        result = bar_chart_to_html(
            categories=['A', 'B', 'C'],
            values=[1, 2, 3],
            title="测试图表"
        )
        assert result["status"] == "SUCCESS"
        assert os.path.exists(result["filepath"])
        
        # 清理生成的文件
        os.unlink(result["filepath"])
    
    def test_error_response_creation(self):
        """测试错误响应创建"""
        error = create_error_response(
            "TEST_ERROR", 
            "测试错误", 
            details={"key": "value"},
            solutions=["解决方案1"]
        )
        assert error["status"] == "ERROR"
        assert error["error_type"] == "TEST_ERROR"
        assert error["message"] == "测试错误"
        assert "timestamp" in error