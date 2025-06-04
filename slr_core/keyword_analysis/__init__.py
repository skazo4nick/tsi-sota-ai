"""
Keyword Analysis Module for Research Analytics Application

This module provides comprehensive keyword analysis capabilities for the
"Agentic AI in SCM" Systematic Literature Review, including:

- API-based keyword extraction from publication metadata
- NLP-based keyword/keyphrase extraction using TF-IDF, RAKE, and YAKE
- Semantic analysis using BGE-M3 embeddings
- Temporal trend analysis and visualization
- Clustering and thematic analysis

Components:
    - KeywordExtractor: Extract keywords from text and API data
    - SemanticAnalyzer: BGE-M3 embeddings and clustering
    - TemporalAnalyzer: Time-series analysis and trend tracking
    - Visualizer: Plotting and export functionality
"""

from .keyword_extractor import KeywordExtractor
from .semantic_analyzer import SemanticAnalyzer
from .temporal_analyzer import TemporalAnalyzer
from .visualizer import Visualizer

__version__ = "1.0.0"
__author__ = "TSI-SOTA-AI Research Team"

__all__ = [
    "KeywordExtractor",
    "SemanticAnalyzer", 
    "TemporalAnalyzer",
    "Visualizer"
]
