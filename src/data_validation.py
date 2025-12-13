"""
Data validation functions for the Stock Moon Dashboard.
Provides validation, sanitization, and conversion utilities for API responses.
"""

import re
from datetime import datetime, date
from typing import Any, Dict, List, Optional, Union, Tuple
import logging

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for data validation errors."""
    pass


class StockDataValidator:
    """Validator for stock price data."""
    
    @staticmethod
    def validate_ticker_symbol(symbol: str) -> str:
        """
        Validate and sanitize stock ticker symbol.
        
        Args:
            symbol: Raw ticker symbol input
            
        Returns:
            Cleaned ticker symbol
            
        Raises:
            ValidationError: If symbol is invalid
        """
        if not symbol or not isinstance(symbol, str):
            raise ValidationError("Ticker symbol must be a non-empty string")
        
        # Clean and uppercase the symbol
        cleaned = symbol.strip().upper()
        
        # Validate format: 1-5 letters, optionally followed by a dot and more letters
        if not re.match(r'^[A-Z]{1,5}(\.[A-Z]{1,3})?$', cleaned):
            raise ValidationError(f"Invalid ticker symbol format: {symbol}")
        
        return cleaned
    
    @staticmethod
    def validate_price_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and sanitize stock price data from API response.
        
        Args:
            data: Raw price data dictionary
            
        Returns:
            Validated and sanitized data
            
        Raises:
            ValidationError: If data is invalid
        """
        required_fields = ['open', 'high', 'low', 'close', 'volume']
        
        # Check required fields exist
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Missing required field: {field}")
        
        validated = {}
        
        # Validate and convert price fields
        for field in ['open', 'high', 'low', 'close']:
            value = data[field]
            if value is None:
                raise ValidationError(f"Price field {field} cannot be None")
            
            try:
                price = float(value)
                if price < 0:
                    raise ValidationError(f"Price field {field} cannot be negative: {price}")
                validated[field] = price
            except (ValueError, TypeError):
                raise ValidationError(f"Invalid price value for {field}: {value}")
        
        # Validate volume
        try:
            volume = int(data['volume'] or 0)
            if volume < 0:
                raise ValidationError(f"Volume cannot be negative: {volume}")
            validated['volume'] = volume
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid volume value: {data['volume']}")
        
        # Validate OHLC relationships
        if not (validated['low'] <= validated['open'] <= validated['high'] and
                validated['low'] <= validated['close'] <= validated['high']):
            logger.warning(f"OHLC relationship violation: O={validated['open']}, "
                         f"H={validated['high']}, L={validated['low']}, C={validated['close']}")
        
        # Copy other fields
        for key, value in data.items():
            if key not in validated:
                validated[key] = value
        
        return validated
    
    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> Tuple[datetime, datetime]:
        """
        Validate and parse date range.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Tuple of parsed datetime objects
            
        Raises:
            ValidationError: If dates are invalid
        """
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError as e:
            raise ValidationError(f"Invalid date format: {str(e)}")
        
        if start_dt > end_dt:
            raise ValidationError("Start date must be before end date")
        
        # Check if dates are too far in the future
        today = datetime.now()
        if start_dt > today or end_dt > today:
            raise ValidationError("Dates cannot be in the future")
        
        # Check if date range is reasonable (not more than 10 years)
        if (end_dt - start_dt).days > 3650:
            raise ValidationError("Date range cannot exceed 10 years")
        
        return start_dt, end_dt


