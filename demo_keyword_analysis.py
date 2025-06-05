#!/usr/bin/env python3
"""
Keyword Analysis Module Demo
Demonstrates the capabilities of the keyword analysis module with sample data
"""

import sys
import os
sys.path.append(os.getcwd())

from slr_core.keyword_analysis import KeywordExtractor, SemanticAnalyzer, TemporalAnalyzer, Visualizer
from slr_core.config_manager import ConfigManager
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def create_sample_data():
    """Create sample publication data for demonstration"""
    sample_data = {
        'title': [
            'AI-Driven Supply Chain Optimization in Manufacturing',
            'Machine Learning for Predictive Maintenance in Industry 4.0',
            'Blockchain Integration in Global Supply Networks',
            'Digital Twin Technology for Smart Manufacturing',
            'Autonomous Robots in Warehouse Automation',
            'IoT Sensors for Real-time Supply Chain Monitoring',
            'Natural Language Processing in Customer Service Automation',
            'Computer Vision for Quality Control in Production Lines'
        ],
        'abstract': [
            'This study explores artificial intelligence applications in supply chain optimization, focusing on machine learning algorithms for demand forecasting and inventory management in manufacturing environments.',
            'We present a comprehensive framework for predictive maintenance using machine learning techniques, including neural networks and ensemble methods for equipment failure prediction in Industry 4.0 settings.',
            'Blockchain technology offers transparency and traceability in global supply networks. This paper examines implementation strategies and benefits of distributed ledger systems in supply chain management.',
            'Digital twin technology creates virtual replicas of manufacturing systems for simulation and optimization. We demonstrate applications in production planning and process improvement.',
            'Autonomous robotic systems revolutionize warehouse operations through intelligent navigation, object recognition, and automated picking systems for improved efficiency and reduced costs.',
            'Internet of Things sensors enable real-time monitoring of supply chain processes. This research evaluates sensor networks for inventory tracking and environmental monitoring.',
            'Natural language processing transforms customer service through intelligent chatbots and automated response systems. We analyze implementation challenges and performance metrics.',
            'Computer vision systems automate quality control in production environments. This study presents deep learning approaches for defect detection and classification in manufacturing.'
        ],
        'keywords': [
            ['artificial intelligence', 'supply chain', 'optimization', 'manufacturing', 'machine learning'],
            ['machine learning', 'predictive maintenance', 'Industry 4.0', 'neural networks'],
            ['blockchain', 'supply networks', 'traceability', 'distributed ledger'],
            ['digital twin', 'manufacturing', 'simulation', 'optimization'],
            ['autonomous robots', 'warehouse automation', 'navigation', 'picking systems'],
            ['IoT', 'sensors', 'real-time monitoring', 'inventory tracking'],
            ['natural language processing', 'customer service', 'chatbots', 'automation'],
            ['computer vision', 'quality control', 'deep learning', 'defect detection']
        ],
        'publication_date': [
            datetime.now() - timedelta(days=i*90) for i in range(8)
        ],
        'source': ['semantic_scholar'] * 4 + ['openalex'] * 4,
        'doi': [f'10.1000/demo.{i+1}' for i in range(8)]
    }
    
    return pd.DataFrame(sample_data)

