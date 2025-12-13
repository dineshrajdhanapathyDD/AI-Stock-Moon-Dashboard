# Design Document

## Overview

The Data Weaver AI dashboard is a client-side web application that analyzes correlations between stock price movements and lunar cycles. The system uses a modular architecture with MCP tools for data fetching, JavaScript for data processing, and D3.js/Chart.js for interactive visualizations. All computation occurs client-side to eliminate backend dependencies while maintaining responsive performance through intelligent caching and batched API requests.

## Architecture

The application follows a layered architecture pattern:

**Presentation Layer**: Interactive dashboard with responsive charts and controls
**Business Logic Layer**: Data processing, statistical analysis, and insight generation
**Data Access Layer**: MCP tools for external API integration
**Caching Layer**: Client-side storage for performance optimization

The system uses an event-driven architecture where user interactions trigger data pipeline updates that flow through processing, analysis, and visualization components.

## Components and Interfaces

### MCP Tools Module
- `getStockPrices(symbol, startDate, endDate, interval)`: Fetches OHLCV data from Yahoo Finance
- `getMoonPhase(latitude, longitude, startDate, endDate)`: Retrieves lunar data from Open-Meteo
- `CacheManager`: Handles local storage of API responses with TTL expiration

### Data Processing Engine
- `DataAligner`: Normalizes timestamps and joins datasets by trading dates
- `MetricsCalculator`: Computes returns, volatility, and lunar metrics
- `StatisticalAnalyzer`: Performs correlation tests and significance testing

### Visualization Components
- `TimeSeriesChart`: Price data with moon phase overlays
- `ScatterPlot`: Illumination vs return correlation analysis
- `BarChart`: Volatility grouped by moon phases
- `CalendarHeatmap`: Daily returns with lunar icons
- `EventTable`: Largest price movements with moon context

### User Interface Controller
- `ParameterPanel`: Stock selection, date ranges, rolling windows
- `FilterManager`: Dynamic chart updates based on user selections
- `InsightGenerator`: Automated narrative creation from analysis results

## Data Models

### StockData
```typescript
interface StockData {
  date: Date;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  dailyReturn: number;
  absReturn: number;
  volatility7d?: number;
}
```

### MoonData
```typescript
interface MoonData {
  date: Date;
  phaseCode: MoonPhase; // 0-7 representing 8 phases
  illumination: number; // 0-100%
  daysFromFullMoon: number;
  isFullMoonWindow: boolean; // ±2 days from full moon
}
```

### CombinedDataPoint
```typescript
interface CombinedDataPoint extends StockData, MoonData {
  tradingDay: boolean;
  anomalyScore?: number;
}
```

