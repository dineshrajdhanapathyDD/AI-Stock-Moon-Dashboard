"""
Data alignment and normalization utilities for the Stock Moon Dashboard.
Handles timestamp normalization, timezone correction, and data joining.
"""

import pytz
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Tuple, Optional, Set
import logging
import pandas as pd

try:
    from .data_models import StockData, MoonData, CombinedDataPoint, DataFactory
    from .data_validation import ValidationError
except ImportError:
    from data_models import StockData, MoonData, CombinedDataPoint, DataFactory
    from data_validation import ValidationError

logger = logging.getLogger(__name__)


class DataAligner:
    """Class for aligning and normalizing stock and moon data."""
    
    def __init__(self, target_timezone: str = 'UTC'):
        """
        Initialize DataAligner.
        
        Args:
            target_timezone: Target timezone for normalization (default: UTC)
        """
        self.target_tz = pytz.timezone(target_timezone)
        self.market_holidays = self._get_market_holidays()
    
    def normalize_timestamps_to_utc(self, stock_data: List[StockData], 
                                  moon_data: List[MoonData]) -> Tuple[List[StockData], List[MoonData]]:
        """
        Normalize all timestamps to UTC.
        
        Args:
            stock_data: List of stock data points
            moon_data: List of moon data points
            
        Returns:
            Tuple of normalized stock and moon data lists
        """
        logger.info("Normalizing timestamps to UTC")
        
        # Normalize stock data timestamps
        normalized_stock = []
        for stock in stock_data:
            normalized_date = self._normalize_datetime_to_utc(stock.date)
            normalized_stock.append(StockData(
                date=normalized_date,
                open=stock.open,
                high=stock.high,
                low=stock.low,
                close=stock.close,
                volume=stock.volume,
                daily_return=stock.daily_return,
                abs_return=stock.abs_return,
                volatility_7d=stock.volatility_7d
            ))
        
        # Normalize moon data timestamps
        normalized_moon = []
        for moon in moon_data:
            normalized_date = self._normalize_datetime_to_utc(moon.date)
            normalized_moon.append(MoonData(
                date=normalized_date,
                phase_code=moon.phase_code,
                illumination=moon.illumination,
                days_from_full_moon=moon.days_from_full_moon,
                is_full_moon_window=moon.is_full_moon_window
            ))
        
        logger.info(f"Normalized {len(normalized_stock)} stock and {len(normalized_moon)} moon data points")
        return normalized_stock, normalized_moon
    
    def align_data_by_trading_dates(self, stock_data: List[StockData], 
                                  moon_data: List[MoonData]) -> List[CombinedDataPoint]:
        """
        Align stock and moon data by trading dates.
        
        Args:
            stock_data: List of stock data points
            moon_data: List of moon data points
            
        Returns:
            List of combined data points aligned by date
        """
        logger.info("Aligning data by trading dates")
        
        # First normalize timestamps
        norm_stock, norm_moon = self.normalize_timestamps_to_utc(stock_data, moon_data)
        
        # Create date-indexed dictionaries for fast lookup
        stock_by_date = {stock.date.date(): stock for stock in norm_stock}
        moon_by_date = {moon.date.date(): moon for moon in norm_moon}
        
        # Find common dates (prioritize trading days)
        stock_dates = set(stock_by_date.keys())
        moon_dates = set(moon_by_date.keys())
        common_dates = stock_dates.intersection(moon_dates)
        
        if not common_dates:
            raise ValidationError("No overlapping dates found between stock and moon data")
        
        # Create combined data points
        combined_data = []
        for date in sorted(common_dates):
            stock = stock_by_date[date]
            moon = moon_by_date[date]
            
            # Only include trading days for stock analysis
            if self._is_trading_day(date):
                combined_point = DataFactory.create_combined_data_point(stock, moon)
                combined_data.append(combined_point)
        
        # Handle missing trading days by interpolating moon data
        combined_data = self._fill_missing_trading_days(combined_data, stock_by_date, moon_by_date)
        
        logger.info(f"Aligned {len(combined_data)} data points")
        return combined_data
    
    def handle_market_closures(self, stock_data: List[StockData]) -> List[StockData]:
        """
        Handle weekends and market holidays gracefully.
        
        Args:
            stock_data: List of stock data points
            
        Returns:
            Filtered stock data excluding non-trading days
        """
        logger.info("Handling market closures")
        
        trading_day_data = []
        excluded_count = 0
        
        for stock in stock_data:
            date = stock.date.date()
            
            if self._is_trading_day(date):
                trading_day_data.append(stock)
            else:
                excluded_count += 1
                logger.debug(f"Excluded non-trading day: {date}")
        
        logger.info(f"Kept {len(trading_day_data)} trading days, excluded {excluded_count} non-trading days")
        return trading_day_data
    
    def correct_timezone_misalignments(self, data_points: List[CombinedDataPoint]) -> List[CombinedDataPoint]:
        """
        Detect and correct timezone misalignments.
        
        Args:
            data_points: List of combined data points
            
        Returns:
            List with corrected timezone alignments
        """
        logger.info("Checking for timezone misalignments")
        
        corrected_data = []
        corrections_made = 0
        
        for point in data_points:
            corrected_date = self._normalize_datetime_to_utc(point.date)
            
            if corrected_date != point.date:
                corrections_made += 1
                logger.debug(f"Corrected timezone: {point.date} -> {corrected_date}")
            
            # Create new point with corrected timestamp
            corrected_point = CombinedDataPoint(
                date=corrected_date,
                open=point.open,
                high=point.high,
                low=point.low,
                close=point.close,
                volume=point.volume,
                daily_return=point.daily_return,
                abs_return=point.abs_return,
                volatility_7d=point.volatility_7d,
                phase_code=point.phase_code,
                illumination=point.illumination,
                days_from_full_moon=point.days_from_full_moon,
                is_full_moon_window=point.is_full_moon_window,
                trading_day=point.trading_day,
                anomaly_score=point.anomaly_score
            )
            
            corrected_data.append(corrected_point)
        
        if corrections_made > 0:
            logger.info(f"Made {corrections_made} timezone corrections")
        else:
            logger.info("No timezone corrections needed")
        
        return corrected_data
    
    def _normalize_datetime_to_utc(self, dt: datetime) -> datetime:
        """Normalize datetime to UTC timezone."""
        if dt.tzinfo is None:
            # Assume naive datetime is in UTC
            return dt.replace(tzinfo=timezone.utc)
        elif dt.tzinfo != timezone.utc:
            # Convert to UTC
            return dt.astimezone(timezone.utc)
        else:
            # Already UTC
            return dt
    
    def _is_trading_day(self, date) -> bool:
        """
        Check if a date is a trading day (weekday, not a holiday).
        
        Args:
            date: Date to check (datetime.date object)
            
        Returns:
            True if it's a trading day, False otherwise
        """
        # Check if it's a weekend
        if date.weekday() >= 5:  # Saturday=5, Sunday=6
            return False
        
        # Check if it's a market holiday
        if date in self.market_holidays:
            return False
        
        return True
    
    def _get_market_holidays(self) -> Set:
        """
        Get set of market holidays for recent years.
        
        Returns:
            Set of holiday dates
        """
        # Common US market holidays (simplified)
        holidays = set()
        
        # Add major holidays for 2023-2025
        for year in range(2023, 2026):
            # New Year's Day
            holidays.add(datetime(year, 1, 1).date())
            
            # Independence Day
            holidays.add(datetime(year, 7, 4).date())
            
            # Christmas Day
            holidays.add(datetime(year, 12, 25).date())
            
            # Thanksgiving (4th Thursday in November)
            thanksgiving = self._get_nth_weekday(year, 11, 3, 4)  # 4th Thursday
            holidays.add(thanksgiving)
            
            # Black Friday (day after Thanksgiving)
            holidays.add(thanksgiving + timedelta(days=1))
        
        return holidays
    
    def _get_nth_weekday(self, year: int, month: int, weekday: int, n: int) -> datetime.date:
        """
        Get the nth occurrence of a weekday in a month.
        
        Args:
            year: Year
            month: Month (1-12)
            weekday: Weekday (0=Monday, 6=Sunday)
            n: Which occurrence (1-5)
            
        Returns:
            Date of the nth weekday
        """
        first_day = datetime(year, month, 1)
        first_weekday = first_day.weekday()
        
        # Calculate days to add to get to the first occurrence
        days_to_add = (weekday - first_weekday) % 7
        first_occurrence = first_day + timedelta(days=days_to_add)
        
        # Add weeks to get to the nth occurrence
        nth_occurrence = first_occurrence + timedelta(weeks=n-1)
        
        return nth_occurrence.date()
    
    def _fill_missing_trading_days(self, combined_data: List[CombinedDataPoint],
                                 stock_by_date: Dict, moon_by_date: Dict) -> List[CombinedDataPoint]:
        """
        Fill missing trading days by interpolating moon data.
        
        Args:
            combined_data: Existing combined data points
            stock_by_date: Stock data indexed by date
            moon_by_date: Moon data indexed by date
            
        Returns:
            Combined data with filled missing days
        """
        if not combined_data:
            return combined_data
        
        # Get date range
        dates = [point.date.date() for point in combined_data]
        start_date = min(dates)
        end_date = max(dates)
        
        # Create complete list of trading days in range
        current_date = start_date
        all_trading_days = []
        
        while current_date <= end_date:
            if self._is_trading_day(current_date):
                all_trading_days.append(current_date)
            current_date += timedelta(days=1)
        
        # Find missing trading days
        existing_dates = set(dates)
        missing_dates = [d for d in all_trading_days if d not in existing_dates]
        
        if not missing_dates:
            return combined_data
        
        logger.info(f"Filling {len(missing_dates)} missing trading days")
        
        # Add missing days with interpolated moon data
        filled_data = list(combined_data)
        
        for missing_date in missing_dates:
            if missing_date in stock_by_date:
                stock = stock_by_date[missing_date]
                
                # Find closest moon data for interpolation
                moon = self._find_closest_moon_data(missing_date, moon_by_date)
                
                if moon:
                    combined_point = DataFactory.create_combined_data_point(stock, moon)
                    filled_data.append(combined_point)
        
        # Sort by date
        filled_data.sort(key=lambda x: x.date)
        
        return filled_data
    
    def _find_closest_moon_data(self, target_date, moon_by_date: Dict) -> Optional[MoonData]:
        """
        Find the closest moon data to a target date.
        
        Args:
            target_date: Target date to find moon data for
            moon_by_date: Moon data indexed by date
            
        Returns:
            Closest MoonData object or None
        """
        if target_date in moon_by_date:
            return moon_by_date[target_date]
        
        # Find closest date within reasonable range (±3 days)
        for offset in range(1, 4):
            # Check previous days
            prev_date = target_date - timedelta(days=offset)
            if prev_date in moon_by_date:
                return moon_by_date[prev_date]
            
            # Check next days
            next_date = target_date + timedelta(days=offset)
            if next_date in moon_by_date:
                return moon_by_date[next_date]
        
        return None


