"""
test_openalex_client.py
----------------------
Unit tests for openalex_client.py
"""
import unittest
from app.openalex_client import OpenAlexClient

class TestOpenAlexClient(unittest.TestCase):
    def test_client_initialization(self):
        client = OpenAlexClient(mailto="test@example.com")
        self.assertEqual(client.mailto, "test@example.com")

    def test_works_interface(self):
        client = OpenAlexClient()
        self.assertIsNotNone(client.works())

    def test_authors_interface(self):
        client = OpenAlexClient()
        self.assertIsNotNone(client.authors())

    def test_concepts_interface(self):
        client = OpenAlexClient()
        self.assertIsNotNone(client.concepts())

if __name__ == "__main__":
    unittest.main()
