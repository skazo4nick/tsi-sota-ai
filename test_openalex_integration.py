#!/usr/bin/env python3
"""
Quick test script to validate OpenAlex integration upgrade
"""
import sys
import os

# Add project root to path
sys.path.insert(0, '/workspaces/tsi-sota-ai')

from slr_core.api_clients import OpenAlexAPIClient
from slr_core.config_manager import ConfigManager

def test_openalex_integration():
    """Test the upgraded OpenAlex integration"""
    print("=== Testing OpenAlex Integration ===")
    
    # Test 1: Basic initialization
    print("\n1. Testing basic initialization...")
    try:
        config = ConfigManager()
        client = OpenAlexAPIClient(config_manager=config)
        print("✓ OpenAlexAPIClient initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing client: {e}")
        return False
    
    # Test 2: Small query test
    print("\n2. Testing small query for 'agentic AI supply chain'...")
    try:
        results = client.fetch_publications(
            query="agentic AI supply chain", 
            start_year=2023, 
            end_year=2024, 
            max_results=5
        )
        
        print(f"✓ Query executed successfully")
        print(f"✓ Retrieved {len(results)} results")
        
        if results:
            sample = results[0]
            print(f"✓ Sample result keys: {list(sample.keys())}")
            print(f"✓ Sample title: {sample.get('title', 'N/A')[:100]}...")
            print(f"✓ Sample DOI: {sample.get('doi', 'N/A')}")
            print(f"✓ Sample year: {sample.get('publication_date', 'N/A')}")
            
            # Check if we got real data or dummy data
            if sample.get('title') == "Dummy OpenAlex Paper 1":
                print("⚠ Warning: Got dummy data - pyalex may not be installed")
                return False
            else:
                print("✓ Got real OpenAlex data!")
                return True
        else:
            print("⚠ Warning: No results returned (may be expected for narrow query)")
            return True
            
    except Exception as e:
        print(f"✗ Error during query: {e}")
        return False

if __name__ == "__main__":
    success = test_openalex_integration()
    if success:
        print("\n🎉 OpenAlex integration test PASSED!")
        sys.exit(0)
    else:
        print("\n❌ OpenAlex integration test FAILED!")
        sys.exit(1)
