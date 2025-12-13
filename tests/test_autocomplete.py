#!/usr/bin/env python3
"""
Test script to verify the autocomplete functionality works correctly.
"""

from src.stock_database import stock_db

def test_autocomplete_functionality():
    """Test the core autocomplete functionality."""
    print("[SEARCH] Testing Autocomplete Functionality")
    print("=" * 40)
    
    # Test cases that should work
    test_cases = [
        ("apple", "Should find AAPL"),
        ("AAPL", "Should find Apple Inc."),
        ("goog", "Should find Google"),
        ("reliance", "Should find Reliance Industries"),
        ("bank", "Should find banking stocks"),
        ("tech", "Should find technology stocks"),
        ("", "Should return empty for empty query"),
        ("xyz123", "Should return empty for invalid query")
    ]
    
    for query, expected in test_cases:
        print(f"\n[SEARCH] Testing: '{query}' ({expected})")
        
        try:
            results = stock_db.search(query, limit=5)
            
            if query == "" or query == "xyz123":
                if not results:
                    print("   [OK] Correctly returned empty results")
                else:
                    print(f"   [ERROR] Expected empty, got {len(results)} results")
            else:
                if results:
                    print(f"   [OK] Found {len(results)} results:")
                    for i, stock in enumerate(results[:3], 1):
                        print(f"      {i}. {stock['symbol']} - {stock['name']}")
                else:
                    print("   [ERROR] No results found")
                    
        except Exception as e:
            print(f"   [ERROR] Error: {e}")
    
    # Test callback simulation
    print(f"\n[PHONE] Testing Callback Logic Simulation")
    print("-" * 30)
    
    # Simulate the callback function logic
    def simulate_callback(search_query):
        """Simulate the dashboard callback."""
        try:
            if not search_query or len(search_query.strip()) < 1:
                return "Empty div", {"display": "none"}
            
            suggestions = stock_db.search(search_query, limit=8)
            
            if not suggestions:
                return "Empty div", {"display": "none"}
            
            # Simulate creating suggestion items
            suggestion_count = len(suggestions)
            
            return f"ListGroup with {suggestion_count} items", {
                "display": "block",
                "zIndex": 1000,
                "backgroundColor": "white"
            }
        except Exception as e:
            return "Empty div", {"display": "none"}
    
    # Test callback simulation
    callback_tests = ["apple", "AAPL", "bank", "", "invalid"]
    
    for query in callback_tests:
        result, style = simulate_callback(query)
        display = style.get("display", "block")
        print(f"   Query: '{query}' -> {result} (display: {display})")
    
    print(f"\n[OK] Autocomplete functionality test complete!")
    print(f"[WEB] Dashboard should be running at: http://localhost:8050")

if __name__ == "__main__":
    test_autocomplete_functionality()