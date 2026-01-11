"""
Scraper for Okręgowa Izba Pielęgniarek i Położnych w Gdańsku job offers.
Source: https://praca.oipip.gda.pl/
"""
from typing import List, Dict
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.scrapers.base import BaseScraper
from app.models import MedicalRole


class OipipGdanskScraper(BaseScraper):
    """Scraper for OIPiP Gdańsk job board."""
    
    def __init__(self):
        super().__init__(
            base_url="https://praca.oipip.gda.pl/",
            facility_name="Okręgowa Izba Pielęgniarek i Położnych w Gdańsku",
            city="Gdańsk"
        )
    
    def scrape(self) -> List[Dict]:
        """
        Scrape job offers from OIPiP Gdańsk.
        
        Returns:
            List of job offer dictionaries
        """
        jobs = []
        soup = self.fetch_page(self.base_url)
        
        if not soup:
            return jobs
        
        # Find all job offer entries
        # Based on the HTML structure, job offers are in list items or article tags
        # Looking for entries with dates and "Oferta pracy" text
        
        # Try to find job listings - common patterns:
        # 1. Articles with job titles
        # 2. List items with job information
        # 3. Divs with specific classes
        
        # Look for links that contain "Oferta pracy" or similar
        job_links = soup.find_all('a', href=True)
        
        for link in job_links:
            link_text = link.get_text(strip=True)
            href = link.get('href', '')
            
            # Check if this looks like a job offer link
            if 'oferta pracy' in link_text.lower() or 'czytaj' in link_text.lower():
                # Get the full URL
                job_url = self.normalize_url(href)
                
                # Try to extract job details from the link or nearby elements
                # Find parent container
                parent = link.find_parent(['article', 'div', 'li'])
                
                if parent:
                    # Extract title
                    title_elem = parent.find(['h1', 'h2', 'h3', 'h4', 'strong', 'b'])
                    if not title_elem:
                        title_elem = link
                    
                    title = title_elem.get_text(strip=True)
                    
                    # Extract date if available
                    date_elem = parent.find(string=lambda text: text and any(
                        char.isdigit() for char in text
                    ))
                    
                    # Extract description from parent or nearby text
                    description = ""
                    desc_elem = parent.find(['p', 'div'])
                    if desc_elem:
                        description = desc_elem.get_text(strip=True)
                    
                    # Detect role from title
                    role = self.detect_role(title)
                    
                    # Extract facility name from title or use default
                    facility_name = self.facility_name
                    
                    # Try to extract facility from title (format: "Oferta pracy – Facility – City – Role")
                    if '–' in title or '-' in title:
                        parts = title.replace('–', '-').split('-')
                        if len(parts) >= 2:
                            facility_name = parts[1].strip()
                    
                    jobs.append({
                        'title': title,
                        'facility_name': facility_name,
                        'city': self.city,
                        'role': role,
                        'description': description[:1000] if description else None,  # Limit description length
                        'source_url': job_url,
                    })
        
        # Remove duplicates based on source_url
        seen_urls = set()
        unique_jobs = []
        for job in jobs:
            if job['source_url'] not in seen_urls:
                seen_urls.add(job['source_url'])
                unique_jobs.append(job)
        
        return unique_jobs

