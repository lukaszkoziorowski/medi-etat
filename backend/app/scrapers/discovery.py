"""
URL discovery engine for finding career/job pages on facility websites.
"""
from typing import List, Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class URLDiscovery:
    """Discover career/job pages from facility homepages."""
    
    # Keywords to search for in links and URLs
    CAREER_KEYWORDS = [
        'kariera', 'praca', 'oferty', 'rekrutacja', 'zatrudnienie',
        'career', 'jobs', 'recruitment', 'employment'
    ]
    
    # URL patterns that likely indicate job pages
    URL_PATTERNS = [
        '/kariera', '/praca', '/oferty', '/rekrutacja', '/zatrudnienie',
        '/career', '/jobs', '/recruitment', '/employment',
        '/oferty-pracy', '/praca-oferty'
    ]
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def discover_career_url(self, homepage_url: str) -> Optional[str]:
        """
        Discover career/job page URL from facility homepage.
        
        Args:
            homepage_url: Facility homepage URL
            
        Returns:
            Career page URL if found, None otherwise
        """
        try:
            response = self.session.get(homepage_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Find all links
            links = soup.find_all('a', href=True)
            
            # Look for links with career keywords
            for link in links:
                href = link.get('href', '')
                text = link.get_text(strip=True).lower()
                href_lower = href.lower()
                
                # Check if link text or URL contains career keywords
                if any(keyword in text or keyword in href_lower for keyword in self.CAREER_KEYWORDS):
                    # Make absolute URL
                    career_url = urljoin(homepage_url, href)
                    return career_url
                
                # Check if URL matches known patterns
                if any(pattern in href_lower for pattern in self.URL_PATTERNS):
                    career_url = urljoin(homepage_url, href)
                    return career_url
            
            return None
            
        except Exception as e:
            print(f"Error discovering career URL from {homepage_url}: {e}")
            return None
    
    def discover_all_career_urls(self, homepage_urls: List[str]) -> List[str]:
        """
        Discover career URLs from multiple homepages.
        
        Args:
            homepage_urls: List of homepage URLs
            
        Returns:
            List of discovered career page URLs
        """
        career_urls = []
        
        for homepage_url in homepage_urls:
            career_url = self.discover_career_url(homepage_url)
            if career_url:
                career_urls.append(career_url)
                print(f"Found career page: {career_url}")
            else:
                print(f"No career page found for: {homepage_url}")
        
        return career_urls

