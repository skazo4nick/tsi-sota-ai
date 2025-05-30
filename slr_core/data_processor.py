import pandas as pd
import os
from typing import List, Dict, Any, Optional # Added Optional
from .config_manager import ConfigManager # Added ConfigManager import

class DataProcessor:
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        """
        Initializes the DataProcessor.

        Args:
            config_manager (Optional[ConfigManager]): Instance of ConfigManager.
        """
        self.config_manager = config_manager
        if self.config_manager:
            self.processed_data_dir = self.config_manager.get("data_paths.processed_data_dir", "data/slr_processed/")
        else:
            self.processed_data_dir = "data/slr_processed/" # Default if no config manager

        os.makedirs(self.processed_data_dir, exist_ok=True)

    def process_raw_data(self, all_fetched_data: Dict[str, List[Dict[str, Any]]]) -> pd.DataFrame:
        """
        Processes raw data from multiple sources, standardizes, and consolidates it.

        Args:
            all_fetched_data (Dict[str, List[Dict[str, Any]]]):
                A dictionary where keys are source names (e.g., "CORE", "arXiv")
                and values are lists of raw publication data dictionaries from that source.
                This raw data is assumed to be the output of the _parse_publication_data
                methods in the respective API clients.

        Returns:
            pd.DataFrame: A DataFrame containing consolidated, standardized, and cleaned publication data.
        """
        standardized_articles = []
        for source_name, articles in all_fetched_data.items():
            for article_data in articles:
                # The _parse_publication_data methods in api_clients should already provide a good level of standardization.
                # This step ensures fields are consistently named and typed if further tweaks are needed across sources.
                standardized_article = self._standardize_article_fields(article_data, source_name)
                if standardized_article:
                    standardized_articles.append(standardized_article)

        if not standardized_articles:
            print("No articles to process after initial standardization.")
            return pd.DataFrame()

        # Consolidate into a DataFrame
        df = pd.DataFrame(standardized_articles)
        print(f"Consolidated {len(df)} articles into a DataFrame.")

        # Basic Cleaning
        df = self._clean_data(df)

        # Deduplication
        df = self._deduplicate_data(df)

        print(f"Processing complete. Resulting DataFrame has {len(df)} articles.")
        return df

    def _standardize_article_fields(self, article_data: Dict[str, Any], source_name: str) -> Dict[str, Any]:
        """
        Ensures consistent field names and types for an article.
        The _parse_publication_data in each client should do most of this.
        This is a safety net or for further common transformations.
        """
        # Example: Ensure 'publication_date' is a string or datetime object consistently
        # For now, assume _parse_publication_data from clients did a good job.
        # Add source if not already there (though it should be)
        if 'source' not in article_data:
            article_data['source'] = source_name

        # Ensure essential fields exist, even if None
        # (doi, arxiv_id, title, abstract, authors, publication_date, keywords, source)
        # This will be more important once real data comes in.
        # For dummy data, this might not be critical yet.

        # Example: Ensure authors is always a list of strings
        if 'authors' in article_data and isinstance(article_data['authors'], list):
            article_data['authors'] = [str(author) for author in article_data['authors'] if author]
        elif 'authors' not in article_data:
             article_data['authors'] = []


        # Example: Ensure keywords is always a list of strings
        if 'keywords' in article_data and isinstance(article_data['keywords'], list):
            article_data['keywords'] = [str(kw) for kw in article_data['keywords'] if kw]
        elif 'keywords' not in article_data:
            article_data['keywords'] = []

        return article_data

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Performs basic data cleaning operations.
        """
        print("Performing basic data cleaning...")
        # Example: Drop rows where essential information like 'title' or 'abstract' is missing
        # df.dropna(subset=['title', 'abstract'], inplace=True)
        # For now, this is commented out as dummy data might be sparse.

        # Example: Convert 'publication_date' to datetime objects if not already
        # df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce')

        # Fill missing abstracts with empty string if any (important for embedding)
        if 'abstract' in df.columns:
            df['abstract'] = df['abstract'].fillna('')
        else:
            df['abstract'] = ''

        if 'title' in df.columns:
            df['title'] = df['title'].fillna('')
        else:
            df['title'] = ''

        print(f"DataFrame shape after cleaning: {df.shape}")
        return df

    def _deduplicate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Deduplicates data based on DOI, then potentially by title/abstract.
        """
        if df.empty:
            return df

        print("Performing deduplication...")
        initial_count = len(df)

        # Prioritize DOI for deduplication
        if 'doi' in df.columns:
            # Ensure DOIs are strings and comparable, handle None/NaN
            df['doi_norm'] = df['doi'].astype(str).str.lower().str.strip()
            df['doi_norm'].replace(['none', 'nan', ''], pd.NA, inplace=True)

            # Keep first, drop duplicates based on normalized DOI, ignoring NA values
            df.sort_values(by='doi_norm', na_position='last', inplace=True) # Keep non-NA DOIs first
            df_deduplicated_doi = df.drop_duplicates(subset=['doi_norm'], keep='first', ignore_index=True)

            # Separate records that had NA DOIs to apply other deduplication logic if needed
            df_na_doi = df_deduplicated_doi[df_deduplicated_doi['doi_norm'].isna()].copy()
            df_with_doi = df_deduplicated_doi[~df_deduplicated_doi['doi_norm'].isna()].copy()

            print(f"  {len(df_with_doi)} articles after DOI deduplication.")
        else:
            df_with_doi = pd.DataFrame(columns=df.columns) # No DOI column, all are "NA DOI"
            df_na_doi = df.copy()


        # For records without a valid DOI, consider title & abstract similarity (placeholder)
        # This is a complex task. For now, we can do a simple title-based deduplication on df_na_doi.
        if not df_na_doi.empty and 'title' in df_na_doi.columns:
            df_na_doi['title_norm'] = df_na_doi['title'].astype(str).str.lower().str.strip()
            df_na_doi.sort_values(by='title_norm', na_position='last', inplace=True)
            df_na_doi_dedup = df_na_doi.drop_duplicates(subset=['title_norm'], keep='first', ignore_index=True)
            print(f"  {len(df_na_doi_dedup)} articles from non-DOI group after title deduplication.")
            df = pd.concat([df_with_doi, df_na_doi_dedup], ignore_index=True)
        else:
            df = df_with_doi # Only keep the DOI-deduplicated part if no titles or no NA DOIs

        # Clean up temporary columns
        if 'doi_norm' in df.columns:
            df.drop(columns=['doi_norm'], inplace=True)
        if 'title_norm' in df.columns:
            df.drop(columns=['title_norm'], inplace=True)

        print(f"Removed {initial_count - len(df)} duplicate articles. Final count: {len(df)}")
        return df.reset_index(drop=True)

    def save_processed_data(self, df: pd.DataFrame, filename: str = "processed_articles.csv") -> Optional[str]:
        """
        Saves the processed DataFrame to a file.
        Returns the path to the saved file, or None if saving failed.
        """
        if df.empty:
            print("No processed data to save.")
            return None

        filepath = os.path.join(self.processed_data_dir, filename)
        try:
            # For CSV, ensure lists/dicts are stored as strings if not handled otherwise
            # df_to_save = df.copy()
            # for col in ['authors', 'keywords']:
            #    if col in df_to_save.columns:
            #        df_to_save[col] = df_to_save[col].apply(lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x)

            df.to_csv(filepath, index=False)
            print(f"Processed data saved to {filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving processed data: {e}")
            return None

