"""
Statistical analysis functions for the Stock Moon Dashboard.
Implements correlation calculations, t-tests, and phase-based aggregations.
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import pearsonr, spearmanr, ttest_ind, mannwhitneyu
from typing import List, Dict, Tuple, Optional, Any
import logging
from dataclasses import dataclass
from collections import defaultdict

try:
    from .data_models import CombinedDataPoint, MoonPhase, PhaseMetric, CorrelationResults, VolatilityTest
    from .data_validation import ValidationError
except ImportError:
    from data_models import CombinedDataPoint, MoonPhase, PhaseMetric, CorrelationResults, VolatilityTest
    from data_validation import ValidationError

logger = logging.getLogger(__name__)


@dataclass
class StatisticalSummary:
    """Summary of statistical analysis results."""
    sample_size: int
    mean: float
    std: float
    min_value: float
    max_value: float
    median: float
    skewness: float
    kurtosis: float


@dataclass
class CorrelationAnalysis:
    """Detailed correlation analysis results."""
    pearson_correlation: float
    pearson_p_value: float
    spearman_correlation: float
    spearman_p_value: float
    sample_size: int
    confidence_interval_95: Tuple[float, float]
    interpretation: str


@dataclass
class PhaseComparisonResult:
    """Results of comparing metrics across moon phases."""
    phase_metrics: List[PhaseMetric]
    anova_f_statistic: float
    anova_p_value: float
    significant_differences: List[Tuple[MoonPhase, MoonPhase, float]]  # phase1, phase2, p_value


class StatisticalAnalyzer:
    """Main class for statistical analysis of stock-moon relationships."""
    
    def __init__(self, significance_level: float = 0.05):
        """
        Initialize statistical analyzer.
        
        Args:
            significance_level: Alpha level for statistical tests (default: 0.05)
        """
        self.alpha = significance_level
        self.correlation_analyzer = CorrelationAnalyzer()
        self.phase_analyzer = PhaseAnalyzer()
        self.volatility_analyzer = VolatilityAnalyzer()
    
    def perform_comprehensive_analysis(self, data: List[CombinedDataPoint]) -> Dict[str, Any]:
        """
        Perform comprehensive statistical analysis.
        
        Args:
            data: List of combined data points
            
        Returns:
            Dictionary containing all analysis results
        """
        logger.info(f"Performing comprehensive statistical analysis on {len(data)} data points")
        
        if len(data) < 10:
            raise ValidationError("Insufficient data for statistical analysis (minimum 10 points required)")
        
        results = {}
        
        # Correlation analysis
        results['correlations'] = self.correlation_analyzer.analyze_correlations(data)
        
        # Phase-based analysis
        results['phase_analysis'] = self.phase_analyzer.analyze_by_phases(data)
        
        # Volatility analysis
        results['volatility_analysis'] = self.volatility_analyzer.analyze_volatility_patterns(data)
        
        # Full moon window analysis
        results['full_moon_analysis'] = self.analyze_full_moon_effects(data)
        
        # Statistical summaries
        results['summaries'] = self.generate_statistical_summaries(data)
        
        logger.info("Comprehensive statistical analysis completed")
        return results
    
    def analyze_full_moon_effects(self, data: List[CombinedDataPoint]) -> Dict[str, Any]:
        """
        Analyze effects during full moon windows (±2 days).
        
        Args:
            data: List of combined data points
            
        Returns:
            Dictionary with full moon analysis results
        """
        # Separate full moon window vs baseline periods
        full_moon_data = [point for point in data if point.is_full_moon_window]
        baseline_data = [point for point in data if not point.is_full_moon_window]
        
        if len(full_moon_data) < 3 or len(baseline_data) < 3:
            logger.warning("Insufficient data for full moon analysis")
            return {'error': 'Insufficient data for full moon analysis'}
        
        # Extract metrics for comparison
        full_moon_returns = [p.abs_return for p in full_moon_data if p.abs_return is not None]
        baseline_returns = [p.abs_return for p in baseline_data if p.abs_return is not None]
        
        full_moon_volatility = [p.volatility_7d for p in full_moon_data if p.volatility_7d is not None]
        baseline_volatility = [p.volatility_7d for p in baseline_data if p.volatility_7d is not None]
        
        results = {
            'full_moon_periods': len(full_moon_data),
            'baseline_periods': len(baseline_data),
            'return_comparison': self._compare_groups(full_moon_returns, baseline_returns, 'Returns'),
            'volatility_comparison': self._compare_groups(full_moon_volatility, baseline_volatility, 'Volatility')
        }
        
        return results
    
    def generate_statistical_summaries(self, data: List[CombinedDataPoint]) -> Dict[str, StatisticalSummary]:
        """
        Generate statistical summaries for key metrics.
        
        Args:
            data: List of combined data points
            
        Returns:
            Dictionary of metric summaries
        """
        summaries = {}
        
        # Daily returns summary
        returns = [p.daily_return for p in data if p.daily_return is not None]
        if returns:
            summaries['daily_returns'] = self._calculate_summary_stats(returns)
        
        # Volatility summary
        volatilities = [p.volatility_7d for p in data if p.volatility_7d is not None]
        if volatilities:
            summaries['volatility'] = self._calculate_summary_stats(volatilities)
        
        # Moon illumination summary
        illuminations = [p.illumination for p in data]
        summaries['moon_illumination'] = self._calculate_summary_stats(illuminations)
        
        return summaries
    
    def _compare_groups(self, group1: List[float], group2: List[float], 
                       metric_name: str) -> Dict[str, Any]:
        """
        Compare two groups using appropriate statistical tests.
        
        Args:
            group1: First group of values
            group2: Second group of values
            metric_name: Name of the metric being compared
            
        Returns:
            Dictionary with comparison results
        """
        if len(group1) < 3 or len(group2) < 3:
            return {'error': f'Insufficient data for {metric_name} comparison'}
        
        # Calculate descriptive statistics
        mean1, mean2 = np.mean(group1), np.mean(group2)
        std1, std2 = np.std(group1, ddof=1), np.std(group2, ddof=1)
        
        # Perform t-test (assuming normal distribution)
        t_stat, t_p_value = ttest_ind(group1, group2)
        
        # Perform Mann-Whitney U test (non-parametric alternative)
        u_stat, u_p_value = mannwhitneyu(group1, group2, alternative='two-sided')
        
        # Calculate effect size (Cohen's d)
        pooled_std = np.sqrt(((len(group1) - 1) * std1**2 + (len(group2) - 1) * std2**2) / 
                           (len(group1) + len(group2) - 2))
        cohens_d = (mean1 - mean2) / pooled_std if pooled_std > 0 else 0
        
        return {
            'group1_stats': {'mean': mean1, 'std': std1, 'n': len(group1)},
            'group2_stats': {'mean': mean2, 'std': std2, 'n': len(group2)},
            't_test': {'statistic': t_stat, 'p_value': t_p_value},
            'mann_whitney': {'statistic': u_stat, 'p_value': u_p_value},
            'effect_size': cohens_d,
            'significant': t_p_value < self.alpha,
            'interpretation': self._interpret_effect_size(cohens_d)
        }
    
    def _calculate_summary_stats(self, values: List[float]) -> StatisticalSummary:
        """Calculate comprehensive summary statistics."""
        if not values:
            raise ValueError("Cannot calculate statistics for empty list")
        
        arr = np.array(values)
        
        return StatisticalSummary(
            sample_size=len(values),
            mean=float(np.mean(arr)),
            std=float(np.std(arr, ddof=1)),
            min_value=float(np.min(arr)),
            max_value=float(np.max(arr)),
            median=float(np.median(arr)),
            skewness=float(stats.skew(arr)),
            kurtosis=float(stats.kurtosis(arr))
        )
    
    def _interpret_effect_size(self, cohens_d: float) -> str:
        """Interpret Cohen's d effect size."""
        abs_d = abs(cohens_d)
        if abs_d < 0.2:
            return "negligible effect"
        elif abs_d < 0.5:
            return "small effect"
        elif abs_d < 0.8:
            return "medium effect"
        else:
            return "large effect"


