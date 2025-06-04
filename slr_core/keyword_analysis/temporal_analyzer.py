"""
Temporal Analysis Module for Keyword Analysis
Handles time-series analysis, trend tracking, and temporal pattern detection.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Union
from datetime import datetime, timedelta
import logging
from collections import defaultdict, Counter
from scipy import stats
from scipy.stats import mannwhitneyu, kruskal
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class TemporalAnalyzer:
    """
    Analyzes temporal patterns in keyword usage and publication trends.
    
    Features:
    - Time-series analysis of keyword frequency
    - Trend detection and change point analysis
    - Seasonal pattern detection
    - Comparative analysis across time periods
    - Keyword lifecycle analysis
    - Publication volume trends
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the TemporalAnalyzer.
        
        Args:
            config: Configuration dictionary containing temporal analysis settings
        """
        self.config = config
        self.temporal_config = config.get('temporal_analysis', {})
        
        # Analysis parameters
        self.min_occurrences = self.temporal_config.get('min_occurrences', 3)
        self.trend_window = self.temporal_config.get('trend_window', 12)  # months
        self.seasonal_periods = self.temporal_config.get('seasonal_periods', [12, 6, 3])  # months
        self.change_point_threshold = self.temporal_config.get('change_point_threshold', 0.05)
        
        # Time period definitions
        self.time_periods = self.temporal_config.get('time_periods', {
            'early': {'start': 2010, 'end': 2015},
            'middle': {'start': 2016, 'end': 2020},
            'recent': {'start': 2021, 'end': 2025}
        })
        
        # Analysis results storage
        self.keyword_trends = {}
        self.publication_trends = {}
        self.temporal_patterns = {}
        self.lifecycle_analysis = {}
        self.comparative_analysis = {}
        
        logger.info("TemporalAnalyzer initialized")
    
    def analyze_keyword_trends(self, publications: List[Dict], keywords: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze temporal trends in keyword usage.
        
        Args:
            publications: List of publication dictionaries
            keywords: Keywords with their metadata
            
        Returns:
            Dictionary containing trend analysis results
        """
        logger.info("Starting keyword trend analysis")
        
        try:
            # Prepare temporal data
            temporal_data = self._prepare_temporal_data(publications, keywords)
            
            # Analyze trends for each keyword
            trend_results = {}
            for keyword, data in temporal_data.items():
                if len(data) >= self.min_occurrences:
                    trend_results[keyword] = self._analyze_single_keyword_trend(keyword, data)
            
            # Aggregate results
            self.keyword_trends = {
                'individual_trends': trend_results,
                'summary_statistics': self._calculate_trend_summary(trend_results),
                'top_growing_keywords': self._identify_growing_keywords(trend_results),
                'declining_keywords': self._identify_declining_keywords(trend_results),
                'stable_keywords': self._identify_stable_keywords(trend_results)
            }
            
            logger.info(f"Analyzed trends for {len(trend_results)} keywords")
            return self.keyword_trends
            
        except Exception as e:
            logger.error(f"Error in keyword trend analysis: {str(e)}")
            raise
    
    def analyze_publication_trends(self, publications: List[Dict]) -> Dict[str, Any]:
        """
        Analyze temporal trends in publication volume and characteristics.
        
        Args:
            publications: List of publication dictionaries
            
        Returns:
            Dictionary containing publication trend analysis
        """
        logger.info("Starting publication trend analysis")
        
        try:
            # Extract publication dates
            pub_dates = []
            for pub in publications:
                date = self._extract_publication_date(pub)
                if date:
                    pub_dates.append(date)
            
            if not pub_dates:
                return {'error': 'No valid publication dates found'}
            
            # Create time series
            df = pd.DataFrame({'date': pub_dates})
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month
            df['year_month'] = df['date'].dt.to_period('M')
            
            # Analyze publication volume trends
            volume_trends = self._analyze_publication_volume(df)
            
            # Analyze seasonal patterns
            seasonal_patterns = self._analyze_seasonal_patterns(df)
            
            # Analyze growth rates
            growth_analysis = self._analyze_growth_rates(df)
            
            self.publication_trends = {
                'volume_trends': volume_trends,
                'seasonal_patterns': seasonal_patterns,
                'growth_analysis': growth_analysis,
                'total_publications': len(publications),
                'date_range': {
                    'start': min(pub_dates).strftime('%Y-%m-%d'),
                    'end': max(pub_dates).strftime('%Y-%m-%d')
                }
            }
            
            logger.info(f"Analyzed publication trends for {len(publications)} publications")
            return self.publication_trends
            
        except Exception as e:
            logger.error(f"Error in publication trend analysis: {str(e)}")
            raise
    
    def detect_temporal_patterns(self, publications: List[Dict], keywords: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect temporal patterns and anomalies in keyword usage.
        
        Args:
            publications: List of publication dictionaries
            keywords: Keywords with their metadata
            
        Returns:
            Dictionary containing pattern detection results
        """
        logger.info("Starting temporal pattern detection")
        
        try:
            # Prepare data for pattern detection
            temporal_data = self._prepare_temporal_data(publications, keywords)
            
            patterns = {}
            for keyword, data in temporal_data.items():
                if len(data) >= self.min_occurrences:
                    patterns[keyword] = self._detect_keyword_patterns(keyword, data)
            
            # Aggregate pattern analysis
            self.temporal_patterns = {
                'keyword_patterns': patterns,
                'pattern_summary': self._summarize_patterns(patterns),
                'anomalies': self._detect_anomalies(patterns),
                'change_points': self._detect_change_points(patterns)
            }
            
            logger.info(f"Detected patterns for {len(patterns)} keywords")
            return self.temporal_patterns
            
        except Exception as e:
            logger.error(f"Error in temporal pattern detection: {str(e)}")
            raise
    
    def analyze_keyword_lifecycle(self, publications: List[Dict], keywords: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the lifecycle of keywords (emergence, growth, maturity, decline).
        
        Args:
            publications: List of publication dictionaries
            keywords: Keywords with their metadata
            
        Returns:
            Dictionary containing lifecycle analysis results
        """
        logger.info("Starting keyword lifecycle analysis")
        
        try:
            temporal_data = self._prepare_temporal_data(publications, keywords)
            
            lifecycle_results = {}
            for keyword, data in temporal_data.items():
                if len(data) >= self.min_occurrences:
                    lifecycle_results[keyword] = self._analyze_keyword_lifecycle(keyword, data)
            
            # Categorize keywords by lifecycle stage
            lifecycle_categories = self._categorize_lifecycle_stages(lifecycle_results)
            
            self.lifecycle_analysis = {
                'individual_lifecycles': lifecycle_results,
                'lifecycle_categories': lifecycle_categories,
                'emerging_keywords': lifecycle_categories.get('emerging', []),
                'mature_keywords': lifecycle_categories.get('mature', []),
                'declining_keywords': lifecycle_categories.get('declining', [])
            }
            
            logger.info(f"Analyzed lifecycle for {len(lifecycle_results)} keywords")
            return self.lifecycle_analysis
            
        except Exception as e:
            logger.error(f"Error in keyword lifecycle analysis: {str(e)}")
            raise
    
    def compare_time_periods(self, publications: List[Dict], keywords: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare keyword usage across different time periods.
        
        Args:
            publications: List of publication dictionaries
            keywords: Keywords with their metadata
            
        Returns:
            Dictionary containing comparative analysis results
        """
        logger.info("Starting time period comparison")
        
        try:
            # Prepare data for each time period
            period_data = {}
            for period_name, period_config in self.time_periods.items():
                period_pubs = self._filter_publications_by_period(publications, period_config)
                period_keywords = self._extract_keywords_from_publications(period_pubs, keywords)
                period_data[period_name] = period_keywords
            
            # Perform comparative analysis
            comparisons = {}
            period_names = list(period_data.keys())
            
            for i, period1 in enumerate(period_names):
                for period2 in period_names[i+1:]:
                    comparison_key = f"{period1}_vs_{period2}"
                    comparisons[comparison_key] = self._compare_keyword_sets(
                        period_data[period1], 
                        period_data[period2],
                        period1,
                        period2
                    )
            
            # Statistical significance testing
            statistical_tests = self._perform_statistical_tests(period_data)
            
            self.comparative_analysis = {
                'period_data': period_data,
                'pairwise_comparisons': comparisons,
                'statistical_tests': statistical_tests,
                'overall_trends': self._analyze_overall_trends(period_data)
            }
            
            logger.info(f"Completed comparison across {len(self.time_periods)} time periods")
            return self.comparative_analysis
            
        except Exception as e:
            logger.error(f"Error in time period comparison: {str(e)}")
            raise
    
    def _prepare_temporal_data(self, publications: List[Dict], keywords: Dict[str, Any]) -> Dict[str, List]:
        """Prepare temporal data for analysis."""
        temporal_data = defaultdict(list)
        
        for pub in publications:
            pub_date = self._extract_publication_date(pub)
            if not pub_date:
                continue
                
            # Extract keywords from publication
            pub_keywords = self._extract_publication_keywords(pub, keywords)
            
            for keyword in pub_keywords:
                temporal_data[keyword].append({
                    'date': pub_date,
                    'year': pub_date.year,
                    'month': pub_date.month,
                    'publication_id': pub.get('id', ''),
                    'title': pub.get('title', ''),
                    'citation_count': pub.get('cited_by_count', 0)
                })
        
        return dict(temporal_data)
    
    def _analyze_single_keyword_trend(self, keyword: str, data: List[Dict]) -> Dict[str, Any]:
        """Analyze trend for a single keyword."""
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Create monthly aggregations
        monthly_counts = df.groupby(df['date'].dt.to_period('M')).size()
        
        # Calculate trend statistics
        x = np.arange(len(monthly_counts))
        y = monthly_counts.values
        
        # Linear regression for trend
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # Calculate additional metrics
        trend_strength = abs(r_value)
        trend_direction = 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable'
        
        return {
            'keyword': keyword,
            'total_occurrences': len(data),
            'time_span_months': len(monthly_counts),
            'trend_slope': slope,
            'trend_direction': trend_direction,
            'trend_strength': trend_strength,
            'r_squared': r_value**2,
            'p_value': p_value,
            'monthly_average': np.mean(y),
            'monthly_std': np.std(y),
            'first_occurrence': df['date'].min().strftime('%Y-%m-%d'),
            'last_occurrence': df['date'].max().strftime('%Y-%m-%d'),
            'peak_month': monthly_counts.idxmax().strftime('%Y-%m'),
            'peak_count': monthly_counts.max(),
            'monthly_data': monthly_counts.to_dict()
        }
    
    def _calculate_trend_summary(self, trend_results: Dict) -> Dict[str, Any]:
        """Calculate summary statistics for all trends."""
        if not trend_results:
            return {}
        
        slopes = [result['trend_slope'] for result in trend_results.values()]
        r_squared_values = [result['r_squared'] for result in trend_results.values()]
        
        return {
            'total_keywords': len(trend_results),
            'average_slope': np.mean(slopes),
            'slope_std': np.std(slopes),
            'average_r_squared': np.mean(r_squared_values),
            'positive_trends': sum(1 for slope in slopes if slope > 0),
            'negative_trends': sum(1 for slope in slopes if slope < 0),
            'neutral_trends': sum(1 for slope in slopes if abs(slope) < 0.01)
        }
    
    def _identify_growing_keywords(self, trend_results: Dict, top_n: int = 10) -> List[Dict]:
        """Identify top growing keywords."""
        growing = []
        for keyword, result in trend_results.items():
            if result['trend_slope'] > 0 and result['p_value'] < 0.05:
                growing.append({
                    'keyword': keyword,
                    'slope': result['trend_slope'],
                    'r_squared': result['r_squared'],
                    'total_occurrences': result['total_occurrences']
                })
        
        return sorted(growing, key=lambda x: x['slope'], reverse=True)[:top_n]
    
    def _identify_declining_keywords(self, trend_results: Dict, top_n: int = 10) -> List[Dict]:
        """Identify top declining keywords."""
        declining = []
        for keyword, result in trend_results.items():
            if result['trend_slope'] < 0 and result['p_value'] < 0.05:
                declining.append({
                    'keyword': keyword,
                    'slope': result['trend_slope'],
                    'r_squared': result['r_squared'],
                    'total_occurrences': result['total_occurrences']
                })
        
        return sorted(declining, key=lambda x: x['slope'])[:top_n]
    
    def _identify_stable_keywords(self, trend_results: Dict, top_n: int = 10) -> List[Dict]:
        """Identify stable keywords with consistent usage."""
        stable = []
        for keyword, result in trend_results.items():
            if abs(result['trend_slope']) < 0.01 and result['total_occurrences'] >= 5:
                stable.append({
                    'keyword': keyword,
                    'slope': result['trend_slope'],
                    'consistency': 1 / (result['monthly_std'] + 1),  # Higher is more consistent
                    'total_occurrences': result['total_occurrences']
                })
        
        return sorted(stable, key=lambda x: x['consistency'], reverse=True)[:top_n]
    
    def _extract_publication_date(self, publication: Dict) -> Optional[datetime]:
        """Extract publication date from publication dictionary."""
        # Try different date fields
        date_fields = ['publication_date', 'published_date', 'date', 'year']
        
        for field in date_fields:
            if field in publication and publication[field]:
                try:
                    if field == 'year':
                        return datetime(int(publication[field]), 1, 1)
                    else:
                        return pd.to_datetime(publication[field])
                except (ValueError, TypeError):
                    continue
        
        return None
    
    def _extract_publication_keywords(self, publication: Dict, keywords: Dict) -> List[str]:
        """Extract keywords associated with a publication."""
        pub_keywords = []
        
        # Check if publication has keywords field
        if 'keywords' in publication:
            pub_keywords.extend(publication['keywords'])
        
        # Check if keywords are derived from title/abstract
        text_content = ' '.join([
            publication.get('title', ''),
            publication.get('abstract', '')
        ]).lower()
        
        for keyword in keywords.get('all_keywords', []):
            if keyword.lower() in text_content:
                pub_keywords.append(keyword)
        
        return list(set(pub_keywords))
    
    def _analyze_publication_volume(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze publication volume trends."""
        yearly_counts = df.groupby('year').size()
        monthly_counts = df.groupby('year_month').size()
        
        # Calculate year-over-year growth
        yearly_growth = yearly_counts.pct_change().fillna(0)
        
        return {
            'yearly_counts': yearly_counts.to_dict(),
            'monthly_counts': {str(k): v for k, v in monthly_counts.to_dict().items()},
            'yearly_growth_rates': yearly_growth.to_dict(),
            'average_yearly_growth': yearly_growth.mean(),
            'total_years': len(yearly_counts),
            'peak_year': yearly_counts.idxmax(),
            'peak_count': yearly_counts.max()
        }
    
    def _analyze_seasonal_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze seasonal patterns in publication volume."""
        monthly_patterns = df.groupby('month').size()
        
        # Calculate seasonal indices
        overall_mean = monthly_patterns.mean()
        seasonal_indices = monthly_patterns / overall_mean
        
        return {
            'monthly_distribution': monthly_patterns.to_dict(),
            'seasonal_indices': seasonal_indices.to_dict(),
            'peak_month': monthly_patterns.idxmax(),
            'low_month': monthly_patterns.idxmin(),
            'seasonal_variation': seasonal_indices.std()
        }
    
    def _analyze_growth_rates(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze growth rates and acceleration."""
        yearly_counts = df.groupby('year').size()
        growth_rates = yearly_counts.pct_change().fillna(0)
        
        # Calculate acceleration (second derivative)
        acceleration = growth_rates.diff().fillna(0)
        
        return {
            'growth_rates': growth_rates.to_dict(),
            'acceleration': acceleration.to_dict(),
            'average_growth_rate': growth_rates.mean(),
            'growth_volatility': growth_rates.std(),
            'compound_annual_growth_rate': (yearly_counts.iloc[-1] / yearly_counts.iloc[0]) ** (1 / (len(yearly_counts) - 1)) - 1 if len(yearly_counts) > 1 else 0
        }
    
    def _detect_keyword_patterns(self, keyword: str, data: List[Dict]) -> Dict[str, Any]:
        """Detect patterns for a single keyword."""
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        monthly_counts = df.groupby(df['date'].dt.to_period('M')).size()
        
        patterns = {
            'keyword': keyword,
            'seasonality': self._detect_seasonality(monthly_counts),
            'cyclical_patterns': self._detect_cycles(monthly_counts),
            'trend_changes': self._detect_trend_changes(monthly_counts),
            'volatility': monthly_counts.std() / monthly_counts.mean() if monthly_counts.mean() > 0 else 0
        }
        
        return patterns
    
    def _detect_seasonality(self, series: pd.Series) -> Dict[str, Any]:
        """Detect seasonal patterns in time series."""
        # Simple seasonality detection using autocorrelation
        if len(series) < 24:  # Need at least 2 years for seasonal analysis
            return {'detected': False, 'reason': 'insufficient_data'}
        
        # Check for 12-month seasonality
        try:
            autocorr_12 = series.autocorr(lag=12)
            seasonal_strength = abs(autocorr_12) if not pd.isna(autocorr_12) else 0
            
            return {
                'detected': seasonal_strength > 0.3,
                'strength': seasonal_strength,
                'period': 12 if seasonal_strength > 0.3 else None
            }
        except:
            return {'detected': False, 'reason': 'calculation_error'}
    
    def _detect_cycles(self, series: pd.Series) -> Dict[str, Any]:
        """Detect cyclical patterns."""
        if len(series) < 6:
            return {'detected': False, 'reason': 'insufficient_data'}
        
        # Simple cycle detection using peaks and troughs
        from scipy.signal import find_peaks
        
        peaks, _ = find_peaks(series.values)
        troughs, _ = find_peaks(-series.values)
        
        return {
            'peaks_detected': len(peaks),
            'troughs_detected': len(troughs),
            'average_cycle_length': np.mean(np.diff(peaks)) if len(peaks) > 1 else None,
            'cyclical': len(peaks) > 1 and len(troughs) > 1
        }
    
    def _detect_trend_changes(self, series: pd.Series) -> List[Dict]:
        """Detect trend change points."""
        if len(series) < 6:
            return []
        
        # Simple trend change detection using rolling windows
        window = min(6, len(series) // 3)
        rolling_slopes = []
        
        for i in range(window, len(series) - window):
            before = series.iloc[i-window:i]
            after = series.iloc[i:i+window]
            
            x_before = np.arange(len(before))
            x_after = np.arange(len(after))
            
            slope_before = np.polyfit(x_before, before.values, 1)[0]
            slope_after = np.polyfit(x_after, after.values, 1)[0]
            
            rolling_slopes.append({
                'index': i,
                'date': series.index[i],
                'slope_change': slope_after - slope_before,
                'significance': abs(slope_after - slope_before)
            })
        
        # Filter significant changes
        if rolling_slopes:
            threshold = np.std([s['slope_change'] for s in rolling_slopes]) * 2
            significant_changes = [s for s in rolling_slopes if s['significance'] > threshold]
            return significant_changes[:5]  # Return top 5 changes
        
        return []
    
    def _summarize_patterns(self, patterns: Dict) -> Dict[str, Any]:
        """Summarize detected patterns across all keywords."""
        if not patterns:
            return {}
        
        seasonal_count = sum(1 for p in patterns.values() if p['seasonality']['detected'])
        cyclical_count = sum(1 for p in patterns.values() if p['cyclical_patterns']['cyclical'])
        
        return {
            'total_keywords_analyzed': len(patterns),
            'seasonal_keywords': seasonal_count,
            'cyclical_keywords': cyclical_count,
            'keywords_with_trend_changes': sum(1 for p in patterns.values() if p['trend_changes']),
            'average_volatility': np.mean([p['volatility'] for p in patterns.values()])
        }
    
    def _detect_anomalies(self, patterns: Dict) -> List[Dict]:
        """Detect anomalous patterns."""
        anomalies = []
        
        for keyword, pattern in patterns.items():
            if pattern['volatility'] > 2.0:  # High volatility threshold
                anomalies.append({
                    'keyword': keyword,
                    'type': 'high_volatility',
                    'value': pattern['volatility']
                })
        
        return anomalies
    
    def _detect_change_points(self, patterns: Dict) -> List[Dict]:
        """Detect significant change points across keywords."""
        change_points = []
        
        for keyword, pattern in patterns.items():
            for change in pattern['trend_changes']:
                if abs(change['slope_change']) > 0.5:  # Significant change threshold
                    change_points.append({
                        'keyword': keyword,
                        'date': str(change['date']),
                        'slope_change': change['slope_change']
                    })
        
        return sorted(change_points, key=lambda x: abs(x['slope_change']), reverse=True)[:20]
    
    def _analyze_keyword_lifecycle(self, keyword: str, data: List[Dict]) -> Dict[str, Any]:
        """Analyze lifecycle of a keyword."""
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Calculate cumulative usage
        monthly_counts = df.groupby(df['date'].dt.to_period('M')).size()
        cumulative_usage = monthly_counts.cumsum()
        
        # Identify lifecycle phases
        phases = self._identify_lifecycle_phases(monthly_counts)
        
        # Calculate lifecycle metrics
        lifespan_months = len(monthly_counts)
        peak_usage_month = monthly_counts.idxmax()
        peak_position = list(monthly_counts.index).index(peak_usage_month) / lifespan_months
        
        return {
            'keyword': keyword,
            'lifespan_months': lifespan_months,
            'total_usage': len(data),
            'peak_month': str(peak_usage_month),
            'peak_position': peak_position,  # 0 = early, 1 = late
            'phases': phases,
            'current_stage': self._determine_current_stage(phases, peak_position),
            'growth_rate': self._calculate_growth_rate(cumulative_usage),
            'maturity_index': self._calculate_maturity_index(monthly_counts)
        }
    
    def _identify_lifecycle_phases(self, monthly_counts: pd.Series) -> Dict[str, Any]:
        """Identify different phases in keyword lifecycle."""
        total_usage = monthly_counts.sum()
        cumulative = monthly_counts.cumsum()
        
        # Find phases based on cumulative usage percentiles
        phase_boundaries = {
            'emergence': 0.1,    # First 10% of usage
            'growth': 0.5,       # Next 40% of usage
            'maturity': 0.9      # Next 40% of usage
        }
        
        phases = {}
        for phase, threshold in phase_boundaries.items():
            target_usage = total_usage * threshold
            phase_end = cumulative[cumulative >= target_usage].index[0] if any(cumulative >= target_usage) else cumulative.index[-1]
            phases[phase] = {
                'end_period': str(phase_end),
                'usage_at_end': int(cumulative.loc[phase_end])
            }
        
        return phases
    
    def _determine_current_stage(self, phases: Dict, peak_position: float) -> str:
        """Determine current lifecycle stage."""
        if peak_position < 0.3:
            return 'early_peak'
        elif peak_position < 0.7:
            return 'mature'
        else:
            return 'late_stage'
    
    def _calculate_growth_rate(self, cumulative_usage: pd.Series) -> float:
        """Calculate overall growth rate."""
        if len(cumulative_usage) < 2:
            return 0
        
        x = np.arange(len(cumulative_usage))
        y = cumulative_usage.values
        
        # Fit exponential growth model
        try:
            slope, _, _, _, _ = stats.linregress(x, np.log(y + 1))  # +1 to avoid log(0)
            return slope
        except:
            return 0
    
    def _calculate_maturity_index(self, monthly_counts: pd.Series) -> float:
        """Calculate maturity index (0 = emerging, 1 = mature/declining)."""
        if len(monthly_counts) < 3:
            return 0
        
        # Compare recent usage to historical peak
        recent_avg = monthly_counts.tail(3).mean()
        historical_peak = monthly_counts.max()
        
        if historical_peak == 0:
            return 0
        
        return min(1.0, recent_avg / historical_peak)
    
    def _categorize_lifecycle_stages(self, lifecycle_results: Dict) -> Dict[str, List[str]]:
        """Categorize keywords by lifecycle stage."""
        categories = {
            'emerging': [],
            'growing': [],
            'mature': [],
            'declining': []
        }
        
        for keyword, result in lifecycle_results.items():
            stage = result['current_stage']
            growth_rate = result['growth_rate']
            maturity_index = result['maturity_index']
            
            if stage == 'early_peak' and growth_rate > 0.1:
                categories['emerging'].append(keyword)
            elif growth_rate > 0.05 and maturity_index < 0.8:
                categories['growing'].append(keyword)
            elif maturity_index > 0.8 and abs(growth_rate) < 0.05:
                categories['mature'].append(keyword)
            elif growth_rate < -0.05 or maturity_index < 0.3:
                categories['declining'].append(keyword)
            else:
                categories['mature'].append(keyword)  # Default to mature
        
        return categories
    
    def _filter_publications_by_period(self, publications: List[Dict], period_config: Dict) -> List[Dict]:
        """Filter publications by time period."""
        filtered_pubs = []
        start_year = period_config['start']
        end_year = period_config['end']
        
        for pub in publications:
            pub_date = self._extract_publication_date(pub)
            if pub_date and start_year <= pub_date.year <= end_year:
                filtered_pubs.append(pub)
        
        return filtered_pubs
    
    def _extract_keywords_from_publications(self, publications: List[Dict], keywords: Dict) -> Dict[str, int]:
        """Extract keyword frequencies from publications."""
        keyword_counts = Counter()
        
        for pub in publications:
            pub_keywords = self._extract_publication_keywords(pub, keywords)
            keyword_counts.update(pub_keywords)
        
        return dict(keyword_counts)
    
    def _compare_keyword_sets(self, keywords1: Dict[str, int], keywords2: Dict[str, int], 
                             period1: str, period2: str) -> Dict[str, Any]:
        """Compare two sets of keywords from different periods."""
        all_keywords = set(keywords1.keys()) | set(keywords2.keys())
        
        # Calculate changes for each keyword
        keyword_changes = {}
        for keyword in all_keywords:
            count1 = keywords1.get(keyword, 0)
            count2 = keywords2.get(keyword, 0)
            
            if count1 > 0 and count2 > 0:
                change_ratio = count2 / count1
                change_type = 'increased' if change_ratio > 1.2 else 'decreased' if change_ratio < 0.8 else 'stable'
            elif count1 > 0 and count2 == 0:
                change_ratio = 0
                change_type = 'disappeared'
            elif count1 == 0 and count2 > 0:
                change_ratio = float('inf')
                change_type = 'emerged'
            else:
                change_ratio = 1
                change_type = 'stable'
            
            keyword_changes[keyword] = {
                f'{period1}_count': count1,
                f'{period2}_count': count2,
                'change_ratio': change_ratio if change_ratio != float('inf') else 999,
                'change_type': change_type,
                'absolute_change': count2 - count1
            }
        
        # Identify top changes
        emerging = [k for k, v in keyword_changes.items() if v['change_type'] == 'emerged']
        disappearing = [k for k, v in keyword_changes.items() if v['change_type'] == 'disappeared']
        increasing = sorted([k for k, v in keyword_changes.items() if v['change_type'] == 'increased'], 
                           key=lambda k: keyword_changes[k]['change_ratio'], reverse=True)[:10]
        decreasing = sorted([k for k, v in keyword_changes.items() if v['change_type'] == 'decreased'], 
                           key=lambda k: keyword_changes[k]['change_ratio'])[:10]
        
        return {
            'comparison_periods': f"{period1} vs {period2}",
            'total_keywords_period1': len(keywords1),
            'total_keywords_period2': len(keywords2),
            'common_keywords': len(set(keywords1.keys()) & set(keywords2.keys())),
            'emerging_keywords': emerging[:10],
            'disappearing_keywords': disappearing[:10],
            'most_increasing': increasing,
            'most_decreasing': decreasing,
            'keyword_changes': keyword_changes
        }
    
    def _perform_statistical_tests(self, period_data: Dict[str, Dict[str, int]]) -> Dict[str, Any]:
        """Perform statistical tests on period data."""
        tests = {}
        
        # Convert to comparable format
        period_names = list(period_data.keys())
        if len(period_names) < 2:
            return {'error': 'Need at least 2 periods for statistical testing'}
        
        # Get common keywords across periods
        common_keywords = set.intersection(*[set(data.keys()) for data in period_data.values()])
        
        if len(common_keywords) < 5:
            return {'error': 'Insufficient common keywords for statistical testing'}
        
        # Prepare data for testing
        period_vectors = {}
        for period_name, keywords in period_data.items():
            vector = [keywords.get(kw, 0) for kw in common_keywords]
            period_vectors[period_name] = vector
        
        # Perform pairwise tests
        for i, period1 in enumerate(period_names):
            for period2 in period_names[i+1:]:
                test_key = f"{period1}_vs_{period2}"
                
                # Mann-Whitney U test for non-parametric comparison
                try:
                    statistic, p_value = mannwhitneyu(
                        period_vectors[period1], 
                        period_vectors[period2],
                        alternative='two-sided'
                    )
                    
                    tests[test_key] = {
                        'test_type': 'Mann-Whitney U',
                        'statistic': float(statistic),
                        'p_value': float(p_value),
                        'significant': p_value < 0.05,
                        'sample_sizes': [len(period_vectors[period1]), len(period_vectors[period2])]
                    }
                except Exception as e:
                    tests[test_key] = {'error': str(e)}
        
        # Overall test (Kruskal-Wallis for multiple groups)
        if len(period_names) > 2:
            try:
                statistic, p_value = kruskal(*period_vectors.values())
                tests['overall_comparison'] = {
                    'test_type': 'Kruskal-Wallis',
                    'statistic': float(statistic),
                    'p_value': float(p_value),
                    'significant': p_value < 0.05,
                    'groups': len(period_names)
                }
            except Exception as e:
                tests['overall_comparison'] = {'error': str(e)}
        
        return tests
    
    def _analyze_overall_trends(self, period_data: Dict[str, Dict[str, int]]) -> Dict[str, Any]:
        """Analyze overall trends across all periods."""
        # Calculate diversity metrics for each period
        period_metrics = {}
        
        for period_name, keywords in period_data.items():
            if not keywords:
                continue
                
            total_keywords = len(keywords)
            total_occurrences = sum(keywords.values())
            
            # Calculate Shannon diversity index
            if total_occurrences > 0:
                proportions = [count / total_occurrences for count in keywords.values()]
                shannon_diversity = -sum(p * np.log(p) for p in proportions if p > 0)
            else:
                shannon_diversity = 0
            
            # Calculate concentration (Gini coefficient approximation)
            sorted_counts = sorted(keywords.values(), reverse=True)
            n = len(sorted_counts)
            if n > 1 and total_occurrences > 0:
                concentration = sum((2 * i - n - 1) * count for i, count in enumerate(sorted_counts, 1)) / (n * total_occurrences)
            else:
                concentration = 0
            
            period_metrics[period_name] = {
                'total_keywords': total_keywords,
                'total_occurrences': total_occurrences,
                'average_frequency': total_occurrences / total_keywords if total_keywords > 0 else 0,
                'shannon_diversity': shannon_diversity,
                'concentration_index': concentration,
                'top_keywords': dict(sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10])
            }
        
        return {
            'period_metrics': period_metrics,
            'trends': {
                'diversity_trend': self._calculate_diversity_trend(period_metrics),
                'concentration_trend': self._calculate_concentration_trend(period_metrics),
                'volume_trend': self._calculate_volume_trend(period_metrics)
            }
        }
    
    def _calculate_diversity_trend(self, period_metrics: Dict) -> Dict[str, Any]:
        """Calculate diversity trend across periods."""
        diversity_values = [metrics['shannon_diversity'] for metrics in period_metrics.values()]
        
        if len(diversity_values) < 2:
            return {'trend': 'insufficient_data'}
        
        # Simple linear trend
        x = np.arange(len(diversity_values))
        slope, _, r_value, p_value, _ = stats.linregress(x, diversity_values)
        
        return {
            'trend': 'increasing' if slope > 0 else 'decreasing',
            'slope': slope,
            'r_squared': r_value**2,
            'p_value': p_value,
            'values': diversity_values
        }
    
    def _calculate_concentration_trend(self, period_metrics: Dict) -> Dict[str, Any]:
        """Calculate concentration trend across periods."""
        concentration_values = [metrics['concentration_index'] for metrics in period_metrics.values()]
        
        if len(concentration_values) < 2:
            return {'trend': 'insufficient_data'}
        
        x = np.arange(len(concentration_values))
        slope, _, r_value, p_value, _ = stats.linregress(x, concentration_values)
        
        return {
            'trend': 'increasing' if slope > 0 else 'decreasing',
            'slope': slope,
            'r_squared': r_value**2,
            'p_value': p_value,
            'values': concentration_values
        }
    
    def _calculate_volume_trend(self, period_metrics: Dict) -> Dict[str, Any]:
        """Calculate volume trend across periods."""
        volume_values = [metrics['total_occurrences'] for metrics in period_metrics.values()]
        
        if len(volume_values) < 2:
            return {'trend': 'insufficient_data'}
        
        x = np.arange(len(volume_values))
        slope, _, r_value, p_value, _ = stats.linregress(x, volume_values)
        
        return {
            'trend': 'increasing' if slope > 0 else 'decreasing',
            'slope': slope,
            'r_squared': r_value**2,
            'p_value': p_value,
            'values': volume_values
        }
    
    def export_temporal_analysis(self, output_path: str, format: str = 'json') -> str:
        """
        Export temporal analysis results.
        
        Args:
            output_path: Path to save the results
            format: Export format ('json', 'csv', 'excel')
            
        Returns:
            Path to the exported file
        """
        try:
            # Compile all analysis results
            analysis_results = {
                'keyword_trends': self.keyword_trends,
                'publication_trends': self.publication_trends,
                'temporal_patterns': self.temporal_patterns,
                'lifecycle_analysis': self.lifecycle_analysis,
                'comparative_analysis': self.comparative_analysis,
                'export_timestamp': datetime.now().isoformat(),
                'config': self.temporal_config
            }
            
            if format == 'json':
                import json
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(analysis_results, f, indent=2, ensure_ascii=False, default=str)
            
            elif format == 'csv':
                # Export key results to CSV
                self._export_csv_results(analysis_results, output_path)
            
            elif format == 'excel':
                # Export to Excel with multiple sheets
                self._export_excel_results(analysis_results, output_path)
            
            else:
                raise ValueError(f"Unsupported export format: {format}")
            
            logger.info(f"Temporal analysis results exported to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error exporting temporal analysis: {str(e)}")
            raise
    
    def _export_csv_results(self, results: Dict[str, Any], output_path: str):
        """Export key results to CSV format."""
        # Create a summary DataFrame
        summary_data = []
        
        # Add keyword trends
        if 'keyword_trends' in results and 'individual_trends' in results['keyword_trends']:
            for keyword, trend in results['keyword_trends']['individual_trends'].items():
                summary_data.append({
                    'type': 'keyword_trend',
                    'item': keyword,
                    'metric': 'trend_slope',
                    'value': trend['trend_slope'],
                    'significance': trend['p_value']
                })
        
        # Add lifecycle analysis
        if 'lifecycle_analysis' in results and 'individual_lifecycles' in results['lifecycle_analysis']:
            for keyword, lifecycle in results['lifecycle_analysis']['individual_lifecycles'].items():
                summary_data.append({
                    'type': 'lifecycle',
                    'item': keyword,
                    'metric': 'current_stage',
                    'value': lifecycle['current_stage'],
                    'significance': lifecycle['growth_rate']
                })
        
        df = pd.DataFrame(summary_data)
        df.to_csv(output_path, index=False)
    
    def _export_excel_results(self, results: Dict[str, Any], output_path: str):
        """Export results to Excel with multiple sheets."""
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Keyword trends sheet
            if 'keyword_trends' in results and 'individual_trends' in results['keyword_trends']:
                trends_data = []
                for keyword, trend in results['keyword_trends']['individual_trends'].items():
                    trends_data.append({
                        'keyword': keyword,
                        'trend_slope': trend['trend_slope'],
                        'trend_direction': trend['trend_direction'],
                        'r_squared': trend['r_squared'],
                        'p_value': trend['p_value'],
                        'total_occurrences': trend['total_occurrences']
                    })
                
                pd.DataFrame(trends_data).to_excel(writer, sheet_name='Keyword_Trends', index=False)
            
            # Lifecycle analysis sheet
            if 'lifecycle_analysis' in results and 'individual_lifecycles' in results['lifecycle_analysis']:
                lifecycle_data = []
                for keyword, lifecycle in results['lifecycle_analysis']['individual_lifecycles'].items():
                    lifecycle_data.append({
                        'keyword': keyword,
                        'current_stage': lifecycle['current_stage'],
                        'lifespan_months': lifecycle['lifespan_months'],
                        'growth_rate': lifecycle['growth_rate'],
                        'maturity_index': lifecycle['maturity_index']
                    })
                
                pd.DataFrame(lifecycle_data).to_excel(writer, sheet_name='Lifecycle_Analysis', index=False)
