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

from sn_custom_client.sn_openaccess_client import SpringerNatureOpenAccessClient
import os
import json
import time
from datetime import date
from dotenv import load_dotenv
import requests # Import requests for downloading XML
from typing import Optional, Dict, List
import logging
from tqdm import tqdm

load_dotenv()

API_KEY_NAME = "SPRINGERNATURE_API"
XML_STORAGE_DIR = "app/data/xml"
DOWNLOADED_ARTICLES_JSON = "app/system_data/downloaded_articles.json"
DAILY_REQUEST_COUNT_FILE = "app/system_data/daily_request_count.json"
DAILY_REQUEST_LIMIT = 495
REQUEST_DELAY_SECONDS = 1

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

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
    try:
        _increment_daily_request_count()
        client = SpringerNatureOpenAccessClient()
        exists = client.article_exists(doi)
        if exists:
            # Optionally return metadata
            return True
        else:
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
        return None
    try:
        _increment_daily_request_count()
        client = SpringerNatureOpenAccessClient()
        xml_path = client.download_xml(doi, out_dir=XML_STORAGE_DIR)
        if xml_path:
            _update_downloaded_articles_tracking(doi, "xml")
            return xml_path
        else:
            print(f"XML download failed for DOI: {doi}")
            return None
    except Exception as e:
        print(f"Error downloading XML for DOI: {doi}. Error: {e}")
        return None

def _load_daily_request_count():
    """Loads the daily request count from file, initializing if necessary."""
    try:
        with open(DAILY_REQUEST_COUNT_FILE, 'r') as f:
            data = json.load(f)
            if data.get('date') == str(date.today()):
                return data.get('count', 0)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return 0

def _save_daily_request_count(count):
    """Saves the daily request count to file."""
    data = {'date': str(date.today()), 'count': count}
    os.makedirs(os.path.dirname(DAILY_REQUEST_COUNT_FILE), exist_ok=True)
    with open(DAILY_REQUEST_COUNT_FILE, 'w') as f:
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

def advanced_query_download(query: str, filters: Optional[Dict] = None, sort: Optional[str] = None, page_size: int = 20, max_records: int = 100, out_dir: str = XML_STORAGE_DIR, show_progress: bool = True) -> List[Dict]:
    """
    Perform an advanced query with boolean logic, filters, and sorting. Downloads XMLs for all matching articles (up to max_records).
    Args:
        query (str): Main query string (can include boolean logic, e.g. 'author:Smith AND year:2024').
        filters (dict, optional): Additional filter parameters (e.g. {"journal": "Nature"}).
        sort (str, optional): Sort string (e.g. 'date desc').
        page_size (int): Number of results per page.
        max_records (int): Maximum number of articles to download.
        out_dir (str): Directory to save XML files.
        show_progress (bool): Whether to show a progress bar.
    Returns:
        List of dicts with download status and metadata for each article.
    """
    client = SpringerNatureOpenAccessClient()
    results = client.advanced_query(query, filters=filters, sort=sort, page_size=page_size, max_records=max_records)
    filepaths = []
    iterator = tqdm(results, desc="Downloading XMLs") if show_progress else results
    for record in iterator:
        doi = record.get("doi")
        if not doi:
            logging.warning("No DOI found in record, skipping.")
            continue
        if is_article_downloaded(doi):
            logging.info(f"Article with DOI: {doi} already downloaded. Skipping.")
            continue
        try:
            _increment_daily_request_count()
            xml_path = client.download_xml(doi, out_dir=out_dir)
            if xml_path:
                _update_downloaded_articles_tracking(doi, "xml")
                filepaths.append({"doi": doi, "xml_path": xml_path, "status": "success", "record": record})
                logging.info(f"Downloaded XML for DOI: {doi} to {xml_path}")
            else:
                filepaths.append({"doi": doi, "xml_path": None, "status": "not_found", "record": record})
                logging.warning(f"XML not found for DOI: {doi}")
        except Exception as e:
            filepaths.append({"doi": doi, "xml_path": None, "status": "error", "error": str(e), "record": record})
            logging.error(f"Error downloading XML for DOI: {doi}: {e}")
        time.sleep(REQUEST_DELAY_SECONDS)
    return filepaths

if __name__ == '__main__':
    # Example usage (for testing purposes)
    test_doi = "10.1186/s40537-020-00329-2"
    if check_article_existence(test_doi):
        xml_filepath = download_xml_full_text(test_doi)
        if xml_filepath:
            print(f"XML downloaded successfully to: {xml_filepath}")
        else:
            print(f"XML download failed for DOI: {test_doi}")
    else:
        print(f"Article with DOI: {test_doi} not found in Springer Nature Open Access.")
