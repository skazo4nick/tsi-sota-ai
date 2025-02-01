import requests
import os
import re
from typing import Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random

# filepath: app/pdf_downloader.py
from utils import config, logger  # Use absolute import now

def resolve_pdf_url(doi: str) -> Optional[str]:
    """Multi-strategy PDF resolution with fallback mechanisms."""
    strategies = [
        f'https://link.springer.com/content/pdf/{doi}.pdf',
        f'https://www.ncbi.nlm.nih.gov/pmc/articles/{doi}/pdf/',
        f'https://doi.org/{doi}'
    ]
    headers = {'User-Agent': config.user_agent}

    for url in strategies:
        try:
            logger.info(f"Trying to resolve PDF URL using strategy: {url}")
            response = requests.head(url, headers=headers, allow_redirects=True, timeout=10) # Shorter timeout for HEAD
            response.raise_for_status()
            if response.status_code == 200 and 'pdf' in response.headers.get('Content-Type', '').lower():
                logger.info(f"Direct PDF URL found (HEAD): {response.url}")
                return response.url

            response_get = requests.get(url, headers=headers, allow_redirects=True, timeout=20) # Longer timeout for GET
            response_get.raise_for_status()
            soup = BeautifulSoup(response_get.content, 'html.parser')
            pdf_link = soup.find('a', href=re.compile(r'\.pdf$', re.I))
            if pdf_link:
                pdf_url = urljoin(response_get.url, pdf_link['href']) # Use urljoin to handle relative paths
                logger.info(f"PDF link found in HTML: {pdf_url}")
                return pdf_url

        except requests.exceptions.RequestException as e:
            logger.warning(f"Request exception for {url}: {e}")
            continue
        except Exception as e:
            logger.error(f"Error processing URL {url}: {e}", exc_info=True) # Log full exception info
            continue

    logger.info(f"No PDF URL found for DOI: {doi}")
    return None

def download_pdf(doi: str, cluster_id: int) -> Optional[str]:
    """Robust PDF downloader with error handling and rate limiting."""
    pdf_url = resolve_pdf_url(doi)
    if not pdf_url:
        return None

    cluster_dir = config.get_cluster_dir(cluster_id)
    os.makedirs(cluster_dir, exist_ok=True)
    pdf_filename = f"{doi.replace('/', '_')}.pdf" # Sanitize DOI for filename
    pdf_path = os.path.join(cluster_dir, pdf_filename)

    headers = {'User-Agent': config.user_agent}

    try:
        logger.info(f"Downloading PDF from: {pdf_url} to {pdf_path}")
        start_time = time.time()
        with requests.get(pdf_url, stream=True, headers=headers, timeout=30) as response: # Increased timeout for download
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            with open(pdf_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        download_time = time.time() - start_time
        logger.info(f"PDF downloaded successfully to {pdf_path} in {download_time:.2f} seconds.")
        return pdf_path
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download PDF for DOI {doi} from {pdf_url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during PDF download for DOI {doi}: {e}", exc_info=True) # Log full exception info
        return None
    finally:
        delay = random.uniform(config.rate_limit_delay_min, config.rate_limit_delay_max)
        time.sleep(delay) # Rate limiting delay after each download attempt
        logger.debug(f"Rate limiting: waiting for {delay:.2f} seconds.")