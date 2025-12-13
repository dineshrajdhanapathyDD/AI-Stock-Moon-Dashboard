#!/usr/bin/env python3
"""
Test script to validate all imports and fix any issues.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test all module imports."""
    try:
        print("Testing imports...")
        
        # Test basic imports
        import numpy as np
        print("[OK] numpy imported successfully")
        
        import pandas as pd
        print("[OK] pandas imported successfully")
        
        # Test dashboard components
        from stock_database import stock_db
        print(f"[OK] stock_database imported: {len(stock_db.stocks)} stocks")
        
        from data_models import DataFactory, MoonPhase
        print("[OK] data_models imported successfully")
        
        from cache_manager import cached_stock_data, cached_moon_data
        print("[OK] cache_manager imported successfully")
        
        from mcp_tools import StockDataFetcher, MoonDataFetcher
        print("[OK] mcp_tools imported successfully")
        
        from dashboard import app
        print("[OK] dashboard imported successfully")
        
        print("\n[PARTY] All imports successful!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Import error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)