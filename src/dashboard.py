"""
Main dashboard application using Dash for the web interface.
Provides interactive visualizations and controls for stock-moon analysis.
"""

import dash
from dash import dcc, html, Input, Output, State, callback, dash_table, ALL
import dash.dependencies
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import json

try:
    # Try relative imports first (when run as module)
    from .cache_manager import cached_stock_data, cached_moon_data, get_performance_optimizer
    from .data_models import DataFactory, MoonPhase
    from .data_alignment import create_aligned_dataset
    from .metrics_calculator import MetricsCalculator
    from .statistical_analyzer import StatisticalAnalyzer
    from .visualizations import create_comprehensive_dashboard
    from .data_validation import validate_analysis_parameters, ValidationError
    from .stock_database import stock_db
    from .suggestions_api import suggestions_api
except ImportError:
    # Fall back to absolute imports (when run directly)
    from cache_manager import cached_stock_data, cached_moon_data, get_performance_optimizer
    from data_models import DataFactory, MoonPhase
    from data_alignment import create_aligned_dataset
    from metrics_calculator import MetricsCalculator
    from statistical_analyzer import StatisticalAnalyzer
    from visualizations import create_comprehensive_dashboard
    from data_validation import validate_analysis_parameters, ValidationError
    from stock_database import stock_db
    from suggestions_api import suggestions_api

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Data Weaver AI - Stock Moon Dashboard"

# Custom CSS for autocomplete
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .stock-autocomplete {
                position: relative;
            }
            .stock-suggestions {
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                z-index: 1000;
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 0.375rem;
                box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
                max-height: 300px;
                overflow-y: auto;
            }
            .stock-suggestion-item:hover {
                background-color: #f8f9fa;
                cursor: pointer;
            }
            .text-uppercase {
                text-transform: uppercase;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Default coordinates (Mumbai, India - for Indian stock analysis)
DEFAULT_LAT = 19.0760
DEFAULT_LON = 72.8777

# Layout components
def create_header():
    """Create the dashboard header."""
    return dbc.Row([
        dbc.Col([
            html.H1("🌙 Data Weaver AI", className="text-primary mb-0"),
            html.P("Uncovering relationships between stock prices and moon phases", 
                  className="text-muted")
        ], width=8),
        dbc.Col([
            html.Div([
                html.I(className="fas fa-chart-line fa-2x text-primary")
            ], className="text-end")
        ], width=4)
    ], className="mb-4 p-3 bg-light rounded")


def create_controls():
    """Create the parameter control panel."""
    return dbc.Card([
        dbc.CardHeader([
            html.H5("📊 Analysis Parameters", className="mb-0 d-inline"),
            dbc.Badge("Interactive Controls", color="info", className="ms-2")
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Stock Symbol", className="fw-bold"),
                    html.Div([
                        dbc.InputGroup([
                            dbc.Input(
                                id="stock-symbol",
                                type="text",
                                value="TCS.NS",
                                placeholder="Search stocks by name or symbol (e.g., TCS.NS, AAPL)...",
                                className="text-uppercase",
                                autoComplete="off"
                            ),
                            dbc.InputGroupText("📈")
                        ]),
                        html.Div(
                            id="stock-suggestions",
                            className="position-absolute w-100",
                            style={"zIndex": 1000, "display": "none"}
                        )
                    ], className="position-relative"),
                    dbc.FormText("Try: Apple, Google, Reliance, TCS", color="muted"),
                    html.Div([
                        html.Small("Quick Select:", className="text-muted me-2"),
                        dbc.ButtonGroup([
                            dbc.Button("AAPL", id={"type": "quick-stock", "symbol": "AAPL"}, 
                                     size="sm", outline=True, color="primary"),
                            dbc.Button("GOOGL", id={"type": "quick-stock", "symbol": "GOOGL"}, 
                                     size="sm", outline=True, color="primary"),
                            dbc.Button("RELIANCE.NS", id={"type": "quick-stock", "symbol": "RELIANCE.NS"}, 
                                     size="sm", outline=True, color="success"),
                            dbc.Button("TCS.NS", id={"type": "quick-stock", "symbol": "TCS.NS"}, 
                                     size="sm", outline=True, color="success")
                        ], size="sm")
                    ], className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Label("Start Date", className="fw-bold"),
                    dbc.InputGroup([
                        dbc.Input(
                            id="start-date",
                            type="date",
                            value=(datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
                        ),
                        dbc.InputGroupText("📅")
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Label("End Date", className="fw-bold"),
                    dbc.InputGroup([
                        dbc.Input(
                            id="end-date",
                            type="date",
                            value=(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
                        ),
                        dbc.InputGroupText("📅")
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Label("Rolling Window", className="fw-bold"),
                    dcc.Dropdown(
                        id="rolling-window",
                        options=[
                            {"label": "7 days", "value": 7},
                            {"label": "14 days", "value": 14},
                            {"label": "30 days", "value": 30}
                        ],
                        value=7,
                        className="mb-2"
                    )
                ], width=3)
            ], className="mb-3"),
            
            # Advanced options
            dbc.Row([
                dbc.Col([
                    dbc.Label("Chart Options", className="fw-bold"),
                    dbc.Checklist(
                        id="chart-options",
                        options=[
                            {"label": "Show Volume", "value": "volume"},
                            {"label": "Show Volatility", "value": "volatility"},
                            {"label": "Show Moon Phases", "value": "moon_phases"}
                        ],
                        value=["volume", "moon_phases"],
                        inline=True
                    )
                ], width=6),
                dbc.Col([
                    dbc.Label("Location (for Moon Data)", className="fw-bold"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Input(
                                id="latitude",
                                type="number",
                                value=DEFAULT_LAT,
                                placeholder="Latitude",
                                step=0.0001,
                                className="mb-1"
                            )
                        ], width=6),
                        dbc.Col([
                            dbc.Input(
                                id="longitude",
                                type="number",
                                value=DEFAULT_LON,
                                placeholder="Longitude",
                                step=0.0001,
                                className="mb-1"
                            )
                        ], width=6)
                    ])
                ], width=6)
            ], className="mb-3"),
            
            dbc.Row([
                dbc.Col([
                    dbc.Button(
                        [html.I(className="fas fa-play me-2"), "Analyze Data"],
                        id="analyze-button",
                        color="primary",
                        size="lg",
                        className="w-100"
                    )
                ], width=8),
                dbc.Col([
                    dbc.Button(
                        [html.I(className="fas fa-trash me-2"), "Clear Cache"],
                        id="clear-cache-button",
                        color="secondary",
                        outline=True,
                        className="w-100"
                    )
                ], width=2),
                dbc.Col([
                    dbc.Button(
                        [html.I(className="fas fa-download me-2"), "Export"],
                        id="export-button",
                        color="success",
                        outline=True,
                        className="w-100",
                        disabled=True
                    )
                ], width=2)
            ])
        ])
    ], className="mb-4")


def create_loading_component():
    """Create loading indicator."""
    return dcc.Loading(
        id="loading",
        type="default",
        children=[html.Div(id="loading-output")],
        color="#007bff"
    )


def create_status_bar():
    """Create status bar for performance metrics."""
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Div(id="status-info", children=[
                        dbc.Badge("Ready", color="success", className="me-2"),
                        html.Span("Click 'Analyze Data' to begin", className="text-muted")
                    ])
                ], width=8),
                dbc.Col([
                    html.Div(id="performance-stats", className="text-end text-muted")
                ], width=4)
            ])
        ], className="py-2")
    ], className="mb-3")


