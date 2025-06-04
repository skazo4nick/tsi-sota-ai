#!/usr/bin/env python3
"""Test Semantic Scholar API directly."""

import requests

def test_api():
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        'query': 'AI',
        'year': '2024',
        'limit': 1,
        'offset': 0,
        'fields': 'title,authors,year,citationCount,referenceCount,fieldsOfStudy,venue'
    }
    
    try:
        response = requests.get(url, params=params)
        print(f"Status: {response.status_code}")
        print(f"URL: {response.url}")
        print(f"Response: {response.text[:500]}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Found {data.get('total', 0)} total results")
            if data.get('data'):
                print(f"First result: {data['data'][0].get('title', 'No title')}")
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_api()
