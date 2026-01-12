#!/usr/bin/env python3
"""
Script to verify and update job offer cities based on title/description content.
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database import SessionLocal, init_db
from app.models import JobOffer
from app.scrapers.base import BaseScraper

class CityVerifierScraper(BaseScraper):
    """Scraper just for city extraction."""
    def __init__(self):
        super().__init__("https://test.pl", "Test", "Gdańsk")
    
    def scrape(self):
        return []

def verify_and_update_cities():
    """Verify and update cities for all jobs."""
    init_db()
    db = SessionLocal()
    scraper = CityVerifierScraper()
    
    try:
        jobs = db.query(JobOffer).all()
        print(f"Verifying cities for {len(jobs)} jobs...\n")
        
        updated = 0
        city_stats = {}
        
        for job in jobs:
            # Try to extract city from title
            city_from_title = scraper.extract_city(job.title)
            
            # Try to extract from description if title didn't work
            city_from_desc = None
            if not city_from_title and job.description:
                city_from_desc = scraper.extract_city(job.description)
            
            extracted_city = city_from_title or city_from_desc
            
            # Update if we found a different city
            if extracted_city and extracted_city != job.city:
                old_city = job.city
                job.city = extracted_city
                updated += 1
                
                # Track city changes
                if extracted_city not in city_stats:
                    city_stats[extracted_city] = 0
                city_stats[extracted_city] += 1
                
                if updated <= 10:  # Show first 10 examples
                    print(f"Job ID {job.id}:")
                    print(f"  Title: {job.title[:60]}...")
                    print(f"  Old city: {old_city}")
                    print(f"  New city: {extracted_city}")
                    print()
        
        db.commit()
        
        print(f"✅ Updated {updated} jobs with verified cities\n")
        
        if city_stats:
            print("City distribution after update:")
            from sqlalchemy import func
            final_stats = db.query(JobOffer.city, func.count(JobOffer.id)).group_by(JobOffer.city).order_by(func.count(JobOffer.id).desc()).all()
            for city, count in final_stats:
                print(f"  {city}: {count} jobs")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    verify_and_update_cities()

