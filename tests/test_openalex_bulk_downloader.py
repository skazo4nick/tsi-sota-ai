"""
test_openalex_bulk_downloader.py
-------------------------------
Unit tests for openalex_bulk_downloader.py
"""
import unittest
from unittest.mock import patch, MagicMock
from app.openalex_bulk_downloader import OpenAlexBulkDownloader

class TestOpenAlexBulkDownloader(unittest.TestCase):
    @patch("app.openalex_bulk_downloader.Works")
    def test_bulk_download(self, mock_works):
        # Simulate 3 works returned
        mock_works.return_value.filter.return_value.paginate.return_value = [{"id": "W1"}, {"id": "W2"}, {"id": "W3"}]
        downloader = OpenAlexBulkDownloader()
        results = downloader.bulk_download({"title": "AI"}, max_records=2)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["id"], "W1")
        self.assertEqual(results[1]["id"], "W2")

if __name__ == "__main__":
    unittest.main()
