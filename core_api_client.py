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

def get_entity(identifier, subresource=None):
    """
    Retrieve a work or its subresource from CORE API by identifier (CORE work id or DOI).
    - identifier: CORE work id (preferred) or DOI (as string)
    - subresource: None (default, gets the work), or one of 'outputs', 'stats', 'tei', 'download'
    Returns the JSON response or file content (for tei/download) or an error message.
    """
    base_url = f"https://api.core.ac.uk/v3/works/{identifier}"
    if subresource == "outputs":
        url = f"{base_url}/outputs"
    elif subresource == "stats":
        url = f"{base_url}/stats"
    elif subresource == "tei":
        url = f"https://api.core.ac.uk/v3/works/tei/{identifier}"
    elif subresource == "download":
        url = f"{base_url}/download"
    else:
        url = base_url
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            # For tei/download, may be XML or file content
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return response.json()
            else:
                return response.content
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def search_publications_by_keywords(keywords, limit=10):
    """
    Search for publications in CORE by keywords.
    Uses POST /search/works endpoint.
    Returns a list of publication metadata dicts (including CORE work id and DOIs if available).
    """
    url = "https://api.core.ac.uk/v3/search/works"
    payload = {"query": keywords, "limit": limit}
    result, elapsed = query_api(url, payload=payload)
    if isinstance(result, dict) and "results" in result and isinstance(result["results"], list):
        return result["results"]
    return []

def retrieve_publication_by_core_id(core_id):
    """
    Retrieve publication metadata by CORE work id using GET /works/{core_id}.
    Returns a dict with publication metadata or an error message.
    """
    url = f"https://api.core.ac.uk/v3/works/{core_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json(), None
        else:
            return {"error": f"Metadata not found in CORE API for work id {core_id}"}, None
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}, None

def retrieve_publication_by_doi(doi, full_text=False):
    """
    Retrieves a publication using its DOI.
    If full_text is True, uses the CORE API v3 'discover' endpoint (POST /discover).
    If the discover endpoint returns a 404 error or an empty result, returns a
    formatted message indicating that full text is not found.
    If full_text is False, uses the /works/{doi} endpoint for metadata.
    Returns a dict with publication metadata or a message if not found.
    """
    if full_text:
        url = "https://api.core.ac.uk/v3/discover"
        payload = {"doi": doi}
        try:
            result, elapsed = query_api(url, payload=payload)
            if not (isinstance(result, dict) and "results" in result and isinstance(result["results"], list) and result["results"]):
                return {"error": f"Full text not found in CORE API for DOI {doi}"}, elapsed
            return result["results"][0], elapsed
        except Exception as e:
            if "404" in str(e):
                return {"error": f"Full text not found in CORE API for DOI {doi}"}, None
            else:
                raise
    else:
        # Use GET /works/{doi} for direct metadata lookup by DOI
        url = f"https://api.core.ac.uk/v3/works/{doi}"
        try:
            response = requests.get(url, headers=HEADERS)
            if response.status_code == 200:
                return response.json(), None
            else:
                return {"error": f"Metadata not found in CORE API for DOI {doi}"}, None
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {e}"}, None

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
    if isinstance(result, dict) and "results" in result and isinstance(result["results"], list):
        return result["results"]
    else:
        return []

def search_works_by_keyword(keyword, field="fullText", limit=10, offset=0):
    """
    Search works by keyword in a specific field (default: fullText).
    Uses GET /search/works?q=field:"keyword"&limit=...&offset=...
    Returns the JSON response from CORE API or None on error.
    """
    url = "https://api.core.ac.uk/v3/search/works"
    params = {"q": f'{field}:"{keyword}"', "limit": limit, "offset": offset}
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def search_works_by_doi(doi, limit=1):
    """
    Search works by DOI using GET /search/works?q=doi:"<doi>"&limit=...
    Returns the JSON response from CORE API or None on error.
    """
    url = "https://api.core.ac.uk/v3/search/works"
    params = {"q": f'doi:"{doi}"', "limit": limit}
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def search_works_by_title(title, limit=1):
    """
    Search works by title using GET /search/works?q=title:"<title>"&limit=...
    Returns the JSON response from CORE API or None on error.
    """
    url = "https://api.core.ac.uk/v3/search/works"
    params = {"q": f'title:"{title}"', "limit": limit}
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def search_works_by_author(author, limit=10, offset=0):
    """
    Search works by author name using GET /search/works?q=authors:"<author>"&limit=...&offset=...
    Returns the JSON response from CORE API or None on error.
    """
    url = "https://api.core.ac.uk/v3/search/works"
    params = {"q": f'authors:"{author}"', "limit": limit, "offset": offset}
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def search_works_by_field(field, value, limit=10, offset=0):
    """
    Generic search works by any field using GET /search/works?q=field:"<value>"&limit=...&offset=...
    Returns the JSON response from CORE API or None on error.
    """
    url = "https://api.core.ac.uk/v3/search/works"
    params = {"q": f'{field}:"{value}"', "limit": limit, "offset": offset}
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

if __name__ == "__main__":
    test_doi = "10.1038/s41586-022-04826-7"
    try:
        publication, elapsed = retrieve_publication_by_doi(test_doi, full_text=True)
        print(publication)
    except Exception as error:
        print(error)
