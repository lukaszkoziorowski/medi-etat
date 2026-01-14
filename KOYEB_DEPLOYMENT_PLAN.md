# Koyeb Deployment Plan for Medietat

## Executive Summary

This document provides a comprehensive deployment plan for migrating the Medietat backend and scrapers from Railway to **Koyeb**. The plan addresses architecture, configuration, scheduling, and deployment workflows while maintaining a free-forever setup.

**Key Advantages of Koyeb:**
- ✅ Always-on free tier (no service sleeping)
- ✅ Built-in cron support (no APScheduler needed)
- ✅ 2 free services (can separate API and workers)
- ✅ Git-based auto-deployment
- ✅ Simpler configuration than Railway

---

## 1. Current Architecture Analysis

### 1.1 What We Have

**Backend Components:**
- FastAPI application (`app/main.py`)
- REST API endpoints (`/api/jobs`, `/api/admin`)
- APScheduler for scheduled scrapes (2 AM Polish time)
- Scraper registry system (hardcoded + config-based)
- Database layer (SQLAlchemy with Supabase PostgreSQL)
- Playwright support for JavaScript-rendered pages

**Current Issues from Railway:**
- APScheduler fails when service sleeps
- Dual scheduling (APScheduler + GitHub Actions)
- Complex build configuration (Nixpacks, multiple requirements files)
- Dependency resolution problems
- Service sleeping unpredictably

**Dependencies:**
- Python 3.9
- FastAPI, Uvicorn
- SQLAlchemy, psycopg2-binary
- BeautifulSoup4, lxml, requests
- Playwright (for some scrapers)
- APScheduler (currently used, can be removed)

### 1.2 Code Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app + lifespan (starts APScheduler)
│   ├── database.py          # DB connection (Supabase-compatible)
│   ├── models.py            # SQLAlchemy models
│   ├── api/                 # API endpoints
│   │   ├── jobs.py          # Public job search API
│   │   └── admin.py         # Admin endpoints (/api/admin/refresh)
│   ├── services/
│   │   ├── scheduler.py     # APScheduler wrapper
│   │   └── refresh.py      # Scraper orchestration
│   ├── scrapers/            # Scraper implementations
│   │   ├── base.py          # Base scraper class
│   │   ├── registry.py      # Scraper registry
│   │   ├── playwright_helper.py
│   │   └── configs/         # JSON config files
│   └── utils/
└── requirements-railway.txt # Locked dependencies
```

---

## 2. Koyeb-Specific Considerations

### 2.1 Koyeb Free Tier Limitations

**Known Limits:**
- **2 services** maximum (free tier)
- **Always-on** (no sleeping) ✅
- **512 MB RAM** per service (may be limiting for Playwright)
- **1 GB disk** per service
- **Build timeout**: ~10 minutes
- **Cron jobs**: Supported (built-in)
- **Git deployments**: Automatic from GitHub
- **Environment variables**: Supported
- **Logs**: Available (retention unclear)

**Potential Issues:**
- ⚠️ **Memory limits**: Playwright + multiple scrapers may exceed 512 MB
- ⚠️ **Disk space**: Playwright browsers (~300 MB) + dependencies
- ⚠️ **Build complexity**: Similar dependency issues possible
- ⚠️ **Cron reliability**: Need to verify cron execution guarantees

### 2.2 Compatibility Analysis

**✅ Compatible:**
- FastAPI/ASGI applications
- PostgreSQL connections (Supabase)
- Python 3.9
- Git-based deployment
- Environment variables
- Background workers

**⚠️ Needs Attention:**
- Playwright installation (large, may slow builds)
- APScheduler (should be replaced with Koyeb cron)
- Database connection pooling (Supabase compatibility)
- Memory usage (Playwright + scrapers)

**❌ Potential Problems:**
- Build timeouts if Playwright install is slow
- Memory exhaustion with multiple Playwright instances
- Cron job reliability (need to verify)

---

## 3. Proposed Architecture

### 3.1 Option A: Single Service (Recommended for Free Tier)

**Architecture:**
```
┌─────────────────────────────────┐
│      Koyeb Service 1            │
│  ┌───────────────────────────┐  │
│  │   FastAPI (API Server)    │  │
│  │   - /api/jobs             │  │
│  │   - /api/admin/refresh    │  │
│  │   - /health               │  │
│  └───────────────────────────┘  │
│  ┌───────────────────────────┐  │
│  │   Cron Job (Daily 2 AM)   │  │
│  │   - Runs refresh script   │  │
│  │   - Calls refresh service │  │
│  └───────────────────────────┘  │
└──────────────┬──────────────────┘
               │
        ┌──────┴──────┐
        │             │
   ┌────▼────┐  ┌────▼────┐
   │ Supabase│  │ Vercel  │
   │(Database)│  │(Frontend)│
   └─────────┘  └─────────┘
