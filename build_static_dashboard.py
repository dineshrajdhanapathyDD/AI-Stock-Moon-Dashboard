#!/usr/bin/env python3
"""
Static Dashboard Builder
Generates a complete static HTML dashboard with embedded data and charts.

Architecture:
Python (build time) → Generate index.html + data.json → Static hosting
"""

import sys
import os
import json
from datetime import datetime, timedelta
import base64

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def generate_sample_data():
    """Generate sample data for static dashboard."""
    print("📊 Generating sample data...")
    
    try:
        from mcp_tools import get_stock_prices, get_moon_phase
        from data_models import DataFactory
        from data_alignment import create_aligned_dataset
        from metrics_calculator import MetricsCalculator
        from statistical_analyzer import StatisticalAnalyzer
        
        # Sample stocks for demo
        stocks = ["AAPL", "GOOGL", "MSFT", "RELIANCE.NS"]
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        
        all_data = {}
        
        for symbol in stocks:
            try:
                print(f"  Fetching {symbol}...")
                
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
                
                # Store processed data
                all_data[symbol] = {
                    'metrics': [
                        {
                            'date': m.date.isoformat(),
                            'close_price': getattr(m, 'close_price', getattr(m, 'stock_price', 0)),
                            'daily_return': getattr(m, 'daily_return', 0),
                            'volatility_7d': getattr(m, 'volatility_7d', 0),
                            'moon_illumination': getattr(m, 'moon_illumination', 0),
                            'moon_phase': getattr(m, 'moon_phase', 'Unknown')
                        } for m in metrics_data
                    ],
                    'analysis': {
                        'correlations': {
                            k: {
                                'pearson_correlation': getattr(v, 'pearson_correlation', 0),
                                'pearson_p_value': getattr(v, 'pearson_p_value', 1),
                                'spearman_correlation': getattr(v, 'spearman_correlation', 0),
                                'spearman_p_value': getattr(v, 'spearman_p_value', 1)
                            } for k, v in analysis_results['correlations'].items()
                        },
                        'phase_analysis': {
                            k: {
                                'avg_return': getattr(v, 'avg_return', 0),
                                'avg_volatility': getattr(v, 'avg_volatility', 0),
                                'count': getattr(v, 'count', 0)
                            } for k, v in analysis_results.get('phase_analysis', {}).items()
                        }
                    }
                }
                
            except Exception as e:
                print(f"  ⚠️  Error with {symbol}: {e}")
                # Create minimal fallback data
                all_data[symbol] = {
                    'metrics': [],
                    'analysis': {'correlations': {}, 'phase_analysis': {}}
                }
        
        return all_data
        
    except ImportError as e:
        print(f"⚠️  Import error: {e}")
        print("📝 Creating mock data for static demo...")
        return create_mock_data()

def create_mock_data():
    """Create mock data when real data fetching fails."""
    import random
    import math
    
    stocks = ["AAPL", "GOOGL", "MSFT", "RELIANCE.NS"]
    mock_data = {}
    
    for symbol in stocks:
        metrics = []
        base_price = random.uniform(100, 300)
        
        for i in range(90):
            date = datetime.now() - timedelta(days=90-i)
            price = base_price + random.uniform(-10, 10)
            daily_return = random.uniform(-0.05, 0.05)
            volatility = random.uniform(0.01, 0.04)
            moon_illumination = abs(math.sin(i * 0.1)) * 100
            phases = ["New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous", 
                     "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"]
            moon_phase = phases[i % 8]
            
            metrics.append({
                'date': date.isoformat(),
                'close_price': round(price, 2),
                'daily_return': round(daily_return, 4),
                'volatility_7d': round(volatility, 4),
                'moon_illumination': round(moon_illumination, 2),
                'moon_phase': moon_phase
            })
        
        mock_data[symbol] = {
            'metrics': metrics,
            'analysis': {
                'correlations': {
                    'returns_vs_illumination': {
                        'pearson_correlation': random.uniform(-0.3, 0.3),
                        'pearson_p_value': random.uniform(0.1, 0.9),
                        'spearman_correlation': random.uniform(-0.3, 0.3),
                        'spearman_p_value': random.uniform(0.1, 0.9)
                    }
                },
                'phase_analysis': {
                    phase: {
                        'avg_return': random.uniform(-0.02, 0.02),
                        'avg_volatility': random.uniform(0.01, 0.04),
                        'count': random.randint(8, 15)
                    } for phase in ["New Moon", "Full Moon", "First Quarter", "Last Quarter"]
                }
            }
        }
    
    return mock_data

