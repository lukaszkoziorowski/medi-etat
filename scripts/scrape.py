#!/usr/bin/env python3
"""
Manual scraper runner script.
Usage: python scripts/scrape.py [scraper_name]
"""
import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

# Change to backend directory so database path is correct
os.chdir(backend_path)

from app.scrapers.registry import get_scraper, list_scrapers
from app.database import SessionLocal, init_db
from app.scrapers.playwright_helper import PlaywrightHelper


def main():
    """Run scraper and save results to database."""
    # Get scraper name from command line or use default
    scraper_name = sys.argv[1] if len(sys.argv) > 1 else 'oipip_gdansk'
    
    if scraper_name == 'list':
        print("Available scrapers:")
        for name in list_scrapers():
            print(f"  - {name}")
        return
    
    try:
        # Get scraper instance
        print(f"Initializing scraper: {scraper_name}")
        scraper = get_scraper(scraper_name)
        
        # Scrape jobs
        print(f"Scraping from: {scraper.base_url}")
        jobs = scraper.scrape()
        print(f"Found {len(jobs)} job offers")
        
        if not jobs:
            print("No jobs found. Exiting.")
            return
        
        # Initialize database if needed
        init_db()
        
        # Save to database
        print("Saving to database...")
        db = SessionLocal()
        try:
            saved_count = scraper.save_to_db(jobs, db)
            print(f"Saved {saved_count} new job offers to database")
        finally:
            db.close()
        
        # Print summary
        print("\nScraped jobs:")
        for i, job in enumerate(jobs[:5], 1):  # Show first 5
            print(f"{i}. {job['title'][:60]}...")
            print(f"   Role: {job['role'].value}, Facility: {job['facility_name']}")
        
        if len(jobs) > 5:
            print(f"... and {len(jobs) - 5} more")
            
    except ValueError as e:
        print(f"Error: {e}")
        print("\nAvailable scrapers:")
        for name in list_scrapers():
            print(f"  - {name}")
    except Exception as e:
        print(f"Error during scraping: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close Playwright browser if it was used
        PlaywrightHelper.close_browser()


if __name__ == '__main__':
    main()

