"""
openaccess.py
-------------
Springer Nature Open Access API client using the official springernature-api-client wrapper.
Supports article existence check, XML/fulltext download, advanced querying, and pagination.
"""

from springernature.client import OpenAccess
from typing import Optional, Dict, Any, List
import os

API_KEY = os.environ.get("SPRINGERNATURE_API_KEY")

class SpringerNatureOpenAccessClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or API_KEY
        if not self.api_key:
            raise ValueError("Springer Nature API key must be provided via argument or SPRINGERNATURE_API_KEY env var.")
        self.client = OpenAccess(self.api_key)

    def article_exists(self, doi: str) -> bool:
        """
        Check if an article exists for the given DOI using the /openaccess endpoint.
        """
        results = self.client.search(q=f"doi:{doi}", p=1)
        return len(results) > 0

    def download_xml(self, doi: str, out_dir: str = "app/system_data") -> Optional[str]:
        """
        Download the XML full text for a given DOI using the /openaccess endpoint.
        Returns the path to the saved XML file, or None if not found.
        """
        results = self.client.search(q=f"doi:{doi}", p=1)
        if not results:
            return None
        record = results[0]
        url = record.get("url")
        if not url or not url.endswith(".xml"):
            return None
        import requests
        r = requests.get(url)
        if r.status_code == 200:
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            xml_filename = f"{doi.replace('/', '_')}.xml"
            xml_path = os.path.join(out_dir, xml_filename)
            with open(xml_path, "wb") as f:
                f.write(r.content)
            return xml_path
        return None

    def advanced_query(self, query: str, filters: Optional[Dict[str, Any]] = None, sort: Optional[str] = None, page_size: int = 20, max_records: int = 100) -> List[Dict[str, Any]]:
        """
        Perform an advanced query with boolean logic, filters, and sorting. Supports pagination.
        Returns a list of records up to max_records.
        """
        params = {"q": query, "p": page_size}
        if filters:
            params.update(filters)
        if sort:
            params["s"] = sort
        results = []
        offset = 0
        while len(results) < max_records:
            params["s"] = offset
            batch = self.client.search(**params)
            if not batch:
                break
            results.extend(batch)
            if len(batch) < page_size:
                break
            offset += page_size
        return results[:max_records]

    def get_metadata(self, doi: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve metadata for a given DOI using the /metadata endpoint.
        """
        return self.client.metadata(doi)

    def get_fulltext(self, doi: str) -> Optional[str]:
        """
        Retrieve the full text (JATS/XML/HTML) for a given DOI using the /fulltext endpoint.
        Returns the full text as a string, or None if not found.
        """
        return self.client.fulltext(doi)
