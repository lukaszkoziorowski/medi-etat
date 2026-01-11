"""
Job offer refresh service.
"""
from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import JobOffer
from app.scrapers.registry import get_scraper, list_scrapers
from app.scrapers.playwright_helper import PlaywrightHelper


class RefreshResult:
    """Result of a refresh operation."""
    
    def __init__(self):
        self.status = 'success'  # 'success', 'partial', 'failed'
        self.sources_processed = 0
        self.sources_failed = 0
        self.new_offers = 0
        self.updated_offers = 0
        self.inactivated_offers = 0
        self.errors: List[Dict[str, str]] = []
        self.source_results: Dict[str, Dict] = {}
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for API response."""
        return {
            'status': self.status,
            'sources_processed': self.sources_processed,
            'sources_failed': self.sources_failed,
            'new_offers': self.new_offers,
            'updated_offers': self.updated_offers,
            'inactivated_offers': self.inactivated_offers,
            'errors': self.errors,
            'source_results': self.source_results,
        }


def refresh_all_sources() -> RefreshResult:
    """
    Refresh job offers from all configured sources.
    
    Returns:
        RefreshResult with summary of the operation
    """
    result = RefreshResult()
    refresh_start_time = datetime.utcnow()
    
    # Get all available scrapers
    scraper_names = list_scrapers()
    
    if not scraper_names:
        result.status = 'failed'
        result.errors.append({'source': 'system', 'message': 'No scrapers configured'})
        return result
    
    db = SessionLocal()
    
    try:
        # Process each source
        for source_id in scraper_names:
            try:
                source_result = refresh_source(source_id, db, refresh_start_time)
                result.sources_processed += 1
                result.new_offers += source_result['new']
                result.updated_offers += source_result['updated']
                result.inactivated_offers += source_result['inactivated']
                result.source_results[source_id] = source_result
                
                if source_result.get('error'):
                    result.sources_failed += 1
                    result.errors.append({
                        'source': source_id,
                        'message': source_result['error']
                    })
            except Exception as e:
                result.sources_failed += 1
                result.sources_processed += 1
                error_msg = str(e)
                result.errors.append({
                    'source': source_id,
                    'message': error_msg
                })
                result.source_results[source_id] = {
                    'error': error_msg,
                    'new': 0,
                    'updated': 0,
                    'inactivated': 0
                }
        
        # Determine overall status
        if result.sources_failed == 0:
            result.status = 'success'
        elif result.sources_failed < result.sources_processed:
            result.status = 'partial'
        else:
            result.status = 'failed'
    
    finally:
        db.close()
        PlaywrightHelper.close_browser()
    
    return result


def refresh_source(source_id: str, db: Session, refresh_start_time: datetime) -> Dict:
    """
    Refresh job offers from a single source.
    
    Args:
        source_id: Source identifier
        db: Database session
        refresh_start_time: When the refresh started (for marking stale offers)
        
    Returns:
        Dictionary with results: {'new': int, 'updated': int, 'inactivated': int, 'error': str (optional)}
    """
    result = {
        'new': 0,
        'updated': 0,
        'inactivated': 0,
    }
    
    try:
        # Get scraper instance
        scraper = get_scraper(source_id)
        
        # Scrape current offers
        current_jobs = scraper.scrape()
        
        if not current_jobs:
            # No jobs found - don't mark existing as inactive (might be temporary)
            return result
        
        # Deduplicate: Remove jobs with same base URL (without hash anchors)
        # This prevents duplicates from sources that create hash-based URLs
        import re
        base_url_seen = set()
        deduplicated_jobs = []
        for job in current_jobs:
            base_url = re.sub(r'#.*$', '', job['source_url'])
            if base_url not in base_url_seen:
                base_url_seen.add(base_url)
                deduplicated_jobs.append(job)
        
        current_jobs = deduplicated_jobs
        
        # Clean up existing duplicates for this source before saving new ones
        # Find all active jobs from this source
        existing_jobs = db.query(JobOffer).filter(
            JobOffer.source_id == source_id,
            JobOffer.status == 'active'
        ).all()
        
        # Group by base URL and remove duplicates
        base_url_groups = {}
        for job in existing_jobs:
            base_url = re.sub(r'#.*$', '', job.source_url)
            if base_url not in base_url_groups:
                base_url_groups[base_url] = [job]
            else:
                base_url_groups[base_url].append(job)
        
        # Delete duplicates (keep the oldest one)
        duplicates_deleted = 0
        for base_url, jobs in base_url_groups.items():
            if len(jobs) > 1:
                # Sort by ID to keep the oldest
                jobs_sorted = sorted(jobs, key=lambda j: j.id)
                keep_job = jobs_sorted[0]
                delete_jobs = jobs_sorted[1:]
                
                for job in delete_jobs:
                    db.delete(job)
                    duplicates_deleted += 1
        
        if duplicates_deleted > 0:
            db.commit()
        
        # Save or update offers
        save_result = scraper.save_or_update_to_db(current_jobs, db, update_existing=True)
        result['new'] = save_result['new']
        result['updated'] = save_result['updated']
        
        # Mark stale offers as inactive
        # Get all source_urls from current scrape
        current_urls = {job['source_url'] for job in current_jobs}
        
        # Find offers from this source that weren't seen in current scrape
        # Also include offers with null source_id that match this source's URL pattern
        from sqlalchemy import or_
        
        # Build query for offers from this source
        source_query = db.query(JobOffer).filter(
            JobOffer.last_seen_at < refresh_start_time,
            JobOffer.status == 'active'
        )
        
        # Filter by source_id if set, or by URL pattern if source_id is null
        if source_id:
            source_query = source_query.filter(
                or_(
                    JobOffer.source_id == source_id,
                    JobOffer.source_id.is_(None)  # Also check offers without source_id
                )
            )
        
        stale_offers = source_query.all()
        
        inactivated_count = 0
        scraper = get_scraper(source_id)  # Get scraper once for URL pattern matching
        
        for offer in stale_offers:
            # Only mark inactive if:
            # 1. Not in current scrape
            # 2. Belongs to this source (by source_id or URL pattern)
            if offer.source_url not in current_urls:
                # Check if this offer belongs to this source
                belongs_to_source = False
                
                if offer.source_id == source_id:
                    belongs_to_source = True
                elif offer.source_id is None:
                    # Try to match by URL pattern
                    if scraper.base_url in offer.source_url:
                        belongs_to_source = True
                
                if belongs_to_source:
                    offer.status = 'inactive'
                    inactivated_count += 1
        
        result['inactivated'] = inactivated_count
        db.commit()
        
    except Exception as e:
        db.rollback()
        result['error'] = str(e)
        raise
    
    return result

