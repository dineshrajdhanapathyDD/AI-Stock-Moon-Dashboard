"""
Caching and performance optimization for the Stock Moon Dashboard.
Implements client-side caching with TTL expiration and batched request handling.
"""

import json
import hashlib
import time
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple, Callable
import logging
from pathlib import Path
import pickle
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


class CacheManager:
    """Client-side cache manager with TTL expiration."""
    
    def __init__(self, cache_dir: str = ".cache", default_ttl: int = 3600):
        """
        Initialize cache manager.
        
        Args:
            cache_dir: Directory to store cache files
            default_ttl: Default time-to-live in seconds (1 hour)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.default_ttl = default_ttl
        self.memory_cache = {}
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'disk_reads': 0,
            'disk_writes': 0
        }
        self._lock = threading.RLock()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            default: Default value if not found
            
        Returns:
            Cached value or default
        """
        with self._lock:
            # Check memory cache first
            if key in self.memory_cache:
                entry = self.memory_cache[key]
                if self._is_valid(entry):
                    self.cache_stats['hits'] += 1
                    logger.debug(f"Memory cache hit for key: {key}")
                    return entry['data']
                else:
                    # Expired, remove from memory
                    del self.memory_cache[key]
                    self.cache_stats['evictions'] += 1
            
            # Check disk cache
            disk_value = self._get_from_disk(key)
            if disk_value is not None:
                # Load into memory cache
                self.memory_cache[key] = disk_value
                self.cache_stats['hits'] += 1
                self.cache_stats['disk_reads'] += 1
                logger.debug(f"Disk cache hit for key: {key}")
                return disk_value['data']
            
            self.cache_stats['misses'] += 1
            logger.debug(f"Cache miss for key: {key}")
            return default
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses default if None)
        """
        with self._lock:
            ttl = ttl or self.default_ttl
            expiry = time.time() + ttl
            
            entry = {
                'data': value,
                'expiry': expiry,
                'created': time.time()
            }
            
            # Store in memory
            self.memory_cache[key] = entry
            
            # Store on disk asynchronously
            self._set_to_disk_async(key, entry)
            
            logger.debug(f"Cached key: {key} (TTL: {ttl}s)")
    
    def invalidate(self, key: str) -> bool:
        """
        Invalidate cache entry.
        
        Args:
            key: Cache key to invalidate
            
        Returns:
            True if key was found and removed
        """
        with self._lock:
            removed = False
            
            # Remove from memory
            if key in self.memory_cache:
                del self.memory_cache[key]
                removed = True
            
            # Remove from disk
            cache_file = self._get_cache_file_path(key)
            if cache_file.exists():
                cache_file.unlink()
                removed = True
            
            if removed:
                logger.debug(f"Invalidated cache key: {key}")
            
            return removed
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            # Clear memory cache
            self.memory_cache.clear()
            
            # Clear disk cache
            for cache_file in self.cache_dir.glob("*.cache"):
                cache_file.unlink()
            
            # Reset stats
            self.cache_stats = {k: 0 for k in self.cache_stats}
            
            logger.info("Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            total_requests = self.cache_stats['hits'] + self.cache_stats['misses']
            hit_rate = (self.cache_stats['hits'] / total_requests * 100) if total_requests > 0 else 0
            
            return {
                **self.cache_stats,
                'hit_rate_percent': round(hit_rate, 2),
                'memory_entries': len(self.memory_cache),
                'disk_entries': len(list(self.cache_dir.glob("*.cache")))
            }
    
    def cleanup_expired(self) -> int:
        """
        Clean up expired cache entries.
        
        Returns:
            Number of entries removed
        """
        with self._lock:
            removed_count = 0
            current_time = time.time()
            
            # Clean memory cache
            expired_keys = [
                key for key, entry in self.memory_cache.items()
                if entry['expiry'] < current_time
            ]
            
            for key in expired_keys:
                del self.memory_cache[key]
                removed_count += 1
            
            # Clean disk cache
            for cache_file in self.cache_dir.glob("*.cache"):
                try:
                    with open(cache_file, 'rb') as f:
                        entry = pickle.load(f)
                    
                    if entry['expiry'] < current_time:
                        cache_file.unlink()
                        removed_count += 1
                except Exception as e:
                    logger.warning(f"Error checking cache file {cache_file}: {e}")
                    cache_file.unlink()  # Remove corrupted files
                    removed_count += 1
            
            if removed_count > 0:
                logger.info(f"Cleaned up {removed_count} expired cache entries")
            
            return removed_count
    
    def _is_valid(self, entry: Dict[str, Any]) -> bool:
        """Check if cache entry is still valid."""
        return entry['expiry'] > time.time()
    
    def _get_cache_file_path(self, key: str) -> Path:
        """Get cache file path for key."""
        # Create safe filename from key
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.cache"
    
    def _get_from_disk(self, key: str) -> Optional[Dict[str, Any]]:
        """Get entry from disk cache."""
        cache_file = self._get_cache_file_path(key)
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'rb') as f:
                entry = pickle.load(f)
            
            if self._is_valid(entry):
                return entry
            else:
                # Expired, remove file
                cache_file.unlink()
                return None
                
        except Exception as e:
            logger.warning(f"Error reading cache file {cache_file}: {e}")
            # Remove corrupted file
            cache_file.unlink()
            return None
    
    def _set_to_disk_async(self, key: str, entry: Dict[str, Any]) -> None:
        """Set entry to disk cache asynchronously."""
        def write_to_disk():
            try:
                cache_file = self._get_cache_file_path(key)
                with open(cache_file, 'wb') as f:
                    pickle.dump(entry, f)
                self.cache_stats['disk_writes'] += 1
            except Exception as e:
                logger.warning(f"Error writing to cache file: {e}")
        
        # Use thread pool for async disk writes
        threading.Thread(target=write_to_disk, daemon=True).start()


class BatchRequestManager:
    """Manager for batching API requests to minimize network overhead."""
    
    def __init__(self, batch_size: int = 5, batch_timeout: float = 1.0):
        """
        Initialize batch request manager.
        
        Args:
            batch_size: Maximum number of requests per batch
            batch_timeout: Maximum time to wait for batch completion (seconds)
        """
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self.pending_requests = []
        self._lock = threading.Lock()
    
    def add_request(self, request_func: Callable, *args, **kwargs) -> Any:
        """
        Add request to batch queue.
        
        Args:
            request_func: Function to call for the request
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Result of the request
        """
        with self._lock:
            self.pending_requests.append((request_func, args, kwargs))
            
            # Execute batch if we've reached batch size
            if len(self.pending_requests) >= self.batch_size:
                return self._execute_batch()
        
        # If not executing immediately, wait for timeout or more requests
        time.sleep(0.1)  # Small delay to allow batching
        
        with self._lock:
            if self.pending_requests:
                return self._execute_batch()
    
    def _execute_batch(self) -> List[Any]:
        """Execute all pending requests in parallel."""
        if not self.pending_requests:
            return []
        
        requests = self.pending_requests.copy()
        self.pending_requests.clear()
        
        logger.info(f"Executing batch of {len(requests)} requests")
        
        results = []
        with ThreadPoolExecutor(max_workers=min(len(requests), 10)) as executor:
            # Submit all requests
            future_to_request = {
                executor.submit(func, *args, **kwargs): (func, args, kwargs)
                for func, args, kwargs in requests
            }
            
            # Collect results
            for future in as_completed(future_to_request, timeout=self.batch_timeout):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.error(f"Batch request failed: {e}")
                    results.append(None)
        
        return results


class PerformanceOptimizer:
    """Performance optimization utilities."""
    
    def __init__(self, cache_manager: CacheManager):
        """
        Initialize performance optimizer.
        
        Args:
            cache_manager: Cache manager instance
        """
        self.cache = cache_manager
        self.batch_manager = BatchRequestManager()
        self.performance_stats = {
            'api_calls': 0,
            'cache_hits': 0,
            'processing_time': 0.0,
            'data_points_processed': 0
        }
    
    def cached_api_call(self, cache_key: str, api_func: Callable, 
                       *args, ttl: int = 3600, **kwargs) -> Any:
        """
        Make API call with caching.
        
        Args:
            cache_key: Unique key for caching
            api_func: API function to call
            *args: Arguments for API function
            ttl: Cache TTL in seconds
            **kwargs: Keyword arguments for API function
            
        Returns:
            API response (cached or fresh)
        """
        # Check cache first
        cached_result = self.cache.get(cache_key)
        if cached_result is not None:
            self.performance_stats['cache_hits'] += 1
            logger.debug(f"Using cached result for: {cache_key}")
            return cached_result
        
        # Make API call
        start_time = time.time()
        try:
            result = api_func(*args, **kwargs)
            self.cache.set(cache_key, result, ttl)
            self.performance_stats['api_calls'] += 1
            
            processing_time = time.time() - start_time
            self.performance_stats['processing_time'] += processing_time
            
            logger.debug(f"API call completed in {processing_time:.2f}s: {cache_key}")
            return result
            
        except Exception as e:
            logger.error(f"API call failed for {cache_key}: {e}")
            raise
    
    def optimize_data_processing(self, data: List[Any], 
                                chunk_size: int = 1000) -> List[Any]:
        """
        Optimize data processing for large datasets.
        
        Args:
            data: Data to process
            chunk_size: Size of processing chunks
            
        Returns:
            Processed data
        """
        if len(data) <= chunk_size:
            return data
        
        logger.info(f"Processing {len(data)} items in chunks of {chunk_size}")
        
        processed_chunks = []
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            processed_chunks.append(chunk)
            
            # Update stats
            self.performance_stats['data_points_processed'] += len(chunk)
        
        # Flatten results
        return [item for chunk in processed_chunks for item in chunk]
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        cache_stats = self.cache.get_stats()
        
        return {
            **self.performance_stats,
            'cache_stats': cache_stats,
            'avg_processing_time': (
                self.performance_stats['processing_time'] / 
                max(self.performance_stats['api_calls'], 1)
            )
        }


# Global cache manager instance
_cache_manager = None
_performance_optimizer = None


def get_cache_manager() -> CacheManager:
    """Get global cache manager instance."""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager


def get_performance_optimizer() -> PerformanceOptimizer:
    """Get global performance optimizer instance."""
    global _performance_optimizer
    if _performance_optimizer is None:
        _performance_optimizer = PerformanceOptimizer(get_cache_manager())
    return _performance_optimizer


def create_cache_key(prefix: str, **params) -> str:
    """
    Create a cache key from parameters.
    
    Args:
        prefix: Key prefix
        **params: Parameters to include in key
        
    Returns:
        Cache key string
    """
    # Sort parameters for consistent keys
    sorted_params = sorted(params.items())
    param_str = "&".join(f"{k}={v}" for k, v in sorted_params)
    return f"{prefix}:{param_str}"


def cached_stock_data(symbol: str, start_date: str, end_date: str, 
                     interval: str = "1d") -> Any:
    """
    Cached wrapper for stock data fetching.
    
    Args:
        symbol: Stock symbol
        start_date: Start date
        end_date: End date
        interval: Data interval
        
    Returns:
        Stock data
    """
    try:
        from .mcp_tools import get_stock_prices
    except ImportError:
        from mcp_tools import get_stock_prices
    
    cache_key = create_cache_key(
        "stock_data",
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        interval=interval
    )
    
    optimizer = get_performance_optimizer()
    return optimizer.cached_api_call(
        cache_key,
        get_stock_prices,
        symbol, start_date, end_date, interval,
        ttl=1800  # 30 minutes TTL for stock data
    )


def cached_moon_data(latitude: float, longitude: float, 
                    start_date: str, end_date: str) -> Any:
    """
    Cached wrapper for moon data fetching.
    
    Args:
        latitude: Latitude
        longitude: Longitude
        start_date: Start date
        end_date: End date
        
    Returns:
        Moon data
    """
    try:
        from .mcp_tools import get_moon_phase
    except ImportError:
        from mcp_tools import get_moon_phase
    
    cache_key = create_cache_key(
        "moon_data",
        latitude=latitude,
        longitude=longitude,
        start_date=start_date,
        end_date=end_date
    )
    
    optimizer = get_performance_optimizer()
    return optimizer.cached_api_call(
        cache_key,
        get_moon_phase,
        latitude, longitude, start_date, end_date,
        ttl=86400  # 24 hours TTL for moon data (changes slowly)
    )


def cleanup_cache_periodically(interval: int = 3600) -> None:
    """
    Start periodic cache cleanup.
    
    Args:
        interval: Cleanup interval in seconds (default: 1 hour)
    """
    def cleanup_worker():
        while True:
            try:
                cache_manager = get_cache_manager()
                removed = cache_manager.cleanup_expired()
                if removed > 0:
                    logger.info(f"Periodic cleanup removed {removed} expired entries")
                time.sleep(interval)
            except Exception as e:
                logger.error(f"Error in periodic cleanup: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
    cleanup_thread.start()
    logger.info(f"Started periodic cache cleanup (interval: {interval}s)")