"""
MCP (Model Context Protocol) tools for external data fetching.
Implements getStockPrices and getMoonPhase tools for Yahoo Finance and Open-Meteo APIs.
"""

import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import time
import logging
from urllib.parse import urlencode

try:
    from .data_models import StockData, MoonData, MoonPhase
except ImportError:
    from data_models import StockData, MoonData, MoonPhase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPToolError(Exception):
    """Custom exception for MCP tool errors."""
    pass


class StockDataFetcher:
    """MCP tool for fetching stock data from Yahoo Finance."""
    
    def __init__(self):
        self.base_url = "https://query1.finance.yahoo.com/v8/finance/chart"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_stock_prices(self, symbol: str, start_date: str, end_date: str, 
                        interval: str = "1d") -> List[StockData]:
        """
        Fetch stock price data from Yahoo Finance.
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL')
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            interval: Data interval ('1d', '1wk', '1mo')
            
        Returns:
            List of StockData objects
            
        Raises:
            MCPToolError: If data fetching fails
        """
        try:
            # Convert dates to timestamps
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            
            start_timestamp = int(start_dt.timestamp())
            end_timestamp = int(end_dt.timestamp())
            
            # Build URL
            url = f"{self.base_url}/{symbol}"
            params = {
                'period1': start_timestamp,
                'period2': end_timestamp,
                'interval': interval,
                'includePrePost': 'false',
                'events': 'div,splits'
            }
            
            logger.info(f"Fetching stock data for {symbol} from {start_date} to {end_date}")
            
            # Make request with retry logic
            response = self._make_request_with_retry(url, params)
            data = response.json()
            
            # Parse response
            if 'chart' not in data or not data['chart']['result']:
                raise MCPToolError(f"No data found for symbol {symbol}")
            
            result = data['chart']['result'][0]
            timestamps = result['timestamp']
            quotes = result['indicators']['quote'][0]
            
            # Convert to StockData objects
            stock_data = []
            for i, timestamp in enumerate(timestamps):
                date = datetime.fromtimestamp(timestamp)
                
                # Skip if any required data is None
                if any(quotes[field][i] is None for field in ['open', 'high', 'low', 'close']):
                    continue
                
                stock_data.append(StockData(
                    date=date,
                    open=float(quotes['open'][i]),
                    high=float(quotes['high'][i]),
                    low=float(quotes['low'][i]),
                    close=float(quotes['close'][i]),
                    volume=int(quotes['volume'][i] or 0)
                ))
            
            logger.info(f"Successfully fetched {len(stock_data)} data points for {symbol}")
            return stock_data
            
        except Exception as e:
            logger.error(f"Error fetching stock data for {symbol}: {str(e)}")
            raise MCPToolError(f"Failed to fetch stock data: {str(e)}")
    
    def _make_request_with_retry(self, url: str, params: Dict[str, Any], 
                                max_retries: int = 3) -> requests.Response:
        """Make HTTP request with retry logic."""
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if attempt == max_retries - 1:
                    raise
                logger.warning(f"Request failed (attempt {attempt + 1}): {str(e)}")
                time.sleep(2 ** attempt)  # Exponential backoff


