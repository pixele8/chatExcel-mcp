"""File Service Module.

Provides secure file operations with access control, validation,
and intelligent file handling.
"""

import os
import shutil
import hashlib
import mimetypes
from pathlib import Path
from typing import Dict, Any, Optional, List, Union, Tuple
from datetime import datetime
import json

try:
    from core.config import get_config
    from core.exceptions import (
        FileAccessError, SecurityError, ValidationError,
        ResourceError
    )
    from core.types import FileInfo
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    # Fallback types
    class FileInfo:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)


class FileService:
    """Secure file service with access control."""
    
    def __init__(self):
        """Initialize file service."""
        self.config = get_config() if CORE_AVAILABLE else None
        self._setup_allowed_paths()
        self._setup_allowed_extensions()
    
    def _setup_allowed_paths(self):
        """Setup allowed file paths."""
        # Default allowed paths
        self.allowed_paths = [
            os.getcwd(),  # Current working directory
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Documents"),
            "/tmp"
        ]
        
        # Add config-based paths if available
        if self.config and hasattr(self.config.security, 'allowed_paths'):
            self.allowed_paths.extend(self.config.security.allowed_paths)
        
        # Normalize paths
        self.allowed_paths = [os.path.abspath(path) for path in self.allowed_paths]
    
    def _setup_allowed_extensions(self):
        """Setup allowed file extensions."""
        self.allowed_extensions = {
            '.xlsx', '.xls', '.csv', '.json', '.txt', '.html', '.xml',
            '.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf'
        }
        
        # Add config-based extensions if available
        if self.config and hasattr(self.config.security, 'allowed_extensions'):
            self.allowed_extensions.update(self.config.security.allowed_extensions)
    
    def validate_file_access(self, file_path: str, operation: str = 'read') -> bool:
        """Validate file access permissions.
        
        Args:
            file_path: Path to the file
            operation: Type of operation ('read', 'write', 'delete')
            
        Returns:
            True if access is allowed
            
        Raises:
            SecurityError: If access is denied
        """
        try:
            abs_path = os.path.abspath(file_path)
            
            # Check if path is within allowed directories
            path_allowed = False
            for allowed_path in self.allowed_paths:
                if abs_path.startswith(allowed_path):
                    path_allowed = True
                    break
            
            if not path_allowed:
                raise SecurityError(operation="文件访问", reason=f"文件路径不在允许的目录中: {abs_path}")
            
            # Check file extension
            file_ext = Path(file_path).suffix.lower()
            if file_ext and file_ext not in self.allowed_extensions:
                raise SecurityError(operation="文件访问", reason=f"不允许的文件扩展名: {file_ext}")
            
            # Check file size for existing files
            if os.path.exists(abs_path):
                file_size = os.path.getsize(abs_path)
                max_size = self.config.security.max_file_size if self.config else 100 * 1024 * 1024  # 100MB default
                
                if file_size > max_size:
                    raise SecurityError(operation="文件大小检查", reason=f"文件大小 ({file_size} 字节) 超过限制 ({max_size} 字节)")
            
            # Check operation permissions
            if operation == 'read' and os.path.exists(abs_path):
                if not os.access(abs_path, os.R_OK):
                    raise SecurityError(operation="读取文件", reason=f"没有读取权限: {abs_path}")
            elif operation == 'write':
                parent_dir = os.path.dirname(abs_path)
                if not os.access(parent_dir, os.W_OK):
                    raise SecurityError(operation="写入文件", reason=f"没有写入权限: {parent_dir}")
            elif operation == 'delete' and os.path.exists(abs_path):
                if not os.access(abs_path, os.W_OK):
                    raise SecurityError(operation="删除文件", reason=f"没有删除权限: {abs_path}")
            
            return True
            
        except SecurityError:
            raise
        except Exception as e:
            if CORE_AVAILABLE:
                raise SecurityError(operation="文件访问验证", reason=f"文件访问验证失败: {e}")
            else:
                raise Exception(f"文件访问验证失败: {e}")
    
    def get_file_info(self, file_path: str) -> FileInfo:
        """Get comprehensive file information.
        
        Args:
            file_path: Path to the file
            
        Returns:
            FileInfo object with file details
        """
        self.validate_file_access(file_path, 'read')
        
        try:
            path = Path(file_path)
            if not path.exists():
                raise FileAccessError(file_path=file_path, reason="文件不存在")
            
            stat = path.stat()
            
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(str(path))
            
            # Calculate file hash for integrity
            file_hash = self._calculate_file_hash(str(path))
            
            return FileInfo(
                path=str(path.absolute()),
                name=path.name,
                size=stat.st_size,
                extension=path.suffix.lower(),
                mime_type=mime_type,
                created_time=datetime.fromtimestamp(stat.st_ctime),
                modified_time=datetime.fromtimestamp(stat.st_mtime),
                accessed_time=datetime.fromtimestamp(stat.st_atime),
                is_readable=os.access(path, os.R_OK),
                is_writable=os.access(path, os.W_OK),
                is_executable=os.access(path, os.X_OK),
                file_hash=file_hash
            )
            
        except Exception as e:
            if CORE_AVAILABLE:
                raise FileAccessError(file_path=file_path, reason=f"获取文件信息失败: {e}")
            else:
                raise Exception(f"获取文件信息失败: {e}")
    
    def read_file_content(self, file_path: str, encoding: str = 'utf-8') -> str:
        """Read file content safely.
        
        Args:
            file_path: Path to the file
            encoding: File encoding
            
        Returns:
            File content as string
        """
        self.validate_file_access(file_path, 'read')
        
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            # Try different encodings
            for enc in ['gbk', 'gb2312', 'latin1']:
                try:
                    with open(file_path, 'r', encoding=enc) as f:
                        return f.read()
                except UnicodeDecodeError:
                    continue
            raise FileAccessError(file_path=file_path, reason="无法解码文件")
        except Exception as e:
            if CORE_AVAILABLE:
                raise FileAccessError(file_path=file_path, reason=f"读取文件失败: {e}")
            else:
                raise Exception(f"读取文件失败: {e}")
    
    def write_file_content(self, file_path: str, content: str, 
                          encoding: str = 'utf-8', backup: bool = True) -> bool:
        """Write content to file safely.
        
        Args:
            file_path: Path to the file
            content: Content to write
            encoding: File encoding
            backup: Whether to create backup of existing file
            
        Returns:
            True if successful
        """
        self.validate_file_access(file_path, 'write')
        
        try:
            # Create backup if file exists and backup is requested
            if backup and os.path.exists(file_path):
                backup_path = f"{file_path}.backup.{int(datetime.now().timestamp())}"
                shutil.copy2(file_path, backup_path)
            
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Write content
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            if CORE_AVAILABLE:
                raise FileAccessError(file_path=file_path, reason=f"写入文件失败: {e}")
            else:
                raise Exception(f"写入文件失败: {e}")
    
    def copy_file(self, source_path: str, dest_path: str, 
                  overwrite: bool = False) -> bool:
        """Copy file safely.
        
        Args:
            source_path: Source file path
            dest_path: Destination file path
            overwrite: Whether to overwrite existing file
            
        Returns:
            True if successful
        """
        self.validate_file_access(source_path, 'read')
        self.validate_file_access(dest_path, 'write')
        
        try:
            if os.path.exists(dest_path) and not overwrite:
                raise FileAccessError(file_path=dest_path, reason="目标文件已存在")
            
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            shutil.copy2(source_path, dest_path)
            return True
            
        except Exception as e:
            if CORE_AVAILABLE:
                raise FileAccessError(file_path=source_path, reason=f"复制文件失败: {e}")
            else:
                raise Exception(f"复制文件失败: {e}")
    
    def move_file(self, source_path: str, dest_path: str, 
                  overwrite: bool = False) -> bool:
        """Move file safely.
        
        Args:
            source_path: Source file path
            dest_path: Destination file path
            overwrite: Whether to overwrite existing file
            
        Returns:
            True if successful
        """
        self.validate_file_access(source_path, 'write')  # Need write to delete source
        self.validate_file_access(dest_path, 'write')
        
        try:
            if os.path.exists(dest_path) and not overwrite:
                raise FileAccessError(dest_path, "目标文件已存在")
            
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            shutil.move(source_path, dest_path)
            return True
            
        except Exception as e:
            if CORE_AVAILABLE:
                raise FileAccessError(file_path=source_path, reason=f"移动文件失败: {e}")
            else:
                raise Exception(f"移动文件失败: {e}")
    
    def delete_file(self, file_path: str, secure: bool = False) -> bool:
        """Delete file safely.
        
        Args:
            file_path: Path to the file
            secure: Whether to perform secure deletion
            
        Returns:
            True if successful
        """
        self.validate_file_access(file_path, 'delete')
        
        try:
            if not os.path.exists(file_path):
                return True  # Already deleted
            
            if secure:
                # Secure deletion by overwriting with random data
                file_size = os.path.getsize(file_path)
                with open(file_path, 'r+b') as f:
                    f.write(os.urandom(file_size))
                    f.flush()
                    os.fsync(f.fileno())
            
            os.remove(file_path)
            return True
            
        except Exception as e:
            if CORE_AVAILABLE:
                raise FileAccessError(file_path=file_path, reason=f"删除文件失败: {e}")
            else:
                raise Exception(f"删除文件失败: {e}")
    
    def list_directory(self, dir_path: str, pattern: Optional[str] = None,
                      recursive: bool = False) -> List[FileInfo]:
        """List directory contents safely.
        
        Args:
            dir_path: Directory path
            pattern: File pattern to match
            recursive: Whether to search recursively
            
        Returns:
            List of FileInfo objects
        """
        self.validate_file_access(dir_path, 'read')
        
        try:
            if not os.path.isdir(dir_path):
                raise FileAccessError(file_path=dir_path, reason="不是有效的目录")
            
            files = []
            
            if recursive:
                for root, dirs, filenames in os.walk(dir_path):
                    for filename in filenames:
                        file_path = os.path.join(root, filename)
                        try:
                            if pattern is None or self._match_pattern(filename, pattern):
                                files.append(self.get_file_info(file_path))
                        except Exception:
                            continue  # Skip files that can't be accessed
            else:
                for item in os.listdir(dir_path):
                    item_path = os.path.join(dir_path, item)
                    try:
                        if os.path.isfile(item_path):
                            if pattern is None or self._match_pattern(item, pattern):
                                files.append(self.get_file_info(item_path))
                    except Exception:
                        continue  # Skip files that can't be accessed
            
            return files
            
        except Exception as e:
            if CORE_AVAILABLE:
                raise FileAccessError(file_path=dir_path, reason=f"列出目录失败: {e}")
            else:
                raise Exception(f"列出目录失败: {e}")
    
    def create_directory(self, dir_path: str, parents: bool = True) -> bool:
        """Create directory safely.
        
        Args:
            dir_path: Directory path to create
            parents: Whether to create parent directories
            
        Returns:
            True if successful
        """
        self.validate_file_access(dir_path, 'write')
        
        try:
            if parents:
                os.makedirs(dir_path, exist_ok=True)
            else:
                os.mkdir(dir_path)
            
            return True
            
        except Exception as e:
            if CORE_AVAILABLE:
                raise FileAccessError(file_path=dir_path, reason=f"创建目录失败: {e}")
            else:
                raise Exception(f"创建目录失败: {e}")
    
    def get_disk_usage(self, path: str) -> Dict[str, int]:
        """Get disk usage information.
        
        Args:
            path: Path to check
            
        Returns:
            Dictionary with total, used, and free space in bytes
        """
        try:
            usage = shutil.disk_usage(path)
            return {
                'total': usage.total,
                'used': usage.total - usage.free,
                'free': usage.free,
                'usage_percentage': ((usage.total - usage.free) / usage.total) * 100
            }
        except Exception as e:
            if CORE_AVAILABLE:
                raise ResourceError(resource_type="磁盘空间", limit="未知", current=f"获取失败: {e}")
            else:
                raise Exception(f"获取磁盘使用情况失败: {e}")
    
    def _calculate_file_hash(self, file_path: str, algorithm: str = 'md5') -> str:
        """Calculate file hash for integrity checking."""
        hash_func = hashlib.new(algorithm)
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception:
            return ""
    
    def _match_pattern(self, filename: str, pattern: str) -> bool:
        """Simple pattern matching for filenames."""
        import fnmatch
        return fnmatch.fnmatch(filename.lower(), pattern.lower())
    
    def cleanup_temp_files(self, max_age_hours: int = 24) -> int:
        """Clean up temporary files.
        
        Args:
            max_age_hours: Maximum age of files to keep
            
        Returns:
            Number of files cleaned up
        """
        import time
        
        temp_dirs = ['/tmp', os.path.expanduser('~/tmp')]
        cleaned_count = 0
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        for temp_dir in temp_dirs:
            if not os.path.exists(temp_dir):
                continue
            
            try:
                for item in os.listdir(temp_dir):
                    item_path = os.path.join(temp_dir, item)
                    
                    if os.path.isfile(item_path):
                        file_age = current_time - os.path.getmtime(item_path)
                        
                        if file_age > max_age_seconds:
                            try:
                                self.delete_file(item_path)
                                cleaned_count += 1
                            except Exception:
                                continue  # Skip files that can't be deleted
            except Exception:
                continue  # Skip directories that can't be accessed
        
        return cleaned_count