def create_results_container():
    """Create container for analysis results."""
    return html.Div(id="results-container", children=[
        # Placeholder for results
        dbc.Alert([
            html.H4("🌙 Welcome to Data Weaver AI", className="alert-heading"),
            html.P("This dashboard analyzes potential relationships between stock price behavior and lunar cycles."),
            html.Hr(),
            html.P("Configure your analysis parameters above and click 'Analyze Data' to begin.", className="mb-0")
        ], color="info", className="text-center")
    ])


def create_insights_panel():
    """Create panel for automated insights."""
    return dbc.Card([
        dbc.CardHeader([
            html.H5("🔍 Automated Insights", className="mb-0 d-inline"),
            dbc.Badge("AI Generated", color="warning", className="ms-2")
        ]),
        dbc.CardBody([
            html.Div(id="insights-content", children=[
                html.P("Insights will appear here after analysis.", className="text-muted text-center")
            ])
        ])
    ], className="mb-4")


def create_statistics_summary():
    """Create statistics summary cards."""
    return html.Div(id="statistics-summary", children=[
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("--", id="total-days", className="text-primary mb-0"),
                        html.P("Trading Days", className="text-muted mb-0")
                    ])
                ], className="text-center h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("--", id="correlation-strength", className="text-info mb-0"),
                        html.P("Correlation", className="text-muted mb-0")
                    ])
                ], className="text-center h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("--", id="volatility-avg", className="text-warning mb-0"),
                        html.P("Avg Volatility", className="text-muted mb-0")
                    ])
                ], className="text-center h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("--", id="significance-level", className="text-success mb-0"),
                        html.P("Significance", className="text-muted mb-0")
                    ])
                ], className="text-center h-100")
            ], width=3)
        ])
    ], className="mb-4")


