"""
test_openalex_publication_retriever.py
--------------------------------------
Unit tests for openalex_publication_retriever.py
"""
import unittest
from unittest.mock import patch, MagicMock
from app.openalex_publication_retriever import OpenAlexPublicationRetriever

class TestOpenAlexPublicationRetriever(unittest.TestCase):
    @patch("app.openalex_publication_retriever.Works")
    def test_search_by_title(self, mock_works):
        mock_works.return_value.filter.return_value.paginate.return_value = [{"id": "W1"}, {"id": "W2"}]
        retriever = OpenAlexPublicationRetriever()
        results = retriever.search_by_title("AI")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["id"], "W1")

    # @patch("app.openalex_publication_retriever.Works")
    # def test_search_by_doi(self, mock_works):
    #     mock_works.return_value.filter.return_value.paginate.return_value = iter([{"id": "W1", "doi": "10.1234/abc"}])
    #     retriever = OpenAlexPublicationRetriever()
    #     result = retriever.search_by_doi("10.1234/abc")
    #     self.assertIsNotNone(result)
    #     self.assertEqual(result["doi"], "10.1234/abc")

    @patch("app.openalex_publication_retriever.Works")
    def test_search_by_author(self, mock_works):
        mock_works.return_value.filter.return_value.paginate.return_value = [{"id": "W1"}]
        retriever = OpenAlexPublicationRetriever()
        results = retriever.search_by_author("A1")
        self.assertEqual(len(results), 1)

    @patch("app.openalex_publication_retriever.Works")
    def test_search_by_any(self, mock_works):
        mock_works.return_value.filter.return_value = [{"id": "W1"}, {"id": "W2"}]
        retriever = OpenAlexPublicationRetriever()
        results = retriever.search_by_any(title="AI")
        self.assertEqual(len(results), 2)

if __name__ == "__main__":
    unittest.main()
