"""
Base scraper class with common functionality.
"""
import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from app.models import JobOffer, MedicalRole
from app.scrapers.playwright_helper import PlaywrightHelper


class BaseScraper(ABC):
    """Base class for all job offer scrapers."""
    
    def __init__(self, base_url: str, facility_name: str, city: str = "Gdańsk"):
        """
        Initialize scraper.
        
        Args:
            base_url: Base URL of the career/job offers page
            facility_name: Name of the medical facility
            city: City name (default: Gdańsk)
        """
        self.base_url = base_url
        self.facility_name = facility_name
        self.city = city
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def fetch_page(self, url: str, use_playwright: bool = False, wait_selector: Optional[str] = None) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a web page.
        
        Args:
            url: URL to fetch
            use_playwright: If True, use Playwright for JavaScript-rendered pages
            wait_selector: Optional CSS selector to wait for (Playwright only)
            
        Returns:
            BeautifulSoup object or None if fetch fails
        """
        if use_playwright:
            return PlaywrightHelper.fetch_page(url, wait_selector=wait_selector)
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def normalize_url(self, url: str) -> str:
        """
        Normalize URL (make absolute if relative).
        
        Args:
            url: URL to normalize
            
        Returns:
            Absolute URL
        """
        if url.startswith('http'):
            return url
        return urljoin(self.base_url, url)
    
    def detect_role(self, text: str) -> MedicalRole:
        """
        Detect medical role from text using keyword matching.
        
        Args:
            text: Text to analyze (title, description, etc.)
            
        Returns:
            Detected MedicalRole
        """
        text_lower = text.lower()
        
        # Role detection keywords (order matters - more specific first)
        role_keywords = {
            MedicalRole.POŁOŻNA: ['położna', 'położny', 'midwife'],
            MedicalRole.RATOWNIK: ['ratownik medyczny', 'ratownik', 'paramedic'],
            MedicalRole.LEKARZ: ['lekarz', 'doktor', 'doctor', 'specjalista'],
            MedicalRole.PIELĘGNIARKA: ['pielęgniarka', 'pielęgniarz', 'nurse'],
        }
        
        for role, keywords in role_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return role
        
        return MedicalRole.INNY
    
    def extract_facility_name(self, text: str) -> str:
        """
        Extract facility name from text if possible.
        
        Args:
            text: Text to extract facility name from
            
        Returns:
            Extracted facility name or empty string
        """
        # Common patterns: "Oferta pracy - Facility Name" or similar
        if '–' in text or '-' in text:
            parts = text.replace('–', '-').split('-')
            if len(parts) >= 2:
                return parts[1].strip()
        return ""
    
    def clean_title(self, title: str) -> str:
        """
        Clean and normalize job title.
        
        Args:
            title: Raw title text
            
        Returns:
            Cleaned title
        """
        if not title:
            return ""
        
        # Remove common prefixes
        title = re.sub(r'^(Oferta pracy|Oferty pracy|Oferta|Praca)\s*[–-]\s*', '', title, flags=re.IGNORECASE)
        
        # Remove navigation text patterns (more aggressive)
        title = re.sub(r'\b(BIP|Intranet|Poczta|Rejestracja|Menu|Szukaj)\b.*', '', title, flags=re.IGNORECASE)
        
        # Remove phone numbers
        title = re.sub(r'\d{2,3}\s*\d{3}\s*\d{2}\s*\d{2}', '', title)
        
        # Remove "Ta strona używa plików cookies" and similar
        title = re.sub(r'Ta strona.*', '', title, flags=re.IGNORECASE)
        
        # Remove "Miejsce pracy:" patterns from title
        title = re.sub(r'Miejsce\s+pracy\s*:?\s*[A-Za-z\s]*', '', title, flags=re.IGNORECASE)
        
        # Remove extra whitespace
        title = ' '.join(title.split())
        
        # Remove trailing dashes and separators (escape dash properly)
        title = re.sub(r'\s*[–\-:]\s*$', '', title)
        
        # If title starts with navigation text, try to find the actual title
        if title and len(title) > 0:
            # Check if first word is navigation
            first_words = title.split()[:3]
            if any(nav in ' '.join(first_words).upper() for nav in ['BIP', 'INTRANET', 'POCZTA']):
                # Try to find job-related keywords and take text from there
                job_keywords = ['pielęgniarka', 'lekarz', 'położna', 'ratownik', 'oferta', 'praca']
                for i, word in enumerate(title.split()):
                    if any(kw in word.lower() for kw in job_keywords):
                        title = ' '.join(title.split()[i:])
                        break
        
        # Limit length
        if len(title) > 500:
            title = title[:497] + "..."
        
        return title.strip()
    
    def clean_facility_name(self, facility_name: str) -> str:
        """
        Clean and normalize facility name.
        
        Args:
            facility_name: Raw facility name
            
        Returns:
            Cleaned facility name
        """
        if not facility_name:
            return self.facility_name
        
        # Remove common suffixes/prefixes that got mixed in (more aggressive)
        facility_name = re.sub(r'\s*(Miejsce pracy|Termin|APLIKUJ|ROZMOWY|Termin zgłoszenia|Aplikuj).*', '', facility_name, flags=re.IGNORECASE)
        
        # Remove patterns like "Miejsce pracy:Gdańsk" or "Miejsce pracy: Gdańsk"
        facility_name = re.sub(r'Miejsce\s+pracy\s*:?\s*[A-Za-z\s]*', '', facility_name, flags=re.IGNORECASE)
        
        # Remove navigation text
        facility_name = re.sub(r'\b(BIP|Intranet|Poczta|Rejestracja|Menu|Szukaj)\b.*', '', facility_name, flags=re.IGNORECASE)
        
        # Remove phone numbers that got mixed in
        facility_name = re.sub(r'\d{2,3}\s*\d{3}\s*\d{2}\s*\d{2}', '', facility_name)
        
        # Remove extra whitespace and newlines
        facility_name = ' '.join(facility_name.split())
        
        # Remove trailing separators and colons (escape dash properly)
        facility_name = re.sub(r'\s*[–\-:]\s*$', '', facility_name)
        
        # If facility name contains the title pattern (e.g., "Pielęgniarka/Pielęgniarz Pracownia..."), extract just the department
        if 'Pielęgniarka' in facility_name or 'Lekarz' in facility_name or 'Położna' in facility_name:
            # Try to extract department name after the role
            parts = re.split(r'(Pielęgniarka|Pielęgniarz|Lekarz|Położna|Ratownik)', facility_name, flags=re.IGNORECASE)
            if len(parts) > 2:
                # Take the part after the role
                facility_name = parts[2].strip()
                # Remove any remaining role mentions
                facility_name = re.sub(r'\s*(Pielęgniarka|Pielęgniarz|Lekarz|Położna|Ratownik)\s*', '', facility_name, flags=re.IGNORECASE)
        
        # Limit length
        if len(facility_name) > 255:
            facility_name = facility_name[:252] + "..."
        
        cleaned = facility_name.strip()
        return cleaned if cleaned else self.facility_name
    
    @abstractmethod
    def scrape(self) -> List[Dict]:
        """
        Scrape job offers from the source.
        
        Returns:
            List of job offer dictionaries with keys:
            - title: str
            - facility_name: str
            - city: str
            - role: MedicalRole
            - description: str (optional)
            - source_url: str
        """
        pass
    
    def save_to_db(self, jobs: List[Dict], db: Session) -> int:
        """
        Save scraped jobs to database (with deduplication).
        
        Args:
            jobs: List of job dictionaries
            db: Database session
            
        Returns:
            Number of new jobs saved
        """
        saved_count = 0
        
        for job_data in jobs:
            # Check if job already exists (by source_url)
            existing = db.query(JobOffer).filter(
                JobOffer.source_url == job_data['source_url']
            ).first()
            
            if existing:
                continue  # Skip duplicates
            
            # Clean data before saving
            cleaned_title = self.clean_title(job_data['title'])
            cleaned_facility = self.clean_facility_name(job_data['facility_name'])
            
            # Create new job offer
            job_offer = JobOffer(
                title=cleaned_title,
                facility_name=cleaned_facility,
                city=job_data['city'],
                role=job_data['role'],
                description=job_data.get('description'),
                source_url=job_data['source_url'],
                scraped_at=datetime.utcnow(),
            )
            
            db.add(job_offer)
            saved_count += 1
        
        db.commit()
        return saved_count

