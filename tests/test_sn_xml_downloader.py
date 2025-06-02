import os
import sys
import json
import unittest
from unittest.mock import patch, MagicMock
from sn_custom_client.sn_openaccess_client import SpringerNatureOpenAccessClient

# Add the app directory to sys.path to import sn_xml_downloader
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(current_dir, "..", "app")
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

import sn_xml_downloader

class TestSpringerNatureDownloader(unittest.TestCase):
    @patch("sn_xml_downloader.SpringerNatureOpenAccessClient")
    def test_check_article_existence_true(self, mock_client):
        mock_client.return_value.article_exists.return_value = True
        self.assertTrue(sn_xml_downloader.check_article_existence("10.1234/abc"))

    @patch("sn_xml_downloader.SpringerNatureOpenAccessClient")
    def test_check_article_existence_false(self, mock_client):
        mock_client.return_value.article_exists.return_value = False
        self.assertIsNone(sn_xml_downloader.check_article_existence("10.1234/xyz"))

    @patch("sn_xml_downloader.SpringerNatureOpenAccessClient")
    @patch("sn_xml_downloader.is_article_downloaded", return_value=False)
    @patch("sn_xml_downloader._update_downloaded_articles_tracking")
    def test_download_xml_full_text_success(self, mock_update, mock_is_downloaded, mock_client):
        mock_client.return_value.download_xml.return_value = "/tmp/test.xml"
        result = sn_xml_downloader.download_xml_full_text("10.1234/abc")
        self.assertEqual(result, "/tmp/test.xml")
        mock_update.assert_called_once()

    @patch("sn_xml_downloader.SpringerNatureOpenAccessClient")
    @patch("sn_xml_downloader.is_article_downloaded", return_value=True)
    def test_download_xml_full_text_already_downloaded(self, mock_is_downloaded, mock_client):
        result = sn_xml_downloader.download_xml_full_text("10.1234/abc")
        self.assertIsNone(result)

    @patch("sn_xml_downloader.SpringerNatureOpenAccessClient")
    @patch("sn_xml_downloader.is_article_downloaded", return_value=False)
    @patch("sn_xml_downloader._update_downloaded_articles_tracking")
    def test_advanced_query_download(self, mock_update, mock_is_downloaded, mock_client):
        mock_client.return_value.advanced_query.return_value = [
            {"doi": "10.1234/abc"}, {"doi": "10.1234/def"}
        ]
        mock_client.return_value.download_xml.side_effect = ["/tmp/abc.xml", "/tmp/def.xml"]
        results = sn_xml_downloader.advanced_query_download("author:Smith", show_progress=False)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["status"], "success")
        self.assertEqual(results[1]["status"], "success")

def load_test_articles():
    """
    Loads the JSON list of articles from:
    ../app/system_data/json_references/test_articles.json
    """
    json_path = os.path.join(app_dir, "system_data", "json_references", "test_articles.json")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading test articles: {e}")
        return []

def save_found_articles(found_articles):
    """
    Saves the list of found articles to:
    ../app/system_data/sn_open_access_articles.json
    """
    output_path = os.path.join(app_dir, "system_data", "sn_open_access_articles.json")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(found_articles, f, indent=4)
        print(f"\nFound articles successfully saved to: {output_path}")
    except Exception as e:
        print(f"Error saving found articles: {e}")

def main():
    articles = load_test_articles()
    if not articles:
        print("No test articles found. Exiting.")
        return

    found_articles = []
    for article in articles:
        doi = article.get("doi")
        if not doi:
            print(f"Article missing DOI: {article}")
            continue

        print(f"\nChecking existence for DOI: {doi}")
        result = sn_xml_downloader.check_article_existence(doi)
        if result:
            print(f"Article with DOI {doi} exists in Springer Nature Open Access.")
            # Store a summary; you may choose to store result or a combination of test article info and API response.
            found_articles.append({
                "doi": doi,
                "title": article.get("title"),
                "found_metadata": result
            })
        else:
            print(f"Article with DOI {doi} does NOT exist in Springer Nature Open Access.")

    count = len(found_articles)
    print(f"\nTotal articles found in Springer Nature Open Access: {count}")
    save_found_articles(found_articles)

    # Proceed with full text download for found articles
    for article in found_articles:
        doi = article.get("doi")
        print(f"\nDownloading full text for DOI: {doi}")
        xml_filepath = sn_xml_downloader.download_xml_full_text(doi)
        if xml_filepath:
            print(f"Full text XML downloaded successfully to: {xml_filepath}")
        else:
            print(f"Full text download skipped or failed for DOI: {doi}")

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../sn_custom_client')))
    unittest.main()
