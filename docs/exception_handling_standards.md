# 异常处理标准化文档

## 概述

本文档定义了 ChatExcel MCP 项目中异常处理的标准化规范，确保代码的一致性、可维护性和调试友好性。

## 异常层次结构

### 基础异常类

```python
ChatExcelError(Exception)
├── FileAccessError          # 文件访问异常
├── CodeExecutionError       # 代码执行异常
├── ValidationError          # 参数验证异常
├── SecurityError           # 安全异常
├── ConfigurationError      # 配置异常
├── DataProcessingError     # 数据处理异常
├── ResourceError           # 资源异常
├── TimeoutError           # 超时异常
├── CacheError             # 缓存异常
├── ServiceUnavailableError # 服务不可用异常
├── ExecutionError         # 执行异常
├── HealthCheckError       # 健康检查异常
├── PerformanceError       # 性能异常
├── SystemMonitorError     # 系统监控异常
└── AlertError             # 告警异常
```

## 异常使用规范

### 1. 异常选择原则

- **具体性原则**: 优先使用最具体的异常类型
- **语义清晰**: 异常类型应该清楚表达错误的性质
- **层次合理**: 遵循异常继承层次，不要跨层使用

### 2. 异常创建规范

#### FileAccessError
```python
# ✅ 正确用法
raise FileAccessError(
    file_path="/path/to/file.xlsx",
    reason="文件不存在"
)

# ❌ 错误用法
raise FileAccessError("文件访问失败")  # 缺少必需参数
```

#### CodeExecutionError
```python
# ✅ 正确用法
raise CodeExecutionError(
    code="df.groupby('column').sum()",
    error_details="列 'column' 不存在"
)

# ❌ 错误用法
raise CodeExecutionError("代码执行失败")  # 缺少必需参数
```

#### DataProcessingError
```python
# ✅ 正确用法
raise DataProcessingError(
    operation="数据清洗",
    data_info="100行3列数据",
    error_details="发现50%缺失值"
)

# ❌ 错误用法
raise DataProcessingError(
    message="数据处理失败",  # 错误的参数名
    data_info="数据信息",
    error_details="错误详情"
)
```

### 3. 异常处理模式

#### 模式1: 捕获并重新抛出
```python
try:
    # 执行可能失败的操作
    result = risky_operation()
except FileNotFoundError as e:
    raise FileAccessError(
        file_path=file_path,
        reason=f"文件不存在: {str(e)}"
    ) from e
except PermissionError as e:
    raise FileAccessError(
        file_path=file_path,
        reason=f"权限不足: {str(e)}"
    ) from e
```

#### 模式2: 验证并抛出
```python
def validate_parameters(data: dict):
    """参数验证"""
    if not isinstance(data, dict):
        raise ValidationError(
            parameter="data",
            value=type(data).__name__,
            expected="字典类型"
        )
    
    if "required_field" not in data:
        raise ValidationError(
            parameter="required_field",
            value="缺失",
            expected="必需字段"
        )
```

#### 模式3: 资源管理异常
```python
def check_memory_usage():
    """检查内存使用"""
    current_memory = get_memory_usage()
    memory_limit = get_memory_limit()
    
    if current_memory > memory_limit:
        raise ResourceError(
            resource_type="内存",
            limit=f"{memory_limit}MB",
            current=f"{current_memory}MB"
        )
```

### 4. 异常信息规范

#### 消息格式
- **中文消息**: 面向用户的错误信息使用中文
- **结构化**: 包含足够的上下文信息
- **可操作**: 提供明确的解决建议

#### 详细信息
- **details**: 包含结构化的错误详情
- **suggestions**: 提供具体的解决建议
- **error_code**: 使用一致的错误代码

### 5. 异常传播规范

#### 服务层异常处理
```python
class ExcelService:
    def process_file(self, file_path: str):
        try:
            # 文件访问
            if not os.path.exists(file_path):
                raise FileAccessError(
                    file_path=file_path,
                    reason="文件不存在"
                )
            
            # 数据处理
            data = self._load_data(file_path)
            result = self._process_data(data)
            return result
            
        except FileAccessError:
            # 直接传播文件访问异常
            raise
        except Exception as e:
            # 包装未预期的异常
            raise DataProcessingError(
                operation="文件处理",
                data_info=f"文件: {file_path}",
                error_details=str(e)
            ) from e
```

