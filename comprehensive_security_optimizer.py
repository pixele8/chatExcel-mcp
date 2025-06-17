#!/usr/bin/env python3
"""
全面的MCP工具安全检测和优化脚本
基于comprehensive_tools_analysis_report.json的发现，实施系统性安全改进
"""

import json
import os
import re
import ast
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('security_optimization.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SecurityOptimizer:
    """MCP工具安全优化器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.server_file = self.project_root / 'server.py'
        self.security_issues = []
        self.optimization_results = []
        
    def load_analysis_report(self) -> Dict[str, Any]:
        """加载分析报告"""
        report_file = self.project_root / 'comprehensive_tools_analysis_report.json'
        if not report_file.exists():
            logger.error(f"分析报告文件不存在: {report_file}")
            return {}
            
        with open(report_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def scan_unsafe_code_patterns(self) -> List[Dict[str, Any]]:
        """扫描不安全的代码模式"""
        unsafe_patterns = [
            (r'exec\s*\(', 'exec() 调用', 'high'),
            (r'eval\s*\(', 'eval() 调用', 'high'),
            (r'__import__\s*\(', '动态导入', 'medium'),
            (r'open\s*\([^)]*["\']w', '文件写入操作', 'medium'),
            (r'subprocess\.|os\.system|os\.popen', '系统命令执行', 'high'),
            (r'pickle\.loads?\s*\(', 'pickle反序列化', 'high'),
            (r'compile\s*\(', '代码编译', 'medium')
        ]
        
        issues = []
        
        if not self.server_file.exists():
            logger.error(f"服务器文件不存在: {self.server_file}")
            return issues
            
        with open(self.server_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            
        for line_num, line in enumerate(lines, 1):
            for pattern, description, severity in unsafe_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        'file': str(self.server_file),
                        'line': line_num,
                        'content': line.strip(),
                        'pattern': pattern,
                        'description': description,
                        'severity': severity,
                        'suggestion': self._get_security_suggestion(description)
                    })
        
        return issues
    
    def _get_security_suggestion(self, description: str) -> str:
        """获取安全建议"""
        suggestions = {
            'exec() 调用': '使用SecureCodeExecutor替代直接的exec()调用',
            'eval() 调用': '使用ast.literal_eval()或JSON解析替代eval()',
            '动态导入': '使用白名单限制可导入的模块',
            '文件写入操作': '验证文件路径，使用安全的文件操作',
            '系统命令执行': '避免执行系统命令，使用安全的替代方案',
            'pickle反序列化': '使用JSON或其他安全的序列化格式',
            '代码编译': '验证代码来源，使用安全的编译环境'
        }
        return suggestions.get(description, '请审查此代码的安全性')
    
    def implement_encoding_detection(self) -> bool:
        """实施智能编码检测机制"""
        encoding_detector_code = '''
# 智能编码检测器
import chardet
from typing import Optional, Tuple

class EncodingDetector:
    """智能编码检测器"""
    
    @staticmethod
    def detect_file_encoding(file_path: str) -> Tuple[str, float]:
        """检测文件编码"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # 读取前10KB用于检测
            
            result = chardet.detect(raw_data)
            encoding = result.get('encoding', 'utf-8')
            confidence = result.get('confidence', 0.0)
            
            # 如果置信度太低，使用默认编码
            if confidence < 0.7:
                encoding = 'utf-8'
                
            return encoding, confidence
            
        except Exception as e:
            logger.warning(f"编码检测失败: {e}")
            return 'utf-8', 0.0
    
    @staticmethod
    def safe_read_file(file_path: str, fallback_encoding: str = 'utf-8') -> Optional[str]:
        """安全读取文件内容"""
        encoding, confidence = EncodingDetector.detect_file_encoding(file_path)
        
        encodings_to_try = [encoding, fallback_encoding, 'latin1', 'cp1252']
        
        for enc in encodings_to_try:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
                
        logger.error(f"无法读取文件 {file_path}，所有编码尝试都失败")
        return None
'''
        
        encoding_file = self.project_root / 'utils' / 'encoding_detector.py'
        encoding_file.parent.mkdir(exist_ok=True)
        
        try:
            with open(encoding_file, 'w', encoding='utf-8') as f:
                f.write(encoding_detector_code)
            logger.info(f"智能编码检测器已创建: {encoding_file}")
            return True
        except Exception as e:
            logger.error(f"创建编码检测器失败: {e}")
            return False
    
    def implement_parameter_validator(self) -> bool:
        """实施统一参数验证框架"""
        validator_code = '''
# 统一参数验证框架
from typing import Any, Dict, List, Optional, Union, Callable
import re
from pathlib import Path

class ParameterValidator:
    """统一参数验证器"""
    
    @staticmethod
    def validate_file_path(path: str, must_exist: bool = True, allowed_extensions: Optional[List[str]] = None) -> bool:
        """验证文件路径"""
        try:
            path_obj = Path(path)
            
            # 检查路径遍历攻击
            if '..' in str(path_obj) or str(path_obj).startswith('/'):
                return False
                
            # 检查文件是否存在
            if must_exist and not path_obj.exists():
                return False
                
            # 检查文件扩展名
            if allowed_extensions:
                if path_obj.suffix.lower() not in [ext.lower() for ext in allowed_extensions]:
                    return False
                    
            return True
            
        except Exception:
            return False
    
    @staticmethod
    def validate_code_content(code: str, max_length: int = 10000) -> Dict[str, Any]:
        """验证代码内容"""
        result = {'valid': True, 'warnings': [], 'errors': []}
        
        # 检查代码长度
        if len(code) > max_length:
            result['errors'].append(f'代码长度超过限制 ({len(code)} > {max_length})')
            result['valid'] = False
            
        # 检查危险模式
        dangerous_patterns = [
            (r'exec\s*\(', 'exec() 调用'),
            (r'eval\s*\(', 'eval() 调用'),
            (r'__import__\s*\(', '动态导入'),
            (r'subprocess\.|os\.system', '系统命令执行')
        ]
        
        for pattern, description in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                result['warnings'].append(f'检测到潜在危险操作: {description}')
                
        return result
    
    @staticmethod
    def sanitize_input(value: Any, input_type: str = 'string') -> Any:
        """清理输入数据"""
        if input_type == 'string':
            if isinstance(value, str):
                # 移除潜在的脚本标签
                value = re.sub(r'<script[^>]*>.*?</script>', '', value, flags=re.IGNORECASE | re.DOTALL)
                # 移除SQL注入模式
                value = re.sub(r'(union|select|insert|update|delete|drop)\s+', '', value, flags=re.IGNORECASE)
                return value.strip()
        elif input_type == 'number':
            try:
                return float(value) if '.' in str(value) else int(value)
            except (ValueError, TypeError):
                return 0
                
        return value
'''
        
        validator_file = self.project_root / 'utils' / 'parameter_validator.py'
        validator_file.parent.mkdir(exist_ok=True)
        
        try:
            with open(validator_file, 'w', encoding='utf-8') as f:
                f.write(validator_code)
            logger.info(f"参数验证框架已创建: {validator_file}")
            return True
        except Exception as e:
            logger.error(f"创建参数验证框架失败: {e}")
            return False
    
    def implement_error_handler(self) -> bool:
        """实施标准化错误处理机制"""
        error_handler_code = '''
# 标准化错误处理机制
import traceback
import logging
from typing import Dict, Any, Optional
from datetime import datetime

class StandardErrorHandler:
    """标准化错误处理器"""
    
    def __init__(self, logger_name: str = 'mcp_tools'):
        self.logger = logging.getLogger(logger_name)
    
    def handle_error(self, error: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """标准化错误处理"""
        error_info = {
            'success': False,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'timestamp': datetime.now().isoformat(),
            'traceback': traceback.format_exc()
        }
        
        if context:
            error_info['context'] = context
            
        # 记录错误
        self.logger.error(f"错误处理: {error_info['error_type']} - {error_info['error_message']}")
        
        # 根据错误类型提供建议
        error_info['suggestion'] = self._get_error_suggestion(error)
        
        return error_info
    
    def _get_error_suggestion(self, error: Exception) -> str:
        """根据错误类型提供建议"""
        suggestions = {
            'FileNotFoundError': '请检查文件路径是否正确',
            'PermissionError': '请检查文件权限设置',
            'UnicodeDecodeError': '请检查文件编码格式',
            'ValueError': '请检查输入参数的格式和范围',
            'TypeError': '请检查参数类型是否正确',
            'KeyError': '请检查字典键是否存在',
            'IndexError': '请检查列表索引是否越界',
            'ImportError': '请检查模块是否已安装',
            'SyntaxError': '请检查代码语法是否正确'
        }
        
        error_type = type(error).__name__
        return suggestions.get(error_type, '请检查错误信息并重试')
    
    def create_success_response(self, data: Any, message: str = '操作成功') -> Dict[str, Any]:
        """创建成功响应"""
        return {
            'success': True,
            'data': data,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
'''
        
        error_handler_file = self.project_root / 'utils' / 'error_handler.py'
        error_handler_file.parent.mkdir(exist_ok=True)
        
        try:
            with open(error_handler_file, 'w', encoding='utf-8') as f:
                f.write(error_handler_code)
            logger.info(f"错误处理框架已创建: {error_handler_file}")
            return True
        except Exception as e:
            logger.error(f"创建错误处理框架失败: {e}")
            return False
    
    def run_comprehensive_optimization(self) -> Dict[str, Any]:
        """运行全面优化"""
        logger.info("开始全面安全优化...")
        
        # 1. 加载分析报告
        report = self.load_analysis_report()
        
        # 2. 扫描安全问题
        security_issues = self.scan_unsafe_code_patterns()
        
        # 3. 实施优化措施
        optimizations = {
            'encoding_detection': self.implement_encoding_detection(),
            'parameter_validation': self.implement_parameter_validator(),
            'error_handling': self.implement_error_handler()
        }
        
        # 4. 生成优化报告
        optimization_report = {
            'timestamp': datetime.now().isoformat(),
            'security_issues_found': len(security_issues),
            'security_issues': security_issues,
            'optimizations_implemented': optimizations,
            'recommendations': self._generate_recommendations(security_issues, report)
        }
        
        # 5. 保存优化报告
        report_file = self.project_root / 'security_optimization_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(optimization_report, f, indent=2, ensure_ascii=False)
            
        logger.info(f"优化完成，报告已保存到: {report_file}")
        return optimization_report
    
    def _generate_recommendations(self, security_issues: List[Dict], analysis_report: Dict) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        # 基于安全问题的建议
        high_severity_count = sum(1 for issue in security_issues if issue['severity'] == 'high')
        if high_severity_count > 0:
            recommendations.append(f"发现 {high_severity_count} 个高危安全问题，需要立即修复")
            
        # 基于分析报告的建议
        if analysis_report:
            tools_with_issues = analysis_report.get('summary', {}).get('tools_with_potential_issues', 0)
            if tools_with_issues > 0:
                recommendations.append(f"有 {tools_with_issues} 个工具存在潜在问题，建议逐一检查")
                
        # 通用建议
        recommendations.extend([
            "建议为所有工具添加输入验证",
            "建议实施统一的错误处理机制",
            "建议定期进行安全审计",
            "建议添加详细的日志记录",
            "建议实施代码执行的沙箱环境"
        ])
        
        return recommendations

def main():
    """主函数"""
    project_root = '/Users/wangdada/Downloads/mcp/chatExcel-mcp'
    optimizer = SecurityOptimizer(project_root)
    
    try:
        report = optimizer.run_comprehensive_optimization()
        print(f"\n=== 安全优化完成 ===")
        print(f"发现安全问题: {report['security_issues_found']} 个")
        print(f"实施优化措施: {sum(report['optimizations_implemented'].values())} 项")
        print(f"生成建议: {len(report['recommendations'])} 条")
        
        if report['security_issues_found'] > 0:
            print("\n高优先级安全问题:")
            for issue in report['security_issues']:
                if issue['severity'] == 'high':
                    print(f"  - {issue['description']} (第{issue['line']}行): {issue['suggestion']}")
                    
    except Exception as e:
        logger.error(f"优化过程中发生错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()