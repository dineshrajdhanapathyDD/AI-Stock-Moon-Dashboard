# Implementation Plan

- [x] 1. Set up project structure and core interfaces



  - Create HTML structure with container divs for dashboard components
  - Set up CSS framework and responsive grid layout
  - Initialize JavaScript modules for data processing and visualization
  - Configure build tools and dependency management
  - _Requirements: 1.1, 5.1, 6.3_

- [ ]* 1.1 Write property test for project structure validation
  - **Property 23: Client-side processing**
  - **Validates: Requirements 6.3**

- [x] 2. Implement MCP tools for external data fetching

  - Create getStockPrices MCP tool for Yahoo Finance API integration
  - Implement getMoonPhase MCP tool for Open-Meteo Astronomy API
  - Add error handling and retry logic for network failures
  - _Requirements: 1.1, 1.2_

- [ ]* 2.1 Write property test for stock data fetching
  - **Property 1: Stock data retrieval consistency**
  - **Validates: Requirements 1.1**

- [ ]* 2.2 Write property test for moon data fetching
  - **Property 2: Moon data retrieval consistency**
  - **Validates: Requirements 1.2**

- [ ]* 2.3 Write property test for API request batching
  - **Property 21: API request optimization**
  - **Validates: Requirements 6.1**

- [x] 3. Create data models and validation functions


  - Define TypeScript interfaces for StockData, MoonData, and CombinedDataPoint
  - Implement data validation functions for API responses
  - Create utility functions for data type conversion and sanitization
  - _Requirements: 1.3, 1.4, 1.5_

- [ ]* 3.1 Write property test for data validation
  - **Property 24: Error handling resilience**
  - **Validates: Requirements 6.4**

- [x] 4. Implement data alignment and normalization



  - Create DataAligner class for timestamp normalization to UTC
  - Implement date matching logic for trading days and lunar data
  - Add timezone correction functionality
  - Handle market closures and non-trading days
  - _Requirements: 1.3, 1.4, 1.5_

- [ ]* 4.1 Write property test for data alignment
  - **Property 3: Data alignment correctness**
  - **Validates: Requirements 1.3**

- [ ]* 4.2 Write property test for market closure handling
  - **Property 4: Market closure handling**
  - **Validates: Requirements 1.4**

- [ ]* 4.3 Write property test for timezone correction
  - **Property 5: Timezone correction accuracy**
  - **Validates: Requirements 1.5**

- [x] 5. Build metrics calculation engine


  - Implement daily return and absolute return calculations
  - Create rolling volatility calculation with configurable windows
  - Add moon phase code computation and illumination processing
  - Calculate days from full moon and full moon window detection
  - _Requirements: 2.1, 2.2, 2.3_

- [ ]* 5.1 Write property test for metric calculations
  - **Property 6: Metric calculation accuracy**
  - **Validates: Requirements 2.1**

- [ ]* 5.2 Write property test for moon metrics
  - **Property 7: Moon metric computation**
  - **Validates: Requirements 2.2**

- [ ]* 5.3 Write property test for rolling windows
  - **Property 8: Rolling window flexibility**
  - **Validates: Requirements 2.3**

- [x] 6. Implement statistical analysis functions



  - Create correlation calculation functions (Pearson and Spearman)
  - Implement t-test for full moon vs baseline volatility comparison
  - Add phase-based aggregation and grouping functions
  - Calculate effect sizes and p-values for statistical significance
  - _Requirements: 2.4, 2.5, 3.5_

- [ ]* 6.1 Write property test for phase aggregation
  - **Property 9: Phase aggregation correctness**
  - **Validates: Requirements 2.4**

- [ ]* 6.2 Write property test for correlation calculations
  - **Property 10: Statistical correlation accuracy**
  - **Validates: Requirements 2.5**

- [ ]* 6.3 Write property test for statistical tests
  - **Property 12: Statistical test implementation**
  - **Validates: Requirements 3.5**

- [x] 7. Create caching and performance optimization


  - Implement CacheManager with TTL expiration for API responses
  - Add client-side storage for previously retrieved data
  - Create batched request handling for multiple API calls
  - Optimize data processing for large datasets
  - _Requirements: 6.1, 6.2, 6.3_

- [ ]* 7.1 Write property test for caching functionality
  - **Property 22: Caching effectiveness**
  - **Validates: Requirements 6.2**

- [x] 8. Build time series visualization component


  - Create TimeSeriesChart class using D3.js or Chart.js
  - Implement price line chart with OHLC data display
  - Add moon phase markers and event annotations overlay
  - Include interactive hover details and zoom functionality
  - _Requirements: 3.1, 5.4_

- [ ]* 8.1 Write property test for chart data representation
  - **Property 11: Chart data representation**
  - **Validates: Requirements 3.1**

- [ ]* 8.2 Write property test for interactive functionality
  - **Property 20: Interactive functionality**
  - **Validates: Requirements 5.4**

