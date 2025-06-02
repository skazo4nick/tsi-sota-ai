"""
openalex_publication_retriever.py
-------------------------------
Publication (works) search and retrieval using pyalex.
"""

from pyalex import Works
from typing import Any, Dict, List, Optional

class OpenAlexPublicationRetriever:
    """
    Provides methods to search and retrieve publications (works) from OpenAlex using pyalex.
    """
    def __init__(self, mailto: Optional[str] = None):
        self.mailto = mailto

    def search_by_title(self, title: str, per_page: int = 10) -> List[Dict[str, Any]]:
        """
        Search for works by title.
        """
        results = Works().filter(title=title).paginate(per_page=per_page)
        return [w for w in results]

    def search_by_doi(self, doi: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a work by DOI.
        """
        results = Works().filter(doi=doi)
        for w in results:
            return w
        return None

    def search_by_author(self, author_id: str, per_page: int = 10) -> List[Dict[str, Any]]:
        """
        Search for works by author OpenAlex ID.
        """
        results = Works().filter(author=author_id).paginate(per_page=per_page)
        return [w for w in results]

    def search_by_any(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Generic search for works using any OpenAlex filter fields.
        """
        results = Works().filter(**kwargs)
        return [w for w in results]
