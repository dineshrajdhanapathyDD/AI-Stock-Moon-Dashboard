# 🌙 Data Weaver AI - Stock Moon Dashboard

A lightweight dashboard that analyzes relationships between stock price behavior and moon phases using MCP tools and external APIs.

## 🚀 Features

- **Intelligent Stock Search**: Auto-complete with 53+ popular stocks from US and Indian markets
- **Real-time Data Fetching**: Yahoo Finance (stocks) + Open-Meteo Astronomy (moon phases)
- **Interactive Visualizations**: Time series, scatter plots, bar charts, calendar heatmaps
- **Statistical Analysis**: Correlation testing, volatility analysis, significance testing
- **Automated Insights**: Pattern recognition and narrative generation
- **MCP Tools Integration**: Model Context Protocol for data fetching
- **Global Market Support**: US stocks, Indian NSE/BSE stocks, and cryptocurrencies
- **No Backend Required**: Pure client-side processing with Python/Dash

## 📋 Requirements

- Python 3.8+
- Internet connection for API access
- Modern web browser

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard:**
   ```bash
   python app.py
   ```

4. **Open your browser and navigate to:**
   ```
   http://localhost:8050
   ```

## 🔧 MCP Tools Testing

Test the MCP tools independently:

```bash
# List available tools
python mcp_server.py list

# Test stock data fetching
python mcp_server.py test-stock

# Test moon phase data fetching  
python mcp_server.py test-moon
```

## 📊 Usage

1. **Search for Stocks**: Use the intelligent search with auto-complete
   - Type company names: "Apple", "Google", "Reliance", "TCS"
   - Type symbols: "AAPL", "GOOGL", "RELIANCE.NS", "TCS.NS"
   - Search by sector: "bank", "tech", "energy"
   - Use quick-select buttons for popular stocks
2. **Select Date Range**: Choose start and end dates for analysis
3. **Configure Parameters**: Set rolling window for volatility calculations
4. **Click Analyze**: Fetch data and generate visualizations
5. **Explore Results**: Interactive charts and statistical insights

### 🔍 Advanced Stock Search Features

#### **Intelligent Autocomplete System**

- **Real-time suggestions** as you type (sub-second response)
- **Smart matching** by company name, symbol, or business sector
- **Visual market indicators** with country flags (🇺🇸 US, 🇮🇳 India, 💰 Crypto)
- **Sector tags** for easy categorization and discovery
- **Relevance scoring** with most relevant results first

#### **Search Methods**

**By Company Name:**

```bash
Type: "apple" → See: AAPL - Apple Inc.
Type: "google" → See: GOOGL - Alphabet Inc. (Google)  
Type: "reliance" → See: RELIANCE.NS - Reliance Industries Ltd.
Type: "tata" → See: TCS.NS - Tata Consultancy Services Ltd.
```

**By Stock Symbol:**

```bash
Type: "AAPL" → Apple Inc. (US Technology)
Type: "MSFT" → Microsoft Corporation (US Technology)
Type: "RELIANCE.NS" → Reliance Industries Ltd. (India Energy)
Type: "TCS.NS" → Tata Consultancy Services Ltd. (India Technology)
```

**By Business Sector:**

```bash
Type: "bank" → All banking stocks (HDFCBANK.NS, ICICIBANK.NS, JPM, BAC)
Type: "tech" → Technology companies (AAPL, GOOGL, TCS.NS, INFY.NS)
Type: "energy" → Energy sector (XOM, CVX, RELIANCE.NS, ONGC.NS)
Type: "pharma" → Pharmaceutical companies (PFE, JNJ, SUNPHARMA.NS)
```

#### **Quick-Select Buttons**

- **US Market Leaders**: AAPL, GOOGL, MSFT, TSLA (Blue buttons)
- **Indian Market Leaders**: RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS (Green buttons)
- **One-click selection** for instant analysis
- **Color-coded by market** for easy identification

#### **Comprehensive Stock Database**

**US Market Coverage (21 stocks):**

- **Technology**: AAPL, GOOGL, MSFT, META, NVDA, NFLX
- **Financial**: JPM, BAC, WFC, GS  
- **Healthcare**: JNJ, PFE
- **Consumer**: KO, PEP, WMT
- **Industrial**: BA, CAT
- **Energy**: XOM, CVX
- **Automotive**: TSLA
- **E-commerce**: AMZN

