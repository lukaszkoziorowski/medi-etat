"""
Job offers API endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models import JobOffer, MedicalRole

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.get("/")
async def list_jobs(
    role: Optional[MedicalRole] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """
    List job offers with optional role filter.
    
    Args:
        role: Filter by medical role (optional)
        limit: Maximum number of results (default: 100)
        offset: Pagination offset (default: 0)
        db: Database session
    """
    query = db.query(JobOffer).filter(JobOffer.status == 'active')
    
    if role:
        query = query.filter(JobOffer.role == role)
    
    total = query.count()
    jobs = query.order_by(JobOffer.created_at.desc()).limit(limit).offset(offset).all()
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "results": [
            {
                "id": job.id,
                "title": job.title,
                "facility_name": job.facility_name,
                "city": job.city,
                "role": job.role.value,
                "description": job.description,
                "summary": job.summary,
                "source_url": job.source_url,
                "created_at": job.created_at.isoformat(),
            }
            for job in jobs
        ],
    }


@router.get("/{job_id}")
async def get_job(job_id: int, db: Session = Depends(get_db)):
    """
    Get a single job offer by ID.
    
    Args:
        job_id: Job offer ID
        db: Database session
    """
    job = db.query(JobOffer).filter(JobOffer.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job offer not found")
    
    return {
        "id": job.id,
        "title": job.title,
        "facility_name": job.facility_name,
        "city": job.city,
        "role": job.role.value,
        "description": job.description,
        "summary": job.summary,
        "source_url": job.source_url,
        "scraped_at": job.scraped_at.isoformat(),
        "created_at": job.created_at.isoformat(),
    }

