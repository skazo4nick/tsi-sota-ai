"""
openalex_author_retriever.py
---------------------------
Author search and retrieval using pyalex.
"""

from pyalex import Authors
from typing import Any, Dict, List, Optional

class OpenAlexAuthorRetriever:
    """
    Provides methods to search and retrieve authors from OpenAlex using pyalex.
    """
    def __init__(self, mailto: Optional[str] = None):
        self.mailto = mailto

    def search_by_name(self, name: str, per_page: int = 10) -> List[Dict[str, Any]]:
        """
        Search for authors by name.
        """
        results = Authors().filter(display_name=name).paginate(per_page=per_page)
        return [a for a in results]

    def get_by_id(self, author_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an author by OpenAlex ID.
        """
        results = Authors().filter(id=author_id)
        for a in results:
            return a
        return None