if __name__ == '__main__':
    # Example Usage (using dummy data structure similar to what DataAcquirer might produce)
    # Ensure slr_core is in PYTHONPATH or this script is run in a way that Python can find it.
    # e.g., run from the project root: python -m slr_core.data_processor
    from slr_core.config_manager import ConfigManager # Adjusted import for potential direct run

    print("--- Testing DataProcessor with ConfigManager ---")
    cfg_mgr = ConfigManager() # Loads default config
    processor = DataProcessor(config_manager=cfg_mgr)

    # Simulate fetched data (output of DataAcquirer.fetch_all_sources)
    dummy_fetched_data = {
        "CORE": [
            {"doi": "10.123/core.paper1", "title": "Core Paper A", "abstract": "Abstract for Core A.", "authors": ["Author X"], "publication_date": "2022", "keywords": ["core", "ai"], "source": "CORE"},
            {"doi": "10.123/common.paper", "title": "Common Paper Title", "abstract": "Abstract for Common.", "authors": ["Author Y"], "publication_date": "2023", "keywords": ["ai", "research"], "source": "CORE"}
        ],
        "arXiv": [
            {"doi": None, "arxiv_id": "2301.0001", "title": "arXiv Paper B", "abstract": "Abstract for arXiv B.", "authors": ["Author Z", "Author W"], "publication_date": "2023-01-15", "keywords": ["ml", "cs.AI"], "source": "arXiv"},
            {"doi": "10.123/common.paper", "title": "Common Paper Title", "abstract": "Abstract for Common.", "authors": ["Author Y"], "publication_date": "2023", "keywords": ["ai", "research"], "source": "arXiv"} # Duplicate by DOI
        ],
        "OpenAlex": [
            {"doi": "10.456/oa.paperC", "title": "OpenAlex Paper C", "abstract": "Abstract for OA C.", "authors": ["Author V"], "publication_date": "2022", "keywords": ["openalex", "data"], "source": "OpenAlex"},
            {"doi": "10.123/core.paper1", "title": "Core Paper A", "abstract": "Abstract for Core A.", "authors": ["Author X"], "publication_date": "2022", "keywords": ["core", "ai"], "source": "OpenAlex"} # Duplicate by DOI
        ]
    }

    processed_df = processor.process_raw_data(dummy_fetched_data)

    if not processed_df.empty:
        print("\n--- Processed DataFrame Sample ---")
        print(processed_df.head())
        print(f"\nShape of processed DataFrame: {processed_df.shape}")
        print(f"\nColumns: {processed_df.columns.tolist()}")

        # Test saving
        # Use filename from config if available, otherwise default
        processed_filename = cfg_mgr.get("data_paths.processed_articles_file", "test_processed_articles.csv")
        processor.save_processed_data(processed_df, processed_filename)

    print("\n--- Testing DataProcessor without ConfigManager (fallback behavior) ---")
    processor_no_cfg = DataProcessor()
    processed_df_no_cfg = processor_no_cfg.process_raw_data(dummy_fetched_data)
    if not processed_df_no_cfg.empty:
        processor_no_cfg.save_processed_data(processed_df_no_cfg, "test_processed_articles_no_cfg.csv")
