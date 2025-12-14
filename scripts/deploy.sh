#!/bin/bash

# Stock Moon Dashboard Python Deployment Script
# Supports multiple Python deployment platforms

set -e

echo "🌙 Stock Moon Dashboard Python Deployment"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    # Check Python
    if command -v python3 &> /dev/null; then
        print_success "Python3 found"
    elif command -v python &> /dev/null; then
        print_success "Python found"
    else
        print_error "Python not found. Please install Python first."
        exit 1
    fi
    
    # Check pip
    if command -v pip3 &> /dev/null; then
        print_success "pip3 found"
    elif command -v pip &> /dev/null; then
        print_success "pip found"
    else
        print_error "pip not found. Please install pip first."
        exit 1
    fi
    
    # Check if port 8050 is available
    if lsof -Pi :8050 -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Port 8050 is already in use"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Local Python deployment
deploy_local() {
    print_info "Setting up local Python environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d ".venv" ]; then
        print_info "Creating virtual environment..."
        python3 -m venv .venv
    fi
    
    print_info "Activating virtual environment..."
    source .venv/bin/activate
    
    print_info "Installing dependencies..."
    pip install -r requirements.txt
    
    print_info "Starting Stock Moon Dashboard..."
    python app.py
}

# Deploy to cloud platforms
deploy_cloud() {
    echo
    print_info "Cloud Deployment Options:"
    echo "1. Railway (Recommended)"
    echo "2. Render.com"
    echo "3. Heroku"
    echo "4. DigitalOcean App Platform"
    echo "5. Vercel"
    echo
    
    read -p "Select platform (1-5): " platform
    
    case $platform in
        1)
            print_info "Railway Deployment:"
            echo "1. Install Railway CLI: npm install -g @railway/cli"
            echo "2. Login: railway login"
            echo "3. Deploy: railway up"
            echo "4. Railway will auto-detect Python and use:"
            echo "   - Build: pip install -r requirements.txt"
            echo "   - Start: python app.py"
            ;;
        2)
            print_info "Render.com Deployment:"
            echo "1. Connect your GitHub repository to Render"
            echo "2. Create a new Web Service"
            echo "3. Build Command: pip install -r requirements.txt"
            echo "4. Start Command: python app.py"
            echo "5. Set environment variables in Render dashboard"
            ;;
        3)
            print_info "Heroku Deployment:"
            echo "1. Create Procfile: echo 'web: python app.py' > Procfile"
            echo "2. Install Heroku CLI"
            echo "3. heroku create your-app-name"
            echo "4. git push heroku main"
            ;;
        4)
            print_info "DigitalOcean App Platform:"
            echo "1. Connect your GitHub repository"
            echo "2. Select Python deployment"
            echo "3. Build Command: pip install -r requirements.txt"
            echo "4. Run Command: python app.py"
            ;;
        5)
            print_info "Vercel Deployment:"
            echo "1. Install Vercel CLI: npm install -g vercel"
            echo "2. vercel --prod"
            echo "3. Configure for Python runtime"
            ;;
        *)
            print_error "Invalid selection"
            ;;
    esac
}

# Production setup
setup_production() {
    print_info "Setting up production environment..."
    
    # Create Procfile for Heroku
    echo "web: python app.py" > Procfile
    print_success "Created Procfile"
    
    # Create runtime.txt for Python version
    python3 --version | sed 's/Python /python-/' > runtime.txt
    print_success "Created runtime.txt"
    
    # Set production environment variables
    export DASH_DEBUG=False
    export DASH_HOST=0.0.0.0
    export PORT=8050
    
    print_success "Production environment configured"
}

# Main menu
show_menu() {
    echo
    print_info "Select deployment option:"
    echo "1. Local Development"
    echo "2. Cloud Deployment"
    echo "3. Production Setup"
    echo "4. Exit"
    echo
}

# Main execution
main() {
    check_prerequisites
    
    while true; do
        show_menu
        read -p "Enter your choice (1-4): " choice
        
        case $choice in
            1)
                deploy_local
                break
                ;;
            2)
                deploy_cloud
                break
                ;;
            3)
                setup_production
                break
                ;;
            4)
                print_info "Goodbye!"
                exit 0
                ;;
            *)
                print_error "Invalid option. Please try again."
                ;;
        esac
    done
}

# Run main function
main "$@"