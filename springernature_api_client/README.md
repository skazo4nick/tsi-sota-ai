# SpringerNature API Client

## Overview

This client is intended to interact with the SpringerNature API, specifically focusing on accessing open access article data. It provides helper functions to check for article existence and download article metadata or full text in XML format.

**Note:** The current implementation of this client (`openaccess.py`) contains dummy functions. It simulates API interactions but does not connect to the actual SpringerNature API. It is intended as a placeholder for future development.

## Files

*   `openaccess.py`: Contains the Python functions for interacting with the (simulated) SpringerNature Open Access API.

## Functions (Intended Functionality)

The client aims to provide functions such as:

*   `article_exists(doi)`: Checks if an article with the given DOI exists and is accessible via the API.
    *   **Current Behavior**: Always returns `True`.
*   `download_xml(doi)`: Downloads the article's XML (metadata and/or full text) for a given DOI.
    *   **Current Behavior**: Creates a dummy XML file in the `app/system_data/` directory (e.g., `app/system_data/doi_replaced_dummy.xml`) with placeholder content.

## Usage (Intended)

When fully implemented, the client would be used as follows:

```python
from springernature_api_client import openaccess

doi = "10.1007/s00248-013-0307-y" # Example DOI

if openaccess.article_exists(doi):
    print(f"Article {doi} exists.")
    xml_path = openaccess.download_xml(doi)
    if xml_path:
        print(f"Article XML downloaded to: {xml_path}")
        # Further processing of the XML file
    else:
        print(f"Failed to download XML for {doi}.")
else:
    print(f"Article {doi} not found or not accessible.")
```

## Configuration

A fully functional client would typically require an API key from SpringerNature. This key would need to be configured, likely through environment variables or a configuration file, and passed to the client's functions or an initialization class. (This is not implemented in the current dummy version).

## Dependencies

This client currently has no external dependencies beyond standard Python libraries. A future, functional version might require libraries like `requests` for making HTTP API calls. These would be listed in the main project's `requirements.txt`.
