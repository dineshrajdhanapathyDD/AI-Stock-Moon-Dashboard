#!/usr/bin/env python3
"""
Build script for AWS Amplify deployment.
Validates the application and prepares it for production deployment.
"""

import sys
import os
import subprocess
import json
from datetime import datetime

def log_message(message, level="INFO"):
    """Log a message with timestamp and level."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def run_command(command, description):
    """Run a command and handle errors."""
    log_message(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        log_message(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        log_message(f"❌ {description} failed: {e.stderr}", "ERROR")
        sys.exit(1)

def validate_python_version():
    """Validate Python version compatibility."""
    log_message("Validating Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        log_message("❌ Python 3.8+ required", "ERROR")
        sys.exit(1)
    log_message(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")

def validate_dependencies():
    """Validate all required dependencies are installed."""
    log_message("Validating dependencies...")
    
    required_packages = [
        'dash', 'plotly', 'pandas', 'numpy', 'scipy', 
        'requests', 'dash-bootstrap-components'
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            log_message(f"✅ {package} is available")
        except ImportError:
            log_message(f"❌ {package} is not installed", "ERROR")
            sys.exit(1)

def test_mcp_tools():
    """Test MCP tools functionality."""
    log_message("Testing MCP tools...")
    
    # Test MCP server list command
    run_command("python mcp_server.py list", "MCP tools listing")
    
    # Test stock database
    run_command("python -c \"from src.stock_database import stock_db; print(f'Stock database: {len(stock_db.stocks)} stocks')\"", 
                "Stock database validation")

def test_dashboard_components():
    """Test dashboard component imports."""
    log_message("Testing dashboard components...")
    
    components = [
        ("src.dashboard", "Dashboard application"),
        ("src.mcp_tools", "MCP tools"),
        ("src.data_models", "Data models"),
        ("src.statistical_analyzer", "Statistical analyzer"),
        ("src.visualizations", "Visualization engine"),
        ("src.cache_manager", "Cache manager")
    ]
    
    for module, description in components:
        run_command(f"python -c \"import {module}; print('{description} imported successfully')\"",
                   f"{description} import test")

def run_system_tests():
    """Run comprehensive system tests."""
    log_message("Running system tests...")
    
    # Run stock search tests
    if os.path.exists("test_stock_search.py"):
        run_command("python test_stock_search.py", "Stock search functionality test")
    
    # Run autocomplete tests
    if os.path.exists("test_autocomplete.py"):
        run_command("python test_autocomplete.py", "Autocomplete functionality test")
    
    # Run complete system test
    if os.path.exists("test_complete_system.py"):
        run_command("python test_complete_system.py", "Complete system integration test")

def create_build_info():
    """Create build information file."""
    log_message("Creating build information...")
    
    build_info = {
        "build_time": datetime.now().isoformat(),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "platform": sys.platform,
        "build_status": "success",
        "components_tested": [
            "MCP tools",
            "Stock database", 
            "Dashboard components",
            "Statistical analysis",
            "Visualization engine",
            "Cache manager"
        ]
    }
    
    with open("build_info.json", "w") as f:
        json.dump(build_info, f, indent=2)
    
    log_message("✅ Build information created")

def optimize_for_production():
    """Apply production optimizations."""
    log_message("Applying production optimizations...")
    
    # Create optimized startup script
    startup_script = """#!/bin/bash
# Production startup script for Stock Moon Dashboard

export PYTHONPATH=/opt/python:$PYTHONPATH
export DASH_DEBUG=False
export DASH_HOST=0.0.0.0
export DASH_PORT=${PORT:-8050}
export DASH_COMPRESS=True
export DASH_SERVE_LOCALLY=False

echo "Starting Stock Moon Dashboard in production mode..."
echo "Dashboard will be available at: http://$DASH_HOST:$DASH_PORT"
echo "Loading optimized components..."

python app.py
"""
    
    with open("start_production.sh", "w") as f:
        f.write(startup_script)
    
    os.chmod("start_production.sh", 0o755)
    log_message("✅ Production startup script created")

def main():
    """Main build process."""
    log_message("🚀 Starting Stock Moon Dashboard build process")
    log_message("=" * 60)
    
    try:
        # Validation phase
        validate_python_version()
        validate_dependencies()
        
        # Testing phase
        test_mcp_tools()
        test_dashboard_components()
        run_system_tests()
        
        # Optimization phase
        optimize_for_production()
        create_build_info()
        
        log_message("=" * 60)
        log_message("🎉 Build completed successfully!")
        log_message("✅ All tests passed")
        log_message("✅ Production optimizations applied")
        log_message("✅ Ready for deployment")
        
    except Exception as e:
        log_message(f"❌ Build failed: {str(e)}", "ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main()