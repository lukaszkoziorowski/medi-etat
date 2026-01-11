"""
AI-assisted HTML structure detector for job listings.
"""
import re
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin

from bs4 import BeautifulSoup

# Polish job-related keywords
JOB_KEYWORDS = [
    'oferta', 'praca', 'zatrudnienie', 'rekrutacja', 'kariera',
    'stanowisko', 'wolne', 'poszukujemy', 'szukamy'
]

MEDICAL_ROLE_KEYWORDS = [
    'lekarz', 'pielęgniarka', 'pielęgniarz', 'położna', 'położny',
    'ratownik', 'specjalista', 'doktor'
]


class StructureDetector:
    """Detects job listing structure in HTML."""
    
    def __init__(self, soup: BeautifulSoup, base_url: str):
        self.soup = soup
        self.base_url = base_url
    
    def detect(self) -> Dict:
        """
        Detect job listing structure.
        
        Returns:
            Dictionary with detected selectors and confidence
        """
        results = {
            'jobListContainer': None,
            'jobItem': None,
            'title': None,
            'link': None,
            'description': None,
            'confidence': 'LOW',
            'sampleJobs': [],
            'reasoning': []
        }
        
        # Strategy 1: Find links with job keywords
        job_links = self._find_job_links()
        if job_links:
            results['reasoning'].append(f"Found {len(job_links)} links with job keywords")
            container = self._find_container(job_links)
            if container:
                results['jobListContainer'] = self._get_selector(container)
                results['jobItem'] = self._detect_item_selector(job_links, container)
                results['title'] = self._detect_title_selector(job_links)
                results['link'] = self._detect_link_selector(job_links)
                results['confidence'] = self._calculate_confidence(job_links, container)
                results['sampleJobs'] = self._extract_samples(job_links[:5])
        
        # Strategy 2: Look for repeating patterns
        if results['confidence'] == 'LOW':
            patterns = self._find_repeating_patterns()
            if patterns:
                results['reasoning'].append(f"Found repeating pattern: {patterns[0]['selector']}")
                results['jobListContainer'] = patterns[0].get('container')
                results['jobItem'] = patterns[0].get('item')
                results['title'] = patterns[0].get('title')
                results['link'] = patterns[0].get('link')
                results['confidence'] = 'MEDIUM'
                results['sampleJobs'] = patterns[0].get('samples', [])
        
        # Strategy 3: Common class/id patterns
        if results['confidence'] == 'LOW':
            common_patterns = self._find_common_patterns()
            if common_patterns:
                results.update(common_patterns)
                results['confidence'] = 'MEDIUM'
        
        return results
    
    def _find_job_links(self) -> List:
        """Find links that likely point to job offers."""
        all_links = self.soup.find_all('a', href=True)
        job_links = []
        
        for link in all_links:
            href = link.get('href', '')
            text = link.get_text(strip=True).lower()
            
            # Check if link text or URL contains job keywords
            has_job_keyword = any(kw in text for kw in JOB_KEYWORDS)
            has_medical_keyword = any(kw in text for kw in MEDICAL_ROLE_KEYWORDS)
            has_job_in_url = any(kw in href.lower() for kw in JOB_KEYWORDS)
            
            if has_job_keyword or (has_medical_keyword and has_job_in_url):
                job_links.append(link)
        
        return job_links
    
    def _find_container(self, links: List) -> Optional:
        """Find the common container for job links."""
        if not links:
            return None
        
        # Find common parent
        parents = []
        for link in links[:10]:  # Check first 10 links
            parent = link.find_parent(['article', 'div', 'li', 'section', 'tr'])
            if parent:
                parents.append(parent)
        
        if not parents:
            return None
        
        # Find most common parent tag and class
        parent_tags = {}
        for parent in parents:
            tag = parent.name
            classes = ' '.join(parent.get('class', []))
            key = f"{tag}.{classes}" if classes else tag
            parent_tags[key] = parent_tags.get(key, 0) + 1
        
        if parent_tags:
            most_common = max(parent_tags.items(), key=lambda x: x[1])
            # Return first parent matching the pattern
            for parent in parents:
                tag = parent.name
                classes = ' '.join(parent.get('class', []))
                key = f"{tag}.{classes}" if classes else tag
                if key == most_common[0]:
                    return parent
        
        return parents[0] if parents else None
    
    def _detect_item_selector(self, links: List, container) -> Optional[str]:
        """Detect selector for individual job items."""
        if not links:
            return None
        
        # Find common parent of links
        item_parents = []
        for link in links[:10]:
            # Try to find parent within container
            if container:
                parent = link.find_parent(['article', 'div', 'li', 'section', 'tr'])
                # Check if parent is within container
                if parent:
                    # Check if parent is container itself or within it
                    if parent == container or (hasattr(container, 'find') and container.find(parent.name, parent.get('class', []))):
                        item_parents.append(parent)
                    else:
                        # Check all parents
                        for p in link.parents:
                            if p == container or (hasattr(container, 'find') and container.find(p.name, p.get('class', []))):
                                item_parents.append(p)
                                break
            else:
                # No container, just get parent
                parent = link.find_parent(['article', 'div', 'li', 'section', 'tr'])
                if parent:
                    item_parents.append(parent)
        
        if not item_parents:
            # Fallback: if links are direct children, use link selector
            return None
        
        # Get most common selector
        selectors = {}
        for item in item_parents:
            selector = self._get_selector(item)
            if selector and selector != 'body':
                selectors[selector] = selectors.get(selector, 0) + 1
        
        if selectors:
            return max(selectors.items(), key=lambda x: x[1])[0]
        
        return None
    
    def _detect_title_selector(self, links: List) -> Optional[str]:
        """Detect selector for job title."""
        if not links:
            return None
        
        # Check if link text itself is the title
        link = links[0]
        if link.get_text(strip=True):
            return "a"
        
        # Check for heading near link
        for link in links[:3]:
            # Check parent for heading
            parent = link.find_parent(['article', 'div', 'li'])
            if parent:
                heading = parent.find(['h1', 'h2', 'h3', 'h4', 'h5'])
                if heading:
                    return self._get_selector(heading)
        
        return "a"
    
    def _detect_link_selector(self, links: List) -> Optional[str]:
        """Detect selector for job link."""
        if not links:
            return None
        
        # Links are already found, return selector
        return "a"
    
    def _get_selector(self, element) -> str:
        """Generate CSS selector for element."""
        if element.name == 'body':
            return 'body'
        
        # Build selector
        selector = element.name
        
        # Add ID if present
        if element.get('id'):
            return f"#{element.get('id')}"
        
        # Add classes if present
        classes = element.get('class', [])
        if classes:
            class_str = '.'.join(classes)
            return f"{element.name}.{class_str}"
        
        return selector
    
    def _calculate_confidence(self, links: List, container) -> str:
        """Calculate confidence level."""
        if not links or not container:
            return 'LOW'
        
        # Count how many links have job keywords
        job_keyword_count = sum(
            1 for link in links[:10]
            if any(kw in link.get_text(strip=True).lower() for kw in JOB_KEYWORDS + MEDICAL_ROLE_KEYWORDS)
        )
        
        # Check if pattern repeats
        if len(links) >= 3 and job_keyword_count >= 3:
            return 'HIGH'
        elif len(links) >= 2 and job_keyword_count >= 2:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _extract_samples(self, links: List) -> List[Dict]:
        """Extract sample job data."""
        samples = []
        
        for link in links[:5]:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            # Make absolute URL
            if href:
                url = urljoin(self.base_url, href)
            else:
                url = self.base_url
            
            samples.append({
                'title': text[:100] if text else "No title",
                'url': url
            })
        
        return samples
    
    def _find_repeating_patterns(self) -> List[Dict]:
        """Find repeating DOM patterns that might be job listings."""
        patterns = []
        
        # Look for articles
        articles = self.soup.find_all('article', limit=20)
        if len(articles) >= 3:
            # Check if articles contain links
            article_links = [a.find('a', href=True) for a in articles[:5]]
            if all(article_links):
                patterns.append({
                    'container': 'body',
                    'item': 'article',
                    'title': 'article h2 a, article h3 a, article a',
                    'link': 'article a',
                    'samples': self._extract_samples([l for l in article_links if l])
                })
        
        # Look for list items
        list_items = self.soup.find_all('li', limit=20)
        if len(list_items) >= 3:
            li_links = [li.find('a', href=True) for li in list_items[:10]]
            job_li_links = [
                link for link in li_links if link and
                any(kw in link.get_text(strip=True).lower() for kw in JOB_KEYWORDS + MEDICAL_ROLE_KEYWORDS)
            ]
            if len(job_li_links) >= 3:
                patterns.append({
                    'container': 'ul, ol',
                    'item': 'li',
                    'title': 'li a',
                    'link': 'li a',
                    'samples': self._extract_samples(job_li_links)
                })
        
        return patterns
    
    def _find_common_patterns(self) -> Dict:
        """Find common job board patterns."""
        # Look for common class patterns
        common_classes = ['job', 'offer', 'vacancy', 'position', 'career', 'kariera', 'praca', 'oferta']
        
        for class_name in common_classes:
            elements = self.soup.find_all(class_=re.compile(class_name, re.I))
            if len(elements) >= 3:
                # Check if they contain links
                links = [el.find('a', href=True) for el in elements[:5]]
                if all(links):
                    return {
                        'jobListContainer': 'body',
                        'jobItem': f'.{class_name}',
                        'title': f'.{class_name} a, .{class_name} h2, .{class_name} h3',
                        'link': f'.{class_name} a',
                        'sampleJobs': self._extract_samples([l for l in links if l])
                    }
        
        return {}