# Main layout
app.layout = dbc.Container([
    create_header(),
    create_controls(),
    create_status_bar(),
    create_loading_component(),
    create_statistics_summary(),
    create_insights_panel(),
    create_results_container(),
    
    # Store components for data
    dcc.Store(id="stock-data-store"),
    dcc.Store(id="moon-data-store"),
    dcc.Store(id="analysis-results-store"),
    dcc.Store(id="chart-data-store"),
    
    # Interval component for periodic updates
    dcc.Interval(
        id="interval-component",
        interval=30*1000,  # Update every 30 seconds
        n_intervals=0,
        disabled=True
    )
], fluid=True, className="py-4")


# Autocomplete callbacks for stock search
@app.callback(
    [Output("stock-suggestions", "children"),
     Output("stock-suggestions", "style")],
    [Input("stock-symbol", "value")],
    prevent_initial_call=True
)
def update_stock_suggestions(search_query):
    """Update stock suggestions based on search query."""
    try:
        if not search_query or len(search_query.strip()) < 1:
            return html.Div(), {"display": "none"}
        
        # Search for matching stocks
        suggestions = stock_db.search(search_query, limit=8)
        
        if not suggestions:
            return html.Div(), {"display": "none"}
        
        # Create suggestion items
        suggestion_items = []
        for stock in suggestions:
            suggestion_items.append(
                dbc.ListGroupItem([
                    html.Div([
                        html.Strong(stock["symbol"], className="text-primary"),
                        html.Span(f" - {stock['name']}", className="text-muted ms-2"),
                        dbc.Badge(stock["market"], color="secondary", size="sm", className="ms-2"),
                        html.Br(),
                        html.Small(stock["sector"], className="text-muted")
                    ])
                ],
                id={"type": "stock-suggestion", "symbol": stock["symbol"]},
                action=True,
                className="py-2"
                )
            )
        
        suggestions_div = dbc.ListGroup(
            suggestion_items,
            className="shadow-sm border"
        )
        
        return suggestions_div, {
            "display": "block",
            "zIndex": 1000,
            "backgroundColor": "white",
            "border": "1px solid #dee2e6",
            "borderRadius": "0.375rem",
            "maxHeight": "300px",
            "overflowY": "auto"
        }
    except Exception as e:
        # Return empty div on error
        return html.Div(), {"display": "none"}


@app.callback(
    Output("stock-symbol", "value"),
    [Input({"type": "stock-suggestion", "symbol": ALL}, "n_clicks")],
    [State({"type": "stock-suggestion", "symbol": ALL}, "id")],
    prevent_initial_call=True
)
def select_stock_suggestion(n_clicks_list, suggestion_ids):
    """Handle stock suggestion selection."""
    try:
        if not n_clicks_list or not suggestion_ids or not any(n_clicks_list):
            return dash.no_update
        
        # Find which suggestion was clicked
        for i, n_clicks in enumerate(n_clicks_list):
            if n_clicks and i < len(suggestion_ids):
                return suggestion_ids[i]["symbol"]
        
        return dash.no_update
    except Exception:
        return dash.no_update


@app.callback(
    Output("stock-suggestions", "style", allow_duplicate=True),
    [Input("stock-symbol", "n_blur")],
    prevent_initial_call=True
)
def hide_suggestions_on_blur(n_blur):
    """Hide suggestions when input loses focus."""
    return {"display": "none"}


@app.callback(
    Output("stock-symbol", "value", allow_duplicate=True),
    [Input({"type": "quick-stock", "symbol": ALL}, "n_clicks")],
    [State({"type": "quick-stock", "symbol": ALL}, "id")],
    prevent_initial_call=True
)
def select_quick_stock(n_clicks_list, button_ids):
    """Handle quick stock selection buttons."""
    try:
        if not n_clicks_list or not button_ids or not any(n_clicks_list):
            return dash.no_update
        
        # Find which button was clicked
        for i, n_clicks in enumerate(n_clicks_list):
            if n_clicks and i < len(button_ids):
                return button_ids[i]["symbol"]
        
        return dash.no_update
    except Exception:
        return dash.no_update