#### API层异常处理
```python
@app.exception_handler(ChatExcelError)
async def chatexcel_exception_handler(request: Request, exc: ChatExcelError):
    """统一异常处理"""
    return JSONResponse(
        status_code=400,
        content=exc.to_dict()
    )
```

## 异常测试规范

### 1. 异常创建测试
```python
def test_file_access_error_creation():
    """测试文件访问异常创建"""
    error = FileAccessError("/path/to/file", "文件不存在")
    assert error.file_path == "/path/to/file"
    assert error.reason == "文件不存在"
    assert "文件访问失败" in error.message
    assert len(error.suggestions) > 0
```

### 2. 异常传播测试
```python
def test_exception_propagation():
    """测试异常传播"""
    with pytest.raises(FileAccessError) as exc_info:
        service.process_nonexistent_file("/nonexistent/file.xlsx")
    
    error = exc_info.value
    assert error.file_path == "/nonexistent/file.xlsx"
    assert "不存在" in error.reason
```

### 3. 异常序列化测试
```python
def test_exception_serialization():
    """测试异常序列化"""
    error = ValidationError("age", -1, "正整数")
    result = error.to_dict()
    
    assert result["error"] == "ValidationError"
    assert result["message"] == "参数验证失败: age = -1, 期望: 正整数"
    assert "parameter" in result["details"]
    assert len(result["suggestions"]) > 0
```

## 日志记录规范

### 1. 异常日志格式
```python
import structlog

logger = structlog.get_logger()

try:
    # 执行操作
    pass
except ChatExcelError as e:
    logger.error(
        "业务异常",
        exception_type=type(e).__name__,
        error_code=e.error_code,
        message=e.message,
        details=e.details,
        suggestions=e.suggestions
    )
    raise
except Exception as e:
    logger.exception(
        "未预期异常",
        exception_type=type(e).__name__,
        message=str(e)
    )
    raise
```

### 2. 性能监控
```python
def monitor_exceptions():
    """异常监控"""
    # 统计异常频率
    # 分析异常模式
    # 生成告警
    pass
```

## 最佳实践

### 1. 异常设计原则
- **单一职责**: 每个异常类只处理一种错误类型
- **信息完整**: 包含足够的调试信息
- **用户友好**: 提供清晰的错误描述和解决建议
- **可测试**: 异常行为应该可以被测试

### 2. 性能考虑
- **避免异常滥用**: 不要用异常控制正常流程
- **异常缓存**: 对于频繁的异常，考虑缓存异常对象
- **堆栈优化**: 在性能敏感场景下，考虑禁用堆栈跟踪

### 3. 安全考虑
- **信息泄露**: 不要在异常消息中包含敏感信息
- **输入验证**: 异常参数也需要验证
- **日志安全**: 确保异常日志不包含敏感数据

### 4. 维护性考虑
- **版本兼容**: 异常接口变更要考虑向后兼容
- **文档同步**: 异常变更要同步更新文档
- **测试覆盖**: 确保异常路径有足够的测试覆盖

## 代码审查清单

### 异常使用检查
- [ ] 是否使用了正确的异常类型？
- [ ] 异常参数是否完整和正确？
- [ ] 异常消息是否清晰和有用？
- [ ] 是否提供了解决建议？
- [ ] 是否正确使用了异常链（from e）？

### 异常处理检查
- [ ] 是否捕获了正确的异常类型？
- [ ] 异常处理逻辑是否合理？
- [ ] 是否有适当的日志记录？
- [ ] 是否有资源清理逻辑？
- [ ] 异常传播是否正确？

### 测试覆盖检查
- [ ] 是否测试了异常创建？
- [ ] 是否测试了异常传播？
- [ ] 是否测试了异常处理逻辑？
- [ ] 是否测试了边界条件？
- [ ] 是否测试了异常序列化？

## 工具支持

### 1. 静态分析
- 使用 `mypy` 检查异常类型注解
- 使用 `flake8` 检查异常处理风格
- 使用 `bandit` 检查异常安全问题

### 2. 动态分析
- 使用 `pytest` 测试异常行为
- 使用覆盖率工具检查异常路径覆盖
- 使用性能分析工具监控异常开销

### 3. 监控告警
- 异常频率监控
- 异常类型分布分析
- 异常响应时间监控
- 异常恢复成功率统计

---

**版本**: 1.0  
**更新日期**: 2024-12-20  
**维护者**: ChatExcel Team