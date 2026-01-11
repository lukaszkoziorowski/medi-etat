"""
Scraper for Szpitale Pomorskie job offers.
Source: https://www.szpitalepomorskie.eu/category/oferty-pracy/
"""
from typing import List, Dict
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.scrapers.base import BaseScraper


class SzpitalePomorskieScraper(BaseScraper):
    """Scraper for Szpitale Pomorskie job board."""
    
    def __init__(self):
        super().__init__(
            base_url="https://www.szpitalepomorskie.eu/category/oferty-pracy/",
            facility_name="Szpitale Pomorskie",
            city="Gdańsk"
        )
    
    def scrape(self) -> List[Dict]:
        """
        Scrape job offers from Szpitale Pomorskie.
        
        Returns:
            List of job offer dictionaries
        """
        jobs = []
        soup = self.fetch_page(self.base_url)
        
        if not soup:
            return jobs
        
        # WordPress-style structure - look for article tags or post entries
        # Common patterns: article.post, .entry, .post-item, etc.
        articles = soup.find_all(['article', 'div'], class_=lambda x: x and any(
            keyword in x.lower() for keyword in ['post', 'entry', 'job', 'oferta']
        ))
        
        # If no articles found with classes, try finding all articles
        if not articles:
            articles = soup.find_all('article')
        
        # If still nothing, look for links with job-related text
        if not articles:
            # Fallback: find all links and filter by context
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                href = link.get('href', '')
                text = link.get_text(strip=True).lower()
                
                # Check if this looks like a job offer link
                if any(keyword in text for keyword in ['oferta', 'praca', 'zatrudnienie', 'rekrutacja']):
                    job_url = self.normalize_url(href)
                    parent = link.find_parent(['article', 'div', 'li'])
                    
                    if parent:
                        title = link.get_text(strip=True) or text
                        if not title:
                            title_elem = parent.find(['h1', 'h2', 'h3', 'h4'])
                            if title_elem:
                                title = title_elem.get_text(strip=True)
                        
                        # Extract description
                        description = ""
                        desc_elem = parent.find(['p', 'div'], class_=lambda x: x and 'excerpt' in str(x).lower())
                        if desc_elem:
                            description = desc_elem.get_text(strip=True)
                        
                        # Detect role and facility
                        role = self.detect_role(title)
                        facility_name = self.extract_facility_name(title) or self.facility_name
                        
                        jobs.append({
                            'title': title[:500] if title else "Oferta pracy",
                            'facility_name': facility_name,
                            'city': self.city,
                            'role': role,
                            'description': description[:1000] if description else None,
                            'source_url': job_url,
                        })
        
        # Process articles if found
        for article in articles:
            # Find title/link
            title_elem = article.find(['h1', 'h2', 'h3', 'h4', 'a'])
            if not title_elem:
                continue
            
            # Get link
            link = article.find('a', href=True)
            if not link:
                continue
            
            href = link.get('href', '')
            job_url = self.normalize_url(href)
            
            # Extract title
            title = link.get_text(strip=True)
            if not title:
                title = title_elem.get_text(strip=True)
            
            if not title:
                continue
            
            # Extract description
            description = ""
            desc_elem = article.find(['p', 'div'], class_=lambda x: x and 'excerpt' in str(x).lower())
            if not desc_elem:
                desc_elem = article.find('p')
            if desc_elem:
                description = desc_elem.get_text(strip=True)
            
            # Detect role and facility
            role = self.detect_role(title)
            facility_name = self.extract_facility_name(title) or self.facility_name
            
            jobs.append({
                'title': title[:500],
                'facility_name': facility_name,
                'city': self.city,
                'role': role,
                'description': description[:1000] if description else None,
                'source_url': job_url,
            })
        
        # Remove duplicates
        seen_urls = set()
        unique_jobs = []
        for job in jobs:
            if job['source_url'] not in seen_urls:
                seen_urls.add(job['source_url'])
                unique_jobs.append(job)
        
        return unique_jobs
    
    def extract_facility_name(self, text: str) -> str:
        """Extract facility name from text if possible."""
        # Common patterns: "Oferta pracy - Facility Name" or similar
        if '–' in text or '-' in text:
            parts = text.replace('–', '-').split('-')
            if len(parts) >= 2:
                return parts[1].strip()
        return ""

