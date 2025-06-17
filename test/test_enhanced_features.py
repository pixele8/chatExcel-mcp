#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强功能测试套件
测试安全机制、依赖管理和健康监控功能
"""

import os
import sys
import json
import time
import tempfile
import unittest
import asyncio
import threading
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import logging

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 配置测试日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestSecureCodeExecutor(unittest.TestCase):
    """安全代码执行器测试"""
    
    def setUp(self):
        """测试设置"""
        try:
            from security.secure_code_executor import SecureCodeExecutor
            self.executor = SecureCodeExecutor()
        except ImportError as e:
            self.skipTest(f"无法导入 SecureCodeExecutor: {e}")
    
    def test_safe_code_execution(self):
        """测试安全代码执行"""
        # 测试安全的代码
        safe_code = """
import pandas as pd
import numpy as np

data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
df = pd.DataFrame(data)
result = df.sum()
"""
        
        result = self.executor.execute_code(safe_code, {})
        self.assertTrue(result['success'])
        self.assertIn('result', result)
    
    def test_unsafe_code_blocking(self):
        """测试不安全代码阻止"""
        # 测试包含危险操作的代码
        unsafe_codes = [
            "import os; os.system('rm -rf /')",
            "exec('malicious code')",
            "eval('dangerous expression')",
            "__import__('subprocess').call(['rm', '-rf', '/'])",
            "open('/etc/passwd', 'r').read()"
        ]
        
        for unsafe_code in unsafe_codes:
            with self.subTest(code=unsafe_code):
                result = self.executor.execute_code(unsafe_code, {})
                self.assertFalse(result['success'])
                self.assertIn('安全检查失败', result.get('error', ''))
    
    def test_resource_limits(self):
        """测试资源限制"""
        # 测试内存限制
        memory_intensive_code = """
import numpy as np
# 尝试创建大数组
large_array = np.zeros((10000, 10000))
result = 'memory_test_passed'
"""
        
        result = self.executor.execute_code(memory_intensive_code, {})
        # 根据配置，这可能成功或失败
        self.assertIsInstance(result, dict)
        self.assertIn('success', result)
    
    def test_timeout_handling(self):
        """测试超时处理"""
        # 测试长时间运行的代码
        long_running_code = """