@app.callback(
    [Output("stock-data-store", "data"),
     Output("moon-data-store", "data"),
     Output("analysis-results-store", "data"),
     Output("loading-output", "children"),
     Output("status-info", "children"),
     Output("export-button", "disabled")],
    [Input("analyze-button", "n_clicks")],
    [State("stock-symbol", "value"),
     State("start-date", "value"),
     State("end-date", "value"),
     State("rolling-window", "value"),
     State("latitude", "value"),
     State("longitude", "value")]
)
def fetch_and_analyze_data(n_clicks, symbol, start_date, end_date, rolling_window, latitude, longitude):
    """Fetch and analyze data when analyze button is clicked."""
    if not n_clicks:
        return None, None, None, "", [
            dbc.Badge("Ready", color="success", className="me-2"),
            html.Span("Click 'Analyze Data' to begin", className="text-muted")
        ], True
    
    try:
        # Validate parameters
        validated_params = validate_analysis_parameters(
            symbol, start_date, end_date, rolling_window, latitude, longitude
        )
        
        logger.info(f"Starting analysis for {validated_params['symbol']}")
        
        # Update status
        status_loading = [
            dbc.Badge("Loading", color="warning", className="me-2"),
            html.Span(f"Fetching data for {validated_params['symbol']}...", className="text-muted")
        ]
        
        # Fetch data using cached functions
        stock_data = cached_stock_data(
            validated_params['symbol'],
            validated_params['start_date'],
            validated_params['end_date']
        )
        
        moon_data = cached_moon_data(
            validated_params['latitude'],
            validated_params['longitude'],
            validated_params['start_date'],
            validated_params['end_date']
        )
        
        # Convert to data objects
        stock_objects = [DataFactory.create_stock_data_from_dict(item) for item in stock_data]
        moon_objects = [DataFactory.create_moon_data_from_dict(item) for item in moon_data]
        
        # Align data
        aligned_data = create_aligned_dataset(stock_objects, moon_objects)
        
        # Calculate metrics
        calculator = MetricsCalculator()
        metrics_data = calculator.calculate_all_metrics(aligned_data, validated_params['rolling_window'])
        
        # Perform statistical analysis
        analyzer = StatisticalAnalyzer()
        analysis_results = analyzer.perform_comprehensive_analysis(metrics_data)
        
        # Prepare results for storage
        results = {
            'metrics_data': [
                {
                    'date': point.date.isoformat(),
                    'close': point.close,
                    'daily_return': point.daily_return,
                    'volatility_7d': point.volatility_7d,
                    'phase_code': int(point.phase_code),
                    'illumination': point.illumination,
                    'is_full_moon_window': point.is_full_moon_window
                }
                for point in metrics_data
            ],
            'analysis_results': {
                'correlations': {
                    name: {
                        'pearson_correlation': corr.pearson_correlation,
                        'pearson_p_value': corr.pearson_p_value,
                        'spearman_correlation': corr.spearman_correlation,
                        'spearman_p_value': corr.spearman_p_value,
                        'interpretation': corr.interpretation
                    }
                    for name, corr in analysis_results['correlations'].items()
                },
                'phase_metrics': [
                    {
                        'phase': metric.phase.name,
                        'avg_volatility': metric.avg_volatility,
                        'green_day_percentage': metric.green_day_percentage,
                        'mean_return': metric.mean_return,
                        'sample_count': metric.sample_count
                    }
                    for metric in analysis_results['phase_analysis'].phase_metrics
                ],
                'full_moon_analysis': analysis_results.get('full_moon_analysis', {}),
                'summaries': {
                    name: {
                        'mean': summary.mean,
                        'std': summary.std,
                        'sample_size': summary.sample_size
                    }
                    for name, summary in analysis_results.get('summaries', {}).items()
                }
            }
        }
        
        logger.info(f"Analysis completed for {len(metrics_data)} data points")
        
        # Success status
        status_success = [
            dbc.Badge("Complete", color="success", className="me-2"),
            html.Span(f"Analyzed {len(metrics_data)} data points", className="text-muted")
        ]
        
        return stock_data, moon_data, results, "", status_success, False
        
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        error_status = [
            dbc.Badge("Error", color="danger", className="me-2"),
            html.Span(f"Validation error: {str(e)}", className="text-muted")
        ]
        return None, None, None, "", error_status, True
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        error_status = [
            dbc.Badge("Error", color="danger", className="me-2"),
            html.Span(f"Analysis failed: {str(e)}", className="text-muted")
        ]
        return None, None, None, "", error_status, True


