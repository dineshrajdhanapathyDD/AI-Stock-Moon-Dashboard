# 📁 Project Structure

## 🏗️ **Clean Architecture**

```
stock-moon-dashboard/
├── 📱 Core Application
│   ├── app.py                    # Main application entry point
│   ├── mcp_server.py            # MCP tools server
│   ├── requirements.txt         # Python dependencies
│   └── src/                     # Source code
│       ├── __init__.py
│       ├── dashboard.py         # Main Dash application
│       ├── data_models.py       # Data structures
│       ├── mcp_tools.py         # MCP data fetching
│       ├── data_alignment.py    # Data processing
│       ├── metrics_calculator.py # Metrics computation
│       ├── statistical_analyzer.py # Statistical analysis
│       ├── visualizations.py    # Chart generation
│       ├── cache_manager.py     # Caching system
│       ├── data_validation.py   # Input validation
│       └── stock_database.py    # Stock database
│
├── 🚀 Deployment Configurations
│   └── deployment/
│       ├── aws-amplify/         # AWS Amplify files
│       ├── render/              # Render.com config
│       ├── heroku/              # Heroku config
│       ├── vercel/              # Vercel config
│       ├── railway/             # Railway config
│       └── github-pages/        # Static demo
│
├── 📚 Documentation
│   └── docs/
│       ├── DEPLOYMENT_*.md      # Deployment guides
│       ├── INDIAN_STOCKS_GUIDE.md
│       ├── STOCK_SEARCH_FEATURES.md
│       └── CONTRIBUTING.md
│
├── 🧪 Testing
│   └── tests/
│       ├── test_*.py           # All test files
│       └── test_complete_system.py
│
├── 🌐 Web Assets
│   ├── index.html              # Landing page
│   └── amplify.yml             # Current deployment config
│
└── 📋 Project Files
    ├── README.md               # Main documentation
    ├── .gitignore             # Git ignore rules
    └── .github/               # GitHub workflows
        └── workflows/
            ├── deploy.yml      # Deployment workflow
            └── pages.yml       # Pages workflow
```

## 🎯 **Key Components**

### **Core Application**
- **`app.py`**: Production-ready entry point with health checks
- **`src/dashboard.py`**: Interactive Dash web application
- **`src/mcp_tools.py`**: Yahoo Finance + Moon Phase APIs
- **`src/statistical_analyzer.py`**: Correlation and volatility analysis

### **Deployment Ready**
- **AWS Amplify**: Global CDN with auto-scaling
- **Render.com**: Container deployment with free tier
- **Heroku**: Traditional PaaS deployment
- **Vercel**: Serverless deployment
- **GitHub Pages**: Static demo version

### **Testing Suite**
- **Unit Tests**: Component-level testing
- **Integration Tests**: End-to-end workflows
- **System Tests**: Complete application validation
- **Indian Market Tests**: NSE/BSE specific testing

### **Documentation**
- **Deployment Guides**: Platform-specific instructions
- **Feature Guides**: Detailed functionality documentation
- **API Documentation**: MCP tools and data models
- **Contributing Guide**: Development setup and guidelines

## 🔧 **Development Workflow**

### **Local Development**
```bash
# Setup
git clone <repository>
cd stock-moon-dashboard
pip install -r requirements.txt

# Run application
python app.py
# Access at http://localhost:8050

# Run tests
python -m pytest tests/
```

### **Deployment**
```bash
# Choose platform and copy config
cp deployment/render/render.yaml ./
# or
cp deployment/aws-amplify/amplify.yml ./

# Deploy via platform-specific method
```

## 📊 **Features Overview**

### **Data Sources**
- **Yahoo Finance**: Real-time stock data (US, India, Crypto)
- **Open-Meteo**: Astronomical moon phase calculations
- **MCP Protocol**: Standardized data fetching

### **Analysis Capabilities**
- **Statistical Correlations**: Pearson, Spearman
- **Volatility Analysis**: Rolling standard deviation
- **Moon Phase Mapping**: 8 distinct lunar phases
- **Significance Testing**: P-values and effect sizes

### **Visualization Types**
- **Time Series**: Stock prices + moon illumination
- **Scatter Plots**: Price relationships
- **Bar Charts**: Phase-based analysis
- **Calendar Heatmaps**: Daily returns visualization

### **Interactive Features**
- **Intelligent Search**: 53+ stock autocomplete
- **Date Range Selection**: Flexible time periods
- **Parameter Configuration**: Rolling windows, thresholds
- **Real-time Updates**: Dynamic chart updates

## 🌐 **Deployment Status**

| Platform | Status | URL Pattern | Features |
|----------|--------|-------------|----------|
| **AWS Amplify** | ✅ Ready | `https://[app-id].amplifyapp.com` | CDN, SSL, Custom domains |
| **Render** | ✅ Ready | `https://[app-name].onrender.com` | Free tier, Auto-deploy |
| **Heroku** | ✅ Ready | `https://[app-name].herokuapp.com` | Paid plans, Add-ons |
| **Vercel** | ✅ Ready | `https://[app-name].vercel.app` | Serverless, Edge functions |
| **Railway** | ✅ Ready | `https://[app-name].railway.app` | Modern platform |
| **GitHub Pages** | ✅ Ready | `https://[user].github.io/[repo]` | Static demo only |

## 🎯 **Next Steps**

1. **Choose deployment platform** based on requirements
2. **Copy appropriate configuration** from deployment folder
3. **Set environment variables** as documented
4. **Deploy and monitor** application performance
5. **Configure custom domain** (optional)

## 📞 **Support**

- **Documentation**: See `docs/` directory
- **Issues**: GitHub repository issues
- **Deployment Help**: Platform-specific guides in `deployment/`