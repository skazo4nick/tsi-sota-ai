from jinaai import WebReader # Consider switching to this later
from typing import Optional
import random
from .utils import config, logger # Import config and logger

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
        logger.info(f"Parsing HTML content from URL: {url}")
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

        logger.info(f"HTML parsing successful for URL: {url}")
        return {
            'title': title,
            'content': markdown_content.strip(),
            'metadata': {'url': url, 'parser': 'BeautifulSoup + html2text'} # Basic metadata
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error during HTML parsing for {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error parsing HTML from {url}: {e}", exc_info=True) # Log full exception info
        return None
    finally:
        delay = random.uniform(config.rate_limit_delay_min, config.rate_limit_delay_max)
        time.sleep(delay) # Rate limiting delay after each parsing attempt
        logger.debug(f"Rate limiting (parsing): waiting for {delay:.2f} seconds.")


def parse_article_html_jinaai(url: str) -> Optional[dict]:
    """
    Parses article HTML using Jina-AI WebReader (to be implemented later).
    This is a placeholder for future integration.
    """
    reader = WebReader() # Initialize WebReader here, or globally if config allows

    try:
        logger.info(f"Parsing HTML content from URL using Jina-AI WebReader: {url}")
        result = reader.get(url=url) # Simplified Jina-AI call
        if result and result.content: # Check if content is not None and not empty
            logger.info(f"HTML parsing with Jina-AI successful for URL: {url}")
            return {
                'title': result.title,
                'content': result.content,
                'metadata': result.metadata # Capture all metadata from Jina-AI
            }
        else:
            logger.warning(f"Jina-AI WebReader returned no content for URL: {url}")
            return None

    except Exception as e:
        logger.error(f"Error during Jina-AI WebReader parsing for {url}: {e}", exc_info=True)
        return None
    finally:
        delay = random.uniform(config.rate_limit_delay_min, config.rate_limit_delay_max)
        time.sleep(delay) # Rate limiting delay
        logger.debug(f"Rate limiting (Jina-AI parsing): waiting for {delay:.2f} seconds.")


def parse_article_html(url: str, use_jinaai: bool = False) -> Optional[dict]:
    """
    Main function to parse article HTML, choosing between BeautifulSoup and Jina-AI.
    Defaults to BeautifulSoup initially.
    """
    if use_jinaai:
        return parse_article_html_jinaai(url) # Implement Jina-AI parsing later
    else:
        return parse_article_html_bs4(url) # Start with BeautifulSoup implementation