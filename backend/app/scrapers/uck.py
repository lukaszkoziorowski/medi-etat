"""
Scraper for Uniwersyteckie Centrum Kliniczne (UCK) job offers.
Source: https://uck.pl/kariera/oferty.html
Note: This site may require JavaScript, so we'll try BeautifulSoup first,
      and can fall back to Playwright if needed.
"""
from typing import List, Dict
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.scrapers.base import BaseScraper


class UckScraper(BaseScraper):
    """Scraper for UCK job board."""
    
    def __init__(self):
        super().__init__(
            base_url="https://uck.pl/kariera/oferty.html",
            facility_name="Uniwersyteckie Centrum Kliniczne",
            city="Gdańsk"
        )
    
    def scrape(self) -> List[Dict]:
        """
        Scrape job offers from UCK.
        
        Returns:
            List of job offer dictionaries
        """
        jobs = []
        soup = self.fetch_page(self.base_url)
        
        if not soup:
            return jobs
        
        # UCK has a specific structure - look for job listings
        # Based on the web search, jobs are listed with titles and details
        # Try multiple strategies to find job listings
        
        # Strategy 1: Look for specific job listing containers
        job_containers = soup.find_all(['div', 'article', 'li'], class_=lambda x: x and any(
            keyword in str(x).lower() for keyword in ['job', 'oferta', 'praca', 'kariera', 'position', 'vacancy']
        ))
        
        # Strategy 2: Look for all articles
        if not job_containers:
            job_containers = soup.find_all('article')
        
        # Strategy 3: Look for list items in job-related sections
        if not job_containers:
            sections = soup.find_all(['section', 'div'], class_=lambda x: x and any(
                keyword in str(x).lower() for keyword in ['job', 'oferta', 'praca', 'kariera']
            ))
            for section in sections:
                job_containers.extend(section.find_all(['li', 'div', 'article']))
        
        # Strategy 4: Find all links and check their context more broadly
        if not job_containers:
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                text_lower = text.lower()
                
                # Check if link text or URL contains job-related keywords
                is_job_link = (
                    any(keyword in text_lower for keyword in ['oferta', 'praca', 'zatrudnienie', 'rekrutacja', 'kariera']) or
                    any(keyword in href.lower() for keyword in ['oferta', 'praca', 'kariera', 'job', 'rekrutacja'])
                )
                
                if is_job_link:
                    job_url = self.normalize_url(href)
                    parent = link.find_parent(['article', 'div', 'li', 'section', 'tr', 'td', 'p'])
                    
                    # Get title from link or parent
                    title = text.strip() if text.strip() else None
                    if not title and parent:
                        title_elem = parent.find(['h1', 'h2', 'h3', 'h4', 'h5', 'strong', 'b'])
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                    
                    # If still no title, use link text or parent text
                    if not title:
                        if text.strip():
                            title = text.strip()
                        elif parent:
                            parent_text = parent.get_text(strip=True)
                            if parent_text:
                                title = parent_text[:100].strip()
                    
                    if not title:
                        continue
                    
                    # Extract description
                    description = ""
                    if parent:
                        desc_elem = parent.find(['p', 'div'], class_=lambda x: x and any(
                            kw in str(x).lower() for kw in ['desc', 'excerpt', 'summary', 'content', 'text']
                        ))
                        if not desc_elem:
                            desc_elem = parent.find('p')
                        if desc_elem:
                            description = desc_elem.get_text(strip=True)
                    
                            # Detect role and facility
                            role = self.detect_role(title)
                            # For UCK, facility is always UCK, but try to extract department/clinic
                            facility_name = self.facility_name
                            # Try to extract department from title (e.g., "Klinika X" or "Zakład Y")
                            if 'klinika' in title.lower() or 'zakład' in title.lower() or 'pracownia' in title.lower():
                                # Extract the department name
                                parts = title.split('-')
                                if len(parts) > 0:
                                    # Take first part that contains department info
                                    for part in parts:
                                        part_lower = part.lower()
                                        if any(kw in part_lower for kw in ['klinika', 'zakład', 'pracownia', 'oddział']):
                                            dept = part.strip()
                                            if dept:
                                                facility_name = f"{self.facility_name} - {dept}"
                                                break
                            
                            jobs.append({
                                'title': title[:500] if title else "Oferta pracy",
                                'facility_name': facility_name,
                                'city': self.city,
                                'role': role,
                                'description': description[:1000] if description else None,
                                'source_url': job_url,
                            })
        
        # Strategy 5: Look for text patterns that indicate job listings (even without links)
        # This handles cases where jobs are listed as plain text
        if not jobs:
            # Look for headings or paragraphs with job-related text
            all_elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'div', 'li'])
            for elem in all_elements:
                text = elem.get_text(strip=True)
                text_lower = text.lower()
                
                # Check if this element contains job-related keywords
                if any(keyword in text_lower for keyword in ['oferta pracy', 'zatrudnienie', 'rekrutacja']):
                    # Check if it also mentions medical roles
                    if any(role_keyword in text_lower for role_keyword in ['pielęgniarka', 'pielęgniarz', 'lekarz', 'położna', 'ratownik']):
                        # Try to find a link nearby
                        link = elem.find('a', href=True)
                        if not link:
                            # Look in parent or siblings
                            parent = elem.find_parent(['div', 'section', 'article'])
                            if parent:
                                link = parent.find('a', href=True)
                        
                        job_url = self.normalize_url(link.get('href', self.base_url)) if link else self.base_url
                        
                        # Use element text as title
                        title = text[:500]
                        role = self.detect_role(title)
                        # For UCK, facility is always UCK
                        facility_name = self.facility_name
                        # Try to extract department if present
                        if 'klinika' in title.lower() or 'zakład' in title.lower() or 'pracownia' in title.lower():
                            parts = title.split('-')
                            for part in parts:
                                part_lower = part.lower()
                                if any(kw in part_lower for kw in ['klinika', 'zakład', 'pracownia', 'oddział']):
                                    dept = part.strip()
                                    if dept:
                                        facility_name = f"{self.facility_name} - {dept}"
                                        break
                        
                        jobs.append({
                            'title': title,
                            'facility_name': facility_name,
                            'city': self.city,
                            'role': role,
                            'description': None,
                            'source_url': job_url,
                        })
        
        # Process containers if found
        for container in job_containers:
            # Find link
            link = container.find('a', href=True)
            if not link:
                continue
            
            href = link.get('href', '')
            # Filter out non-job links
            if not any(keyword in href.lower() for keyword in ['oferta', 'praca', 'kariera', 'job', 'rekrutacja']):
                continue
            
            job_url = self.normalize_url(href)
            
            # Extract title
            title = link.get_text(strip=True)
            if not title:
                title_elem = container.find(['h1', 'h2', 'h3', 'h4', 'h5', 'strong', 'b'])
                if title_elem:
                    title = title_elem.get_text(strip=True)
            
            if not title:
                continue
            
            # Extract description
            description = ""
            desc_elem = container.find(['p', 'div'], class_=lambda x: x and any(
                kw in str(x).lower() for kw in ['desc', 'excerpt', 'summary', 'content', 'text']
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

