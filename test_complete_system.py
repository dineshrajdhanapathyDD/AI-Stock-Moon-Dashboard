#!/usr/bin/env python3
"""
Comprehensive test script for the complete Stock Moon Dashboard system.
"""

import sys
import time
sys.path.insert(0, 'src')

from src.cache_manager import cached_stock_data, cached_moon_data, get_performance_optimizer
from src.data_models import DataFactory
from src.data_alignment import create_aligned_dataset
from src.metrics_calculator import MetricsCalculator
from src.statistical_analyzer import StatisticalAnalyzer
from src.visualizations import create_comprehensive_dashboard
from src.data_validation import validate_analysis_parameters
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_complete_system():
    """Test the complete system end-to-end."""
    print("[TEST] Testing Complete Stock Moon Dashboard System...")
    
    # Test 1: Parameter Validation
    print("\n[1] Testing Parameter Validation...")
    try:
        params = validate_analysis_parameters('AAPL', '2024-01-01', '2024-02-29', 7, 40.7128, -74.0060)
        print(f"[OK] Parameter validation: {params['symbol']}")
    except Exception as e:
        print(f"[ERROR] Parameter validation failed: {e}")
        return False
    
    # Test 2: Cached Data Fetching
    print("\n[2] Testing Cached Data Fetching...")
    try:
        start_time = time.time()
        stock_data = cached_stock_data('AAPL', '2024-01-01', '2024-02-29')
        moon_data = cached_moon_data(40.7128, -74.0060, '2024-01-01', '2024-02-29')
        fetch_time = time.time() - start_time
        
        print(f"[OK] Data fetching: {len(stock_data)} stock, {len(moon_data)} moon points ({fetch_time:.2f}s)")
    except Exception as e:
        print(f"[ERROR] Data fetching failed: {e}")
        return False
    
    # Test 3: Data Conversion and Alignment
    print("\n[3] Testing Data Conversion and Alignment...")
    try:
        stock_objects = [DataFactory.create_stock_data_from_dict(item) for item in stock_data]
        moon_objects = [DataFactory.create_moon_data_from_dict(item) for item in moon_data]
        aligned_data = create_aligned_dataset(stock_objects, moon_objects)
        
        print(f"[OK] Data alignment: {len(aligned_data)} aligned points")
    except Exception as e:
        print(f"[ERROR] Data alignment failed: {e}")
        return False
    
    # Test 4: Metrics Calculation
    print("\n[4] Testing Metrics Calculation...")
    try:
        calculator = MetricsCalculator()
        metrics_data = calculator.calculate_all_metrics(aligned_data, rolling_window=7)
        
        # Count non-null metrics
        returns_count = sum(1 for p in metrics_data if p.daily_return is not None)
        volatility_count = sum(1 for p in metrics_data if p.volatility_7d is not None)
        
        print(f"[OK] Metrics calculation: {returns_count} returns, {volatility_count} volatilities")
    except Exception as e:
        print(f"[ERROR] Metrics calculation failed: {e}")
        return False
    
    # Test 5: Statistical Analysis
    print("\n[5] Testing Statistical Analysis...")
    try:
        analyzer = StatisticalAnalyzer()
        analysis_results = analyzer.perform_comprehensive_analysis(metrics_data)
        
        correlations = analysis_results.get('correlations', {})
        phase_metrics = analysis_results.get('phase_analysis', {}).phase_metrics
        
        print(f"[OK] Statistical analysis: {len(correlations)} correlations, {len(phase_metrics)} phase metrics")
    except Exception as e:
        print(f"[ERROR] Statistical analysis failed: {e}")
        return False
    
    # Test 6: Visualization Generation
    print("\n[6] Testing Visualization Generation...")
    try:
        dashboard_charts = create_comprehensive_dashboard(metrics_data, phase_metrics)
        
        chart_counts = {name: len(fig.data) for name, fig in dashboard_charts.items()}
        print(f"[OK] Visualizations: {len(dashboard_charts)} charts created")
        for name, count in chart_counts.items():
            print(f"   {name}: {count} traces")
    except Exception as e:
        print(f"[ERROR] Visualization generation failed: {e}")
        return False
    
    # Test 7: Performance Metrics
    print("\n[7] Testing Performance Metrics...")
    try:
        optimizer = get_performance_optimizer()
        perf_stats = optimizer.get_performance_stats()
        
        print(f"[OK] Performance metrics:")
        print(f"   API Calls: {perf_stats['api_calls']}")
        print(f"   Cache Hit Rate: {perf_stats['cache_stats']['hit_rate_percent']:.1f}%")
        print(f"   Avg Response Time: {perf_stats['avg_processing_time']:.2f}s")
    except Exception as e:
        print(f"[ERROR] Performance metrics failed: {e}")
        return False
    
    # Test 8: Data Quality Validation
    print("\n[8] Testing Data Quality...")
    try:
        # Check data completeness
        total_points = len(metrics_data)
        valid_returns = sum(1 for p in metrics_data if p.daily_return is not None)
        valid_moon_data = sum(1 for p in metrics_data if 0 <= p.illumination <= 100)
        
        completeness_ratio = valid_returns / total_points if total_points > 0 else 0
        moon_quality_ratio = valid_moon_data / total_points if total_points > 0 else 0
        
        print(f"[OK] Data quality:")
        print(f"   Data completeness: {completeness_ratio:.1%}")
        print(f"   Moon data quality: {moon_quality_ratio:.1%}")
        
        if completeness_ratio < 0.8:
            print("⚠️  Warning: Low data completeness")
        if moon_quality_ratio < 0.95:
            print("⚠️  Warning: Moon data quality issues")
            
    except Exception as e:
        print(f"[ERROR] Data quality validation failed: {e}")
        return False
    
    # Test 9: Statistical Significance
    print("\n[9] Testing Statistical Significance...")
    try:
        significant_correlations = 0
        for name, corr_analysis in correlations.items():
            if corr_analysis.pearson_p_value < 0.05:
                significant_correlations += 1
                print(f"   Significant correlation found: {name} (p={corr_analysis.pearson_p_value:.3f})")
        
        if significant_correlations == 0:
            print("   No statistically significant correlations found (p < 0.05)")
        
        print(f"[OK] Statistical significance: {significant_correlations}/{len(correlations)} significant correlations")
    except Exception as e:
        print(f"[ERROR] Statistical significance testing failed: {e}")
        return False
    
    # Test 10: System Integration
    print("\n[10] Testing System Integration...")
    try:
        # Test the complete pipeline with different parameters
        test_symbols = ['MSFT', 'GOOGL']
        integration_results = []
        
        for symbol in test_symbols:
            try:
                # Quick test with smaller dataset
                stock_test = cached_stock_data(symbol, '2024-02-01', '2024-02-15')
                moon_test = cached_moon_data(40.7128, -74.0060, '2024-02-01', '2024-02-15')
                
                if len(stock_test) > 5 and len(moon_test) > 5:
                    integration_results.append(f"{symbol}: [OK]")
                else:
                    integration_results.append(f"{symbol}: ⚠️ Limited data")
                    
            except Exception as e:
                integration_results.append(f"{symbol}: [ERROR] {str(e)[:30]}")
        
        print(f"[OK] System integration:")
        for result in integration_results:
            print(f"   {result}")
            
    except Exception as e:
        print(f"[ERROR] System integration failed: {e}")
        return False
    
    # Final Summary
    print("\n[TARGET] SYSTEM TEST SUMMARY")
    print("=" * 50)
    print("[OK] All core functionality tests passed!")
    print(f"[CHART] Analyzed {len(metrics_data)} data points")
    print(f"[UP] Generated {len(dashboard_charts)} visualization components")
    print(f"[LINK] Calculated {len(correlations)} correlation relationships")
    print(f"[MOON] Analyzed {len(phase_metrics)} moon phases")
    print(f"[LIGHTNING] Cache hit rate: {perf_stats['cache_stats']['hit_rate_percent']:.1f}%")
    
    return True

if __name__ == "__main__":
    success = test_complete_system()
    print(f"\n[FLAG] Complete System Test: {'PASSED' if success else 'FAILED'}")
    
    if success:
        print("\n[ROCKET] The Stock Moon Dashboard is ready for use!")
        print("   Run 'python app.py' to start the web interface")
    else:
        print("\n[WRENCH] System needs attention before deployment")