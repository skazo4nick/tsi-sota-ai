"""
openalex_bulk_downloader.py (optional)
--------------------------------------
Batch/bulk download support for OpenAlex works using pyalex.
"""

from pyalex import Works
from typing import Any, Dict, List, Optional

class OpenAlexBulkDownloader:
    """
    Provides methods to download large batches of works from OpenAlex using pyalex.
    """
    def __init__(self, mailto: Optional[str] = None):
        self.mailto = mailto

    def bulk_download(self, filter_kwargs: dict, max_records: int = 1000) -> List[Dict[str, Any]]:
        """
        Download up to max_records works matching filter_kwargs.
        """
        results = Works().filter(**filter_kwargs).paginate(per_page=200)
        batch = []
        for i, w in enumerate(results):
            if i >= max_records:
                break
            batch.append(w)
        return batch
