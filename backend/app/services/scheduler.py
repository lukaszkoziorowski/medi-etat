"""
Automatic job offer refresh scheduler.

This module handles scheduled automatic refreshes of job offers.
Refreshes run daily at 2 AM Polish time (Europe/Warsaw timezone).
"""
import logging
from datetime import datetime
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from app.services.refresh import refresh_all_sources

logger = logging.getLogger(__name__)

# Polish timezone
POLISH_TZ = pytz.timezone('Europe/Warsaw')

# Global scheduler instance
_scheduler: Optional[BackgroundScheduler] = None


def run_refresh_job():
    """
    Execute the scheduled refresh job.
    
    This function is called by the scheduler and handles the refresh
    process with proper error handling and logging.
    """
    logger.info("Starting scheduled job offer refresh...")
    start_time = datetime.now(POLISH_TZ)
    
    try:
        result = refresh_all_sources()
        
        end_time = datetime.now(POLISH_TZ)
        duration = (end_time - start_time).total_seconds()
        
        logger.info(
            f"Refresh completed in {duration:.2f}s. "
            f"Status: {result.status}, "
            f"Sources: {result.sources_processed} processed, {result.sources_failed} failed, "
            f"New: {result.new_offers}, Updated: {result.updated_offers}, "
            f"Inactivated: {result.inactivated_offers}"
        )
        
        if result.errors:
            for error in result.errors:
                logger.warning(f"Refresh error for {error.get('source', 'unknown')}: {error.get('message', 'Unknown error')}")
        
    except Exception as e:
        logger.error(f"Fatal error during scheduled refresh: {str(e)}", exc_info=True)


def start_scheduler():
    """
    Start the background scheduler for automatic job offer refreshes.
    
    The scheduler runs refresh_all_sources() daily at 2 AM Polish time.
    This function should be called during application startup.
    """
    global _scheduler
    
    if _scheduler is not None:
        logger.warning("Scheduler is already running")
        return
    
    logger.info("Starting automatic refresh scheduler...")
    
    # Create background scheduler
    _scheduler = BackgroundScheduler(timezone=POLISH_TZ)
    
    # Schedule refresh job: daily at 2:00 AM Polish time
    _scheduler.add_job(
        func=run_refresh_job,
        trigger=CronTrigger(hour=2, minute=0, timezone=POLISH_TZ),
        id='daily_refresh',
        name='Daily Job Offer Refresh',
        replace_existing=True,
        max_instances=1,  # Prevent overlapping runs
    )
    
    # Start the scheduler
    _scheduler.start()
    
    # Log next run time
    next_run = _scheduler.get_job('daily_refresh').next_run_time
    if next_run:
        logger.info(f"Scheduler started. Next refresh scheduled for: {next_run.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    else:
        logger.warning("Scheduler started but next run time is not available")


def stop_scheduler():
    """
    Stop the background scheduler.
    
    This function should be called during application shutdown.
    """
    global _scheduler
    
    if _scheduler is None:
        return
    
    logger.info("Stopping automatic refresh scheduler...")
    _scheduler.shutdown(wait=True)
    _scheduler = None
    logger.info("Scheduler stopped")


def get_scheduler() -> Optional[BackgroundScheduler]:
    """
    Get the current scheduler instance.
    
    Returns:
        The scheduler instance or None if not started
    """
    return _scheduler


def is_scheduler_running() -> bool:
    """
    Check if the scheduler is currently running.
    
    Returns:
        True if scheduler is running, False otherwise
    """
    return _scheduler is not None and _scheduler.running
