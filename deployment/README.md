# 🚀 Deployment Configurations

This directory contains deployment configurations for various platforms.

## 📁 Directory Structure

```
deployment/
├── aws-amplify/          # AWS Amplify deployment files
│   ├── amplify.yml       # Amplify build configuration
│   ├── amplify_env_vars.json
│   ├── deploy_amplify.py
│   └── AMPLIFY_*.md      # Documentation
├── render/               # Render.com deployment
│   └── render.yaml
├── heroku/              # Heroku deployment
│   ├── Procfile
│   └── runtime.txt
├── vercel/              # Vercel deployment
│   └── vercel.json
├── railway/             # Railway deployment
│   └── (auto-detected)
└── github-pages/        # GitHub Pages static demo
    ├── generate_static_demo.py
    └── setup_github_pages.py
```

## 🎯 Quick Deploy Options

### **AWS Amplify**
```bash
# Use files from deployment/aws-amplify/
# Copy amplify.yml to root for deployment
cp deployment/aws-amplify/amplify.yml ./
```

### **Render.com**
```bash
# Uses deployment/render/render.yaml
# Connect GitHub repository to Render
```

### **Heroku**
```bash
# Uses deployment/heroku/Procfile and runtime.txt
cp deployment/heroku/* ./
git push heroku main
```

### **Vercel**
```bash
# Uses deployment/vercel/vercel.json
cp deployment/vercel/vercel.json ./
```

### **GitHub Pages**
```bash
# Generate static demo
python deployment/github-pages/generate_static_demo.py
python deployment/github-pages/setup_github_pages.py
```

## 📋 Platform Comparison

| Platform | Type | Pros | Cons |
|----------|------|------|------|
| **AWS Amplify** | Static/Serverless | Global CDN, Auto-scaling | Complex setup |
| **Render** | Container | Easy setup, Free tier | Limited free hours |
| **Heroku** | Container | Simple, Popular | Paid plans only |
| **Vercel** | Serverless | Fast, Free tier | Function limits |
| **Railway** | Container | Modern, Simple | Newer platform |
| **GitHub Pages** | Static | Free, Simple | Static only |

## 🔧 Current Status

- ✅ **AWS Amplify**: Configured and ready
- ✅ **Render**: Configured with render.yaml
- ✅ **Heroku**: Configured with Procfile
- ✅ **Vercel**: Configured with vercel.json
- ✅ **Railway**: Auto-detects Python app
- ✅ **GitHub Pages**: Static demo generator ready

## 📞 Support

See individual platform documentation in each subdirectory for detailed setup instructions.