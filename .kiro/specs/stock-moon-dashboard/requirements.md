# Requirements Document

## Introduction

The Data Weaver AI is a lightweight dashboard application that analyzes and visualizes potential relationships between stock price behavior and lunar cycles. The system fetches real-time financial data and astronomical information to provide statistical insights, interactive visualizations, and automated narrative analysis of correlations between market movements and moon phases.

## Glossary

- **Dashboard**: The web-based user interface displaying all visualizations and controls
- **MCP Tools**: Model Context Protocol tools for data fetching operations
- **Moon Phase Code**: 8-phase classification system (New, Waxing Crescent, First Quarter, Waxing Gibbous, Full, Waning Gibbous, Last Quarter, Waning Crescent)
- **Daily Return**: Percentage change in stock price from previous trading day
- **Volatility Window**: Rolling period for calculating price volatility metrics
- **Full Moon Window**: ±2 day period around full moon events
- **Illumination**: Percentage of moon surface visible from Earth (0-100%)
- **Market Closure**: Non-trading days including weekends and holidays

## Requirements

### Requirement 1

**User Story:** As a financial analyst, I want to fetch and combine stock price data with moon phase information, so that I can analyze potential correlations between lunar cycles and market behavior.

#### Acceptance Criteria

1. WHEN the system requests stock data THEN the Dashboard SHALL fetch price information from Yahoo Finance unofficial endpoint without requiring API keys
2. WHEN the system requests astronomical data THEN the Dashboard SHALL retrieve moon phase information from Open-Meteo Astronomy API for the specified date range
3. WHEN both datasets are retrieved THEN the Dashboard SHALL normalize all timestamps to UTC and align data by trading dates
4. WHEN market closures occur THEN the Dashboard SHALL handle weekends and holidays gracefully without data gaps
5. WHEN timezone misalignment is detected THEN the Dashboard SHALL correct temporal inconsistencies automatically

### Requirement 2

**User Story:** As a data scientist, I want comprehensive data processing and metric calculation capabilities, so that I can extract meaningful insights from the combined datasets.

#### Acceptance Criteria

1. WHEN processing daily stock data THEN the Dashboard SHALL calculate daily returns, absolute returns, and rolling volatility metrics
2. WHEN processing moon data THEN the Dashboard SHALL compute moon phase codes, illumination percentages, and days from full moon
3. WHEN calculating volatility THEN the Dashboard SHALL provide configurable rolling window periods (7, 14, 30 days)
4. WHEN grouping data by moon phases THEN the Dashboard SHALL compute average volatility and percentage of positive return days per phase
5. WHEN analyzing correlations THEN the Dashboard SHALL calculate Pearson and Spearman correlation coefficients between moon illumination and price movements

### Requirement 3

**User Story:** As a trader, I want interactive visualizations and statistical analysis tools, so that I can identify patterns and test hypotheses about lunar market effects.

#### Acceptance Criteria

1. WHEN displaying time series data THEN the Dashboard SHALL render price charts with overlaid moon phase markers and event annotations
2. WHEN showing correlation analysis THEN the Dashboard SHALL provide scatter plots of illumination versus daily returns with trend lines
3. WHEN presenting phase analysis THEN the Dashboard SHALL display bar charts of volatility grouped by moon phases
4. WHEN creating calendar views THEN the Dashboard SHALL show heatmaps of return magnitudes with moon phase icons
5. WHEN running statistical tests THEN the Dashboard SHALL perform t-tests comparing full moon periods versus baseline volatility with p-values and effect sizes

### Requirement 4

**User Story:** As a researcher, I want automated insight generation and narrative analysis, so that I can quickly understand key patterns and anomalies in the data.

#### Acceptance Criteria

1. WHEN analysis completes THEN the Dashboard SHALL generate automated narrative summaries of key findings
2. WHEN anomalies are detected THEN the Dashboard SHALL highlight unusual price movements and their corresponding moon phases
3. WHEN patterns emerge THEN the Dashboard SHALL identify clustering of significant moves around lunar events
4. WHEN correlations are found THEN the Dashboard SHALL provide evidence-based commentary on statistical significance
5. WHEN displaying results THEN the Dashboard SHALL present insights in clear, non-technical language suitable for various audiences

### Requirement 5

**User Story:** As an interactive user, I want dynamic controls and responsive interface elements, so that I can explore different stocks, time periods, and analysis parameters.

#### Acceptance Criteria

1. WHEN selecting stocks THEN the Dashboard SHALL provide a ticker symbol input with validation
2. WHEN choosing date ranges THEN the Dashboard SHALL offer flexible start and end date selection with reasonable defaults
3. WHEN adjusting parameters THEN the Dashboard SHALL allow modification of rolling window periods and moon phase toggles
4. WHEN interacting with charts THEN the Dashboard SHALL support hover details, brushing to zoom, and dynamic filtering
5. WHEN parameters change THEN the Dashboard SHALL recompute all visualizations and statistics automatically

### Requirement 6

**User Story:** As a performance-conscious user, I want efficient data handling and caching mechanisms, so that the dashboard remains responsive during analysis.

#### Acceptance Criteria

1. WHEN fetching external data THEN the Dashboard SHALL use batched API requests to minimize network overhead
2. WHEN processing large datasets THEN the Dashboard SHALL implement client-side caching for previously retrieved data
3. WHEN performing calculations THEN the Dashboard SHALL execute all transformations on the client side without backend dependencies
4. WHEN handling missing data THEN the Dashboard SHALL gracefully manage gaps in stock or moon data without system failures
5. WHEN displaying results THEN the Dashboard SHALL maintain responsive performance across all visualization components

### Requirement 7

**User Story:** As a quantitative analyst, I want optional simulation capabilities, so that I can test simple trading strategies based on lunar patterns.

#### Acceptance Criteria

1. WHEN simulation mode is enabled THEN the Dashboard SHALL implement rule-based trading strategies using moon phase triggers
2. WHEN backtesting strategies THEN the Dashboard SHALL calculate hypothetical profit and loss for lunar-based entry signals
3. WHEN evaluating performance THEN the Dashboard SHALL compare strategy returns against buy-and-hold benchmarks
4. WHEN displaying simulation results THEN the Dashboard SHALL show trade history and performance metrics
5. WHEN strategy parameters change THEN the Dashboard SHALL recalculate all simulation results dynamically