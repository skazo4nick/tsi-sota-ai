"""
openalex_client.py
------------------
Thin wrapper for pyalex library, handling configuration and base access for OpenAlex API.
"""

from pyalex import Works, Authors, Concepts

class OpenAlexClient:
    """
    Wrapper for pyalex configuration and base access.
    """
    def __init__(self, mailto: str = None):
        """
        Initialize the OpenAlex client.
        Args:
            mailto (str, optional): Contact email for OpenAlex API (recommended).
        """
        self.mailto = mailto
        # pyalex uses environment variable OPENALEX_MAILTO, but can also be set per request

    def works(self):
        """Return the pyalex Works interface."""
        return Works

    def authors(self):
        """Return the pyalex Authors interface."""
        return Authors

    def concepts(self):
        """Return the pyalex Concepts interface."""
        return Concepts
