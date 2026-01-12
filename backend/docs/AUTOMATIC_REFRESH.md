# Automatic Job Offer Refresh System

## Overview

The system automatically refreshes job offers from all configured sources on a daily schedule without any manual intervention.

## Schedule

- **Frequency**: Once every 24 hours
- **Time**: 2:00 AM Polish time (Europe/Warsaw timezone)
- **Timezone**: Europe/Warsaw (CET/CEST)

## How It Works

1. **Scheduler Startup**: When the FastAPI application starts, the background scheduler is automatically initialized
2. **Daily Execution**: At 2:00 AM Polish time, the scheduler triggers `refresh_all_sources()`
3. **Source Processing**: Each configured source is scraped sequentially
4. **Data Updates**:
   - Existing offers are updated if content has changed
   - New offers are added to the database
   - Offers no longer present on source websites are marked as `inactive`
5. **Error Handling**: If one source fails, processing continues with other sources

## Features

### Automatic Operation
- No manual intervention required
- Runs in the background
- UI remains unaware of refresh timing

### Resilient Design
- Continues processing other sources if one fails
- Logs all errors for monitoring
- Prevents overlapping refresh runs

### Data Consistency
- Updates existing offers only when content changes
- Summary generation only triggers if underlying content changed
- Avoids creating duplicates
- Historical offers marked inactive (not deleted)

## Monitoring

### Check Scheduler Status

```bash
GET /api/admin/scheduler/status
```

Response:
```json
{
  "running": true,
  "next_run": "2024-01-15T02:00:00+01:00",
  "timezone": "Europe/Warsaw",
  "schedule": "Daily at 2:00 AM (Polish time)"
}
```

### Logs

The scheduler logs all refresh operations:
- Start and completion times
- Number of sources processed
- New, updated, and inactivated offers
- Any errors encountered

## Manual Refresh

Manual refresh is still available via the admin API:

```bash
POST /api/admin/refresh
```

This is useful for:
- Testing refresh functionality
- Immediate updates outside scheduled time
- Troubleshooting

## Configuration

The scheduler is configured in `app/services/scheduler.py`:

- **Schedule**: Cron expression for daily at 2:00 AM
- **Timezone**: Europe/Warsaw
- **Max Instances**: 1 (prevents overlapping runs)

## Future Extensions

The system is designed to be easily extended:

- **More Frequent Updates**: Change cron schedule in `scheduler.py`
- **Per-Source Scheduling**: Add individual schedules for different sources
- **Monitoring & Alerts**: Integrate with monitoring systems via logs
- **Scalability**: Can be moved to external task queue (Celery, RQ) if needed

## Technical Details

### Dependencies
- `apscheduler==3.10.4`: Background job scheduling
- `pytz==2023.3`: Timezone handling

### Architecture
- **Scheduler Service** (`app/services/scheduler.py`): Manages background scheduling
- **Refresh Service** (`app/services/refresh.py`): Handles actual refresh logic
- **FastAPI Integration**: Scheduler starts/stops with application lifecycle

### Lifecycle
1. Application starts → Scheduler initializes
2. Daily at 2 AM → Refresh job executes
3. Application shuts down → Scheduler stops gracefully
