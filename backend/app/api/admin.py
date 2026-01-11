"""
Admin API endpoints (internal use).
"""
from fastapi import APIRouter, HTTPException
from app.services.refresh import refresh_all_sources

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/refresh")
async def refresh_jobs():
    """
    Trigger a manual refresh of all job offers.
    
    This endpoint:
    - Re-scrapes all configured sources
    - Updates existing offers
    - Adds new offers
    - Marks missing offers as inactive
    
    Returns:
        Refresh result with statistics
    """
    try:
        result = refresh_all_sources()
        return result.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Refresh failed: {str(e)}")