@app.callback(
    [Output("results-container", "children"),
     Output("total-days", "children"),
     Output("correlation-strength", "children"),
     Output("volatility-avg", "children"),
     Output("significance-level", "children"),
     Output("insights-content", "children")],
    [Input("analysis-results-store", "data")],
    [State("stock-symbol", "value"),
     State("chart-options", "value")]
)
def update_results(analysis_data, symbol, chart_options):
    """Update results container with comprehensive analysis."""
    if not analysis_data:
        return [
            dbc.Alert([
                html.H4("🌙 Welcome to Data Weaver AI", className="alert-heading"),
                html.P("This dashboard analyzes potential relationships between stock price behavior and lunar cycles."),
                html.Hr(),
                html.P("Configure your analysis parameters above and click 'Analyze Data' to begin.", className="mb-0")
            ], color="info", className="text-center")
        ], "--", "--", "--", "--", [
            html.P("Insights will appear here after analysis.", className="text-muted text-center")
        ]
    
    try:
        # Extract data
        metrics_data = analysis_data['metrics_data']
        analysis_results = analysis_data['analysis_results']
        
        # Recreate data objects for visualization
        combined_data = []
        for item in metrics_data:
            point_data = {
                'date': item['date'],
                'close': item['close'],
                'daily_return': item['daily_return'],
                'volatility_7d': item['volatility_7d'],
                'phase_code': item['phase_code'],
                'illumination': item['illumination'],
                'is_full_moon_window': item['is_full_moon_window']
            }
            combined_data.append(point_data)
        
        # Convert to DataFrame for visualization
        df = pd.DataFrame(combined_data)
        df['date'] = pd.to_datetime(df['date'])
        
        # Create visualizations
        charts = create_dashboard_charts(df, analysis_results, symbol, chart_options or [])
        
        # Update summary statistics
        total_days = len(df)
        
        # Get strongest correlation
        correlations = analysis_results.get('correlations', {})
        strongest_corr = 0
        for corr_data in correlations.values():
            abs_corr = abs(corr_data.get('pearson_correlation', 0))
            if abs_corr > abs(strongest_corr):
                strongest_corr = corr_data.get('pearson_correlation', 0)
        
        # Average volatility
        volatilities = [item['volatility_7d'] for item in metrics_data if item['volatility_7d'] is not None]
        avg_volatility = sum(volatilities) / len(volatilities) if volatilities else 0
        
        # Significance level (lowest p-value)
        min_p_value = 1.0
        for corr_data in correlations.values():
            p_val = corr_data.get('pearson_p_value', 1.0)
            if p_val < min_p_value:
                min_p_value = p_val
        
        # Generate insights
        insights = generate_insights(analysis_results, total_days)
        
        return (
            charts,
            str(total_days),
            f"{strongest_corr:.3f}",
            f"{avg_volatility:.2f}%",
            f"p={min_p_value:.3f}",
            insights
        )
        
    except Exception as e:
        logger.error(f"Error updating results: {str(e)}")
        return [
            dbc.Alert(f"Error updating results: {str(e)}", color="danger")
        ], "--", "--", "--", "--", [
            html.P("Error generating insights.", className="text-danger text-center")
        ]


@app.callback(
    Output("performance-stats", "children"),
    [Input("interval-component", "n_intervals")]
)
def update_performance_stats(n_intervals):
    """Update performance statistics."""
    try:
        optimizer = get_performance_optimizer()
        stats = optimizer.get_performance_stats()
        
        return html.Small([
            f"API Calls: {stats['api_calls']} | ",
            f"Cache Hit Rate: {stats['cache_stats']['hit_rate_percent']:.1f}% | ",
            f"Avg Response: {stats['avg_processing_time']:.2f}s"
        ])
    except:
        return ""


@app.callback(
    Output("status-info", "children", allow_duplicate=True),
    [Input("clear-cache-button", "n_clicks")],
    prevent_initial_call=True
)
def clear_cache(n_clicks):
    """Clear cache when button is clicked."""
    if n_clicks:
        try:
            try:
                from .cache_manager import get_cache_manager
            except ImportError:
                from cache_manager import get_cache_manager
            cache_manager = get_cache_manager()
            cache_manager.clear()
            
            return [
                dbc.Badge("Cache Cleared", color="info", className="me-2"),
                html.Span("Cache has been cleared", className="text-muted")
            ]
        except Exception as e:
            return [
                dbc.Badge("Error", color="danger", className="me-2"),
                html.Span(f"Failed to clear cache: {str(e)}", className="text-muted")
            ]
    
    return dash.no_update


def create_time_series_chart(stock_df, moon_df, symbol):
    """Create time series chart with stock prices and moon phase markers."""
    fig = go.Figure()
    
    # Add stock price line
    fig.add_trace(go.Scatter(
        x=stock_df['date'],
        y=stock_df['close'],
        mode='lines',
        name=f'{symbol} Close Price',
        line=dict(color='blue', width=2)
    ))
    
    # Add moon phase markers
    moon_colors = {
        0: 'black',      # New
        1: 'gray',       # Waxing Crescent
        2: 'lightgray',  # First Quarter
        3: 'silver',     # Waxing Gibbous
        4: 'gold',       # Full
        5: 'silver',     # Waning Gibbous
        6: 'lightgray',  # Last Quarter
        7: 'gray'        # Waning Crescent
    }
    
    moon_names = {
        0: 'New Moon',
        1: 'Waxing Crescent',
        2: 'First Quarter',
        3: 'Waxing Gibbous',
        4: 'Full Moon',
        5: 'Waning Gibbous',
        6: 'Last Quarter',
        7: 'Waning Crescent'
    }
    
    # Merge dataframes to align dates
    merged_df = pd.merge(stock_df, moon_df, on='date', how='inner')
    
    for phase in range(8):
        phase_data = merged_df[merged_df['phase_code'] == phase]
        if not phase_data.empty:
            fig.add_trace(go.Scatter(
                x=phase_data['date'],
                y=phase_data['close'],
                mode='markers',
                name=moon_names[phase],
                marker=dict(
                    color=moon_colors[phase],
                    size=8,
                    symbol='circle'
                ),
                showlegend=True
            ))
    
    fig.update_layout(
        title=f'{symbol} Stock Price with Moon Phase Markers',
        xaxis_title='Date',
        yaxis_title='Price ($)',
        hovermode='x unified',
        height=500
    )
    
    return fig