```

**Components:**
- **Web Service**: FastAPI API (always running)
- **Cron Job**: Daily scrape at 2 AM Polish time
- **Shared Codebase**: Same code, different entry points

**Pros:**
- ✅ Uses only 1 service (free tier allows 2)
- ✅ Simple architecture
- ✅ Always-on API
- ✅ Reliable cron execution

**Cons:**
- ⚠️ Scrapes run in same process (memory concerns)
- ⚠️ API may be slower during scraping

### 3.2 Option B: Two Services (If Memory Issues)

**Architecture:**
```
┌──────────────────┐  ┌──────────────────┐
│  Koyeb Service 1 │  │  Koyeb Service 2 │
│  ┌────────────┐  │  │  ┌────────────┐ │
│  │ FastAPI    │  │  │  │ Cron Job   │ │
│  │ (API Only) │  │  │  │ (Scrapers) │ │
│  └────────────┘  │  │  └────────────┘ │
└────────┬─────────┘  └────────┬─────────┘
         │                     │
         └──────────┬──────────┘
                    │
            ┌───────┴───────┐
            │               │
       ┌────▼────┐    ┌────▼────┐
       │ Supabase│    │ Vercel  │
       └─────────┘    └─────────┘
```

**Components:**
- **Service 1**: FastAPI API only
- **Service 2**: Cron job that runs scrapers (calls refresh service)

**Pros:**
- ✅ Separation of concerns
- ✅ API unaffected by scraping
- ✅ Can scale independently

**Cons:**
- ❌ Uses both free services (no room for expansion)
- ⚠️ More complex deployment
- ⚠️ Service 2 only runs during cron (wasted resources)

**Recommendation**: Start with **Option A** (single service), migrate to Option B if memory issues occur.

---

## 4. Deployment Strategy

### 4.1 Service Configuration

#### Service 1: API + Cron (Single Service Approach)

**Service Type**: Web Service + Cron Job

**Build Configuration:**
- **Build Command**: `cd backend && pip install -r requirements-koyeb.txt`
- **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Python Version**: 3.9

**Cron Configuration:**
- **Schedule**: `0 2 * * *` (2 AM UTC = 3 AM Polish time, 4 AM during DST)
- **Command**: `cd backend && python -m app.services.refresh refresh_all_sources`
- **OR**: HTTP trigger to `/api/admin/refresh` endpoint

**Environment Variables:**
```
DATABASE_URL=postgresql://postgres:[PASSWORD]@[SUPABASE_HOST]:5432/postgres
FRONTEND_URL=https://medi-etat.vercel.app
PORT=8000
PYTHONUNBUFFERED=1
```

### 4.2 Database Strategy

**Current Setup:**
- Supabase PostgreSQL (external)
- Connection string with pooler support
- IPv4/IPv6 compatibility logic in `database.py`

**Koyeb Considerations:**
- ✅ Koyeb supports both IPv4 and IPv6
- ✅ No port blocking (unlike PythonAnywhere)
- ✅ Can use direct Supabase connection or pooler
- ⚠️ Connection pooling still recommended

**Recommendation:**
- Use Supabase **Session Pooler** (port 5432)
- Keep existing `database.py` logic (works with Koyeb)
- Monitor connection pool usage

**Backup Strategy:**
- Supabase provides automatic backups (free tier)
- No additional backup needed
- Consider periodic exports if needed

### 4.3 Scraper Execution Strategy

**Current Approach:**
- APScheduler runs `refresh_all_sources()` at 2 AM
- Scrapers run sequentially
- Playwright browser shared across scrapers

**Koyeb Approach:**

**Option 1: Cron → Python Script** (Recommended)
```bash
# Cron job runs:
python -m app.services.refresh refresh_all_sources
```

**Option 2: Cron → HTTP Endpoint**
```bash
# Cron job calls:
curl -X POST http://localhost:$PORT/api/admin/refresh
```

**Option 3: Separate Worker Service** (If Option A has issues)
- Service 2 runs only during cron execution
- Calls refresh service via HTTP or direct import

**Recommendation**: **Option 1** (direct Python call)
- Simpler
- No HTTP overhead
- Better error handling
- Can reuse database connections

### 4.4 Playwright Handling

**Challenge:**
- Playwright requires browser binaries (~300 MB)
- Slow to install during build
- High memory usage during execution

**Solutions:**

**Option A: Install During Build** (Simplest)
- Add Playwright to requirements
- Install browsers in build command
- Risk: Slow builds, may timeout

**Option B: Lazy Installation** (Better)
- Install Playwright package only
- Install browsers on first use (cached)
- Risk: First scrape is slow

**Option C: Pre-built Docker Image** (Best, but complex)
- Custom Docker image with Playwright pre-installed
- Faster builds
- More complex setup

**Recommendation**: Start with **Option A**, optimize if needed.

**Build Command:**
```bash
cd backend && \
pip install -r requirements-koyeb.txt && \
playwright install chromium --with-deps
```

---

## 5. Code Changes Required

### 5.1 Remove APScheduler Dependency

**Files to Modify:**

1. **`app/main.py`**
   - Remove `start_scheduler()` and `stop_scheduler()` from lifespan
   - Keep API functionality
   - Remove scheduler import

2. **`app/services/scheduler.py`**
   - Keep file for now (admin endpoint uses it)
   - Or remove entirely if not needed

3. **`app/api/admin.py`**
   - Keep `/api/admin/refresh` endpoint
   - Remove or modify `/api/admin/scheduler/status` (no scheduler)

4. **`requirements-koyeb.txt`**
   - Remove `apscheduler==3.10.4`
   - Remove `pytz==2023.3` (if only used by scheduler)
   - Keep all other dependencies

### 5.2 Create Standalone Refresh Script

**New File: `app/services/refresh_cli.py`**
```python
"""
CLI entry point for running refresh from cron.
"""
import sys
from app.services.refresh import refresh_all_sources

