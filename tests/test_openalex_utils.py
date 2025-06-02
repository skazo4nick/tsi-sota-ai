"""
test_openalex_utils.py
---------------------
Unit tests for openalex_utils.py
"""
import unittest
from app.openalex_utils import OpenAlexUtils

class TestOpenAlexUtils(unittest.TestCase):
    def test_normalize_openalex_id(self):
        norm = OpenAlexUtils.normalize_openalex_id("W123456")
        self.assertEqual(norm, "https://openalex.org/W123456")
        norm2 = OpenAlexUtils.normalize_openalex_id("https://openalex.org/W123456")
        self.assertEqual(norm2, "https://openalex.org/W123456")

    def test_safe_get(self):
        d = {"a": {"b": {"c": 42}}}
        self.assertEqual(OpenAlexUtils.safe_get(d, "a", "b", "c"), 42)
        self.assertIsNone(OpenAlexUtils.safe_get(d, "a", "x"))
        self.assertEqual(OpenAlexUtils.safe_get(d, "a", "x", default=0), 0)

if __name__ == "__main__":
    unittest.main()
