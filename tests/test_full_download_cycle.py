import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import os
import time
from app.sn_xml_downloader import check_article_existence, download_xml_full_text

SN_OPEN_ACCESS_ARTICLES_JSON = "app/system_data/sn_open_access_articles.json"

def run_full_download_cycle():
    """
    Runs the full download cycle for articles listed in sn_open_access_articles.json.
    """
    try:
        with open(SN_OPEN_ACCESS_ARTICLES_JSON, 'r') as f:
            articles = json.load(f)
    except FileNotFoundError:
        print(f"Error: {SN_OPEN_ACCESS_ARTICLES_JSON} not found.")
        return

    for article_data in articles:
        doi = article_data.get("doi")
        if doi:
            print(f"Processing DOI: {doi}")
            if check_article_existence(doi):
                xml_filepath = download_xml_full_text(doi)
                try:
                    xml_filepath = download_xml_full_text(doi)
                    if xml_filepath:
                        print(f"  XML downloaded successfully to: {xml_filepath}", flush=True)
                    else:
                        print(f"  XML download failed for DOI: {doi}", flush=True)
                except Exception as e:
                    print(f"  Error downloading XML: {e}", flush=True)
            else:
                print(f"  Article with DOI: {doi} not found in Springer Nature Open Access.", flush=True)
        else:
            print("  Warning: Article data missing DOI.", flush=True)
        time.sleep(5)  # Add a 5-second delay between requests to avoid rate limiting

if __name__ == "__main__":
    run_full_download_cycle()
