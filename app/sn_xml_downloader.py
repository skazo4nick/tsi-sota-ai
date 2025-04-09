'''
Springer Nature XML Downloader Module (sn_xml_downloader.py)

This module is dedicated to downloading XML full text articles from the Springer Nature Open Access API.
It uses the 'springernature-api-client' Python library and requires the SPRINGERNATURE_API key
to be set in the .env file.

Functionalities include:
    - Checking if an article exists in the Springer Nature Open Access repository.
    - Downloading the full text XML of available articles.
    - Implementing rate limiting and daily request tracking.
    - Storing downloaded XML files and tracking downloaded articles.
'''

import springernature_api_client.openaccess as openaccess
import os
import json
import time
from datetime import date
# from dotenv import load_dotenv
import requests # Import requests for downloading XML

load_dotenv()

API_KEY_NAME = "SPRINGERNATURE_API"
XML_STORAGE_DIR = "app/data/xml"
DOWNLOADED_ARTICLES_JSON = "app/system_data/downloaded_articles.json"
DAILY_REQUEST_COUNT_FILE = "app/system_data/daily_request_count.json"
DAILY_REQUEST_LIMIT = 495
REQUEST_DELAY_SECONDS = 1

def _load_api_key():
    """Loads the Springer Nature API key from environment variables."""
    api_key = os.getenv(API_KEY_NAME)
    if not api_key:
        raise ValueError(f"API key not found in environment variables. Please set '{API_KEY_NAME}'.")
    return api_key

def check_article_existence(doi):
    """
    Checks if an article with the given DOI exists in the Springer Nature Open Access API.
    Returns metadata if the article exists, None otherwise.
    """
    api_key = _load_api_key()
    try:
        _increment_daily_request_count()  # Increment request count at start
        query = f"doi:{doi}"
        api_url = "https://api.springernature.com/openaccess/json"
        params = {"q": query, "api_key": api_key, "p": 10, "s": 1}
        print(f"API Request URL: {api_url} with params: {params}")
        r = requests.get(api_url, params=params)
        r.raise_for_status()
        time.sleep(REQUEST_DELAY_SECONDS)  # Rate limiting delay after API call
        response_json = r.json()
        print(f"Response from Springer Nature API: {response_json}")
        if isinstance(response_json, dict) and response_json.get("records") and len(response_json["records"]) > 0:
            print(f"Article with DOI: {doi} found in Springer Nature Open Access.")
            return response_json["records"][0]
        else:
            print(f"Article with DOI: {doi} not found in Springer Nature Open Access.")
            return None
    except Exception as e:
        print(f"Error checking article existence for DOI: {doi}. Error: {e}")
        return None

def download_xml_full_text(doi):
    """
    Downloads the full text XML of an article with the given DOI from Springer Nature Open Access API.
    Saves the XML to app/data/xml and updates downloaded articles tracking.
    Returns the filepath to the downloaded XML if successful, None otherwise.
    """
    if is_article_downloaded(doi):
        print(f"Article with DOI: {doi} already downloaded. Skipping.")
        return None # Or filepath if you want to return it

    api_key = _load_api_key()
    openaccess_client = openaccess.OpenAccessAPI(api_key=api_key)
    try:
        _increment_daily_request_count() # Increment request count at start
        query = f"doi:{doi}"
        response = openaccess_client.search(q=query)
        time.sleep(REQUEST_DELAY_SECONDS) # Rate limiting delay after API call
        if response and response.get("records"): # Changed to use get method for dictionary access
            article_metadata = response["records"][0] # Changed to use dictionary-style access
            xml_url = article_metadata.get('fullTextUrl') # Assuming 'fullTextUrl' points to XML - verify
            if xml_url:
                print(f"XML URL found: {xml_url}")
                print(f"Downloading XML content from URL: {xml_url}")
                try:
                    response = requests.get(xml_url)
                    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                    xml_content = response.text
                    filepath = os.path.join(XML_STORAGE_DIR, f"{doi.replace('/', '_')}.xml")
                    os.makedirs(XML_STORAGE_DIR, exist_ok=True)
                    with open(filepath, 'w', encoding='utf-8') as f: # Ensure utf-8 encoding
                        f.write(xml_content)
                    _update_downloaded_articles_tracking(doi, "xml")
                    return filepath
                except requests.exceptions.RequestException as download_error:
                    print(f"Error downloading XML content from {xml_url}. Error: {download_error}")
                    return None
            else:
                print(f"No XML fullTextUrl found for DOI: {doi}")
                return None
        else:
            print(f"Article metadata not found for DOI: {doi}") # Should be already checked in existence check
            return None
    except Exception as e:
        print(f"Error downloading XML for DOI: {doi}. Error: {e}")
        return None

_DAILY_REQUEST_COUNT_FILE = "app/data/daily_request_count.json"

def _load_daily_request_count():
    """Loads the daily request count from file, initializing if necessary."""
    try:
        with open(_DAILY_REQUEST_COUNT_FILE, 'r') as f:
            data = json.load(f)
            if data.get('date') == str(date.today()):
                return data.get('count', 0)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return 0

def _save_daily_request_count(count):
    """Saves the daily request count to file."""
    data = {'date': str(date.today()), 'count': count}
    os.makedirs(os.path.dirname(_DAILY_REQUEST_COUNT_FILE), exist_ok=True)
    with open(_DAILY_REQUEST_COUNT_FILE, 'w') as f:
        json.dump(data, f)

def _increment_daily_request_count():
    """Increments the daily request count, checking against the limit."""
    count = _load_daily_request_count()
    if count >= DAILY_REQUEST_LIMIT:
        raise Exception("Daily request limit reached.")
    count += 1
    _save_daily_request_count(count)
    return count

def _load_downloaded_articles_tracking():
    """Loads the downloaded articles tracking data from JSON file."""
    try:
        with open(DOWNLOADED_ARTICLES_JSON, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def _update_downloaded_articles_tracking(doi, format):
    """Updates the downloaded articles tracking JSON file."""
    downloaded_articles = _load_downloaded_articles_tracking()
    downloaded_articles[doi] = format
    os.makedirs(os.path.dirname(DOWNLOADED_ARTICLES_JSON), exist_ok=True)
    with open(DOWNLOADED_ARTICLES_JSON, 'w') as f:
        json.dump(downloaded_articles, f, indent=4)

def is_article_downloaded(doi):
    """Checks if an article with the given DOI is already tracked as downloaded."""
    downloaded_articles = _load_downloaded_articles_tracking()
    return doi in downloaded_articles

if __name__ == '__main__':
    # Example usage (for testing purposes)
    test_doi = "10.1186/s40537-020-00329-2" # Error DOI - replace with a real DOI for testing
    if check_article_existence(test_doi):
        xml_filepath = download_xml_full_text(test_doi)
        if xml_filepath:
            print(f"XML downloaded successfully to: {xml_filepath}")
        else:
            print(f"XML download failed for DOI: {test_doi}")
    else:
        print(f"Article with DOI: {test_doi} not found in Springer Nature Open Access.")
