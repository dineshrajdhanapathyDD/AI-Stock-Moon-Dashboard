"""
Dynamic Stock Suggestions API
Provides intelligent stock recommendations based on user input.
"""

import re
from typing import List, Dict, Any
from .stock_database import stock_db

class StockSuggestionEngine:
    """Intelligent stock suggestion engine with fuzzy matching."""
    
    def __init__(self):
        self.stocks = stock_db.stocks
        self._build_search_index()
    
    def _build_search_index(self):
        """Build search index for fast lookups."""
        self.search_index = {}
        
        for stock in self.stocks:
            # Index by symbol
            symbol_key = stock['symbol'].lower()
            self.search_index[symbol_key] = stock
            
            # Index by company name words
            name_words = re.findall(r'\w+', stock['name'].lower())
            for word in name_words:
                if word not in self.search_index:
                    self.search_index[word] = []
                if isinstance(self.search_index[word], list):
                    self.search_index[word].append(stock)
                else:
                    self.search_index[word] = [self.search_index[word], stock]
            
            # Index by sector
            sector_key = stock['sector'].lower()
            if sector_key not in self.search_index:
                self.search_index[sector_key] = []
            if isinstance(self.search_index[sector_key], list):
                self.search_index[sector_key].append(stock)
            else:
                self.search_index[sector_key] = [self.search_index[sector_key], stock]
    
    def get_suggestions(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get intelligent stock suggestions based on query."""
        if not query or len(query.strip()) < 1:
            return self._get_popular_stocks(limit)
        
        query = query.lower().strip()
        suggestions = []
        seen_symbols = set()
        
        # 1. Exact symbol match (highest priority)
        if query in self.search_index and isinstance(self.search_index[query], dict):
            stock = self.search_index[query]
            suggestions.append(self._format_suggestion(stock, 'exact_symbol', 1.0))
            seen_symbols.add(stock['symbol'])
        
        # 2. Symbol prefix match
        for key, stock in self.search_index.items():
            if (isinstance(stock, dict) and 
                key.startswith(query) and 
                stock['symbol'] not in seen_symbols):
                score = len(query) / len(key)
                suggestions.append(self._format_suggestion(stock, 'symbol_prefix', score))
                seen_symbols.add(stock['symbol'])
        
        # 3. Company name word match
        query_words = query.split()
        for word in query_words:
            if word in self.search_index:
                stocks = self.search_index[word]
                if isinstance(stocks, dict):
                    stocks = [stocks]
                
                for stock in stocks:
                    if stock['symbol'] not in seen_symbols:
                        score = self._calculate_name_score(query, stock['name'])
                        suggestions.append(self._format_suggestion(stock, 'name_match', score))
                        seen_symbols.add(stock['symbol'])
        
        # 4. Fuzzy name matching
        for stock in self.stocks:
            if stock['symbol'] not in seen_symbols:
                score = self._fuzzy_match_score(query, stock['name'].lower())
                if score > 0.3:  # Threshold for fuzzy matching
                    suggestions.append(self._format_suggestion(stock, 'fuzzy_match', score))
                    seen_symbols.add(stock['symbol'])
        
        # 5. Sector matching
        if query in self.search_index:
            stocks = self.search_index[query]
            if isinstance(stocks, list):
                for stock in stocks[:3]:  # Limit sector matches
                    if stock['symbol'] not in seen_symbols:
                        suggestions.append(self._format_suggestion(stock, 'sector_match', 0.7))
                        seen_symbols.add(stock['symbol'])
        
        # Sort by relevance score and return top results
        suggestions.sort(key=lambda x: x['relevance_score'], reverse=True)
        return suggestions[:limit]
    
    def _format_suggestion(self, stock: Dict, match_type: str, score: float) -> Dict[str, Any]:
        """Format stock suggestion with metadata."""
        return {
            'symbol': stock['symbol'],
            'name': stock['name'],
            'sector': stock['sector'],
            'market': stock['market'],
            'country': stock['country'],
            'match_type': match_type,
            'relevance_score': score,
            'display_text': f"{stock['symbol']} - {stock['name']}",
            'flag': stock.get('flag', '🏢'),
            'sector_tag': stock['sector'][:4].upper()
        }
    
    def _calculate_name_score(self, query: str, name: str) -> float:
        """Calculate relevance score for name matching."""
        query_lower = query.lower()
        name_lower = name.lower()
        
        # Exact match
        if query_lower == name_lower:
            return 1.0
        
        # Starts with query
        if name_lower.startswith(query_lower):
            return 0.9
        
        # Contains query
        if query_lower in name_lower:
            return 0.7
        
        # Word boundary match
        words = name_lower.split()
        for word in words:
            if word.startswith(query_lower):
                return 0.6
        
        return 0.0
    
    def _fuzzy_match_score(self, query: str, text: str) -> float:
        """Calculate fuzzy matching score using simple algorithm."""
        if not query or not text:
            return 0.0
        
        # Simple character-based fuzzy matching
        query_chars = set(query.lower())
        text_chars = set(text.lower())
        
        intersection = len(query_chars.intersection(text_chars))
        union = len(query_chars.union(text_chars))
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def _get_popular_stocks(self, limit: int) -> List[Dict[str, Any]]:
        """Get popular stocks when no query is provided."""
        popular_symbols = [
            'AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'META',
            'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS'
        ]
        
        suggestions = []
        for symbol in popular_symbols[:limit]:
            stock = next((s for s in self.stocks if s['symbol'] == symbol), None)
            if stock:
                suggestions.append(self._format_suggestion(stock, 'popular', 0.8))
        
        return suggestions

# Global suggestion engine instance
suggestion_engine = StockSuggestionEngine()