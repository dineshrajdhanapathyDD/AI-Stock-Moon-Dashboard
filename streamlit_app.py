#!/usr/bin/env python3
"""
Stock Moon Dashboard - Streamlit Version
Minimal deployment for Streamlit Cloud
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from mcp_tools import get_stock_prices, get_moon_phase
    from data_alignment import create_aligned_dataset
    from statistical_analyzer import StatisticalAnalyzer
    from stock_database import stock_db
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Page config
st.set_page_config(
    page_title="🌙 Stock Moon Dashboard",
    page_icon="🌙",
    layout="wide"
)

# Header
st.title("🌙 Stock Moon Dashboard")
st.markdown("*Analyzing relationships between stock prices and moon phases*")

# Sidebar controls
st.sidebar.header("📊 Analysis Parameters")

# Stock selection
symbol = st.sidebar.selectbox(
    "Stock Symbol",
    ["TCS.NS", "AAPL", "GOOGL", "RELIANCE.NS", "INFY.NS", "MSFT"],
    index=0
)

# Date range
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input(
        "Start Date",
        value=datetime.now() - timedelta(days=120)
    )
with col2:
    end_date = st.date_input(
        "End Date", 
        value=datetime.now() - timedelta(days=7)
    )

# Location (Mumbai default)
st.sidebar.subheader("📍 Location")
latitude = st.sidebar.number_input("Latitude", value=19.0760, format="%.4f")
longitude = st.sidebar.number_input("Longitude", value=72.8777, format="%.4f")

# Analyze button
if st.sidebar.button("🚀 Analyze Data", type="primary"):
    
    with st.spinner("Fetching data..."):
        try:
            # Fetch data
            stock_data = get_stock_prices(
                symbol, 
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )
            
            moon_data = get_moon_phase(
                latitude, longitude,
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )
            
            if not stock_data or not moon_data:
                st.error("No data available for the selected parameters")
                st.stop()
            
            # Convert to objects
            from data_models import DataFactory
            stock_objects = [DataFactory.create_stock_data_from_dict(item) for item in stock_data]
            moon_objects = [DataFactory.create_moon_data_from_dict(item) for item in moon_data]
            
            # Align data
            aligned_data = create_aligned_dataset(stock_objects, moon_objects)
            
            if not aligned_data:
                st.error("No aligned data available")
                st.stop()
            
            # Calculate metrics
            from metrics_calculator import MetricsCalculator
            calculator = MetricsCalculator()
            metrics_data = calculator.calculate_all_metrics(aligned_data, 14)
            
            # Statistical analysis
            analyzer = StatisticalAnalyzer()
            results = analyzer.analyze_moon_stock_correlation(metrics_data)
            
            # Store in session state
            st.session_state.metrics_data = metrics_data
            st.session_state.analysis_results = results
            st.session_state.symbol = symbol
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            st.stop()

# Display results if available
if hasattr(st.session_state, 'metrics_data'):
    
    # Key metrics
    st.header("📊 Key Results")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Trading Days", len(st.session_state.metrics_data))
    
    with col2:
        corr = st.session_state.analysis_results.correlation_analysis.returns_illumination_pearson
        st.metric("Moon Correlation", f"{corr:.3f}")
    
    with col3:
        prices = [p.close for p in st.session_state.metrics_data]
        st.metric("Price Range", f"₹{min(prices):.0f} - ₹{max(prices):.0f}")
    
    with col4:
        p_val = st.session_state.analysis_results.correlation_analysis.returns_illumination_p_value
        st.metric("P-value", f"{p_val:.3f}")
    
    # Create DataFrame for visualization
    df_data = []
    for point in st.session_state.metrics_data:
        df_data.append({
            'date': point.date,
            'close': point.close,
            'daily_return': point.daily_return or 0,
            'illumination': point.illumination,
            'phase_code': point.phase_code,
            'volatility': point.volatility_7d or 0
        })
    
    df = pd.DataFrame(df_data)
    
    # Price chart with moon phases
    st.header("📈 Price Chart with Moon Phases")
    
    fig = go.Figure()
    
    # Price line
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['close'],
        mode='lines',
        name='Price',
        line=dict(color='blue', width=2)
    ))
    
    # Moon phase markers
    phase_names = ['New Moon', 'Waxing Crescent', 'First Quarter', 'Waxing Gibbous',
                   'Full Moon', 'Waning Gibbous', 'Last Quarter', 'Waning Crescent']
    
    for i, phase in enumerate(phase_names):
        phase_data = df[df['phase_code'] == i]
        if not phase_data.empty:
            fig.add_trace(go.Scatter(
                x=phase_data['date'],
                y=phase_data['close'],
                mode='markers',
                name=phase,
                marker=dict(size=8, symbol='circle')
            ))
    
    fig.update_layout(
        title=f"{st.session_state.symbol} Price with Moon Phases",
        xaxis_title="Date",
        yaxis_title="Price",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Correlation analysis
    st.header("🌙 Moon Phase Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Returns by moon phase
        phase_returns = df.groupby('phase_code')['daily_return'].mean()
        
        fig_bar = go.Figure(data=[
            go.Bar(x=[phase_names[i] for i in phase_returns.index], 
                   y=phase_returns.values,
                   marker_color='lightblue')
        ])
        fig_bar.update_layout(
            title="Average Returns by Moon Phase",
            xaxis_title="Moon Phase",
            yaxis_title="Average Return (%)",
            height=400
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Illumination vs Returns scatter
        fig_scatter = px.scatter(
            df, x='illumination', y='daily_return',
            title="Returns vs Moon Illumination",
            labels={'illumination': 'Moon Illumination (%)', 'daily_return': 'Daily Return (%)'}
        )
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Statistical summary
    st.header("📊 Statistical Summary")
    
    st.write(f"""
    **Analysis Results for {st.session_state.symbol}:**
    
    - **Sample Size**: {len(st.session_state.metrics_data)} trading days
    - **Correlation (Returns vs Illumination)**: {corr:.3f}
    - **P-value**: {p_val:.3f}
    - **Statistical Significance**: {'Yes' if p_val < 0.05 else 'Approaching' if p_val < 0.1 else 'No'}
    - **Average Daily Return**: {df['daily_return'].mean():.3f}%
    - **Volatility**: {df['volatility'].mean():.2f}%
    """)
    
    # Phase breakdown table
    st.subheader("Moon Phase Breakdown")
    
    phase_summary = []
    for i, phase in enumerate(phase_names):
        phase_data = df[df['phase_code'] == i]
        if not phase_data.empty:
            phase_summary.append({
                'Moon Phase': phase,
                'Days': len(phase_data),
                'Avg Return (%)': f"{phase_data['daily_return'].mean():.3f}",
                'Avg Volatility (%)': f"{phase_data['volatility'].mean():.2f}"
            })
    
    st.dataframe(pd.DataFrame(phase_summary), use_container_width=True)

else:
    # Welcome message
    st.info("👆 Configure your analysis parameters in the sidebar and click 'Analyze Data' to begin!")
    
    st.markdown("""
    ### 🌙 About This Dashboard
    
    This dashboard analyzes potential relationships between stock price behavior and lunar cycles using:
    
    - **Real-time Data**: Yahoo Finance + Moon Phase APIs
    - **Statistical Analysis**: Correlation testing and significance analysis  
    - **Interactive Charts**: Price movements with moon phase overlays
    - **Global Markets**: US stocks, Indian NSE/BSE, and more
    
    **Featured Analysis**: TCS.NS (India's largest IT company) shows moderate lunar correlation (r = 0.143)
    
    ### 🚀 Quick Start
    1. Select a stock symbol (TCS.NS recommended)
    2. Choose date range (last 3-4 months works well)
    3. Set location (Mumbai coordinates pre-loaded for Indian stocks)
    4. Click "Analyze Data" to see the results!
    """)

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit • Data from Yahoo Finance & Open-Meteo • For educational purposes*")