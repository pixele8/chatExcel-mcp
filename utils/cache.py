"""Cache Management Module.

Provides intelligent caching for file metadata, Excel structures,
and execution results to improve performance.
"""

import os
import json
import pickle
import hashlib
import time
from typing import Dict, Any, Optional, Union, List
from pathlib import Path
from dataclasses import dataclass, asdict
from threading import Lock

try:
    from core.config import get_config
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    def get_config():
        return {'cache': {'enabled': True, 'ttl': 3600, 'max_size': 100}}


@dataclass
class CacheEntry:
    """Cache entry with metadata."""
    key: str
    value: Any
    created_at: float
    accessed_at: float
    access_count: int
    size_bytes: int
    ttl: Optional[float] = None


class CacheManager:
    """Intelligent cache manager with TTL and size limits."""
    
    def __init__(self, cache_dir: Optional[str] = None, 
                 max_memory_size: int = 100 * 1024 * 1024,  # 100MB
                 default_ttl: int = 3600):
        """Initialize cache manager.
        
        Args:
            cache_dir: Directory for persistent cache
            max_memory_size: Maximum memory cache size in bytes
            default_ttl: Default TTL in seconds
        """
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / '.chatexcel_cache'
        self.max_memory_size = max_memory_size
        self.default_ttl = default_ttl
        
        # In-memory cache
        self._memory_cache: Dict[str, CacheEntry] = {}
        self._memory_size = 0
        self._lock = Lock()
        
        # Ensure cache directory exists
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        if CORE_AVAILABLE:
            config = get_config()
            cache_config = config.get('cache', {})
            self.enabled = cache_config.get('enabled', True)
            self.default_ttl = cache_config.get('ttl', default_ttl)
            self.max_memory_size = cache_config.get('max_size', max_memory_size) * 1024 * 1024
        else:
            self.enabled = True
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache.
        
        Args:
            key: Cache key
            default: Default value if not found
            
        Returns:
            Cached value or default
        """
        if not self.enabled:
            return default
        
        with self._lock:
            # Check memory cache first
            if key in self._memory_cache:
                entry = self._memory_cache[key]
                
                # Check TTL
                if self._is_expired(entry):
                    self._remove_from_memory(key)
                    return default
                
                # Update access info
                entry.accessed_at = time.time()
                entry.access_count += 1
                return entry.value
            
            # Check persistent cache
            persistent_value = self._get_from_disk(key)
            if persistent_value is not None:
                # Add to memory cache
                self._add_to_memory(key, persistent_value)
                return persistent_value
            
            return default
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None, 
            persist: bool = False) -> bool:
        """Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
            persist: Whether to persist to disk
            
        Returns:
            True if successfully cached
        """
        if not self.enabled:
            return False
        
        try:
            with self._lock:
                # Add to memory cache
                success = self._add_to_memory(key, value, ttl)
                
                # Persist to disk if requested
                if persist and success:
                    self._save_to_disk(key, value, ttl)
                
                return success
        except Exception:
            return False
    
    def delete(self, key: str) -> bool:
        """Delete value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if successfully deleted
        """
        if not self.enabled:
            return False
        
        with self._lock:
            # Remove from memory
            memory_removed = self._remove_from_memory(key)
            
            # Remove from disk
            disk_removed = self._remove_from_disk(key)
            
            return memory_removed or disk_removed
    
    def clear(self, memory_only: bool = False) -> None:
        """Clear cache.
        
        Args:
            memory_only: If True, only clear memory cache
        """
        with self._lock:
            # Clear memory cache
            self._memory_cache.clear()
            self._memory_size = 0
            
            # Clear disk cache
            if not memory_only:
                try:
                    for cache_file in self.cache_dir.glob('*.cache'):
                        cache_file.unlink()
                except Exception:
                    pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        with self._lock:
            memory_entries = len(self._memory_cache)
            disk_entries = len(list(self.cache_dir.glob('*.cache')))
            
            # Calculate hit rates (simplified)
            total_accesses = sum(entry.access_count for entry in self._memory_cache.values())
            
            return {
                'enabled': self.enabled,
                'memory_entries': memory_entries,
                'disk_entries': disk_entries,
                'memory_size_bytes': self._memory_size,
                'memory_size_mb': self._memory_size / (1024 * 1024),
                'max_memory_size_mb': self.max_memory_size / (1024 * 1024),
                'total_accesses': total_accesses,
                'cache_dir': str(self.cache_dir)
            }
    
    def cleanup_expired(self) -> int:
        """Clean up expired entries.
        
        Returns:
            Number of entries removed
        """
        if not self.enabled:
            return 0
        
        removed_count = 0
        
        with self._lock:
            # Clean memory cache
            expired_keys = []
            for key, entry in self._memory_cache.items():
                if self._is_expired(entry):
                    expired_keys.append(key)
            
            for key in expired_keys:
                self._remove_from_memory(key)
                removed_count += 1
            
            # Clean disk cache
            try:
                for cache_file in self.cache_dir.glob('*.cache'):
                    try:
                        with open(cache_file, 'rb') as f:
                            entry_data = pickle.load(f)
                            if self._is_disk_entry_expired(entry_data):
                                cache_file.unlink()
                                removed_count += 1
                    except Exception:
                        # Remove corrupted cache files
                        cache_file.unlink()
                        removed_count += 1
            except Exception:
                pass
        
        return removed_count
    
    def cache_file_info(self, file_path: str) -> str:
        """Generate cache key for file info.
        
        Args:
            file_path: Path to file
            
        Returns:
            Cache key for file info
        """
        return f"file_info:{self._hash_key(file_path)}"
    
    def cache_excel_structure(self, file_path: str) -> str:
        """Generate cache key for Excel structure.
        
        Args:
            file_path: Path to Excel file
            
        Returns:
            Cache key for Excel structure
        """
        return f"excel_structure:{self._hash_key(file_path)}"
    
    def cache_execution_result(self, code: str, file_path: str) -> str:
        """Generate cache key for execution result.
        
        Args:
            code: Python code
            file_path: Path to file
            
        Returns:
            Cache key for execution result
        """
        combined = f"{code}:{file_path}"
        return f"execution:{self._hash_key(combined)}"
    
    def _add_to_memory(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Add entry to memory cache."""
        try:
            # Calculate size
            size_bytes = self._calculate_size(value)
            
            # Check if we need to make space
            while (self._memory_size + size_bytes > self.max_memory_size and 
                   self._memory_cache):
                self._evict_lru()
            
            # Don't cache if too large
            if size_bytes > self.max_memory_size:
                return False
            
            # Create entry
            entry = CacheEntry(
                key=key,
                value=value,
                created_at=time.time(),
                accessed_at=time.time(),
                access_count=1,
                size_bytes=size_bytes,
                ttl=ttl or self.default_ttl
            )
            
            # Remove existing entry if present
            if key in self._memory_cache:
                self._remove_from_memory(key)
            
            # Add new entry
            self._memory_cache[key] = entry
            self._memory_size += size_bytes
            
            return True
        except Exception:
            return False
    
    def _remove_from_memory(self, key: str) -> bool:
        """Remove entry from memory cache."""
        if key in self._memory_cache:
            entry = self._memory_cache.pop(key)
            self._memory_size -= entry.size_bytes
            return True
        return False
    
    def _evict_lru(self) -> None:
        """Evict least recently used entry."""
        if not self._memory_cache:
            return
        
        # Find LRU entry
        lru_key = min(self._memory_cache.keys(), 
                     key=lambda k: self._memory_cache[k].accessed_at)
        self._remove_from_memory(lru_key)
    
    def _is_expired(self, entry: CacheEntry) -> bool:
        """Check if cache entry is expired."""
        if entry.ttl is None:
            return False
        return time.time() - entry.created_at > entry.ttl
    
    def _save_to_disk(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Save entry to disk."""
        try:
            cache_file = self.cache_dir / f"{self._hash_key(key)}.cache"
            
            entry_data = {
                'key': key,
                'value': value,
                'created_at': time.time(),
                'ttl': ttl or self.default_ttl
            }
            
            with open(cache_file, 'wb') as f:
                pickle.dump(entry_data, f)
            
            return True
        except Exception:
            return False
    
    def _get_from_disk(self, key: str) -> Any:
        """Get entry from disk."""
        try:
            cache_file = self.cache_dir / f"{self._hash_key(key)}.cache"
            
            if not cache_file.exists():
                return None
            
            with open(cache_file, 'rb') as f:
                entry_data = pickle.load(f)
            
            # Check expiration
            if self._is_disk_entry_expired(entry_data):
                cache_file.unlink()
                return None
            
            return entry_data['value']
        except Exception:
            return None
    
    def _remove_from_disk(self, key: str) -> bool:
        """Remove entry from disk."""
        try:
            cache_file = self.cache_dir / f"{self._hash_key(key)}.cache"
            if cache_file.exists():
                cache_file.unlink()
                return True
        except Exception:
            pass
        return False
    
    def _is_disk_entry_expired(self, entry_data: Dict[str, Any]) -> bool:
        """Check if disk entry is expired."""
        ttl = entry_data.get('ttl')
        if ttl is None:
            return False
        
        created_at = entry_data.get('created_at', 0)
        return time.time() - created_at > ttl
    
    def _hash_key(self, key: str) -> str:
        """Generate hash for cache key."""
        return hashlib.md5(key.encode('utf-8')).hexdigest()
    
    def _calculate_size(self, obj: Any) -> int:
        """Calculate approximate size of object in bytes."""
        try:
            return len(pickle.dumps(obj))
        except Exception:
            # Fallback estimation
            if isinstance(obj, str):
                return len(obj.encode('utf-8'))
            elif isinstance(obj, (int, float)):
                return 8
            elif isinstance(obj, bool):
                return 1
            elif isinstance(obj, (list, tuple)):
                return sum(self._calculate_size(item) for item in obj)
            elif isinstance(obj, dict):
                return sum(self._calculate_size(k) + self._calculate_size(v) 
                          for k, v in obj.items())
            else:
                return 1024  # Default estimate


# Global cache instance
_global_cache = None


def get_cache_manager() -> CacheManager:
    """Get global cache manager instance.
    
    Returns:
        Global CacheManager instance
    """
    global _global_cache
    if _global_cache is None:
        _global_cache = CacheManager()
    return _global_cache


def cache_result(key_func=None, ttl: Optional[int] = None, persist: bool = False):
    """Decorator for caching function results.
    
    Args:
        key_func: Function to generate cache key
        ttl: Time to live in seconds
        persist: Whether to persist to disk
        
    Returns:
        Decorated function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            cache = get_cache_manager()
            
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Default key generation
                key_parts = [func.__name__]
                key_parts.extend(str(arg) for arg in args)
                key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
                cache_key = ":".join(key_parts)
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl=ttl, persist=persist)
            
            return result
        
        return wrapper
    return decorator