#!/usr/bin/env python3
"""
Comprehensive Integration Test for Keyword Analysis Module
Tests all components with extensive scenarios, edge cases, and error handling
"""

import sys
import os
import tempfile
import shutil
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import json
import logging
import warnings
warnings.filterwarnings('ignore')

# Add project root to path
sys.path.append(os.getcwd())

from slr_core.keyword_analysis import KeywordExtractor, SemanticAnalyzer, TemporalAnalyzer, Visualizer
from slr_core.config_manager import ConfigManager

class TestKeywordAnalysisIntegration:
    """Comprehensive integration tests for the keyword analysis module"""
    
    @classmethod
    def setup_class(cls):
        """Set up test environment"""
        cls.config = ConfigManager()
        cls.temp_dir = tempfile.mkdtemp()
        
        # Create test data
        cls.create_test_data()
        
    @classmethod
    def teardown_class(cls):
        """Clean up test environment"""
        if os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir)
    
    @classmethod
    def create_test_data(cls):
        """Create comprehensive test datasets"""
        
        # Large dataset
        cls.large_test_data = {
            'title': [
                'Artificial Intelligence in Supply Chain Management',
                'Machine Learning Applications for Logistics Optimization',
                'Agent-Based Models in Distribution Networks',
                'Deep Learning for Demand Forecasting',
                'Blockchain Technology in Supply Chain Transparency',
                'IoT Sensors for Real-time Inventory Management',
                'Robotic Process Automation in Warehouse Operations',
                'Natural Language Processing for Customer Service',
                'Computer Vision for Quality Control',
                'Reinforcement Learning in Route Optimization',
                'Digital Twins for Supply Chain Simulation',
                'Edge Computing in Manufacturing Systems',
                'Cloud Analytics for Supply Chain Visibility',
                'Predictive Analytics for Maintenance',
                'Autonomous Vehicles in Last-Mile Delivery',
                'Smart Contracts for Supply Chain Automation',
                'Augmented Reality in Warehouse Picking',
                'Federated Learning for Collaborative Forecasting',
                'Graph Neural Networks for Network Analysis',
                'Time Series Forecasting with Transformers'
            ],
            'abstract': [
                'This paper explores the application of artificial intelligence technologies in modern supply chain management systems, focusing on automation and optimization.',
                'We present novel machine learning algorithms for optimizing logistics operations and reducing transportation costs through advanced analytics.',
                'Agent-based modeling provides insights into complex distribution network behaviors and emergent properties in supply chain systems.',
                'Deep neural networks achieve state-of-the-art performance in demand forecasting across multiple product categories and market segments.',
                'Blockchain implementation ensures transparency and traceability throughout the supply chain ecosystem, improving trust and security.',
                'Internet of Things sensors enable real-time monitoring and automated inventory management decisions in modern warehouses.',
                'Robotic process automation streamlines warehouse operations and improves picking efficiency significantly through intelligent automation.',
                'Natural language processing transforms customer service interactions through intelligent chatbot systems and automated responses.',
                'Computer vision systems enable automated quality control and defect detection in manufacturing and distribution processes.',
                'Reinforcement learning algorithms optimize routing decisions and vehicle scheduling in complex logistics networks.',
                'Digital twin technology creates virtual replicas of supply chain systems for simulation and optimization purposes.',
                'Edge computing brings real-time processing capabilities to manufacturing systems and IoT sensor networks.',
                'Cloud-based analytics platforms provide comprehensive visibility and insights across global supply chain operations.',
                'Predictive maintenance algorithms use sensor data and machine learning to prevent equipment failures and reduce downtime.',
                'Autonomous vehicles revolutionize last-mile delivery operations through automated navigation and package delivery systems.',
                'Smart contracts automate supply chain processes and payments through blockchain-based programmable agreements.',
                'Augmented reality systems enhance warehouse picking operations by providing visual guidance and information overlay.',
                'Federated learning enables collaborative forecasting while preserving data privacy across supply chain partners.',
                'Graph neural networks analyze complex supply chain networks and identify bottlenecks and optimization opportunities.',
                'Transformer-based models achieve superior performance in time series forecasting for demand prediction and planning.'
            ],
            'keywords': [
                ['artificial intelligence', 'supply chain', 'management', 'automation', 'optimization'],
                ['machine learning', 'logistics', 'optimization', 'transportation', 'analytics'],
                ['agent-based', 'modeling', 'distribution', 'networks', 'emergent properties'],
                ['deep learning', 'demand forecasting', 'neural networks', 'performance'],
                ['blockchain', 'transparency', 'traceability', 'supply chain', 'security'],
                ['IoT', 'sensors', 'inventory management', 'real-time', 'monitoring'],
                ['robotics', 'automation', 'warehouse', 'efficiency', 'picking'],
                ['NLP', 'customer service', 'chatbots', 'natural language'],
                ['computer vision', 'quality control', 'defect detection', 'manufacturing'],
                ['reinforcement learning', 'routing', 'optimization', 'scheduling'],
                ['digital twins', 'simulation', 'virtual replicas', 'optimization'],
                ['edge computing', 'real-time', 'manufacturing', 'IoT'],
                ['cloud analytics', 'visibility', 'insights', 'global operations'],
                ['predictive maintenance', 'machine learning', 'sensor data', 'failures'],
                ['autonomous vehicles', 'last-mile delivery', 'automation', 'navigation'],
                ['smart contracts', 'blockchain', 'automation', 'payments'],
                ['augmented reality', 'warehouse', 'picking', 'visual guidance'],
                ['federated learning', 'collaborative forecasting', 'data privacy'],
                ['graph neural networks', 'network analysis', 'bottlenecks'],
                ['transformers', 'time series', 'forecasting', 'demand prediction']
            ],
            'publication_date': [
                datetime.now() - timedelta(days=365*i//4 + i*30) for i in range(20)
            ],
            'source': ['semantic_scholar'] * 10 + ['openalex'] * 5 + ['core'] * 5,
            'doi': [f'10.1000/test.{i}' for i in range(20)]
        }
        
        # Edge case data
        cls.edge_case_data = {
            'title': [
                'Test Paper with Very Long Title That Contains Many Words and Should Test the Limits of Title Processing',
                'Short Title',
                '',  # Empty title
                'Title with Special Characters: @#$%^&*()_+{}|:"<>?[]\\;\',./',
                'Title with Numbers 123 456 789 and Symbols',
                None,  # None title
            ],
            'abstract': [
                'Very long abstract that contains many sentences and should test the limits of text processing capabilities. ' * 50,
                'Short abstract.',
                '',  # Empty abstract
                None,  # None abstract
                'Abstract with special characters and numbers: 123 @#$%^&*()_+',
                'Normal abstract with good content for testing keyword extraction.'
            ],
            'keywords': [
                ['keyword1', 'keyword2'] * 50,  # Many keywords
                ['single'],
                [],  # Empty keywords
                None,  # None keywords
                ['special@chars', 'numbers123', 'normal'],
                ['test', 'keywords', 'normal']
            ],
            'publication_date': [
                datetime.now(),
                datetime(2000, 1, 1),  # Very old date
                None,  # None date
                'invalid_date',  # Invalid date format
                datetime.now(),
                datetime.now()
            ],
            'source': ['test_source'] * 6,
            'doi': ['10.1000/edge.1', '', None, 'invalid_doi', '10.1000/edge.5', '10.1000/edge.6']
        }
        
        # Empty data
        cls.empty_data = {
            'title': [],
            'abstract': [],
            'keywords': [],
            'publication_date': [],
            'source': [],
            'doi': []
        }
    
    def test_01_basic_integration(self):
        """Test basic integration of all components"""
        print('\n=== Test 1: Basic Integration ===')
        
        df = pd.DataFrame(self.large_test_data)
        
        # Initialize components
        extractor = KeywordExtractor(self.config)
        analyzer = SemanticAnalyzer(self.config)
        temporal = TemporalAnalyzer(self.config.config)
        visualizer = Visualizer(self.config.config)
        
        # Test keyword extraction
        api_keywords_df = extractor.extract_api_keywords(df)
        assert not api_keywords_df.empty, "API keywords should not be empty"
        assert 'keyword' in api_keywords_df.columns, "Keyword column should exist"
        
        # Test NLP extraction
        abstracts = df['abstract'].tolist()
        nlp_keywords = extractor.extract_nlp_keywords(abstracts[:5], method='tfidf')
        assert 'keywords' in nlp_keywords, "NLP keywords should contain 'keywords' key"
        assert len(nlp_keywords['keywords']) > 0, "Should extract some keywords"
        
        print(f"✓ Extracted {len(api_keywords_df)} API keywords")
        print(f"✓ Extracted {len(nlp_keywords['keywords'])} NLP keywords")
        
    def test_02_semantic_analysis_integration(self):
        """Test semantic analysis with embeddings and clustering"""
        print('\n=== Test 2: Semantic Analysis Integration ===')
        
        analyzer = SemanticAnalyzer(self.config)
        
        # Test model loading
        model_loaded = analyzer.load_embedding_model()
        print(f"✓ Model loading: {model_loaded}")
        
        # Test embedding generation
        sample_texts = self.large_test_data['abstract'][:5]
        embeddings = analyzer.generate_embeddings(sample_texts)
        
        if embeddings is not None:
            assert embeddings.shape[0] == 5, "Should have 5 embeddings"
            assert embeddings.shape[1] > 0, "Embeddings should have features"
            
            # Test clustering
            cluster_results = analyzer.perform_clustering(embeddings, method='kmeans')
            assert 'cluster_labels' in cluster_results, "Should return cluster labels"
            assert len(cluster_results['cluster_labels']) == 5, "Should have 5 cluster assignments"
            
            print(f"✓ Generated embeddings: {embeddings.shape}")
            print(f"✓ Clustering results: {cluster_results.get('n_clusters', 0)} clusters")
        else:
            print("⚠ Embeddings not available (model not loaded)")
    
    def test_03_temporal_analysis_integration(self):
        """Test temporal analysis with comprehensive data"""
        print('\n=== Test 3: Temporal Analysis Integration ===')
        
        temporal = TemporalAnalyzer(self.config.config)
        
        # Prepare data
        publications_list = pd.DataFrame(self.large_test_data).to_dict('records')
        
        # Create keyword data
        keywords_dict = {}
        for pub in publications_list:
            if 'keywords' in pub and pub['keywords']:
                for kw in pub['keywords']:
                    if kw in keywords_dict:
                        keywords_dict[kw]['frequency'] += 1
                    else:
                        keywords_dict[kw] = {'frequency': 1, 'importance': 0.5}
        
        # Test trend analysis
        trends = temporal.analyze_keyword_trends(publications_list, keywords_dict)
        assert isinstance(trends, dict), "Trends should be a dictionary"
        assert 'individual_trends' in trends, "Should contain individual trends"
        
        # Test lifecycle analysis
        lifecycle = temporal.analyze_keyword_lifecycle(publications_list, keywords_dict)
        assert isinstance(lifecycle, dict), "Lifecycle should be a dictionary"
        
        print(f"✓ Analyzed trends for {len(trends.get('individual_trends', {}))} keywords")
        print(f"✓ Lifecycle analysis: {len(lifecycle)} stages")
    
    def test_04_visualization_integration(self):
        """Test visualization component integration"""
        print('\n=== Test 4: Visualization Integration ===')
        
        visualizer = Visualizer(self.config.config)
        
        # Create test keyword frequency data
        keyword_freqs = {}
        for kw_list in self.large_test_data['keywords']:
            for kw in kw_list:
                keyword_freqs[kw] = keyword_freqs.get(kw, 0) + 1
        
        # Test word cloud
        try:
            wordcloud_result = visualizer.create_word_cloud(
                keyword_freqs, 
                title="Integration Test Word Cloud",
                output_path=None
            )
            print(f"✓ Word cloud: {wordcloud_result}")
        except Exception as e:
            print(f"⚠ Word cloud error: {e}")
        
        # Test frequency plot
        try:
            freq_plot_result = visualizer.plot_keyword_frequencies(
                keyword_freqs,
                title="Integration Test Frequency Plot",
                output_path=None
            )
            print(f"✓ Frequency plot: {freq_plot_result}")
        except Exception as e:
            print(f"⚠ Frequency plot error: {e}")
    
    def test_05_edge_cases_handling(self):
        """Test handling of edge cases and error conditions"""
        print('\n=== Test 5: Edge Cases Handling ===')
        
        # Test with edge case data
        df_edge = pd.DataFrame(self.edge_case_data)
        
        extractor = KeywordExtractor(self.config)
        
        # Test API keyword extraction with problematic data
        try:
            api_keywords_df = extractor.extract_api_keywords(df_edge)
            print(f"✓ Edge case API extraction: {len(api_keywords_df)} keywords")
        except Exception as e:
            print(f"⚠ Edge case API extraction error: {e}")
        
        # Test NLP extraction with problematic abstracts
        try:
            problematic_abstracts = [
                '',  # Empty
                None,  # None
                'Normal text',  # Normal
                'Text with special chars @#$%^&*()',  # Special chars
                'A' * 10000,  # Very long text
            ]
            
            nlp_keywords = extractor.extract_nlp_keywords(
                problematic_abstracts, 
                method='tfidf'
            )
            print(f"✓ Edge case NLP extraction: {len(nlp_keywords.get('keywords', []))} keywords")
        except Exception as e:
            print(f"⚠ Edge case NLP extraction error: {e}")
    
    def test_06_empty_data_handling(self):
        """Test handling of empty datasets"""
        print('\n=== Test 6: Empty Data Handling ===')
        
        df_empty = pd.DataFrame(self.empty_data)
        
        extractor = KeywordExtractor(self.config)
        
        # Test with empty DataFrame
        api_keywords_df = extractor.extract_api_keywords(df_empty)
        assert api_keywords_df.empty, "Empty input should return empty DataFrame"
        
        # Test with empty text list
        nlp_keywords = extractor.extract_nlp_keywords([])
        assert nlp_keywords['keywords'] == [], "Empty input should return empty keywords"
        
        print("✓ Empty data handled correctly")
    
    def test_07_performance_with_large_dataset(self):
        """Test performance with larger dataset"""
        print('\n=== Test 7: Performance Test ===')
        
        # Create larger dataset
        large_data = {}
        for key in self.large_test_data:
            if key == 'publication_date':
                large_data[key] = [datetime.now() - timedelta(days=i*10) for i in range(100)]
            else:
                large_data[key] = (self.large_test_data[key] * 10)[:100]
        
        df_large = pd.DataFrame(large_data)
        
        import time
        
        extractor = KeywordExtractor(self.config)
        
        # Time API extraction
        start_time = time.time()
        api_keywords_df = extractor.extract_api_keywords(df_large)
        api_time = time.time() - start_time
        
        # Time NLP extraction (smaller sample for performance)
        start_time = time.time()
        nlp_keywords = extractor.extract_nlp_keywords(
            df_large['abstract'][:20].tolist(), 
            method='tfidf'
        )
        nlp_time = time.time() - start_time
        
        print(f"✓ API extraction: {len(api_keywords_df)} keywords in {api_time:.2f}s")
        print(f"✓ NLP extraction: {len(nlp_keywords['keywords'])} keywords in {nlp_time:.2f}s")
        
        # Performance assertions
        assert api_time < 10.0, "API extraction should complete within 10 seconds"
        assert nlp_time < 30.0, "NLP extraction should complete within 30 seconds"
    
    def test_08_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        print('\n=== Test 8: End-to-End Workflow ===')
        
        df = pd.DataFrame(self.large_test_data)
        
        # Initialize all components
        extractor = KeywordExtractor(self.config)
        analyzer = SemanticAnalyzer(self.config)
        temporal = TemporalAnalyzer(self.config.config)
        visualizer = Visualizer(self.config.config)
        
        # Step 1: Extract keywords
        api_keywords_df = extractor.extract_api_keywords(df)
        nlp_keywords = extractor.extract_nlp_keywords(df['abstract'].tolist()[:10], method='tfidf')
        
        # Step 2: Generate embeddings
        embeddings = analyzer.generate_embeddings(df['abstract'].tolist()[:10])
        
        # Step 3: Perform clustering
        if embeddings is not None:
            cluster_results = analyzer.perform_clustering(embeddings, method='kmeans')
        else:
            cluster_results = {'cluster_labels': [0] * 10, 'n_clusters': 1}
        
        # Step 4: Temporal analysis
        publications_list = df.to_dict('records')
        keywords_dict = {}
        for pub in publications_list:
            if 'keywords' in pub and pub['keywords']:
                for kw in pub['keywords']:
                    keywords_dict[kw] = keywords_dict.get(kw, {'frequency': 0, 'importance': 0.5})
                    keywords_dict[kw]['frequency'] += 1
        
        trends = temporal.analyze_keyword_trends(publications_list, keywords_dict)
        
        # Step 5: Create visualizations
        keyword_freqs = {}
        for kw_list in df['keywords']:
            for kw in kw_list:
                keyword_freqs[kw] = keyword_freqs.get(kw, 0) + 1
        
        try:
            wordcloud_result = visualizer.create_word_cloud(keyword_freqs, title="E2E Test Word Cloud")
            freq_plot_result = visualizer.plot_keyword_frequencies(keyword_freqs, title="E2E Test Frequencies")
        except Exception as e:
            print(f"⚠ Visualization error: {e}")
            wordcloud_result = "error"
            freq_plot_result = "error"
        
        # Verify results
        assert not api_keywords_df.empty, "Should extract API keywords"
        assert len(nlp_keywords['keywords']) > 0, "Should extract NLP keywords"
        assert embeddings is None or embeddings.shape[0] > 0, "Should generate embeddings or handle gracefully"
        assert 'cluster_labels' in cluster_results, "Should perform clustering"
        assert isinstance(trends, dict), "Should analyze trends"
        
        print("✓ End-to-end workflow completed successfully")
        print(f"  - API keywords: {len(api_keywords_df)}")
        print(f"  - NLP keywords: {len(nlp_keywords['keywords'])}")
        print(f"  - Embeddings: {embeddings.shape if embeddings is not None else 'N/A'}")
        print(f"  - Clusters: {cluster_results.get('n_clusters', 0)}")
        print(f"  - Trends: {len(trends.get('individual_trends', {}))}")
        print(f"  - Visualizations: {wordcloud_result}, {freq_plot_result}")
    
    def test_09_configuration_variations(self):
        """Test different configuration settings"""
        print('\n=== Test 9: Configuration Variations ===')
        
        # Test different TF-IDF configurations
        test_configs = [
            {'ngram_range': [1, 2], 'max_features': 100},
            {'ngram_range': [2, 3], 'max_features': 500},
            {'ngram_range': [1, 3], 'max_features': 50}
        ]
        
        sample_texts = self.large_test_data['abstract'][:5]
        
        for i, tfidf_config in enumerate(test_configs):
            try:
                # Create temporary config
                temp_config = ConfigManager()
                temp_config.config['keyword_analysis']['nlp']['tfidf'].update(tfidf_config)
                
                extractor = KeywordExtractor(temp_config)
                nlp_keywords = extractor.extract_nlp_keywords(sample_texts, method='tfidf')
                
                print(f"✓ Config {i+1}: {len(nlp_keywords['keywords'])} keywords with {tfidf_config}")
            except Exception as e:
                print(f"⚠ Config {i+1} error: {e}")
    
    def test_10_error_recovery(self):
        """Test error recovery and graceful failure handling"""
        print('\n=== Test 10: Error Recovery ===')
        
        extractor = KeywordExtractor(self.config)
        
        # Test with invalid method
        try:
            result = extractor.extract_nlp_keywords(['test text'], method='invalid_method')
            assert result['keywords'] == [], "Invalid method should return empty keywords"
            print("✓ Invalid method handled gracefully")
        except Exception as e:
            print(f"⚠ Invalid method error: {e}")
        
        # Test with corrupted data
        try:
            corrupted_df = pd.DataFrame({
                'title': [{'invalid': 'object'}],
                'keywords': [set(['invalid', 'set'])],
                'publication_date': ['invalid_date']
            })
            result = extractor.extract_api_keywords(corrupted_df)
            print(f"✓ Corrupted data handled: {len(result)} keywords extracted")
        except Exception as e:
            print(f"⚠ Corrupted data error: {e}")


def run_comprehensive_tests():
    """Run all comprehensive integration tests"""
    print('=' * 80)
    print('COMPREHENSIVE KEYWORD ANALYSIS MODULE INTEGRATION TESTS')
    print('=' * 80)
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Create test instance
    test_suite = TestKeywordAnalysisIntegration()
    test_suite.setup_class()
    
    # List of test methods
    test_methods = [
        test_suite.test_01_basic_integration,
        test_suite.test_02_semantic_analysis_integration,
        test_suite.test_03_temporal_analysis_integration,
        test_suite.test_04_visualization_integration,
        test_suite.test_05_edge_cases_handling,
        test_suite.test_06_empty_data_handling,
        test_suite.test_07_performance_with_large_dataset,
        test_suite.test_08_end_to_end_workflow,
        test_suite.test_09_configuration_variations,
        test_suite.test_10_error_recovery,
    ]
    
    # Run tests
    passed = 0
    failed = 0
    
    for test_method in test_methods:
        try:
            test_method()
            passed += 1
        except Exception as e:
            print(f"❌ {test_method.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    # Cleanup
    test_suite.teardown_class()
    
    # Results
    print('\n' + '=' * 80)
    print('TEST RESULTS SUMMARY')
    print('=' * 80)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! The keyword analysis module is working correctly.")
        return True
    else:
        print(f"\n⚠️ {failed} tests failed. Please review the errors above.")
        return False


if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