class MoonDataFetcher:
    """MCP tool for fetching moon phase data using astronomical calculations."""
    
    def __init__(self):
        # Fallback to astronomical calculations since Open-Meteo API has issues
        pass
    
    def get_moon_phase(self, latitude: float, longitude: float, 
                      start_date: str, end_date: str) -> List[MoonData]:
        """
        Calculate moon phase data using astronomical formulas.
        
        Args:
            latitude: Latitude coordinate (not used in calculation but kept for API compatibility)
            longitude: Longitude coordinate (not used in calculation but kept for API compatibility)
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            List of MoonData objects
            
        Raises:
            MCPToolError: If calculation fails
        """
        try:
            logger.info(f"Calculating moon data from {start_date} to {end_date}")
            
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            
            moon_data = []
            current_date = start_dt
            
            while current_date <= end_dt:
                # Calculate moon phase using astronomical formula
                phase_value = self._calculate_moon_phase(current_date)
                
                # Convert phase value to our enum and calculate metrics
                phase_code = self._convert_phase_value(phase_value)
                illumination = self._calculate_illumination(phase_value)
                days_from_full = self._calculate_days_from_full_moon(phase_value)
                is_full_window = abs(days_from_full) <= 2
                
                moon_data.append(MoonData(
                    date=current_date,
                    phase_code=phase_code,
                    illumination=illumination,
                    days_from_full_moon=days_from_full,
                    is_full_moon_window=is_full_window
                ))
                
                current_date += timedelta(days=1)
            
            logger.info(f"Successfully calculated {len(moon_data)} moon phase data points")
            return moon_data
            
        except Exception as e:
            logger.error(f"Error calculating moon data: {str(e)}")
            raise MCPToolError(f"Failed to calculate moon data: {str(e)}")
    
    def _calculate_moon_phase(self, date: datetime) -> float:
        """
        Calculate moon phase using astronomical formula.
        Returns value between 0 (new moon) and 1 (next new moon).
        """
        # Known new moon date: January 11, 2024
        known_new_moon = datetime(2024, 1, 11)
        
        # Lunar cycle is approximately 29.53059 days
        lunar_cycle = 29.53059
        
        # Calculate days since known new moon
        days_since = (date - known_new_moon).total_seconds() / (24 * 3600)
        
        # Calculate phase (0 to 1)
        phase = (days_since % lunar_cycle) / lunar_cycle
        
        return phase
    
    def _make_request_with_retry(self, url: str, params: Dict[str, Any], 
                                max_retries: int = 3) -> requests.Response:
        """Make HTTP request with retry logic."""
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if attempt == max_retries - 1:
                    raise
                logger.warning(f"Request failed (attempt {attempt + 1}): {str(e)}")
                time.sleep(2 ** attempt)
    
    def _convert_phase_value(self, phase_value: float) -> MoonPhase:
        """Convert Open-Meteo phase value to our MoonPhase enum."""
        # Open-Meteo uses 0-1 scale where 0=new moon, 0.5=full moon
        if phase_value < 0.0625:  # 0-1/16
            return MoonPhase.NEW
        elif phase_value < 0.1875:  # 1/16-3/16
            return MoonPhase.WAXING_CRESCENT
        elif phase_value < 0.3125:  # 3/16-5/16
            return MoonPhase.FIRST_QUARTER
        elif phase_value < 0.4375:  # 5/16-7/16
            return MoonPhase.WAXING_GIBBOUS
        elif phase_value < 0.5625:  # 7/16-9/16
            return MoonPhase.FULL
        elif phase_value < 0.6875:  # 9/16-11/16
            return MoonPhase.WANING_GIBBOUS
        elif phase_value < 0.8125:  # 11/16-13/16
            return MoonPhase.LAST_QUARTER
        else:  # 13/16-1
            return MoonPhase.WANING_CRESCENT
    
    def _calculate_illumination(self, phase_value: float) -> float:
        """Calculate moon illumination percentage from phase value."""
        # Convert 0-1 phase to illumination percentage
        # Full moon (0.5) = 100%, new moon (0 or 1) = 0%
        if phase_value <= 0.5:
            return phase_value * 200  # 0-0.5 -> 0-100%
        else:
            return (1 - phase_value) * 200  # 0.5-1 -> 100-0%
    
    def _calculate_days_from_full_moon(self, phase_value: float) -> int:
        """Calculate days from full moon based on phase value."""
        # Approximate calculation: full lunar cycle is ~29.5 days
        cycle_days = 29.5
        if phase_value <= 0.5:
            # Waxing phase: days until full moon
            return int((0.5 - phase_value) * cycle_days)
        else:
            # Waning phase: days since full moon
            return -int((phase_value - 0.5) * cycle_days)


# MCP tool instances
stock_fetcher = StockDataFetcher()
moon_fetcher = MoonDataFetcher()


def get_stock_prices(symbol: str, start_date: str, end_date: str, 
                    interval: str = "1d") -> List[Dict[str, Any]]:
    """
    MCP tool function for fetching stock prices.
    
    Returns data as list of dictionaries for JSON serialization.
    """
    stock_data = stock_fetcher.get_stock_prices(symbol, start_date, end_date, interval)
    return [
        {
            'date': data.date.isoformat(),
            'open': data.open,
            'high': data.high,
            'low': data.low,
            'close': data.close,
            'volume': data.volume
        }
        for data in stock_data
    ]


def get_moon_phase(latitude: float, longitude: float, 
                  start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """
    MCP tool function for fetching moon phase data.
    
    Returns data as list of dictionaries for JSON serialization.
    """
    moon_data = moon_fetcher.get_moon_phase(latitude, longitude, start_date, end_date)
    return [
        {
            'date': data.date.isoformat(),
            'phase_code': int(data.phase_code),
            'illumination': data.illumination,
            'days_from_full_moon': data.days_from_full_moon,
            'is_full_moon_window': data.is_full_moon_window
        }
        for data in moon_data
    ]