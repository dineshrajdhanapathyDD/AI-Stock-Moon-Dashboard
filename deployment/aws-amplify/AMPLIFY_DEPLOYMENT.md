# 🚀 AWS Amplify Deployment Guide

Complete guide to deploy the Stock Moon Dashboard on AWS Amplify with automatic scaling and global CDN.

## 📋 **Prerequisites**

- AWS Account with Amplify access
- GitHub repository with the Stock Moon Dashboard
- AWS CLI configured (optional but recommended)
- Node.js 16+ for Amplify CLI

## 🎯 **Deployment Options**

### **Option 1: Amplify Console (Recommended)**
✅ **Easiest setup**  
✅ **Visual interface**  
✅ **Automatic deployments**

### **Option 2: Amplify CLI**
✅ **Command line control**  
✅ **Advanced configuration**  
✅ **Infrastructure as code**

---

## 🌐 **Option 1: Deploy via Amplify Console**

### **Step 1: Connect Repository**

1. **Go to AWS Amplify Console**
   - Visit: https://console.aws.amazon.com/amplify/
   - Click "Get Started" under "Deploy"

2. **Connect GitHub Repository**
   - Select "GitHub" as source
   - Authorize AWS Amplify to access your repositories
   - Select your `stock-moon-dashboard` repository
   - Choose `main` branch

### **Step 2: Configure Build Settings**

The `amplify.yml` file is already configured, but verify these settings:

```yaml
# Build settings are automatically detected from amplify.yml
App name: stock-moon-dashboard
Environment: production
Branch: main
```

### **Step 3: Environment Variables**

Add these environment variables in Amplify Console:

```bash
# Required Variables
PYTHONPATH=/opt/python:/opt/python/lib/python3.9/site-packages
PORT=8050
DASH_DEBUG=False
DASH_HOST=0.0.0.0

# Performance Variables
DASH_COMPRESS=True
DASH_SERVE_LOCALLY=False
DASH_REQUESTS_PATHNAME_PREFIX=/

# Optional Variables
CACHE_TTL=3600
MAX_RETRIES=3
LOG_LEVEL=INFO
```

### **Step 4: Deploy**

1. **Review and Deploy**
   - Review all settings
   - Click "Save and Deploy"
   - Wait for deployment (usually 5-10 minutes)

2. **Monitor Deployment**
   - Watch build logs in real-time
   - Check for any errors in the console
   - Verify all phases complete successfully

### **Step 5: Configure Domain (Optional)**

1. **Add Custom Domain**
   - Go to "Domain Management"
   - Click "Add domain"
   - Enter your domain (e.g., `stockmoon.yourdomain.com`)
   - Configure DNS settings
   - Wait for SSL certificate provisioning

---

## 💻 **Option 2: Deploy via Amplify CLI**

### **Step 1: Install Amplify CLI**

```bash
# Install Amplify CLI globally
npm install -g @aws-amplify/cli

# Configure Amplify with your AWS credentials
amplify configure
```

### **Step 2: Initialize Amplify Project**

```bash
# Navigate to your project directory
cd stock-moon-dashboard

# Initialize Amplify
amplify init

# Configuration prompts:
# Project name: stock-moon-dashboard
# Environment: prod
# Default editor: Visual Studio Code
# App type: javascript
# Framework: react (we'll customize for Python)
# Source directory: src
# Distribution directory: dist
# Build command: python build.py
# Start command: python app.py
# AWS Profile: default
```

### **Step 3: Add Hosting**

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

### **Step 4: Configure Environment**

```bash
# Set environment variables
amplify env add prod

# Configure production environment
amplify configure project
```

### **Step 5: Deploy**

```bash
# Deploy to AWS Amplify
amplify publish

# Monitor deployment
amplify status

# View deployment logs
amplify console
```

---

## ⚙️ **Advanced Configuration**

### **Custom Build Configuration**

The `amplify.yml` includes:

- **Backend Phase**: Python application deployment
- **Frontend Phase**: Static demo generation
- **Security Headers**: CSP, HSTS, XSS protection
- **Caching**: Optimized for performance
- **Error Handling**: Comprehensive error recovery

