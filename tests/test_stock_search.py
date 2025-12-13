#!/usr/bin/env python3
"""
Test script for stock database search functionality.
"""

from src.stock_database import stock_db

def test_stock_search():
    """Test the stock search functionality."""
    print("Testing Stock Database Search Functionality")
    print("=" * 50)
    
    # Test various search queries
    test_queries = [
        "apple",
        "goog", 
        "reliance",
        "tcs",
        "bank",
        "tech",
        "AAPL",
        "microsoft",
        "infosys"
    ]
    
    for query in test_queries:
        results = stock_db.search(query, limit=3)
        print(f"\n[SEARCH] Query: '{query}'")
        if results:
            for stock in results:
                print(f"   [UP] {stock['symbol']} - {stock['name']} ({stock['market']})")
        else:
            print("   [ERROR] No results found")
    
    # Test popular stocks
    print("\n[STAR] Popular Stocks:")
    popular = stock_db.get_popular_stocks(8)
    for stock in popular:
        print(f"   [CHART] {stock['symbol']} - {stock['name']} ({stock['market']})")
    
    # Test market filtering
    print("\n[INDIA] Indian Stocks:")
    indian_stocks = stock_db.filter_by_market("India")[:5]
    for stock in indian_stocks:
        print(f"   [BUILDING] {stock['symbol']} - {stock['name']}")
    
    # Test sector filtering
    print("\n[TECH] Technology Stocks:")
    tech_stocks = stock_db.filter_by_sector("Technology")[:5]
    for stock in tech_stocks:
        print(f"   [COMPUTER]  {stock['symbol']} - {stock['name']} ({stock['market']})")
    
    print(f"\n[OK] Stock database contains {len(stock_db.stocks)} stocks")
    print(f"[CHART] Markets: {', '.join(stock_db.get_markets())}")
    print(f"[FACTORY] Sectors: {len(stock_db.get_sectors())} different sectors")

if __name__ == "__main__":
    test_stock_search()