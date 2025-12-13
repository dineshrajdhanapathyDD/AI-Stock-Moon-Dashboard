"""
Stock database for auto-suggestions and search functionality.
Contains popular stocks from US and Indian markets.
"""

from typing import List, Dict, Tuple
import re

class StockDatabase:
    """Database of popular stocks with search functionality."""
    
    def __init__(self):
        self.stocks = self._initialize_stock_database()
        self.search_index = self._build_search_index()
    
    def _initialize_stock_database(self) -> List[Dict[str, str]]:
        """Initialize the stock database with popular stocks."""
        return [
            # US Tech Giants
            {"symbol": "AAPL", "name": "Apple Inc.", "sector": "Technology", "market": "US"},
            {"symbol": "GOOGL", "name": "Alphabet Inc. (Google)", "sector": "Technology", "market": "US"},
            {"symbol": "MSFT", "name": "Microsoft Corporation", "sector": "Technology", "market": "US"},
            {"symbol": "AMZN", "name": "Amazon.com Inc.", "sector": "Consumer Discretionary", "market": "US"},
            {"symbol": "META", "name": "Meta Platforms Inc. (Facebook)", "sector": "Technology", "market": "US"},
            {"symbol": "TSLA", "name": "Tesla Inc.", "sector": "Automotive", "market": "US"},
            {"symbol": "NVDA", "name": "NVIDIA Corporation", "sector": "Technology", "market": "US"},
            {"symbol": "NFLX", "name": "Netflix Inc.", "sector": "Entertainment", "market": "US"},
            
            # US Financial
            {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "sector": "Financial", "market": "US"},
            {"symbol": "BAC", "name": "Bank of America Corp.", "sector": "Financial", "market": "US"},
            {"symbol": "WFC", "name": "Wells Fargo & Company", "sector": "Financial", "market": "US"},
            {"symbol": "GS", "name": "Goldman Sachs Group Inc.", "sector": "Financial", "market": "US"},
            
            # US Healthcare & Consumer
            {"symbol": "JNJ", "name": "Johnson & Johnson", "sector": "Healthcare", "market": "US"},
            {"symbol": "PFE", "name": "Pfizer Inc.", "sector": "Healthcare", "market": "US"},
            {"symbol": "KO", "name": "Coca-Cola Company", "sector": "Consumer Staples", "market": "US"},
            {"symbol": "PEP", "name": "PepsiCo Inc.", "sector": "Consumer Staples", "market": "US"},
            {"symbol": "WMT", "name": "Walmart Inc.", "sector": "Consumer Staples", "market": "US"},
            
            # US Industrial & Energy
            {"symbol": "BA", "name": "Boeing Company", "sector": "Industrial", "market": "US"},
            {"symbol": "CAT", "name": "Caterpillar Inc.", "sector": "Industrial", "market": "US"},
            {"symbol": "XOM", "name": "Exxon Mobil Corporation", "sector": "Energy", "market": "US"},
            {"symbol": "CVX", "name": "Chevron Corporation", "sector": "Energy", "market": "US"},
            
            # Cryptocurrency
            {"symbol": "BTC-USD", "name": "Bitcoin USD", "sector": "Cryptocurrency", "market": "Crypto"},
            {"symbol": "ETH-USD", "name": "Ethereum USD", "sector": "Cryptocurrency", "market": "Crypto"},
            
            # Indian Large Cap Stocks
            {"symbol": "RELIANCE.NS", "name": "Reliance Industries Ltd.", "sector": "Energy", "market": "India"},
            {"symbol": "TCS.NS", "name": "Tata Consultancy Services Ltd.", "sector": "Technology", "market": "India"},
            {"symbol": "INFY.NS", "name": "Infosys Ltd.", "sector": "Technology", "market": "India"},
            {"symbol": "HDFCBANK.NS", "name": "HDFC Bank Ltd.", "sector": "Financial", "market": "India"},
            {"symbol": "ICICIBANK.NS", "name": "ICICI Bank Ltd.", "sector": "Financial", "market": "India"},
            {"symbol": "BHARTIARTL.NS", "name": "Bharti Airtel Ltd.", "sector": "Telecom", "market": "India"},
            {"symbol": "ITC.NS", "name": "ITC Ltd.", "sector": "Consumer Goods", "market": "India"},
            {"symbol": "SBIN.NS", "name": "State Bank of India", "sector": "Financial", "market": "India"},
            {"symbol": "LT.NS", "name": "Larsen & Toubro Ltd.", "sector": "Industrial", "market": "India"},
            {"symbol": "WIPRO.NS", "name": "Wipro Ltd.", "sector": "Technology", "market": "India"},
            {"symbol": "MARUTI.NS", "name": "Maruti Suzuki India Ltd.", "sector": "Automotive", "market": "India"},
            {"symbol": "ASIANPAINT.NS", "name": "Asian Paints Ltd.", "sector": "Consumer Goods", "market": "India"},
            {"symbol": "NESTLEIND.NS", "name": "Nestle India Ltd.", "sector": "Consumer Goods", "market": "India"},
            {"symbol": "KOTAKBANK.NS", "name": "Kotak Mahindra Bank Ltd.", "sector": "Financial", "market": "India"},
            {"symbol": "BAJFINANCE.NS", "name": "Bajaj Finance Ltd.", "sector": "Financial", "market": "India"},
            {"symbol": "HINDUNILVR.NS", "name": "Hindustan Unilever Ltd.", "sector": "Consumer Goods", "market": "India"},
            {"symbol": "AXISBANK.NS", "name": "Axis Bank Ltd.", "sector": "Financial", "market": "India"},
            {"symbol": "ULTRACEMCO.NS", "name": "UltraTech Cement Ltd.", "sector": "Materials", "market": "India"},
            {"symbol": "SUNPHARMA.NS", "name": "Sun Pharmaceutical Industries Ltd.", "sector": "Healthcare", "market": "India"},
            {"symbol": "TITAN.NS", "name": "Titan Company Ltd.", "sector": "Consumer Discretionary", "market": "India"},
            
            # Indian Mid Cap
            {"symbol": "TECHM.NS", "name": "Tech Mahindra Ltd.", "sector": "Technology", "market": "India"},
            {"symbol": "HCLTECH.NS", "name": "HCL Technologies Ltd.", "sector": "Technology", "market": "India"},
            {"symbol": "POWERGRID.NS", "name": "Power Grid Corporation of India Ltd.", "sector": "Utilities", "market": "India"},
            {"symbol": "NTPC.NS", "name": "NTPC Ltd.", "sector": "Utilities", "market": "India"},
            {"symbol": "ONGC.NS", "name": "Oil & Natural Gas Corporation Ltd.", "sector": "Energy", "market": "India"},
            {"symbol": "COALINDIA.NS", "name": "Coal India Ltd.", "sector": "Materials", "market": "India"},
            {"symbol": "JSWSTEEL.NS", "name": "JSW Steel Ltd.", "sector": "Materials", "market": "India"},
            {"symbol": "TATASTEEL.NS", "name": "Tata Steel Ltd.", "sector": "Materials", "market": "India"},
            {"symbol": "INDUSINDBK.NS", "name": "IndusInd Bank Ltd.", "sector": "Financial", "market": "India"},
            {"symbol": "ADANIPORTS.NS", "name": "Adani Ports and Special Economic Zone Ltd.", "sector": "Industrial", "market": "India"},
        ]
    
    def _build_search_index(self) -> Dict[str, List[int]]:
        """Build search index for fast lookups."""
        index = {}
        
        for i, stock in enumerate(self.stocks):
            # Index by symbol
            symbol_words = stock["symbol"].lower().split(".")
            for word in symbol_words:
                if word not in index:
                    index[word] = []
                index[word].append(i)
            
            # Index by company name words
            name_words = re.findall(r'\b\w+\b', stock["name"].lower())
            for word in name_words:
                if len(word) > 2:  # Skip short words
                    if word not in index:
                        index[word] = []
                    if i not in index[word]:
                        index[word].append(i)
            
            # Index by sector
            sector_words = stock["sector"].lower().split()
            for word in sector_words:
                if word not in index:
                    index[word] = []
                if i not in index[word]:
                    index[word].append(i)
        
        return index
    
    def search(self, query: str, limit: int = 10) -> List[Dict[str, str]]:
        """
        Search for stocks by symbol, name, or sector.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of matching stock dictionaries
        """
        if not query or len(query.strip()) < 1:
            return []  # Return empty for empty queries
        
        query = query.lower().strip()
        matching_indices = set()
        
        # Direct symbol match (highest priority)
        for stock_idx, stock in enumerate(self.stocks):
            if stock["symbol"].lower().startswith(query):
                matching_indices.add(stock_idx)
        
        # Search in index
        query_words = re.findall(r'\b\w+\b', query)
        for word in query_words:
            # Exact word match
            if word in self.search_index:
                matching_indices.update(self.search_index[word])
            
            # Partial word match
            for indexed_word in self.search_index:
                if indexed_word.startswith(word) and len(word) >= 2:
                    matching_indices.update(self.search_index[indexed_word])
        
        # Get matching stocks and sort by relevance
        results = []
        for idx in matching_indices:
            stock = self.stocks[idx].copy()
            stock["relevance"] = self._calculate_relevance(stock, query)
            results.append(stock)
        
        # Sort by relevance (higher is better)
        results.sort(key=lambda x: x["relevance"], reverse=True)
        
        return results[:limit]
    
    def _calculate_relevance(self, stock: Dict[str, str], query: str) -> float:
        """Calculate relevance score for search results."""
        score = 0.0
        query_lower = query.lower()
        
        # Symbol match (highest weight)
        if stock["symbol"].lower().startswith(query_lower):
            score += 100
        elif query_lower in stock["symbol"].lower():
            score += 50
        
        # Company name match
        name_lower = stock["name"].lower()
        if query_lower in name_lower:
            score += 30
            # Bonus for word boundary matches
            if f" {query_lower}" in f" {name_lower}" or name_lower.startswith(query_lower):
                score += 20
        
        # Sector match
        if query_lower in stock["sector"].lower():
            score += 10
        
        # Market preference (slight boost for popular markets)
        if stock["market"] == "US":
            score += 2
        elif stock["market"] == "India":
            score += 1
        
        return score
    
    def get_popular_stocks(self, limit: int = 10) -> List[Dict[str, str]]:
        """Get most popular stocks for default suggestions."""
        popular_symbols = [
            "AAPL", "GOOGL", "MSFT", "TSLA", "AMZN",
            "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"
        ]
        
        results = []
        for symbol in popular_symbols[:limit]:
            for stock in self.stocks:
                if stock["symbol"] == symbol:
                    results.append(stock)
                    break
        
        return results
    
    def get_by_symbol(self, symbol: str) -> Dict[str, str]:
        """Get stock info by exact symbol match."""
        symbol_upper = symbol.upper()
        for stock in self.stocks:
            if stock["symbol"].upper() == symbol_upper:
                return stock
        return None
    
    def get_markets(self) -> List[str]:
        """Get list of available markets."""
        markets = set(stock["market"] for stock in self.stocks)
        return sorted(list(markets))
    
    def get_sectors(self) -> List[str]:
        """Get list of available sectors."""
        sectors = set(stock["sector"] for stock in self.stocks)
        return sorted(list(sectors))
    
    def filter_by_market(self, market: str) -> List[Dict[str, str]]:
        """Filter stocks by market."""
        return [stock for stock in self.stocks if stock["market"] == market]
    
    def filter_by_sector(self, sector: str) -> List[Dict[str, str]]:
        """Filter stocks by sector."""
        return [stock for stock in self.stocks if stock["sector"] == sector]


# Global instance
stock_db = StockDatabase()