### **Environment-Specific Settings**

```bash
# Development Environment
amplify env add dev
amplify env checkout dev

# Production Environment  
amplify env add prod
amplify env checkout prod
```

### **Custom Domain with SSL**

```bash
# Add custom domain via CLI
amplify add hosting

# Configure domain in console
# 1. Go to Domain Management
# 2. Add domain (e.g., stockmoon.yourdomain.com)
# 3. Configure DNS settings:
#    - CNAME: www -> your-app-id.amplifyapp.com
#    - A: @ -> Amplify IP addresses
# 4. Wait for SSL certificate (5-10 minutes)
```

---

## 🔧 **Troubleshooting**

### **Common Issues**

**Issue: Python dependencies fail to install**
```bash
# Solution: Update requirements.txt with specific versions
pip freeze > requirements.txt
```

**Issue: Build timeout**
```bash
# Solution: Optimize build process in amplify.yml
# Remove unnecessary test steps for production builds
```

**Issue: Memory errors**
```bash
# Solution: Increase build resources
# Contact AWS support to increase build instance size
```

**Issue: Port binding errors**
```bash
# Solution: Ensure PORT environment variable is set
PORT=8050
DASH_HOST=0.0.0.0
```

### **Debug Build Issues**

```bash
# View detailed build logs
amplify console

# Check environment variables
amplify env get --name prod

# Test locally with same environment
export DASH_DEBUG=False
export PORT=8050
python app.py
```

---

## 📊 **Performance Optimization**

### **Build Performance**

```yaml
# Optimized amplify.yml settings
cache:
  paths:
    - ~/.cache/pip/**/*
    - /opt/python/**/*
```

### **Runtime Performance**

```bash
# Environment variables for optimization
DASH_COMPRESS=True
DASH_SERVE_LOCALLY=False
PYTHONPATH=/opt/python:/opt/python/lib/python3.9/site-packages
```

### **CDN Configuration**

Amplify automatically provides:
- Global CDN distribution
- Automatic compression
- Edge caching
- SSL termination

---

## 🔒 **Security Configuration**

### **Security Headers**

Already configured in `amplify.yml`:
- Content Security Policy (CSP)
- HTTP Strict Transport Security (HSTS)
- X-Frame-Options
- X-Content-Type-Options
- Referrer Policy

### **Environment Security**

```bash
# Secure environment variables
# Never commit sensitive data to repository
# Use Amplify Console to set environment variables
```

---

## 📈 **Monitoring & Analytics**

### **Built-in Monitoring**

Amplify provides:
- Build success/failure notifications
- Performance metrics
- Error tracking
- Access logs

### **Custom Monitoring**

```python
# Add to app.py for custom monitoring
import logging

# Configure CloudWatch logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## 🎯 **Deployment Checklist**

- [ ] Repository pushed to GitHub
- [ ] `amplify.yml` configured
- [ ] Environment variables set
- [ ] Build completes successfully
- [ ] Application starts without errors
- [ ] Health check endpoints respond
- [ ] Custom domain configured (optional)
- [ ] SSL certificate active
- [ ] Performance monitoring setup

---

## 🚀 **Success!**

Your Stock Moon Dashboard is now deployed on AWS Amplify with:

✅ **Global CDN** - Fast worldwide access  
✅ **Auto-scaling** - Handles traffic spikes  
✅ **SSL/HTTPS** - Secure connections  
✅ **Continuous Deployment** - Auto-deploy on git push  
✅ **Custom Domain** - Professional URL  
✅ **Monitoring** - Built-in analytics  

**Live URL**: `https://your-app-id.amplifyapp.com`  
**Custom Domain**: `https://your-custom-domain.com`

## 📞 **Support**

- **AWS Amplify Docs**: https://docs.amplify.aws/
- **Amplify Console**: https://console.aws.amazon.com/amplify/
- **GitHub Issues**: Report deployment issues in the repository

---

**Your Stock Moon Dashboard is now live on AWS Amplify with enterprise-grade infrastructure!** 🌙📈🚀