if __name__ == "__main__":
    result = refresh_all_sources()
    if result.status == 'failed':
        sys.exit(1)
    sys.exit(0)
```

**Usage in Cron:**
```bash
python -m app.services.refresh_cli
```

### 5.3 Environment Variable Handling

**No Changes Needed:**
- Current code uses `os.getenv()` for all config
- `DATABASE_URL` already handled
- `FRONTEND_URL` already handled

**Consider Adding:**
- `LOG_LEVEL` (default: INFO)
- `SCRAPE_TIMEOUT` (default: 30 minutes)

### 5.4 Database Connection

**No Changes Needed:**
- `database.py` already handles Supabase
- IPv4/IPv6 logic works with Koyeb
- Connection pooling configured

**Potential Optimization:**
- Reduce pool size if memory constrained
- Add connection timeout handling

---

## 6. Build & Deployment Configuration

### 6.1 Requirements File

**Create: `backend/requirements-koyeb.txt`**
- Copy from `requirements-railway.txt`
- Remove `apscheduler` and `pytz` (if not needed)
- Keep Playwright (needed for some scrapers)
- Keep all other dependencies

### 6.2 Koyeb Configuration File

**Create: `koyeb.yaml`** (Optional, Koyeb can auto-detect)
```yaml
services:
  - name: medi-etat-api
    type: web
    build:
      type: buildpacks
      env:
        - name: PYTHON_VERSION
          value: "3.9"
    run:
      command: "cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
    cron:
      - schedule: "0 2 * * *"
        command: "cd backend && python -m app.services.refresh_cli"
    env:
      - name: DATABASE_URL
        value: "${DATABASE_URL}"
      - name: FRONTEND_URL
        value: "${FRONTEND_URL}"
