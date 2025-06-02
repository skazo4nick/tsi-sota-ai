"""
test_openalex_author_retriever.py
-------------------------------
Unit tests for openalex_author_retriever.py
"""
import unittest
from unittest.mock import patch, MagicMock
from app.openalex_author_retriever import OpenAlexAuthorRetriever

class TestOpenAlexAuthorRetriever(unittest.TestCase):
    @patch("app.openalex_author_retriever.Authors")
    def test_search_by_name(self, mock_authors):
        mock_authors.return_value.filter.return_value.paginate.return_value = [{"id": "A1"}, {"id": "A2"}]
        retriever = OpenAlexAuthorRetriever()
        results = retriever.search_by_name("Smith")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["id"], "A1")

    @patch("app.openalex_author_retriever.Authors")
    def test_get_by_id(self, mock_authors):
        mock_authors.return_value.filter.return_value = iter([{"id": "A1"}])
        retriever = OpenAlexAuthorRetriever()
        result = retriever.get_by_id("A1")
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "A1")

if __name__ == "__main__":
    unittest.main()
