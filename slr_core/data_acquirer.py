import json
import os
from datetime import datetime
from typing import Optional, Dict, List, Any # Added Optional, Dict, List, Any
from .api_clients import CoreAPIClient, ArxivAPIClient, OpenAlexAPIClient # Relative import
from .config_manager import ConfigManager # Added ConfigManager import

class DataAcquirer:
    SUPPORTED_SOURCES = ["CORE", "arXiv", "OpenAlex"]

    def __init__(self, config_manager: Optional[ConfigManager] = None):
        """
        Initializes the DataAcquirer.

        Args:
            config_manager (Optional[ConfigManager]): Instance of ConfigManager.
        """
        self.config_manager = config_manager

        if self.config_manager:
            self.raw_data_dir = self.config_manager.get("data_paths.raw_data_dir", "data/slr_raw/")
            self.clients: Dict[str, Any] = { # Added type hint for self.clients
                "CORE": CoreAPIClient(config_manager=self.config_manager),
                "arXiv": ArxivAPIClient(config_manager=self.config_manager),
                "OpenAlex": OpenAlexAPIClient(config_manager=self.config_manager)
            }
        else:
            self.raw_data_dir = "data/slr_raw/" # Default if no config manager
            self.clients: Dict[str, Any] = { # Added type hint for self.clients
                "CORE": CoreAPIClient(),
                "arXiv": ArxivAPIClient(),
                "OpenAlex": OpenAlexAPIClient()
            }

        os.makedirs(self.raw_data_dir, exist_ok=True)

    def fetch_all_sources(self, query: str, start_year: int, end_year: int, max_results_per_source: int = 100) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetches publications from all supported sources for a given query and timeframe.

        Args:
            query (str): The search query.
            start_year (int): The start year for the search.
            end_year (int): The end year for the search.
            max_results_per_source (int): Max results to fetch from each source.

        Returns:
            dict: A dictionary where keys are source names and values are lists of fetched publications.
        """
        all_results: Dict[str, List[Dict[str, Any]]] = {} # Added type hint
        for source_name in self.SUPPORTED_SOURCES:
            print(f"Fetching from {source_name}...")
            try:
                client = self.clients.get(source_name)
                if client:
                    results = client.fetch_publications(query, start_year, end_year, max_results_per_source)
                    all_results[source_name] = results
                    self._save_raw_data(results, source_name, query, start_year, end_year)
                else:
                    print(f"Warning: Client for source '{source_name}' not found.")
                    all_results[source_name] = []
            except Exception as e:
                print(f"Error fetching from {source_name}: {e}")
                all_results[source_name] = []

        print("Data acquisition from all sources complete.")
        return all_results

    def _save_raw_data(self, data: List[Dict[str, Any]], source_name: str, query: str, start_year: int, end_year: int):
        """
        Saves the raw fetched data to a JSON file.
        Filename includes source, query parts, date range, and timestamp.
        """
        if not data:
            return

        # Sanitize query for filename
        safe_query = "".join(c if c.isalnum() else "_" for c in query[:30]) # First 30 chars, sanitized
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{source_name}_{safe_query}_{start_year}-{end_year}_{timestamp}.json"
        filepath = os.path.join(self.raw_data_dir, filename)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"Saved raw data for {source_name} to {filepath}")
        except Exception as e:
            print(f"Error saving raw data for {source_name}: {e}")

    def load_raw_data_for_query(self, source_name: str, query: str, start_year: int, end_year: int) -> List[Dict[str, Any]]:
        """
        Placeholder for loading previously saved raw data for a specific query.
        This would involve finding the relevant file(s) in raw_data_dir.
        """
        print(f"Placeholder: Load raw data for {source_name}, query '{query}', {start_year}-{end_year}")
        # Logic to find and load files would go here.
        return []

if __name__ == '__main__':
    # Example Usage (assuming api_clients.py provides dummy data for now)
    # Ensure slr_core is in PYTHONPATH or this script is run in a way that Python can find it.
    # e.g., run from the project root: python -m slr_core.data_acquirer

    # If running this file directly for tests, you might need:
    # import sys
    # sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from slr_core.config_manager import ConfigManager # Adjusted import for potential direct run

    print("--- Testing DataAcquirer with ConfigManager ---")
    cfg_mgr = ConfigManager() # Loads default config
    acquirer = DataAcquirer(config_manager=cfg_mgr)

    search_query = cfg_mgr.get("default_search_params.query", "agentic AI in SCM") # Example of using config
    s_year = cfg_mgr.get("default_search_params.start_year", 2022)
    e_year = cfg_mgr.get("default_search_params.end_year", 2023)
    max_res = cfg_mgr.get("default_search_params.max_results_per_source", 5)

    print(f"Using query: '{search_query}', years: {s_year}-{e_year}, max_results: {max_res}")

    fetched_data = acquirer.fetch_all_sources(search_query, s_year, e_year, max_results_per_source=max_res)

    for source, results in fetched_data.items():
        print(f"--- Results from {source} ---")
        if results:
            for i, paper in enumerate(results[:2]): # Print first 2 results
                print(f"  Paper {i+1}: {paper.get('title', 'N/A')}")
        else:
            print("  No results.")

    print("\n--- Testing DataAcquirer without ConfigManager (fallback behavior) ---")
    acquirer_no_cfg = DataAcquirer()
    fetched_data_no_cfg = acquirer_no_cfg.fetch_all_sources("fallback query", 2023, 2023, 2)
    for source, results in fetched_data_no_cfg.items():
        print(f"--- Results from {source} (no_cfg) ---")
        if results:
            print(f"  {results[0].get('title', 'N/A')}")
        else:
            print("  No results.")