def create_summary_statistics(stock_df, moon_df):
    """Create summary statistics cards."""
    # Calculate basic statistics
    total_days = len(stock_df)
    price_change = ((stock_df['close'].iloc[-1] - stock_df['close'].iloc[0]) / 
                   stock_df['close'].iloc[0] * 100)
    
    # Calculate daily returns
    stock_df['daily_return'] = stock_df['close'].pct_change() * 100
    avg_return = stock_df['daily_return'].mean()
    volatility = stock_df['daily_return'].std()
    
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{total_days}", className="text-primary"),
                    html.P("Trading Days", className="mb-0")
                ])
            ], className="text-center")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{price_change:.1f}%", className="text-success" if price_change > 0 else "text-danger"),
                    html.P("Total Return", className="mb-0")
                ])
            ], className="text-center")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{avg_return:.2f}%", className="text-primary"),
                    html.P("Avg Daily Return", className="mb-0")
                ])
            ], className="text-center")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{volatility:.2f}%", className="text-warning"),
                    html.P("Volatility", className="mb-0")
                ])
            ], className="text-center")
        ], width=3)
    ], className="mb-4")


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)


def create_dashboard_charts(df, analysis_results, symbol, chart_options):
    """Create dashboard charts based on analysis results."""
    charts = []
    
    # Time Series Chart
    fig_timeseries = create_time_series_chart(df, symbol, chart_options)
    charts.append(
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5(f"📈 {symbol} Price Analysis", className="mb-0 d-inline"),
                        dbc.Badge(f"{len(df)} days", color="primary", className="ms-2")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(figure=fig_timeseries, config={'displayModeBar': True})
                    ])
                ])
            ], width=12)
        ], className="mb-4")
    )
    
    # Correlation Analysis
    correlations = analysis_results.get('correlations', {})
    if correlations:
        correlation_charts = create_correlation_charts(df, correlations)
        charts.append(correlation_charts)
    
    # Phase Analysis
    phase_metrics = analysis_results.get('phase_metrics', [])
    if phase_metrics:
        phase_charts = create_phase_analysis_charts(phase_metrics)
        charts.append(phase_charts)
    
    # Full Moon Analysis
    full_moon_analysis = analysis_results.get('full_moon_analysis', {})
    if full_moon_analysis and 'return_comparison' in full_moon_analysis:
        full_moon_chart = create_full_moon_analysis_chart(full_moon_analysis)
        charts.append(full_moon_chart)
    
    return charts


def create_time_series_chart(df, symbol, chart_options):
    """Create time series chart with stock prices."""
    fig = go.Figure()
    
    # Add price line
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['close'],
        mode='lines',
        name=f'{symbol} Price',
        line=dict(color='blue', width=2)
    ))
    
    # Add moon phase markers if enabled
    if 'moon_phases' in chart_options:
        # Color points by moon phase
        phase_colors = {
            0: 'black',      # New
            1: 'gray',       # Waxing Crescent
            2: 'lightgray',  # First Quarter
            3: 'silver',     # Waxing Gibbous
            4: 'gold',       # Full
            5: 'silver',     # Waning Gibbous
            6: 'lightgray',  # Last Quarter
            7: 'gray'        # Waning Crescent
        }
        
        for phase in range(8):
            phase_data = df[df['phase_code'] == phase]
            if not phase_data.empty:
                fig.add_trace(go.Scatter(
                    x=phase_data['date'],
                    y=phase_data['close'],
                    mode='markers',
                    name=f'Phase {phase}',
                    marker=dict(color=phase_colors[phase], size=6),
                    showlegend=False
                ))
    
    # Add volatility if enabled
    if 'volatility' in chart_options:
        volatility_data = df[df['volatility_7d'].notna()]
        if not volatility_data.empty:
            fig.add_trace(go.Scatter(
                x=volatility_data['date'],
                y=volatility_data['volatility_7d'],
                mode='lines',
                name='Volatility',
                yaxis='y2',
                line=dict(color='red', width=1, dash='dash')
            ))
    
    fig.update_layout(
        title=f'{symbol} Stock Price Analysis',
        xaxis_title='Date',
        yaxis_title='Price ($)',
        template='plotly_white',
        height=500,
        hovermode='x unified'
    )
    
    if 'volatility' in chart_options:
        fig.update_layout(
            yaxis2=dict(
                title='Volatility (%)',
                overlaying='y',
                side='right'
            )
        )
    
    return fig