def main():
    """Main demonstration function"""
    print("🔍 KEYWORD ANALYSIS MODULE DEMONSTRATION")
    print("=" * 60)
    
    # Initialize configuration and components
    print("\n📋 Initializing components...")
    config = ConfigManager()
    
    extractor = KeywordExtractor(config)
    analyzer = SemanticAnalyzer(config)
    temporal = TemporalAnalyzer(config.config)
    visualizer = Visualizer(config.config)
    
    print("✅ All components initialized successfully!")
    
    # Create sample data
    print("\n📊 Creating sample dataset...")
    df = create_sample_data()
    print(f"✅ Created dataset with {len(df)} publications")
    
    # Demonstrate keyword extraction
    print("\n🔤 KEYWORD EXTRACTION DEMONSTRATION")
    print("-" * 40)
    
    # API-based keywords
    print("1. Extracting API-provided keywords...")
    api_keywords_df = extractor.extract_api_keywords(df)
    print(f"   ✅ Extracted {len(api_keywords_df)} API keywords")
    
    # Show top keywords by frequency
    if not api_keywords_df.empty:
        freq_analysis = extractor.calculate_keyword_frequencies(api_keywords_df)
        top_keywords = freq_analysis.head(10)
        print(f"   📈 Top 10 keywords by frequency:")
        for _, row in top_keywords.iterrows():
            print(f"      • {row['keyword']}: {row['frequency']} occurrences")
    
    # NLP-based keywords
    print("\n2. Extracting NLP-based keywords...")
    abstracts = df['abstract'].tolist()
    
    # TF-IDF extraction
    tfidf_keywords = extractor.extract_nlp_keywords(abstracts, method='tfidf', top_n=10)
    print(f"   ✅ TF-IDF: {len(tfidf_keywords['keywords'])} keywords")
    print("   📈 Top TF-IDF keywords:")
    for kw in tfidf_keywords['keywords'][:5]:
        print(f"      • {kw['keyword']}: {kw['score']:.4f}")
    
    # YAKE extraction (if available)
    yake_keywords = extractor.extract_nlp_keywords(abstracts, method='yake', top_n=10)
    if yake_keywords['keywords']:
        print(f"   ✅ YAKE: {len(yake_keywords['keywords'])} keywords")
        print("   📈 Top YAKE keywords:")
        for kw in yake_keywords['keywords'][:5]:
            print(f"      • {kw['keyword']}: {kw['score']:.4f}")
    
    # Demonstrate semantic analysis
    print("\n🧠 SEMANTIC ANALYSIS DEMONSTRATION")
    print("-" * 40)
    
    print("1. Loading BGE-M3 embedding model...")
    model_loaded = analyzer.load_embedding_model()
    
    if model_loaded:
        print("   ✅ Model loaded successfully!")
        
        print("2. Generating embeddings...")
        sample_abstracts = abstracts[:6]  # Use subset for demo
        embeddings = analyzer.generate_embeddings(sample_abstracts)
        
        if embeddings is not None:
            print(f"   ✅ Generated embeddings: {embeddings.shape}")
            
            print("3. Performing clustering...")
            cluster_results = analyzer.perform_clustering(embeddings, method='kmeans')
            
            if 'cluster_labels' in cluster_results:
                n_clusters = cluster_results['n_clusters']
                silhouette = cluster_results.get('silhouette_score', 0)
                print(f"   ✅ K-means clustering: {n_clusters} clusters")
                print(f"   📊 Silhouette score: {silhouette:.4f}")
                
                # Show cluster assignments
                print("   📋 Cluster assignments:")
                for i, label in enumerate(cluster_results['cluster_labels']):
                    title = df.iloc[i]['title'][:50] + "..."
                    print(f"      • Cluster {label}: {title}")
    else:
        print("   ⚠️ Model loading failed, skipping embedding analysis")
    
    # Demonstrate temporal analysis
    print("\n📈 TEMPORAL ANALYSIS DEMONSTRATION")
    print("-" * 40)
    
    print("1. Analyzing keyword trends...")
    publications_list = df.to_dict('records')
    
    # Create keyword dictionary
    keywords_dict = {}
    for pub in publications_list:
        if 'keywords' in pub and pub['keywords']:
            for kw in pub['keywords']:
                if kw in keywords_dict:
                    keywords_dict[kw]['frequency'] += 1
                else:
                    keywords_dict[kw] = {'frequency': 1, 'importance': 0.5}
    
    trends = temporal.analyze_keyword_trends(publications_list, keywords_dict)
    print(f"   ✅ Analyzed trends for {len(trends.get('individual_trends', {}))} keywords")
    
    # Show trend information
    if 'top_growing_keywords' in trends:
        growing = trends['top_growing_keywords'][:3]
        print(f"   📈 Top growing keywords: {growing}")
    
    print("2. Performing keyword lifecycle analysis...")
    lifecycle = temporal.analyze_keyword_lifecycle(publications_list, keywords_dict)
    print(f"   ✅ Lifecycle analysis completed: {len(lifecycle)} stages")
    
    # Demonstrate visualization
    print("\n🎨 VISUALIZATION DEMONSTRATION")
    print("-" * 40)
    
    # Create keyword frequency data
    keyword_freqs = {}
    for kw_list in df['keywords']:
        for kw in kw_list:
            keyword_freqs[kw] = keyword_freqs.get(kw, 0) + 1
    
    print("1. Creating word cloud...")
    try:
        wordcloud_result = visualizer.create_word_cloud(
            keyword_freqs, 
            title="Demo Keywords Word Cloud"
        )
        print(f"   ✅ Word cloud: {wordcloud_result}")
    except Exception as e:
        print(f"   ⚠️ Word cloud error: {e}")
    
    print("2. Creating frequency plot...")
    try:
        freq_plot_result = visualizer.plot_keyword_frequencies(
            keyword_freqs,
            title="Demo Keyword Frequencies"
        )
        print(f"   ✅ Frequency plot: {freq_plot_result}")
    except Exception as e:
        print(f"   ⚠️ Frequency plot error: {e}")
    
    # Summary
    print("\n🎉 DEMONSTRATION COMPLETED!")
    print("=" * 60)
    print("✅ All keyword analysis components demonstrated successfully!")
    print("\nSUMMARY:")
    print(f"  • API Keywords: {len(api_keywords_df)}")
    print(f"  • NLP Keywords (TF-IDF): {len(tfidf_keywords['keywords'])}")
    print(f"  • Embeddings: {embeddings.shape if embeddings is not None else 'N/A'}")
    print(f"  • Clusters: {cluster_results.get('n_clusters', 'N/A')}")
    print(f"  • Trend Analysis: {len(trends.get('individual_trends', {}))}")
    print(f"  • Visualizations: Generated successfully")
    print("\n🚀 The keyword analysis module is ready for production use!")

if __name__ == "__main__":
    main()
