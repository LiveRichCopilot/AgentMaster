"""
Content Extractor Module
Extracts clean text content from web pages
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Any


def extract_text_from_url(url: str, timeout: int = 10) -> Dict[str, Any]:
    """
    Fetches a URL and extracts the main text content.
    
    Args:
        url: The URL to fetch
        timeout: Request timeout in seconds (default: 10)
        
    Returns:
        Dictionary with:
        - 'url': Original URL
        - 'title': Page title
        - 'text': Extracted content
        - 'success': Boolean indicating if extraction succeeded
        - 'error': Error message if failed
    """
    try:
        # Set a user agent to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fetch the page
        response = requests.get(url, timeout=timeout, headers=headers)
        response.raise_for_status()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = soup.find('title')
        title_text = title.string if title else 'Untitled'
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe', 'noscript']):
            element.decompose()
        
        # Get text content
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up the text - remove excessive whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        cleaned_text = '\n'.join(lines)
        
        # Limit to 8000 characters to avoid token limits
        if len(cleaned_text) > 8000:
            cleaned_text = cleaned_text[:8000] + "..."
        
        print(f"✅ Extracted {len(cleaned_text)} characters from: {title_text}")
        
        return {
            'url': url,
            'title': title_text,
            'text': cleaned_text,
            'success': True,
            'error': None
        }
        
    except requests.Timeout:
        error_msg = f"Timeout fetching {url}"
        print(f"⏱️  {error_msg}")
        return {
            'url': url,
            'title': None,
            'text': '',
            'success': False,
            'error': error_msg
        }
        
    except requests.RequestException as e:
        error_msg = f"Request error: {str(e)}"
        print(f"❌ {error_msg} for {url}")
        return {
            'url': url,
            'title': None,
            'text': '',
            'success': False,
            'error': error_msg
        }
        
    except Exception as e:
        error_msg = f"Extraction error: {str(e)}"
        print(f"❌ {error_msg} for {url}")
        return {
            'url': url,
            'title': None,
            'text': '',
            'success': False,
            'error': error_msg
        }


def extract_from_multiple_urls(urls: list, timeout: int = 10) -> list:
    """
    Extract content from multiple URLs.
    
    Args:
        urls: List of URLs to extract from
        timeout: Timeout per URL
        
    Returns:
        List of extraction results (only successful ones)
    """
    results = []
    
    for url in urls:
        result = extract_text_from_url(url, timeout=timeout)
        if result['success'] and result['text']:
            results.append(result)
    
    print(f"📄 Successfully extracted content from {len(results)}/{len(urls)} URLs")
    return results

