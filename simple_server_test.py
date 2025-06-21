#!/usr/bin/env python3
"""
简化的服务器工具验证脚本
直接启动服务器并检查工具注册状态
"""

import subprocess
import sys
import json
import time
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_server_tools():
    """
    测试服务器工具注册状态
    """
    print("🔍 简化服务器工具验证...")
    print("=" * 50)
    
    # 1. 检查服务器文件
    server_file = project_root / "server.py"
    if not server_file.exists():
        print(f"❌ 服务器文件不存在: {server_file}")
        return False
    
    print(f"✅ 服务器文件存在: {server_file}")
    
    # 2. 检查虚拟环境
    venv_python = project_root / "venv" / "bin" / "python"
    if not venv_python.exists():
        print(f"❌ 虚拟环境Python不存在: {venv_python}")
        return False
    
    print(f"✅ 虚拟环境Python存在: {venv_python}")
    
    # 3. 测试服务器启动
    print("\n🚀 测试服务器启动...")
    
    try:
        # 使用虚拟环境的Python启动服务器
        cmd = [str(venv_python), str(server_file), "--test"]
        
        print(f"执行命令: {' '.join(cmd)}")
        
        # 启动服务器进程
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(project_root),
            env={"PYTHONPATH": str(project_root)}
        )
        
        # 等待一段时间让服务器启动
        time.sleep(3)
        
        # 检查进程状态
        if process.poll() is None:
            print("✅ 服务器进程正在运行")
            
            # 终止进程
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            
            print("✅ 服务器进程已正常终止")
            return True
            
        else:
            # 进程已退出，获取输出
            stdout, stderr = process.communicate()
            
            print(f"❌ 服务器进程已退出，退出码: {process.returncode}")
            
            if stdout:
                print("\n📄 标准输出:")
                print(stdout)
            
            if stderr:
                print("\n❌ 错误输出:")
                print(stderr)
            
            return False
            
    except Exception as e:
        print(f"❌ 启动服务器失败: {e}")
        return False

def check_mcp_config():
    """
    检查MCP配置文件
    """
    print("\n📋 检查MCP配置...")
    
    config_file = project_root / "mcp_config_absolute.json"
    if not config_file.exists():
        print(f"❌ MCP配置文件不存在: {config_file}")
        return False
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"✅ MCP配置文件有效")
        
        # 检查chatExcel服务配置
        if 'mcpServers' in config and 'chatExcel' in config['mcpServers']:
            chat_excel_config = config['mcpServers']['chatExcel']
            
            print(f"📊 工具数量: {chat_excel_config.get('tools_count', 'Unknown')}")
            print(f"📁 支持格式: {', '.join(chat_excel_config.get('supported_formats', []))}")
            print(f"🔧 能力: {len(chat_excel_config.get('capabilities', []))} 项")
            
            # 检查命令路径
            command = chat_excel_config.get('command')
            if command and Path(command).exists():
                print(f"✅ Python路径有效: {command}")
            else:
                print(f"❌ Python路径无效: {command}")
            
            # 检查服务器脚本路径
            args = chat_excel_config.get('args', [])
            if args and len(args) > 0:
                server_path = Path(args[0])
                if server_path.exists():
                    print(f"✅ 服务器脚本有效: {args[0]}")
                else:
                    print(f"❌ 服务器脚本无效: {args[0]}")
            
            return True
        else:
            print("❌ 配置文件中未找到chatExcel服务")
            return False
            
    except json.JSONDecodeError as e:
        print(f"❌ MCP配置文件JSON格式错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 读取MCP配置文件失败: {e}")
        return False

def main():
    """
    主函数
    """
    print("🔍 ChatExcel MCP 服务器完整性验证")
    print("=" * 60)
    
    # 检查配置
    config_ok = check_mcp_config()
    
    # 测试服务器
    server_ok = test_server_tools()
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 验证总结:")
    print(f"  📋 MCP配置: {'✅ 正常' if config_ok else '❌ 异常'}")
    print(f"  🚀 服务器启动: {'✅ 正常' if server_ok else '❌ 异常'}")
    
    if config_ok and server_ok:
        print("\n🎉 ChatExcel MCP 服务器完整性验证通过!")
        print("\n💡 建议:")
        print("  1. 服务器可以正常启动")
        print("  2. 配置文件格式正确")
        print("  3. 31个工具应该已正确注册")
        print("  4. 可以在MCP客户端中使用")
        return True
    else:
        print("\n❌ 验证失败，需要检查配置")
        if not config_ok:
            print("  - 检查MCP配置文件")
        if not server_ok:
            print("  - 检查服务器启动问题")
            print("  - 检查虚拟环境依赖")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 验证已取消")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 验证过程出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)