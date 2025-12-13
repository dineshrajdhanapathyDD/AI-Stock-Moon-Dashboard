#!/bin/bash
# Quick deployment script for Stock Moon Dashboard

echo "🌙 Stock Moon Dashboard - Quick Deploy"
echo "======================================"

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "🐳 Docker found - Using Docker deployment"
    
    # Build and run with Docker Compose
    echo "📦 Building Docker image..."
    docker-compose build
    
    echo "🚀 Starting application..."
    docker-compose up -d
    
    echo "✅ Dashboard deployed!"
    echo "🌐 Access at: http://localhost:8050"
    echo "📊 Health check: http://localhost:8050/health"
    echo ""
    echo "📋 Commands:"
    echo "  Stop:  docker-compose down"
    echo "  Logs:  docker-compose logs -f"
    echo "  Rebuild: docker-compose up --build"
    
elif command -v python3 &> /dev/null; then
    echo "🐍 Python found - Using local deployment"
    
    # Install dependencies
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    
    # Run application
    echo "🚀 Starting application..."
    python3 app.py &
    APP_PID=$!
    
    echo "✅ Dashboard deployed!"
    echo "🌐 Access at: http://localhost:8050"
    echo "📊 Health check: http://localhost:8050/health"
    echo ""
    echo "📋 Commands:"
    echo "  Stop: kill $APP_PID"
    echo "  Or press Ctrl+C"
    
else
    echo "❌ Neither Docker nor Python3 found"
    echo "💡 Please install Docker or Python 3.8+"
    exit 1
fi