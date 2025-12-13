# 🚀 Stock Moon Dashboard - Deployment Guide

Complete deployment guide for the Stock Moon Dashboard across multiple platforms including AWS Amplify, Heroku, Docker, and more.

## 📋 **Prerequisites**

### **System Requirements**
- **Python**: 3.8 or higher
- **Memory**: Minimum 512MB RAM (1GB+ recommended)
- **Storage**: 100MB for application files
- **Network**: Internet connection for API access

### **Development Tools**
- **Git**: For version control
- **Node.js**: 16+ (for AWS Amplify CLI)
- **Docker**: Latest version (for containerized deployment)
- **AWS CLI**: Configured with appropriate permissions

---

## 🌐 **AWS Amplify Deployment (Recommended)**

AWS Amplify provides managed hosting with automatic scaling, custom domains, and continuous deployment.

### **Step 1: Setup AWS Amplify CLI**

```bash
# Install Amplify CLI globally
npm install -g @aws-amplify/cli

# Configure Amplify with your AWS credentials
amplify configure

# Follow the interactive setup:
# 1. Sign in to AWS Console
# 2. Create IAM user with AdministratorAccess
# 3. Enter Access Key ID and Secret Access Key
# 4. Choose AWS region (e.g., us-east-1)
```

### **Step 2: Initialize Amplify Project**

```bash
# Navigate to your project directory
cd stock-moon-dashboard

# Initialize Amplify
amplify init

# Configuration options:
# Project name: stock-moon-dashboard
# Environment name: prod
# Default editor: Visual Studio Code
# App type: javascript
# Framework: react (we'll customize for Python)
# Source Directory Path: src
# Distribution Directory Path: dist
# Build Command: python build.py
# Start Command: python app.py
# AWS Profile: default
```

### **Step 3: Configure Build Settings**

The `amplify.yml` file is already configured for Python/Dash deployment:

```yaml
version: 1
applications:
  - frontend:
      phases:
        preBuild:
          commands:
            - yum update -y
            - yum install -y python3 python3-pip
            - python3 -m pip install --upgrade pip
            - python3 -m pip install -r requirements.txt
        build:
          commands:
            - python3 test_complete_system.py
            - python3 -c "from src.dashboard import app; print('Dashboard ready')"
        postBuild:
          commands:
            - echo 'python3 app.py' > start.sh
            - chmod +x start.sh
```

### **Step 4: Add Hosting**

```bash
# Add hosting service
amplify add hosting

# Choose hosting type:
# ❯ Amplify Console (Managed hosting with custom domains, Continuous deployment)
#   Amazon CloudFront and S3

# Deployment type:
# ❯ Continuous deployment (Git-based deployments)
#   Manual deployment
```

### **Step 5: Environment Variables**

Set environment variables in Amplify Console:

```bash
# Required environment variables
PYTHONPATH=/opt/python
PORT=8050
DASH_DEBUG=False
DASH_HOST=0.0.0.0
DASH_REQUESTS_PATHNAME_PREFIX=/

# Optional performance settings
DASH_COMPRESS=True
DASH_SERVE_LOCALLY=False
```

### **Step 6: Deploy**

```bash
# Deploy to AWS Amplify
amplify publish

# Monitor deployment progress
amplify status

# View deployment logs
amplify console
```

### **Step 7: Custom Domain (Optional)**

```bash
# Add custom domain through Amplify Console
# 1. Navigate to Domain Management
# 2. Add domain (e.g., stockmoon.yourdomain.com)
# 3. Configure DNS settings
# 4. Wait for SSL certificate provisioning (5-10 minutes)
```

### **Amplify Deployment Benefits**
- ✅ **Automatic scaling** based on traffic
- ✅ **Global CDN** for fast worldwide access
- ✅ **SSL certificates** automatically managed
- ✅ **Custom domains** with Route 53 integration
- ✅ **Continuous deployment** from Git repositories
- ✅ **Environment management** (dev, staging, prod)

---

## 🟣 **Heroku Deployment**

Heroku provides simple deployment with managed infrastructure.

### **Step 1: Prepare Heroku Files**

```bash
# Create Procfile
echo "web: python app.py" > Procfile

# Create runtime.txt
echo "python-3.9.16" > runtime.txt

# Update app.py for Heroku
# Ensure the app runs on the PORT environment variable
```

