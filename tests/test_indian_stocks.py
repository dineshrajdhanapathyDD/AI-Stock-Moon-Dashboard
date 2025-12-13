#!/usr/bin/env python3
"""
Test script to demonstrate Indian stock market compatibility
with the Stock Moon Dashboard system.
"""

from src.mcp_tools import get_stock_prices, get_moon_phase
from src.data_models import DataFactory
from src.data_alignment import create_aligned_dataset
from src.metrics_calculator import MetricsCalculator
from src.statistical_analyzer import StatisticalAnalyzer
from datetime import datetime, timedelta
import sys

def test_indian_stock(symbol, name):
    """Test a single Indian stock with moon phase analysis."""
    print(f"\n🇮🇳 Testing {name} ({symbol})")
    print("-" * 50)
    
    # Date range for analysis
    end_date = datetime.now()
    start_date = end_date - timedelta(days=45)
    
    try:
        # Fetch stock data
        print("[UP] Fetching stock data...")
        raw_stock_data = get_stock_prices(
            symbol=symbol,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )
        
        # Convert to StockData objects
        stock_data = []
        for raw_data in raw_stock_data:
            try:
                stock_obj = DataFactory.create_stock_data_from_dict(raw_data)
                stock_data.append(stock_obj)
            except Exception as e:
                continue
        
        # Fetch moon data (using Mumbai coordinates)
        print("[MOON] Fetching moon phase data...")
        raw_moon_data = get_moon_phase(
            latitude=19.0760,  # Mumbai latitude
            longitude=72.8777,  # Mumbai longitude
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )
        
        # Convert to MoonData objects
        moon_data = []
        for raw_data in raw_moon_data:
            try:
                moon_obj = DataFactory.create_moon_data_from_dict(raw_data)
                moon_data.append(moon_obj)
            except Exception as e:
                continue
        
        # Create aligned dataset
        print("[REFRESH] Aligning data...")
        aligned_data = create_aligned_dataset(stock_data, moon_data)
        
        if not aligned_data:
            print("[ERROR] No aligned data available")
            return False
        
        # Calculate metrics
        print("[CHART] Calculating metrics...")
        calculator = MetricsCalculator()
        metrics_data = calculator.calculate_all_metrics(aligned_data, rolling_window=7)
        
        # Perform statistical analysis
        print("[SEARCH] Performing statistical analysis...")
        analyzer = StatisticalAnalyzer()
        results = analyzer.perform_comprehensive_analysis(metrics_data)
        
        # Display results
        print(f"[OK] Analysis complete!")
        print(f"   [CHART] Data points: {len(metrics_data)}")
        print(f"   [MONEY] Latest price: ₹{metrics_data[-1].close:.2f}")
        print(f"   [UP] Price range: ₹{min(p.close for p in metrics_data):.2f} - ₹{max(p.close for p in metrics_data):.2f}")
        
        # Show returns
        returns = [p.daily_return for p in metrics_data if p.daily_return is not None]
        if returns:
            avg_return = sum(returns) / len(returns)
            print(f"   [CHART] Average daily return: {avg_return:.2f}%")
        
        # Show correlations
        correlations = results.get('correlations', {})
        significant_corr = sum(1 for corr in correlations.values() if corr.p_value < 0.05)
        print(f"   [MOON] Correlations analyzed: {len(correlations)}")
        print(f"   [UP] Significant correlations: {significant_corr}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

def main():
    """Main test function."""
    print("[MOON] Indian Stock Market + Moon Phase Analysis Test")
    print("=" * 60)
    
    # List of popular Indian stocks to test
    indian_stocks = [
        ("RELIANCE.NS", "Reliance Industries"),
        ("TCS.NS", "Tata Consultancy Services"),
        ("INFY.NS", "Infosys"),
        ("HDFCBANK.NS", "HDFC Bank"),
        ("ICICIBANK.NS", "ICICI Bank")
    ]
    
    # Test each stock
    successful_tests = 0
    for symbol, name in indian_stocks:
        if test_indian_stock(symbol, name):
            successful_tests += 1
    
    # Summary
    print(f"\n[TARGET] TEST SUMMARY")
    print("=" * 60)
    print(f"[OK] Successful tests: {successful_tests}/{len(indian_stocks)}")
    
    if successful_tests == len(indian_stocks):
        print("[ROCKET] ALL INDIAN STOCKS ARE FULLY COMPATIBLE!")
        print("\n[PHONE] You can now use these symbols in the dashboard:")
        for symbol, name in indian_stocks:
            print(f"   • {symbol} - {name}")
        print("\n[WEB] Access the dashboard at: http://localhost:8050")
        print("💡 Tip: Use .NS suffix for NSE stocks (e.g., RELIANCE.NS)")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main()