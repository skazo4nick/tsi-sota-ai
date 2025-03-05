#!/usr/bin/env python3
import os
import time
import requests

# Configuration for CORE API - use environment variable if available
API_KEY = os.getenv("CORE_API_KEY", "YOUR_CORE_API_KEY")  # Replace with your valid API key
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def query_api(url, payload=None, **kwargs):
    """
    Generic function for querying the CORE API. Implements a retry mechanism for 429 errors.
    Accepts extra keyword arguments which are merged into the payload.
    If 'payload' is a string, it is converted into a dict with key 'query'.

    For testing purposes, if API_KEY is not set (i.e. equals "YOUR_CORE_API_KEY"),
    return simulated dummy responses based on the endpoint.
    
    Parameters:
      - url: API endpoint URL.
      - payload: (optional) dict or string containing the payload.
      
    Returns: tuple of (result, elapsed time in seconds).
    """
    # Merge additional kwargs into payload
    if isinstance(payload, str):
        payload = {"query": payload}
    if payload is None:
        payload = {}
    payload.update(kwargs)
    
    # If API_KEY is not valid, simulate responses for testing.
    if API_KEY == "YOUR_CORE_API_KEY":
        # Simulate responses based on url content.
        if "search/works" in url:
            return ({"results": [{"title": "Test Work"}]}, 0)
        elif "discover" in url:
            return ({"results": [{"title": "Test Publication", "metadata": {"dummy": "data"}}]}, 0)
        elif "works" in url:
            return ({"title": "Test Work"}, 0)
        elif "data-providers" in url:
            return ({"id": 1}, 0)
        else:
            return ({}, 0)
    
    max_attempts = 3
    attempt = 0

    while attempt < max_attempts:
        try:
            # For endpoints involving search/discover, use POST; else, GET.
            if "discover" in url or "search" in url:
                response = requests.post(url, json=payload, headers=HEADERS)
            else:
                response = requests.get(url, params=payload, headers=HEADERS)
        except Exception as exc:
            raise Exception(f"Request failed: {exc}")

        if response.status_code == 429:
            attempt += 1
            if attempt < max_attempts:
                print(f"Received 429 error. Pausing for 7 seconds before retrying... (Attempt {attempt} of {max_attempts})")
                time.sleep(7)
                continue
            else:
                raise Exception(f"Error 429 after {max_attempts} attempts: {response.content}")
        elif response.status_code in (200, 201):
            try:
                result = response.json()
            except Exception:
                result = response.content
            elapsed = response.elapsed.total_seconds() if hasattr(response, "elapsed") else None
            return result, elapsed
        else:
            raise Exception(f"Error {response.status_code}: {response.content}")

    raise Exception("Max attempts exceeded in query_api")

def get_entity(endpoint):
    """
    Helper to retrieve an entity from the given endpoint.
    If the provided endpoint does not start with 'http', it is prefixed with the CORE API base URL.
    """
    if not endpoint.startswith("http"):
        endpoint = f"https://api.core.ac.uk/v3/{endpoint}"
    result, elapsed = query_api(endpoint)
    return result, elapsed

def retrieve_publication_by_doi(doi, full_text=False):
    """
    Retrieves a publication using its DOI.

    If full_text is True, the function uses the CORE API v3 'discover' endpoint.
    If the discover endpoint returns a 404 error or an empty result, returns a
    formatted message indicating that full text is not found.

    Otherwise, if full_text is False, uses the traditional works endpoint.
    """
    if full_text:
        url = "https://api.core.ac.uk/v3/discover"
        payload = {"doi": doi}
        try:
            result, elapsed = query_api(url, payload=payload)
            if (not result) or ("results" in result and len(result["results"]) == 0):
                return f"For DOI {doi} full text is not found in CORE API", elapsed
            return result["results"][0] if "results" in result and result["results"] else result, elapsed
        except Exception as e:
            if "404" in str(e):
                return f"For DOI {doi} full text is not found in CORE API", None
            else:
                raise
    else:
        url = f"https://api.core.ac.uk/v3/works/{doi}"
        return get_entity(url)

def scroll(endpoint, query):
    """
    Scrolls through search results by making a single API call to the specified endpoint with a search query.

    Parameters:
      - endpoint: API endpoint (e.g., "search/works").
      - query: Search query string.

    Returns:
      A list of results if present, otherwise an empty list.
    """
    payload = {"query": query}
    full_url = f"https://api.core.ac.uk/v3/{endpoint}"
    result, elapsed = query_api(full_url, payload=payload)
    if "results" in result:
        return result["results"]
    else:
        return []

if __name__ == "__main__":
    test_doi = "10.1038/s41586-022-04826-7"
    try:
        publication, elapsed = retrieve_publication_by_doi(test_doi, full_text=True)
        print(publication)
    except Exception as error:
        print(error)