- [x] 9. Implement correlation scatter plot

  - Create ScatterPlot component for illumination vs return analysis
  - Add trend line calculation and display
  - Implement brushing and selection functionality
  - Include correlation coefficient display and significance indicators
  - _Requirements: 3.2, 5.4_

- [x] 10. Build phase analysis bar chart

  - Create BarChart component for volatility by moon phase
  - Implement grouped bar display with error bars
  - Add interactive filtering and drill-down capabilities
  - Include statistical significance indicators
  - _Requirements: 3.3, 5.4_

- [x] 11. Create calendar heatmap visualization

  - Implement CalendarHeatmap component for daily returns
  - Add moon phase icons and return magnitude color coding
  - Create interactive date selection and filtering
  - Include tooltip details for individual days
  - _Requirements: 3.4, 5.4_


- [ ] 12. Implement event table for large movements
  - Create EventTable component for significant price changes
  - Add sorting and filtering capabilities by magnitude and moon phase
  - Include contextual information about lunar conditions
  - Implement export functionality for analysis results
  - _Requirements: 4.2, 4.3_

- [x] 13. Build user interface controls


  - Create ParameterPanel with ticker symbol input and validation
  - Implement date range picker with reasonable defaults
  - Add rolling window selector and moon phase toggle controls
  - Create responsive layout for different screen sizes
  - _Requirements: 5.1, 5.2, 5.3_

- [ ]* 13.1 Write property test for input validation
  - **Property 17: Input validation robustness**
  - **Validates: Requirements 5.1**

- [ ]* 13.2 Write property test for date validation
  - **Property 18: Date range validation**
  - **Validates: Requirements 5.2**

- [ ]* 13.3 Write property test for parameter controls
  - **Property 19: Parameter control responsiveness**
  - **Validates: Requirements 5.3**

- [x] 14. Implement automated insight generation

  - Create InsightGenerator class for narrative analysis
  - Implement anomaly detection algorithms for unusual price movements
  - Add pattern recognition for lunar event clustering
  - Generate statistical interpretation and commentary
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ]* 14.1 Write property test for narrative generation
  - **Property 13: Narrative generation accuracy**
  - **Validates: Requirements 4.1**

- [ ]* 14.2 Write property test for anomaly detection
  - **Property 14: Anomaly detection precision**
  - **Validates: Requirements 4.2**

- [ ]* 14.3 Write property test for pattern recognition
  - **Property 15: Pattern recognition reliability**
  - **Validates: Requirements 4.3**

- [ ]* 14.4 Write property test for statistical interpretation
  - **Property 16: Statistical interpretation correctness**
  - **Validates: Requirements 4.4**

- [x] 15. Create reactive update system

  - Implement FilterManager for dynamic chart updates
  - Add event-driven architecture for parameter changes
  - Create automatic recalculation pipeline for all visualizations
  - Optimize update performance for large datasets
  - _Requirements: 5.5_

- [ ]* 15.1 Write property test for reactive updates
  - **Property 19: Parameter control responsiveness**
  - **Validates: Requirements 5.5**

- [x] 16. Checkpoint - Ensure all core functionality tests pass


  - Ensure all tests pass, ask the user if questions arise.

- [x] 17. Implement optional simulation module

  - Create simulation engine for rule-based trading strategies
  - Implement P&L calculation for lunar-based entry signals
  - Add benchmark comparison against buy-and-hold strategy
  - Create trade history display and performance metrics
  - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [ ]* 17.1 Write property test for trading rules
  - **Property 25: Trading rule implementation**
  - **Validates: Requirements 7.1**

- [ ]* 17.2 Write property test for P&L calculations
  - **Property 26: P&L calculation accuracy**
  - **Validates: Requirements 7.2**

- [ ]* 17.3 Write property test for benchmark comparison
  - **Property 27: Benchmark comparison correctness**
  - **Validates: Requirements 7.3**

- [ ]* 17.4 Write property test for simulation results
  - **Property 28: Simulation result presentation**
  - **Validates: Requirements 7.4**

- [ ]* 17.5 Write property test for dynamic simulation updates
  - **Property 29: Dynamic simulation updates**
  - **Validates: Requirements 7.5**

- [x] 18. Add comprehensive error handling and edge cases

  - Implement graceful handling of API failures and rate limits
  - Add fallback strategies for missing or corrupted data
  - Create user-friendly error messages and recovery options
  - Test browser compatibility and performance optimization
  - _Requirements: 6.4_

- [x] 19. Final integration and polish

  - Integrate all components into cohesive dashboard interface
  - Optimize performance for production deployment
  - Add loading indicators and progress feedback
  - Implement final UI polish and accessibility features
  - _Requirements: All_

- [x] 20. Final Checkpoint - Ensure all tests pass


  - Ensure all tests pass, ask the user if questions arise.