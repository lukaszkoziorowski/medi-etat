"""
CLI entry point for running refresh from cron jobs.

This script is designed to be called by Koyeb cron jobs or other
scheduled task systems. It runs the refresh process and exits with
appropriate exit codes for monitoring.
"""
import sys
import logging
from app.services.refresh import refresh_all_sources

# Configure logging for CLI usage
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for refresh CLI."""
    logger.info("Starting scheduled job offer refresh (CLI)...")
    
    try:
        result = refresh_all_sources()
        
        # Log summary
        logger.info(
            f"Refresh completed. "
            f"Status: {result.status}, "
            f"Sources: {result.sources_processed} processed, {result.sources_failed} failed, "
            f"New: {result.new_offers}, Updated: {result.updated_offers}, "
            f"Inactivated: {result.inactivated_offers}"
        )
        
        # Log errors if any
        if result.errors:
            for error in result.errors:
                logger.warning(
                    f"Refresh error for {error.get('source', 'unknown')}: "
                    f"{error.get('message', 'Unknown error')}"
                )
        
        # Exit with appropriate code
        if result.status == 'failed':
            logger.error("Refresh failed - exiting with error code")
            sys.exit(1)
        elif result.status == 'partial':
            logger.warning("Refresh partially succeeded - some sources failed")
            sys.exit(0)  # Partial success is still success
        else:
            logger.info("Refresh completed successfully")
            sys.exit(0)
            
    except Exception as e:
        logger.error(f"Fatal error during refresh: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
