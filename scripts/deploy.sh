#!/bin/bash

# Stock Moon Dashboard Deployment Script
set -e

echo "🌙 Stock Moon Dashboard - Deployment Script"
echo "============================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    log_success "Docker and Docker Compose are installed"
}

# Build and deploy
deploy_docker() {
    log_info "Building Docker image..."
    docker-compose build
    
    log_info "Starting services..."
    docker-compose up -d
    
    log_info "Waiting for services to be ready..."
    sleep 10
    
    # Check if service is running
    if docker-compose ps | grep -q "Up"; then
        log_success "Services are running!"
        log_info "Dashboard available at: http://localhost:8050"
        log_info "Health check: http://localhost:8050/health"
    else
        log_error "Services failed to start"
        docker-compose logs
        exit 1
    fi
}

# Deploy to cloud platforms
deploy_render() {
    log_info "Deploying to Render.com..."
    log_info "1. Push code to GitHub"
    log_info "2. Connect repository to Render"
    log_info "3. Use Docker deployment"
    log_info "4. Set environment variables"
}

deploy_railway() {
    log_info "Deploying to Railway..."
    if command -v railway &> /dev/null; then
        railway login
        railway init
        railway up
    else
        log_warning "Railway CLI not installed"
        log_info "Install: npm install -g @railway/cli"
    fi
}

deploy_fly() {
    log_info "Deploying to Fly.io..."
    if command -v flyctl &> /dev/null; then
        flyctl launch
        flyctl deploy
    else
        log_warning "Fly CLI not installed"
        log_info "Install: curl -L https://fly.io/install.sh | sh"
    fi
}

# Main deployment options
show_menu() {
    echo ""
    echo "🚀 Deployment Options:"
    echo "1. Local Docker deployment"
    echo "2. Render.com (recommended)"
    echo "3. Railway"
    echo "4. Fly.io"
    echo "5. Show logs"
    echo "6. Stop services"
    echo "7. Exit"
    echo ""
}

# Main script
main() {
    check_docker
    
    while true; do
        show_menu
        read -p "Select option (1-7): " choice
        
        case $choice in
            1)
                deploy_docker
                ;;
            2)
                deploy_render
                ;;
            3)
                deploy_railway
                ;;
            4)
                deploy_fly
                ;;
            5)
                docker-compose logs -f
                ;;
            6)
                log_info "Stopping services..."
                docker-compose down
                log_success "Services stopped"
                ;;
            7)
                log_info "Goodbye!"
                exit 0
                ;;
            *)
                log_error "Invalid option. Please select 1-7."
                ;;
        esac
    done
}

# Run main function
main