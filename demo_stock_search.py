#!/usr/bin/env python3
"""
Demo script showcasing the new stock search and autocomplete functionality
in the Stock Moon Dashboard.
"""

from src.stock_database import stock_db
import time

def print_banner(text):
    """Print a formatted banner."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def demo_search_functionality():
    """Demonstrate the search functionality."""
    print_banner("🔍 STOCK SEARCH & AUTOCOMPLETE DEMO")
    
    print("\n🎯 The Stock Moon Dashboard now includes intelligent stock search!")
    print("   Users can search by company name, symbol, or sector.")
    
    # Demo different search types
    search_demos = [
        ("Symbol Search", "AAPL", "Search by exact symbol"),
        ("Company Name", "apple", "Search by company name"),
        ("Partial Match", "goog", "Partial symbol matching"),
        ("Indian Stocks", "reliance", "Indian market support"),
        ("Sector Search", "bank", "Search by business sector"),
        ("Technology", "tech", "Technology companies"),
    ]
    
    for demo_type, query, description in search_demos:
        print(f"\n📊 {demo_type}: '{query}' ({description})")
        results = stock_db.search(query, limit=3)
        
        if results:
            for i, stock in enumerate(results, 1):
                market_emoji = "🇺🇸" if stock["market"] == "US" else "🇮🇳" if stock["market"] == "India" else "💰"
                print(f"   {i}. {market_emoji} {stock['symbol']} - {stock['name']}")
                print(f"      📈 {stock['sector']} | {stock['market']} Market")
        else:
            print("   ❌ No results found")
        
        time.sleep(0.5)  # Small delay for readability

def demo_market_coverage():
    """Demonstrate market coverage."""
    print_banner("🌍 GLOBAL MARKET COVERAGE")
    
    markets = stock_db.get_markets()
    print(f"\n📊 Supported Markets: {', '.join(markets)}")
    
    for market in markets:
        stocks = stock_db.filter_by_market(market)
        market_emoji = "🇺🇸" if market == "US" else "🇮🇳" if market == "India" else "💰"
        print(f"\n{market_emoji} {market} Market ({len(stocks)} stocks):")
        
        # Show top 5 stocks from each market
        for stock in stocks[:5]:
            print(f"   • {stock['symbol']} - {stock['name']}")

def demo_sector_analysis():
    """Demonstrate sector-based filtering."""
    print_banner("🏭 SECTOR-BASED ANALYSIS")
    
    sectors = stock_db.get_sectors()
    print(f"\n📊 Available Sectors: {len(sectors)} different industries")
    
    # Show popular sectors
    popular_sectors = ["Technology", "Financial", "Healthcare", "Energy", "Consumer Goods"]
    
    for sector in popular_sectors:
        if sector in sectors:
            stocks = stock_db.filter_by_sector(sector)
            sector_emoji = {"Technology": "💻", "Financial": "🏦", "Healthcare": "🏥", 
                          "Energy": "⚡", "Consumer Goods": "🛍️"}.get(sector, "🏭")
            
            print(f"\n{sector_emoji} {sector} Sector ({len(stocks)} stocks):")
            for stock in stocks[:4]:
                market_flag = "🇺🇸" if stock["market"] == "US" else "🇮🇳"
                print(f"   • {market_flag} {stock['symbol']} - {stock['name']}")

def demo_dashboard_features():
    """Demonstrate dashboard integration."""
    print_banner("📱 DASHBOARD INTEGRATION FEATURES")
    
    print("\n🎯 New Dashboard Features:")
    print("   ✅ Real-time autocomplete as you type")
    print("   ✅ Smart search by company name or symbol")
    print("   ✅ Market and sector filtering")
    print("   ✅ Quick-select buttons for popular stocks")
    print("   ✅ Visual indicators for different markets")
    print("   ✅ Comprehensive stock database (53+ stocks)")
    
    print("\n🚀 How to Use:")
    print("   1. Start typing in the stock symbol field")
    print("   2. See instant suggestions with company names")
    print("   3. Click on any suggestion to select it")
    print("   4. Use quick-select buttons for popular stocks")
    print("   5. Search works for both US and Indian markets")
    
    print("\n💡 Search Examples:")
    examples = [
        "Type 'apple' → See AAPL - Apple Inc.",
        "Type 'bank' → See all banking stocks",
        "Type 'TCS' → Find Tata Consultancy Services",
        "Type 'tech' → See technology companies",
        "Type 'RELIANCE' → Find Indian conglomerate"
    ]
    
    for example in examples:
        print(f"   • {example}")

def demo_popular_stocks():
    """Show popular stock recommendations."""
    print_banner("⭐ POPULAR STOCK RECOMMENDATIONS")
    
    popular = stock_db.get_popular_stocks(10)
    
    print("\n🔥 Most Popular Stocks for Analysis:")
    print("   (Pre-loaded in quick-select buttons)")
    
    us_stocks = [s for s in popular if s["market"] == "US"]
    indian_stocks = [s for s in popular if s["market"] == "India"]
    
    print("\n🇺🇸 US Market Leaders:")
    for stock in us_stocks:
        print(f"   📈 {stock['symbol']} - {stock['name']}")
        print(f"      💼 {stock['sector']}")
    
    print("\n🇮🇳 Indian Market Leaders:")
    for stock in indian_stocks:
        print(f"   📈 {stock['symbol']} - {stock['name']}")
        print(f"      💼 {stock['sector']}")

def main():
    """Run the complete demo."""
    print("🌙 Stock Moon Dashboard - Enhanced Stock Search Demo")
    print("   Intelligent autocomplete and search functionality")
    
    demo_search_functionality()
    demo_market_coverage()
    demo_sector_analysis()
    demo_popular_stocks()
    demo_dashboard_features()
    
    print_banner("🎉 DEMO COMPLETE")
    print("\n✨ The Stock Moon Dashboard now offers:")
    print("   🔍 Intelligent stock search and autocomplete")
    print("   🌍 Global market support (US + India)")
    print("   📊 53+ popular stocks across 14 sectors")
    print("   🚀 Enhanced user experience")
    
    print(f"\n🌐 Start the dashboard: python app.py")
    print(f"📱 Access at: http://localhost:8050")
    print(f"💡 Try searching for: Apple, Google, Reliance, TCS, Bank, Tech")

if __name__ == "__main__":
    main()