def create_static_html(data):
    """Create complete static HTML dashboard."""
    print("🎨 Creating static HTML dashboard...")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌙 Stock Moon Dashboard - Interactive Demo</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .dashboard-header {{ 
            background: rgba(255,255,255,0.95); 
            backdrop-filter: blur(10px);
            border-radius: 15px;
            margin: 20px 0;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }}
        .chart-container {{ 
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
            margin: 20px 0; 
            padding: 25px; 
            border-radius: 15px; 
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }}
        .stats-card {{ 
            background: rgba(255,255,255,0.9);
            backdrop-filter: blur(10px);
            text-align: center; 
            padding: 20px; 
            margin: 10px; 
            border-radius: 15px; 
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        .stats-card:hover {{ transform: translateY(-5px); }}
        .stock-selector {{ 
            background: rgba(255,255,255,0.9);
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
        }}
        .btn-stock {{ 
            margin: 5px;
            border-radius: 25px;
            padding: 8px 20px;
            font-weight: 500;
        }}
        .correlation-badge {{
            font-size: 1.2em;
            padding: 10px 15px;
            border-radius: 25px;
            margin: 5px;
        }}
    </style>
</head>
<body>
    <div class="container-fluid">
        <!-- Header -->
        <div class="dashboard-header text-center">
            <h1 class="display-4 mb-3">🌙 Stock Moon Dashboard</h1>
            <p class="lead mb-3">Interactive Analysis of Stock Prices vs Moon Phases</p>
            <div class="row">
                <div class="col-md-3">
                    <div class="stats-card">
                        <h4 class="text-primary">{len(data)}</h4>
                        <p class="text-muted mb-0">Stocks Analyzed</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stats-card">
                        <h4 class="text-info">90</h4>
                        <p class="text-muted mb-0">Days of Data</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stats-card">
                        <h4 class="text-warning">8</h4>
                        <p class="text-muted mb-0">Moon Phases</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stats-card">
                        <h4 class="text-success">Live</h4>
                        <p class="text-muted mb-0">Static Demo</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Stock Selector -->
        <div class="stock-selector text-center">
            <h5 class="mb-3">📊 Select Stock to Analyze:</h5>
            <div class="btn-group" role="group">"""
    
    for i, symbol in enumerate(data.keys()):
        active = "active" if i == 0 else ""
        html_content += f"""
                <button type="button" class="btn btn-outline-primary btn-stock {active}" 
                        onclick="showStock('{symbol}')">{symbol}</button>"""
    
    html_content += f"""
            </div>
        </div>
        
        <!-- Charts Container -->
        <div id="charts-container">
            <!-- Charts will be dynamically loaded here -->
        </div>
        
        <!-- Correlations Summary -->
        <div class="chart-container">
            <h4 class="mb-4">📈 Correlation Summary</h4>
            <div id="correlations-summary" class="text-center">
                <!-- Correlation badges will be loaded here -->
            </div>
        </div>
        
        <!-- Footer -->
        <div class="chart-container text-center">
            <h5>🚀 Want More Features?</h5>
            <p>This is a static demo with sample data. For the full interactive dashboard:</p>
            <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                <a href="https://github.com/dineshrajdhanapathyDD/stock" class="btn btn-primary">
                    📂 View Source Code
                </a>
                <a href="https://render.com/deploy" class="btn btn-success">
                    🚀 Deploy Live Version
                </a>
            </div>
            <div class="mt-3">
                <small class="text-muted">
                    💡 Full version includes real-time data, more stocks, custom date ranges, and advanced analytics.
                </small>
            </div>
        </div>
    </div>
    
    <script>
        // Embedded data
        const stockData = {json.dumps(data, indent=2)};
        let currentStock = Object.keys(stockData)[0];
        
        function showStock(symbol) {{
            currentStock = symbol;
            
            // Update active button
            document.querySelectorAll('.btn-stock').forEach(btn => {{
                btn.classList.remove('active');
            }});
            event.target.classList.add('active');
            
            // Update charts
            updateCharts(symbol);
            updateCorrelations(symbol);
        }}
        
        function updateCharts(symbol) {{
            const data = stockData[symbol];
            const metrics = data.metrics;
            
            if (!metrics || metrics.length === 0) {{
                document.getElementById('charts-container').innerHTML = 
                    '<div class="chart-container"><div class="alert alert-warning">No data available for ' + symbol + '</div></div>';
                return;
            }}
            
            // Prepare data arrays
            const dates = metrics.map(m => m.date);
            const prices = metrics.map(m => m.close_price);
            const returns = metrics.map(m => m.daily_return * 100);
            const volatility = metrics.map(m => m.volatility_7d * 100);
            const illumination = metrics.map(m => m.moon_illumination);
            
            // Create charts container
            document.getElementById('charts-container').innerHTML = `
                <div class="row">
                    <div class="col-lg-6">
                        <div class="chart-container">
                            <h5>📈 ${{symbol}} Price Over Time</h5>
                            <div id="price-chart"></div>
                        </div>
                    </div>
                    <div class="col-lg-6">
                        <div class="chart-container">
                            <h5>🌙 Moon Illumination</h5>
                            <div id="moon-chart"></div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-6">
                        <div class="chart-container">
                            <h5>📊 Daily Returns vs Moon Illumination</h5>
                            <div id="scatter-chart"></div>
                        </div>
                    </div>
                    <div class="col-lg-6">
                        <div class="chart-container">
                            <h5>📈 Volatility Over Time</h5>
                            <div id="volatility-chart"></div>
                        </div>
                    </div>
                </div>
            `;
            
            // Price Chart
            Plotly.newPlot('price-chart', [{{
                x: dates,
                y: prices,
                type: 'scatter',
                mode: 'lines',
                name: 'Price',
                line: {{color: '#667eea', width: 3}}
            }}], {{
                margin: {{t: 20, r: 20, b: 40, l: 60}},
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                font: {{family: 'Segoe UI', size: 12}}
            }});
            
            // Moon Chart
            Plotly.newPlot('moon-chart', [{{
                x: dates,
                y: illumination,
                type: 'scatter',
                mode: 'lines',
                name: 'Illumination %',
                line: {{color: '#ffd700', width: 3}}
            }}], {{
                margin: {{t: 20, r: 20, b: 40, l: 60}},
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                font: {{family: 'Segoe UI', size: 12}}
            }});
            
            // Scatter Chart
            Plotly.newPlot('scatter-chart', [{{
                x: illumination,
                y: returns,
                type: 'scatter',
                mode: 'markers',
                name: 'Returns vs Moon',
                marker: {{
                    color: returns,
                    colorscale: 'RdYlBu',
                    size: 8,
                    opacity: 0.7
                }}
            }}], {{
                margin: {{t: 20, r: 20, b: 40, l: 60}},
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                font: {{family: 'Segoe UI', size: 12}},
                xaxis: {{title: 'Moon Illumination (%)'}},
                yaxis: {{title: 'Daily Return (%)'}}
            }});
            
            // Volatility Chart
            Plotly.newPlot('volatility-chart', [{{
                x: dates,
                y: volatility,
                type: 'scatter',
                mode: 'lines',
                name: 'Volatility',
                line: {{color: '#ff6b6b', width: 3}}
            }}], {{
                margin: {{t: 20, r: 20, b: 40, l: 60}},
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                font: {{family: 'Segoe UI', size: 12}},
                yaxis: {{title: 'Volatility (%)'}}
            }});
        }}
        
        function updateCorrelations(symbol) {{
            const correlations = stockData[symbol].analysis.correlations;
            let html = '';
            
            for (const [key, corr] of Object.entries(correlations)) {{
                const value = corr.pearson_correlation;
                const pValue = corr.pearson_p_value;
                const strength = Math.abs(value);
                
                let badgeClass = 'bg-secondary';
                if (strength > 0.3) badgeClass = 'bg-success';
                else if (strength > 0.1) badgeClass = 'bg-warning';
                
                html += `
                    <span class="badge correlation-badge ${{badgeClass}}">
                        ${{key.replace('_', ' ').toUpperCase()}}: ${{value.toFixed(3)}}
                        <small>(p=${{pValue.toFixed(3)}})</small>
                    </span>
                `;
            }}
            
            document.getElementById('correlations-summary').innerHTML = html || 
                '<div class="alert alert-info">No correlation data available</div>';
        }}
        
        // Initialize with first stock
        document.addEventListener('DOMContentLoaded', function() {{
            showStock(currentStock);
        }});
    </script>
    
    <footer class="text-center py-4 mt-5" style="background: rgba(255,255,255,0.1); color: white;">
        <div class="container">
            <p>&copy; 2025 Stock Moon Dashboard - Educational Research Tool</p>
            <p class="small">Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
        </div>
    </footer>
</body>
</html>"""
    
    return html_content

def main():
    """Build static dashboard."""
    print("🌙 Building Static Stock Moon Dashboard...")
    print("=" * 50)
    
    try:
        # Generate data
        data = generate_sample_data()
        
        # Create HTML
        html_content = create_static_html(data)
        
        # Write main dashboard
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Write data file for external access
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print("✅ Static dashboard generated successfully!")
        print("📁 Files created:")
        print("   - index.html (Complete interactive dashboard)")
        print("   - data.json (Raw data for external use)")
        print("")
        print("🌐 Ready for static hosting:")
        print("   - AWS Amplify")
        print("   - GitHub Pages") 
        print("   - Netlify")
        print("   - Vercel")
        print("")
        print("🚀 Features included:")
        print("   - Interactive stock selection")
        print("   - Real-time chart updates")
        print("   - Correlation analysis")
        print("   - Professional UI design")
        print("   - Mobile responsive")
        
        return True
        
    except Exception as e:
        print(f"❌ Error building static dashboard: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)