def create_correlation_charts(df, correlations):
    """Create correlation analysis charts."""
    charts = []
    
    for name, corr_data in correlations.items():
        if 'illumination' in name:
            # Create scatter plot
            y_col = 'daily_return' if 'returns' in name else 'volatility_7d'
            y_data = df[df[y_col].notna()]
            
            if not y_data.empty:
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=y_data['illumination'],
                    y=y_data[y_col],
                    mode='markers',
                    marker=dict(
                        color=y_data[y_col],
                        colorscale='Viridis',
                        size=8,
                        opacity=0.7
                    ),
                    name='Data Points'
                ))
                
                # Add trend line
                if len(y_data) > 2:
                    z = np.polyfit(y_data['illumination'], y_data[y_col], 1)
                    p = np.poly1d(z)
                    x_trend = np.linspace(y_data['illumination'].min(), y_data['illumination'].max(), 100)
                    y_trend = p(x_trend)
                    
                    fig.add_trace(go.Scatter(
                        x=x_trend,
                        y=y_trend,
                        mode='lines',
                        name='Trend Line',
                        line=dict(color='red', dash='dash')
                    ))
                
                fig.update_layout(
                    title=f'{name.replace("_", " ").title()}',
                    xaxis_title='Moon Illumination (%)',
                    yaxis_title=y_col.replace('_', ' ').title(),
                    template='plotly_white',
                    height=400
                )
                
                # Add correlation info
                corr_text = f"r = {corr_data['pearson_correlation']:.3f}, p = {corr_data['pearson_p_value']:.3f}"
                fig.add_annotation(
                    text=corr_text,
                    xref="paper", yref="paper",
                    x=0.02, y=0.98,
                    showarrow=False,
                    bgcolor="white",
                    bordercolor="gray",
                    borderwidth=1
                )
                
                charts.append(
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H6(name.replace('_', ' ').title(), className="mb-0")),
                            dbc.CardBody([
                                dcc.Graph(figure=fig, config={'displayModeBar': False})
                            ])
                        ])
                    ], width=6)
                )
    
    if charts:
        return dbc.Row(charts, className="mb-4")
    return html.Div()


def create_phase_analysis_charts(phase_metrics):
    """Create moon phase analysis charts."""
    phases = [metric['phase'] for metric in phase_metrics]
    volatilities = [metric['avg_volatility'] for metric in phase_metrics]
    returns = [metric['mean_return'] for metric in phase_metrics]
    
    # Volatility by phase
    fig_vol = go.Figure()
    fig_vol.add_trace(go.Bar(
        x=phases,
        y=volatilities,
        name='Avg Volatility',
        marker_color='lightblue'
    ))
    
    fig_vol.update_layout(
        title='Average Volatility by Moon Phase',
        xaxis_title='Moon Phase',
        yaxis_title='Volatility (%)',
        template='plotly_white',
        height=400
    )
    
    # Returns by phase
    fig_ret = go.Figure()
    colors = ['green' if r > 0 else 'red' for r in returns]
    fig_ret.add_trace(go.Bar(
        x=phases,
        y=returns,
        name='Mean Return',
        marker_color=colors
    ))
    
    fig_ret.update_layout(
        title='Mean Returns by Moon Phase',
        xaxis_title='Moon Phase',
        yaxis_title='Return (%)',
        template='plotly_white',
        height=400
    )
    
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H6("Volatility Analysis", className="mb-0")),
                dbc.CardBody([
                    dcc.Graph(figure=fig_vol, config={'displayModeBar': False})
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H6("Returns Analysis", className="mb-0")),
                dbc.CardBody([
                    dcc.Graph(figure=fig_ret, config={'displayModeBar': False})
                ])
            ])
        ], width=6)
    ], className="mb-4")


def create_full_moon_analysis_chart(full_moon_analysis):
    """Create full moon analysis chart."""
    return_comp = full_moon_analysis.get('return_comparison', {})
    
    if not return_comp or 'group1_stats' not in return_comp:
        return html.Div()
    
    # Create comparison chart
    fig = go.Figure()
    
    categories = ['Full Moon Window', 'Baseline']
    means = [
        return_comp['group1_stats']['mean'],
        return_comp['group2_stats']['mean']
    ]
    stds = [
        return_comp['group1_stats']['std'],
        return_comp['group2_stats']['std']
    ]
    
    fig.add_trace(go.Bar(
        x=categories,
        y=means,
        error_y=dict(type='data', array=stds),
        name='Mean Return',
        marker_color=['gold', 'lightblue']
    ))
    
    fig.update_layout(
        title='Full Moon Window vs Baseline Returns',
        xaxis_title='Period',
        yaxis_title='Mean Return (%)',
        template='plotly_white',
        height=400
    )
    
    # Add significance annotation
    p_value = return_comp.get('t_test', {}).get('p_value', 1.0)
    significance = "Significant" if p_value < 0.05 else "Not Significant"
    
    fig.add_annotation(
        text=f"p-value: {p_value:.3f} ({significance})",
        xref="paper", yref="paper",
        x=0.02, y=0.98,
        showarrow=False,
        bgcolor="white",
        bordercolor="gray",
        borderwidth=1
    )
    
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H6("Full Moon Effect Analysis", className="mb-0")),
                dbc.CardBody([
                    dcc.Graph(figure=fig, config={'displayModeBar': False})
                ])
            ])
        ], width=12)
    ], className="mb-4")


