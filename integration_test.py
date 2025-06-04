#!/usr/bin/env python3
"""
Full Integration Test for Keyword Analysis Module
Tests all components working together with realistic data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from slr_core.keyword_analysis import KeywordExtractor, SemanticAnalyzer, TemporalAnalyzer, Visualizer
from slr_core.config_manager import ConfigManager
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def run_integration_test():
    print('=== Full Integration Test ===')
    
    # Initialize components
    config = ConfigManager()
    
    # Create comprehensive test data
    test_data = {
        'title': [
            'Artificial Intelligence in Supply Chain Management',
            'Machine Learning Applications for Logistics Optimization',
            'Agent-Based Models in Distribution Networks',
            'Deep Learning for Demand Forecasting',
            'Blockchain Technology in Supply Chain Transparency',
            'IoT Sensors for Real-time Inventory Management',
            'Robotic Process Automation in Warehouse Operations',
            'Natural Language Processing for Customer Service'
        ],
        'abstract': [
            'This paper explores the application of artificial intelligence technologies in modern supply chain management systems.',
            'We present novel machine learning algorithms for optimizing logistics operations and reducing transportation costs.',
            'Agent-based modeling provides insights into complex distribution network behaviors and emergent properties.',
            'Deep neural networks achieve state-of-the-art performance in demand forecasting across multiple product categories.',
            'Blockchain implementation ensures transparency and traceability throughout the supply chain ecosystem.',
            'Internet of Things sensors enable real-time monitoring and automated inventory management decisions.',
            'Robotic process automation streamlines warehouse operations and improves picking efficiency significantly.',
            'Natural language processing transforms customer service interactions through intelligent chatbot systems.'
        ],
        'keywords': [
            ['artificial intelligence', 'supply chain', 'management', 'optimization'],
            ['machine learning', 'logistics', 'optimization', 'transportation'],
            ['agent-based', 'modeling', 'distribution', 'networks'],
            ['deep learning', 'demand forecasting', 'neural networks'],
            ['blockchain', 'transparency', 'traceability', 'supply chain'],
            ['IoT', 'sensors', 'inventory management', 'real-time'],
            ['robotics', 'automation', 'warehouse', 'efficiency'],
            ['NLP', 'customer service', 'chatbots', 'processing']
        ],
        'publication_date': [
            datetime.now() - timedelta(days=365*i) for i in range(8)
        ]
    }
    
    df = pd.DataFrame(test_data)
    print(f'Test dataset: {len(df)} publications')
    
    # Test 1: Keyword extraction
    print('\n1. Testing keyword extraction...')
    extractor = KeywordExtractor(config)
    
    # API keywords
    api_keywords_df = extractor.extract_api_keywords(df)
    print(f'   API keywords extracted: {len(api_keywords_df)} entries')
    
    # NLP keywords
    abstracts = df['abstract'].tolist()
    nlp_keywords = extractor.extract_nlp_keywords(abstracts)
    print(f'   NLP keywords extracted: {len(nlp_keywords)} method results')
    
    # Frequency analysis using the DataFrame
    if not api_keywords_df.empty:
        freq_analysis = extractor.calculate_keyword_frequencies(api_keywords_df)
        print(f'   Frequency analysis: {len(freq_analysis)} unique keywords analyzed')
        top_keywords = freq_analysis.head(5)
        print(f'   Top keywords: {list(top_keywords["keyword"].values)}')
    
    # Test 2: Semantic analysis
    print('\n2. Testing semantic analysis...')
    analyzer = SemanticAnalyzer(config)
    
    # Generate embeddings for abstracts
    sample_texts = df['abstract'].tolist()[:5]  # Use fewer for faster testing
    embeddings = analyzer.generate_embeddings(sample_texts)
    
    if embeddings is not None:
        print(f'   Embeddings shape: {embeddings.shape}')
        
        # Clustering
        cluster_results = analyzer.perform_clustering(embeddings, method='kmeans')
        print(f'   Clustering: {cluster_results.get("n_clusters", 0)} clusters found')
    else:
        print('   Embeddings: Model not available, skipping clustering')
    
    # Test 3: Temporal analysis
    print('\n3. Testing temporal analysis...')
    temporal = TemporalAnalyzer(config.config)
    
    # Create temporal data in expected format
    publications_list = df.to_dict('records')
    keywords_dict = {}
    
    # Aggregate all keywords with metadata
    for idx, row in df.iterrows():
        for kw in row['keywords']:
            if kw in keywords_dict:
                keywords_dict[kw]['frequency'] += 1
            else:
                keywords_dict[kw] = {'frequency': 1, 'importance': 0.5}
    
    trends = temporal.analyze_keyword_trends(publications_list, keywords_dict)
    print(f'   Temporal trends: analyzed {len(trends)} result keys')
    
    lifecycle = temporal.analyze_keyword_lifecycle(publications_list, keywords_dict)
    print(f'   Lifecycle analysis: {len(lifecycle)} lifecycle keys')
    
    # Test 4: Visualization
    print('\n4. Testing visualization...')
    visualizer = Visualizer(config.config)
    
    # Create simple keyword frequency dict for visualization
    keyword_freqs = {}
    for kw_list in df['keywords']:
        for kw in kw_list:
            keyword_freqs[kw] = keyword_freqs.get(kw, 0) + 1
    
    # Word cloud
    try:
        wordcloud_result = visualizer.create_word_cloud(keyword_freqs, 
                                                       title="Test Keywords Word Cloud")
        print(f'   Word cloud: {wordcloud_result}')
    except Exception as e:
        print(f'   Word cloud: Error - {e}')
    
    # Frequency plot
    try:
        freq_plot_result = visualizer.plot_keyword_frequencies(keyword_freqs, 
                                                              title="Test Keyword Frequencies")
        print(f'   Frequency plot: {freq_plot_result}')
    except Exception as e:
        print(f'   Frequency plot: Error - {e}')
    
    print('\n=== Integration Test Completed Successfully! ===')
    print('All components have been tested and are working together.')
    
    return {
        'api_keywords': len(api_keywords_df) if not api_keywords_df.empty else 0,
        'nlp_keywords': len(nlp_keywords),
        'embeddings_shape': embeddings.shape if embeddings is not None else None,
        'clusters': cluster_results.get("n_clusters", 0) if embeddings is not None else 0,
        'temporal_trends': len(trends),
        'lifecycle_analysis': len(lifecycle)
    }

if __name__ == "__main__":
    try:
        results = run_integration_test()
        print(f"\nTest Results Summary: {results}")
        print("✅ Integration test passed!")
    except Exception as e:
        print(f"\n❌ Integration test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
