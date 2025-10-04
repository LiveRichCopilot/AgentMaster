"""
🕷️ SCRAPPY JOHNSON - Live Website Design Scraper
Extracts design data from any public website
"""

import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
from typing import Dict, List, Any
from urllib.parse import urljoin, urlparse


class ScrappyJohnson:
    """The badass website scraper"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
    
    def scrape_design(self, url: str) -> Dict[str, Any]:
        """
        Scrape a live website and extract design intelligence.
        
        Args:
            url: The website URL to scrape
            
        Returns:
            Dictionary with colors, fonts, structure, CSS files, and more
        """
        try:
            print(f"\n🕷️ SCRAPPY JOHNSON ACTIVATED")
            print(f"🎯 Target: {url}")
            print("="*60)
            
            # Fetch the page
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract all the goodies
            result = {
                'url': url,
                'status': 'success',
                'colors': self._extract_colors(soup),
                'fonts': self._extract_fonts(soup),
                'css_files': self._extract_css_files(soup, url),
                'structure': self._extract_structure(soup),
                'meta': self._extract_meta(soup),
                'components': self._extract_components(soup),
            }
            
            print("✅ SCRAPE COMPLETE")
            print("="*60)
            
            return result
            
        except requests.exceptions.RequestException as e:
            return {
                'url': url,
                'status': 'error',
                'error': f'Failed to fetch website: {str(e)}'
            }
        except Exception as e:
            return {
                'url': url,
                'status': 'error',
                'error': f'Scraping error: {str(e)}'
            }
    
    def _extract_colors(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract color palette from inline styles"""
        colors = []
        
        # Get colors from inline styles
        for tag in soup.find_all(style=True):
            style = tag['style']
            # Match hex colors and rgb values
            hex_colors = re.findall(r'#[0-9a-fA-F]{6}', style)
            rgb_colors = re.findall(r'rgb\([^)]+\)', style)
            colors.extend(hex_colors + rgb_colors)
        
        # Count occurrences
        if colors:
            color_counts = Counter(colors).most_common(15)
            return {
                'found': len(set(colors)),
                'top_colors': [
                    {'color': color, 'usage': count} 
                    for color, count in color_counts
                ],
                'palette': [color for color, _ in color_counts[:10]]
            }
        else:
            return {
                'found': 0,
                'note': 'Colors likely in external CSS files',
                'palette': []
            }
    
    def _extract_fonts(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract font families"""
        fonts = set()
        
        # From inline styles
        for tag in soup.find_all(style=True):
            style = tag['style']
            if 'font-family' in style:
                font_match = re.search(r'font-family:\s*([^;]+)', style)
                if font_match:
                    fonts.add(font_match.group(1).strip())
        
        # Try to get from meta or common font tags
        for tag in soup.find_all(['h1', 'h2', 'h3', 'p', 'span']):
            if tag.get('style') and 'font' in tag['style']:
                fonts.add(tag.get('style'))
        
        return {
            'found': len(fonts),
            'fonts': list(fonts)[:10] if fonts else ['Check CSS files for font stack']
        }
    
    def _extract_css_files(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract all CSS file URLs"""
        css_files = []
        
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                # Convert relative URLs to absolute
                full_url = urljoin(base_url, href)
                css_files.append(full_url)
        
        return css_files
    
    def _extract_structure(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract page structure and hierarchy"""
        structure = {}
        
        # Headings
        for level in range(1, 7):
            h_tags = soup.find_all(f'h{level}')
            if h_tags:
                structure[f'h{level}'] = {
                    'count': len(h_tags),
                    'examples': [tag.get_text().strip()[:60] for tag in h_tags[:3]]
                }
        
        # Sections
        sections = soup.find_all(['section', 'article', 'main'])
        structure['sections'] = len(sections)
        
        # Navigation
        navs = soup.find_all('nav')
        structure['navigation'] = len(navs)
        
        # Forms
        forms = soup.find_all('form')
        structure['forms'] = len(forms)
        
        return structure
    
    def _extract_meta(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract meta information"""
        meta = {}
        
        # Title
        title = soup.find('title')
        meta['title'] = title.text if title else 'No title'
        
        # Description
        desc = soup.find('meta', attrs={'name': 'description'})
        if desc:
            meta['description'] = desc.get('content', '')
        
        # OG Image
        og_image = soup.find('meta', property='og:image')
        if og_image:
            meta['og_image'] = og_image.get('content', '')
        
        return meta
    
    def _extract_components(self, soup: BeautifulSoup) -> Dict[str, int]:
        """Extract UI components"""
        components = {}
        
        # Buttons
        buttons = soup.find_all(['button', 'a'], class_=re.compile('button|btn', re.I))
        components['buttons'] = len(buttons)
        
        # Cards
        cards = soup.find_all(class_=re.compile('card', re.I))
        components['cards'] = len(cards)
        
        # Images
        images = soup.find_all('img')
        components['images'] = len(images)
        
        # Links
        links = soup.find_all('a')
        components['links'] = len(links)
        
        return components
    
    def scrape_css_file(self, css_url: str) -> Dict[str, Any]:
        """
        Scrape a CSS file to extract detailed design tokens.
        
        Args:
            css_url: URL of the CSS file
            
        Returns:
            Dictionary with colors, fonts, spacing from CSS
        """
        try:
            response = requests.get(css_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            css_content = response.text
            
            # Extract colors
            hex_colors = re.findall(r'#[0-9a-fA-F]{6}', css_content)
            rgb_colors = re.findall(r'rgb\([^)]+\)', css_content)
            
            # Extract font families
            font_families = re.findall(r'font-family:\s*([^;]+)', css_content)
            
            # Extract font sizes
            font_sizes = re.findall(r'font-size:\s*([^;]+)', css_content)
            
            return {
                'url': css_url,
                'status': 'success',
                'colors': {
                    'hex': list(set(hex_colors))[:20],
                    'rgb': list(set(rgb_colors))[:10]
                },
                'fonts': {
                    'families': list(set(font_families))[:10],
                    'sizes': list(set(font_sizes))[:15]
                }
            }
            
        except Exception as e:
            return {
                'url': css_url,
                'status': 'error',
                'error': str(e)
            }


# Global instance
scrappy = ScrappyJohnson()


def scrape_website_design(url: str) -> Dict[str, Any]:
    """
    🕷️ SCRAPPY JOHNSON - Scrape live website for design intelligence.
    
    Extracts colors, fonts, structure, CSS files, and components from any public website.
    This goes BEYOND what an LLM can do - it accesses real, live website data.
    
    Args:
        url: The website URL to scrape (e.g., "https://stripe.com")
        
    Returns:
        Complete design analysis with colors, fonts, structure, and more
        
    Examples:
        scrape_website_design("https://stripe.com")
        scrape_website_design("https://vercel.com")
    """
    return scrappy.scrape_design(url)


def scrape_css_file(css_url: str) -> Dict[str, Any]:
    """
    🕷️ SCRAPPY JOHNSON - Deep dive into a CSS file.
    
    Extracts detailed design tokens (colors, fonts, sizes) from a specific CSS file.
    Use this after scrape_website_design to get complete design system.
    
    Args:
        css_url: URL of the CSS file
        
    Returns:
        Detailed design tokens from the CSS file
    """
    return scrappy.scrape_css_file(css_url)

