"""
test_openalex_concept_retriever.py
---------------------------------
Unit tests for openalex_concept_retriever.py
"""
import unittest
from unittest.mock import patch, MagicMock
from app.openalex_concept_retriever import OpenAlexConceptRetriever

class TestOpenAlexConceptRetriever(unittest.TestCase):
    @patch("app.openalex_concept_retriever.Concepts")
    def test_search_by_name(self, mock_concepts):
        mock_concepts.return_value.filter.return_value.paginate.return_value = [{"id": "C1"}, {"id": "C2"}]
        retriever = OpenAlexConceptRetriever()
        results = retriever.search_by_name("AI")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["id"], "C1")

    # @patch("app.openalex_concept_retriever.Concepts")
    # def test_get_by_id(self, mock_concepts):
    #     mock_concepts.return_value.filter.return_value = [{"id": "C1"}]
    #     retriever = OpenAlexConceptRetriever()
    #     result = retriever.get_by_id("C1")
    #     self.assertIsNotNone(result)
    #     self.assertEqual(result["id"], "C1")

    @patch("app.openalex_concept_retriever.Concepts")
    def test_get_by_id_not_found(self, mock_concepts):
        mock_concepts.return_value.filter.return_value = []
        retriever = OpenAlexConceptRetriever()
        result = retriever.get_by_id("C3")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
