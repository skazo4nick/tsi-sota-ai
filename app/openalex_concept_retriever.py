"""
openalex_concept_retriever.py
----------------------------
Concept/field-of-study search using pyalex.
"""

from pyalex import Concepts
from typing import Any, Dict, List, Optional

class OpenAlexConceptRetriever:
    """
    Provides methods to search and retrieve concepts (fields of study) from OpenAlex using pyalex.
    """
    def __init__(self, mailto: Optional[str] = None):
        self.mailto = mailto

    def search_by_name(self, name: str, per_page: int = 10) -> List[Dict[str, Any]]:
        """
        Search for concepts by name.
        """
        results = Concepts().filter(display_name=name).paginate(per_page=per_page)
        return [c for c in results]

    def get_by_id(self, concept_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a concept by OpenAlex ID.
        """
        results = Concepts().filter(id=concept_id)
        for c in results:
            return c
        return None
