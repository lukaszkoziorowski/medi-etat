#!/usr/bin/env python3
"""
Script to clean existing job titles and descriptions in the database.
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database import SessionLocal, init_db
from app.models import JobOffer
from app.scrapers.base import BaseScraper
from app.models import MedicalRole

class CleanerScraper(BaseScraper):
    """Dummy scraper just for cleaning functions."""
    def __init__(self):
        super().__init__("", "", "")
    
    def scrape(self):
        return []

def clean_database():
    """Clean all job titles and descriptions in the database."""
    init_db()
    db = SessionLocal()
    scraper = CleanerScraper("", "", "")
    
    try:
        jobs = db.query(JobOffer).all()
        print(f"Found {len(jobs)} jobs to clean...")
        
        updated_count = 0
        for job in jobs:
            original_title = job.title
            cleaned_title = scraper.clean_title(original_title)
            cleaned_facility = scraper.clean_facility_name(job.facility_name)
            
            # Check if cleaning made a difference
            if cleaned_title != original_title or cleaned_facility != job.facility_name:
                job.title = cleaned_title
                job.facility_name = cleaned_facility
                updated_count += 1
                
                if updated_count <= 5:  # Show first 5 examples
                    print(f"\nUpdated job ID {job.id}:")
                    print(f"  Old title: {original_title[:100]}...")
                    print(f"  New title: {cleaned_title}")
        
        db.commit()
        print(f"\n✅ Cleaned {updated_count} job titles")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    clean_database()

