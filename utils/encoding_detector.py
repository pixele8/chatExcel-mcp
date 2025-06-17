
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