```

**Note**: Koyeb may not support YAML config. Use dashboard instead.

### 6.3 Build Process

**Koyeb Auto-Detection:**
- Detects Python from `requirements.txt` or `runtime.txt`
- Uses buildpacks (similar to Heroku)
- Auto-installs dependencies

**Manual Build Command** (if needed):
```bash
cd backend && \
pip install --no-cache-dir -r requirements-koyeb.txt && \
playwright install chromium --with-deps
```

**Start Command:**
```bash
cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 6.4 Git Deployment Flow

**Automatic Deployment:**
1. Push to GitHub `main` branch
2. Koyeb detects changes
3. Triggers build automatically
4. Deploys new version
5. Zero-downtime deployment (if configured)

**Manual Deployment:**
- Koyeb dashboard → "Redeploy"
- Or use Koyeb CLI

**Branch Strategy:**
- `main` → Production (auto-deploy)
- `develop` → Staging (optional, uses 2nd service)

---

## 7. Cron Job Configuration

### 7.1 Schedule

**Current Schedule:**
- APScheduler: 2 AM Polish time (Europe/Warsaw)
- GitHub Actions: 2 AM UTC (3 AM Polish time)

**Koyeb Cron:**
- Use UTC timezone
- Schedule: `0 2 * * *` = 2 AM UTC = 3 AM Polish time (4 AM during DST)
- **OR**: `0 1 * * *` = 1 AM UTC = 2 AM Polish time (3 AM during DST)

**Recommendation**: `0 1 * * *` (1 AM UTC) to match 2 AM Polish time

### 7.2 Execution Method

**Option 1: Direct Python Call** (Recommended)
```bash
cd /app/backend && python -m app.services.refresh_cli
```

**Option 2: HTTP Call**
```bash
curl -X POST http://localhost:$PORT/api/admin/refresh
```

**Option 3: Shell Script**
```bash
#!/bin/bash
cd /app/backend
source venv/bin/activate  # If using venv
python -m app.services.refresh_cli
```

**Recommendation**: **Option 1** (simplest, most reliable)

### 7.3 Error Handling

**Cron Job Should:**
- Log output to Koyeb logs
- Exit with non-zero code on failure
- Send notifications (if Koyeb supports it)

**Implementation:**
```python
# app/services/refresh_cli.py
import sys
import logging
from app.services.refresh import refresh_all_sources

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    try:
        result = refresh_all_sources()
        if result.status == 'failed':
            logging.error(f"Refresh failed: {result.errors}")
            sys.exit(1)
        logging.info(f"Refresh completed: {result.to_dict()}")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
```

---

## 8. Environment Variables & Secrets

### 8.1 Required Variables

**Koyeb Dashboard → Service → Environment Variables:**

```
DATABASE_URL=postgresql://postgres:[PASSWORD]@[SUPABASE_HOST]:5432/postgres
FRONTEND_URL=https://medi-etat.vercel.app
PORT=8000
PYTHONUNBUFFERED=1
```

**Optional:**
```
LOG_LEVEL=INFO
SCRAPE_TIMEOUT=1800
PLAYWRIGHT_BROWSER_PATH=/usr/bin/chromium  # If pre-installed
```

### 8.2 Secrets Management

**Koyeb Approach:**
- Environment variables in dashboard (encrypted at rest)
- No separate secrets service (free tier)
- Can reference other services' variables

**Security:**
- ✅ Variables encrypted in Koyeb
- ✅ Not exposed in logs (by default)
- ⚠️ Visible in dashboard (team members)