class MoonDataValidator:
    """Validator for moon phase data."""
    
    @staticmethod
    def validate_coordinates(latitude: float, longitude: float) -> Tuple[float, float]:
        """
        Validate geographic coordinates.
        
        Args:
            latitude: Latitude in degrees
            longitude: Longitude in degrees
            
        Returns:
            Validated coordinates
            
        Raises:
            ValidationError: If coordinates are invalid
        """
        try:
            lat = float(latitude)
            lon = float(longitude)
        except (ValueError, TypeError):
            raise ValidationError("Coordinates must be numeric values")
        
        if not (-90 <= lat <= 90):
            raise ValidationError(f"Latitude must be between -90 and 90: {lat}")
        
        if not (-180 <= lon <= 180):
            raise ValidationError(f"Longitude must be between -180 and 180: {lon}")
        
        return lat, lon
    
    @staticmethod
    def validate_moon_phase_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate moon phase data.
        
        Args:
            data: Raw moon phase data
            
        Returns:
            Validated data
            
        Raises:
            ValidationError: If data is invalid
        """
        validated = {}
        
        # Validate phase code
        if 'phase_code' in data:
            try:
                phase_code = int(data['phase_code'])
                if not (0 <= phase_code <= 7):
                    raise ValidationError(f"Phase code must be 0-7: {phase_code}")
                validated['phase_code'] = phase_code
            except (ValueError, TypeError):
                raise ValidationError(f"Invalid phase code: {data['phase_code']}")
        
        # Validate illumination
        if 'illumination' in data:
            try:
                illumination = float(data['illumination'])
                if not (0 <= illumination <= 100):
                    raise ValidationError(f"Illumination must be 0-100%: {illumination}")
                validated['illumination'] = illumination
            except (ValueError, TypeError):
                raise ValidationError(f"Invalid illumination: {data['illumination']}")
        
        # Validate days from full moon
        if 'days_from_full_moon' in data:
            try:
                days = int(data['days_from_full_moon'])
                if not (-15 <= days <= 15):  # Reasonable range for lunar cycle
                    raise ValidationError(f"Days from full moon out of range: {days}")
                validated['days_from_full_moon'] = days
            except (ValueError, TypeError):
                raise ValidationError(f"Invalid days from full moon: {data['days_from_full_moon']}")
        
        # Copy other fields
        for key, value in data.items():
            if key not in validated:
                validated[key] = value
        
        return validated


class DataSanitizer:
    """Utility functions for data sanitization and conversion."""
    
    @staticmethod
    def sanitize_string(value: Any) -> Optional[str]:
        """Sanitize string input."""
        if value is None:
            return None
        
        if isinstance(value, str):
            return value.strip()
        
        return str(value).strip()
    
    @staticmethod
    def sanitize_number(value: Any, allow_none: bool = False) -> Optional[float]:
        """Sanitize numeric input."""
        if value is None:
            return None if allow_none else 0.0
        
        if isinstance(value, (int, float)):
            return float(value)
        
        if isinstance(value, str):
            try:
                return float(value.strip())
            except ValueError:
                if allow_none:
                    return None
                raise ValidationError(f"Cannot convert to number: {value}")
        
        raise ValidationError(f"Invalid numeric type: {type(value)}")
    
    @staticmethod
    def sanitize_date(value: Any) -> Optional[datetime]:
        """Sanitize date input."""
        if value is None:
            return None
        
        if isinstance(value, datetime):
            return value
        
        if isinstance(value, date):
            return datetime.combine(value, datetime.min.time())
        
        if isinstance(value, str):
            # Try common date formats
            formats = [
                "%Y-%m-%d",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M:%S",
                "%m/%d/%Y",
                "%d/%m/%Y"
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(value.strip(), fmt)
                except ValueError:
                    continue
            
            raise ValidationError(f"Cannot parse date: {value}")
        
        raise ValidationError(f"Invalid date type: {type(value)}")
    
    @staticmethod
    def clean_api_response(response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and standardize API response data.
        
        Args:
            response: Raw API response
            
        Returns:
            Cleaned response data
        """
        if not isinstance(response, dict):
            raise ValidationError("API response must be a dictionary")
        
        cleaned = {}
        
        for key, value in response.items():
            # Convert keys to lowercase with underscores
            clean_key = key.lower().replace(' ', '_').replace('-', '_')
            
            # Clean the value based on type
            if isinstance(value, str):
                cleaned[clean_key] = DataSanitizer.sanitize_string(value)
            elif isinstance(value, (int, float)):
                cleaned[clean_key] = DataSanitizer.sanitize_number(value)
            elif isinstance(value, list):
                cleaned[clean_key] = [DataSanitizer.clean_api_response(item) 
                                    if isinstance(item, dict) else item 
                                    for item in value]
            elif isinstance(value, dict):
                cleaned[clean_key] = DataSanitizer.clean_api_response(value)
            else:
                cleaned[clean_key] = value
        
        return cleaned


def validate_analysis_parameters(symbol: str, start_date: str, end_date: str, 
                               rolling_window: int = 7, 
                               latitude: float = 40.7128, 
                               longitude: float = -74.0060) -> Dict[str, Any]:
    """
    Validate all analysis parameters at once.
    
    Args:
        symbol: Stock ticker symbol
        start_date: Start date string
        end_date: End date string
        rolling_window: Rolling window size for calculations
        latitude: Latitude for moon calculations
        longitude: Longitude for moon calculations
        
    Returns:
        Dictionary of validated parameters
        
    Raises:
        ValidationError: If any parameter is invalid
    """
    # Validate ticker symbol
    clean_symbol = StockDataValidator.validate_ticker_symbol(symbol)
    
    # Validate date range
    start_dt, end_dt = StockDataValidator.validate_date_range(start_date, end_date)
    
    # Validate rolling window
    if not isinstance(rolling_window, int) or rolling_window < 1:
        raise ValidationError(f"Rolling window must be a positive integer: {rolling_window}")
    
    if rolling_window > 365:
        raise ValidationError(f"Rolling window too large: {rolling_window}")
    
    # Validate coordinates
    clean_lat, clean_lon = MoonDataValidator.validate_coordinates(latitude, longitude)
    
    return {
        'symbol': clean_symbol,
        'start_date': start_dt.strftime("%Y-%m-%d"),
        'end_date': end_dt.strftime("%Y-%m-%d"),
        'rolling_window': rolling_window,
        'latitude': clean_lat,
        'longitude': clean_lon
    }