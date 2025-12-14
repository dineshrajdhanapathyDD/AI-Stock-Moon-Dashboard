#!/usr/bin/env python3
"""
Dynamic Stock Suggestions API
Provides intelligent stock suggestions based on user input.
"""

import re
from typing import List, Dict, Any
from src.stock_database import stock_db

class StockSuggestionsAPI:
    """Enhanced stock suggestions with dynamic filtering."""
    
    def __init__(self):
        self.stocks = stock_db.stocks
        self.sectors = self._build_sector_index()
        
    def _build_sector_index(self) -> Dict[str, List[str]]:
        """Build sector-based index for faster searching."""
        sectors = {}
        for stock in self.stocks:
            sector = stock.get('sector', 'Other')
            if sector not in sectors:
                sectors[sector] = []
            sectors[sector].append(stock['symbol'])
        return sectors
    
    def get_suggestions(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get dynamic stock suggestions based on query.
        
        Args:
            query: Search query (company name, symbol, or sector)
            limit: Maximum number of suggestions
            
        Returns:
            List of stock suggestions with relevance scores
        """
        if not query or len(query.strip()) < 1:
            return self._get_popular_stocks(limit)
        
        query = query.strip().lower()
        suggestions = []
        
        # Search by symbol (highest priority)
        symbol_matches = self._search_by_symbol(query)
        suggestions.extend(symbol_matches)
        
        # Search by company name
        name_matches = self._search_by_name(query)
        suggestions.extend(name_matches)
        
        # Search by sector
        sector_matches = self._search_by_sector(query)
        suggestions.extend(sector_matches)
        
        # Remove duplicates and sort by relevance
        seen = set()
        unique_suggestions = []
        for suggestion in suggestions:
            if suggestion['symbol'] not in seen:
                seen.add(suggestion['symbol'])
                unique_suggestions.append(suggestion)
        
        # Sort by relevance score (descending)
        unique_suggestions.sort(key=lambda x: x['relevance'], reverse=True)
        
        return unique_suggestions[:limit]
    
    def _search_by_symbol(self, query: str) -> List[Dict[str, Any]]:
        """Search stocks by symbol."""
        matches = []
        for stock in self.stocks:
            symbol = stock['symbol'].lower()
            if symbol.startswith(query):
                relevance = 100 - len(symbol)  # Shorter symbols get higher score
                matches.append({
                    'symbol': stock['symbol'],
                    'name': stock['name'],
                    'sector': stock.get('sector', 'Other'),
                    'market': stock.get('market', 'US'),
                    'relevance': relevance,
                    'match_type': 'symbol'
                })
        return matches
    
    def _search_by_name(self, query: str) -> List[Dict[str, Any]]:
        """Search stocks by company name."""
        matches = []
        for stock in self.stocks:
            name = stock['name'].lower()
            if query in name:
                # Calculate relevance based on position and length
                position = name.find(query)
                relevance = 80 - position - (len(name) - len(query)) * 0.1
                matches.append({
                    'symbol': stock['symbol'],
                    'name': stock['name'],
                    'sector': stock.get('sector', 'Other'),
                    'market': stock.get('market', 'US'),
                    'relevance': max(relevance, 10),
                    'match_type': 'name'
                })
        return matches
    
    def _search_by_sector(self, query: str) -> List[Dict[str, Any]]:
        """Search stocks by sector."""
        matches = []
        for stock in self.stocks:
            sector = stock.get('sector', '').lower()
            if query in sector:
                relevance = 60 - len(sector)  # Shorter sector names get higher score
                matches.append({
                    'symbol': stock['symbol'],
                    'name': stock['name'],
                    'sector': stock.get('sector', 'Other'),
                    'market': stock.get('market', 'US'),
                    'relevance': max(relevance, 5),
                    'match_type': 'sector'
                })
        return matches
    
    def _get_popular_stocks(self, limit: int) -> List[Dict[str, Any]]:
        """Get popular stocks when no query is provided."""
        popular = [
            'AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN',
            'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS'
        ]
        
        suggestions = []
        for symbol in popular[:limit]:
            stock = next((s for s in self.stocks if s['symbol'] == symbol), None)
            if stock:
                suggestions.append({
                    'symbol': stock['symbol'],
                    'name': stock['name'],
                    'sector': stock.get('sector', 'Other'),
                    'market': stock.get('market', 'US'),
                    'relevance': 90,
                    'match_type': 'popular'
                })
        
        return suggestions
    
    def get_sectors(self) -> List[str]:
        """Get all available sectors."""
        return list(self.sectors.keys())
    
    def get_stocks_by_sector(self, sector: str) -> List[Dict[str, Any]]:
        """Get all stocks in a specific sector."""
        sector_stocks = []
        for stock in self.stocks:
            if stock.get('sector', '').lower() == sector.lower():
                sector_stocks.append({
                    'symbol': stock['symbol'],
                    'name': stock['name'],
                    'sector': stock['sector'],
                    'market': stock.get('market', 'US')
                })
        return sector_stocks

# Global instance
suggestions_api = StockSuggestionsAPI()