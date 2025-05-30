import yaml
import os
from typing import Any, Dict, Optional

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "slr_config.yaml")

class ConfigManager:
    def __init__(self, config_path: Optional[str] = None):
        """
        Initializes the ConfigManager.

        Loads configuration from a YAML file. Defaults to `config/slr_config.yaml`
        relative to the project root.

        Args:
            config_path (Optional[str]): Path to the YAML configuration file.
                                         If None, uses DEFAULT_CONFIG_PATH.
        """
        self.config_path = config_path if config_path else DEFAULT_CONFIG_PATH
        self.config: Dict[str, Any] = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Loads the YAML configuration file.
        Returns an empty dict if the file is not found or is invalid.
        """
        if not os.path.exists(self.config_path):
            print(f"Warning: Configuration file not found at {self.config_path}. Using empty config.")
            return {}

        try:
            with open(self.config_path, "r") as f:
                config_data = yaml.safe_load(f)
            if config_data is None: # Handles empty YAML file
                print(f"Warning: Configuration file at {self.config_path} is empty. Using empty config.")
                return {}
            print(f"Configuration loaded successfully from {self.config_path}")
            return config_data
        except yaml.YAMLError as e:
            print(f"Error parsing YAML configuration file at {self.config_path}: {e}")
            return {} # Return empty or raise an exception, depending on desired strictness
        except Exception as e:
            print(f"An unexpected error occurred while loading config from {self.config_path}: {e}")
            return {}

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Retrieves a configuration value using a dot-separated key path.

        Example: config_manager.get("data_paths.raw_data_dir")

        Args:
            key_path (str): Dot-separated path to the configuration key
                            (e.g., "parent_key.child_key.grandchild_key").
            default (Any, optional): Default value to return if the key is not found.

        Returns:
            Any: The configuration value, or the default if not found.
        """
        value = self.config
        try:
            for key in key_path.split('.'):
                if isinstance(value, dict):
                    value = value[key]
                else:
                    # Path goes deeper than the structure allows (e.g. trying to key into a string)
                    return default
            return value
        except (KeyError, TypeError): # KeyError for missing keys, TypeError for trying to index non-dict
            return default

    def get_api_key(self, service_name: str) -> Optional[str]:
        """
        Retrieves an API key from environment variables.
        This centralizes how API keys are fetched, even if they are not in slr_config.yaml.
        (Matches the pattern already in api_clients.py but good to have in ConfigManager too)

        Args:
            service_name (str): The name of the service (e.g., "CORE", "OPENALEX_EMAIL").
                                Environment variable is expected to be {SERVICE_NAME}_API_KEY or just SERVICE_NAME for email.

        Returns:
            Optional[str]: The API key, or None if not found.
        """
        if service_name.upper() == "OPENALEX_EMAIL": # Special case for email
            env_var_name = "OPENALEX_EMAIL"
        else:
            env_var_name = f"{service_name.upper()}_API_KEY"

        key = os.getenv(env_var_name)
        if not key:
            print(f"Warning: Environment variable {env_var_name} not set for {service_name}.")
        return key

    # Convenience properties for commonly accessed sections (optional)
    @property
    def data_paths(self) -> Dict[str, Any]:
        return self.get("data_paths", {})

    @property
    def default_search_params(self) -> Dict[str, Any]:
        return self.get("default_search_params", {})

    @property
    def logging_config(self) -> Dict[str, Any]:
        return self.get("logging", {"level": "INFO"}) # Provide a default for logging

if __name__ == '__main__':
    # Example Usage:
    # Assuming slr_config.yaml is in ../config/ relative to this file

    # Test with default path
    print("--- Testing with default config path ---")
    cfg_mgr = ConfigManager()
    print(f"Raw data directory: {cfg_mgr.get('data_paths.raw_data_dir', 'Default Path')}")
    print(f"Processed data directory: {cfg_mgr.data_paths.get('processed_data_dir')}")
    print(f"Default start year: {cfg_mgr.default_search_params.get('start_year')}")
    print(f"Logging level: {cfg_mgr.logging_config.get('level')}")

    # Test API key retrieval (requires .env file or environment variables to be set)
    print(f"CORE API Key from env: {cfg_mgr.get_api_key('CORE')}")
    print(f"OpenAlex Email from env: {cfg_mgr.get_api_key('OPENALEX_EMAIL')}") # Uses special handling

    # Test getting a non-existent key with a default
    print(f"Non-existent key: {cfg_mgr.get('non_existent.key', 'Not Found')}")

    # Test with a specific (potentially non-existent) path to demonstrate error handling
    print("\n--- Testing with a non-existent config path ---")
    non_existent_cfg_mgr = ConfigManager(config_path="config/non_existent_config.yaml")
    print(f"Raw data directory (non-existent config): {non_existent_cfg_mgr.get('data_paths.raw_data_dir', 'Default Path if Config Missing')}")
