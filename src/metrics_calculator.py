"""
Metrics calculation engine for the Stock Moon Dashboard.
Handles daily returns, volatility calculations, and moon phase metrics.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional, Union
import logging
from math import sqrt, pi, sin, cos

try:
    from .data_models import StockData, MoonData, CombinedDataPoint, MoonPhase
    from .data_validation import ValidationError
except ImportError:
    from data_models import StockData, MoonData, CombinedDataPoint, MoonPhase
    from data_validation import ValidationError

logger = logging.getLogger(__name__)


class MetricsCalculator:
    """Main class for calculating financial and lunar metrics."""
    
    def __init__(self):
        self.stock_calculator = StockMetricsCalculator()
        self.moon_calculator = MoonMetricsCalculator()
    
    def calculate_all_metrics(self, combined_data: List[CombinedDataPoint], 
                            rolling_window: int = 7) -> List[CombinedDataPoint]:
        """
        Calculate all metrics for combined dataset.
        
        Args:
            combined_data: List of combined data points
            rolling_window: Window size for rolling calculations
            
        Returns:
            List of data points with calculated metrics
        """
        logger.info(f"Calculating metrics for {len(combined_data)} data points with {rolling_window}-day window")
        
        if not combined_data:
            return combined_data
        
        # Sort by date to ensure proper order
        sorted_data = sorted(combined_data, key=lambda x: x.date)
        
        # Calculate stock metrics
        updated_data = self.stock_calculator.calculate_stock_metrics(sorted_data, rolling_window)
        
        # Calculate moon metrics (already calculated during data creation, but validate)
        validated_data = self.moon_calculator.validate_moon_metrics(updated_data)
        
        logger.info("Metrics calculation completed")
        return validated_data


class StockMetricsCalculator:
    """Calculator for stock-related metrics."""
    
    def calculate_stock_metrics(self, data_points: List[CombinedDataPoint], 
                              rolling_window: int = 7) -> List[CombinedDataPoint]:
        """
        Calculate stock metrics including returns and volatility.
        
        Args:
            data_points: List of combined data points
            rolling_window: Window size for rolling calculations
            
        Returns:
            List with calculated stock metrics
        """
        if len(data_points) < 2:
            logger.warning("Insufficient data for stock metrics calculation")
            return data_points
        
        updated_points = []
        
        for i, point in enumerate(data_points):
            # Calculate daily return
            if i > 0:
                prev_close = data_points[i-1].close
                daily_return = self.calculate_daily_return(point.close, prev_close)
                abs_return = abs(daily_return)
            else:
                daily_return = 0.0
                abs_return = 0.0
            
            # Calculate rolling volatility
            volatility = self.calculate_rolling_volatility(
                data_points, i, rolling_window
            )
            
            # Create updated point
            updated_point = CombinedDataPoint(
                date=point.date,
                open=point.open,
                high=point.high,
                low=point.low,
                close=point.close,
                volume=point.volume,
                daily_return=daily_return,
                abs_return=abs_return,
                volatility_7d=volatility,
                phase_code=point.phase_code,
                illumination=point.illumination,
                days_from_full_moon=point.days_from_full_moon,
                is_full_moon_window=point.is_full_moon_window,
                trading_day=point.trading_day,
                anomaly_score=point.anomaly_score
            )
            
            updated_points.append(updated_point)
        
        return updated_points
    
    def calculate_daily_return(self, current_price: float, previous_price: float) -> float:
        """
        Calculate daily return percentage.
        
        Args:
            current_price: Current closing price
            previous_price: Previous closing price
            
        Returns:
            Daily return as percentage
        """
        if previous_price <= 0:
            return 0.0
        
        return ((current_price - previous_price) / previous_price) * 100
    
    def calculate_rolling_volatility(self, data_points: List[CombinedDataPoint], 
                                   current_index: int, window_size: int) -> Optional[float]:
        """
        Calculate rolling volatility (standard deviation of returns).
        
        Args:
            data_points: List of all data points
            current_index: Index of current point
            window_size: Rolling window size
            
        Returns:
            Rolling volatility or None if insufficient data
        """
        if current_index < window_size:
            return None
        
        # Get returns for the window
        returns = []
        for i in range(max(0, current_index - window_size + 1), current_index + 1):
            if i > 0:  # Skip first point as it has no return
                prev_close = data_points[i-1].close
                curr_close = data_points[i].close
                daily_return = self.calculate_daily_return(curr_close, prev_close)
                returns.append(daily_return)
        
        if len(returns) < 2:
            return None
        
        # Calculate standard deviation
        return float(np.std(returns, ddof=1))
    
    def calculate_price_momentum(self, data_points: List[CombinedDataPoint], 
                               current_index: int, lookback_days: int = 5) -> float:
        """
        Calculate price momentum over specified period.
        
        Args:
            data_points: List of all data points
            current_index: Index of current point
            lookback_days: Number of days to look back
            
        Returns:
            Price momentum as percentage change
        """
        if current_index < lookback_days:
            return 0.0
        
        current_price = data_points[current_index].close
        past_price = data_points[current_index - lookback_days].close
        
        return self.calculate_daily_return(current_price, past_price)
    
    def calculate_intraday_range(self, point: CombinedDataPoint) -> float:
        """
        Calculate intraday price range as percentage of close.
        
        Args:
            point: Data point with OHLC data
            
        Returns:
            Intraday range percentage
        """
        if point.close <= 0:
            return 0.0
        
        return ((point.high - point.low) / point.close) * 100


class MoonMetricsCalculator:
    """Calculator for moon-related metrics."""
    
    def validate_moon_metrics(self, data_points: List[CombinedDataPoint]) -> List[CombinedDataPoint]:
        """
        Validate and enhance moon metrics.
        
        Args:
            data_points: List of combined data points
            
        Returns:
            List with validated moon metrics
        """
        validated_points = []
        
        for point in data_points:
            # Validate phase consistency
            validated_phase = self.validate_phase_consistency(
                point.phase_code, point.illumination, point.days_from_full_moon
            )
            
            # Calculate additional moon metrics
            lunar_cycle_position = self.calculate_lunar_cycle_position(point.days_from_full_moon)
            
            # Create validated point (keeping all existing data)
            validated_point = CombinedDataPoint(
                date=point.date,
                open=point.open,
                high=point.high,
                low=point.low,
                close=point.close,
                volume=point.volume,
                daily_return=point.daily_return,
                abs_return=point.abs_return,
                volatility_7d=point.volatility_7d,
                phase_code=validated_phase,
                illumination=point.illumination,
                days_from_full_moon=point.days_from_full_moon,
                is_full_moon_window=point.is_full_moon_window,
                trading_day=point.trading_day,
                anomaly_score=point.anomaly_score
            )
            
            validated_points.append(validated_point)
        
        return validated_points
    
    def validate_phase_consistency(self, phase_code: MoonPhase, 
                                 illumination: float, days_from_full: int) -> MoonPhase:
        """
        Validate consistency between phase code, illumination, and days from full moon.
        
        Args:
            phase_code: Current phase code
            illumination: Illumination percentage
            days_from_full: Days from full moon
            
        Returns:
            Validated phase code
        """
        # Check if illumination matches phase expectations
        expected_ranges = {
            MoonPhase.NEW: (0, 12.5),
            MoonPhase.WAXING_CRESCENT: (12.5, 37.5),
            MoonPhase.FIRST_QUARTER: (37.5, 62.5),
            MoonPhase.WAXING_GIBBOUS: (62.5, 87.5),
            MoonPhase.FULL: (87.5, 100),
            MoonPhase.WANING_GIBBOUS: (62.5, 87.5),
            MoonPhase.LAST_QUARTER: (37.5, 62.5),
            MoonPhase.WANING_CRESCENT: (12.5, 37.5)
        }
        
        min_illum, max_illum = expected_ranges.get(phase_code, (0, 100))
        
        if not (min_illum <= illumination <= max_illum):
            logger.warning(f"Phase-illumination mismatch: {phase_code.name} with {illumination}% illumination")
        
        return phase_code
    
    def calculate_lunar_cycle_position(self, days_from_full: int) -> float:
        """
        Calculate position in lunar cycle (0-1).
        
        Args:
            days_from_full: Days from full moon
            
        Returns:
            Cycle position (0 = new moon, 0.5 = full moon)
        """
        # Lunar cycle is approximately 29.5 days
        cycle_length = 29.5
        
        # Convert days from full moon to cycle position
        # Full moon is at position 0.5
        if days_from_full >= 0:
            # Before full moon (waxing)
            position = 0.5 - (days_from_full / cycle_length)
        else:
            # After full moon (waning)
            position = 0.5 + (abs(days_from_full) / cycle_length)
        
        # Normalize to 0-1 range
        return position % 1.0
    
    def calculate_moon_phase_strength(self, illumination: float, phase_code: MoonPhase) -> float:
        """
        Calculate the "strength" of a moon phase (how close to peak).
        
        Args:
            illumination: Moon illumination percentage
            phase_code: Moon phase code
            
        Returns:
            Phase strength (0-1, where 1 is peak phase)
        """
        # Define peak illumination for each phase
        peak_illuminations = {
            MoonPhase.NEW: 0,
            MoonPhase.WAXING_CRESCENT: 25,
            MoonPhase.FIRST_QUARTER: 50,
            MoonPhase.WAXING_GIBBOUS: 75,
            MoonPhase.FULL: 100,
            MoonPhase.WANING_GIBBOUS: 75,
            MoonPhase.LAST_QUARTER: 50,
            MoonPhase.WANING_CRESCENT: 25
        }
        
        peak_illum = peak_illuminations.get(phase_code, 50)
        
        # Calculate how close current illumination is to peak
        max_deviation = 25  # Maximum expected deviation from peak
        deviation = abs(illumination - peak_illum)
        
        # Convert to strength (1 = at peak, 0 = maximum deviation)
        strength = max(0, 1 - (deviation / max_deviation))
        
        return strength


class VolatilityCalculator:
    """Specialized calculator for various volatility measures."""
    
    @staticmethod
    def calculate_garman_klass_volatility(data_points: List[CombinedDataPoint], 
                                        window_size: int = 20) -> List[float]:
        """
        Calculate Garman-Klass volatility estimator using OHLC data.
        
        Args:
            data_points: List of data points with OHLC data
            window_size: Rolling window size
            
        Returns:
            List of volatility estimates
        """
        volatilities = []
        
        for i in range(len(data_points)):
            if i < window_size - 1:
                volatilities.append(None)
                continue
            
            # Calculate GK volatility for window
            gk_values = []
            for j in range(i - window_size + 1, i + 1):
                point = data_points[j]
                
                if point.open > 0 and point.close > 0:
                    # Garman-Klass formula components
                    ln_h_o = np.log(point.high / point.open)
                    ln_l_o = np.log(point.low / point.open)
                    ln_c_o = np.log(point.close / point.open)
                    
                    gk_value = ln_h_o * (ln_h_o - ln_c_o) + ln_l_o * (ln_l_o - ln_c_o)
                    gk_values.append(gk_value)
            
            if gk_values:
                volatility = np.sqrt(np.mean(gk_values)) * np.sqrt(252) * 100  # Annualized %
                volatilities.append(volatility)
            else:
                volatilities.append(None)
        
        return volatilities
    
    @staticmethod
    def calculate_parkinson_volatility(data_points: List[CombinedDataPoint], 
                                     window_size: int = 20) -> List[float]:
        """
        Calculate Parkinson volatility estimator using high-low range.
        
        Args:
            data_points: List of data points with OHLC data
            window_size: Rolling window size
            
        Returns:
            List of volatility estimates
        """
        volatilities = []
        
        for i in range(len(data_points)):
            if i < window_size - 1:
                volatilities.append(None)
                continue
            
            # Calculate Parkinson volatility for window
            ln_hl_squared = []
            for j in range(i - window_size + 1, i + 1):
                point = data_points[j]
                
                if point.high > 0 and point.low > 0:
                    ln_hl = np.log(point.high / point.low)
                    ln_hl_squared.append(ln_hl ** 2)
            
            if ln_hl_squared:
                # Parkinson estimator
                volatility = np.sqrt(np.mean(ln_hl_squared) / (4 * np.log(2))) * np.sqrt(252) * 100
                volatilities.append(volatility)
            else:
                volatilities.append(None)
        
        return volatilities


def calculate_comprehensive_metrics(combined_data: List[CombinedDataPoint], 
                                  rolling_windows: List[int] = [7, 14, 30]) -> Dict[str, List[float]]:
    """
    Calculate comprehensive metrics for multiple rolling windows.
    
    Args:
        combined_data: List of combined data points
        rolling_windows: List of window sizes to calculate
        
    Returns:
        Dictionary of metric names to lists of values
    """
    calculator = MetricsCalculator()
    volatility_calc = VolatilityCalculator()
    
    metrics = {}
    
    # Calculate basic metrics for each window
    for window in rolling_windows:
        updated_data = calculator.calculate_all_metrics(combined_data, window)
        
        # Extract volatility values
        volatilities = [point.volatility_7d for point in updated_data]
        metrics[f'volatility_{window}d'] = volatilities
        
        # Calculate returns
        returns = [point.daily_return or 0.0 for point in updated_data]
        metrics[f'returns_{window}d'] = returns
        
        # Calculate absolute returns
        abs_returns = [point.abs_return or 0.0 for point in updated_data]
        metrics[f'abs_returns_{window}d'] = abs_returns
    
    # Calculate advanced volatility measures
    gk_volatility = volatility_calc.calculate_garman_klass_volatility(combined_data)
    parkinson_volatility = volatility_calc.calculate_parkinson_volatility(combined_data)
    
    metrics['garman_klass_volatility'] = gk_volatility
    metrics['parkinson_volatility'] = parkinson_volatility
    
    # Calculate moon-related metrics
    illuminations = [point.illumination for point in combined_data]
    days_from_full = [point.days_from_full_moon for point in combined_data]
    
    metrics['moon_illumination'] = illuminations
    metrics['days_from_full_moon'] = days_from_full
    
    # Calculate phase strengths
    moon_calc = MoonMetricsCalculator()
    phase_strengths = [
        moon_calc.calculate_moon_phase_strength(point.illumination, point.phase_code)
        for point in combined_data
    ]
    metrics['moon_phase_strength'] = phase_strengths
    
    logger.info(f"Calculated comprehensive metrics for {len(combined_data)} data points")
    return metrics


def validate_metrics_quality(metrics: Dict[str, List[float]]) -> Dict[str, bool]:
    """
    Validate the quality of calculated metrics.
    
    Args:
        metrics: Dictionary of calculated metrics
        
    Returns:
        Dictionary of metric names to validation results
    """
    validation_results = {}
    
    for metric_name, values in metrics.items():
        # Remove None values for validation
        clean_values = [v for v in values if v is not None]
        
        if not clean_values:
            validation_results[metric_name] = False
            continue
        
        # Check for reasonable ranges
        if 'volatility' in metric_name:
            # Volatility should be positive and reasonable (0-200%)
            valid = all(0 <= v <= 200 for v in clean_values)
        elif 'return' in metric_name:
            # Returns should be reasonable (-50% to +50% daily)
            valid = all(-50 <= v <= 50 for v in clean_values)
        elif 'illumination' in metric_name:
            # Illumination should be 0-100%
            valid = all(0 <= v <= 100 for v in clean_values)
        elif 'days_from_full' in metric_name:
            # Days from full moon should be reasonable (-15 to +15)
            valid = all(-15 <= v <= 15 for v in clean_values)
        else:
            # Generic validation - check for finite values
            valid = all(np.isfinite(v) for v in clean_values)
        
        validation_results[metric_name] = valid
        
        if not valid:
            logger.warning(f"Metric validation failed for {metric_name}")
    
    return validation_results