**Best Practices:**
- Use strong database passwords
- Rotate secrets periodically
- Don't commit secrets to Git
- Use Koyeb's variable references if possible

---

## 9. Monitoring & Observability

### 9.1 Logs

**Koyeb Logs:**
- Available in dashboard
- Real-time streaming
- Retention: Unknown (likely limited on free tier)

**Logging Strategy:**
- Use Python `logging` module (already configured)
- Log to stdout (Koyeb captures automatically)
- Structured logging for better parsing

**Example:**
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 9.2 Health Checks

**Current Endpoints:**
- `/health` - Basic health check
- `/api/admin/scheduler/status` - Scheduler status (remove or modify)

**Add:**
- `/health/detailed` - Database connection, scraper count, etc.

### 9.3 Error Tracking

**Options:**
- **Sentry** (free tier): Error tracking and alerts
- **Logtail** (free tier): Log aggregation
- **Koyeb built-in**: Basic logs only

**Recommendation**: Add Sentry for production

---

## 10. Risks & Mitigations

### 10.1 Build Timeouts

**Risk**: Playwright installation may exceed build timeout

**Mitigation:**
- Optimize build command
- Use `--no-cache-dir` for pip
- Install Playwright browsers separately if needed
- Consider Docker image with pre-installed Playwright

### 10.2 Memory Limits

**Risk**: 512 MB RAM may be insufficient for Playwright + scrapers

**Mitigation:**
- Monitor memory usage
- Close Playwright browser after each scrape
- Run scrapers sequentially (not parallel)
- Consider splitting to 2 services if needed

### 10.3 Cron Reliability

**Risk**: Cron jobs may not execute reliably

**Mitigation:**
- Verify cron execution in logs
- Add manual trigger endpoint
- Consider external cron service as backup
- Monitor scrape success/failure rates

### 10.4 Database Connection Issues

**Risk**: Connection pool exhaustion or timeouts

**Mitigation:**
- Use connection pooling (already configured)
- Monitor connection usage
- Add retry logic
- Use Supabase Session Pooler

### 10.5 Service Limits

**Risk**: Free tier limits may be exceeded

**Mitigation:**
- Monitor resource usage
- Optimize code and dependencies
- Plan upgrade path if needed
- Consider alternative if limits too restrictive

---

## 11. Migration Steps

### 11.1 Pre-Migration Checklist

- [ ] Review and understand Koyeb free tier limits
- [ ] Test Playwright installation locally
- [ ] Verify database connection from local machine
- [ ] Prepare requirements file without APScheduler
- [ ] Create refresh CLI script
- [ ] Document current Railway setup (for rollback)

### 11.2 Code Preparation (No Deployment Yet)

1. **Create `requirements-koyeb.txt`**
   - Remove APScheduler
   - Keep all other dependencies
   - Include Playwright

2. **Create `app/services/refresh_cli.py`**
   - Standalone script for cron execution
   - Proper error handling and exit codes

3. **Modify `app/main.py`**
   - Remove APScheduler startup/shutdown
   - Keep API functionality

4. **Update `app/api/admin.py`**
   - Modify or remove scheduler status endpoint

5. **Test Locally**
   - Verify API still works
   - Test refresh script manually
   - Check Playwright installation

### 11.3 Koyeb Setup

1. **Create Koyeb Account**
   - Sign up at koyeb.com
   - Connect GitHub account

2. **Create Service**
   - New App → GitHub
   - Select repository
   - Configure build/run commands

3. **Set Environment Variables**
   - Add DATABASE_URL
   - Add FRONTEND_URL
   - Add other required vars

4. **Configure Cron Job**
   - Add cron schedule
   - Set command to run refresh script

5. **Deploy**
   - Push to GitHub (triggers auto-deploy)
   - Or manually deploy from dashboard

### 11.4 Testing & Validation

1. **API Testing**
   - Verify `/health` endpoint
   - Test `/api/jobs` endpoint
   - Check CORS configuration

2. **Cron Testing**
   - Manually trigger cron job
   - Verify scrapes execute
   - Check logs for errors

