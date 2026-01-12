#!/usr/bin/env python3
"""
Migration script to add refresh mechanism fields to job_offers table.
"""
import os
import sys
from datetime import datetime

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)

from sqlalchemy import text
from app.database import engine, SessionLocal, init_db
from app.models import JobOffer


def migrate():
    """Add new columns and backfill data."""
    db = SessionLocal()
    
    try:
        print("Starting migration...")
        
        # Check if columns already exist by querying table info
        with engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(job_offers)"))
            existing_columns = [row[1] for row in result.fetchall()]
        
        # Add new columns if they don't exist
        with engine.connect() as conn:
            if 'source_id' not in existing_columns:
                print("Adding source_id column...")
                conn.execute(text("ALTER TABLE job_offers ADD COLUMN source_id VARCHAR(100)"))
                conn.commit()
            
            if 'external_job_url' not in existing_columns:
                print("Adding external_job_url column...")
                conn.execute(text("ALTER TABLE job_offers ADD COLUMN external_job_url VARCHAR(1000)"))
                conn.commit()
            
            if 'first_seen_at' not in existing_columns:
                print("Adding first_seen_at column...")
                conn.execute(text("ALTER TABLE job_offers ADD COLUMN first_seen_at DATETIME"))
                conn.commit()
            
            if 'last_seen_at' not in existing_columns:
                print("Adding last_seen_at column...")
                conn.execute(text("ALTER TABLE job_offers ADD COLUMN last_seen_at DATETIME"))
                conn.commit()
            
            if 'status' not in existing_columns:
                print("Adding status column...")
                conn.execute(text("ALTER TABLE job_offers ADD COLUMN status VARCHAR(20) DEFAULT 'active'"))
                conn.commit()
        
        # Backfill data
        print("Backfilling existing records...")
        jobs = db.query(JobOffer).all()
        updated = 0
        
        for job in jobs:
            needs_update = False
            
            # Set status to active if null
            if job.status is None:
                job.status = 'active'
                needs_update = True
            
            # Set first_seen_at from created_at if null
            if job.first_seen_at is None:
                job.first_seen_at = job.created_at
                needs_update = True
            
            # Set last_seen_at from scraped_at if null
            if job.last_seen_at is None:
                job.last_seen_at = job.scraped_at
                needs_update = True
            
            # Try to infer source_id from source_url
            if job.source_id is None:
                source_id = infer_source_id(job.source_url)
                if source_id:
                    job.source_id = source_id
                    needs_update = True
            
            if needs_update:
                updated += 1
        
        db.commit()
        print(f"✅ Migration complete! Updated {updated} records.")
        
        # Create indexes
        print("Creating indexes...")
        with engine.connect() as conn:
            try:
                conn.execute(text("CREATE INDEX IF NOT EXISTS ix_job_offers_source_id ON job_offers(source_id)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS ix_job_offers_last_seen_at ON job_offers(last_seen_at)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS ix_job_offers_status ON job_offers(status)"))
                conn.commit()
                print("✅ Indexes created.")
            except Exception as e:
                print(f"⚠️  Index creation note: {e}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


def infer_source_id(source_url: str) -> str:
    """Try to infer source_id from source_url pattern."""
    if not source_url:
        return None
    
    # Check for known patterns
    if 'oipip.gda.pl' in source_url:
        return 'oipip_gdansk'
    elif 'szpitalepomorskie.eu' in source_url:
        return 'szpitalepomorskie'
    elif 'copernicus.gda.pl' in source_url:
        return 'copernicus'
    elif 'uck.pl' in source_url or 'uck.traffit.com' in source_url:
        return 'uck'
    elif 'luxmed.pl' in source_url:
        return 'lux_med_szpital_gdask'
    
    return None


if __name__ == '__main__':
    init_db()
    migrate()

