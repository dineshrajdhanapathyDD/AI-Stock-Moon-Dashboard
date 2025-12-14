#!/usr/bin/env python3
"""
Data Weaver AI - Stock Moon Dashboard
Main application entry point with production and development configurations.
"""

import sys
import os
import logging
from datetime import datetime
from flask import request

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_config():
    """Get configuration based on environment."""
    config = {
        'host': os.getenv('DASH_HOST', '0.0.0.0'),
        'port': int(os.getenv('PORT', os.getenv('DASH_PORT', 8050))),
        'debug': os.getenv('DASH_DEBUG', 'True').lower() == 'true',
        'compress': os.getenv('DASH_COMPRESS', 'True').lower() == 'true',
        'serve_locally': os.getenv('DASH_SERVE_LOCALLY', 'True').lower() == 'true'
    }
    
    # Production optimizations
    if not config['debug']:
        config.update({
            'dev_tools_hot_reload': False,
            'dev_tools_ui': False,
            'dev_tools_props_check': False,
            'serve_locally': False
        })
    
    return config

def log_startup_info(config):
    """Log startup information."""
    mode = "PRODUCTION" if not config['debug'] else "DEVELOPMENT"
    
    print("🌙 Data Weaver AI - Stock Moon Dashboard")
    print("=" * 50)
    print(f"🚀 Mode: {mode}")
    print(f"📊 Dashboard URL: http://{config['host']}:{config['port']}")
    print(f"🔄 Loading components...")
    print(f"⚡ Compression: {'Enabled' if config.get('compress') else 'Disabled'}")
    print(f"📱 Serve Locally: {'Yes' if config.get('serve_locally') else 'No (CDN)'}")
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

def add_security_headers(app):
    """Add security headers for production."""
    @app.server.after_request
    def security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Only add HSTS in production with HTTPS
        if not os.getenv('DASH_DEBUG', 'True').lower() == 'true':
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response
    
    return app

def add_health_check(app):
    """Add health check endpoint."""
    @app.server.route('/health')
    def health_check():
        return {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'service': 'stock-moon-dashboard'
        }
    
    @app.server.route('/ready')
    def readiness_check():
        try:
            # Quick validation that core components are working
            from src.stock_database import stock_db
            stock_count = len(stock_db.stocks)
            
            return {
                'status': 'ready',
                'timestamp': datetime.now().isoformat(),
                'stocks_loaded': stock_count,
                'components': ['dashboard', 'mcp_tools', 'statistical_analyzer', 'suggestions_api']
            }
        except Exception as e:
            return {'status': 'not_ready', 'error': str(e)}, 503
    
    @app.server.route('/api/suggestions')
    def stock_suggestions():
        query = request.args.get('q', '')
        limit = int(request.args.get('limit', 10))
        
        try:
            from src.suggestions_api import suggestions_api
            suggestions = suggestions_api.get_suggestions(query, limit)
            return {'suggestions': suggestions}
        except Exception as e:
            return {'error': str(e)}, 500
    
    return app

def main():
    """Main application entry point."""
    try:
        # Import dashboard after path setup
        from src.dashboard import app
        from src.suggestions_api import suggestions_api
        
        # Get configuration
        config = get_config()
        
        # Log startup information
        log_startup_info(config)
        
        # Add production enhancements
        if not config['debug']:
            app = add_security_headers(app)
            logger.info("✅ Security headers configured")
        
        # Add health check endpoints
        app = add_health_check(app)
        logger.info("✅ Health check endpoints configured")
        
        # Log component status
        logger.info("🔄 Validating components...")
        
        try:
            from src.stock_database import stock_db
            logger.info(f"✅ Stock database loaded: {len(stock_db.stocks)} stocks")
        except Exception as e:
            logger.error(f"❌ Stock database error: {e}")
            
        try:
            from src.mcp_tools import StockDataFetcher, MoonDataFetcher
            logger.info("✅ MCP tools loaded successfully")
        except Exception as e:
            logger.error(f"❌ MCP tools error: {e}")
        
        logger.info("🚀 Starting dashboard server...")
        
        # Run the application
        app.run(
            host=config['host'],
            port=config['port'],
            debug=config['debug'],
            **{k: v for k, v in config.items() 
               if k not in ['host', 'port', 'debug', 'compress', 'serve_locally']}
        )
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.error("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()