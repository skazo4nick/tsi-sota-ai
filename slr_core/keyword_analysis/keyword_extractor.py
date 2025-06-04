"""
KeywordExtractor: Extract keywords from publication metadata and abstracts

This module handles:
1. Extraction of existing keywords provided by academic APIs
2. NLP-based keyword extraction using TF-IDF, RAKE, and YAKE
3. Frequency analysis and temporal distribution tracking
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Union, Tuple
import re
from collections import Counter, defaultdict
import logging

# NLP Libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.chunk import ne_chunk
from nltk.tag import pos_tag

# Keyword extraction libraries
try:
    import yake
except ImportError:
    yake = None
    
try:
    from rake_nltk import Rake
except ImportError:
    Rake = None

# Scikit-learn for TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Configuration
from ..config_manager import ConfigManager

class KeywordExtractor:
    """
    Comprehensive keyword extraction from publication data
    
    Supports:
    - API-provided keywords extraction
    - TF-IDF based keyword extraction
    - RAKE (Rapid Automatic Keyword Extraction)
    - YAKE (Yet Another Keyword Extractor)
    - Frequency analysis and temporal tracking
    """
    
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        """
        Initialize KeywordExtractor with configuration
        
        Args:
            config_manager: ConfigManager instance for settings
        """
        self.config = config_manager or ConfigManager()
        self.logger = logging.getLogger(__name__)
        
        # Get configuration settings
        self.keyword_config = self.config.get('keyword_analysis', {})
        self.nlp_config = self.keyword_config.get('nlp', {})
        self.output_config = self.keyword_config.get('output', {})
        
        # Initialize NLP components
        self._init_nltk_components()
        self._init_extractors()
        
    def _init_nltk_components(self):
        """Initialize NLTK components with error handling"""
        try:
            # Download required NLTK data
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)  
            nltk.download('wordnet', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            nltk.download('maxent_ne_chunker', quiet=True)
            nltk.download('words', quiet=True)
            
            self.stop_words = set(stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
            
            # Add domain-specific stop words
            domain_stop_words = {
                'paper', 'article', 'study', 'research', 'analysis', 'approach',
                'method', 'result', 'conclusion', 'abstract', 'introduction',
                'literature', 'review', 'survey', 'work', 'works', 'author',
                'authors', 'et', 'al', 'also', 'however', 'therefore', 'thus',
                'furthermore', 'moreover', 'additionally', 'finally'
            }
            self.stop_words.update(domain_stop_words)
            
        except Exception as e:
            self.logger.warning(f"Error initializing NLTK components: {e}")
            self.stop_words = set()
            self.lemmatizer = None
    
    def _init_extractors(self):
        """Initialize keyword extraction algorithms"""
        # Initialize TF-IDF vectorizer
        tfidf_config = self.nlp_config.get('tfidf', {})
        self.tfidf_vectorizer = TfidfVectorizer(
            ngram_range=tuple(tfidf_config.get('ngram_range', [1, 3])),
            max_features=tfidf_config.get('max_features', 1000),
            min_df=tfidf_config.get('min_df', 2),
            max_df=tfidf_config.get('max_df', 0.85),
            stop_words=list(self.stop_words) if self.stop_words else 'english',
            lowercase=True,
            token_pattern=r'\b[a-zA-Z][a-zA-Z]+\b'  # Only alphabetic tokens
        )
        
        # Initialize RAKE
        if Rake is not None:
            rake_config = self.nlp_config.get('rake', {})
            self.rake = Rake(
                min_length=rake_config.get('min_length', 1),
                max_length=rake_config.get('max_length', 4),
                stopwords=self.stop_words if self.stop_words else None
            )
        else:
            self.rake = None
            self.logger.warning("RAKE not available. Install rake-nltk package.")
            
        # Initialize YAKE
        if yake is not None:
            yake_config = self.nlp_config.get('yake', {})
            self.yake_extractor = yake.KeywordExtractor(
                lan=yake_config.get('language', 'en'),
                n=yake_config.get('max_ngram_size', 3),
                dedupLim=yake_config.get('deduplication_threshold', 0.7),
                top=yake_config.get('num_keywords', 20)
            )
        else:
            self.yake_extractor = None
            self.logger.warning("YAKE not available. Install yake package.")

    def extract_api_keywords(self, publications_df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract keywords that are already provided by academic APIs
        
        Args:
            publications_df: DataFrame with publication metadata
            
        Returns:
            DataFrame with extracted API keywords and metadata
        """
        if publications_df.empty:
            return pd.DataFrame()
            
        api_keywords_data = []
        
        for idx, row in publications_df.iterrows():
            # Extract keywords from the API-provided keywords field
            api_keywords = []
            
            # Handle different keyword field formats
            try:
                if 'keywords' in publications_df.columns and row['keywords'] is not None and str(row['keywords']) != 'nan':
                    keywords_raw = row['keywords']
                    
                    if isinstance(keywords_raw, list):
                        api_keywords = [str(kw).strip() for kw in keywords_raw if kw is not None and str(kw).strip()]
                    elif isinstance(keywords_raw, str):
                        # Handle comma-separated, semicolon-separated, or pipe-separated
                        for sep in [',', ';', '|']:
                            if sep in keywords_raw:
                                api_keywords = [kw.strip() for kw in keywords_raw.split(sep) if kw.strip()]
                                break
                        if not api_keywords:
                            api_keywords = [keywords_raw.strip()]
            except Exception as e:
                self.logger.warning(f"Error extracting API keywords from row {idx}: {e}")
                api_keywords = []
            
            # Also extract from fieldsOfStudy if available (OpenAlex, Semantic Scholar)
            if 'fieldsOfStudy' in publications_df.columns and not pd.isna(row['fieldsOfStudy']):
                fields = row['fieldsOfStudy']
                if isinstance(fields, list):
                    api_keywords.extend([str(field).strip() for field in fields if field is not None and str(field).strip()])
                elif isinstance(fields, str):
                    api_keywords.extend([field.strip() for field in fields.split(',') if field.strip()])
            
            # Clean and normalize keywords
            cleaned_keywords = []
            for kw in api_keywords:
                kw_clean = self._clean_keyword(kw)
                if kw_clean and len(kw_clean) > 2:  # Filter very short keywords
                    cleaned_keywords.append(kw_clean)
            
            # Add to results
            for keyword in cleaned_keywords:
                api_keywords_data.append({
                    'publication_id': idx,
                    'doi': row.get('doi', ''),
                    'title': row.get('title', ''),
                    'publication_date': row.get('publication_date', ''),
                    'source': row.get('source', ''),
                    'keyword': keyword,
                    'extraction_method': 'api_provided',
                    'keyword_type': 'api'
                })
        
        api_keywords_df = pd.DataFrame(api_keywords_data)
        
        if not api_keywords_df.empty:
            # Add year column for temporal analysis
            api_keywords_df['year'] = api_keywords_df['publication_date'].apply(
                self._extract_year_from_date
            )
            
            self.logger.info(f"Extracted {len(api_keywords_df)} API-provided keywords from {len(publications_df)} publications")
        
        return api_keywords_df
    
    def extract_nlp_keywords(self, 
                           texts: List[str], 
                           method: str = 'tfidf',
                           **kwargs) -> Dict[str, Any]:
        """
        Extract keywords using NLP techniques
        
        Args:
            texts: List of text documents (abstracts, titles, etc.)
            method: Extraction method ('tfidf', 'rake', 'yake', 'all')
            **kwargs: Additional parameters for specific methods
            
        Returns:
            Dictionary with extracted keywords and metadata
        """
        if not texts or all(not text or pd.isna(text) for text in texts):
            return {'keywords': [], 'method': method, 'metadata': {}}
        
        # Clean texts
        cleaned_texts = [self._preprocess_text(text) for text in texts if text and not pd.isna(text)]
        
        if method == 'all':
            # Extract using all available methods
            results = {}
            for m in ['tfidf', 'rake', 'yake']:
                if self._is_method_available(m):
                    results[m] = self.extract_nlp_keywords(cleaned_texts, method=m, **kwargs)
            return results
        
        if method == 'tfidf':
            return self._extract_tfidf_keywords(cleaned_texts, **kwargs)
        elif method == 'rake' and self.rake is not None:
            return self._extract_rake_keywords(cleaned_texts, **kwargs)
        elif method == 'yake' and self.yake_extractor is not None:
            return self._extract_yake_keywords(cleaned_texts, **kwargs)
        else:
            self.logger.warning(f"Method '{method}' not available or not implemented")
            return {'keywords': [], 'method': method, 'metadata': {'error': 'Method not available'}}
    
    def _extract_tfidf_keywords(self, texts: List[str], top_n: Optional[int] = None, **kwargs) -> Dict[str, Any]:
        """Extract keywords using TF-IDF"""
        try:
            if not texts:
                return {'keywords': [], 'method': 'tfidf', 'metadata': {}}
            
            # Fit TF-IDF
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
            feature_names = self.tfidf_vectorizer.get_feature_names_out()
            
            # Calculate mean TF-IDF scores across all documents
            mean_scores = np.array(tfidf_matrix.mean(axis=0)).flatten()
            
            # Create keyword-score pairs
            keyword_scores = list(zip(feature_names, mean_scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Get top keywords
            top_n = top_n or self.output_config.get('top_n_keywords', 20)
            top_keywords = keyword_scores[:top_n]
            
            return {
                'keywords': [{'keyword': kw, 'score': float(score)} for kw, score in top_keywords],
                'method': 'tfidf',
                'metadata': {
                    'total_features': len(feature_names),
                    'documents_processed': len(texts),
                    'vocabulary_size': len(self.tfidf_vectorizer.vocabulary_) if hasattr(self.tfidf_vectorizer, 'vocabulary_') else 0,
                    'parameters': {
                        'ngram_range': getattr(self.tfidf_vectorizer, 'ngram_range', (1, 1)),
                        'max_features': getattr(self.tfidf_vectorizer, 'max_features', None),
                        'min_df': getattr(self.tfidf_vectorizer, 'min_df', 1),
                        'max_df': getattr(self.tfidf_vectorizer, 'max_df', 1.0)
                    }
                }
            }
        except Exception as e:
            self.logger.error(f"Error in TF-IDF extraction: {e}")
            return {'keywords': [], 'method': 'tfidf', 'metadata': {'error': str(e)}}
    
    def _extract_rake_keywords(self, texts: List[str], top_n: Optional[int] = None, **kwargs) -> Dict[str, Any]:
        """Extract keywords using RAKE"""
        try:
            if not texts or self.rake is None:
                return {'keywords': [], 'method': 'rake', 'metadata': {}}
            
            all_keywords = []
            
            for text in texts:
                self.rake.extract_keywords_from_text(text)
                keyword_scores = self.rake.get_ranked_phrases_with_scores()
                all_keywords.extend([(phrase, score) for score, phrase in keyword_scores])
            
            # Aggregate scores for duplicate keywords
            keyword_totals = defaultdict(float)
            keyword_counts = defaultdict(int)
            
            for phrase, score in all_keywords:
                keyword_totals[phrase] += score
                keyword_counts[phrase] += 1
            
            # Calculate average scores
            avg_keywords = [(phrase, score / keyword_counts[phrase]) for phrase, score in keyword_totals.items()]
            avg_keywords.sort(key=lambda x: x[1], reverse=True)
            
            # Get top keywords
            top_n = top_n or self.output_config.get('top_n_keywords', 20)
            top_keywords = avg_keywords[:top_n]
            
            return {
                'keywords': [{'keyword': kw, 'score': float(score)} for kw, score in top_keywords],
                'method': 'rake',
                'metadata': {
                    'total_extracted': len(all_keywords),
                    'unique_keywords': len(keyword_totals),
                    'documents_processed': len(texts),
                    'parameters': {
                        'min_length': getattr(self.rake, 'min_length', None),
                        'max_length': getattr(self.rake, 'max_length', None)
                    }
                }
            }
        except Exception as e:
            self.logger.error(f"Error in RAKE extraction: {e}")
            return {'keywords': [], 'method': 'rake', 'metadata': {'error': str(e)}}
    
    def _extract_yake_keywords(self, texts: List[str], top_n: Optional[int] = None, **kwargs) -> Dict[str, Any]:
        """Extract keywords using YAKE"""
        try:
            if not texts or self.yake_extractor is None:
                return {'keywords': [], 'method': 'yake', 'metadata': {}}
            
            all_keywords = []
            
            for text in texts:
                # YAKE returns (score, keyword) tuples, lower score = better
                keywords = self.yake_extractor.extract_keywords(text)
                all_keywords.extend(keywords)
            
            # Aggregate and average scores for duplicate keywords
            keyword_totals = defaultdict(float)
            keyword_counts = defaultdict(int)
            
            for score, keyword in all_keywords:
                keyword_totals[keyword] += score
                keyword_counts[keyword] += 1
            
            # Calculate average scores and sort (lower is better for YAKE)
            avg_keywords = [(keyword, score / keyword_counts[keyword]) for keyword, score in keyword_totals.items()]
            avg_keywords.sort(key=lambda x: x[1])  # Lower scores first
            
            # Get top keywords
            top_n = top_n or self.output_config.get('top_n_keywords', 20)
            top_keywords = avg_keywords[:top_n]
            
            return {
                'keywords': [{'keyword': kw, 'score': float(score)} for kw, score in top_keywords],
                'method': 'yake',
                'metadata': {
                    'total_extracted': len(all_keywords),
                    'unique_keywords': len(keyword_totals),
                    'documents_processed': len(texts),
                    'parameters': {
                        'language': getattr(self.yake_extractor, 'lan', 'en'),
                        'max_ngram_size': getattr(self.yake_extractor, 'n', 3),
                        'deduplication_threshold': getattr(self.yake_extractor, 'dedupLim', 0.7)
                    }
                }
            }
        except Exception as e:
            self.logger.error(f"Error in YAKE extraction: {e}")
            return {'keywords': [], 'method': 'yake', 'metadata': {'error': str(e)}}
    
    def calculate_keyword_frequencies(self, keywords_data: Union[pd.DataFrame, Dict]) -> pd.DataFrame:
        """
        Calculate frequency statistics for extracted keywords
        
        Args:
            keywords_data: Keywords DataFrame or dictionary from extraction methods
            
        Returns:
            DataFrame with keyword frequency statistics
        """
        if isinstance(keywords_data, dict):
            # Convert extraction results to DataFrame
            if 'keywords' in keywords_data:
                keywords_list = keywords_data['keywords']
                if not keywords_list:
                    return pd.DataFrame()
                
                freq_data = []
                for item in keywords_list:
                    freq_data.append({
                        'keyword': item['keyword'],
                        'frequency': 1,  # Individual extraction count
                        'score': item.get('score', 0),
                        'method': keywords_data.get('method', 'unknown')
                    })
                
                freq_df = pd.DataFrame(freq_data)
            else:
                return pd.DataFrame()
        
        elif isinstance(keywords_data, pd.DataFrame):
            # Calculate frequencies from keywords DataFrame
            if 'keyword' not in keywords_data.columns:
                return pd.DataFrame()
            
            freq_counts = keywords_data['keyword'].value_counts()
            freq_df = pd.DataFrame({
                'keyword': freq_counts.index,
                'frequency': freq_counts.values
            })
            
            # Add additional statistics if available
            if 'extraction_method' in keywords_data.columns:
                method_info = keywords_data.groupby('keyword')['extraction_method'].first()
                freq_df['method'] = freq_df['keyword'].map(method_info)
            
            if 'year' in keywords_data.columns:
                # Add temporal frequency information
                year_info = keywords_data.groupby('keyword')['year'].apply(list)
                freq_df['years'] = freq_df['keyword'].map(year_info)
                freq_df['year_span'] = freq_df['years'].apply(lambda x: len(set(x)) if x else 0)
                freq_df['first_year'] = freq_df['years'].apply(lambda x: min(x) if x else None)
                freq_df['last_year'] = freq_df['years'].apply(lambda x: max(x) if x else None)
        
        else:
            return pd.DataFrame()
        
        # Sort by frequency
        if not freq_df.empty:
            freq_df = freq_df.sort_values('frequency', ascending=False).reset_index(drop=True)
            
            # Add relative frequency
            total_keywords = freq_df['frequency'].sum()
            freq_df['relative_frequency'] = freq_df['frequency'] / total_keywords
            
            # Add rank
            freq_df['rank'] = range(1, len(freq_df) + 1)
        
        return freq_df
    
    def analyze_temporal_distribution(self, keywords_df: pd.DataFrame, 
                                    time_granularity: str = 'year') -> pd.DataFrame:
        """
        Analyze keyword frequency distribution over time
        
        Args:
            keywords_df: DataFrame with keywords and temporal information
            time_granularity: Time granularity ('year', 'quarter', 'month')
            
        Returns:
            DataFrame with temporal distribution analysis
        """
        if keywords_df.empty or 'keyword' not in keywords_df.columns:
            return pd.DataFrame()
        
        # Ensure we have temporal information
        if 'year' not in keywords_df.columns:
            if 'publication_date' in keywords_df.columns:
                keywords_df['year'] = keywords_df['publication_date'].apply(self._extract_year_from_date)
            else:
                self.logger.warning("No temporal information available for temporal analysis")
                return pd.DataFrame()
        
        # Remove rows with missing year information
        keywords_df = keywords_df.dropna(subset=['year'])
        
        if time_granularity == 'year':
            time_col = 'year'
        elif time_granularity == 'quarter':
            keywords_df['quarter'] = keywords_df['publication_date'].apply(self._extract_quarter_from_date)
            time_col = 'quarter'
        elif time_granularity == 'month':
            keywords_df['month'] = keywords_df['publication_date'].apply(self._extract_month_from_date)
            time_col = 'month'
        else:
            time_col = 'year'
        
        # Calculate temporal distribution
        temporal_dist = keywords_df.groupby(['keyword', time_col]).size().reset_index(name='count')
        
        # Pivot to get keywords as rows and time periods as columns
        temporal_pivot = temporal_dist.pivot(index='keyword', columns=time_col, values='count').fillna(0)
        
        # Calculate summary statistics
        temporal_stats = []
        for keyword in temporal_pivot.index:
            keyword_data = temporal_pivot.loc[keyword]
            non_zero_periods = keyword_data[keyword_data > 0]
            
            temporal_stats.append({
                'keyword': keyword,
                'total_frequency': keyword_data.sum(),
                'active_periods': len(non_zero_periods),
                'first_appearance': non_zero_periods.index.min() if len(non_zero_periods) > 0 else None,
                'last_appearance': non_zero_periods.index.max() if len(non_zero_periods) > 0 else None,
                'peak_period': non_zero_periods.idxmax() if len(non_zero_periods) > 0 else None,
                'peak_frequency': non_zero_periods.max() if len(non_zero_periods) > 0 else 0,
                'temporal_distribution': keyword_data.to_dict()
            })
        
        temporal_df = pd.DataFrame(temporal_stats)
        temporal_df = temporal_df.sort_values('total_frequency', ascending=False).reset_index(drop=True)
        
        return temporal_df
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for keyword extraction"""
        if not text or pd.isna(text):
            return ""
        
        # Convert to string and lowercase
        text = str(text).lower()
        
        # Remove special characters but keep spaces and hyphens
        text = re.sub(r'[^\w\s\-]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove very short words (less than 3 characters)
        words = text.split()
        words = [word for word in words if len(word) >= 3]
        
        return ' '.join(words)
    
    def _clean_keyword(self, keyword: str) -> str:
        """Clean and normalize a keyword"""
        if not keyword or pd.isna(keyword):
            return ""
        
        # Convert to string and strip
        keyword = str(keyword).strip()
        
        # Remove special characters at start and end
        keyword = re.sub(r'^[^\w]+|[^\w]+$', '', keyword)
        
        # Convert to lowercase
        keyword = keyword.lower()
        
        # Remove extra whitespace
        keyword = re.sub(r'\s+', ' ', keyword).strip()
        
        return keyword
    
    def _extract_year_from_date(self, date_str: Union[str, int]) -> Optional[int]:
        """Extract year from various date formats"""
        if pd.isna(date_str):
            return None
        
        try:
            # If already an integer year
            if isinstance(date_str, int):
                if 1900 <= date_str <= 2030:  # Reasonable year range
                    return date_str
                else:
                    return None
            
            # Convert to string
            date_str = str(date_str).strip()
            
            # Extract 4-digit year using regex
            year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
            if year_match:
                return int(year_match.group())
            
            # Try to extract just first 4 digits if they look like a year
            if len(date_str) >= 4 and date_str[:4].isdigit():
                year = int(date_str[:4])
                if 1900 <= year <= 2030:
                    return year
            
            return None
        except (ValueError, TypeError):
            return None
    
    def _extract_quarter_from_date(self, date_str: Union[str, int]) -> Optional[str]:
        """Extract quarter from date string"""
        year = self._extract_year_from_date(date_str)
        if not year:
            return None
        
        try:
            date_str = str(date_str)
            # Simple month extraction for quarter calculation
            month_match = re.search(r'-(\d{1,2})-', date_str)
            if month_match:
                month = int(month_match.group(1))
                quarter = (month - 1) // 3 + 1
                return f"{year}Q{quarter}"
            else:
                return f"{year}Q1"  # Default to Q1 if month not found
        except (ValueError, TypeError):
            return f"{year}Q1"
    
    def _extract_month_from_date(self, date_str: Union[str, int]) -> Optional[str]:
        """Extract year-month from date string"""
        year = self._extract_year_from_date(date_str)
        if not year:
            return None
        
        try:
            date_str = str(date_str)
            month_match = re.search(r'-(\d{1,2})-', date_str)
            if month_match:
                month = int(month_match.group(1))
                return f"{year}-{month:02d}"
            else:
                return f"{year}-01"  # Default to January if month not found
        except (ValueError, TypeError):
            return f"{year}-01"
    
    def _is_method_available(self, method: str) -> bool:
        """Check if a keyword extraction method is available"""
        if method == 'tfidf':
            return True
        elif method == 'rake':
            return self.rake is not None
        elif method == 'yake':
            return self.yake_extractor is not None
        else:
            return False

    def export_keywords(self, keywords_df: pd.DataFrame, 
                       output_path: str, 
                       format: str = 'csv') -> bool:
        """
        Export keywords to file
        
        Args:
            keywords_df: Keywords DataFrame to export
            output_path: Output file path
            format: Export format ('csv', 'json', 'excel')
            
        Returns:
            Success boolean
        """
        try:
            if keywords_df.empty:
                self.logger.warning("Empty DataFrame, nothing to export")
                return False
            
            if format.lower() == 'csv':
                keywords_df.to_csv(output_path, index=False)
            elif format.lower() == 'json':
                keywords_df.to_json(output_path, orient='records', indent=2)
            elif format.lower() in ['excel', 'xlsx']:
                keywords_df.to_excel(output_path, index=False)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            self.logger.info(f"Keywords exported to {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting keywords: {e}")
            return False
