"""
Admin API endpoints (internal use).
"""
import asyncio
import logging
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.refresh import refresh_all_sources
# Note: APScheduler removed - using Koyeb cron jobs instead

router = APIRouter(prefix="/api/admin", tags=["admin"])
logger = logging.getLogger(__name__)


def run_refresh_background():
    """Run refresh in background thread."""
    try:
        logger.info("Starting background refresh...")
        result = refresh_all_sources()
        logger.info(
            f"Background refresh completed: {result.status}, "
            f"{result.sources_processed} sources, "
            f"{result.new_offers} new, {result.updated_offers} updated"
        )
    except Exception as e:
        logger.error(f"Background refresh failed: {str(e)}", exc_info=True)


@router.post("/refresh")
async def refresh_jobs(background_tasks: BackgroundTasks):
    """
    Trigger a manual refresh of all job offers.
    
    This endpoint:
    - Returns immediately (for cron services with short timeouts)
    - Runs scraping in background
    - Re-scrapes all configured sources
    - Updates existing offers
    - Adds new offers
    - Marks missing offers as inactive
    
    Returns:
        Immediate response indicating refresh started
    """
    # Run refresh in background to avoid timeout issues
    background_tasks.add_task(run_refresh_background)
    
    return {
        "status": "started",
        "message": "Refresh job started in background. Check logs for progress.",
        "note": "This endpoint returns immediately to avoid timeout issues with cron services."
    }


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

