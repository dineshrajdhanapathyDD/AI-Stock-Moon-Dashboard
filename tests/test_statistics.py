#!/usr/bin/env python3
"""
Test script for statistical analysis functionality.
"""

import sys
sys.path.insert(0, 'src')

from src.mcp_tools import get_stock_prices, get_moon_phase
from src.data_models import DataFactory
from src.data_alignment import create_aligned_dataset
from src.metrics_calculator import MetricsCalculator
from src.statistical_analyzer import StatisticalAnalyzer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_statistical_analysis():
    """Test statistical analysis with real data."""
    print("[TEST] Testing statistical analysis...")
    
    # Fetch test data (larger dataset for better statistics)
    print("[CHART] Fetching stock data...")
    stock_raw = get_stock_prices('AAPL', '2024-01-01', '2024-03-31')
    
    print("[MOON] Fetching moon data...")
    moon_raw = get_moon_phase(40.7128, -74.0060, '2024-01-01', '2024-03-31')
    
    # Convert to data objects
    print("[REFRESH] Converting to data objects...")
    stock_data = [DataFactory.create_stock_data_from_dict(item) for item in stock_raw]
    moon_data = [DataFactory.create_moon_data_from_dict(item) for item in moon_raw]
    
    # Align data
    print("[LIGHTNING] Aligning data...")
    aligned_data = create_aligned_dataset(stock_data, moon_data)
    
    # Calculate metrics
    print("[CHART] Calculating metrics...")
    calculator = MetricsCalculator()
    metrics_data = calculator.calculate_all_metrics(aligned_data, rolling_window=7)
    
    print(f"[UP] Data points with metrics: {len(metrics_data)}")
    
    # Perform statistical analysis
    print("[UP] Performing statistical analysis...")
    analyzer = StatisticalAnalyzer()
    analysis_results = analyzer.perform_comprehensive_analysis(metrics_data)
    
    # Display correlation results
    print("\n[LINK] Correlation Analysis:")
    correlations = analysis_results.get('correlations', {})
    for name, corr_analysis in correlations.items():
        print(f"  {name}:")
        print(f"    Pearson r: {corr_analysis.pearson_correlation:.4f} (p={corr_analysis.pearson_p_value:.4f})")
        print(f"    Spearman ρ: {corr_analysis.spearman_correlation:.4f} (p={corr_analysis.spearman_p_value:.4f})")
        print(f"    Interpretation: {corr_analysis.interpretation}")
        print(f"    Sample size: {corr_analysis.sample_size}")
        print()
    
    # Display phase analysis results
    print("[MOON] Moon Phase Analysis:")
    phase_analysis = analysis_results.get('phase_analysis')
    if phase_analysis:
        print(f"  ANOVA F-statistic: {phase_analysis.anova_f_statistic:.4f}")
        print(f"  ANOVA p-value: {phase_analysis.anova_p_value:.4f}")
        print("  Phase Metrics:")
        for metric in phase_analysis.phase_metrics:
            print(f"    {metric.phase.name}: avg_vol={metric.avg_volatility:.2f}%, "
                  f"green_days={metric.green_day_percentage:.1f}%, "
                  f"mean_return={metric.mean_return:.2f}%, n={metric.sample_count}")
    
    # Display full moon analysis
    print("\n[FULL_MOON] Full Moon Analysis:")
    full_moon_analysis = analysis_results.get('full_moon_analysis', {})
    if 'return_comparison' in full_moon_analysis:
        ret_comp = full_moon_analysis['return_comparison']
        print(f"  Return comparison:")
        print(f"    Full moon periods: {ret_comp['group1_stats']['n']}")
        print(f"    Baseline periods: {ret_comp['group2_stats']['n']}")
        print(f"    T-test p-value: {ret_comp['t_test']['p_value']:.4f}")
        print(f"    Effect size: {ret_comp['effect_size']:.4f} ({ret_comp['interpretation']})")
        print(f"    Significant: {ret_comp['significant']}")
    
    # Display statistical summaries
    print("\n[CHART] Statistical Summaries:")
    summaries = analysis_results.get('summaries', {})
    for metric_name, summary in summaries.items():
        print(f"  {metric_name}:")
        print(f"    Mean: {summary.mean:.4f}, Std: {summary.std:.4f}")
        print(f"    Range: [{summary.min_value:.4f}, {summary.max_value:.4f}]")
        print(f"    Skewness: {summary.skewness:.4f}, Kurtosis: {summary.kurtosis:.4f}")
        print(f"    Sample size: {summary.sample_size}")
    
    return len(analysis_results) > 0

if __name__ == "__main__":
    success = test_statistical_analysis()
    print(f"\n[TARGET] Test {'PASSED' if success else 'FAILED'}")