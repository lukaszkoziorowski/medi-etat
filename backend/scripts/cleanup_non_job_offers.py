#!/usr/bin/env python3
"""
Cleanup script to remove job offers that aren't actual job offers.

Removes:
- Document attachments (załącznik, attachment)
- Competition announcements for director positions (konkurs na dyrektora)
- Privacy clauses (klauzula)
- Non-medical jobs (developer, PHP, etc.)
- Other non-job content
"""
import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, init_db
from app.models import JobOffer

# Patterns that indicate non-job offers
NON_JOB_PATTERNS = [
    # Document attachments
    r'\bzałącznik\b',
    r'\bzałacznik\b',
    r'\battachment\b',
    r'\bzałącznik_nr',
    r'\bzałacznik_nr',
    
    # Director competitions (not regular job offers)
    r'konkurs\s+na\s+dyr',
    r'konkurs_na_dyr',
    r'konkurs\s+na\s+stanowisko\s+dyrektora',
    
    # Privacy clauses
    r'\bklauzula\s+informacyjna',
    r'\bklauzula\b',
    
    # Non-medical jobs
    r'\bphp\b',
    r'\bdeveloper\b',
    r'\bразработчик\b',  # Russian: developer
    r'\bмладший\b',  # Russian: junior
    
    # Other non-job indicators
    r'^załącznik',
    r'^załacznik',
    r'^attachment',
    r'^klauzula',
    
    # Tenders and auctions (not job offers)
    r'\bprzetarg\b',
    r'\bsprzedaż\b.*\bśrodka\s+trwałego\b',
    r'\bkonkurs\s+ofert\s+na\s+udzielanie',
    
    # Non-medical job titles
    r'\bfull\s+stack\s+developer\b',
    r'\bteam\s+leader\s+developer\b',
    r'\bmid\s+developer\b',
    r'\bjunior\s+developer\b',
]

def is_non_job_offer(job: JobOffer) -> bool:
    """
    Check if a job offer is actually a non-job offer.
    
    Returns:
        True if this should be removed, False otherwise
    """
    title = (job.title or '').lower()
    description = (job.description or '').lower()
    text = f"{title} {description}"
    
    # Check against patterns
    for pattern in NON_JOB_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    
    # Additional checks
    # Very short titles that are just filenames
    if len(title) < 10 and ('_' in title or title.startswith('załącznik')):
        return True
    
    # Titles that are clearly document names
    if title.startswith('załącznik') or title.startswith('załacznik'):
        return True
    
    return False

def cleanup_non_job_offers(dry_run: bool = False):
    """
    Remove non-job offers from the database.
    
    Args:
        dry_run: If True, only report what would be deleted without actually deleting
    """
    init_db()
    db = SessionLocal()
    
    try:
        # Get all active jobs
        all_jobs = db.query(JobOffer).filter(JobOffer.status == 'active').all()
        
        to_delete = []
        for job in all_jobs:
            if is_non_job_offer(job):
                to_delete.append(job)
        
        print(f"Found {len(to_delete)} non-job offers to remove")
        
        if not to_delete:
            print("No non-job offers found. Database is clean!")
            return
        
        print("\nNon-job offers to be removed:")
        print("=" * 70)
        for job in to_delete:
            print(f"ID {job.id}: {job.title[:70]}")
            print(f"  Facility: {job.facility_name}, Source: {job.source_id}")
            print(f"  URL: {job.source_url[:80]}...")
            print()
        
        if not dry_run:
            # Delete the offers
            deleted_count = 0
            for job in to_delete:
                db.delete(job)
                deleted_count += 1
            
            db.commit()
            print(f"\n✓ Deleted {deleted_count} non-job offers")
        else:
            print(f"\n[DRY RUN] Would delete {len(to_delete)} non-job offers")
            print("Run without --dry-run to actually delete them")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Cleanup non-job offers from database')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be deleted without actually deleting')
    args = parser.parse_args()
    
    print("=" * 70)
    print("Non-Job Offers Cleanup")
    print("=" * 70)
    
    cleanup_non_job_offers(dry_run=args.dry_run)
    
    print("\n✅ Cleanup complete!")
