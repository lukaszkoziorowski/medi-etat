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
from app.utils.summary import extract_summary


class BaseScraper(ABC):
    """Base class for all job offer scrapers."""
    
    def __init__(self, base_url: str, facility_name: str, city: str = "Gdańsk", source_id: str = None):
        """
        Initialize scraper.
        
        Args:
            base_url: Base URL of the career/job offers page
            facility_name: Name of the medical facility
            city: City name (default: Gdańsk)
            source_id: Unique identifier for this source (e.g., 'oipip_gdansk')
        """
        self.base_url = base_url
        self.facility_name = facility_name
        self.city = city
        self.source_id = source_id
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
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
            # Add retry logic for 503 errors
            import time
            max_retries = 3
            retry_delay = 2  # seconds
            
            for attempt in range(max_retries):
                response = self.session.get(url, timeout=15)
                
                # If 503, wait and retry
                if response.status_code == 503 and attempt < max_retries - 1:
                    print(f"503 error for {url}, retrying in {retry_delay}s (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                
                response.raise_for_status()
                
                # Try to detect encoding, fallback to utf-8 with error handling
                content = response.content
                encoding = response.encoding or 'utf-8'
                
                # Try to decode with detected encoding, fallback to utf-8 with errors='replace'
                try:
                    text = content.decode(encoding)
                except (UnicodeDecodeError, LookupError):
                    try:
                        text = content.decode('utf-8', errors='replace')
                    except:
                        text = content.decode('latin-1', errors='replace')
                
                return BeautifulSoup(text, 'lxml')
                
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
    
    def extract_city(self, text: str) -> Optional[str]:
        """
        Extract city name from text (title or description).
        
        Args:
            text: Text to search for city name
            
        Returns:
            City name if found, None otherwise
        """
        if not text:
            return None
        
        # List of major Polish cities and towns (expanded list)
        polish_cities = [
            'Warszawa', 'Kraków', 'Wrocław', 'Poznań', 'Gdańsk', 'Szczecin',
            'Bydgoszcz', 'Lublin', 'Katowice', 'Białystok', 'Gdynia', 'Częstochowa',
            'Radom', 'Sosnowiec', 'Toruń', 'Kielce', 'Gliwice', 'Zabrze', 'Bytom',
            'Olsztyn', 'Bielsko-Biała', 'Rzeszów', 'Ruda Śląska', 'Rybnik',
            'Tychy', 'Dąbrowa Górnicza', 'Elbląg', 'Płock', 'Opole', 'Gorzów Wielkopolski',
            'Wałbrzych', 'Zielona Góra', 'Włocławek', 'Tarnów', 'Chorzów', 'Kalisz',
            'Koszalin', 'Legnica', 'Grudziądz', 'Słupsk', 'Jaworzno', 'Jastrzębie-Zdrój',
            'Jelenia Góra', 'Nowy Sącz', 'Jaworzno', 'Konin', 'Piotrków Trybunalski',
            'Lubin', 'Inowrocław', 'Ostrów Wielkopolski', 'Stargard', 'Mysłowice',
            'Piekary Śląskie', 'Gniezno', 'Oława', 'Głogów', 'Żory', 'Tarnowskie Góry',
            # Smaller towns from job titles we've seen
            'Kartuzy', 'Kościerzyna', 'Chojnice', 'Człuchów', 'Reda', 'Sopot', 'Gdynia',
            'Wejherowo', 'Rumia', 'Pruszcz Gdański', 'Tczew', 'Malbork', 'Kwidzyn',
            'Starogard Gdański', 'Lębork', 'Bytów', 'Puck', 'Władysławowo', 'Hel',
            'Jastarnia', 'Ustka', 'Słupsk', 'Miastko', 'Bytów', 'Czarna Woda',
            'Skarszewy', 'Nowy Dwór Gdański', 'Krynica Morska', 'Stegna', 'Jantar',
        ]
        
        text_upper = text.upper()
        
        # Search for cities (case-insensitive)
        for city in polish_cities:
            # Match whole word to avoid false positives
            pattern = r'\b' + re.escape(city) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                return city
        
        # Also check for patterns like "Miejsce pracy: City" or "City –" or "– City"
        city_patterns = [
            r'Miejsce\s+pracy\s*:?\s*([A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+(?:\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+)?)',
            r'[–-]\s*([A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+(?:\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+)?)\s*[–-]',
        ]
        
        for pattern in city_patterns:
            match = re.search(pattern, text)
            if match:
                potential_city = match.group(1).strip()
                # Verify it's a known city
                if potential_city in polish_cities:
                    return potential_city
        
        return None
    
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
        Extracts only the actual job title, removing location, dates, and other metadata.
        
        Args:
            title: Raw title text
            
        Returns:
            Cleaned title
        """
        if not title:
            return ""
        
        # Remove duplicated text patterns (e.g., "Asystent zarząduAsystent zarządu")
        # This happens when screen-reader text or HTML structure causes duplication
        # Check if the title is essentially duplicated (first half matches second half)
        if len(title) > 10:
            mid = len(title) // 2
            first_half = title[:mid].strip()
            second_half = title[mid:].strip()
            
            # Check if halves are identical (case-insensitive)
            if first_half.lower() == second_half.lower():
                title = first_half
            # Check if first half is contained in second half (with some tolerance)
            elif len(first_half) > 5 and first_half.lower() in second_half.lower():
                # If second half starts with first half, remove the duplicate
                if second_half.lower().startswith(first_half.lower()):
                    title = first_half
            # Check if second half is contained in first half
            elif len(second_half) > 5 and second_half.lower() in first_half.lower():
                if first_half.lower().endswith(second_half.lower()):
                    title = second_half
        
        # Also check for word-level duplication (e.g., "Word Word" or "Phrase Phrase")
        words = title.split()
        if len(words) > 1:
            cleaned_words = []
            i = 0
            while i < len(words):
                current_word = words[i]
                # Check if next word is duplicate
                if i + 1 < len(words) and current_word.lower() == words[i + 1].lower():
                    cleaned_words.append(current_word)
                    i += 2  # Skip the duplicate
                # Check for phrase duplication (two-word phrases)
                elif i + 3 < len(words):
                    phrase1 = f"{current_word} {words[i + 1]}"
                    phrase2 = f"{words[i + 2]} {words[i + 3]}"
                    if phrase1.lower() == phrase2.lower():
                        cleaned_words.append(current_word)
                        cleaned_words.append(words[i + 1])
                        i += 4  # Skip the duplicate phrase
                    else:
                        cleaned_words.append(current_word)
                        i += 1
                else:
                    cleaned_words.append(current_word)
                    i += 1
            title = ' '.join(cleaned_words)
        
        # First, try to split on common separators that indicate metadata sections
        # Patterns like "Miejsce pracy:", "Termin zgłoszenia", "APLIKUJ", etc.
        separators = [
            r'Miejsce\s+pracy\s*:',
            r'Termin\s+zgłoszenia\s*do\s*:',
            r'Termin\s+zgłoszenia\s*:',
            r'APLIKUJ',
            r'ROZMOWY\s+REKRUTACYJNE',
            r'Zatrudnienie\s+na',
            r'MOŻLIWOŚĆ\s+ZATRUDNIENIA',
        ]
        
        # Find the first separator and cut everything after it
        for separator in separators:
            match = re.search(separator, title, re.IGNORECASE)
            if match:
                title = title[:match.start()].strip()
                break
        
        # Handle patterns like:
        # "Oferta pracy – Facility – City – Role" → extract "Role"
        # "Facility – City – Role" → extract "Role"
        if '–' in title or '-' in title:
            # Split by dash (both en-dash and hyphen)
            parts = re.split(r'[–-]+', title)
            parts = [p.strip() for p in parts if p.strip()]
            
            # Check if we have at least 3 parts (Facility – City – Role pattern)
            if len(parts) >= 3:
                # Check if it starts with "Oferta pracy" or similar (remove that prefix)
                if re.match(r'^(Oferta\s+pracy|Oferty\s+pracy|Oferta|Praca)', parts[0], re.IGNORECASE):
                    parts = parts[1:]  # Remove the "Oferta pracy" part
                
                if len(parts) >= 2:
                    # The last part is usually the role
                    last_part = parts[-1]
                    
                    # Check if last part is a medical role
                    role_keywords = ['pielęgniarka', 'pielęgniarz', 'lekarz', 'położna', 'położny', 
                                   'ratownik', 'specjalista', 'asystent', 'koordynator', 'kierownik',
                                   'operacyjn', 'anestezjolog', 'okulista', 'kardiolog', 'radiolog']
                    
                    # Check if last part contains role keywords
                    last_has_role = any(kw in last_part.lower() for kw in role_keywords)
                    
                    if last_has_role:
                        # If last part has multiple roles separated by dash, check if second-to-last is also a role
                        if len(parts) >= 3:
                            second_last = parts[-2]
                            second_has_role = any(kw in second_last.lower() for kw in role_keywords)
                            
                            # If both last and second-to-last are roles, combine them
                            if second_has_role:
                                # Combine: "Pielęgniarka – Pielęgniarz" or similar
                                title = f"{second_last} – {last_part}"
                            else:
                                # Just use the last part
                                title = last_part
                        else:
                            # Use the last part as the title
                            title = last_part
                    elif len(parts) >= 3:
                        # If we have 3+ parts, try the second-to-last as it might be the role
                        second_last = parts[-2]
                        if any(kw in second_last.lower() for kw in role_keywords):
                            title = second_last
                    # If last part has multiple roles separated by slash, use it as is
                    elif '/' in last_part:
                        # Multiple roles in last part separated by slash, use it
                        title = last_part
        
        # Remove common prefixes
        title = re.sub(r'^(Oferta pracy|Oferty pracy|Oferta|Praca)\s*[–-]\s*', '', title, flags=re.IGNORECASE)
        
        # Remove navigation text patterns (more aggressive)
        title = re.sub(r'\b(BIP|Intranet|Poczta|Rejestracja|Menu|Szukaj)\b.*', '', title, flags=re.IGNORECASE)
        
        # Remove phone numbers
        title = re.sub(r'\d{2,3}\s*\d{3}\s*\d{2}\s*\d{2}', '', title)
        
        # Remove "Ta strona używa plików cookies" and similar
        title = re.sub(r'Ta strona.*', '', title, flags=re.IGNORECASE)
        
        # Remove "Miejsce pracy:" patterns from title (in case it wasn't caught above)
        title = re.sub(r'Miejsce\s+pracy\s*:?\s*[A-Za-z\s]*', '', title, flags=re.IGNORECASE)
        
        # Remove date patterns that might be in the title
        title = re.sub(r'\d{1,2}\.\d{1,2}\.\d{4}', '', title)
        
        # Remove extra whitespace
        title = ' '.join(title.split())
        
        # Remove trailing dashes and separators (escape dash properly)
        title = re.sub(r'\s*[–\-:]\s*$', '', title)
        
        # If title starts with navigation text, try to find the actual title
        if title and len(title) > 0:
            # Check if title is mostly navigation text (BIP, Intranet, etc.)
            nav_keywords = ['BIP', 'INTRANET', 'POCZTA', 'REJESTRACJA', 'MENU', 'SZUKAJ']
            title_upper = title.upper()
            nav_count = sum(1 for nav in nav_keywords if nav in title_upper)
            
            # If more than 2 navigation keywords, it's likely all navigation
            if nav_count >= 2:
                # Try to find job-related keywords and take text from there
                job_keywords = ['pielęgniarka', 'lekarz', 'położna', 'ratownik', 'oferta', 'praca', 'zatrudn', 'rekrut']
                words = title.split()
                for i, word in enumerate(words):
                    if any(kw in word.lower() for kw in job_keywords):
                        title = ' '.join(words[i:])
                        break
                else:
                    # If no job keywords found, try to find first meaningful word
                    # Skip common navigation words
                    skip_words = ['bip', 'intranet', 'poczta', 'rejestracja', 'menu', 'szukaj', 'ta', 'strona', 'używa', 'plików', 'cookies']
                    for i, word in enumerate(words):
                        if word.lower() not in skip_words and len(word) > 2:
                            title = ' '.join(words[i:])
                            break
        
        # Limit length - titles should be concise
        if len(title) > 200:
            # Try to find a natural break point (sentence end, dash, etc.)
            for break_char in ['.', '–', '-', ':', ';']:
                if break_char in title[:200]:
                    title = title[:title[:200].rfind(break_char)].strip()
                    break
            else:
                # If no break point, just truncate at word boundary
                words = title[:200].split()
                title = ' '.join(words[:-1]) if len(words) > 1 else title[:200]
        
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
        Legacy method - use save_or_update_to_db for refresh mechanism.
        
        Args:
            jobs: List of job dictionaries
            db: Database session
            
        Returns:
            Number of new jobs saved
        """
        return self.save_or_update_to_db(jobs, db, update_existing=False)
    
    def save_or_update_to_db(self, jobs: List[Dict], db: Session, update_existing: bool = True) -> Dict[str, int]:
        """
        Save or update scraped jobs to database.
        
        Args:
            jobs: List of job dictionaries
            db: Database session
            update_existing: If True, update existing offers; if False, skip them
            
        Returns:
            Dictionary with counts: {'new': int, 'updated': int, 'skipped': int}
        """
        now = datetime.utcnow()
        result = {'new': 0, 'updated': 0, 'skipped': 0}
        
        for job_data in jobs:
            # Check if job already exists (by source_url)
            existing = db.query(JobOffer).filter(
                JobOffer.source_url == job_data['source_url']
            ).first()
            
            # Clean data before saving/updating
            cleaned_title = self.clean_title(job_data['title'])
            cleaned_facility = self.clean_facility_name(job_data['facility_name'])
            
            # Extract city from title or description if not explicitly set or if default
            extracted_city = job_data.get('city', self.city)
            
            # If city is the default (Gdańsk) or seems generic, try to extract from title/description
            if extracted_city == "Gdańsk" or not extracted_city:
                # Try to extract city from original title (before cleaning)
                city_from_title = self.extract_city(job_data['title'])
                if city_from_title:
                    extracted_city = city_from_title
                else:
                    # Try description if available
                    if job_data.get('description'):
                        city_from_desc = self.extract_city(job_data['description'])
                        if city_from_desc:
                            extracted_city = city_from_desc
            
            # If description is missing but title had extra info, try to extract it
            if not job_data.get('description') and job_data['title'] != cleaned_title:
                # Extract the part that was removed from title as potential description
                original_title = job_data['title']
                # Find where the cleaned title ends in the original
                if cleaned_title in original_title:
                    remaining = original_title[original_title.find(cleaned_title) + len(cleaned_title):].strip()
                    if remaining and len(remaining) > 10:
                        # Clean up the remaining text for description
                        remaining = re.sub(r'^(Miejsce\s+pracy|Termin\s+zgłoszenia|APLIKUJ|ROZMOWY).*', '', remaining, flags=re.IGNORECASE)
                        if remaining and len(remaining) > 10:
                            job_data['description'] = remaining[:1000]
            
            if existing:
                if not update_existing:
                    result['skipped'] += 1
                    continue
                
                # Case A: Update existing offer
                updated = False
                content_changed = False
                
                # Check if content changed
                if existing.title != cleaned_title:
                    existing.title = cleaned_title
                    updated = True
                    content_changed = True
                if existing.facility_name != cleaned_facility:
                    existing.facility_name = cleaned_facility
                    updated = True
                if existing.city != extracted_city:
                    existing.city = extracted_city
                    updated = True
                if existing.role != job_data['role']:
                    existing.role = job_data['role']
                    updated = True
                if existing.description != job_data.get('description'):
                    existing.description = job_data.get('description')
                    updated = True
                    content_changed = True
                
                # Generate summary only if content changed (title or description)
                if content_changed:
                    job_summary = extract_summary(
                        title=cleaned_title,
                        description=job_data.get('description'),
                        facility_name=cleaned_facility,
                        city=extracted_city
                    )
                    if existing.summary != job_summary:
                        existing.summary = job_summary
                        updated = True
                
                # Always update timestamps
                existing.scraped_at = now
                existing.last_seen_at = now
                
                # Update source_id if not set
                if not existing.source_id and self.source_id:
                    existing.source_id = self.source_id
                
                # Update external_job_url if provided
                if job_data.get('external_job_url') and existing.external_job_url != job_data['external_job_url']:
                    existing.external_job_url = job_data.get('external_job_url')
                
                # Reactivate if was inactive
                if existing.status == 'inactive':
                    existing.status = 'active'
                    updated = True
                
                if updated:
                    result['updated'] += 1
                else:
                    result['skipped'] += 1
            else:
                # Case B: Insert new offer
                # Generate summary for new offers
                job_summary = extract_summary(
                    title=cleaned_title,
                    description=job_data.get('description'),
                    facility_name=cleaned_facility,
                    city=extracted_city
                )
                
                job_offer = JobOffer(
                    title=cleaned_title,
                    facility_name=cleaned_facility,
                    city=extracted_city,
                    role=job_data['role'],
                    description=job_data.get('description'),
                    summary=job_summary,
                    source_url=job_data['source_url'],
                    source_id=self.source_id,
                    external_job_url=job_data.get('external_job_url'),
                    scraped_at=now,
                    first_seen_at=now,
                    last_seen_at=now,
                    status='active',
                )
                
                db.add(job_offer)
                result['new'] += 1
        
        db.commit()
        return result

