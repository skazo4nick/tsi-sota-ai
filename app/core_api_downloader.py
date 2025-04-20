"""
CORE API Downloader

This script reads test articles from "app/system_data/json_references/test_articles.json", checks if 
each article (by DOI) has already been downloaded (using "app/system_data/downloaded_articles.json"), and if not,
retrieves the publication full text and metadata from the CORE API. If the publication is found, its metadata is
saved to "app/system_data/core_api_articles.json", and if the full text is in XML format, it is saved to 
"app/data/xml". The DOI of each successfully downloaded article is added to the downloaded articles record
to avoid duplicate downloads.

A 7-second delay is applied between API calls to adhere to the rate limit (10 calls per minute).

Requires:
    - CORE_API_KEY environment variable set.
    - core_api_client.py module in the workspace.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import os
import json
import time
import shutil
from core_api_client import retrieve_publication_by_doi

# File paths
TEST_ARTICLES_PATH = "app/system_data/json_references/test_articles.json"
CORE_API_ARTICLES_PATH = "app/system_data/core_api_articles.json"
DOWNLOADED_ARTICLES_PATH = "app/system_data/downloaded_articles.json"
XML_DOWNLOAD_DIR = "app/data/xml"

# Delay between API calls (in seconds)
API_DELAY = 7

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return {}

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_article_xml(doi, publication_data):
    """
    Save the XML full text if available.
    We assume that if the publication_data contains a key indicating XML format (e.g. "format" == "xml")
    then the full text is XML. Alternatively, if the content starts with '<?xml', we'll treat it as XML.
    The file is saved in XML_DOWNLOAD_DIR with filename based on the DOI.
    """
    # Here, we use a simple heuristic: if the publication_data has a key "fullText" that is a string
    # and starts with '<?xml', we consider it XML.
    full_text = publication_data.get("fullText")
    if full_text and isinstance(full_text, str) and full_text.lstrip().startswith("<?xml"):
        # Create a safe filename from DOI by replacing "/" and ":" with underscores.
        safe_doi = doi.replace("/", "_").replace(":", "_")
        filename = os.path.join(XML_DOWNLOAD_DIR, f"{safe_doi}.xml")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(full_text)
        return filename
    return None

def main():
    print("Starting CORE API Download process...")

    # Load test articles from file (expecting a list of article objects with at least a "doi" field)
    test_articles = load_json(TEST_ARTICLES_PATH)
    if not test_articles:
        print(f"No test articles found in {TEST_ARTICLES_PATH}. Exiting.")
        return

    # Load already downloaded article DOIs (stored as a list)
    downloaded_articles = load_json(DOWNLOADED_ARTICLES_PATH)
    if not isinstance(downloaded_articles, list):
        downloaded_articles = []

    # Load existing CORE API articles metadata, keyed by DOI
    core_api_articles = load_json(CORE_API_ARTICLES_PATH)
    if not isinstance(core_api_articles, dict):
        core_api_articles = {}

    ensure_directory(XML_DOWNLOAD_DIR)

    for article in test_articles:
        doi = article.get("doi")
        if not doi:
            print("Skipping article with no DOI.")
            continue

        if doi in downloaded_articles:
            print(f"Article {doi} already downloaded. Skipping.")
            continue

        print(f"Processing article {doi}...")
        try:
            publication_data, elapsed = retrieve_publication_by_doi(doi, full_text=True)
            print(f"Retrieved publication for {doi} in {elapsed} seconds.")

            # Save publication metadata
            core_api_articles[doi] = publication_data

            # Attempt to download XML full text if available.
            xml_file = download_article_xml(doi, publication_data)
            if xml_file:
                print(f"Full text XML saved to {xml_file}.")
            else:
                print("Full text XML not available or not detected.")

            # Record this article as downloaded
            downloaded_articles.append(doi)

            # Save updated metadata and downloaded records to files
            save_json(CORE_API_ARTICLES_PATH, core_api_articles)
            save_json(DOWNLOADED_ARTICLES_PATH, downloaded_articles)

        except Exception as e:
            print(f"Error processing article {doi}: {e}")

        # Respect API rate limit delay
        time.sleep(API_DELAY)

    print("Download process complete.")

if __name__ == "__main__":
    main()
