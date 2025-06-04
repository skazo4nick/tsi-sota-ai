#!/usr/bin/env python3
"""
Test the Semantic Scholar bulk search functionality specifically.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from slr_core.api_clients import SemanticScholarAPIClient
from slr_core.config_manager import ConfigManager

def test_bulk_search():
    """Test the bulk search functionality."""
    print("Testing Semantic Scholar Bulk Search")
    print("=" * 50)
    
    try:
        config_manager = ConfigManager()
        client = SemanticScholarAPIClient(config_manager)
        print("✓ Client initialized successfully")
        
        # Check if bulk search method exists
        if hasattr(client, 'fetch_bulk_publications'):
            print("✓ Bulk search method found")
        else:
            print("⚠ Bulk search method not found")
            
    except Exception as e:
        print(f"⚠ Error initializing client: {e}")

    # Test basic search as comparison
    print(f"\n{'='*50}")
    print("Testing regular search for comparison...")
    
    try:
        regular_results = client.fetch_publications("deep learning", 2024, 2024, max_results=1)
        print(f"✓ Regular search retrieved {len(regular_results)} papers")
        
        if regular_results:
            paper = regular_results[0]
            print(f"Sample regular result:")
            print(f"  Title: {paper.get('title', 'N/A')}")
            print(f"  Citations: {paper.get('citation_count', 'N/A')}")
            
    except Exception as e:
        print(f"⚠ Error during regular search: {e}")

if __name__ == "__main__":
    test_bulk_search()