**Indian Market Coverage (30 stocks):**

- **Technology**: TCS.NS, INFY.NS, WIPRO.NS, TECHM.NS, HCLTECH.NS
- **Financial**: HDFCBANK.NS, ICICIBANK.NS, SBIN.NS, KOTAKBANK.NS, AXISBANK.NS
- **Energy**: RELIANCE.NS, ONGC.NS
- **Telecom**: BHARTIARTL.NS
- **Consumer Goods**: ITC.NS, ASIANPAINT.NS, NESTLEIND.NS, HINDUNILVR.NS
- **Industrial**: LT.NS, ADANIPORTS.NS
- **Materials**: ULTRACEMCO.NS, JSWSTEEL.NS, TATASTEEL.NS, COALINDIA.NS
- **Utilities**: POWERGRID.NS, NTPC.NS
- **Healthcare**: SUNPHARMA.NS
- **Automotive**: MARUTI.NS
- **Consumer Discretionary**: TITAN.NS

**Cryptocurrency Support (2 assets):**

- **BTC-USD**: Bitcoin USD
- **ETH-USD**: Ethereum USD

#### **Search Performance**

- **Response Time**: < 100ms for autocomplete suggestions
- **Database Size**: 53+ stocks across 14 sectors and 3 markets
- **Search Index**: Optimized for O(1) average lookup performance
- **Caching**: Intelligent caching for repeated searches
- **Error Handling**: Graceful handling of invalid queries

## 🌙 Moon Phase Analysis

The dashboard analyzes 8 moon phases:
- 🌑 New Moon
- 🌒 Waxing Crescent  
- 🌓 First Quarter
- 🌔 Waxing Gibbous
- 🌕 Full Moon
- 🌖 Waning Gibbous
- 🌗 Last Quarter
- 🌘 Waning Crescent

## 📈 Metrics Calculated

- **Daily Returns**: Percentage price changes
- **Volatility**: Rolling standard deviation
- **Moon Illumination**: Percentage of visible moon surface
- **Phase Correlations**: Statistical relationships
- **Anomaly Detection**: Unusual price movements
- **Full Moon Windows**: ±2 day periods around full moons

## 🔍 Statistical Tests

- Pearson & Spearman correlations
- T-tests for volatility differences
- Effect size calculations
- P-value significance testing

## 🏗️ Project Structure

```
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── mcp_server.py         # MCP tools server
├── index.html            # Landing page
├── amplify.yml           # Current deployment config
├── src/                  # Source code
│   ├── dashboard.py      # Main Dash application
│   ├── mcp_tools.py      # MCP data fetching tools
│   ├── statistical_analyzer.py # Analysis engine
│   └── [8 more modules]  # Complete application
├── deployment/           # Platform configurations
│   ├── aws-amplify/      # AWS Amplify setup
│   ├── render/           # Render.com config
│   ├── heroku/           # Heroku config
│   └── [4 more platforms] # All deployment options
├── docs/                 # Documentation
├── tests/                # Test suite
└── README.md             # This file
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for complete details.

## 🌐 API Endpoints Used

- **Yahoo Finance**: `https://query1.finance.yahoo.com/v8/finance/chart/`
  - Supports global markets: US, India (.NS), Europe, Asia
- **Moon Phase**: Astronomical calculations for any location

## 🚨 Error Handling

The application includes comprehensive error handling for:
- Network failures and API timeouts
- Invalid stock symbols or date ranges
- Missing or corrupted data
- Rate limiting and retry logic

## 🔮 Future Enhancements

- Additional statistical tests
- More visualization types
- Export functionality
- Trading simulation module
- Multiple location support for moon data
- Historical backtesting capabilities

## 🚀 Deployment Options

### **One-Click Deploy**

