import os
import time
import requests
import abc # Abstract Base Classes
from datetime import datetime
from typing import Optional, Dict, Any, List # Added Optional, Dict, Any, List for type hinting
from .config_manager import ConfigManager # Added import

# Removed module-level CORE_API_KEY and OPENALEX_EMAIL fetching
# Removed get_api_key helper function

def make_request_with_retry(url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None,
                            method: str = "GET", data: Optional[Dict[str, Any]] = None,
                            max_retries: int = 3, delay_seconds: int = 5) -> Optional[Dict[str, Any]]:
    """Makes an HTTP request with a simple retry mechanism."""
    for attempt in range(max_retries):
        try:
            response = requests.request(method, url, params=params, headers=headers, json=data)
            response.raise_for_status() # Raise an exception for HTTP errors (4XX, 5XX)
            return response.json() # Assuming JSON response
        except requests.exceptions.RequestException as e:
            print(f"Request failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(delay_seconds)
            else:
                raise # Re-raise the exception after the last attempt
    return None # Should not be reached if an exception is raised on the last attempt


# --- Abstract Base Class for API Clients ---
class BaseAPIClient(abc.ABC):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    @abc.abstractmethod
    def fetch_publications(self, query: str, start_year: int, end_year: int, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Fetches publications based on a query and timeframe.
        Returns:
            list: A list of publication metadata objects (dictionaries).
        """
        pass

    @abc.abstractmethod
    def _parse_publication_data(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses raw API item data into a standardized format.
        Returns:
            dict: Standardized publication metadata.
        """
        pass

# --- CORE API Client ---
class CoreAPIClient(BaseAPIClient):
    BASE_URL = "https://api.core.ac.uk/v3/" # Default Base URL

    def __init__(self, config_manager: Optional[ConfigManager] = None):
        api_key_val: Optional[str] = None
        effective_base_url: str = self.BASE_URL

        if config_manager:
            api_key_val = config_manager.get_api_key("CORE")
            base_url_from_config = config_manager.get("api_settings.CORE.base_url")
            if base_url_from_config:
                effective_base_url = base_url_from_config
        else:
            api_key_val = os.getenv("CORE_API_KEY")

        super().__init__(api_key_val) # Pass api_key to BaseAPIClient's __init__
        self.base_url = effective_base_url # Set the instance base_url

        if not self.api_key:
            print("Warning: CORE_API_KEY not found. CORE API calls may fail or use dummy data.")
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

    def fetch_publications(self, query: str, start_year: int, end_year: int, max_results: int = 100) -> List[Dict[str, Any]]:
        print(f"[CoreAPIClient] Fetching from {self.base_url}: '{query}' from {start_year}-{end_year} (max: {max_results})")
        # Example query construction (simplified)
        # core_query = f'({query}) AND yearPublished:>={start_year} AND yearPublished:<={end_year}'
        # params = {"q": core_query, "limit": min(max_results, 100), "scroll": True} # Example for scroll
        # search_url = f"{self.base_url}search/works"
        # Note: Actual pagination might require multiple calls and handling of 'scrollId' or offset.
        # response_data = make_request_with_retry(search_url, params=params, headers=self.headers)
        # if response_data and "results" in response_data:
        #    return [self._parse_publication_data(item) for item in response_data["results"]]
        return [{"title": "Dummy CORE Paper 1", "doi": "10.xxxx/core1", "yearPublished": start_year}]

    def _parse_publication_data(self, item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "doi": item.get("doi"),
            "title": item.get("title"),
            "abstract": item.get("abstract"),
            "authors": [author.get("name") for author in item.get("authors", []) if isinstance(author, dict) and author.get("name")],
            "publication_date": str(item.get("yearPublished")),
            "keywords": item.get("keywords", []),
            "source": "CORE"
        }

# --- arXiv API Client ---
class ArxivAPIClient(BaseAPIClient):
    BASE_URL = "http://export.arxiv.org/api/" # Default Base URL

    def __init__(self, config_manager: Optional[ConfigManager] = None):
        super().__init__() # arXiv doesn't strictly require an API key for search
        effective_base_url: str = self.BASE_URL
        if config_manager:
            base_url_from_config = config_manager.get("api_settings.arXiv.base_url")
            if base_url_from_config:
                effective_base_url = base_url_from_config
        self.base_url = effective_base_url

    def fetch_publications(self, query: str, start_year: int, end_year: int, max_results: int = 100) -> List[Dict[str, Any]]:
        print(f"[ArxivAPIClient] Fetching from {self.base_url}: '{query}' from {start_year}-{end_year} (max: {max_results})")
        # Actual implementation needs XML parsing, complex date filtering, etc.
        return [{"title": "Dummy arXiv Paper 1", "doi": None, "id": "2301.0001v1", "published_date": f"{start_year}-01-01"}]

    def _parse_publication_data(self, entry: Dict[str, Any]) -> Dict[str, Any]: # Assuming entry is dict after XML parsing
        arxiv_id = entry.get("id", "").split('/')[-1]
        title = entry.get("title", "N/A")
        abstract = entry.get("summary", "N/A")
        return {
            "doi": entry.get("doi"),
            "arxiv_id": arxiv_id,
            "title": title,
            "abstract": abstract,
            "authors": [author.get("name") for author in entry.get("authors", []) if isinstance(author, dict) and author.get("name")],
            "publication_date": entry.get("published_date"),
            "keywords": [tag.get("term") for tag in entry.get("categories", []) if isinstance(tag, dict) and tag.get("term")],
            "source": "arXiv"
        }

# --- OpenAlex API Client ---
class OpenAlexAPIClient(BaseAPIClient):
    BASE_URL = "https://api.openalex.org/" # Default Base URL

    def __init__(self, config_manager: Optional[ConfigManager] = None):
        super().__init__()

        email_for_polite_pool: str = "your_email@example.com" # Default polite pool email
        effective_base_url: str = self.BASE_URL

        if config_manager:
            configured_email = config_manager.get_api_key("OPENALEX_EMAIL") # This method handles env var name
            if configured_email:
                email_for_polite_pool = configured_email

            base_url_from_config = config_manager.get("api_settings.OpenAlex.base_url")
            if base_url_from_config:
                effective_base_url = base_url_from_config
        else:
            env_email = os.getenv("OPENALEX_EMAIL")
            if env_email:
                email_for_polite_pool = env_email

        self.base_url = effective_base_url
        self.headers = {'User-Agent': f'SLRAnalyticsApp/0.1 (mailto:{email_for_polite_pool})'}

    def fetch_publications(self, query: str, start_year: int, end_year: int, max_results: int = 100) -> List[Dict[str, Any]]:
        print(f"[OpenAlexAPIClient] Fetching from {self.base_url} with User-Agent {self.headers.get('User-Agent')}: '{query}' from {start_year}-{end_year} (max: {max_results})")
        # params = {
        #     'search': query,
        #     'filter': f'publication_year:{start_year}-{end_year}',
        #     'per_page': min(max_results, 200),
        #     # 'mailto': email_for_polite_pool # OpenAlex doesn't use mailto in query params, it's for User-Agent
        # }
        # search_url = f"{self.base_url}works"
        # response_data = make_request_with_retry(search_url, params=params, headers=self.headers)
        # if response_data and "results" in response_data:
        #     return [self._parse_publication_data(item) for item in response_data["results"]]
        return [{"title": "Dummy OpenAlex Paper 1", "doi": "10.xxxx/oa1", "publication_year": start_year}]

    def _parse_publication_data(self, item: Dict[str, Any]) -> Dict[str, Any]:
        doi_url = item.get("doi")
        doi = doi_url.replace("https://doi.org/", "") if doi_url else None

        abstract = "N/A" # Placeholder for abstract reconstruction
        if item.get("abstract_inverted_index"):
             # This is a very simplified reconstruction. Real one is complex.
            aii = item["abstract_inverted_index"]
            words = [""] * sum(len(positions) for positions in aii.values())
            for word, positions in aii.items():
                for pos in positions:
                    if pos < len(words): words[pos] = word
            abstract = " ".join(filter(None, words))


        return {
            "doi": doi,
            "title": item.get("display_name"),
            "abstract": abstract,
            "authors": [author.get("author", {}).get("display_name") for author in item.get("authorships", []) if isinstance(author, dict)],
            "publication_date": str(item.get("publication_year")),
            "keywords": [concept.get("display_name") for concept in item.get("concepts", []) if isinstance(concept, dict) and concept.get("display_name")],
            "source": "OpenAlex"
        }

# --- Semantic Scholar API Client ---
class SemanticScholarAPIClient(BaseAPIClient):
    BASE_URL = "https://api.semanticscholar.org/graph/v1/"
    RECOMMENDATIONS_URL = "https://api.semanticscholar.org/recommendations/v1/"
    
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        api_key_val: Optional[str] = None
        effective_base_url: str = self.BASE_URL
        
        if config_manager:
            api_key_val = config_manager.get_api_key("SEMANTIC_SCHOLAR_API_KEY")
            base_url_from_config = config_manager.get("api_settings.semantic_scholar.base_url")
            if base_url_from_config:
                effective_base_url = base_url_from_config
        else:
            api_key_val = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
        
        super().__init__(api_key_val)
        self.base_url = effective_base_url
        self.recommendations_url = self.RECOMMENDATIONS_URL
        
        # Set up headers
        self.headers = {
            'User-Agent': 'tsi-sota-ai/1.0 (research@example.com)',  # Replace with your contact
            'Content-Type': 'application/json'
        }
        
        if self.api_key:
            self.headers['x-api-key'] = self.api_key
        else:
            print("Info: No Semantic Scholar API key found. Using public access with shared rate limits.")

    def fetch_publications(self, query: str, start_year: int, end_year: int, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch publications from Semantic Scholar API using paper bulk search endpoint.
        
        Args:
            query: Search query string
            start_year: Start year for publication date filter
            end_year: End year for publication date filter
            max_results: Maximum number of results to return
        
        Returns:
            List of standardized publication dictionaries
        """
        print(f"[SemanticScholarAPIClient] Fetching from {self.base_url}: '{query}' from {start_year}-{end_year} (max: {max_results})")
        
        # Use paper bulk search endpoint for better performance
        search_url = f"{self.base_url}paper/search/bulk"
        
        # Construct query parameters
        params = {
            'query': query,
            'year': f"{start_year}-{end_year}",
            'fields': 'title,abstract,authors,year,citationCount,referenceCount,fieldsOfStudy,doi,externalIds,publicationTypes,venue,openAccessPdf'
        }
        
        all_results = []
        retrieved_count = 0
        
        try:
            while retrieved_count < max_results:
                # Calculate remaining results needed
                batch_size = min(1000, max_results - retrieved_count)  # Semantic Scholar max per request
                
                # Add pagination token if we have one
                current_params = params.copy()
                if hasattr(self, '_current_token') and self._current_token:
                    current_params['token'] = self._current_token
                
                # Make the request
                response_data = make_request_with_retry(
                    search_url, 
                    params=current_params, 
                    headers=self.headers,
                    max_retries=3,
                    delay_seconds=1  # Respect 1 req/sec rate limit
                )
                
                if not response_data:
                    print("No response data received from Semantic Scholar API")
                    break
                
                # Check if we have data
                if "data" not in response_data:
                    print("No 'data' field in response")
                    break
                
                # Process the batch
                batch_results = [self._parse_publication_data(item) for item in response_data["data"]]
                all_results.extend(batch_results)
                retrieved_count += len(batch_results)
                
                print(f"Retrieved {len(batch_results)} papers in this batch, total: {retrieved_count}")
                
                # Check for continuation token
                if "token" in response_data and retrieved_count < max_results:
                    self._current_token = response_data["token"]
                    time.sleep(1)  # Rate limiting
                else:
                    break
            
            # Clean up token
            if hasattr(self, '_current_token'):
                delattr(self, '_current_token')
                
            return all_results[:max_results]  # Ensure we don't exceed max_results
            
        except Exception as e:
            print(f"Error fetching from Semantic Scholar API: {e}")
            return []

    def fetch_paper_recommendations(self, positive_paper_ids: List[str], negative_paper_ids: Optional[List[str]] = None, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch paper recommendations based on seed papers.
        
        Args:
            positive_paper_ids: List of paper IDs to use as positive seeds
            negative_paper_ids: Optional list of paper IDs to use as negative seeds
            max_results: Maximum number of recommendations to return
        
        Returns:
            List of standardized publication dictionaries
        """
        print(f"[SemanticScholarAPIClient] Fetching recommendations for {len(positive_paper_ids)} positive seeds")
        
        recommendations_url = f"{self.recommendations_url}papers"
        
        # Prepare request data
        request_data = {
            "positivePaperIds": positive_paper_ids
        }
        
        if negative_paper_ids:
            request_data["negativePaperIds"] = negative_paper_ids
        
        # Query parameters
        params = {
            "fields": "title,abstract,authors,year,citationCount,referenceCount,fieldsOfStudy,doi,externalIds",
            "limit": str(min(max_results, 500))  # API max is 500
        }
        
        try:
            response_data = make_request_with_retry(
                recommendations_url,
                params=params,
                headers=self.headers,
                method="POST",
                data=request_data,
                delay_seconds=1
            )
            
            if response_data and "recommendedPapers" in response_data:
                results = [self._parse_publication_data(item) for item in response_data["recommendedPapers"]]
                print(f"Retrieved {len(results)} recommended papers")
                return results
            else:
                print("No recommendations returned")
                return []
                
        except Exception as e:
            print(f"Error fetching recommendations from Semantic Scholar API: {e}")
            return []

    def search_papers_advanced(self, query: str, filters: Optional[Dict[str, Any]] = None, sort: Optional[str] = None, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Advanced paper search with filters and sorting.
        
        Args:
            query: Search query with advanced syntax support
            filters: Optional filters (year, venue, fieldsOfStudy, etc.)
            sort: Optional sort parameter (publicationDate, citationCount, paperId)
            max_results: Maximum number of results to return
        
        Returns:
            List of standardized publication dictionaries
        """
        print(f"[SemanticScholarAPIClient] Advanced search: '{query}' with filters: {filters}")
        
        search_url = f"{self.base_url}paper/search/bulk"
        
        # Start with base parameters
        params = {
            'query': query,
            'fields': 'title,abstract,authors,year,citationCount,referenceCount,fieldsOfStudy,doi,externalIds,publicationTypes,venue,openAccessPdf'
        }
        
        # Apply filters
        if filters:
            if 'year' in filters:
                params['year'] = filters['year']
            if 'venue' in filters:
                params['venue'] = filters['venue']
            if 'fieldsOfStudy' in filters:
                params['fieldsOfStudy'] = filters['fieldsOfStudy']
            if 'publicationTypes' in filters:
                params['publicationTypes'] = filters['publicationTypes']
            if 'openAccessPdf' in filters:
                params['openAccessPdf'] = filters['openAccessPdf']
            if 'minCitationCount' in filters:
                params['minCitationCount'] = str(filters['minCitationCount'])
        
        # Apply sorting
        if sort:
            params['sort'] = sort
        
        try:
            response_data = make_request_with_retry(
                search_url,
                params=params,
                headers=self.headers,
                delay_seconds=1
            )
            
            if response_data and "data" in response_data:
                results = [self._parse_publication_data(item) for item in response_data["data"]]
                print(f"Advanced search retrieved {len(results)} papers")
                return results[:max_results]
            else:
                print("No results from advanced search")
                return []
                
        except Exception as e:
            print(f"Error in advanced search: {e}")
            return []

    def get_paper_details(self, paper_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific paper.
        
        Args:
            paper_id: Semantic Scholar paper ID
        
        Returns:
            Standardized publication dictionary or None if not found
        """
        details_url = f"{self.base_url}paper/{paper_id}"
        
        params = {
            'fields': 'title,abstract,authors,year,citationCount,referenceCount,fieldsOfStudy,doi,externalIds,publicationTypes,venue,openAccessPdf,citations,references'
        }
        
        try:
            response_data = make_request_with_retry(
                details_url,
                params=params,
                headers=self.headers,
                delay_seconds=1
            )
            
            if response_data:
                return self._parse_publication_data(response_data)
            else:
                return None
                
        except Exception as e:
            print(f"Error fetching paper details for {paper_id}: {e}")
            return None

    def _parse_publication_data(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse Semantic Scholar API response into standardized format.
        
        Args:
            item: Raw API response item
        
        Returns:
            Standardized publication dictionary
        """
        # Extract DOI
        doi = item.get("doi")
        if not doi and item.get("externalIds"):
            external_ids = item["externalIds"]
            doi = external_ids.get("DOI")
        
        # Extract authors
        authors = []
        if item.get("authors"):
            authors = [
                author.get("name", "Unknown") 
                for author in item["authors"] 
                if isinstance(author, dict)
            ]
        
        # Extract keywords from fields of study
        keywords = []
        if item.get("fieldsOfStudy"):
            keywords = [
                field for field in item["fieldsOfStudy"] 
                if isinstance(field, str)
            ]
        
        # Extract venue information
        venue = ""
        if item.get("venue"):
            venue = item["venue"]
        
        # Extract publication types
        pub_types = []
        if item.get("publicationTypes"):
            pub_types = item["publicationTypes"]
        
        # Check for open access PDF
        open_access_pdf = None
        if item.get("openAccessPdf"):
            open_access_pdf = item["openAccessPdf"].get("url")
        
        return {
            "doi": doi,
            "title": item.get("title", ""),
            "abstract": item.get("abstract", ""),
            "authors": authors,
            "publication_date": str(item.get("year", "")),
            "keywords": keywords,
            "citation_count": item.get("citationCount", 0),
            "reference_count": item.get("referenceCount", 0),
            "venue": venue,
            "publication_types": pub_types,
            "open_access_pdf": open_access_pdf,
            "paper_id": item.get("paperId"),
            "source": "Semantic Scholar"
        }

if __name__ == '__main__':
    # Ensure slr_core is in PYTHONPATH or adjust path for testing
    # For this example, assume ConfigManager can be imported directly if this script is run
    # as part of a package where slr_core is recognized, or path is adjusted.
    # If running this file directly for tests, you might need:
    # import sys
    # sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    from slr_core.config_manager import ConfigManager # Relative import for example

    print("--- Testing API Clients with ConfigManager ---")
    cfg = ConfigManager() # Will load default config/slr_config.yaml

    print("\n--- CORE API Client Test ---")
    core_client = CoreAPIClient(config_manager=cfg)
    core_client.fetch_publications("supply chain AI", 2022, 2023)

    print("\n--- arXiv API Client Test ---")
    arxiv_client = ArxivAPIClient(config_manager=cfg)
    arxiv_client.fetch_publications("agent logistics", 2022, 2023)

    print("\n--- OpenAlex API Client Test ---")
    openalex_client = OpenAlexAPIClient(config_manager=cfg)
    openalex_client.fetch_publications("LLM SCM", 2022, 2023)

    print("\n--- Semantic Scholar API Client Test ---")
    semantic_scholar_client = SemanticScholarAPIClient(config_manager=cfg)
    semantic_scholar_client.fetch_publications("deep learning", 2022, 2023)

    print("\n--- Testing API Clients without ConfigManager (fallback behavior) ---")
    print("\n--- CORE API Client Test (no config) ---")
    core_client_no_cfg = CoreAPIClient()
    core_client_no_cfg.fetch_publications("test query", 2023, 2023)

    print("\n--- OpenAlex API Client Test (no config) ---")
    openalex_client_no_cfg = OpenAlexAPIClient() # Will use default email or env var
    openalex_client_no_cfg.fetch_publications("test query", 2023, 2023)

    print("\n--- Semantic Scholar API Client Test (no config) ---")
    semantic_scholar_client_no_cfg = SemanticScholarAPIClient() # Will use public access
    semantic_scholar_client_no_cfg.fetch_publications("test query", 2023, 2023)
