"""
Web Searcher Module
Performs web searches using Google Custom Search API
"""

import os
import requests
from typing import List, Dict, Any


def perform_web_search(query: str, num_results: int = 5) -> List[str]:
    """
    Performs a web search and returns a list of URLs.
    
    Args:
        query: The search query
        num_results: Number of results to return (default: 5)
        
    Returns:
        List of URLs from search results
    """
    try:
        # Get API credentials from environment
        api_key = os.environ.get("GOOGLE_SEARCH_API_KEY")
        search_engine_id = os.environ.get("GOOGLE_SEARCH_ENGINE_ID")
        
        if not api_key or not search_engine_id:
            print("⚠️  Google Search API credentials not configured")
            print("   Set GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_ENGINE_ID environment variables")
            # Fallback: return empty list for now
            return []
        
        # Build API request URL
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': search_engine_id,
            'q': query,
            'num': num_results
        }
        
        # Make request
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        # Parse results
        search_results = response.json().get("items", [])
        urls = [result["link"] for result in search_results[:num_results]]
        
        print(f"🔍 Found {len(urls)} URLs for: {query}")
        return urls
        
    except requests.RequestException as e:
        print(f"❌ Search API error: {e}")
        return []
    except Exception as e:
        print(f"❌ Unexpected error in web search: {e}")
        return []


def get_search_snippets(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Performs a web search and returns results with snippets.
    
    Args:
        query: The search query
        num_results: Number of results to return
        
    Returns:
        List of dictionaries with 'url', 'title', 'snippet'
    """
    try:
        api_key = os.environ.get("GOOGLE_SEARCH_API_KEY")
        search_engine_id = os.environ.get("GOOGLE_SEARCH_ENGINE_ID")
        
        if not api_key or not search_engine_id:
            return []
        
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': search_engine_id,
            'q': query,
            'num': num_results
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        search_results = response.json().get("items", [])
        
        results = []
        for result in search_results[:num_results]:
            results.append({
                'url': result.get('link', ''),
                'title': result.get('title', 'Untitled'),
                'snippet': result.get('snippet', '')
            })
        
        return results
        
    except Exception as e:
        print(f"❌ Error getting search snippets: {e}")
        return []

