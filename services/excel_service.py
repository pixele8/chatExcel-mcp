"""Excel Service Module.

Provides high-level Excel processing services with intelligent parameter detection,
caching, and enhanced error handling.
"""

import os
import pandas as pd
from typing import Dict, Any, Optional, List, Tuple, Union
from pathlib import Path
import hashlib
import json
from datetime import datetime

try:
    from core.config import get_config
    from core.exceptions import (
        FileAccessError, DataProcessingError, ValidationError,
        SecurityError, ResourceError
    )
    from core.types import FileInfo, ExcelMetadata, ExecutionResult
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    # Fallback types
    class FileInfo:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
    
    class ExcelMetadata:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
    
    class ExecutionResult:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)


class ExcelService:
    """Excel processing service with intelligent features."""
    
    def __init__(self):
        """Initialize Excel service."""
        self.config = get_config() if CORE_AVAILABLE else None
        self._file_cache = {}
        self._metadata_cache = {}
        
    def get_file_info(self, file_path: str) -> FileInfo:
        """Get comprehensive file information.
        
        Args:
            file_path: Path to the file
            
        Returns:
            FileInfo object with file details
            
        Raises:
            FileAccessError: If file cannot be accessed
        """
        try:
            path = Path(file_path)
            if not path.exists():
                raise FileAccessError(file_path=file_path, reason="文件不存在")
            
            stat = path.stat()
            
            # Check file size limits
            if self.config and stat.st_size > self.config.security.max_file_size:
                raise SecurityError(
                    f"文件大小 ({stat.st_size} 字节) 超过限制 "
                    f"({self.config.security.max_file_size} 字节)"
                )
            
            return FileInfo(
                path=str(path.absolute()),
                name=path.name,
                size=stat.st_size,
                extension=path.suffix.lower(),
                modified_time=datetime.fromtimestamp(stat.st_mtime),
                is_readable=os.access(path, os.R_OK),
                is_writable=os.access(path, os.W_OK)
            )
            
        except Exception as e:
            if CORE_AVAILABLE:
                raise FileAccessError(file_path=file_path, reason=f"获取文件信息失败: {e}")
            else:
                raise Exception(f"获取文件信息失败: {e}")
    
    def detect_excel_structure(self, file_path: str) -> ExcelMetadata:
        """Intelligently detect Excel file structure.
        
        Args:
            file_path: Path to Excel file
            
        Returns:
            ExcelMetadata with detected structure information
        """
        # Check cache first
        cache_key = self._get_cache_key(file_path)
        if cache_key in self._metadata_cache:
            return self._metadata_cache[cache_key]
        
        try:
            file_info = self.get_file_info(file_path)
            
            # Read Excel file with error handling
            if file_info.extension in ['.xlsx', '.xls']:
                # Get sheet names first
                excel_file = pd.ExcelFile(file_path)
                sheet_names = excel_file.sheet_names
                
                # Analyze first sheet for structure
                df_sample = pd.read_excel(file_path, sheet_name=0, nrows=10)
                
                # Detect encoding and separators for CSV-like analysis
                encoding = 'utf-8'
                separator = None
                
            elif file_info.extension == '.csv':
                # Detect CSV encoding and separator
                encoding = self._detect_encoding(file_path)
                separator = self._detect_separator(file_path, encoding)
                
                # Read sample
                df_sample = pd.read_csv(file_path, encoding=encoding, sep=separator, nrows=10)
                sheet_names = ['Sheet1']  # CSV has only one "sheet"
                
            else:
                raise ValidationError(parameter="file_extension", value=file_info.extension, expected="支持的Excel格式(.xlsx, .xls, .csv)")
            
            # Analyze data structure
            columns_info = []
            for col in df_sample.columns:
                col_data = df_sample[col].dropna()
                if len(col_data) > 0:
                    dtype = str(col_data.dtype)
                    sample_values = col_data.head(3).tolist()
                    unique_count = col_data.nunique()
                    null_count = df_sample[col].isnull().sum()
                else:
                    dtype = 'object'
                    sample_values = []
                    unique_count = 0
                    null_count = len(df_sample)
                
                columns_info.append({
                    'name': col,
                    'dtype': dtype,
                    'sample_values': sample_values,
                    'unique_count': unique_count,
                    'null_count': null_count,
                    'null_percentage': (null_count / len(df_sample)) * 100 if len(df_sample) > 0 else 0
                })
            
            # Create metadata
            metadata = ExcelMetadata(
                file_info=file_info,
                sheet_names=sheet_names,
                total_sheets=len(sheet_names),
                columns_info=columns_info,
                total_columns=len(columns_info),
                sample_rows=len(df_sample),
                encoding=encoding,
                separator=separator,
                detected_at=datetime.now()
            )
            
            # Cache the result
            self._metadata_cache[cache_key] = metadata
            
            return metadata
            
        except Exception as e:
            if CORE_AVAILABLE:
                raise DataProcessingError(
                    operation="Excel结构检测",
                    data_info=str({'file_path': file_path}),
                    error_details=f"Excel结构检测失败: {e}"
                )
            else:
                raise Exception(f"Excel结构检测失败: {e}")
    
    def smart_read_excel(self, file_path: str, **kwargs) -> pd.DataFrame:
        """Smart Excel reading with automatic parameter detection.
        
        Args:
            file_path: Path to Excel file
            **kwargs: Override parameters
            
        Returns:
            pandas DataFrame
        """
        # Get metadata for smart parameter detection
        metadata = self.detect_excel_structure(file_path)
        
        # Prepare reading parameters
        read_params = {
            'sheet_name': kwargs.get('sheet_name', 0),
            'header': kwargs.get('header', 0),
            'index_col': kwargs.get('index_col', None),
            'usecols': kwargs.get('usecols', None),
            'nrows': kwargs.get('nrows', None),
            'skiprows': kwargs.get('skiprows', None)
        }
        
        # Smart parameter adjustments based on metadata
        if metadata.file_info.extension == '.csv':
            read_params.update({
                'encoding': metadata.encoding,
                'sep': metadata.separator
            })
            df = pd.read_csv(file_path, **read_params)
        else:
            df = pd.read_excel(file_path, **read_params)
        
        return df
    
    def get_smart_suggestions(self, file_path: str) -> Dict[str, Any]:
        """Get intelligent parameter suggestions for Excel processing.
        
        Args:
            file_path: Path to Excel file
            
        Returns:
            Dictionary with parameter suggestions
        """
        metadata = self.detect_excel_structure(file_path)
        
        suggestions = {
            'file_info': {
                'name': metadata.file_info.name,
                'size_mb': round(metadata.file_info.size / (1024 * 1024), 2),
                'format': metadata.file_info.extension,
                'sheets_available': metadata.sheet_names
            },
            'reading_suggestions': {
                'recommended_sheet': metadata.sheet_names[0] if metadata.sheet_names else None,
                'has_header': True,  # Most Excel files have headers
                'encoding': metadata.encoding if hasattr(metadata, 'encoding') else 'utf-8',
                'separator': metadata.separator if hasattr(metadata, 'separator') else None
            },
            'data_insights': {
                'total_columns': metadata.total_columns,
                'sample_rows_analyzed': metadata.sample_rows,
                'columns_with_nulls': len([c for c in metadata.columns_info if c['null_count'] > 0]),
                'numeric_columns': len([c for c in metadata.columns_info if 'int' in c['dtype'] or 'float' in c['dtype']]),
                'text_columns': len([c for c in metadata.columns_info if 'object' in c['dtype']])
            },
            'processing_recommendations': []
        }
        
        # Add specific recommendations
        high_null_cols = [c for c in metadata.columns_info if c['null_percentage'] > 50]
        if high_null_cols:
            suggestions['processing_recommendations'].append(
                f"注意: {len(high_null_cols)} 个列的空值超过50%，建议进行数据清洗"
            )
        
        if metadata.file_info.size > 10 * 1024 * 1024:  # 10MB
            suggestions['processing_recommendations'].append(
                "文件较大，建议使用分块读取或指定列范围以提高性能"
            )
        
        if len(metadata.sheet_names) > 1:
            suggestions['processing_recommendations'].append(
                f"文件包含 {len(metadata.sheet_names)} 个工作表，请指定要处理的工作表"
            )
        
        return suggestions
    
    def _get_cache_key(self, file_path: str) -> str:
        """Generate cache key for file."""
        stat = os.stat(file_path)
        content = f"{file_path}_{stat.st_mtime}_{stat.st_size}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _detect_encoding(self, file_path: str) -> str:
        """Detect file encoding."""
        try:
            import chardet
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Read first 10KB
                result = chardet.detect(raw_data)
                return result.get('encoding', 'utf-8')
        except ImportError:
            # Fallback to common encodings
            for encoding in ['utf-8', 'gbk', 'gb2312', 'latin1']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        f.read(1000)
                    return encoding
                except UnicodeDecodeError:
                    continue
            return 'utf-8'
    
    def _detect_separator(self, file_path: str, encoding: str) -> str:
        """Detect CSV separator."""
        try:
            import csv
            with open(file_path, 'r', encoding=encoding) as f:
                sample = f.read(1024)
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                return delimiter
        except:
            # Fallback to common separators
            separators = [',', ';', '\t', '|']
            with open(file_path, 'r', encoding=encoding) as f:
                first_line = f.readline()
                for sep in separators:
                    if sep in first_line:
                        return sep
            return ','
    
    def clear_cache(self):
        """Clear all caches."""
        self._file_cache.clear()
        self._metadata_cache.clear()