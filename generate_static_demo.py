#!/usr/bin/env python3
"""
Generate a static HTML demo version for GitHub Pages.
Creates standalone HTML files with embedded data and charts.
"""

import sys
import os
import json
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_tools import get_stock_prices, get_moon_phase
from data_models import DataFactory
from data_alignment import create_aligned_dataset
from metrics_calculator import MetricsCalculator
from statistical_analyzer import StatisticalAnalyzer
from visualizations import create_comprehensive_dashboard

def generate_sample_data():
    """Generate sample data for the static demo."""
    print("📊 Generating sample data...")
    
    # Use AAPL as example
    symbol = "AAPL"
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    
    # Fetch data
    stock_data = get_stock_prices(symbol, start_date, end_date)
    moon_data = get_moon_phase(40.7128, -74.0060, start_date, end_date)
    
    # Convert to objects
    stock_objects = [DataFactory.create_stock_data_from_dict(item) for item in stock_data]
    moon_objects = [DataFactory.create_moon_data_from_dict(item) for item in moon_data]
    
    # Align and calculate metrics
    aligned_data = create_aligned_dataset(stock_objects, moon_objects)
    calculator = MetricsCalculator()
    metrics_data = calculator.calculate_all_metrics(aligned_data, rolling_window=7)
    
    # Perform analysis
    analyzer = StatisticalAnalyzer()
    analysis_results = analyzer.perform_comprehensive_analysis(metrics_data)
    
    return metrics_data, analysis_results

def create_static_html(metrics_data, analysis_results):
    """Create static HTML with embedded charts."""
    print("🎨 Creating static HTML...")
    
    # Generate charts
    charts = create_comprehensive_dashboard(metrics_data, analysis_results['phase_analysis'])
    
    # Convert charts to HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock Moon Dashboard - Demo</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ background-color: #f8f9fa; }}
        .chart-container {{ margin: 20px 0; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 0; }}
        .stats-card {{ text-align: center; padding: 20px; margin: 10px; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1 class="display-4">🌙 Stock Moon Dashboard</h1>
            <p class="lead">Analyzing relationships between AAPL stock prices and moon phases</p>
            <p class="text-light">Static Demo - Data from last 90 days</p>
        </div>
    </div>
    
    <div class="container mt-4">
        <div class="row">
            <div class="col-md-3">
                <div class="stats-card">
                    <h4 class="text-primary">{len(metrics_data)}</h4>
                    <p class="text-muted">Trading Days</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card">
                    <h4 class="text-info">
                    {max(abs(corr.pearson_correlation) for corr in analysis_results['correlations'].values()):.3f}
                    </h4>
                    <p class="text-muted">Max Correlation</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card">
                    <h4 class="text-warning">
                    {sum(p.volatility_7d for p in metrics_data if p.volatility_7d) / len([p for p in metrics_data if p.volatility_7d]):.2f}%
                    </h4>
                    <p class="text-muted">Avg Volatility</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card">
                    <h4 class="text-success">
                    {min(corr.pearson_p_value for corr in analysis_results['correlations'].values()):.3f}
                    </h4>
                    <p class="text-muted">Min P-Value</p>
                </div>
            </div>
        </div>
        
        <div class="alert alert-info mt-4">
            <h5>📊 Demo Features</h5>
            <ul class="mb-0">
                <li>Interactive charts with zoom and pan</li>
                <li>Statistical analysis of price-moon correlations</li>
                <li>90-day historical data for AAPL</li>
                <li>Real-time calculations and insights</li>
            </ul>
        </div>
"""
    
    # Add each chart
    chart_titles = {
        'time_series': '📈 Stock Price & Moon Phases Over Time',
        'returns_vs_illumination': '🌙 Returns vs Moon Illumination',
        'volatility_vs_illumination': '📊 Volatility vs Moon Illumination',
        'volatility_by_phase': '🌕 Volatility by Moon Phase',
        'returns_by_phase': '📈 Returns by Moon Phase',
        'calendar_heatmap': '📅 Returns Calendar Heatmap'
    }
    
    for chart_name, fig in charts.items():
        title = chart_titles.get(chart_name, chart_name.replace('_', ' ').title())
        html_content += f"""
        <div class="chart-container">
            <h4>{title}</h4>
            <div id="{chart_name}"></div>
        </div>
        """
    
    # Add JavaScript to render charts
    html_content += """
    <div class="mt-5 p-4 bg-light rounded">
        <h5>🚀 Want the Full Interactive Version?</h5>
        <p>This is a static demo. For the full interactive dashboard with real-time data:</p>
        <a href="https://github.com/yourusername/stock-moon-dashboard" class="btn btn-primary">
            View on GitHub
        </a>
        <a href="#" class="btn btn-success">
            Live Demo
        </a>
    </div>
    
    </div>
    
    <script>
"""
    
    # Add Plotly chart rendering
    for chart_name, fig in charts.items():
        fig_json = fig.to_json()
        html_content += f"""
        Plotly.newPlot('{chart_name}', {fig_json});
        """
    
    html_content += """
    </script>
    
    <footer class="mt-5 py-4 bg-dark text-light text-center">
        <div class="container">
            <p>&copy; 2025 Stock Moon Dashboard - Educational Research Tool</p>
            <p class="small">Disclaimer: For research purposes only. Not financial advice.</p>
        </div>
    </footer>
    
</body>
</html>
"""
    
    return html_content

def main():
    """Generate static demo."""
    print("🌙 Generating Static Demo for GitHub Pages...")
    
    try:
        # Create static directory
        os.makedirs('static-demo', exist_ok=True)
        
        # Generate data and analysis
        metrics_data, analysis_results = generate_sample_data()
        
        # Create HTML
        html_content = create_static_html(metrics_data, analysis_results)
        
        # Write files
        with open('static-demo/index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Create GitHub Pages config
        with open('static-demo/_config.yml', 'w') as f:
            f.write('theme: jekyll-theme-minimal\\n')
        
        print("✅ Static demo generated successfully!")
        print("📁 Files created in 'static-demo/' directory")
        print("🌐 Ready for GitHub Pages deployment")
        print("")
        print("📋 Next steps:")
        print("1. Push to GitHub")
        print("2. Enable GitHub Pages in repository settings")
        print("3. Select 'static-demo' folder as source")
        print("4. Your demo will be live at: https://yourusername.github.io/stock-moon-dashboard/")
        
    except Exception as e:
        print(f"❌ Error generating static demo: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()