def generate_insights(analysis_results, total_days):
    """Generate automated insights from analysis results."""
    insights = []
    
    # Data summary
    insights.append(
        dbc.Alert([
            html.H6("📊 Data Summary", className="alert-heading"),
            html.P(f"Analyzed {total_days} trading days of stock and moon phase data.")
        ], color="info")
    )
    
    # Correlation insights
    correlations = analysis_results.get('correlations', {})
    strongest_corr = None
    strongest_corr_name = None
    
    for name, corr_data in correlations.items():
        abs_corr = abs(corr_data.get('pearson_correlation', 0))
        if strongest_corr is None or abs_corr > abs(strongest_corr):
            strongest_corr = corr_data.get('pearson_correlation', 0)
            strongest_corr_name = name
    
    if strongest_corr is not None:
        corr_strength = "strong" if abs(strongest_corr) > 0.5 else "moderate" if abs(strongest_corr) > 0.3 else "weak"
        corr_direction = "positive" if strongest_corr > 0 else "negative"
        
        insights.append(
            dbc.Alert([
                html.H6("🔗 Correlation Analysis", className="alert-heading"),
                html.P(f"The strongest correlation found was a {corr_strength} {corr_direction} "
                      f"relationship ({strongest_corr:.3f}) in {strongest_corr_name.replace('_', ' ')}.")
            ], color="primary")
        )
    
    # Phase analysis insights
    phase_metrics = analysis_results.get('phase_metrics', [])
    if phase_metrics:
        # Find phase with highest volatility
        highest_vol_phase = max(phase_metrics, key=lambda x: x['avg_volatility'])
        lowest_vol_phase = min(phase_metrics, key=lambda x: x['avg_volatility'])
        
        insights.append(
            dbc.Alert([
                html.H6("🌙 Moon Phase Analysis", className="alert-heading"),
                html.P(f"Highest volatility observed during {highest_vol_phase['phase']} "
                      f"({highest_vol_phase['avg_volatility']:.2f}%). "
                      f"Lowest during {lowest_vol_phase['phase']} "
                      f"({lowest_vol_phase['avg_volatility']:.2f}%).")
            ], color="warning")
        )
    
    # Full moon analysis
    full_moon_analysis = analysis_results.get('full_moon_analysis', {})
    if full_moon_analysis and 'return_comparison' in full_moon_analysis:
        return_comp = full_moon_analysis['return_comparison']
        p_value = return_comp.get('t_test', {}).get('p_value', 1.0)
        
        if p_value < 0.05:
            insights.append(
                dbc.Alert([
                    html.H6("🌕 Full Moon Effect", className="alert-heading"),
                    html.P(f"Statistically significant difference found during full moon windows "
                          f"(p = {p_value:.3f}). This suggests lunar cycles may influence market behavior.")
                ], color="success")
            )
        else:
            insights.append(
                dbc.Alert([
                    html.H6("🌕 Full Moon Effect", className="alert-heading"),
                    html.P(f"No statistically significant full moon effect detected "
                          f"(p = {p_value:.3f}). Market behavior appears independent of lunar cycles.")
                ], color="secondary")
            )
    
    return insights


# Helper functions for the original simple charts
def create_time_series_chart(stock_df, moon_df, symbol):
    """Create simple time series chart (legacy function)."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=stock_df['date'],
        y=stock_df['close'],
        mode='lines',
        name=f'{symbol} Close Price',
        line=dict(color='blue', width=2)
    ))
    
    fig.update_layout(
        title=f'{symbol} Stock Price',
        xaxis_title='Date',
        yaxis_title='Price ($)',
        template='plotly_white',
        height=400
    )
    
    return fig


def create_summary_statistics(stock_df, moon_df):
    """Create summary statistics (legacy function)."""
    total_days = len(stock_df)
    price_change = ((stock_df['close'].iloc[-1] - stock_df['close'].iloc[0]) / 
                   stock_df['close'].iloc[0] * 100) if len(stock_df) > 1 else 0
    
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{total_days}", className="text-primary"),
                    html.P("Trading Days", className="mb-0")
                ])
            ], className="text-center")
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{price_change:.1f}%", className="text-success" if price_change > 0 else "text-danger"),
                    html.P("Total Return", className="mb-0")
                ])
            ], className="text-center")
        ], width=6)
    ])


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)