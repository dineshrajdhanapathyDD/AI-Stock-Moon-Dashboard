"""
Visualization components for the Stock Moon Dashboard.
Implements interactive charts using Plotly for time series, scatter plots, and more.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import logging

try:
    from .data_models import CombinedDataPoint, MoonPhase, PhaseMetric
    from .statistical_analyzer import CorrelationAnalysis, PhaseComparisonResult
except ImportError:
    from data_models import CombinedDataPoint, MoonPhase, PhaseMetric
    from statistical_analyzer import CorrelationAnalysis, PhaseComparisonResult

logger = logging.getLogger(__name__)


class TimeSeriesChart:
    """Time series chart component for stock prices with moon phase overlays."""
    
    def __init__(self, title: str = "Stock Price with Moon Phases"):
        """
        Initialize time series chart.
        
        Args:
            title: Chart title
        """
        self.title = title
        self.moon_phase_colors = {
            MoonPhase.NEW: '#1f1f1f',           # Dark gray
            MoonPhase.WAXING_CRESCENT: '#4a4a4a',  # Gray
            MoonPhase.FIRST_QUARTER: '#7a7a7a',    # Light gray
            MoonPhase.WAXING_GIBBOUS: '#b8860b',   # Dark goldenrod
            MoonPhase.FULL: '#ffd700',             # Gold
            MoonPhase.WANING_GIBBOUS: '#daa520',   # Goldenrod
            MoonPhase.LAST_QUARTER: '#a9a9a9',     # Dark gray
            MoonPhase.WANING_CRESCENT: '#696969'   # Dim gray
        }
        
        self.moon_phase_symbols = {
            MoonPhase.NEW: 'circle',
            MoonPhase.WAXING_CRESCENT: 'circle-open',
            MoonPhase.FIRST_QUARTER: 'square',
            MoonPhase.WAXING_GIBBOUS: 'diamond',
            MoonPhase.FULL: 'star',
            MoonPhase.WANING_GIBBOUS: 'diamond-open',
            MoonPhase.LAST_QUARTER: 'square-open',
            MoonPhase.WANING_CRESCENT: 'circle-dot'
        }
    
    def create_chart(self, data: List[CombinedDataPoint], 
                    show_volume: bool = True, 
                    show_moon_phases: bool = True,
                    show_volatility: bool = False) -> go.Figure:
        """
        Create time series chart with stock prices and moon phase markers.
        
        Args:
            data: List of combined data points
            show_volume: Whether to show volume subplot
            show_moon_phases: Whether to show moon phase markers
            show_volatility: Whether to show volatility subplot
            
        Returns:
            Plotly figure object
        """
        if not data:
            return self._create_empty_chart()
        
        # Determine subplot configuration
        subplot_count = 1
        subplot_titles = [f"{self.title}"]
        
        if show_volume:
            subplot_count += 1
            subplot_titles.append("Volume")
        
        if show_volatility:
            subplot_count += 1
            subplot_titles.append("Volatility")
        
        # Create subplots
        fig = make_subplots(
            rows=subplot_count,
            cols=1,
            shared_xaxes=True,
            subplot_titles=subplot_titles,
            vertical_spacing=0.05,
            row_heights=[0.6] + [0.2] * (subplot_count - 1) if subplot_count > 1 else [1.0]
        )
        
        # Extract data for plotting
        dates = [point.date for point in data]
        closes = [point.close for point in data]
        opens = [point.open for point in data]
        highs = [point.high for point in data]
        lows = [point.low for point in data]
        volumes = [point.volume for point in data]
        
        # Add candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=dates,
                open=opens,
                high=highs,
                low=lows,
                close=closes,
                name="Price",
                increasing_line_color='green',
                decreasing_line_color='red'
            ),
            row=1, col=1
        )
        
        # Add moon phase markers
        if show_moon_phases:
            self._add_moon_phase_markers(fig, data, row=1)
        
        # Add volume subplot
        if show_volume:
            volume_colors = ['green' if c >= o else 'red' 
                           for c, o in zip(closes, opens)]
            
            fig.add_trace(
                go.Bar(
                    x=dates,
                    y=volumes,
                    name="Volume",
                    marker_color=volume_colors,
                    opacity=0.7
                ),
                row=2, col=1
            )
        
        # Add volatility subplot
        if show_volatility:
            volatilities = [point.volatility_7d for point in data]
            valid_volatilities = [(d, v) for d, v in zip(dates, volatilities) if v is not None]
            
            if valid_volatilities:
                vol_dates, vol_values = zip(*valid_volatilities)
                
                fig.add_trace(
                    go.Scatter(
                        x=vol_dates,
                        y=vol_values,
                        mode='lines',
                        name="7-day Volatility",
                        line=dict(color='purple', width=2)
                    ),
                    row=subplot_count, col=1
                )
        
        # Update layout
        fig.update_layout(
            title=self.title,
            xaxis_title="Date",
            yaxis_title="Price ($)",
            template="plotly_white",
            height=400 + (200 * (subplot_count - 1)),
            showlegend=True,
            hovermode='x unified'
        )
        
        # Update x-axis for all subplots
        fig.update_xaxes(rangeslider_visible=False)
        
        return fig
    
    def _add_moon_phase_markers(self, fig: go.Figure, data: List[CombinedDataPoint], 
                               row: int = 1) -> None:
        """Add moon phase markers to the chart."""
        # Group data by moon phase
        phase_groups = {}
        for point in data:
            if point.phase_code not in phase_groups:
                phase_groups[point.phase_code] = []
            phase_groups[point.phase_code].append(point)
        
        # Add scatter plot for each phase
        for phase, points in phase_groups.items():
            if not points:
                continue
            
            dates = [p.date for p in points]
            prices = [p.close for p in points]
            illuminations = [p.illumination for p in points]
            
            # Create hover text
            hover_text = [
                f"Phase: {phase.name}<br>"
                f"Illumination: {illum:.1f}%<br>"
                f"Price: ${price:.2f}<br>"
                f"Date: {date.strftime('%Y-%m-%d')}"
                for date, price, illum in zip(dates, prices, illuminations)
            ]
            
            fig.add_trace(
                go.Scatter(
                    x=dates,
                    y=prices,
                    mode='markers',
                    name=phase.name,
                    marker=dict(
                        color=self.moon_phase_colors[phase],
                        size=8,
                        symbol=self.moon_phase_symbols[phase],
                        line=dict(width=1, color='white')
                    ),
                    hovertext=hover_text,
                    hoverinfo='text'
                ),
                row=row, col=1
            )
    
    def _create_empty_chart(self) -> go.Figure:
        """Create empty chart when no data is available."""
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=20, color="gray")
        )
        fig.update_layout(
            title=self.title,
            template="plotly_white",
            height=400
        )
        return fig


class ScatterPlot:
    """Scatter plot component for correlation analysis."""
    
    def __init__(self, title: str = "Correlation Analysis"):
        """
        Initialize scatter plot.
        
        Args:
            title: Chart title
        """
        self.title = title
    
    def create_illumination_vs_returns_plot(self, data: List[CombinedDataPoint]) -> go.Figure:
        """
        Create scatter plot of moon illumination vs daily returns.
        
        Args:
            data: List of combined data points
            
        Returns:
            Plotly figure object
        """
        if not data:
            return self._create_empty_plot()
        
        # Extract data for plotting
        illuminations = []
        returns = []
        phases = []
        dates = []
        
        for point in data:
            if point.daily_return is not None:
                illuminations.append(point.illumination)
                returns.append(point.daily_return)
                phases.append(point.phase_code.name)
                dates.append(point.date.strftime('%Y-%m-%d'))
        
        if not illuminations:
            return self._create_empty_plot()
        
        # Create scatter plot
        fig = go.Figure()
        
        # Add scatter points colored by moon phase
        phase_colors = px.colors.qualitative.Set3
        unique_phases = list(set(phases))
        
        for i, phase in enumerate(unique_phases):
            phase_mask = [p == phase for p in phases]
            phase_illuminations = [ill for ill, mask in zip(illuminations, phase_mask) if mask]
            phase_returns = [ret for ret, mask in zip(returns, phase_mask) if mask]
            phase_dates = [date for date, mask in zip(dates, phase_mask) if mask]
            
            if phase_illuminations:
                fig.add_trace(
                    go.Scatter(
                        x=phase_illuminations,
                        y=phase_returns,
                        mode='markers',
                        name=phase,
                        marker=dict(
                            color=phase_colors[i % len(phase_colors)],
                            size=8,
                            opacity=0.7
                        ),
                        text=phase_dates,
                        hovertemplate=(
                            f"Phase: {phase}<br>"
                            "Illumination: %{x:.1f}%<br>"
                            "Return: %{y:.2f}%<br>"
                            "Date: %{text}<br>"
                            "<extra></extra>"
                        )
                    )
                )
        
        # Add trend line
        if len(illuminations) > 2:
            z = np.polyfit(illuminations, returns, 1)
            p = np.poly1d(z)
            x_trend = np.linspace(min(illuminations), max(illuminations), 100)
            y_trend = p(x_trend)
            
            fig.add_trace(
                go.Scatter(
                    x=x_trend,
                    y=y_trend,
                    mode='lines',
                    name='Trend Line',
                    line=dict(color='red', dash='dash', width=2),
                    hoverinfo='skip'
                )
            )
        
        # Update layout
        fig.update_layout(
            title="Daily Returns vs Moon Illumination",
            xaxis_title="Moon Illumination (%)",
            yaxis_title="Daily Return (%)",
            template="plotly_white",
            height=500,
            showlegend=True
        )
        
        return fig
    
    def create_volatility_vs_illumination_plot(self, data: List[CombinedDataPoint]) -> go.Figure:
        """
        Create scatter plot of volatility vs moon illumination.
        
        Args:
            data: List of combined data points
            
        Returns:
            Plotly figure object
        """
        if not data:
            return self._create_empty_plot()
        
        # Extract data for plotting
        illuminations = []
        volatilities = []
        phases = []
        dates = []
        
        for point in data:
            if point.volatility_7d is not None:
                illuminations.append(point.illumination)
                volatilities.append(point.volatility_7d)
                phases.append(point.phase_code.name)
                dates.append(point.date.strftime('%Y-%m-%d'))
        
        if not illuminations:
            return self._create_empty_plot()
        
        # Create scatter plot with color scale based on volatility
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(
                x=illuminations,
                y=volatilities,
                mode='markers',
                marker=dict(
                    color=volatilities,
                    colorscale='Viridis',
                    size=10,
                    opacity=0.7,
                    colorbar=dict(title="Volatility (%)")
                ),
                text=[f"{phase}<br>{date}" for phase, date in zip(phases, dates)],
                hovertemplate=(
                    "Illumination: %{x:.1f}%<br>"
                    "Volatility: %{y:.2f}%<br>"
                    "%{text}<br>"
                    "<extra></extra>"
                )
            )
        )
        
        # Add trend line
        if len(illuminations) > 2:
            z = np.polyfit(illuminations, volatilities, 1)
            p = np.poly1d(z)
            x_trend = np.linspace(min(illuminations), max(illuminations), 100)
            y_trend = p(x_trend)
            
            fig.add_trace(
                go.Scatter(
                    x=x_trend,
                    y=y_trend,
                    mode='lines',
                    name='Trend Line',
                    line=dict(color='red', dash='dash', width=2),
                    hoverinfo='skip'
                )
            )
        
        # Update layout
        fig.update_layout(
            title="Volatility vs Moon Illumination",
            xaxis_title="Moon Illumination (%)",
            yaxis_title="Volatility (%)",
            template="plotly_white",
            height=500,
            showlegend=False
        )
        
        return fig
    
    def _create_empty_plot(self) -> go.Figure:
        """Create empty plot when no data is available."""
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for correlation analysis",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title=self.title,
            template="plotly_white",
            height=400
        )
        return fig


class BarChart:
    """Bar chart component for phase-based analysis."""
    
    def __init__(self, title: str = "Moon Phase Analysis"):
        """
        Initialize bar chart.
        
        Args:
            title: Chart title
        """
        self.title = title
    
    def create_volatility_by_phase_chart(self, phase_metrics: List[PhaseMetric]) -> go.Figure:
        """
        Create bar chart of volatility grouped by moon phases.
        
        Args:
            phase_metrics: List of phase metrics
            
        Returns:
            Plotly figure object
        """
        if not phase_metrics:
            return self._create_empty_chart()
        
        # Extract data for plotting
        phases = [metric.phase.name for metric in phase_metrics]
        volatilities = [metric.avg_volatility for metric in phase_metrics]
        sample_counts = [metric.sample_count for metric in phase_metrics]
        
        # Create bar chart
        fig = go.Figure()
        
        fig.add_trace(
            go.Bar(
                x=phases,
                y=volatilities,
                name="Average Volatility",
                marker_color='lightblue',
                text=[f"n={n}" for n in sample_counts],
                textposition='outside',
                hovertemplate=(
                    "Phase: %{x}<br>"
                    "Avg Volatility: %{y:.2f}%<br>"
                    "Sample Size: %{text}<br>"
                    "<extra></extra>"
                )
            )
        )
        
        # Update layout
        fig.update_layout(
            title="Average Volatility by Moon Phase",
            xaxis_title="Moon Phase",
            yaxis_title="Average Volatility (%)",
            template="plotly_white",
            height=400,
            showlegend=False
        )
        
        # Rotate x-axis labels for better readability
        fig.update_xaxes(tickangle=45)
        
        return fig
    
    def create_returns_by_phase_chart(self, phase_metrics: List[PhaseMetric]) -> go.Figure:
        """
        Create bar chart of returns grouped by moon phases.
        
        Args:
            phase_metrics: List of phase metrics
            
        Returns:
            Plotly figure object
        """
        if not phase_metrics:
            return self._create_empty_chart()
        
        # Extract data for plotting
        phases = [metric.phase.name for metric in phase_metrics]
        mean_returns = [metric.mean_return for metric in phase_metrics]
        green_percentages = [metric.green_day_percentage for metric in phase_metrics]
        sample_counts = [metric.sample_count for metric in phase_metrics]
        
        # Create subplot with two y-axes
        fig = make_subplots(
            rows=1, cols=1,
            specs=[[{"secondary_y": True}]]
        )
        
        # Add mean returns bars
        fig.add_trace(
            go.Bar(
                x=phases,
                y=mean_returns,
                name="Mean Return",
                marker_color=['green' if r > 0 else 'red' for r in mean_returns],
                opacity=0.7,
                hovertemplate=(
                    "Phase: %{x}<br>"
                    "Mean Return: %{y:.2f}%<br>"
                    "<extra></extra>"
                )
            ),
            secondary_y=False
        )
        
        # Add green day percentage line
        fig.add_trace(
            go.Scatter(
                x=phases,
                y=green_percentages,
                mode='lines+markers',
                name="Green Day %",
                line=dict(color='orange', width=3),
                marker=dict(size=8),
                hovertemplate=(
                    "Phase: %{x}<br>"
                    "Green Days: %{y:.1f}%<br>"
                    "<extra></extra>"
                )
            ),
            secondary_y=True
        )
        
        # Update layout
        fig.update_layout(
            title="Returns and Green Day Percentage by Moon Phase",
            template="plotly_white",
            height=500,
            showlegend=True
        )
        
        # Update y-axes
        fig.update_yaxes(title_text="Mean Return (%)", secondary_y=False)
        fig.update_yaxes(title_text="Green Day Percentage (%)", secondary_y=True)
        fig.update_xaxes(title_text="Moon Phase", tickangle=45)
        
        return fig
    
    def _create_empty_chart(self) -> go.Figure:
        """Create empty chart when no data is available."""
        fig = go.Figure()
        fig.add_annotation(
            text="No phase data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title=self.title,
            template="plotly_white",
            height=400
        )
        return fig


class CalendarHeatmap:
    """Calendar heatmap component for daily returns with moon phase icons."""
    
    def __init__(self, title: str = "Daily Returns Calendar"):
        """
        Initialize calendar heatmap.
        
        Args:
            title: Chart title
        """
        self.title = title
    
    def create_returns_heatmap(self, data: List[CombinedDataPoint], 
                              year: Optional[int] = None) -> go.Figure:
        """
        Create calendar heatmap of daily returns.
        
        Args:
            data: List of combined data points
            year: Specific year to display (if None, uses data range)
            
        Returns:
            Plotly figure object
        """
        if not data:
            return self._create_empty_heatmap()
        
        # Filter data by year if specified
        if year:
            data = [point for point in data if point.date.year == year]
        
        if not data:
            return self._create_empty_heatmap()
        
        # Create DataFrame for easier manipulation
        df_data = []
        for point in data:
            if point.daily_return is not None:
                df_data.append({
                    'date': point.date.date(),
                    'return': point.daily_return,
                    'phase': point.phase_code.name,
                    'illumination': point.illumination
                })
        
        if not df_data:
            return self._create_empty_heatmap()
        
        df = pd.DataFrame(df_data)
        
        # Create calendar grid
        start_date = df['date'].min()
        end_date = df['date'].max()
        
        # Generate all dates in range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Create calendar matrix
        calendar_data = []
        for date in date_range:
            row_data = df[df['date'] == date.date()]
            if not row_data.empty:
                return_val = row_data.iloc[0]['return']
                phase = row_data.iloc[0]['phase']
                illumination = row_data.iloc[0]['illumination']
            else:
                return_val = None
                phase = "No Data"
                illumination = 0
            
            calendar_data.append({
                'date': date,
                'return': return_val,
                'phase': phase,
                'illumination': illumination,
                'weekday': date.weekday(),
                'week': date.isocalendar()[1]
            })
        
        cal_df = pd.DataFrame(calendar_data)
        
        # Create heatmap using scatter plot
        fig = go.Figure()
        
        # Add scatter points for each day
        for _, row in cal_df.iterrows():
            if row['return'] is not None and not pd.isna(row['return']):
                color = 'green' if row['return'] > 0 else 'red'
                size = min(abs(row['return']) * 5 + 5, 20)  # Scale size by return magnitude
                
                fig.add_trace(
                    go.Scatter(
                        x=[row['weekday']],
                        y=[row['week']],
                        mode='markers',
                        marker=dict(
                            color=color,
                            size=size,
                            opacity=0.7,
                            line=dict(width=1, color='white')
                        ),
                        name=row['date'].strftime('%Y-%m-%d'),
                        hovertemplate=(
                            f"Date: {row['date'].strftime('%Y-%m-%d')}<br>"
                            f"Return: {row['return']:.2f}%<br>"
                            f"Phase: {row['phase']}<br>"
                            f"Illumination: {row['illumination']:.1f}%<br>"
                            "<extra></extra>"
                        ),
                        showlegend=False
                    )
                )
        
        # Update layout
        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        fig.update_layout(
            title=f"Daily Returns Calendar - {start_date.year}",
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(7)),
                ticktext=weekdays,
                title="Day of Week"
            ),
            yaxis=dict(
                title="Week of Year",
                autorange='reversed'  # Reverse to show weeks chronologically
            ),
            template="plotly_white",
            height=600,
            showlegend=False
        )
        
        return fig
    
    def _create_empty_heatmap(self) -> go.Figure:
        """Create empty heatmap when no data is available."""
        fig = go.Figure()
        fig.add_annotation(
            text="No return data available for calendar",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title=self.title,
            template="plotly_white",
            height=400
        )
        return fig


def create_comprehensive_dashboard(data: List[CombinedDataPoint], 
                                 phase_metrics: List[PhaseMetric]) -> Dict[str, go.Figure]:
    """
    Create all visualization components for the dashboard.
    
    Args:
        data: List of combined data points
        phase_metrics: List of phase metrics
        
    Returns:
        Dictionary of chart names to Plotly figures
    """
    charts = {}
    
    # Time series chart
    ts_chart = TimeSeriesChart()
    charts['time_series'] = ts_chart.create_chart(data, show_volume=True, show_volatility=True)
    
    # Scatter plots
    scatter_plot = ScatterPlot()
    charts['returns_vs_illumination'] = scatter_plot.create_illumination_vs_returns_plot(data)
    charts['volatility_vs_illumination'] = scatter_plot.create_volatility_vs_illumination_plot(data)
    
    # Bar charts
    bar_chart = BarChart()
    charts['volatility_by_phase'] = bar_chart.create_volatility_by_phase_chart(phase_metrics)
    charts['returns_by_phase'] = bar_chart.create_returns_by_phase_chart(phase_metrics)
    
    # Calendar heatmap
    calendar_heatmap = CalendarHeatmap()
    charts['calendar_heatmap'] = calendar_heatmap.create_returns_heatmap(data)
    
    logger.info(f"Created {len(charts)} visualization components")
    return charts