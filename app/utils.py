import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file="/Users/max/Documents/Code/tsi-sota-ai/app/.env", yaml_file="/Users/max/Documents/Code/tsi-sota-ai/app/config.yaml")

    pdf_dir_root: str = "./data/pdfs"
    cluster_dir_format: str = "./data/cluster_{}"
    use_clustering_in_pipeline: bool = True
    n_clusters: int = 20
    user_agent: str = "MyArticleDownloader/1.0 (Contact: your-email@example.com)"
    rate_limit_delay_min: float = 0.5
    rate_limit_delay_max: float = 1.5
    unpaywall_email: Optional[str] = None  # Optional Unpaywall email
    core_api_key: Optional[str] = None      # Optional CORE API key
    openai_api_key: Optional[str] = None    # Optional OpenAI API key
    google_api_key: Optional[str] = None    # Optional Google API key
    use_jina_reader_api_config: bool = False # New config option to use Jina Reader API
    jina_api_key: Optional[str] = None      # Jina AI Reader API Key - loaded from .env

    def get_cluster_dir(self, cluster_id: int) -> str:
        return self.cluster_dir_format.format(cluster_id)

config = Config()

def create_data_directories():
    """Creates necessary data directories if they don't exist."""
    os.makedirs(config.pdf_dir_root, exist_ok=True)
    # Cluster directories will be created dynamically in download_pdf function
    print(f"Data directories created or already exist at: {config.pdf_dir_root}")

def setup_logging():
    import logging
    logging.basicConfig(filename='scraper.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

logger = setup_logging()