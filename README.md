# 🌙 Stock Moon Dashboard

A real-time interactive dashboard analyzing relationships between stock prices and moon phases with intelligent suggestions and Python deployment.

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/dineshrajdhanapathyDD/stock.git
cd stock

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Access dashboard
open http://localhost:8050
```

## 📊 Features

- **🔍 Intelligent Stock Search**: Dynamic suggestions with autocomplete
- **📈 Real-time Data**: Yahoo Finance + Moon Phase APIs
- **📊 Interactive Charts**: Plotly visualizations with statistical analysis
- **🌙 Moon Phase Analysis**: 8 lunar phases with correlation testing
- **🌍 Global Markets**: US stocks, Indian NSE/BSE, cryptocurrencies
- **🚀 Python Ready**: Simple pip install and run
- **📱 Mobile Responsive**: Works on all devices

## 🛠️ Tech Stack

- **Backend**: Python, Dash, Flask
- **Frontend**: Plotly.js, Bootstrap
- **Data**: Yahoo Finance API, Open-Meteo Astronomy
- **Deployment**: Pure Python, Railway, Render, Heroku
- **Hosting**: Railway, Render, Heroku, DigitalOcean

## 📋 API Endpoints

- `GET /health` - Health check
- `GET /ready` - Readiness probe
- `GET /api/suggestions?q=query&limit=10` - Stock suggestions

## 🐍 Python Deployment

### Local Development

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

## ☁️ Cloud Deployment

### Railway (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway up
```

### Render.com

1. Connect GitHub repository
2. Create Web Service
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python app.py`

### Heroku

```bash
# Deploy with Heroku CLI
echo "web: python app.py" > Procfile
heroku create your-app-name
git push heroku main
```

### DigitalOcean App Platform

1. Connect GitHub repository
2. Select Python deployment
3. Build Command: `pip install -r requirements.txt`
4. Run Command: `python app.py`

## 🔧 Environment Variables

```bash
PORT=8050                    # Application port
DASH_DEBUG=False            # Debug mode
DASH_HOST=0.0.0.0          # Host binding
DASH_COMPRESS=True         # Response compression
```

## 📁 Project Structure

```
├── app.py                 # Main application
├── requirements.txt       # Dependencies
├── scripts/              # Deployment scripts
├── src/                  # Source code
│   ├── dashboard.py      # Main dashboard
│   ├── suggestions_api.py # Dynamic suggestions
│   ├── mcp_tools.py      # Data fetching
│   ├── stock_database.py # Stock database
│   └── [8 more modules]  # Analysis & visualization
├── scripts/              # Deployment scripts
│   └── deploy.sh         # Multi-platform deployment
├── tests/                # Test suite
└── docs/                 # Documentation
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python tests/test_complete_system.py

# Test with coverage
python -m pytest tests/ --cov=src
```

## 📊 Stock Database

**53+ Stocks Supported:**

- **US Markets**: AAPL, GOOGL, MSFT, TSLA, AMZN, META, NVDA, etc.
- **Indian Markets**: RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS, etc.
- **Cryptocurrencies**: BTC-USD, ETH-USD

## 🌙 Moon Phase Analysis

Analyzes 8 distinct moon phases:
- 🌑 New Moon → 🌒 Waxing Crescent → 🌓 First Quarter → 🌔 Waxing Gibbous
- 🌕 Full Moon → 🌖 Waning Gibbous → 🌗 Last Quarter → 🌘 Waning Crescent

## 📈 Statistical Analysis

- **Correlations**: Pearson & Spearman coefficients
- **Volatility**: Rolling standard deviation analysis
- **Significance Testing**: P-values and effect sizes
- **Phase Comparison**: Returns and volatility by moon phase

## 🔍 Intelligent Search

Dynamic stock suggestions with:
- **Symbol matching**: Type "AAPL" → Apple Inc.
- **Company name**: Type "Apple" → AAPL
- **Sector search**: Type "tech" → All technology stocks
- **Relevance scoring**: Most relevant results first

## 🚀 Deployment Options

| Platform | Difficulty | Cost | Features |
|----------|------------|------|----------|
| **Local Python** | Easy | Free | Full control |
| **Railway** | Easy | Free tier | Auto-deploy |
| **Render** | Easy | Free tier | GitHub integration |
| **Heroku** | Medium | Paid | Mature platform |
| **DigitalOcean** | Medium | Paid | Scalable |

## 📞 Support

- **Issues**: GitHub repository issues
- **Documentation**: See `docs/` directory
- **Deployment Help**: Run `./scripts/deploy.sh`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## 📝 License

Educational and research purposes. Respect API usage limits.

---

**🌙 Start analyzing stock-moon correlations with: `python app.py`** 📈