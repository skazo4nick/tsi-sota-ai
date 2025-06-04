"""
SemanticAnalyzer: Semantic embedding and clustering analysis

This module handles:
1. BGE-M3 embedding generation for abstracts and text
2. Semantic clustering using K-means and DBSCAN
3. Dimensionality reduction for visualization
4. Cluster analysis and interpretation
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Union, Tuple
import logging
import os
import pickle
from pathlib import Path

# Machine learning libraries
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.preprocessing import StandardScaler

# Sentence transformers for BGE-M3
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    SentenceTransformer = None

# UMAP for dimensionality reduction
try:
    import umap
    UMAP_AVAILABLE = True
except ImportError:
    UMAP_AVAILABLE = False
    umap = None

# Configuration
from ..config_manager import ConfigManager

class SemanticAnalyzer:
    """
    Semantic analysis using BGE-M3 embeddings and clustering
    
    Features:
    - BGE-M3 model loading and embedding generation
    - K-means and DBSCAN clustering
    - PCA and UMAP dimensionality reduction
    - Cluster quality metrics and analysis
    - Embedding caching for performance
    """
    
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        """
        Initialize SemanticAnalyzer with configuration
        
        Args:
            config_manager: ConfigManager instance for settings
        """
        self.config = config_manager or ConfigManager()
        self.logger = logging.getLogger(__name__)
        
        # Get configuration settings
        self.semantic_config = self.config.get('semantic_analysis', {})
        self.embedding_config = self.semantic_config.get('embedding', {})
        self.clustering_config = self.semantic_config.get('clustering', {})
        self.reduction_config = self.semantic_config.get('dimensionality_reduction', {})
        
        # Initialize components
        self.embedding_model = None
        self.embeddings_cache = {}
        self.scaler = StandardScaler()
        
        # Set up cache directory
        self.cache_dir = Path(self.embedding_config.get('cache_dir', './data/embeddings_cache'))
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Check dependencies
        self._check_dependencies()
    
    def _check_dependencies(self):
        """Check if required dependencies are available"""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            self.logger.warning("sentence-transformers not available. BGE-M3 functionality will be limited.")
        
        if not UMAP_AVAILABLE:
            self.logger.warning("umap-learn not available. UMAP dimensionality reduction will not be available.")
    
    def load_embedding_model(self, model_name: Optional[str] = None) -> bool:
        """
        Load the BGE-M3 embedding model
        
        Args:
            model_name: Model name/path, defaults to config setting
            
        Returns:
            Success boolean
        """
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            self.logger.error("sentence-transformers package not available")
            return False
        
        try:
            model_name = model_name or self.embedding_config.get('model_name', 'BAAI/bge-m3')
            device = self.embedding_config.get('device', 'cpu')
            
            self.logger.info(f"Loading embedding model: {model_name}")
            
            # Load model with configuration
            self.embedding_model = SentenceTransformer(
                model_name,
                device=device,
                cache_folder=str(self.cache_dir / 'models')
            )
            
            # Set maximum sequence length
            max_length = self.embedding_config.get('max_length', 512)
            if hasattr(self.embedding_model, 'max_seq_length'):
                self.embedding_model.max_seq_length = max_length
            
            self.logger.info(f"Successfully loaded model {model_name} on device {device}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading embedding model: {e}")
            return False
    
    def generate_embeddings(self, 
                          texts: List[str], 
                          use_cache: bool = True,
                          cache_key: Optional[str] = None) -> Optional[np.ndarray]:
        """
        Generate embeddings for text documents
        
        Args:
            texts: List of text documents
            use_cache: Whether to use embedding cache
            cache_key: Cache key for storing/retrieving embeddings
            
        Returns:
            Numpy array of embeddings or None if failed
        """
        if not texts:
            self.logger.warning("No texts provided for embedding generation")
            return None
        
        # Clean texts
        cleaned_texts = [self._preprocess_text_for_embedding(text) for text in texts]
        cleaned_texts = [text for text in cleaned_texts if text.strip()]
        
        if not cleaned_texts:
            self.logger.warning("No valid texts after preprocessing")
            return None
        
        # Check cache first
        if use_cache and cache_key:
            cached_embeddings = self._load_embeddings_from_cache(cache_key)
            if cached_embeddings is not None:
                self.logger.info(f"Loaded embeddings from cache: {cache_key}")
                return cached_embeddings
        
        # Load model if not already loaded
        if self.embedding_model is None:
            if not self.load_embedding_model():
                self.logger.error("Failed to load embedding model")
                return None
        
        try:
            batch_size = self.embedding_config.get('batch_size', 32)
            
            self.logger.info(f"Generating embeddings for {len(cleaned_texts)} texts")
            
            # Generate embeddings in batches
            embeddings = self.embedding_model.encode(
                cleaned_texts,
                batch_size=batch_size,
                show_progress_bar=True,
                convert_to_numpy=True,
                normalize_embeddings=True  # L2 normalize for cosine similarity
            )
            
            # Cache embeddings if requested
            if use_cache and cache_key:
                self._save_embeddings_to_cache(embeddings, cache_key)
            
            self.logger.info(f"Generated embeddings shape: {embeddings.shape}")
            return embeddings
            
        except Exception as e:
            self.logger.error(f"Error generating embeddings: {e}")
            return None
    
    def perform_clustering(self, 
                         embeddings: np.ndarray, 
                         method: str = 'kmeans',
                         **kwargs) -> Dict[str, Any]:
        """
        Perform clustering on embeddings
        
        Args:
            embeddings: Numpy array of embeddings
            method: Clustering method ('kmeans', 'dbscan', 'both')
            **kwargs: Additional parameters for clustering algorithms
            
        Returns:
            Dictionary with clustering results and metadata
        """
        if embeddings is None or embeddings.size == 0:
            return {'labels': [], 'method': method, 'metadata': {'error': 'No embeddings provided'}}
        
        try:
            if method == 'both':
                # Perform both clustering methods
                kmeans_result = self.perform_clustering(embeddings, method='kmeans', **kwargs)
                dbscan_result = self.perform_clustering(embeddings, method='dbscan', **kwargs)
                
                return {
                    'kmeans': kmeans_result,
                    'dbscan': dbscan_result,
                    'method': 'both'
                }
            
            elif method == 'kmeans':
                return self._perform_kmeans_clustering(embeddings, **kwargs)
            
            elif method == 'dbscan':
                return self._perform_dbscan_clustering(embeddings, **kwargs)
            
            else:
                raise ValueError(f"Unknown clustering method: {method}")
                
        except Exception as e:
            self.logger.error(f"Error in clustering: {e}")
            return {'labels': [], 'method': method, 'metadata': {'error': str(e)}}
    
    def _perform_kmeans_clustering(self, embeddings: np.ndarray, **kwargs) -> Dict[str, Any]:
        """Perform K-means clustering"""
        kmeans_config = self.clustering_config.get('kmeans', {})
        
        # Get parameters
        n_clusters = kwargs.get('n_clusters', kmeans_config.get('n_clusters', 10))
        random_state = kwargs.get('random_state', kmeans_config.get('random_state', 42))
        init = kwargs.get('init', kmeans_config.get('init', 'k-means++'))
        max_iter = kwargs.get('max_iter', kmeans_config.get('max_iter', 300))
        
        # Ensure reasonable number of clusters
        n_clusters = min(n_clusters, len(embeddings) - 1)
        
        self.logger.info(f"Performing K-means clustering with {n_clusters} clusters")
        
        # Perform clustering
        kmeans = KMeans(
            n_clusters=n_clusters,
            random_state=random_state,
            init=init,
            max_iter=max_iter,
            n_init=10
        )
        
        labels = kmeans.fit_predict(embeddings)
        
        # Calculate quality metrics
        silhouette = silhouette_score(embeddings, labels) if len(set(labels)) > 1 else -1
        calinski_harabasz = calinski_harabasz_score(embeddings, labels) if len(set(labels)) > 1 else 0
        
        # Calculate cluster statistics
        cluster_stats = self._calculate_cluster_statistics(embeddings, labels)
        
        return {
            'labels': labels.tolist(),
            'method': 'kmeans',
            'model': kmeans,
            'cluster_centers': kmeans.cluster_centers_.tolist(),
            'inertia': float(kmeans.inertia_),
            'silhouette_score': float(silhouette),
            'calinski_harabasz_score': float(calinski_harabasz),
            'n_clusters': n_clusters,
            'cluster_statistics': cluster_stats,
            'metadata': {
                'n_samples': len(embeddings),
                'n_features': embeddings.shape[1],
                'parameters': {
                    'n_clusters': n_clusters,
                    'random_state': random_state,
                    'init': init,
                    'max_iter': max_iter
                }
            }
        }
    
    def _perform_dbscan_clustering(self, embeddings: np.ndarray, **kwargs) -> Dict[str, Any]:
        """Perform DBSCAN clustering"""
        dbscan_config = self.clustering_config.get('dbscan', {})
        
        # Get parameters
        eps = kwargs.get('eps', dbscan_config.get('eps', 0.5))
        min_samples = kwargs.get('min_samples', dbscan_config.get('min_samples', 5))
        metric = kwargs.get('metric', dbscan_config.get('metric', 'cosine'))
        
        self.logger.info(f"Performing DBSCAN clustering with eps={eps}, min_samples={min_samples}")
        
        # Perform clustering
        dbscan = DBSCAN(
            eps=eps,
            min_samples=min_samples,
            metric=metric,
            n_jobs=-1
        )
        
        labels = dbscan.fit_predict(embeddings)
        
        # Calculate metrics (excluding noise points labeled as -1)
        unique_labels = set(labels)
        n_clusters = len(unique_labels) - (1 if -1 in unique_labels else 0)
        n_noise = list(labels).count(-1)
        
        silhouette = silhouette_score(embeddings, labels) if n_clusters > 1 else -1
        calinski_harabasz = calinski_harabasz_score(embeddings, labels) if n_clusters > 1 else 0
        
        # Calculate cluster statistics
        cluster_stats = self._calculate_cluster_statistics(embeddings, labels)
        
        return {
            'labels': labels.tolist(),
            'method': 'dbscan',
            'model': dbscan,
            'n_clusters': n_clusters,
            'n_noise_points': n_noise,
            'silhouette_score': float(silhouette),
            'calinski_harabasz_score': float(calinski_harabasz),
            'cluster_statistics': cluster_stats,
            'metadata': {
                'n_samples': len(embeddings),
                'n_features': embeddings.shape[1],
                'noise_ratio': n_noise / len(embeddings) if len(embeddings) > 0 else 0,
                'parameters': {
                    'eps': eps,
                    'min_samples': min_samples,
                    'metric': metric
                }
            }
        }
    
    def reduce_dimensions(self, 
                         embeddings: np.ndarray, 
                         method: str = 'umap',
                         n_components: int = 2,
                         **kwargs) -> Optional[np.ndarray]:
        """
        Reduce dimensionality of embeddings for visualization
        
        Args:
            embeddings: Input embeddings
            method: Reduction method ('umap', 'pca')
            n_components: Number of output components
            **kwargs: Additional parameters
            
        Returns:
            Reduced embeddings or None if failed
        """
        if embeddings is None or embeddings.size == 0:
            self.logger.warning("No embeddings provided for dimension reduction")
            return None
        
        try:
            if method == 'umap':
                return self._reduce_with_umap(embeddings, n_components, **kwargs)
            elif method == 'pca':
                return self._reduce_with_pca(embeddings, n_components, **kwargs)
            else:
                raise ValueError(f"Unknown dimension reduction method: {method}")
                
        except Exception as e:
            self.logger.error(f"Error in dimension reduction: {e}")
            return None
    
    def _reduce_with_umap(self, embeddings: np.ndarray, n_components: int, **kwargs) -> Optional[np.ndarray]:
        """Reduce dimensions using UMAP"""
        if not UMAP_AVAILABLE:
            self.logger.error("UMAP not available. Install umap-learn package.")
            return None
        
        umap_config = self.reduction_config.get('umap', {})
        
        # Get parameters
        n_neighbors = kwargs.get('n_neighbors', umap_config.get('n_neighbors', 15))
        min_dist = kwargs.get('min_dist', umap_config.get('min_dist', 0.1))
        metric = kwargs.get('metric', umap_config.get('metric', 'cosine'))
        random_state = kwargs.get('random_state', umap_config.get('random_state', 42))
        
        # Ensure n_neighbors is not larger than n_samples
        n_neighbors = min(n_neighbors, len(embeddings) - 1)
        
        self.logger.info(f"Reducing dimensions with UMAP to {n_components} components")
        
        # Create UMAP reducer
        reducer = umap.UMAP(
            n_components=n_components,
            n_neighbors=n_neighbors,
            min_dist=min_dist,
            metric=metric,
            random_state=random_state,
            verbose=False
        )
        
        # Fit and transform
        reduced_embeddings = reducer.fit_transform(embeddings)
        
        self.logger.info(f"UMAP reduction completed. Shape: {reduced_embeddings.shape}")
        return reduced_embeddings
    
    def _reduce_with_pca(self, embeddings: np.ndarray, n_components: int, **kwargs) -> np.ndarray:
        """Reduce dimensions using PCA"""
        pca_config = self.reduction_config.get('pca', {})
        
        # Get parameters
        random_state = kwargs.get('random_state', pca_config.get('random_state', 42))
        
        # Ensure n_components is not larger than min(n_samples, n_features)
        max_components = min(embeddings.shape[0], embeddings.shape[1])
        n_components = min(n_components, max_components)
        
        self.logger.info(f"Reducing dimensions with PCA to {n_components} components")
        
        # Create PCA reducer
        pca = PCA(n_components=n_components, random_state=random_state)
        
        # Fit and transform
        reduced_embeddings = pca.fit_transform(embeddings)
        
        # Log explained variance
        explained_variance_ratio = pca.explained_variance_ratio_.sum()
        self.logger.info(f"PCA reduction completed. Explained variance: {explained_variance_ratio:.3f}")
        
        return reduced_embeddings
    
    def _calculate_cluster_statistics(self, embeddings: np.ndarray, labels: np.ndarray) -> Dict[str, Any]:
        """Calculate statistics for each cluster"""
        cluster_stats = {}
        unique_labels = set(labels)
        
        for label in unique_labels:
            if label == -1:  # Skip noise points in DBSCAN
                continue
                
            cluster_mask = labels == label
            cluster_embeddings = embeddings[cluster_mask]
            
            if len(cluster_embeddings) == 0:
                continue
            
            # Calculate cluster statistics
            centroid = np.mean(cluster_embeddings, axis=0)
            
            # Calculate intra-cluster distances
            distances_to_centroid = np.linalg.norm(cluster_embeddings - centroid, axis=1)
            
            cluster_stats[int(label)] = {
                'size': int(np.sum(cluster_mask)),
                'centroid': centroid.tolist(),
                'mean_distance_to_centroid': float(np.mean(distances_to_centroid)),
                'std_distance_to_centroid': float(np.std(distances_to_centroid)),
                'max_distance_to_centroid': float(np.max(distances_to_centroid)),
                'min_distance_to_centroid': float(np.min(distances_to_centroid))
            }
        
        return cluster_stats
    
    def _preprocess_text_for_embedding(self, text: str) -> str:
        """Preprocess text for embedding generation"""
        if not text or pd.isna(text):
            return ""
        
        # Convert to string and strip
        text = str(text).strip()
        
        # Remove excessive whitespace
        import re
        text = re.sub(r'\s+', ' ', text)
        
        # Truncate if too long (BGE-M3 has token limits)
        max_length = self.embedding_config.get('max_length', 512)
        
        # Rough estimation: 1 token ≈ 4 characters
        max_chars = max_length * 4
        if len(text) > max_chars:
            text = text[:max_chars]
        
        return text
    
    def _load_embeddings_from_cache(self, cache_key: str) -> Optional[np.ndarray]:
        """Load embeddings from cache file"""
        try:
            cache_file = self.cache_dir / f"{cache_key}.pkl"
            if cache_file.exists():
                with open(cache_file, 'rb') as f:
                    embeddings = pickle.load(f)
                return embeddings
        except Exception as e:
            self.logger.warning(f"Error loading embeddings from cache: {e}")
        
        return None
    
    def _save_embeddings_to_cache(self, embeddings: np.ndarray, cache_key: str) -> bool:
        """Save embeddings to cache file"""
        try:
            cache_file = self.cache_dir / f"{cache_key}.pkl"
            with open(cache_file, 'wb') as f:
                pickle.dump(embeddings, f)
            
            self.logger.info(f"Saved embeddings to cache: {cache_key}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving embeddings to cache: {e}")
            return False
    
    def analyze_cluster_topics(self, 
                             publications_df: pd.DataFrame, 
                             cluster_labels: List[int],
                             keywords_df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """
        Analyze topics and characteristics of each cluster
        
        Args:
            publications_df: DataFrame with publication data
            cluster_labels: Cluster assignment for each publication
            keywords_df: Optional keywords DataFrame for topic analysis
            
        Returns:
            Dictionary with cluster topic analysis
        """
        if len(publications_df) != len(cluster_labels):
            self.logger.error("Mismatch between publications and cluster labels length")
            return {}
        
        cluster_analysis = {}
        
        # Add cluster labels to publications
        publications_with_clusters = publications_df.copy()
        publications_with_clusters['cluster'] = cluster_labels
        
        # Analyze each cluster
        for cluster_id in set(cluster_labels):
            if cluster_id == -1:  # Skip noise cluster
                continue
                
            cluster_pubs = publications_with_clusters[publications_with_clusters['cluster'] == cluster_id]
            
            if cluster_pubs.empty:
                continue
            
            # Basic statistics
            cluster_info = {
                'cluster_id': cluster_id,
                'size': len(cluster_pubs),
                'percentage': len(cluster_pubs) / len(publications_df) * 100,
                'publications': cluster_pubs[['title', 'doi', 'publication_date']].to_dict('records')
            }
            
            # Temporal analysis
            if 'publication_date' in cluster_pubs.columns:
                years = cluster_pubs['publication_date'].apply(self._extract_year_from_date).dropna()
                if not years.empty:
                    cluster_info['temporal_span'] = {
                        'first_year': int(years.min()),
                        'last_year': int(years.max()),
                        'year_distribution': years.value_counts().to_dict()
                    }
            
            # Source analysis
            if 'source' in cluster_pubs.columns:
                source_dist = cluster_pubs['source'].value_counts()
                cluster_info['source_distribution'] = source_dist.to_dict()
            
            # Keywords analysis for this cluster
            if keywords_df is not None and 'publication_id' in keywords_df.columns:
                cluster_pub_ids = cluster_pubs.index.tolist()
                cluster_keywords = keywords_df[keywords_df['publication_id'].isin(cluster_pub_ids)]
                
                if not cluster_keywords.empty:
                    top_keywords = cluster_keywords['keyword'].value_counts().head(10)
                    cluster_info['top_keywords'] = top_keywords.to_dict()
            
            # Abstract analysis (if available)
            if 'abstract' in cluster_pubs.columns:
                abstracts = cluster_pubs['abstract'].dropna()
                if not abstracts.empty:
                    # Simple word frequency analysis
                    all_text = ' '.join(abstracts.astype(str))
                    words = all_text.lower().split()
                    word_freq = Counter(words)
                    
                    # Filter out common words
                    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'}
                    filtered_words = {word: count for word, count in word_freq.items() 
                                    if word not in common_words and len(word) > 3}
                    
                    top_words = dict(Counter(filtered_words).most_common(10))
                    cluster_info['top_abstract_words'] = top_words
            
            cluster_analysis[cluster_id] = cluster_info
        
        return cluster_analysis
    
    def _extract_year_from_date(self, date_str: Union[str, int]) -> Optional[int]:
        """Extract year from date string - same as in KeywordExtractor"""
        if pd.isna(date_str):
            return None
        
        try:
            if isinstance(date_str, int):
                if 1900 <= date_str <= 2030:
                    return date_str
                else:
                    return None
            
            date_str = str(date_str).strip()
            
            import re
            year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
            if year_match:
                return int(year_match.group())
            
            if len(date_str) >= 4 and date_str[:4].isdigit():
                year = int(date_str[:4])
                if 1900 <= year <= 2030:
                    return year
            
            return None
        except (ValueError, TypeError):
            return None
