#!/usr/bin/env python3
"""
Test script for metrics calculation functionality.
"""

import sys
sys.path.insert(0, 'src')

from src.mcp_tools import get_stock_prices, get_moon_phase
from src.data_models import DataFactory
from src.data_alignment import create_aligned_dataset
from src.metrics_calculator import MetricsCalculator, calculate_comprehensive_metrics
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_metrics_calculation():
    """Test metrics calculation with real data."""
    print("[TEST] Testing metrics calculation...")
    
    # Fetch test data
    print("[CHART] Fetching stock data...")
    stock_raw = get_stock_prices('AAPL', '2024-01-01', '2024-01-31')
    
    print("[MOON] Fetching moon data...")
    moon_raw = get_moon_phase(40.7128, -74.0060, '2024-01-01', '2024-01-31')
    
    # Convert to data objects
    print("[REFRESH] Converting to data objects...")
    stock_data = [DataFactory.create_stock_data_from_dict(item) for item in stock_raw]
    moon_data = [DataFactory.create_moon_data_from_dict(item) for item in moon_raw]
    
    # Align data
    print("[LIGHTNING] Aligning data...")
    aligned_data = create_aligned_dataset(stock_data, moon_data)
    
    print(f"[UP] Aligned data points: {len(aligned_data)}")
    
    # Calculate metrics
    print("[CHART] Calculating metrics...")
    calculator = MetricsCalculator()
    metrics_data = calculator.calculate_all_metrics(aligned_data, rolling_window=7)
    
    # Calculate comprehensive metrics
    print("🔢 Calculating comprehensive metrics...")
    comprehensive_metrics = calculate_comprehensive_metrics(metrics_data, [7, 14])
    
    # Display results
    print("\n[CLIPBOARD] Metrics Summary:")
    for i, point in enumerate(metrics_data[:5]):  # Show first 5 points
        print(f"📅 {point.date.date()}")
        print(f"  [MONEY] Close: ${point.close:.2f}")
        print(f"  [UP] Daily Return: {point.daily_return:.2f}%" if point.daily_return else "  [UP] Daily Return: N/A")
        print(f"  [CHART] Volatility (7d): {point.volatility_7d:.2f}%" if point.volatility_7d else "  [CHART] Volatility (7d): N/A")
        print(f"  [MOON] Moon Phase: {point.phase_code.name} ({point.illumination:.1f}%)")
        print(f"  [FULL_MOON] Days from Full: {point.days_from_full_moon}")
        print()
    
    # Show comprehensive metrics summary
    print("[CHART] Comprehensive Metrics Available:")
    for metric_name, values in comprehensive_metrics.items():
        non_null_count = sum(1 for v in values if v is not None)
        print(f"  {metric_name}: {non_null_count}/{len(values)} values")
    
    return len(metrics_data) > 0 and len(comprehensive_metrics) > 0

if __name__ == "__main__":
    success = test_metrics_calculation()
    print(f"[TARGET] Test {'PASSED' if success else 'FAILED'}")