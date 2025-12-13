#!/bin/bash

# 🚀 Stock Moon Dashboard - Quick Deploy Script

echo "🌙 Stock Moon Dashboard - Docker Deployment"
echo "============================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose."
    exit 1
fi

echo "✅ Docker environment ready"

# Build and start services
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "🎉 Deployment Complete!"
echo "========================"
echo "📊 Static Dashboard: http://localhost:8080"
echo "🔍 Suggestions API:  http://localhost:8081"
echo ""
echo "📋 Available Commands:"
echo "  docker-compose logs -f     # View logs"
echo "  docker-compose stop        # Stop services"
echo "  docker-compose down        # Remove containers"
echo ""
echo "🌐 Ready for production!"