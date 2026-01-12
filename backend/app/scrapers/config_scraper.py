"""
Generic scraper that uses configuration files.
"""
from typing import List, Dict, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.scrapers.base import BaseScraper
from app.scrapers.config_loader import SourceConfig


class ConfigBasedScraper(BaseScraper):
    """Scraper that uses a configuration file."""
    
    def __init__(self, config: SourceConfig):
        super().__init__(
            base_url=config.base_url,
            facility_name=config.facility_name,
            city=config.city
        )
        self.config = config
    
    def scrape(self) -> List[Dict]:
        """
        Scrape job offers using configuration.
        
        Returns:
            List of job offer dictionaries
        """
        jobs = []
        
        # Fetch page (use Playwright if needed)
        use_playwright = self.config._config_dict.get('requiresPlaywright', False)
        soup = self.fetch_page(self.base_url, use_playwright=use_playwright)
        
        if not soup:
            return jobs
        
        # Find job list container
        if self.config.job_list_container:
            # Try to select container - might be multiple
            try:
                containers = soup.select(self.config.job_list_container)
                if len(containers) == 1:
                    container = containers[0]
                elif len(containers) > 1:
                    # Multiple containers found - use the first one that has job links
                    # or combine them
                    container = soup  # Use whole page if multiple containers
                else:
                    container = soup
            except Exception:
                container = soup
        else:
            container = soup
        
        # Find job items
        job_items = []
        
        if self.config.job_item:
            try:
                # Try selecting within container first
                job_items = container.select(self.config.job_item)
                # If that doesn't work or container is whole page, try selecting from whole page
                if not job_items or container == soup:
                    job_items = soup.select(self.config.job_item)
            except Exception as e:
                pass  # Will fall back to link search
        
        # If no items found or jobItem is same as container, look for links directly
        if not job_items:
            # Look for links with job keywords
            search_area = container if container != soup else soup
            all_links = search_area.find_all('a', href=True)
            job_keywords = ['oferta', 'praca', 'zatrudnienie', 'rekrutacja', 'kariera', 'pielęgniarka', 'lekarz', 'położna']
            job_items = [
                link for link in all_links
                if any(kw in link.get_text(strip=True).lower() for kw in job_keywords)
            ]
        
        # Extract jobs from items
        for item in job_items:
            job = self._extract_job(item)
            if job:
                jobs.append(job)
        
        # Handle pagination if configured
        if self.config.pagination_type != 'none' and len(jobs) > 0:
            # For MVP, we'll skip pagination - can be added later
            pass
        
        # Remove duplicates by source_url
        seen_urls = set()
        unique_jobs = []
        for job in jobs:
            if job['source_url'] not in seen_urls:
                seen_urls.add(job['source_url'])
                unique_jobs.append(job)
        
        # Additional deduplication: For sources that create hash-based URLs from the same base URL,
        # group by base URL (without hash) and keep only one job per base URL
        # This prevents duplicates like: base_url#hash1, base_url#hash2, etc.
        import re
        base_url_groups = {}
        final_jobs = []
        
        for job in unique_jobs:
            # Remove hash anchor from URL to get base URL
            base_url = re.sub(r'#.*$', '', job['source_url'])
            
            # If we haven't seen this base URL, keep the job
            if base_url not in base_url_groups:
                base_url_groups[base_url] = job
                final_jobs.append(job)
            else:
                # We've seen this base URL before - this is a duplicate
                # Keep the first one we encountered (already in final_jobs)
                # Skip this duplicate
                pass
        
        return final_jobs
    
    def _extract_job(self, item) -> Optional[Dict]:
        """Extract job data from a job item element."""
        # Find title
        title = self._extract_title(item)
        if not title:
            return None
        
        # Filter out non-job headings (navigation, etc.)
        title_lower = title.lower()
        exclude_keywords = ['rekrutacje', 'menu', 'kontakt', 'o nas', 'oferta', 'dla pacjenta', 
                           'aktualne oferty', 'dołącz do zespołu', 'aktualne oferty pracy',
                           'lux med szpital gdańsk', 'szpital gdańsk']
        if any(exclude in title_lower for exclude in exclude_keywords):
            return None
        
        # Filter out document attachments and non-job content
        non_job_patterns = [
            'załącznik', 'załacznik', 'attachment',
            'konkurs na dyr', 'konkurs_na_dyr', 'konkurs na stanowisko dyrektora',
            'klauzula informacyjna', 'klauzula',
            'przetarg', 'sprzedaż środka trwałego',
            'konkurs ofert na udzielanie',
            'full stack developer', 'team leader developer', 'mid developer', 'junior developer',
            'разработчик', 'младший',  # Russian: developer, junior
        ]
        if any(pattern in title_lower for pattern in non_job_patterns):
            return None
        
        # Filter out titles that are clearly document names
        if title_lower.startswith('załącznik') or title_lower.startswith('załacznik'):
            return None
        
        # Filter out email addresses
        if '@' in title or 'mailto:' in title_lower:
            return None
        
        # Check if it's actually a job title (has medical role keywords or job-related terms)
        job_keywords = ['lekarz', 'fizjoterapeuta', 'specjalista', 'pielęgniarka', 'pielęgniarz', 
                       'anestezjolog', 'okulista', 'kardiolog', 'radiolog', 'gastroenterolog',
                       'ortopeda', 'internista', 'ratownik', 'młodszy', 'starszy', 'koordynator']
        if not any(kw in title_lower for kw in job_keywords):
            # Might still be a job, but be more lenient - check length
            if len(title) < 10 or len(title) > 150:
                return None
            # If it's a very short title without keywords, skip it
            if len(title) < 20:
                return None
        
        # Find link
        link = self._extract_link(item)
        if not link:
            link = self.base_url
        
        job_url = self.normalize_url(link) if self.config.normalize_link and link != self.base_url else link
        
        # If URL is the base URL (no individual page), make it unique by adding title hash
        if job_url == self.base_url or job_url == self.base_url.rstrip('/'):
            # Create unique URL by adding title-based anchor
            import hashlib
            title_hash = hashlib.md5(title.encode('utf-8')).hexdigest()[:8]
            job_url = f"{self.base_url.rstrip('/')}#{title_hash}"
        
        # Find description
        description = self._extract_description(item)
        
        # Detect role
        role = self.detect_role(title)
        
        # Extract facility name
        facility_name = self.extract_facility_name(title) or self.facility_name
        
        return {
            'title': title[:500],
            'facility_name': facility_name,
            'city': self.city,
            'role': role,
            'description': description[:1000] if description else None,
            'source_url': job_url,
        }
    
    def _extract_title(self, item) -> Optional[str]:
        """Extract title from job item."""
        def get_text_without_hidden(elem):
            """Get text from element excluding screen-reader and hidden elements."""
            if not elem:
                return None
            # Clone the element to avoid modifying the original
            from bs4 import BeautifulSoup
            elem_str = str(elem)
            elem_copy = BeautifulSoup(elem_str, 'html.parser')
            # Remove hidden elements
            for hidden in elem_copy.select('.screen-reader-text, .sr-only, [aria-hidden="true"]'):
                hidden.decompose()
            return elem_copy.get_text(strip=True)
        
        if self.config.title_selector:
            title_elem = item.select_one(self.config.title_selector)
            if title_elem:
                if self.config.title_from == 'text':
                    # Remove screen-reader text and other hidden elements to avoid duplication
                    text = get_text_without_hidden(title_elem)
                    return text if text else title_elem.get_text(strip=True)
                elif self.config.title_from == 'attribute':
                    return title_elem.get(self.config.title_from, '')
                else:
                    # Remove screen-reader text
                    text = get_text_without_hidden(title_elem)
                    return text if text else title_elem.get_text(strip=True)
        
        # Fallback: try to find title in item
        heading = item.find(['h1', 'h2', 'h3', 'h4', 'h5'])
        if heading:
            # Remove screen-reader text
            text = get_text_without_hidden(heading)
            return text if text else heading.get_text(strip=True)
        
        link = item.find('a')
        if link:
            # Remove screen-reader text
            text = get_text_without_hidden(link)
            return text if text else link.get_text(strip=True)
        
        # Remove screen-reader text from item
        text = get_text_without_hidden(item)
        return text if text else item.get_text(strip=True)
    
    def _extract_link(self, item) -> Optional[str]:
        """Extract link from job item."""
        # If no link selector configured, use base URL
        if not self.config.link_selector:
            return self.base_url
        
        # If item is already a link, use it directly
        if item.name == 'a' and item.get('href'):
            if self.config.link_from == 'href':
                return item.get('href', '')
            elif self.config.link_from == 'text':
                return item.get_text(strip=True)
            else:
                return item.get(self.config.link_from, '')
        
        # Otherwise, try to find link using selector
        if self.config.link_selector:
            try:
                link_elem = item.select_one(self.config.link_selector)
                if link_elem:
                    if self.config.link_from == 'href':
                        return link_elem.get('href', '')
                    elif self.config.link_from == 'text':
                        return link_elem.get_text(strip=True)
                    else:
                        return link_elem.get(self.config.link_from, '')
            except Exception:
                pass
        
        # Fallback: find any link in item
        link = item.find('a', href=True)
        if link:
            return link.get('href', '')
        
        # If no link found, use base URL
        return self.base_url
    
    def _extract_description(self, item) -> Optional[str]:
        """Extract description from job item."""
        if self.config.description_selector:
            desc_elem = item.select_one(self.config.description_selector)
            if desc_elem:
                return desc_elem.get_text(strip=True)
        
        # Fallback: find paragraph in item
        paragraph = item.find('p')
        if paragraph:
            return paragraph.get_text(strip=True)
        
        return None

