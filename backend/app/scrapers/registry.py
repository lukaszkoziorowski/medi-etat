"""
Scraper registry - manages all available scrapers.
"""
from typing import Dict, Type

from app.scrapers.base import BaseScraper
from app.scrapers.oipip_gdansk import OipipGdanskScraper
from app.scrapers.szpitalepomorskie import SzpitalePomorskieScraper
from app.scrapers.copernicus import CopernicusScraper
from app.scrapers.uck import UckScraper
from app.scrapers.config_loader import load_config, list_configs
from app.scrapers.config_scraper import ConfigBasedScraper


# Registry of hardcoded scrapers (legacy)
HARDCODED_SCRAPERS: Dict[str, Type[BaseScraper]] = {
    'oipip_gdansk': OipipGdanskScraper,
    'szpitalepomorskie': SzpitalePomorskieScraper,
    'copernicus': CopernicusScraper,
    'uck': UckScraper,
}


def get_scraper(name: str) -> BaseScraper:
    """
    Get scraper instance by name.
    Tries config-based scrapers first, then falls back to hardcoded scrapers.
    
    Args:
        name: Scraper name (config ID or hardcoded scraper name)
        
    Returns:
        Scraper instance with source_id set
        
    Raises:
        ValueError: If scraper name not found
    """
    # Try config-based scraper first
    config = load_config(name)
    if config:
        scraper = ConfigBasedScraper(config)
        scraper.source_id = name  # Set source_id
        return scraper
    
    # Fall back to hardcoded scrapers
    if name in HARDCODED_SCRAPERS:
        scraper_class = HARDCODED_SCRAPERS[name]
        scraper = scraper_class()
        scraper.source_id = name  # Set source_id
        return scraper
    
    # List all available scrapers
    all_scrapers = list_hardcoded_scrapers() + list_config_scrapers()
    available = ', '.join(all_scrapers)
    raise ValueError(f"Scraper '{name}' not found. Available: {available}")


def list_scrapers() -> list:
    """List all available scraper names (hardcoded + config-based)."""
    return list_hardcoded_scrapers() + list_config_scrapers()


def list_hardcoded_scrapers() -> list:
    """List hardcoded scraper names."""
    return list(HARDCODED_SCRAPERS.keys())


def list_config_scrapers() -> list:
    """List config-based scraper names."""
    return list_configs()

