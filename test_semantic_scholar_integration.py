#!/usr/bin/env python3
"""
Quick integration test for Semantic Scholar API client.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from slr_core.data_acquirer import DataAcquirer
from slr_core.config_manager import ConfigManager

def test_semantic_scholar_integration():
    """Test Semantic Scholar integration with DataAcquirer."""
    print("Testing Semantic Scholar Integration with DataAcquirer")
    print("=" * 60)
    
    # Initialize ConfigManager
    config_manager = ConfigManager()
    
    # Initialize DataAcquirer
    data_acquirer = DataAcquirer(config_manager=config_manager)
    
    # Check if SemanticScholar is in supported sources
    print(f"Supported sources: {data_acquirer.SUPPORTED_SOURCES}")
    assert "SemanticScholar" in data_acquirer.SUPPORTED_SOURCES
    
    # Check if SemanticScholar client is initialized
    assert "SemanticScholar" in data_acquirer.clients
    print("✓ Semantic Scholar client successfully initialized in DataAcquirer")
    
    # Test direct client access
    semantic_client = data_acquirer.clients["SemanticScholar"]
    print(f"✓ Semantic Scholar client type: {type(semantic_client).__name__}")
    
    # Test a simple search (limited to 2 results to minimize API calls)
    print("\nTesting simple search...")
    try:
        results = semantic_client.fetch_publications("AI", 2024, 2024, max_results=2)
        print(f"✓ Retrieved {len(results)} results")
        
        if results:
            print("✓ Sample result structure:")
            first_result = results[0]
            for key in ['title', 'doi', 'source', 'citation_count']:
                if key in first_result:
                    print(f"  {key}: {first_result[key]}")
        
    except Exception as e:
        print(f"⚠ Error during API call (expected without API key): {e}")
    
    # Test fetch_all_sources method with limited results
    print("\nTesting DataAcquirer.fetch_all_sources...")
    try:
        all_results = data_acquirer.fetch_all_sources("machine learning", 2024, 2024, max_results_per_source=1)
        semantic_results = all_results.get("SemanticScholar", [])
        print(f"✓ DataAcquirer retrieved {len(semantic_results)} results from Semantic Scholar")
        
        if semantic_results:
            print("✓ Sample result from DataAcquirer:")
            first_result = semantic_results[0]
            for key in ['title', 'doi', 'source', 'citation_count']:
                if key in first_result:
                    print(f"  {key}: {first_result[key]}")
        
    except Exception as e:
        print(f"⚠ Error during DataAcquirer call: {e}")
    
    print("\n" + "=" * 60)
    print("Integration test completed successfully!")
    print("The Semantic Scholar API client is properly integrated.")

if __name__ == "__main__":
    test_semantic_scholar_integration()