class CorrelationAnalyzer:
    """Analyzer for correlation relationships."""
    
    def analyze_correlations(self, data: List[CombinedDataPoint]) -> Dict[str, CorrelationAnalysis]:
        """
        Analyze correlations between stock metrics and moon phases.
        
        Args:
            data: List of combined data points
            
        Returns:
            Dictionary of correlation analyses
        """
        correlations = {}
        
        # Prepare data arrays
        illuminations = np.array([p.illumination for p in data])
        days_from_full = np.array([p.days_from_full_moon for p in data])
        
        # Returns vs moon metrics
        returns_data = [(i, p.daily_return) for i, p in enumerate(data) if p.daily_return is not None]
        if len(returns_data) > 10:
            returns_indices, returns_values = zip(*returns_data)
            returns = np.array(returns_values)
            aligned_illuminations = illuminations[list(returns_indices)]
            aligned_days_from_full = days_from_full[list(returns_indices)]
            
            correlations['returns_vs_illumination'] = self._calculate_correlation(
                returns, aligned_illuminations, 'Daily Returns vs Moon Illumination'
            )
            
            correlations['returns_vs_days_from_full'] = self._calculate_correlation(
                returns, aligned_days_from_full, 'Daily Returns vs Days from Full Moon'
            )
        
        # Volatility vs moon metrics
        volatilities = np.array([p.volatility_7d for p in data if p.volatility_7d is not None])
        if len(volatilities) > 10:
            # Find indices where volatility is available
            vol_indices = [i for i, p in enumerate(data) if p.volatility_7d is not None]
            vol_illuminations = illuminations[vol_indices]
            vol_days_from_full = days_from_full[vol_indices]
            
            correlations['volatility_vs_illumination'] = self._calculate_correlation(
                volatilities, vol_illuminations, 'Volatility vs Moon Illumination'
            )
            
            correlations['volatility_vs_days_from_full'] = self._calculate_correlation(
                volatilities, vol_days_from_full, 'Volatility vs Days from Full Moon'
            )
        
        # Absolute returns vs moon metrics
        abs_returns_data = [(i, p.abs_return) for i, p in enumerate(data) if p.abs_return is not None]
        if len(abs_returns_data) > 10:
            abs_returns_indices, abs_returns_values = zip(*abs_returns_data)
            abs_returns = np.array(abs_returns_values)
            aligned_illuminations = illuminations[list(abs_returns_indices)]
            
            correlations['abs_returns_vs_illumination'] = self._calculate_correlation(
                abs_returns, aligned_illuminations, 'Absolute Returns vs Moon Illumination'
            )
        
        return correlations
    
    def _calculate_correlation(self, x: np.ndarray, y: np.ndarray, 
                             description: str) -> CorrelationAnalysis:
        """
        Calculate comprehensive correlation analysis.
        
        Args:
            x: First variable
            y: Second variable
            description: Description of the correlation
            
        Returns:
            CorrelationAnalysis object
        """
        # Remove any NaN or infinite values
        mask = np.isfinite(x) & np.isfinite(y)
        x_clean = x[mask]
        y_clean = y[mask]
        
        if len(x_clean) < 3:
            logger.warning(f"Insufficient data for correlation: {description}")
            return CorrelationAnalysis(
                pearson_correlation=0.0,
                pearson_p_value=1.0,
                spearman_correlation=0.0,
                spearman_p_value=1.0,
                sample_size=len(x_clean),
                confidence_interval_95=(0.0, 0.0),
                interpretation="Insufficient data"
            )
        
        # Calculate Pearson correlation
        pearson_r, pearson_p = pearsonr(x_clean, y_clean)
        
        # Calculate Spearman correlation
        spearman_r, spearman_p = spearmanr(x_clean, y_clean)
        
        # Calculate 95% confidence interval for Pearson correlation
        ci_lower, ci_upper = self._correlation_confidence_interval(pearson_r, len(x_clean))
        
        # Interpret correlation strength
        interpretation = self._interpret_correlation(pearson_r, pearson_p)
        
        return CorrelationAnalysis(
            pearson_correlation=float(pearson_r),
            pearson_p_value=float(pearson_p),
            spearman_correlation=float(spearman_r),
            spearman_p_value=float(spearman_p),
            sample_size=len(x_clean),
            confidence_interval_95=(ci_lower, ci_upper),
            interpretation=interpretation
        )
    
    def _correlation_confidence_interval(self, r: float, n: int, 
                                       confidence: float = 0.95) -> Tuple[float, float]:
        """Calculate confidence interval for correlation coefficient."""
        if n < 4:
            return (0.0, 0.0)
        
        # Fisher z-transformation
        z = 0.5 * np.log((1 + r) / (1 - r))
        
        # Standard error
        se = 1 / np.sqrt(n - 3)
        
        # Critical value for 95% confidence
        alpha = 1 - confidence
        z_critical = stats.norm.ppf(1 - alpha/2)
        
        # Confidence interval in z-space
        z_lower = z - z_critical * se
        z_upper = z + z_critical * se
        
        # Transform back to correlation space
        r_lower = (np.exp(2 * z_lower) - 1) / (np.exp(2 * z_lower) + 1)
        r_upper = (np.exp(2 * z_upper) - 1) / (np.exp(2 * z_upper) + 1)
        
        return (float(r_lower), float(r_upper))
    
    def _interpret_correlation(self, r: float, p_value: float) -> str:
        """Interpret correlation strength and significance."""
        abs_r = abs(r)
        
        # Determine strength
        if abs_r < 0.1:
            strength = "negligible"
        elif abs_r < 0.3:
            strength = "weak"
        elif abs_r < 0.5:
            strength = "moderate"
        elif abs_r < 0.7:
            strength = "strong"
        else:
            strength = "very strong"
        
        # Determine direction
        direction = "positive" if r > 0 else "negative"
        
        # Determine significance
        significance = "significant" if p_value < 0.05 else "not significant"
        
        return f"{strength} {direction} correlation ({significance})"


