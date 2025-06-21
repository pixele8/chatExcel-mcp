#!/usr/bin/env python3
"""
最小化工具注册测试
验证 FastMCP 的基本工具注册机制
"""

from fastmcp import FastMCP

# 创建 FastMCP 实例
mcp = FastMCP("test_server")

print("🔍 最小化工具注册测试")
print("=" * 40)

# 1. 检查初始状态
print("\n📊 1. 初始状态检查:")
print(f"  MCP 实例: {type(mcp)}")
print(f"  MCP 名称: {getattr(mcp, 'name', 'Unknown')}")

# 检查可能的工具存储属性
attrs_to_check = ['_tools', 'tools', '_tool_registry', 'tool_registry', '_handlers', 'handlers']
for attr in attrs_to_check:
    if hasattr(mcp, attr):
        value = getattr(mcp, attr)
        print(f"  {attr}: {type(value)} - 长度: {len(value) if hasattr(value, '__len__') else 'N/A'}")

# 2. 注册一个简单工具
print("\n🔧 2. 注册测试工具:")

try:
    @mcp.tool()
    def simple_test_tool(message: str) -> str:
        """简单的测试工具"""
        return f"收到消息: {message}"
    
    print("  ✅ 工具注册成功")
except Exception as e:
    print(f"  ❌ 工具注册失败: {e}")
    import traceback
    traceback.print_exc()

# 3. 检查注册后状态
print("\n📊 3. 注册后状态检查:")
for attr in attrs_to_check:
    if hasattr(mcp, attr):
        value = getattr(mcp, attr)
        length = len(value) if hasattr(value, '__len__') else 'N/A'
        print(f"  {attr}: {type(value)} - 长度: {length}")
        
        # 如果是字典类型，显示键
        if hasattr(value, 'keys') and len(value) > 0:
            print(f"    键: {list(value.keys())}")

# 4. 尝试多种注册方式
print("\n🧪 4. 多种注册方式测试:")

# 方式1: 带参数的装饰器
try:
    @mcp.tool(name="custom_tool", description="自定义工具")
    def custom_tool(data: str) -> dict:
        """自定义工具"""
        return {"result": f"处理了: {data}"}
    
    print("  ✅ 带参数装饰器注册成功")
except Exception as e:
    print(f"  ❌ 带参数装饰器注册失败: {e}")

# 方式2: 手动调用装饰器
try:
    def manual_tool(input_data: str) -> str:
        """手动注册的工具"""
        return f"手动处理: {input_data}"
    
    # 手动应用装饰器
    manual_tool = mcp.tool()(manual_tool)
    print("  ✅ 手动装饰器应用成功")
except Exception as e:
    print(f"  ❌ 手动装饰器应用失败: {e}")

# 5. 最终状态检查
print("\n📊 5. 最终状态检查:")
total_tools = 0
for attr in attrs_to_check:
    if hasattr(mcp, attr):
        value = getattr(mcp, attr)
        length = len(value) if hasattr(value, '__len__') else 0
        total_tools = max(total_tools, length)
        print(f"  {attr}: 长度 {length}")

print(f"\n🎯 总结: 成功注册 {total_tools} 个工具")

# 6. 检查 FastMCP 内部机制
print("\n🔍 6. FastMCP 内部机制检查:")

# 检查是否有 server 属性
if hasattr(mcp, 'server'):
    server = getattr(mcp, 'server')
    print(f"  server 属性: {type(server)}")
    print(f"  server 属性列表: {[attr for attr in dir(server) if not attr.startswith('_')][:10]}")
else:
    print("  ❌ 未找到 server 属性")

# 检查是否有 app 属性
if hasattr(mcp, 'app'):
    app = getattr(mcp, 'app')
    print(f"  app 属性: {type(app)}")
else:
    print("  ❌ 未找到 app 属性")

print("\n" + "=" * 40)
print("🏁 测试完成")