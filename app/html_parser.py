# from jinaai import WebReader # Consider switching to this later - BeautifulSoup is used now as default, Jina-ai reader is used via API call
from typing import Optional
import random
import requests
import os
import time  # ADDED: Import time module
from .utils import config, logger # Import config and logger

# This module contains functions for parsing HTML content of research articles
# into Markdown format. It includes functions using BeautifulSoup and
# Jina Reader API for HTML parsing.


JINA_API_KEY = os.environ.get("JINA_API_KEY") # Get your Jina AI API key for free: https://jina.ai/?sui=apikey

def parse_article_html_jina_reader_api(url: str) -> Optional[dict]:
    """
    Parses article HTML using Jina Reader API.
    Returns a dictionary containing title and content (in Markdown) from Jina Reader API response.
    """
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}", # Get your Jina AI API key for free: https://jina.ai/?sui=apikey
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = {
        "url": url
    }

    try:
        logger.info(f"Parsing HTML content from URL using Jina Reader API: {url}")
        response = requests.post('https://r.jina.ai/', headers=headers, json=data, timeout=30) # POST request as per Jina API docs
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        response_json = response.json() # Parse JSON response

        if response_json["code"] == 200 and response_json["status"] == 20000 and "data" in response_json and "content" in response_json["data"]:
            content = response_json["data"]["content"]
            title = response_json["data"].get("title", "No Title Found") # Extract title, default if not found
            logger.info(f"Jina Reader API parsing successful for URL: {url}")
            return {
                'title': title,
                'content': content,
                'metadata': {'url': url, 'parser': 'Jina Reader API'}
            }
        else:
            logger.warning(f"Jina Reader API returned an error or unexpected response for URL: {url}. Response: {response_json}")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error during Jina Reader API parsing for {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during Jina Reader API parsing for {url}: {e}", exc_info=True) # Log full exception info
        return None
    finally:
        delay = random.uniform(config.rate_limit_delay_min, config.rate_limit_delay_max)
        time.sleep(delay) # Rate limiting delay
        logger.debug(f"Rate limiting (Jina Reader API parsing): waiting for {delay:.2f} seconds.")


def parse_article_html_bs4(url: str) -> Optional[dict]:
    """
    Parses article HTML from a given URL using BeautifulSoup and html2text (initially).
    Returns a dictionary containing title and content (in Markdown).
    """
    import requests
    from bs4 import BeautifulSoup
    import html2text

    headers = {'User-Agent': config.user_agent}
    try:
        logger.info(f"Parsing HTML content from URL using BeautifulSoup: {url}")
        response = requests.get(url, headers=headers, timeout=30) # Increased timeout for parsing
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Basic title extraction - you might need to refine this based on website structure
        title_tag = soup.find('h1') or soup.find('title') # Try h1 or title tag
        title = title_tag.text.strip() if title_tag else "No Title Found"

        # Attempt to extract main content - this is very generic, needs customization
        article_content_element = soup.find('article') or soup.find('div', {'class': 'article-content'}) or soup.find('div', {'id': 'content'}) # Example selectors
        if article_content_element:
            html_content = str(article_content_element)
        else:
            html_content = str(soup.body) # Fallback to body content if no specific article element found

        # Convert HTML to Markdown using html2text
        h = html2text.HTML2Text()
        h.ignore_links = False # Keep links in Markdown
        markdown_content = h.handle(html_content)

        logger.info(f"HTML parsing using BeautifulSoup successful for URL: {url}")
        return {
            'title': title,
            'content': markdown_content.strip(),
            'metadata': {'url': url, 'parser': 'BeautifulSoup + html2text'} # Basic metadata
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error during BeautifulSoup HTML parsing for {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error parsing HTML from {url} using BeautifulSoup: {e}", exc_info=True) # Log full exception info
        return None
    finally:
        delay = random.uniform(config.rate_limit_delay_min, config.rate_limit_delay_max)
        time.sleep(delay) # Rate limiting delay
        logger.debug(f"Rate limiting (BeautifulSoup parsing): waiting for {delay:.2f} seconds.")


def parse_article_html(url: str, use_jina_reader_api_config: bool = False) -> Optional[dict]:
    """
    Main function to parse article HTML, choosing between BeautifulSoup and Jina Reader API based on config.
    Defaults to BeautifulSoup initially or if Jina Reader API is not configured.
    """
    if use_jina_reader_api_config and config.jina_api_key: # Use Jina Reader API if configured and API key is available
        return parse_article_html_jina_reader_api(url)
    else:
        return parse_article_html_bs4(url) # Fallback to BeautifulSoup implementation