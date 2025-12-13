#!/usr/bin/env python3
"""
Test script for visualization components.
"""

import sys
sys.path.insert(0, 'src')

from src.mcp_tools import get_stock_prices, get_moon_phase
from src.data_models import DataFactory
from src.data_alignment import create_aligned_dataset
from src.metrics_calculator import MetricsCalculator
from src.statistical_analyzer import StatisticalAnalyzer
from src.visualizations import (
    TimeSeriesChart, ScatterPlot, BarChart, CalendarHeatmap,
    create_comprehensive_dashboard
)
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_visualizations():
    """Test visualization components."""
    print("[TEST] Testing visualization components...")
    
    # Fetch test data
    print("[CHART] Fetching data for visualizations...")
    stock_raw = get_stock_prices('AAPL', '2024-01-01', '2024-03-31')
    moon_raw = get_moon_phase(40.7128, -74.0060, '2024-01-01', '2024-03-31')
    
    # Convert and align data
    stock_data = [DataFactory.create_stock_data_from_dict(item) for item in stock_raw]
    moon_data = [DataFactory.create_moon_data_from_dict(item) for item in moon_raw]
    aligned_data = create_aligned_dataset(stock_data, moon_data)
    
    # Calculate metrics
    calculator = MetricsCalculator()
    metrics_data = calculator.calculate_all_metrics(aligned_data, rolling_window=7)
    
    # Perform statistical analysis
    analyzer = StatisticalAnalyzer()
    analysis_results = analyzer.perform_comprehensive_analysis(metrics_data)
    phase_metrics = analysis_results['phase_analysis'].phase_metrics
    
    print(f"[UP] Testing with {len(metrics_data)} data points")
    
    # Test Time Series Chart
    print("\n[UP] Testing Time Series Chart...")
    ts_chart = TimeSeriesChart("AAPL Stock Price with Moon Phases")
    ts_fig = ts_chart.create_chart(metrics_data, show_volume=True, show_volatility=True)
    
    print(f"[OK] Time series chart created with {len(ts_fig.data)} traces")
    
    # Test Scatter Plots
    print("\n[LINK] Testing Scatter Plots...")
    scatter_plot = ScatterPlot()
    
    returns_scatter = scatter_plot.create_illumination_vs_returns_plot(metrics_data)
    print(f"[OK] Returns vs illumination scatter plot created with {len(returns_scatter.data)} traces")
    
    volatility_scatter = scatter_plot.create_volatility_vs_illumination_plot(metrics_data)
    print(f"[OK] Volatility vs illumination scatter plot created with {len(volatility_scatter.data)} traces")
    
    # Test Bar Charts
    print("\n[CHART] Testing Bar Charts...")
    bar_chart = BarChart()
    
    volatility_bar = bar_chart.create_volatility_by_phase_chart(phase_metrics)
    print(f"[OK] Volatility by phase bar chart created with {len(volatility_bar.data)} traces")
    
    returns_bar = bar_chart.create_returns_by_phase_chart(phase_metrics)
    print(f"[OK] Returns by phase bar chart created with {len(returns_bar.data)} traces")
    
    # Test Calendar Heatmap
    print("\n📅 Testing Calendar Heatmap...")
    calendar_heatmap = CalendarHeatmap()
    calendar_fig = calendar_heatmap.create_returns_heatmap(metrics_data, year=2024)
    print(f"[OK] Calendar heatmap created with {len(calendar_fig.data)} traces")
    
    # Test Comprehensive Dashboard
    print("\n🎛️ Testing Comprehensive Dashboard...")
    dashboard_charts = create_comprehensive_dashboard(metrics_data, phase_metrics)
    
    print("[CHART] Dashboard Charts Created:")
    for chart_name, fig in dashboard_charts.items():
        print(f"  {chart_name}: {len(fig.data)} traces")
    
    # Verify all charts were created
    expected_charts = [
        'time_series', 'returns_vs_illumination', 'volatility_vs_illumination',
        'volatility_by_phase', 'returns_by_phase', 'calendar_heatmap'
    ]
    
    missing_charts = [chart for chart in expected_charts if chart not in dashboard_charts]
    if missing_charts:
        print(f"[ERROR] Missing charts: {missing_charts}")
        return False
    
    print("[OK] All expected charts created successfully")
    
    # Test chart properties
    print("\n[SEARCH] Validating Chart Properties...")
    
    # Check time series chart has candlestick data
    ts_trace_types = [type(trace).__name__ for trace in ts_fig.data]
    if 'Candlestick' not in ts_trace_types:
        print("[ERROR] Time series chart missing candlestick trace")
        return False
    print("[OK] Time series chart has candlestick data")
    
    # Check scatter plots have trend lines
    if len(returns_scatter.data) < 2:
        print("[ERROR] Returns scatter plot missing trend line")
        return False
    print("[OK] Scatter plots have trend lines")
    
    # Check bar charts have data
    if not volatility_bar.data or not returns_bar.data:
        print("[ERROR] Bar charts missing data")
        return False
    print("[OK] Bar charts have data")
    
    # Test with empty data
    print("\n[SEARCH] Testing with empty data...")
    empty_ts = ts_chart.create_chart([])
    empty_scatter = scatter_plot.create_illumination_vs_returns_plot([])
    empty_bar = bar_chart.create_volatility_by_phase_chart([])
    empty_calendar = calendar_heatmap.create_returns_heatmap([])
    
    print("[OK] Empty data handling works for all chart types")
    
    return True

if __name__ == "__main__":
    success = test_visualizations()
    print(f"\n[TARGET] Test {'PASSED' if success else 'FAILED'}")