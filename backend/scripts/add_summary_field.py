#!/usr/bin/env python3
"""
Migration script to add summary field to existing job offers.

This script:
1. Adds the summary column to the database (if it doesn't exist)
2. Generates summaries for all existing job offers that don't have one
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.database import SessionLocal, engine, init_db
from app.models import JobOffer, Base
from app.utils.summary import extract_summary

def migrate():
    """Add summary column and generate summaries for existing jobs."""
    db = SessionLocal()
    
    try:
        # Check if summary column exists
        inspector = __import__('sqlalchemy').inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('job_offers')]
        
        if 'summary' not in columns:
            print("Adding summary column to job_offers table...")
            db.execute(text("ALTER TABLE job_offers ADD COLUMN summary VARCHAR(500)"))
            db.commit()
            print("✅ Summary column added")
        else:
            print("✅ Summary column already exists")
        
        # Generate summaries for jobs that don't have one
        jobs_without_summary = db.query(JobOffer).filter(
            (JobOffer.summary.is_(None)) | (JobOffer.summary == '')
        ).all()
        
        print(f"\nFound {len(jobs_without_summary)} jobs without summaries")
        
        updated = 0
        for job in jobs_without_summary:
            summary = extract_summary(
                title=job.title,
                description=job.description,
                facility_name=job.facility_name,
                city=job.city
            )
            job.summary = summary
            updated += 1
            
            if updated % 50 == 0:
                db.commit()
                print(f"  Processed {updated} jobs...")
        
        db.commit()
        print(f"\n✅ Generated summaries for {updated} jobs")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == '__main__':
    print("Starting summary migration...")
    init_db()
    migrate()
    print("\n✅ Migration complete!")
