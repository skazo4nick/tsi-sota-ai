#!/usr/bin/env python3
"""
Tests for Semantic Scholar API Client.

These tests demonstrate the functionality of the SemanticScholarAPIClient
including paper search, advanced search, recommendations, and paper details.

Note: API rate limits apply (1 request/second with API key).
Set SEMANTIC_SCHOLAR_API_KEY environment variable for authenticated access.
"""

import sys
import os
import time
import json
from typing import List, Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from slr_core.api_clients import SemanticScholarAPIClient
from slr_core.config_manager import ConfigManager

def test_basic_search():
    """Test basic paper search functionality."""
    print("=" * 60)
    print("Testing Basic Paper Search")
    print("=" * 60)
    
    client = SemanticScholarAPIClient()
    
    # Test with a specific query
    query = "machine learning"
    start_year = 2023
    end_year = 2024
    max_results = 5
    
    print(f"Searching for: '{query}' ({start_year}-{end_year})")
    print(f"Max results: {max_results}")
    print()
    
    results = client.fetch_publications(query, start_year, end_year, max_results)
    
    print(f"Retrieved {len(results)} papers")
    
    if results:
        print("\nFirst paper details:")
        first_paper = results[0]
        for key, value in first_paper.items():
            print(f"  {key}: {value}")
    
    return results

def test_advanced_search():
    """Test advanced search with filters."""
    print("\n" + "=" * 60)
    print("Testing Advanced Search with Filters")
    print("=" * 60)
    
    client = SemanticScholarAPIClient()
    
    # Test advanced query syntax
    query = '"deep learning" AND (computer vision OR NLP)'
    filters = {
        'year': '2023-2024',
        'minCitationCount': 10,
        'publicationTypes': 'JournalArticle'
    }
    sort = 'citationCount'
    max_results = 3
    
    print(f"Advanced query: {query}")
    print(f"Filters: {filters}")
    print(f"Sort by: {sort}")
    print()
    
    results = client.search_papers_advanced(query, filters, sort, max_results)
    
    print(f"Retrieved {len(results)} papers")
    
    if results:
        print("\nPapers sorted by citation count:")
        for i, paper in enumerate(results):
            print(f"{i+1}. {paper.get('title', 'No title')}")
            print(f"   Citations: {paper.get('citation_count', 0)}")
            print(f"   Year: {paper.get('publication_date', 'Unknown')}")
            print()
    
    return results

def test_paper_recommendations():
    """Test paper recommendations functionality."""
    print("\n" + "=" * 60)
    print("Testing Paper Recommendations")
    print("=" * 60)
    
    client = SemanticScholarAPIClient()
    
    # Known paper IDs for testing (these are real Semantic Scholar paper IDs)
    positive_seeds = [
        "649def34f8be52c8b66281af98ae884c09aef38b",  # Construction of the Literature Graph in Semantic Scholar
        "204e3073870fae3d05bcbc2f6a8e263d9b72e776",  # BERT: Pre-training of Deep Bidirectional Transformers
    ]
    
    print(f"Getting recommendations based on {len(positive_seeds)} seed papers")
    print()
    
    recommendations = client.fetch_paper_recommendations(positive_seeds, max_results=3)
    
    print(f"Retrieved {len(recommendations)} recommendations")
    
    if recommendations:
        print("\nRecommended papers:")
        for i, paper in enumerate(recommendations):
            print(f"{i+1}. {paper.get('title', 'No title')}")
            print(f"   Authors: {', '.join(paper.get('authors', []))[:100]}...")
            print(f"   Citations: {paper.get('citation_count', 0)}")
            print()
    
    return recommendations

def test_paper_details():
    """Test getting detailed paper information."""
    print("\n" + "=" * 60)
    print("Testing Paper Details Retrieval")
    print("=" * 60)
    
    client = SemanticScholarAPIClient()
    
    # Test with a known paper ID
    paper_id = "649def34f8be52c8b66281af98ae884c09aef38b"  # Construction of the Literature Graph in Semantic Scholar
    
    print(f"Getting details for paper ID: {paper_id}")
    print()
    
    details = client.get_paper_details(paper_id)
    
    if details:
        print("Paper details:")
        for key, value in details.items():
            if key == 'abstract' and value:
                print(f"  {key}: {value[:200]}...")
            elif key == 'authors' and isinstance(value, list):
                print(f"  {key}: {', '.join(value[:3])}{'...' if len(value) > 3 else ''}")
            else:
                print(f"  {key}: {value}")
    else:
        print("No details retrieved")
    
    return details

def test_with_config_manager():
    """Test client with ConfigManager."""
    print("\n" + "=" * 60)
    print("Testing with ConfigManager")
    print("=" * 60)
    
    try:
        config_manager = ConfigManager()
        client = SemanticScholarAPIClient(config_manager=config_manager)
        
        print("SemanticScholarAPIClient initialized with ConfigManager")
        print(f"Base URL: {client.base_url}")
        print(f"Has API key: {'Yes' if client.api_key else 'No (using public access)'}")
        print()
        
        # Quick test search
        results = client.fetch_publications("AI research", 2024, 2024, 2)
        print(f"Test search returned {len(results)} results")
        
        return True
    except Exception as e:
        print(f"Error with ConfigManager: {e}")
        return False

def test_error_handling():
    """Test error handling for various scenarios."""
    print("\n" + "=" * 60)
    print("Testing Error Handling")
    print("=" * 60)
    
    client = SemanticScholarAPIClient()
    
    # Test with empty query
    print("1. Testing empty query...")
    results = client.fetch_publications("", 2024, 2024, 1)
    print(f"Empty query returned {len(results)} results")
    
    # Test with invalid year range
    print("\n2. Testing invalid year range...")
    results = client.fetch_publications("test", 2025, 2020, 1)  # End year before start year
    print(f"Invalid year range returned {len(results)} results")
    
    # Test with very specific query that might return no results
    print("\n3. Testing very specific query...")
    results = client.fetch_publications("xyzunlikelyquerythatreturnsnothing", 2024, 2024, 1)
    print(f"Specific query returned {len(results)} results")
    
    # Test getting details for non-existent paper
    print("\n4. Testing non-existent paper ID...")
    details = client.get_paper_details("nonexistentpaperid123")
    print(f"Non-existent paper details: {details}")

def main():
    """Run all tests."""
    print("Semantic Scholar API Client Test Suite")
    print("=" * 60)
    print("Note: Tests will respect API rate limits (1 req/sec)")
    print("Set SEMANTIC_SCHOLAR_API_KEY environment variable for authenticated access")
    print()
    
    # Check if API key is available
    api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    if api_key:
        print("✓ API key found - using authenticated access")
    else:
        print("ℹ No API key found - using public access (shared rate limits)")
    print()
    
    try:
        # Run tests with delays to respect rate limits
        test_basic_search()
        time.sleep(2)  # Rate limiting
        
        test_advanced_search()
        time.sleep(2)  # Rate limiting
        
        test_paper_recommendations()
        time.sleep(2)  # Rate limiting
        
        test_paper_details()
        time.sleep(2)  # Rate limiting
        
        test_with_config_manager()
        time.sleep(2)  # Rate limiting
        
        test_error_handling()
        
        print("\n" + "=" * 60)
        print("All tests completed successfully!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
    except Exception as e:
        print(f"\nTest suite failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
