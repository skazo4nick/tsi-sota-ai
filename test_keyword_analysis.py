#!/usr/bin/env python3
"""
Quick test script for the Keyword Analysis Module
Tests all main components to ensure they work correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from slr_core.keyword_analysis import KeywordExtractor, SemanticAnalyzer, TemporalAnalyzer, Visualizer
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def create_test_data():
    """Create sample publication data for testing"""
    test_data = [
        {
            'title': 'Machine Learning Applications in Supply Chain Management',
            'abstract': 'This paper explores the use of machine learning algorithms in optimizing supply chain operations.',
            'keywords': ['machine learning', 'supply chain', 'optimization'],
            'publication_date': '2023-01-15',
            'authors': ['Smith, J.', 'Johnson, M.']
        },
        {
            'title': 'AI-Driven Logistics Optimization',
            'abstract': 'Artificial intelligence methods for improving logistics efficiency and reducing costs.',
            'keywords': ['artificial intelligence', 'logistics', 'optimization'],
            'publication_date': '2023-06-20',
            'authors': ['Brown, A.', 'Davis, K.']
        },
        {
            'title': 'Deep Learning for Demand Forecasting',
            'abstract': 'Using deep neural networks to predict customer demand in retail supply chains.',
            'keywords': ['deep learning', 'demand forecasting', 'neural networks'],
            'publication_date': '2024-02-10',
            'authors': ['Wilson, R.', 'Taylor, S.']
        }
    ]
    return pd.DataFrame(test_data)

def test_keyword_extractor():
    """Test the KeywordExtractor component"""
    print("Testing KeywordExtractor...")
    
    # Load configuration
    from slr_core.config_manager import ConfigManager
    config = ConfigManager()
    
    # Create extractor
    extractor = KeywordExtractor(config)
    
    # Create test data
    df = create_test_data()
    
    # Test API keyword extraction
    print("  - Testing API keyword extraction...")
    api_keywords_df = extractor.extract_api_keywords(df)
    print(f"    Found {len(api_keywords_df)} API keyword entries")
    
    # Extract list of keyword strings from DataFrame
    api_keywords_list = []
    if not api_keywords_df.empty and 'keyword' in api_keywords_df.columns:
        api_keywords_list = api_keywords_df['keyword'].tolist()
    
    print(f"    Extracted {len(api_keywords_list)} unique API keywords")
    
    # Test NLP keyword extraction
    print("  - Testing NLP keyword extraction...")
    text_data = " ".join(df['title'] + " " + df['abstract'])
    nlp_keywords = extractor.extract_nlp_keywords([text_data])  # Pass as list
    print(f"    Found {len(nlp_keywords)} NLP keyword result keys")
    
    # Extract keyword lists from the result
    nlp_keyword_list = []
    if isinstance(nlp_keywords, dict):
        for method_results in nlp_keywords.values():
            if isinstance(method_results, dict) and 'keywords' in method_results:
                method_keywords = method_results['keywords']
                if isinstance(method_keywords, list):
                    nlp_keyword_list.extend([kw['keyword'] if isinstance(kw, dict) else str(kw) for kw in method_keywords])
                elif isinstance(method_keywords, dict):
                    nlp_keyword_list.extend(method_keywords.keys())
    
    print(f"    Extracted {len(nlp_keyword_list)} individual keywords")
    
    # Test frequency analysis
    print("  - Testing frequency analysis...")
    all_keywords = api_keywords_list + nlp_keyword_list
    
    # Create a simple DataFrame for frequency analysis
    keyword_data = []
    for kw in all_keywords:
        keyword_data.append({
            'keyword': kw,
            'frequency': 1,
            'extraction_method': 'mixed'
        })
    
    if keyword_data:
        keywords_df = pd.DataFrame(keyword_data)
        frequency_analysis = extractor.calculate_keyword_frequencies(keywords_df)
        print(f"    Analyzed {len(frequency_analysis)} keyword frequencies")
    else:
        print("    No keywords found for frequency analysis")
    
    print("  ✓ KeywordExtractor tests passed\n")
    return all_keywords

def test_semantic_analyzer():
    """Test the SemanticAnalyzer component"""
    print("Testing SemanticAnalyzer...")
    
    # Load configuration
    from slr_core.config_manager import ConfigManager
    config = ConfigManager()
    
    # Create analyzer
    analyzer = SemanticAnalyzer(config)
    
    # Test keywords
    keywords = ['machine learning', 'artificial intelligence', 'deep learning', 'optimization', 'logistics']
    
    print("  - Testing embedding generation...")
    embeddings = analyzer.generate_embeddings(keywords)
    print(f"    Generated embeddings shape: {embeddings.shape if embeddings is not None else 'None'}")
    
    print("  - Testing clustering...")
    cluster_results = analyzer.perform_clustering(embeddings, method='kmeans')
    print(f"    Found {cluster_results.get('n_clusters', 0)} clusters")
    
    print("  ✓ SemanticAnalyzer tests passed\n")
    return cluster_results

def test_temporal_analyzer():
    """Test the TemporalAnalyzer component"""
    print("Testing TemporalAnalyzer...")
    
    # Load configuration
    from slr_core.config_manager import ConfigManager
    config = ConfigManager()
    
    # Create analyzer
    analyzer = TemporalAnalyzer(config.config)
    
    # Create test data
    df = create_test_data()
    
    print("  - Testing temporal trends...")
    # Convert DataFrame to list of dictionaries
    publications_list = df.to_dict('records')
    keywords_dict = {
        'machine learning': {'frequency': 3, 'importance': 0.8},
        'optimization': {'frequency': 2, 'importance': 0.7}
    }
    trends = analyzer.analyze_keyword_trends(publications_list, keywords_dict)
    print(f"    Analyzed trends for {len(trends)} result keys")
    
    print("  - Testing keyword lifecycle...")
    # Convert DataFrame to list of dictionaries
    publications_list = df.to_dict('records')
    keywords_dict = {
        'machine learning': {'frequency': 3, 'importance': 0.8},
        'optimization': {'frequency': 2, 'importance': 0.7}
    }
    lifecycle = analyzer.analyze_keyword_lifecycle(publications_list, keywords_dict)
    print(f"    Analyzed lifecycle for {len(lifecycle)} keywords")
    
    print("  ✓ TemporalAnalyzer tests passed\n")
    return trends

def test_visualizer():
    """Test the Visualizer component"""
    print("Testing Visualizer...")
    
    # Load configuration
    from slr_core.config_manager import ConfigManager
    config = ConfigManager()
    
    # Create visualizer
    visualizer = Visualizer(config.config)
    
    # Test data
    keywords = ['machine learning', 'artificial intelligence', 'optimization', 'logistics']
    frequencies = [10, 8, 6, 4]
    
    print("  - Testing word cloud generation...")
    wordcloud_data = dict(zip(keywords, frequencies))
    wordcloud_fig = visualizer.create_word_cloud(wordcloud_data)
    print("    Word cloud created successfully")
    
    print("  - Testing frequency plot...")
    keywords_dict = dict(zip(keywords, frequencies))
    freq_fig = visualizer.plot_keyword_frequencies(keywords_dict)
    print("    Frequency plot created successfully")
    
    print("  ✓ Visualizer tests passed\n")

def main():
    """Run all tests"""
    print("=== Keyword Analysis Module Test Suite ===\n")
    
    try:
        # Test each component
        keywords = test_keyword_extractor()
        cluster_results = test_semantic_analyzer()
        trends = test_temporal_analyzer()
        test_visualizer()
        
        print("=== All Tests Passed Successfully! ===")
        print("The Keyword Analysis Module is ready to use.")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
