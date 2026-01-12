"""
Admin API endpoints (internal use).
"""
from fastapi import APIRouter, HTTPException
from app.services.refresh import refresh_all_sources
from app.services.scheduler import get_scheduler, is_scheduler_running

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


@router.get("/scheduler/status")
async def get_scheduler_status():
    """
    Get the status of the automatic refresh scheduler.
    
    Returns:
        Dictionary with scheduler status and next run time
    """
    scheduler = get_scheduler()
    
    if not scheduler or not is_scheduler_running():
        return {
            "running": False,
            "next_run": None,
            "message": "Scheduler is not running"
        }
    
    job = scheduler.get_job('daily_refresh')
    next_run = job.next_run_time if job else None
    
    return {
        "running": True,
        "next_run": next_run.isoformat() if next_run else None,
        "timezone": "Europe/Warsaw",
        "schedule": "Daily at 2:00 AM (Polish time)"
    }