3. **Integration Testing**
   - Verify frontend can connect
   - Test full scrape cycle
   - Monitor resource usage

### 11.5 Rollback Plan

**If Issues Occur:**
1. Keep Railway deployment running
2. Test Koyeb in parallel
3. Switch DNS/Vercel config only after validation
4. Keep Railway as backup for 1-2 weeks

---

## 12. Assumptions & Trade-offs

### 12.1 Assumptions

1. **Koyeb Free Tier:**
   - Always-on (no sleeping) ✅
   - 2 services available ✅
   - Cron jobs work reliably ⚠️ (needs verification)
   - 512 MB RAM sufficient ⚠️ (needs testing)
   - Build timeout sufficient ⚠️ (needs testing)

2. **Playwright:**
   - Can install during build ✅
   - Works in Koyeb environment ✅
   - Memory usage acceptable ⚠️ (needs monitoring)

3. **Database:**
   - Supabase connection works ✅
   - No port blocking ✅
   - Connection pooling sufficient ✅

4. **Cron Jobs:**
   - Execute reliably ✅ (assumed)
   - Have access to same environment ✅
   - Can run Python scripts ✅

### 12.2 Trade-offs

**Simplified Architecture:**
- ✅ Removed APScheduler complexity
- ✅ Single service (simpler)
- ⚠️ Less flexibility than separate workers

**Free Tier Limitations:**
- ✅ Always-on (better than Railway)
- ⚠️ Memory constraints may limit scalability
- ⚠️ 2 services limit (can't expand easily)

**Cron vs APScheduler:**
- ✅ More reliable (platform-managed)
- ✅ Simpler code (no scheduler logic)
- ⚠️ Less flexible (can't change schedule easily)
- ⚠️ Platform-dependent (harder to migrate)

**Playwright in Build:**
- ✅ Simpler deployment
- ⚠️ Slower builds
- ⚠️ Larger image size

---

## 13. Success Criteria

### 13.1 Functional Requirements

- [ ] API responds to requests
- [ ] Cron job executes daily at correct time
- [ ] Scrapers run successfully
- [ ] Data saved to database
- [ ] Frontend can connect to API
- [ ] Health checks pass

### 13.2 Performance Requirements

- [ ] API response time < 500ms (p95)
- [ ] Scrape completes in < 30 minutes
- [ ] Memory usage < 512 MB (during normal operation)
- [ ] Build completes in < 10 minutes

### 13.3 Reliability Requirements

- [ ] Cron job executes 99%+ of scheduled times
- [ ] API uptime > 99%
- [ ] Scrapes succeed > 95% of the time
- [ ] Database connections stable

---

## 14. Next Steps (After Approval)

1. **Create code changes** (remove APScheduler, add CLI script)
2. **Create Koyeb configuration files**
3. **Set up Koyeb service** (dashboard configuration)
4. **Test deployment** (staging/test environment)
5. **Validate functionality** (API + cron)
6. **Monitor and optimize** (memory, performance)
7. **Switch production traffic** (update Vercel config)
8. **Decommission Railway** (after validation period)

---

## 15. Questions & Unknowns

**Need to Verify:**
1. Koyeb cron job execution guarantees
2. Cron job log visibility and retention
3. Memory usage with Playwright + multiple scrapers
4. Build timeout limits (exact value)
5. Disk space limits and usage
6. Network restrictions (if any)
7. IPv6 support for Supabase connections

**Recommendation**: Create test service first to verify these before full migration.

---

## Conclusion

This plan provides a **clean, realistic deployment strategy** for Koyeb that:
- ✅ Removes APScheduler complexity
- ✅ Uses Koyeb's built-in cron
- ✅ Maintains free-forever setup
- ✅ Simplifies architecture
- ✅ Addresses Railway's limitations

**Key Decision Points:**
1. **Single vs Two Services**: Start with single, migrate if needed
2. **Cron Execution**: Direct Python call vs HTTP endpoint
3. **Playwright Installation**: Build-time vs lazy installation

**Ready for Implementation**: After approval, we'll proceed with code changes and configuration.
