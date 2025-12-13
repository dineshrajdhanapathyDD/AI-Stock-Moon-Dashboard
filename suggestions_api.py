#!/usr/bin/env python3
"""
Dynamic Stock Suggestions API
Provides real-time stock suggestions and search functionality.
"""

import sys
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from stock_database import stock_db

app = Flask(__name__)
CORS(app)

@app.route('/api/suggestions')
def get_suggestions():
    """Get stock suggestions based on query."""
    query = request.args.get('q', '').lower()
    limit = int(request.args.get('limit', 10))
    
    if not query:
        # Return popular stocks
        popular = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'RELIANCE.NS', 'TCS.NS']
        return jsonify([
            {
                'symbol': symbol,
                'name': stock_db.get_stock_info(symbol)['name'],
                'market': stock_db.get_stock_info(symbol)['market'],
                'sector': stock_db.get_stock_info(symbol)['sector']
            }
            for symbol in popular if symbol in [s['symbol'] for s in stock_db.stocks]
        ][:limit])
    
    # Search stocks
    results = stock_db.search_stocks(query)
    return jsonify([
        {
            'symbol': stock['symbol'],
            'name': stock['name'],
            'market': stock['market'],
            'sector': stock['sector'],
            'relevance': stock.get('relevance', 0)
        }
        for stock in results[:limit]
    ])

@app.route('/api/stock/<symbol>')
def get_stock_info(symbol):
    """Get detailed stock information."""
    try:
        info = stock_db.get_stock_info(symbol)
        return jsonify(info)
    except:
        return jsonify({'error': 'Stock not found'}), 404

@app.route('/api/markets')
def get_markets():
    """Get available markets."""
    markets = {}
    for stock in stock_db.stocks:
        market = stock['market']
        if market not in markets:
            markets[market] = []
        markets[market].append(stock['symbol'])
    
    return jsonify(markets)

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'stocks_loaded': len(stock_db.stocks),
        'markets': len(set(s['market'] for s in stock_db.stocks))
    })

if __name__ == '__main__':
    print("🚀 Starting Stock Suggestions API...")
    print(f"📊 Loaded {len(stock_db.stocks)} stocks")
    app.run(host='0.0.0.0', port=5000, debug=False)