### **Step 2: Heroku Configuration**

```bash
# Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create Heroku app
heroku create stock-moon-dashboard-prod

# Set environment variables
heroku config:set DASH_DEBUG=False
heroku config:set DASH_HOST=0.0.0.0
heroku config:set PORT=8050
```

### **Step 3: Deploy to Heroku**

```bash
# Add Heroku remote
git remote add heroku https://git.heroku.com/stock-moon-dashboard-prod.git

# Deploy
git push heroku main

# Open deployed app
heroku open

# View logs
heroku logs --tail
```

### **Heroku Deployment Benefits**
- ✅ **Simple deployment** with Git push
- ✅ **Automatic dependency** management
- ✅ **Built-in monitoring** and logging
- ✅ **Add-ons ecosystem** for databases, caching, etc.
- ✅ **Free tier available** for testing

---

## 🐳 **Docker Deployment**

Containerized deployment for consistent environments across platforms.

### **Step 1: Create Dockerfile**

```dockerfile
# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DASH_HOST=0.0.0.0
ENV DASH_PORT=8050

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Expose port
EXPOSE 8050

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8050/ || exit 1

# Run application
CMD ["python", "app.py"]
```

### **Step 2: Create Docker Compose**

```yaml
# docker-compose.yml
version: '3.8'

services:
  stock-moon-dashboard:
    build: .
    ports:
      - "8050:8050"
    environment:
      - DASH_DEBUG=False
      - DASH_HOST=0.0.0.0
      - DASH_PORT=8050
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8050/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Optional: Add Redis for caching
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
```

### **Step 3: Build and Deploy**

```bash
# Build Docker image
docker build -t stock-moon-dashboard .

# Run container
docker run -d \
  --name stock-moon-dashboard \
  -p 8050:8050 \
  -e DASH_DEBUG=False \
  stock-moon-dashboard

# Or use Docker Compose
docker-compose up -d

# View logs
docker logs stock-moon-dashboard

# Stop container
docker stop stock-moon-dashboard
```

### **Docker Deployment Benefits**
- ✅ **Consistent environment** across development and production
- ✅ **Easy scaling** with orchestration tools
- ✅ **Isolation** from host system
- ✅ **Version control** for infrastructure
- ✅ **Multi-platform support** (Linux, Windows, macOS)

---

## 🚄 **Railway Deployment**

Modern deployment platform with simple Git-based deployments.

### **Step 1: Install Railway CLI**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login
```

### **Step 2: Deploy to Railway**

```bash
# Initialize Railway project
railway init

# Deploy current directory
railway up

# Set environment variables
railway variables set DASH_DEBUG=False
railway variables set DASH_HOST=0.0.0.0
railway variables set PORT=8050

# Open deployed application
railway open
```

### **Railway Deployment Benefits**
- ✅ **Zero-config deployment** from Git
- ✅ **Automatic HTTPS** and custom domains
- ✅ **Built-in databases** and services
- ✅ **Usage-based pricing** with generous free tier
- ✅ **Real-time logs** and monitoring

---

## ☁️ **Google Cloud Platform (GCP) Deployment**

Deploy using Google App Engine for serverless scaling.

### **Step 1: Create app.yaml**

```yaml
# app.yaml
runtime: python39

env_variables:
  DASH_DEBUG: "False"
  DASH_HOST: "0.0.0.0"
  PORT: "8080"

automatic_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_utilization: 0.6

resources:
  cpu: 1
  memory_gb: 1
  disk_size_gb: 10
```

### **Step 2: Deploy to App Engine**

```bash
# Install Google Cloud SDK
# Download from: https://cloud.google.com/sdk/docs/install

# Initialize gcloud
gcloud init

# Deploy to App Engine
gcloud app deploy

# View deployed app
gcloud app browse
```

---

## 🔧 **Environment Configuration**

### **Required Environment Variables**

```bash
# Core application settings
DASH_HOST=0.0.0.0          # Host to bind the server
DASH_PORT=8050             # Port to run the server
DASH_DEBUG=False           # Debug mode (False for production)

# Performance settings
DASH_COMPRESS=True         # Enable gzip compression
DASH_SERVE_LOCALLY=False   # Serve assets from CDN

# Security settings
DASH_REQUESTS_PATHNAME_PREFIX=/  # URL prefix for the app
```

### **Optional Environment Variables**

```bash
# Caching configuration
CACHE_TTL=3600            # Cache time-to-live in seconds
CACHE_MAX_SIZE=1000       # Maximum cache entries