def create_aligned_dataset(stock_data: List[StockData], moon_data: List[MoonData],
                         target_timezone: str = 'UTC') -> List[CombinedDataPoint]:
    """
    Convenience function to create a fully aligned dataset.
    
    Args:
        stock_data: List of stock data points
        moon_data: List of moon data points
        target_timezone: Target timezone for normalization
        
    Returns:
        List of aligned combined data points
    """
    aligner = DataAligner(target_timezone)
    
    # Handle market closures first
    trading_stock_data = aligner.handle_market_closures(stock_data)
    
    # Align data by trading dates
    aligned_data = aligner.align_data_by_trading_dates(trading_stock_data, moon_data)
    
    # Correct any timezone misalignments
    corrected_data = aligner.correct_timezone_misalignments(aligned_data)
    
    return corrected_data


def validate_data_alignment(combined_data: List[CombinedDataPoint]) -> bool:
    """
    Validate that aligned data meets quality requirements.
    
    Args:
        combined_data: List of combined data points
        
    Returns:
        True if alignment is valid, False otherwise
    """
    if not combined_data:
        logger.error("No combined data to validate")
        return False
    
    # Check for chronological order
    dates = [point.date for point in combined_data]
    if dates != sorted(dates):
        logger.error("Data is not in chronological order")
        return False
    
    # Check for duplicate dates
    date_set = set(dates)
    if len(date_set) != len(dates):
        logger.error("Duplicate dates found in aligned data")
        return False
    
    # Check for reasonable data gaps
    for i in range(1, len(combined_data)):
        gap = (combined_data[i].date - combined_data[i-1].date).days
        if gap > 7:  # More than a week gap
            logger.warning(f"Large gap in data: {gap} days between {combined_data[i-1].date.date()} and {combined_data[i].date.date()}")
    
    # Check timezone consistency
    timezones = {point.date.tzinfo for point in combined_data}
    if len(timezones) > 1:
        logger.error(f"Inconsistent timezones in aligned data: {timezones}")
        return False
    
    logger.info(f"Data alignment validation passed for {len(combined_data)} points")
    return True