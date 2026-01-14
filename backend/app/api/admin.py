"""
Admin API endpoints (internal use).
"""
from fastapi import APIRouter, HTTPException
from app.services.refresh import refresh_all_sources
# Note: APScheduler removed - using Koyeb cron jobs instead

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
    Get the status of scheduled refreshes.
    
    Note: Scheduled refreshes are handled by Koyeb cron jobs,
    not by an in-process scheduler. This endpoint provides
    information about the cron schedule.
    
    Returns:
        Dictionary with cron schedule information
    """
    return {
        "scheduler_type": "koyeb_cron",
        "running": True,  # Cron is always "running" (managed by Koyeb)
        "next_run": None,  # Cannot determine next run time from API
        "timezone": "UTC",
        "schedule": "Daily at 1:00 AM UTC (2:00 AM Polish time, 3:00 AM during DST)",
        "cron_expression": "0 1 * * *",
        "message": "Scheduled refreshes are handled by Koyeb cron jobs. Use /api/admin/refresh for manual refresh."
    }