# API configuration
YAHOO_FINANCE_TIMEOUT=30  # API request timeout
MAX_RETRIES=3             # Maximum API retry attempts

# Logging configuration
LOG_LEVEL=INFO            # Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_FORMAT=json           # Log format (json, text)
```

---

## 📊 **Performance Optimization**

### **Production Optimizations**

```python
# Update app.py for production
import os

# Production configuration
if os.getenv('DASH_DEBUG', 'True').lower() == 'false':
    app.run(
        host=os.getenv('DASH_HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 8050)),
        debug=False,
        dev_tools_hot_reload=False,
        dev_tools_ui=False,
        dev_tools_props_check=False
    )
else:
    # Development configuration
    app.run(debug=True)
```

### **Caching Strategy**

```python
# Enhanced caching for production
from functools import lru_cache
import redis

# Redis caching (optional)
if os.getenv('REDIS_URL'):
    import redis
    redis_client = redis.from_url(os.getenv('REDIS_URL'))
    
    @lru_cache(maxsize=1000)
    def cached_stock_data(symbol, start_date, end_date):
        cache_key = f"stock:{symbol}:{start_date}:{end_date}"
        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
        
        data = fetch_stock_data(symbol, start_date, end_date)
        redis_client.setex(cache_key, 3600, json.dumps(data))
        return data
```

---

## 🔒 **Security Considerations**

### **Production Security Checklist**

- ✅ **HTTPS enforcement** (handled by deployment platforms)
- ✅ **Environment variables** for sensitive configuration
- ✅ **Input validation** for all user inputs
- ✅ **Rate limiting** for API endpoints
- ✅ **CORS configuration** for cross-origin requests
- ✅ **Security headers** (CSP, HSTS, X-Frame-Options)

### **Security Headers Configuration**

```python
# Add security headers to Dash app
@app.server.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

---

## 📈 **Monitoring and Logging**

### **Application Monitoring**

```python
# Add application monitoring
import logging
import time
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Performance monitoring decorator
def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logging.info(f"{func.__name__} completed in {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logging.error(f"{func.__name__} failed after {duration:.2f}s: {e}")
            raise
    return wrapper
```

### **Health Check Endpoint**

```python
# Add health check endpoint
@app.server.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }
```

---

## 🚨 **Troubleshooting**

### **Common Deployment Issues**

**Issue: Module not found errors**
```bash
# Solution: Ensure PYTHONPATH is set correctly
export PYTHONPATH=/app:$PYTHONPATH
```

**Issue: Port binding errors**
```bash
# Solution: Use environment PORT variable
port = int(os.environ.get('PORT', 8050))
app.run(host='0.0.0.0', port=port)
```

**Issue: Memory errors on large datasets**
```bash
# Solution: Implement data pagination and caching
# Limit analysis to reasonable date ranges
# Use efficient data structures (pandas with appropriate dtypes)
```

**Issue: API rate limiting**
```bash
# Solution: Implement exponential backoff
import time
import random

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait_time)
```

### **Performance Troubleshooting**

```bash
# Monitor memory usage
import psutil
import os

def log_memory_usage():
    process = psutil.Process(os.getpid())
    memory_mb = process.memory_info().rss / 1024 / 1024
    logging.info(f"Memory usage: {memory_mb:.2f} MB")

# Monitor API response times
import time

def monitor_api_calls(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        logging.info(f"API call took {duration:.2f}s")
        return result
    return wrapper
```

---

## 📞 **Support and Maintenance**

### **Deployment Support**

- 📧 **Email**: deployment-support@stockmoondashboard.com
- 💬 **Discord**: [Join our deployment channel](https://discord.gg/deployment)
- 📚 **Documentation**: [Complete deployment docs](https://docs.stockmoondashboard.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/your-repo/stock-moon-dashboard/issues)

### **Maintenance Schedule**

- **Daily**: Automated health checks and monitoring
- **Weekly**: Dependency updates and security patches
- **Monthly**: Performance optimization and feature updates
- **Quarterly**: Major version updates and infrastructure reviews

---

**The Stock Moon Dashboard is designed for easy deployment across multiple platforms. Choose the deployment method that best fits your needs and infrastructure requirements.** 🚀🌙📈