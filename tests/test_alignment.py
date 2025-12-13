#!/usr/bin/env python3
"""
Test script for data alignment functionality.
"""

import sys
sys.path.insert(0, 'src')

from src.mcp_tools import get_stock_prices, get_moon_phase
from src.data_models import DataFactory
from src.data_alignment import create_aligned_dataset
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_alignment():
    """Test data alignment with real data."""
    print("[TEST] Testing data alignment...")
    
    # Fetch test data
    print("[CHART] Fetching stock data...")
    stock_raw = get_stock_prices('AAPL', '2024-01-01', '2024-01-15')
    
    print("[MOON] Fetching moon data...")
    moon_raw = get_moon_phase(40.7128, -74.0060, '2024-01-01', '2024-01-15')
    
    # Convert to data objects
    print("[REFRESH] Converting to data objects...")
    stock_data = [DataFactory.create_stock_data_from_dict(item) for item in stock_raw]
    moon_data = [DataFactory.create_moon_data_from_dict(item) for item in moon_raw]
    
    print(f"[UP] Stock data points: {len(stock_data)}")
    print(f"[MOON] Moon data points: {len(moon_data)}")
    
    # Align data
    print("[LIGHTNING] Aligning data...")
    aligned_data = create_aligned_dataset(stock_data, moon_data)
    
    print(f"[OK] Aligned data points: {len(aligned_data)}")
    
    # Show sample
    if aligned_data:
        sample = aligned_data[0]
        print(f"📅 Sample point: {sample.date.date()}")
        print(f"[MONEY] Close price: ${sample.close:.2f}")
        print(f"[MOON] Moon phase: {sample.phase_code.name} ({sample.illumination:.1f}% illuminated)")
    
    return len(aligned_data) > 0

if __name__ == "__main__":
    success = test_alignment()
    print(f"[TARGET] Test {'PASSED' if success else 'FAILED'}")