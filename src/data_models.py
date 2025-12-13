"""
Data models for the Stock Moon Dashboard.
Defines the core data structures used throughout the application.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any, ClassVar
from enum import IntEnum
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class MoonPhase(IntEnum):
    """8-phase moon classification system."""
    NEW = 0
    WAXING_CRESCENT = 1
    FIRST_QUARTER = 2
    WAXING_GIBBOUS = 3
    FULL = 4
    WANING_GIBBOUS = 5
    LAST_QUARTER = 6
    WANING_CRESCENT = 7


@dataclass
class StockData:
    """Stock price and volume data for a single trading day."""
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    daily_return: Optional[float] = None
    abs_return: Optional[float] = None
    volatility_7d: Optional[float] = None
    
    def __post_init__(self):
        """Validate data after initialization."""
        self._validate_ohlc_relationships()
        self._validate_positive_values()
    
    def _validate_ohlc_relationships(self):
        """Validate OHLC price relationships."""
        if not (self.low <= self.open <= self.high and 
                self.low <= self.close <= self.high):
            logger.warning(f"OHLC relationship violation on {self.date}: "
                         f"O={self.open}, H={self.high}, L={self.low}, C={self.close}")
    
    def _validate_positive_values(self):
        """Validate that prices and volume are positive."""
        if any(price < 0 for price in [self.open, self.high, self.low, self.close]):
            raise ValueError("Stock prices cannot be negative")
        
        if self.volume < 0:
            raise ValueError("Volume cannot be negative")
    
    def calculate_daily_return(self, previous_close: float) -> float:
        """Calculate daily return percentage."""
        if previous_close <= 0:
            return 0.0
        
        self.daily_return = ((self.close - previous_close) / previous_close) * 100
        self.abs_return = abs(self.daily_return)
        return self.daily_return
    
    def is_trading_day(self) -> bool:
        """Check if this is a valid trading day (weekday)."""
        return self.date.weekday() < 5  # Monday=0, Friday=4


@dataclass
class MoonData:
    """Moon phase and illumination data for a single day."""
    date: datetime
    phase_code: MoonPhase
    illumination: float  # 0-100%
    days_from_full_moon: int
    is_full_moon_window: bool  # ±2 days from full moon
    
    def __post_init__(self):
        """Validate data after initialization."""
        self._validate_illumination()
        self._validate_phase_consistency()
    
    def _validate_illumination(self):
        """Validate illumination percentage."""
        if not (0 <= self.illumination <= 100):
            raise ValueError(f"Illumination must be 0-100%: {self.illumination}")
    
    def _validate_phase_consistency(self):
        """Validate phase code and days from full moon consistency."""
        if not isinstance(self.phase_code, MoonPhase):
            raise ValueError(f"Invalid phase code: {self.phase_code}")
        
        if not (-15 <= self.days_from_full_moon <= 15):
            logger.warning(f"Days from full moon out of typical range: {self.days_from_full_moon}")
    
    def get_phase_name(self) -> str:
        """Get human-readable phase name."""
        phase_names = {
            MoonPhase.NEW: "New Moon",
            MoonPhase.WAXING_CRESCENT: "Waxing Crescent",
            MoonPhase.FIRST_QUARTER: "First Quarter",
            MoonPhase.WAXING_GIBBOUS: "Waxing Gibbous",
            MoonPhase.FULL: "Full Moon",
            MoonPhase.WANING_GIBBOUS: "Waning Gibbous",
            MoonPhase.LAST_QUARTER: "Last Quarter",
            MoonPhase.WANING_CRESCENT: "Waning Crescent"
        }
        return phase_names.get(self.phase_code, "Unknown")
    
    def get_phase_emoji(self) -> str:
        """Get emoji representation of moon phase."""
        phase_emojis = {
            MoonPhase.NEW: "🌑",
            MoonPhase.WAXING_CRESCENT: "🌒",
            MoonPhase.FIRST_QUARTER: "🌓",
            MoonPhase.WAXING_GIBBOUS: "🌔",
            MoonPhase.FULL: "🌕",
            MoonPhase.WANING_GIBBOUS: "🌖",
            MoonPhase.LAST_QUARTER: "🌗",
            MoonPhase.WANING_CRESCENT: "🌘"
        }
        return phase_emojis.get(self.phase_code, "🌙")


@dataclass
class CombinedDataPoint:
    """Combined stock and moon data for analysis."""
    date: datetime
    # Stock data
    open: float
    high: float
    low: float
    close: float
    volume: int
    daily_return: Optional[float] = None
    abs_return: Optional[float] = None
    volatility_7d: Optional[float] = None
    # Moon data
    phase_code: MoonPhase = MoonPhase.NEW
    illumination: float = 0.0
    days_from_full_moon: int = 0
    is_full_moon_window: bool = False
    # Analysis data
    trading_day: bool = True
    anomaly_score: Optional[float] = None


@dataclass
class PhaseMetric:
    """Aggregated metrics for a specific moon phase."""
    phase: MoonPhase
    avg_volatility: float
    green_day_percentage: float
    mean_return: float
    sample_count: int


@dataclass
class CorrelationResults:
    """Statistical correlation analysis results."""
    pearson: float
    spearman: float
    p_values: Dict[str, float]


@dataclass
class VolatilityTest:
    """T-test results for full moon vs baseline volatility."""
    full_moon_volatility: float
    baseline_volatility: float
    t_statistic: float
    p_value: float
    effect_size: float


@dataclass
class AnomalyEvent:
    """Detected anomaly in price movement."""
    date: datetime
    return_magnitude: float
    moon_phase: MoonPhase
    illumination: float
    description: str


@dataclass
class AnalysisResults:
    """Complete analysis results for the dashboard."""
    correlations: CorrelationResults
    phase_metrics: List[PhaseMetric]
    volatility_test: VolatilityTest
    insights: List[str]
    anomalies: List[AnomalyEvent]


def stock_data_to_dict(stock_data: StockData) -> Dict[str, Any]:
    """Convert StockData to dictionary for JSON serialization."""
    return {
        'date': stock_data.date.isoformat(),
        'open': stock_data.open,
        'high': stock_data.high,
        'low': stock_data.low,
        'close': stock_data.close,
        'volume': stock_data.volume,
        'daily_return': stock_data.daily_return,
        'abs_return': stock_data.abs_return,
        'volatility_7d': stock_data.volatility_7d
    }


def moon_data_to_dict(moon_data: MoonData) -> Dict[str, Any]:
    """Convert MoonData to dictionary for JSON serialization."""
    return {
        'date': moon_data.date.isoformat(),
        'phase_code': int(moon_data.phase_code),
        'illumination': moon_data.illumination,
        'days_from_full_moon': moon_data.days_from_full_moon,
        'is_full_moon_window': moon_data.is_full_moon_window
    }

class DataFactory:
    """Factory class for creating data objects from various sources."""
    
    @staticmethod
    def create_stock_data_from_dict(data: Dict[str, Any]) -> StockData:
        """Create StockData from dictionary (e.g., API response)."""
        try:
            from .data_validation import StockDataValidator, DataSanitizer
        except ImportError:
            from data_validation import StockDataValidator, DataSanitizer
        
        # Validate and sanitize the data
        validated_data = StockDataValidator.validate_price_data(data)
        
        # Parse date
        date_obj = DataSanitizer.sanitize_date(validated_data.get('date'))
        if not date_obj:
            raise ValueError("Date is required for StockData")
        
        return StockData(
            date=date_obj,
            open=validated_data['open'],
            high=validated_data['high'],
            low=validated_data['low'],
            close=validated_data['close'],
            volume=validated_data['volume'],
            daily_return=validated_data.get('daily_return'),
            abs_return=validated_data.get('abs_return'),
            volatility_7d=validated_data.get('volatility_7d')
        )
    
    @staticmethod
    def create_moon_data_from_dict(data: Dict[str, Any]) -> MoonData:
        """Create MoonData from dictionary (e.g., API response)."""
        try:
            from .data_validation import MoonDataValidator, DataSanitizer
        except ImportError:
            from data_validation import MoonDataValidator, DataSanitizer
        
        # Validate and sanitize the data
        validated_data = MoonDataValidator.validate_moon_phase_data(data)
        
        # Parse date
        date_obj = DataSanitizer.sanitize_date(validated_data.get('date'))
        if not date_obj:
            raise ValueError("Date is required for MoonData")
        
        # Convert phase code to enum
        phase_code = MoonPhase(validated_data['phase_code'])
        
        return MoonData(
            date=date_obj,
            phase_code=phase_code,
            illumination=validated_data['illumination'],
            days_from_full_moon=validated_data['days_from_full_moon'],
            is_full_moon_window=validated_data.get('is_full_moon_window', False)
        )
    
    @staticmethod
    def create_combined_data_point(stock_data: StockData, moon_data: MoonData) -> CombinedDataPoint:
        """Create CombinedDataPoint from StockData and MoonData."""
        if stock_data.date.date() != moon_data.date.date():
            logger.warning(f"Date mismatch: stock={stock_data.date.date()}, moon={moon_data.date.date()}")
        
        return CombinedDataPoint(
            date=stock_data.date,
            open=stock_data.open,
            high=stock_data.high,
            low=stock_data.low,
            close=stock_data.close,
            volume=stock_data.volume,
            daily_return=stock_data.daily_return,
            abs_return=stock_data.abs_return,
            volatility_7d=stock_data.volatility_7d,
            phase_code=moon_data.phase_code,
            illumination=moon_data.illumination,
            days_from_full_moon=moon_data.days_from_full_moon,
            is_full_moon_window=moon_data.is_full_moon_window,
            trading_day=stock_data.is_trading_day()
        )


def create_dataframe_from_stock_data(stock_data_list: List[StockData]) -> pd.DataFrame:
    """Convert list of StockData to pandas DataFrame."""
    if not stock_data_list:
        return pd.DataFrame()
    
    data = []
    for stock in stock_data_list:
        data.append({
            'date': stock.date,
            'open': stock.open,
            'high': stock.high,
            'low': stock.low,
            'close': stock.close,
            'volume': stock.volume,
            'daily_return': stock.daily_return,
            'abs_return': stock.abs_return,
            'volatility_7d': stock.volatility_7d
        })
    
    df = pd.DataFrame(data)
    df.set_index('date', inplace=True)
    return df


def create_dataframe_from_moon_data(moon_data_list: List[MoonData]) -> pd.DataFrame:
    """Convert list of MoonData to pandas DataFrame."""
    if not moon_data_list:
        return pd.DataFrame()
    
    data = []
    for moon in moon_data_list:
        data.append({
            'date': moon.date,
            'phase_code': int(moon.phase_code),
            'phase_name': moon.get_phase_name(),
            'phase_emoji': moon.get_phase_emoji(),
            'illumination': moon.illumination,
            'days_from_full_moon': moon.days_from_full_moon,
            'is_full_moon_window': moon.is_full_moon_window
        })
    
    df = pd.DataFrame(data)
    df.set_index('date', inplace=True)
    return df


def create_dataframe_from_combined_data(combined_data_list: List[CombinedDataPoint]) -> pd.DataFrame:
    """Convert list of CombinedDataPoint to pandas DataFrame."""
    if not combined_data_list:
        return pd.DataFrame()
    
    data = []
    for point in combined_data_list:
        data.append({
            'date': point.date,
            'open': point.open,
            'high': point.high,
            'low': point.low,
            'close': point.close,
            'volume': point.volume,
            'daily_return': point.daily_return,
            'abs_return': point.abs_return,
            'volatility_7d': point.volatility_7d,
            'phase_code': int(point.phase_code),
            'illumination': point.illumination,
            'days_from_full_moon': point.days_from_full_moon,
            'is_full_moon_window': point.is_full_moon_window,
            'trading_day': point.trading_day,
            'anomaly_score': point.anomaly_score
        })
    
    df = pd.DataFrame(data)
    df.set_index('date', inplace=True)
    return df


def validate_data_consistency(stock_data: List[StockData], moon_data: List[MoonData]) -> bool:
    """
    Validate consistency between stock and moon data lists.
    
    Args:
        stock_data: List of stock data points
        moon_data: List of moon data points
        
    Returns:
        True if data is consistent, False otherwise
    """
    if not stock_data or not moon_data:
        logger.warning("Empty data lists provided")
        return False
    
    # Check date ranges
    stock_dates = {s.date.date() for s in stock_data}
    moon_dates = {m.date.date() for m in moon_data}
    
    # Find overlapping dates
    common_dates = stock_dates.intersection(moon_dates)
    
    if not common_dates:
        logger.error("No overlapping dates between stock and moon data")
        return False
    
    # Check for significant gaps
    missing_stock = moon_dates - stock_dates
    missing_moon = stock_dates - moon_dates
    
    if missing_stock:
        logger.warning(f"Missing stock data for {len(missing_stock)} dates")
    
    if missing_moon:
        logger.warning(f"Missing moon data for {len(missing_moon)} dates")
    
    # Data is consistent if we have at least some overlap
    overlap_ratio = len(common_dates) / max(len(stock_dates), len(moon_dates))
    
    if overlap_ratio < 0.5:
        logger.warning(f"Low data overlap ratio: {overlap_ratio:.2%}")
        return False
    
    logger.info(f"Data consistency check passed. Overlap: {len(common_dates)} dates ({overlap_ratio:.2%})")
    return True