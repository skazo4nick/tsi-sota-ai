"""
openalex_utils.py
----------------
Helpers for normalization, error handling, and conversion for OpenAlex/pyalex integration.
"""

from typing import Any, Dict

class OpenAlexUtils:
    @staticmethod
    def normalize_openalex_id(openalex_id: str) -> str:
        """
        Normalize OpenAlex IDs to standard format (e.g., add prefix if missing).
        """
        if not openalex_id.startswith("https://openalex.org/"):
            return f"https://openalex.org/{openalex_id}"
        return openalex_id

    @staticmethod
    def safe_get(d: Dict[str, Any], *keys, default=None):
        """
        Safely get a nested value from a dict.
        """
        for key in keys:
            if isinstance(d, dict) and key in d:
                d = d[key]
            else:
                return default
        return d
