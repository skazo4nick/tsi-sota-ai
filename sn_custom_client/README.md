# SpringerNature API Client

## Overview

This client provides a robust, production-ready interface to the Springer Nature Open Access API, wrapping the official `springernature-api-client` PyPI package. It supports advanced querying, article existence checks, XML/fulltext download, pagination, rate limiting, and error handling. All API key management is handled via environment variables (see below).

## Files

*   `sn_openaccess_client.py`: Main wrapper for the official Springer Nature Open Access API client. Use this for all real API interactions.

## Usage Example

```python
from sn_custom_client.sn_openaccess_client import SpringerNatureOpenAccessClient

client = SpringerNatureOpenAccessClient()
doi = "10.1007/s00248-013-0307-y"
if client.article_exists(doi):
    print(f"Article {doi} exists.")
    xml_path = client.download_xml(doi)
    if xml_path:
        print(f"Article XML downloaded to: {xml_path}")
    else:
        print(f"Failed to download XML for {doi}.")
else:
    print(f"Article {doi} not found or not accessible.")
```

## Advanced Features
- **Advanced Querying**: Boolean logic, filters, and sorting supported via the `advanced_query` method.
- **Pagination**: Handles large result sets with built-in paging.
- **Rate Limiting**: Enforces daily and per-request limits as per Springer Nature guidelines.
- **Error Handling**: Robust error handling and logging throughout.

## Configuration
- Set your Springer Nature API key in your environment (e.g., in a `.env` file):
  ```
  SPRINGERNATURE_API=your_api_key_here
  ```
- The client will automatically load this key.

## Dependencies
- `springernature-api-client` (official PyPI package)
- `python-dotenv`
- `requests`

All dependencies are listed in the main `requirements.txt` and `app/environment.yml`.

## Migration Note
- This client replaces the old `springernature_api_client/` directory and dummy logic. All code and documentation should now reference `sn_custom_client/` for Springer Nature API integration.