[![Deploy with Amplify Console](https://oneclick.amplifyapp.com/button.svg)](https://console.aws.amazon.com/amplify/home#/deploy?repo=https://github.com/dineshrajdhanapathyDD/stock)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

[![Deploy to Railway](https://railway.app/button.svg)](https://railway.app/new)

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

**📁 All deployment configurations are in the [`deployment/`](deployment/) directory**

### **Local Development**

```bash
# Quick start for local development
git clone <repository-url>
cd stock-moon-dashboard
pip install -r requirements.txt
python app.py
# Access at http://localhost:8050
```

### **GitHub Pages Static Demo**

```bash
# Automatic deployment via GitHub Actions
git push origin main
# Demo will be available at: https://yourusername.github.io/stock-moon-dashboard/

# Or generate manually
python generate_static_demo.py
python setup_github_pages.py
```



### **AWS Amplify Deployment**

Deploy the dashboard to AWS Amplify for global access with automatic scaling:

#### **Prerequisites**

- AWS Account with Amplify access
- AWS CLI configured
- Node.js 16+ installed
- Python 3.8+ installed

#### **Step 1: Prepare for Amplify**

```bash
# Install Amplify CLI
npm install -g @aws-amplify/cli

# Configure Amplify
amplify configure
```

#### **Step 2: Initialize Amplify Project**

```bash
# Initialize Amplify in your project
amplify init

# Follow the prompts:
# Project name: stock-moon-dashboard
# Environment: prod
# Default editor: Visual Studio Code
# App type: javascript
# Framework: react (we'll customize for Python)
# Source directory: src
# Distribution directory: dist
# Build command: python build.py
# Start command: python app.py
```

#### **Step 3: Add Hosting**

```bash
# Add hosting with Amplify Console
amplify add hosting

# Select: Amplify Console (Managed hosting with custom domains, Continuous deployment)
# Manual deployment or Continuous deployment: Continuous deployment
```

#### **Step 4: Deploy**

```bash
# Deploy to AWS
amplify publish
```

#### **Custom Build Configuration**

The `amplify.yml` is already configured for Python/Dash deployment:

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - yum update -y
        - yum install -y python3 python3-pip python3-devel gcc
        - python3 -m pip install --upgrade pip
        - python3 -m pip install -r requirements.txt
    build:
      commands:
        - echo "Build completed"
  artifacts:
    baseDirectory: /
    files:
      - '**/*'
```

#### **Environment Variables**

Set these in Amplify Console → App Settings → Environment Variables:

```bash
PYTHONPATH=/opt/python
PORT=8050
DASH_DEBUG=False
DASH_HOST=0.0.0.0
```

#### **Custom Domain Setup**

```bash
# Add custom domain (optional)
amplify add hosting

# Configure custom domain in Amplify Console:
# 1. Go to Domain Management
# 2. Add domain (e.g., stockmoon.yourdomain.com)
# 3. Configure DNS settings
# 4. Wait for SSL certificate provisioning
```

### **Alternative Deployment Options**

#### **Heroku Deployment**

```bash
# Create Procfile
echo "web: python app.py" > Procfile

# Create runtime.txt
echo "python-3.9.16" > runtime.txt

# Deploy to Heroku
heroku create stock-moon-dashboard
git push heroku main
```

#### **Docker Deployment**

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8050

CMD ["python", "app.py"]
```

```bash
# Build and run Docker container
docker build -t stock-moon-dashboard .
docker run -p 8050:8050 stock-moon-dashboard
```

#### **Railway Deployment**

```bash
# Deploy to Railway
npm install -g @railway/cli
railway login
railway init
railway up
```

## 🇮🇳 Indian Stock Market Support

The dashboard fully supports Indian stocks from NSE and BSE:

- **Format**: Use `.NS` suffix (e.g., `RELIANCE.NS`, `TCS.NS`)
- **Currency**: Prices displayed in Indian Rupees (₹)
- **Coverage**: 1,600+ NSE stocks, 5,000+ BSE stocks
- **Location**: Mumbai coordinates for moon phase calculations
- **See**: `INDIAN_STOCKS_GUIDE.md` for complete details

## 📚 Additional Documentation

- **[Stock Search Features Guide](STOCK_SEARCH_FEATURES.md)** - Comprehensive search functionality
- **[Indian Stocks Guide](INDIAN_STOCKS_GUIDE.md)** - Indian market integration details
- **[Blog Post](BLOG_POST.md)** - Complete project case study with Kiro AI
- **[Deployment Guide](DEPLOYMENT.md)** - Detailed deployment instructions

## 📝 License

This project is for educational and research purposes. Please respect API usage limits and terms of service for external data providers.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the dashboard functionality.

---

**Disclaimer**: This tool is for research and educational purposes only. Past performance does not guarantee future results. Always conduct your own research before making investment decisions.