class PhaseAnalyzer:
    """Analyzer for moon phase-based comparisons."""
    
    def analyze_by_phases(self, data: List[CombinedDataPoint]) -> PhaseComparisonResult:
        """
        Analyze metrics grouped by moon phases.
        
        Args:
            data: List of combined data points
            
        Returns:
            PhaseComparisonResult object
        """
        # Group data by moon phase
        phase_groups = defaultdict(list)
        for point in data:
            phase_groups[point.phase_code].append(point)
        
        # Calculate metrics for each phase
        phase_metrics = []
        volatility_by_phase = []
        
        for phase in MoonPhase:
            points = phase_groups[phase]
            if not points:
                continue
            
            # Calculate phase metrics
            returns = [p.daily_return for p in points if p.daily_return is not None]
            volatilities = [p.volatility_7d for p in points if p.volatility_7d is not None]
            
            green_days = sum(1 for r in returns if r > 0)
            green_percentage = (green_days / len(returns) * 100) if returns else 0
            
            avg_volatility = np.mean(volatilities) if volatilities else 0
            mean_return = np.mean(returns) if returns else 0
            
            phase_metric = PhaseMetric(
                phase=phase,
                avg_volatility=float(avg_volatility),
                green_day_percentage=float(green_percentage),
                mean_return=float(mean_return),
                sample_count=len(points)
            )
            
            phase_metrics.append(phase_metric)
            
            # Collect volatilities for ANOVA
            if volatilities:
                volatility_by_phase.extend([(phase, v) for v in volatilities])
        
        # Perform ANOVA on volatility across phases
        anova_f, anova_p = self._perform_phase_anova(volatility_by_phase)
        
        # Perform pairwise comparisons if ANOVA is significant
        significant_differences = []
        if anova_p < 0.05:
            significant_differences = self._pairwise_phase_comparisons(phase_groups)
        
        return PhaseComparisonResult(
            phase_metrics=phase_metrics,
            anova_f_statistic=float(anova_f),
            anova_p_value=float(anova_p),
            significant_differences=significant_differences
        )
    
    def _perform_phase_anova(self, volatility_by_phase: List[Tuple[MoonPhase, float]]) -> Tuple[float, float]:
        """Perform ANOVA test on volatility across moon phases."""
        if len(volatility_by_phase) < 10:
            return 0.0, 1.0
        
        # Group volatilities by phase
        phase_volatilities = defaultdict(list)
        for phase, volatility in volatility_by_phase:
            phase_volatilities[phase].append(volatility)
        
        # Filter phases with sufficient data
        groups = [volatilities for volatilities in phase_volatilities.values() 
                 if len(volatilities) >= 3]
        
        if len(groups) < 2:
            return 0.0, 1.0
        
        # Perform one-way ANOVA
        f_stat, p_value = stats.f_oneway(*groups)
        
        return float(f_stat), float(p_value)
    
    def _pairwise_phase_comparisons(self, phase_groups: Dict[MoonPhase, List[CombinedDataPoint]]) -> List[Tuple[MoonPhase, MoonPhase, float]]:
        """Perform pairwise comparisons between moon phases."""
        significant_pairs = []
        
        phases = list(phase_groups.keys())
        
        for i in range(len(phases)):
            for j in range(i + 1, len(phases)):
                phase1, phase2 = phases[i], phases[j]
                
                # Get volatilities for both phases
                vol1 = [p.volatility_7d for p in phase_groups[phase1] if p.volatility_7d is not None]
                vol2 = [p.volatility_7d for p in phase_groups[phase2] if p.volatility_7d is not None]
                
                if len(vol1) >= 3 and len(vol2) >= 3:
                    # Perform t-test
                    _, p_value = ttest_ind(vol1, vol2)
                    
                    # Apply Bonferroni correction for multiple comparisons
                    corrected_alpha = 0.05 / (len(phases) * (len(phases) - 1) / 2)
                    
                    if p_value < corrected_alpha:
                        significant_pairs.append((phase1, phase2, float(p_value)))
        
        return significant_pairs


