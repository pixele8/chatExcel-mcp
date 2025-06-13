# MCP Excel服务修复记录

## 问题描述

在测试MCP Excel服务时遇到了503 Service Unavailable错误，导致Python客户端无法正常访问Go服务的健康检查接口。

## 问题分析

### 1. 初始症状
- Python `requests` 库访问 `http://localhost:8080/api/v1/health` 返回503错误
- `curl` 命令可以正常访问同一接口并返回200状态码
- Go服务日志显示正常启动并监听8080端口

### 2. 根本原因
通过系统代理检查发现：
```bash
scutil --proxy
```
显示系统配置了HTTP代理：
- HTTPProxy: 127.0.0.1:15236
- HTTPSProxy: 127.0.0.1:15236
- SOCKSProxy: 127.0.0.1:15235

Python `requests` 库默认使用系统代理设置，导致本地服务访问被代理拦截，而 `curl` 可能绕过了代理或有不同的代理处理机制。

## 解决方案

### 1. 修复ExcelGoClient代理问题
在 `excel_go_client.py` 的 `_make_request` 方法中添加代理绕过设置：

```python
def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict[str, Any]:
    """发送 HTTP 请求"""
    url = f"{self.api_base}/{endpoint.lstrip('/')}"
    
    # 绕过系统代理设置，直接访问本地服务
    proxies = {
        'http': None,
        'https': None
    }
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params, timeout=30, proxies=proxies)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=30, proxies=proxies)
        # ...
```

### 2. 修复数据格式问题
发现Go服务期望的数据格式与Python客户端发送的格式不匹配：
- Go服务期望：`[]map[string]string` (字典数组)
- 原测试数据：二维数组格式

修复后的测试数据格式：
```python
test_data = [
    {"姓名": "张三", "年龄": "25", "城市": "北京", "薪资": "8000"},
    {"姓名": "李四", "年龄": "30", "城市": "上海", "薪资": "12000"},
    # ...
]
```

### 3. 修复图表创建参数
调整图表创建调用，使用正确的参数格式：
```python
chart_result = client.create_chart(
    file_path=test_file,
    chart_type="col",  # 柱状图
    data_range="A1:D5",  # 数据范围
    sheet_name="员工信息",
    title="员工薪资对比",
    x_axis_title="员工",
    y_axis_title="薪资(元)"
)
```

## 验证结果

运行完整功能测试 `test_mcp_complete.py`，所有功能正常：

✅ 健康检查通过  
✅ Excel写入成功  
✅ Excel读取成功  
✅ 文件信息获取成功  
✅ 图表生成成功  

## 经验总结

1. **代理问题排查**：在本地开发环境中，系统代理设置可能影响本地服务访问，需要在HTTP客户端中显式绕过代理

2. **数据格式对齐**：确保前后端数据格式严格匹配，特别是结构化数据的传输

3. **分层测试**：使用不同工具（curl vs requests）进行对比测试，有助于快速定位问题层级

4. **完整性验证**：修复后进行端到端的完整功能测试，确保所有组件协同工作

## 文件修改清单

- `excel_go_client.py`: 添加代理绕过设置
- `test_mcp_complete.py`: 修复数据格式和API调用参数
- `record.md`: 新增问题记录和解决方案文档

---

**修复时间**: 2025年6月13日  
**状态**: 已完成，服务正常运行