#!/usr/bin/env python3
"""
Test script for caching and performance optimization.
"""

import sys
import time
sys.path.insert(0, 'src')

from src.cache_manager import (
    CacheManager, PerformanceOptimizer, 
    cached_stock_data, cached_moon_data,
    get_cache_manager, get_performance_optimizer
)
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_caching():
    """Test caching functionality."""
    print("[TEST] Testing caching functionality...")
    
    # Test basic cache operations
    print("📦 Testing basic cache operations...")
    cache = CacheManager(cache_dir=".test_cache")
    
    # Test set/get
    cache.set("test_key", {"data": "test_value"}, ttl=60)
    result = cache.get("test_key")
    assert result["data"] == "test_value", "Cache set/get failed"
    print("[OK] Basic cache set/get works")
    
    # Test cache miss
    missing = cache.get("nonexistent_key", "default")
    assert missing == "default", "Cache miss handling failed"
    print("[OK] Cache miss handling works")
    
    # Test cache stats
    stats = cache.get_stats()
    print(f"[CHART] Cache stats: {stats}")
    
    # Test cached API calls
    print("\n[WEB] Testing cached API calls...")
    
    # First call (should hit API)
    start_time = time.time()
    stock_data1 = cached_stock_data('AAPL', '2024-01-01', '2024-01-05')
    first_call_time = time.time() - start_time
    print(f"⏱️ First API call took: {first_call_time:.2f}s")
    print(f"[CHART] Got {len(stock_data1)} stock data points")
    
    # Second call (should hit cache)
    start_time = time.time()
    stock_data2 = cached_stock_data('AAPL', '2024-01-01', '2024-01-05')
    second_call_time = time.time() - start_time
    print(f"⏱️ Second API call took: {second_call_time:.2f}s")
    
    # Verify caching worked
    assert len(stock_data1) == len(stock_data2), "Cached data mismatch"
    assert second_call_time < first_call_time, "Cache didn't improve performance"
    print("[OK] API caching works - second call was faster")
    
    # Test moon data caching
    print("\n[MOON] Testing moon data caching...")
    moon_data1 = cached_moon_data(40.7128, -74.0060, '2024-01-01', '2024-01-05')
    moon_data2 = cached_moon_data(40.7128, -74.0060, '2024-01-01', '2024-01-05')
    
    assert len(moon_data1) == len(moon_data2), "Moon data cache mismatch"
    print(f"[MOON] Got {len(moon_data1)} moon data points (cached)")
    
    # Test performance stats
    print("\n[UP] Performance Statistics:")
    optimizer = get_performance_optimizer()
    perf_stats = optimizer.get_performance_stats()
    
    for key, value in perf_stats.items():
        if key != 'cache_stats':
            print(f"  {key}: {value}")
    
    print("  Cache Statistics:")
    for key, value in perf_stats['cache_stats'].items():
        print(f"    {key}: {value}")
    
    # Test cache invalidation
    print("\n🗑️ Testing cache invalidation...")
    cache_manager = get_cache_manager()
    
    # Count entries before
    stats_before = cache_manager.get_stats()
    entries_before = stats_before['memory_entries'] + stats_before['disk_entries']
    
    # Clear cache
    cache_manager.clear()
    
    # Count entries after
    stats_after = cache_manager.get_stats()
    entries_after = stats_after['memory_entries'] + stats_after['disk_entries']
    
    print(f"[CHART] Cache entries before clear: {entries_before}")
    print(f"[CHART] Cache entries after clear: {entries_after}")
    assert entries_after == 0, "Cache clear failed"
    print("[OK] Cache invalidation works")
    
    return True

if __name__ == "__main__":
    success = test_caching()
    print(f"\n[TARGET] Test {'PASSED' if success else 'FAILED'}")