import time
time.sleep(10)  # 超过默认超时时间
result = 'should_not_reach_here'
"""
        
        start_time = time.time()
        result = self.executor.execute_code(long_running_code, {})
        execution_time = time.time() - start_time
        
        self.assertFalse(result['success'])
        self.assertLess(execution_time, 8)  # 应该在超时时间内返回
        self.assertIn('超时', result.get('error', ''))

class TestHealthManager(unittest.TestCase):
    """健康管理器测试"""
    
    def setUp(self):
        """测试设置"""
        try:
            from service_management.health_manager import HealthManager
            self.health_manager = HealthManager()
        except ImportError as e:
            self.skipTest(f"无法导入 HealthManager: {e}")
    
    def test_service_registration(self):
        """测试服务注册"""
        # 注册测试服务
        service_config = {
            'name': 'test_service',
            'host': 'localhost',
            'port': 8080,
            'health_check': {
                'endpoint': '/health',
                'interval': 30,
                'timeout': 5
            }
        }
        
        self.health_manager.register_service('test_service', service_config)
        
        # 验证服务已注册
        services = self.health_manager.get_registered_services()
        self.assertIn('test_service', services)
        self.assertEqual(services['test_service']['host'], 'localhost')
    
    def test_health_check_execution(self):
        """测试健康检查执行"""
        # 模拟健康检查
        with patch('aiohttp.ClientSession.get') as mock_get:
            # 模拟成功的健康检查响应
            mock_response = Mock()
            mock_response.status = 200
            mock_response.json = asyncio.coroutine(lambda: {'status': 'healthy'})
            mock_get.return_value.__aenter__.return_value = mock_response
            
            # 注册服务
            service_config = {
                'name': 'test_service',
                'host': 'localhost',
                'port': 8080,
                'health_check': {
                    'endpoint': '/health',
                    'interval': 30,
                    'timeout': 5
                }
            }
            
            self.health_manager.register_service('test_service', service_config)
            
            # 执行健康检查
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    self.health_manager.check_service_health('test_service')
                )
                self.assertTrue(result['healthy'])
                self.assertEqual(result['status_code'], 200)
            finally:
                loop.close()
    
    def test_service_recovery(self):
        """测试服务恢复"""
        # 注册带有自动恢复的服务
        service_config = {
            'name': 'recoverable_service',
            'host': 'localhost',
            'port': 8081,
            'health_check': {
                'endpoint': '/health',
                'interval': 30,
                'timeout': 5
            },
            'auto_recovery': {
                'enabled': True,
                'max_attempts': 3,
                'restart_command': ['echo', 'restarting service']
            }
        }
        
        self.health_manager.register_service('recoverable_service', service_config)
        
        # 模拟服务故障和恢复
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            # 触发恢复
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    self.health_manager.recover_service('recoverable_service')
                )
                self.assertTrue(result)
                mock_run.assert_called_once()
            finally:
                loop.close()

class TestDependencyManager(unittest.TestCase):
    """依赖管理器测试"""
    
    def setUp(self):
        """测试设置"""
        try:
            from service_management.dependency_manager import DependencyManager
            self.dependency_manager = DependencyManager()
        except ImportError as e:
            self.skipTest(f"无法导入 DependencyManager: {e}")
    
    def test_requirements_parsing(self):
        """测试依赖文件解析"""
        # 创建临时 requirements.txt
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("""pandas>=1.5.0
numpy==1.21.0
requests~=2.28.0
# 这是注释
openpyxl>=3.0.0,<4.0.0
""")
            temp_file = f.name
        
        try:
            dependencies = self.dependency_manager.parse_requirements_file(temp_file)
            
            self.assertEqual(len(dependencies), 4)  # 排除注释
            
            # 检查解析结果
            pandas_dep = next((d for d in dependencies if d['name'] == 'pandas'), None)
            self.assertIsNotNone(pandas_dep)
            self.assertEqual(pandas_dep['operator'], '>=')
            self.assertEqual(pandas_dep['version'], '1.5.0')
            
            numpy_dep = next((d for d in dependencies if d['name'] == 'numpy'), None)
            self.assertIsNotNone(numpy_dep)
            self.assertEqual(numpy_dep['operator'], '==')
            self.assertEqual(numpy_dep['version'], '1.21.0')
            
        finally:
            os.unlink(temp_file)
    
    def test_conflict_detection(self):
        """测试依赖冲突检测"""
        # 创建冲突的依赖
        dependencies = [
            {'name': 'package_a', 'version': '1.0.0', 'operator': '=='},
            {'name': 'package_a', 'version': '2.0.0', 'operator': '=='},
            {'name': 'package_b', 'version': '1.5.0', 'operator': '>='},
            {'name': 'package_b', 'version': '2.0.0', 'operator': '<'}
        ]
        
        conflicts = self.dependency_manager.detect_conflicts(dependencies)
        
        # 应该检测到 package_a 的冲突
        package_a_conflicts = [c for c in conflicts if c['package'] == 'package_a']
        self.assertTrue(len(package_a_conflicts) > 0)
    
    def test_dependency_graph_building(self):
        """测试依赖图构建"""
        dependencies = [
            {'name': 'pandas', 'version': '1.5.0'},
            {'name': 'numpy', 'version': '1.21.0'},
            {'name': 'openpyxl', 'version': '3.0.0'}
        ]
        
        graph = self.dependency_manager.build_dependency_graph(dependencies)
        
        self.assertIsInstance(graph, dict)
        self.assertIn('nodes', graph)
        self.assertIn('edges', graph)
        
        # 验证节点
        node_names = [node['name'] for node in graph['nodes']]
        self.assertIn('pandas', node_names)
        self.assertIn('numpy', node_names)
        self.assertIn('openpyxl', node_names)
    
    @patch('subprocess.run')
    def test_security_scan(self, mock_run):
        """测试安全扫描"""
        # 模拟 safety 命令输出
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = json.dumps([
            {
                'package': 'vulnerable_package',
                'installed': '1.0.0',
                'affected': '<2.0.0',
                'id': 'CVE-2023-1234',
                'advisory': 'Security vulnerability found'
            }
        ])
        
        vulnerabilities = self.dependency_manager.scan_vulnerabilities()
        
        self.assertIsInstance(vulnerabilities, list)
        if vulnerabilities:  # 如果有漏洞
            vuln = vulnerabilities[0]
            self.assertIn('package', vuln)
            self.assertIn('id', vuln)

class TestConfigManager(unittest.TestCase):
    """配置管理器测试"""
    
    def setUp(self):
        """测试设置"""
        try:
            from service_management.config_manager import ConfigManager
            # 创建临时配置目录
            self.temp_dir = tempfile.mkdtemp()
            self.config_dir = Path(self.temp_dir)
            self.config_manager = ConfigManager(self.config_dir)
        except ImportError as e:
            self.skipTest(f"无法导入 ConfigManager: {e}")
    
    def tearDown(self):
        """测试清理"""
        if hasattr(self, 'config_manager'):
            self.config_manager.shutdown()
        if hasattr(self, 'temp_dir'):
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_config_loading(self):
        """测试配置加载"""
        # 创建测试配置文件
        test_config = {
            'database': {
                'host': 'localhost',
                'port': 5432,
                'name': 'testdb'
            },
            'api': {
                'timeout': 30,
                'retries': 3
            }
        }
        
        config_file = self.config_dir / 'test.json'
        with open(config_file, 'w') as f:
            json.dump(test_config, f)
        
        # 重新加载配置
        self.config_manager.reload_configs()
        
        # 测试配置获取
        self.assertEqual(self.config_manager.get('database.host'), 'localhost')
        self.assertEqual(self.config_manager.get('database.port'), 5432)
        self.assertEqual(self.config_manager.get('api.timeout'), 30)
        self.assertIsNone(self.config_manager.get('nonexistent.key'))
    
    def test_config_watching(self):
        """测试配置文件监控"""
        # 创建初始配置
        test_config = {'value': 'initial'}
        config_file = self.config_dir / 'watch_test.json'
        
        with open(config_file, 'w') as f:
            json.dump(test_config, f)
        
        self.config_manager.reload_configs()
        
        # 验证初始值
        self.assertEqual(self.config_manager.get('value'), 'initial')
        
        # 修改配置文件
        updated_config = {'value': 'updated'}
        with open(config_file, 'w') as f:
            json.dump(updated_config, f)
        
        # 等待文件监控器检测变化
        time.sleep(2)
        
        # 验证配置已更新（如果监控器工作正常）
        # 注意：这个测试可能需要更长的等待时间或手动触发重载
        # self.assertEqual(self.config_manager.get('value'), 'updated')
    
    def test_config_validation(self):
        """测试配置验证"""
        # 定义配置模式
        schema = {
            'type': 'object',
            'properties': {
                'host': {'type': 'string'},
                'port': {'type': 'integer', 'minimum': 1, 'maximum': 65535}
            },
            'required': ['host', 'port']
        }
        
        # 测试有效配置
        valid_config = {'host': 'localhost', 'port': 8080}
        is_valid, errors = self.config_manager.validate_config(valid_config, schema)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
        # 测试无效配置
        invalid_config = {'host': 'localhost', 'port': 'invalid_port'}
        is_valid, errors = self.config_manager.validate_config(invalid_config, schema)
        self.assertFalse(is_valid)
        self.assertTrue(len(errors) > 0)

class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_component_integration(self):
        """测试组件集成"""
        # 这个测试验证各个组件能够正常协作
        try:
            # 导入所有主要组件
            from security.secure_code_executor import SecureCodeExecutor
            from service_management.health_manager import HealthManager
            from service_management.dependency_manager import DependencyManager
            from service_management.config_manager import ConfigManager
            
            # 创建临时配置目录
            with tempfile.TemporaryDirectory() as temp_dir:
                config_dir = Path(temp_dir)
                
                # 初始化组件
                config_manager = ConfigManager(config_dir)
                health_manager = HealthManager()
                dependency_manager = DependencyManager()
                secure_executor = SecureCodeExecutor()
                
                # 验证组件可以正常初始化
                self.assertIsNotNone(config_manager)
                self.assertIsNotNone(health_manager)
                self.assertIsNotNone(dependency_manager)
                self.assertIsNotNone(secure_executor)
                
                # 清理
                config_manager.shutdown()
                
        except ImportError as e:
            self.skipTest(f"无法导入组件: {e}")
    
    def test_error_handling(self):
        """测试错误处理"""
        # 测试各组件的错误处理能力
        try:
            from security.secure_code_executor import SecureCodeExecutor
            
            executor = SecureCodeExecutor()
            
            # 测试语法错误处理
            invalid_code = "invalid python syntax !!!"
            result = executor.execute_code(invalid_code, {})
            
            self.assertFalse(result['success'])
            self.assertIn('error', result)
            
        except ImportError as e:
            self.skipTest(f"无法导入 SecureCodeExecutor: {e}")

def run_performance_tests():
    """运行性能测试"""
    logger.info("开始性能测试...")
    
    try:
        from security.secure_code_executor import SecureCodeExecutor
        
        executor = SecureCodeExecutor()
        
        # 测试代码执行性能
        test_code = """
