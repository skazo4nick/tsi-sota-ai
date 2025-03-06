import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""
Tests for CORE API Client functions.

These tests interact with the actual CORE API. Please ensure that the environment variable CORE_API_KEY is set
before running these tests. A 7-second delay is added between calls to respect the API rate limit of 10 calls per minute.
"""

import unittest
import time
import json
from core_api_client import get_entity, query_api, scroll, retrieve_publication_by_doi

# Adjust this DOI to one known to work with CORE API for full text retrieval.
TEST_DOI = "10.1038/s41586-022-04826-7"

class TestCoreAPIClient(unittest.TestCase):
    
    def test_retrieve_publication_by_doi_fulltext(self):
        """Test retrieving publication full text by DOI."""
        publication, elapsed = retrieve_publication_by_doi(TEST_DOI, full_text=True)
        # Check that some expected keys are in the returned JSON
        self.assertIsInstance(publication, dict)
        print("Publication retrieved:", json.dumps(publication, indent=2)) # Print publication for debugging
        if isinstance(publication, dict):
            self.assertTrue("title" in publication or "metadata" in publication)
        else:
            self.assertIsInstance(publication, str) # Expect a string when full text is not found
        time.sleep(7)  # lag between calls

    def test_get_entity(self):
        """Test get_entity function fetching a specific entity."""
        # Using a simple test for a data provider, endpoint may vary as needed.
        response_json, elapsed = get_entity("data-providers/1")
        self.assertIsInstance(response_json, dict)
        self.assertTrue("id" in response_json)
        print("Data provider fetched:", json.dumps(response_json, indent=2))
        time.sleep(7)

    def test_query_api_search_works(self):
        """Test query_api function by performing a simple works search query."""
        query = "covid"
        response_json, elapsed = query_api("search/works", query, limit=10)
        self.assertIsInstance(response_json, dict)
        self.assertTrue("results" in response_json)
        print("Works search results:", json.dumps(response_json, indent=2))
        time.sleep(7)

    def test_scroll(self):
        """Test scroll function to retrieve a list of works matching a query."""
        query = "machine learning"
        results = scroll("search/works", query)
        # The results might be empty if no matches, but we expect a list.
        self.assertIsInstance(results, list)
        print(f"Scrolled and fetched {len(results)} results")
        time.sleep(7)

if __name__ == '__main__':
    unittest.main()
