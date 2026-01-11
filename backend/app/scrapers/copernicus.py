"""
Scraper for Copernicus Podmiot Leczniczy job offers.
Source: https://copernicus.gda.pl/ogloszenia/kariera
Note: This page is JavaScript-rendered, so we use Playwright.
"""
from typing import List, Dict
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.scrapers.base import BaseScraper


class CopernicusScraper(BaseScraper):
    """Scraper for Copernicus job board."""
    
    def __init__(self):
        super().__init__(
            base_url="https://copernicus.gda.pl/ogloszenia/kariera",
            facility_name="COPERNICUS Podmiot Leczniczy Sp. z o.o.",
            city="Gdańsk"
        )
    
    def scrape(self) -> List[Dict]:
        """
        Scrape job offers from Copernicus using Playwright.
        
        Returns:
            List of job offer dictionaries
        """
        jobs = []
        # Use Playwright for JavaScript-rendered page
        soup = self.fetch_page(self.base_url, use_playwright=True, wait_selector="body")
        
        if not soup:
            print("Warning: Could not fetch Copernicus page with Playwright.")
            return jobs
        
        # Check if page loaded properly
        page_text = soup.get_text(strip=True)
        if len(page_text) < 100:
            print("Warning: Copernicus page appears to be empty or not fully loaded.")
            return jobs
        
        # Look for job listings - try multiple strategies
        # Strategy 1: Look for articles or job containers
        job_containers = soup.find_all(['article', 'div', 'li'], class_=lambda x: x and any(
            keyword in str(x).lower() for keyword in ['job', 'oferta', 'praca', 'kariera', 'post', 'entry', 'position']
        ))
        
        # Strategy 2: Look for all articles
        if not job_containers:
            job_containers = soup.find_all('article')
        
        # Strategy 3: Look for links with job-related text
        if not job_containers:
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                text_lower = text.lower()
                
                # Check if this looks like a job offer link
                is_job_link = (
                    any(keyword in text_lower for keyword in ['oferta', 'praca', 'zatrudnienie', 'rekrutacja', 'kariera']) or
                    any(keyword in href.lower() for keyword in ['oferta', 'praca', 'kariera', 'job', 'rekrutacja'])
                )
                
                if is_job_link:
                    job_url = self.normalize_url(href)
                    parent = link.find_parent(['article', 'div', 'li', 'section'])
                    
                    if parent:
                        title = text.strip() if text.strip() else None
                        if not title:
                            title_elem = parent.find(['h1', 'h2', 'h3', 'h4', 'h5'])
                            if title_elem:
                                title = title_elem.get_text(strip=True)
                        
                        if not title:
                            continue
                        
                        # Extract description
                        description = ""
                        desc_elem = parent.find(['p', 'div'], class_=lambda x: x and any(
                            kw in str(x).lower() for kw in ['desc', 'excerpt', 'summary', 'content']
                        ))
                        if not desc_elem:
                            desc_elem = parent.find('p')
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
        
        # Process containers if found
        for container in job_containers:
            # Find link
            link = container.find('a', href=True)
            if not link:
                continue
            
            href = link.get('href', '')
            job_url = self.normalize_url(href)
            
            # Extract title
            title = link.get_text(strip=True)
            if not title:
                title_elem = container.find(['h1', 'h2', 'h3', 'h4', 'h5'])
                if title_elem:
                    title = title_elem.get_text(strip=True)
            
            if not title:
                continue
            
            # Extract description
            description = ""
            desc_elem = container.find(['p', 'div'], class_=lambda x: x and any(
                kw in str(x).lower() for kw in ['desc', 'excerpt', 'summary', 'content']
            ))
            if not desc_elem:
                desc_elem = container.find('p')
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