class VolatilityAnalyzer:
    """Specialized analyzer for volatility patterns."""
    
    def analyze_volatility_patterns(self, data: List[CombinedDataPoint]) -> Dict[str, Any]:
        """
        Analyze volatility patterns in relation to moon phases.
        
        Args:
            data: List of combined data points
            
        Returns:
            Dictionary with volatility analysis results
        """
        # Extract volatility data
        volatilities = [p.volatility_7d for p in data if p.volatility_7d is not None]
        illuminations = [data[i].illumination for i, p in enumerate(data) if p.volatility_7d is not None]
        
        if len(volatilities) < 10:
            return {'error': 'Insufficient volatility data for analysis'}
        
        # Volatility clustering analysis
        clustering_results = self._analyze_volatility_clustering(volatilities)
        
        # Volatility vs illumination relationship
        illumination_relationship = self._analyze_volatility_illumination(volatilities, illuminations)
        
        # Volatility regime detection
        regimes = self._detect_volatility_regimes(volatilities)
        
        return {
            'clustering': clustering_results,
            'illumination_relationship': illumination_relationship,
            'regimes': regimes,
            'summary_stats': {
                'mean_volatility': float(np.mean(volatilities)),
                'volatility_of_volatility': float(np.std(volatilities)),
                'max_volatility': float(np.max(volatilities)),
                'min_volatility': float(np.min(volatilities))
            }
        }
    
    def _analyze_volatility_clustering(self, volatilities: List[float]) -> Dict[str, float]:
        """Analyze volatility clustering using autocorrelation."""
        if len(volatilities) < 20:
            return {'error': 'Insufficient data for clustering analysis'}
        
        # Calculate autocorrelations at different lags
        autocorrs = {}
        for lag in [1, 2, 3, 5, 10]:
            if len(volatilities) > lag:
                corr = np.corrcoef(volatilities[:-lag], volatilities[lag:])[0, 1]
                autocorrs[f'lag_{lag}'] = float(corr) if not np.isnan(corr) else 0.0
        
        return autocorrs
    
    def _analyze_volatility_illumination(self, volatilities: List[float], 
                                       illuminations: List[float]) -> Dict[str, float]:
        """Analyze relationship between volatility and moon illumination."""
        if len(volatilities) != len(illuminations) or len(volatilities) < 10:
            return {'error': 'Data mismatch for volatility-illumination analysis'}
        
        # Calculate correlation
        corr, p_value = pearsonr(volatilities, illuminations)
        
        # Bin illumination and calculate average volatility per bin
        bins = np.linspace(0, 100, 11)  # 10 bins
        bin_indices = np.digitize(illuminations, bins)
        
        bin_volatilities = {}
        for i in range(1, len(bins)):
            bin_mask = bin_indices == i
            if np.any(bin_mask):
                bin_vol = np.mean(np.array(volatilities)[bin_mask])
                bin_volatilities[f'bin_{i-1}'] = float(bin_vol)
        
        return {
            'correlation': float(corr),
            'p_value': float(p_value),
            'bin_volatilities': bin_volatilities
        }
    
    def _detect_volatility_regimes(self, volatilities: List[float]) -> Dict[str, Any]:
        """Detect high and low volatility regimes."""
        if len(volatilities) < 20:
            return {'error': 'Insufficient data for regime detection'}
        
        # Use median as threshold for regime detection
        threshold = np.median(volatilities)
        
        # Identify regime periods
        high_vol_periods = sum(1 for v in volatilities if v > threshold)
        low_vol_periods = len(volatilities) - high_vol_periods
        
        # Calculate regime persistence (average length of consecutive periods)
        regimes = ['high' if v > threshold else 'low' for v in volatilities]
        
        regime_lengths = []
        current_length = 1
        for i in range(1, len(regimes)):
            if regimes[i] == regimes[i-1]:
                current_length += 1
            else:
                regime_lengths.append(current_length)
                current_length = 1
        regime_lengths.append(current_length)
        
        return {
            'threshold': float(threshold),
            'high_vol_periods': high_vol_periods,
            'low_vol_periods': low_vol_periods,
            'avg_regime_length': float(np.mean(regime_lengths)),
            'max_regime_length': max(regime_lengths),
            'regime_switches': len(regime_lengths) - 1
        }