### AnalysisResults
```typescript
interface AnalysisResults {
  correlations: {
    pearson: number;
    spearman: number;
    pValues: { pearson: number; spearman: number };
  };
  phaseMetrics: PhaseMetric[];
  volatilityTest: {
    fullMoonVolatility: number;
    baselineVolatility: number;
    tStatistic: number;
    pValue: number;
    effectSize: number;
  };
  insights: string[];
  anomalies: AnomalyEvent[];
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Data Fetching Properties

**Property 1: Stock data retrieval consistency**
*For any* valid stock symbol and date range, the getStockPrices function should return properly formatted OHLCV data with all required fields populated
**Validates: Requirements 1.1**

**Property 2: Moon data retrieval consistency**
*For any* valid coordinates and date range, the getMoonPhase function should return complete lunar data with phase codes and illumination values
**Validates: Requirements 1.2**

**Property 3: Data alignment correctness**
*For any* stock and moon datasets, the alignment function should produce UTC-normalized timestamps with proper date matching between trading days and lunar data
**Validates: Requirements 1.3**

**Property 4: Market closure handling**
*For any* dataset containing weekends and holidays, the system should handle non-trading days without creating data gaps or system errors
**Validates: Requirements 1.4**

**Property 5: Timezone correction accuracy**
*For any* datasets with timezone misalignments, the correction function should normalize all timestamps to UTC consistently
**Validates: Requirements 1.5**

### Data Processing Properties

**Property 6: Metric calculation accuracy**
*For any* price series, calculated daily returns, absolute returns, and rolling volatility should match expected mathematical formulas within numerical precision
**Validates: Requirements 2.1**

**Property 7: Moon metric computation**
*For any* moon data, computed phase codes, illumination percentages, and days from full moon should be mathematically correct
**Validates: Requirements 2.2**

**Property 8: Rolling window flexibility**
*For any* price series and window size (7, 14, 30 days), volatility calculations should correctly apply the specified rolling period
**Validates: Requirements 2.3**

**Property 9: Phase aggregation correctness**
*For any* dataset grouped by moon phases, average volatility and percentage calculations should accurately reflect the underlying data distribution
**Validates: Requirements 2.4**

**Property 10: Statistical correlation accuracy**
*For any* paired datasets, Pearson and Spearman correlation calculations should match standard statistical library results
**Validates: Requirements 2.5**

### Visualization Properties

**Property 11: Chart data representation**
*For any* input dataset, rendered charts should accurately represent all data points and maintain visual consistency with the underlying data
**Validates: Requirements 3.1, 3.2, 3.3, 3.4**

**Property 12: Statistical test implementation**
*For any* full moon and baseline volatility datasets, t-test calculations should produce correct p-values and effect sizes according to statistical standards
**Validates: Requirements 3.5**

### Analysis Properties

**Property 13: Narrative generation accuracy**
*For any* analysis results, generated narratives should accurately reflect the statistical findings without misrepresenting data
**Validates: Requirements 4.1**

**Property 14: Anomaly detection precision**
*For any* dataset with known anomalies, the detection algorithm should correctly identify unusual price movements with appropriate sensitivity
**Validates: Requirements 4.2**

**Property 15: Pattern recognition reliability**
*For any* dataset with artificial clustering patterns, the system should detect lunar event clustering with measurable accuracy
**Validates: Requirements 4.3**

**Property 16: Statistical interpretation correctness**
*For any* correlation results with known significance levels, the commentary should accurately interpret statistical significance
**Validates: Requirements 4.4**

### User Interface Properties

**Property 17: Input validation robustness**
*For any* ticker symbol input (valid or invalid), the validation system should correctly accept valid symbols and reject invalid ones
**Validates: Requirements 5.1**

**Property 18: Date range validation**
*For any* date input combination, the system should properly validate ranges and apply reasonable defaults when needed
**Validates: Requirements 5.2**

**Property 19: Parameter control responsiveness**
*For any* parameter modification, the system should correctly apply changes and update all dependent calculations
**Validates: Requirements 5.3, 5.5**

**Property 20: Interactive functionality**
*For any* user interaction with charts, the system should respond with appropriate state changes and visual feedback
**Validates: Requirements 5.4**

### Performance Properties

**Property 21: API request optimization**
*For any* series of data requests, the system should batch requests efficiently rather than making individual API calls
**Validates: Requirements 6.1**

**Property 22: Caching effectiveness**
*For any* repeated data request, the system should use cached results rather than making redundant API calls
**Validates: Requirements 6.2**

**Property 23: Client-side processing**
*For any* data transformation operation, the system should execute calculations locally without backend dependencies
**Validates: Requirements 6.3**

**Property 24: Error handling resilience**
*For any* dataset with missing or corrupted values, the system should handle errors gracefully without system failures
**Validates: Requirements 6.4**

### Simulation Properties

**Property 25: Trading rule implementation**
*For any* moon phase condition and price data, trading signals should be generated correctly according to specified rules
**Validates: Requirements 7.1**

**Property 26: P&L calculation accuracy**
*For any* series of trades with known entry/exit points, profit and loss calculations should be mathematically correct
**Validates: Requirements 7.2**

**Property 27: Benchmark comparison correctness**
*For any* strategy returns and benchmark data, performance comparisons should accurately reflect relative performance
**Validates: Requirements 7.3**

**Property 28: Simulation result presentation**
*For any* completed simulation, trade history and metrics should be correctly displayed and formatted
**Validates: Requirements 7.4**

**Property 29: Dynamic simulation updates**
*For any* parameter change in simulation mode, all results should be recalculated and updated consistently
**Validates: Requirements 7.5**

## Error Handling

The system implements comprehensive error handling across all layers:

**API Error Management**: Graceful handling of network failures, rate limits, and invalid responses from external APIs with automatic retry mechanisms and fallback strategies.

**Data Validation**: Input sanitization for all user inputs including ticker symbols, date ranges, and numerical parameters with clear error messaging.

**Missing Data Handling**: Intelligent gap filling for missing trading days and lunar data using interpolation and forward-fill strategies where appropriate.

**Performance Degradation**: Automatic data sampling and progressive loading for large datasets to maintain responsive user experience.

**Browser Compatibility**: Fallback implementations for older browsers and graceful degradation of advanced visualization features.

## Testing Strategy

The testing approach combines unit testing for specific functionality with property-based testing for universal correctness guarantees:

**Unit Testing Framework**: Jest for JavaScript unit tests covering specific examples, edge cases, and integration points between components.

**Property-Based Testing Library**: fast-check for JavaScript property-based testing, configured to run minimum 100 iterations per property to ensure statistical confidence.

**Testing Requirements**:
- Each correctness property must be implemented by a single property-based test
- Property-based tests must be tagged with format: '**Feature: stock-moon-dashboard, Property {number}: {property_text}**'
- Unit tests focus on specific examples and error conditions
- Property tests verify universal behaviors across all valid inputs
- Integration tests validate end-to-end data flow from API to visualization

**Test Coverage Goals**:
- 100% coverage of data processing functions
- Comprehensive validation of statistical calculations
- Interactive UI component testing with simulated user events
- Performance testing for large dataset handling
- Cross-browser compatibility validation