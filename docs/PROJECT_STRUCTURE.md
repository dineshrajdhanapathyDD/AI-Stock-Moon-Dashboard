# 📁 Project Structure

## Overview
Stock Moon Dashboard - A Python/Dash application analyzing relationships between stock prices and moon phases.

```
stock-moon-dashboard/
├── 📄 README.md                    # Main project documentation
├── 📄 LICENSE                      # MIT License
├── 📄 requirements.txt             # Python dependencies
├── 📄 app.py                       # Main application entry point
├── 📄 mcp_server.py                # MCP tools server
├── 📄 amplify.yml                  # AWS Amplify deployment config
├── 📄 build.py                     # Build and validation script
├── 📄 .gitignore                   # Git ignore rules
├── 📄 CONTRIBUTING.md              # Contribution guidelines
├── 📄 PROJECT_STRUCTURE.md         # This file
├── 📄 DEPLOYMENT_STATUS.md         # Deployment readiness status
├── 📄 DEPLOYMENT.md                # Comprehensive deployment guide
├── 📄 DEPLOYMENT_CHECKLIST.md     # Deployment checklist
├── 📄 INDIAN_STOCKS_GUIDE.md      # Indian market integration guide
├── 📄 STOCK_SEARCH_FEATURES.md    # Search functionality guide
│
├── 📁 src/                         # Core application source code
│   ├── 📄 __init__.py             # Package initialization
│   ├── 📄 dashboard.py            # Main Dash web application
│   ├── 📄 mcp_tools.py            # MCP data fetching tools
│   ├── 📄 stock_database.py       # Stock search and autocomplete
│   ├── 📄 data_models.py          # Data structures and models
│   ├── 📄 data_alignment.py       # Data synchronization utilities
│   ├── 📄 data_validation.py      # Input validation and sanitization
│   ├── 📄 metrics_calculator.py   # Financial metrics computation
│   ├── 📄 statistical_analyzer.py # Statistical analysis engine
│   ├── 📄 visualizations.py       # Chart and graph generation
│   └── 📄 cache_manager.py        # Caching and performance optimization
│
├── 📁 .kiro/                      # Kiro IDE configuration
│   ├── 📁 specs/                  # Feature specifications
│   │   └── 📁 stock-moon-dashboard/
│   │       ├── 📄 requirements.md # Feature requirements (EARS format)
│   │       ├── 📄 design.md       # Technical design document
│   │       └── 📄 tasks.md        # Implementation task list
│   └── 📁 settings/               # IDE settings
│       └── 📄 mcp.json            # MCP server configuration
│
├── 📁 .test_cache/                # Test result caching
│
└── 📄 test_*.py                   # Test suite files
    ├── 📄 test_complete_system.py # End-to-end system tests
    ├── 📄 test_stock_search.py    # Stock database tests
    ├── 📄 test_autocomplete.py    # Autocomplete functionality tests
    ├── 📄 test_indian_stocks.py   # Indian market integration tests
    ├── 📄 test_alignment.py       # Data alignment tests
    ├── 📄 test_caching.py         # Cache performance tests
    ├── 📄 test_metrics.py         # Metrics calculation tests
    ├── 📄 test_statistics.py      # Statistical analysis tests
    └── 📄 test_visualizations.py  # Visualization generation tests
```

## Key Components

### 🚀 **Application Layer**
- `app.py` - Production-ready entry point with health checks
- `src/dashboard.py` - Interactive Dash web interface
- `src/mcp_tools.py` - External API integration (Yahoo Finance, Moon data)

### 📊 **Data Processing**
- `src/data_models.py` - Type-safe data structures
- `src/data_alignment.py` - Timestamp synchronization
- `src/metrics_calculator.py` - Financial calculations
- `src/statistical_analyzer.py` - Correlation analysis

### 🔍 **Search & Discovery**
- `src/stock_database.py` - 53+ stocks with intelligent search
- Autocomplete with fuzzy matching and relevance scoring
- Multi-market support (US, India, Crypto)

### 📈 **Visualization**
- `src/visualizations.py` - Interactive Plotly charts
- Time series, scatter plots, bar charts, calendar heatmaps
- Real-time updates and responsive design

### ⚡ **Performance**
- `src/cache_manager.py` - Intelligent caching with TTL
- Sub-second autocomplete responses
- Optimized data structures and algorithms

### 🧪 **Testing**
- Comprehensive test suite with 100% core functionality coverage
- Property-based testing for statistical correctness
- Integration tests for end-to-end workflows

### 🚀 **Deployment**
- AWS Amplify ready with `amplify.yml`
- Docker, Heroku, Railway configurations
- Production optimizations and security headers

## Development Workflow

1. **Setup**: `pip install -r requirements.txt`
2. **Run**: `python app.py`
3. **Test**: `python test_complete_system.py`
4. **Build**: `python build.py`
5. **Deploy**: Follow `DEPLOYMENT.md` guide

## Architecture Highlights

- **MCP Integration**: Model Context Protocol for data fetching
- **Modular Design**: Loosely coupled components
- **Type Safety**: Comprehensive data validation
- **Performance**: Intelligent caching and optimization
- **Scalability**: Production-ready with health monitoring
- **Multi-Market**: Global stock market support