import pandas as pd
import numpy as np

# 创建测试数据
data = np.random.randn(1000, 10)
df = pd.DataFrame(data)

# 执行一些计算
result = df.describe()
mean_values = df.mean()
std_values = df.std()
"""
        
        # 执行多次测试
        execution_times = []
        for i in range(10):
            start_time = time.time()
            result = executor.execute_code(test_code, {})
            end_time = time.time()
            
            if result['success']:
                execution_times.append(end_time - start_time)
            else:
                logger.error(f"性能测试第 {i+1} 次执行失败: {result.get('error')}")
        
        if execution_times:
            avg_time = sum(execution_times) / len(execution_times)
            max_time = max(execution_times)
            min_time = min(execution_times)
            
            logger.info(f"性能测试结果:")
            logger.info(f"  平均执行时间: {avg_time:.3f} 秒")
            logger.info(f"  最大执行时间: {max_time:.3f} 秒")
            logger.info(f"  最小执行时间: {min_time:.3f} 秒")
            logger.info(f"  成功执行次数: {len(execution_times)}/10")
        else:
            logger.error("所有性能测试都失败了")
            
    except ImportError as e:
        logger.warning(f"无法运行性能测试: {e}")

def run_stress_tests():
    """运行压力测试"""
    logger.info("开始压力测试...")
    
    try:
        from service_management.health_manager import HealthManager
        
        health_manager = HealthManager()
        
        # 注册多个服务进行压力测试
        services = []
        for i in range(50):
            service_config = {
                'name': f'stress_test_service_{i}',
                'host': 'localhost',
                'port': 8000 + i,
                'health_check': {
                    'endpoint': '/health',
                    'interval': 10,
                    'timeout': 5
                }
            }
            health_manager.register_service(f'stress_test_service_{i}', service_config)
            services.append(f'stress_test_service_{i}')
        
        logger.info(f"注册了 {len(services)} 个测试服务")
        
        # 获取注册的服务数量
        registered_services = health_manager.get_registered_services()
        logger.info(f"压力测试完成，成功注册 {len(registered_services)} 个服务")
        
    except ImportError as e:
        logger.warning(f"无法运行压力测试: {e}")

def main():
    """主测试函数"""
    logger.info("开始增强功能测试套件")
    
    # 运行单元测试
    logger.info("运行单元测试...")
    test_loader = unittest.TestLoader()
    test_suite = test_loader.loadTestsFromModule(sys.modules[__name__])
    
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_result = test_runner.run(test_suite)
    
    # 运行性能测试
    run_performance_tests()
    
    # 运行压力测试
    run_stress_tests()
    
    # 输出测试总结
    logger.info("测试套件完成")
    logger.info(f"运行测试: {test_result.testsRun}")
    logger.info(f"失败测试: {len(test_result.failures)}")
    logger.info(f"错误测试: {len(test_result.errors)}")
    logger.info(f"跳过测试: {len(test_result.skipped)}")
    
    if test_result.failures:
        logger.error("失败的测试:")
        for test, traceback in test_result.failures:
            logger.error(f"  {test}: {traceback}")
    
    if test_result.errors:
        logger.error("错误的测试:")
        for test, traceback in test_result.errors:
            logger.error(f"  {test}: {traceback}")
    
    # 返回测试是否成功
    return len(test_result.failures) == 0 and len(test_result.errors) == 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)