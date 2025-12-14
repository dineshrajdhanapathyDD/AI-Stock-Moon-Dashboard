# 🚀 Deployment Guide

## Quick Deploy Options

### 1. Local Python (Recommended)
```bash
pip install -r requirements.txt
python app.py
```
Access: http://localhost:8050

### 2. Railway
```bash
npm install -g @railway/cli
railway login
railway up
```

### 3. Render.com
1. Connect GitHub repository
2. Create Web Service
3. Build: `pip install -r requirements.txt`
4. Start: `python app.py`

### 4. Local Development
```bash
pip install -r requirements.txt
python app.py
```

## Environment Variables
- `PORT=8050` - Application port
- `DASH_DEBUG=False` - Production mode
- `DASH_HOST=0.0.0.0` - Host binding

## Health Checks
- `/health` - Basic health check
- `/ready` - Readiness probe
- `/api/suggestions` - Stock suggestions API