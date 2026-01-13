# Free-Forever Deployment Stack Recommendation

## Executive Summary

After evaluating multiple options and considering your constraints (Playwright scrapers, scheduled tasks, free forever), here is the recommended stack:

**Recommended Stack:**
- **Backend API**: **Railway** (Free tier: $5/month credit, 500 hours)
- **Scrapers/Scheduled Tasks**: **GitHub Actions** (Free for public repos, unlimited for private)
- **Database**: **Supabase** (Free forever: 500MB, 2GB bandwidth/month)
- **Frontend**: **Vercel** (Free forever: unlimited deployments)
- **Alternative Backend**: **Koyeb** (Free tier: 2 services, always-on)

## Detailed Analysis

### Current Issues with PythonAnywhere

1. **PostgreSQL Blocked**: Free tier blocks outbound connections to ports 5432/6543
2. **Playwright Limitations**: May not support headless browser automation well
3. **Resource Constraints**: Limited CPU/memory for scraping operations
4. **Scheduling Limitations**: Basic cron support but not ideal for complex tasks

### Recommended Solution: Hybrid Architecture

#### Option A: Railway + GitHub Actions (Recommended)

**Architecture:**
```
┌─────────────────┐
│  GitHub Repo    │
│  (Code Source)  │
└────────┬────────┘
         │
    ┌────┴────┬──────────────────┐
    │         │                  │
    ▼         ▼                  ▼
┌─────────┐ ┌──────────────┐ ┌──────────┐
│ Railway │ │ GitHub       │ │ Supabase  │
│ (API)   │ │ Actions      │ │ (Database)│
│         │ │ (Scrapers)   │ │           │
└────┬────┘ └──────┬───────┘ └─────┬──────┘
     │             │               │
     └─────────────┴───────────────┘
              │
         ┌────▼────┐
         │ Vercel │
         │(Frontend)│
         └─────────┘
```

**Components:**

1. **Railway** (Backend API)
   - ✅ Free tier: $5/month credit (500 hours)
   - ✅ Supports PostgreSQL connections
   - ✅ Can run Playwright (with proper setup)
   - ✅ Auto-deploy from GitHub
   - ✅ Environment variables support
   - ✅ Persistent storage available
   - ⚠️ Credit expires if not used (but resets monthly)
   - ⚠️ Sleeps after inactivity (but wakes on request)

2. **GitHub Actions** (Scheduled Scraping)
   - ✅ Free for public repos (unlimited)
   - ✅ Free for private repos (2000 minutes/month)
   - ✅ Cron scheduling (every 5 minutes minimum)
   - ✅ Can run Playwright in headless mode
   - ✅ Can trigger Railway API endpoints
   - ✅ Full control over execution environment
   - ✅ Free forever, no credit card needed

3. **Supabase** (Database)
   - ✅ Free forever: 500MB storage, 2GB bandwidth/month
   - ✅ PostgreSQL with REST API
   - ✅ Works with Railway (no port blocking)
   - ✅ Can use HTTP API if direct connection fails

4. **Vercel** (Frontend)
   - ✅ Free forever
   - ✅ Already working
   - ✅ Auto-deploy from GitHub

**Why This Works:**
- Railway handles the API (always available)
- GitHub Actions runs scrapers on schedule (no cost)
- Scrapers can either:
  - Run in GitHub Actions and POST results to Railway API
  - Or trigger Railway's `/api/admin/refresh` endpoint
- Supabase accessible from Railway (no port blocking)

**Deployment Flow:**
1. Push code to GitHub
2. Railway auto-deploys API
3. GitHub Actions runs scrapers on schedule
4. Scrapers update database via Railway API or direct Supabase connection

---

#### Option B: Koyeb (Alternative - Simpler)

**Architecture:**
```
┌──────────┐
│  Koyeb   │ (Backend API + Scrapers)
│          │
└────┬─────┘
     │
┌────▼────┐ ┌──────────┐
│ Supabase│ │  Vercel │
│(Database)│ │(Frontend)│
└─────────┘ └──────────┘
```

**Components:**

1. **Koyeb** (Backend + Scrapers)
   - ✅ Free tier: 2 services, always-on
   - ✅ Supports PostgreSQL
   - ✅ Can run Playwright
   - ✅ Auto-deploy from GitHub
   - ✅ Built-in cron support
   - ⚠️ 2 services limit (can run API + scheduler in one service)
   - ⚠️ Less known platform

**Why This Works:**
- Single platform for API and scrapers
- Always-on (no sleeping)
- Free forever with clear limits
- Simpler architecture

---

#### Option C: Keep PythonAnywhere + Use Supabase REST API

**Architecture:**
```
┌──────────────────┐
│ PythonAnywhere   │ (Backend API)
│                  │ (Uses Supabase REST API)
└────────┬─────────┘
         │
    ┌────┴────┐
    │        │
┌───▼───┐ ┌──▼────┐
│Supabase│ │Vercel│
│(REST)  │ │      │
└────────┘ └──────┘
```

**Components:**

1. **PythonAnywhere** (Backend API)
   - ✅ Free forever
   - ✅ Already set up
   - ⚠️ Use Supabase REST API instead of direct DB connection
   - ⚠️ Requires code changes (use HTTP instead of SQLAlchemy)

2. **GitHub Actions** (Scrapers)
   - ✅ Run scrapers on schedule
   - ✅ POST results to PythonAnywhere API or Supabase REST API

**Why This Works:**
- No migration needed (keep PythonAnywhere)
- Use Supabase REST API (HTTP, no port blocking)
- GitHub Actions handles scraping
- Minimal code changes

---

## Comparison Table

| Feature | Railway + GitHub Actions | Koyeb | PythonAnywhere + REST |
|---------|------------------------|-------|----------------------|
| **Cost** | Free ($5 credit/month) | Free (2 services) | Free forever |
| **PostgreSQL Support** | ✅ Yes | ✅ Yes | ⚠️ Via REST API |
| **Playwright Support** | ✅ Yes | ✅ Yes | ⚠️ Limited |
| **Scheduled Tasks** | ✅ GitHub Actions | ✅ Built-in cron | ⚠️ Basic cron |
| **Auto-deploy** | ✅ Yes | ✅ Yes | ⚠️ Manual |
| **Always-on** | ⚠️ Sleeps if idle | ✅ Yes | ✅ Yes |
| **Complexity** | Medium | Low | Low |
| **Migration Effort** | Medium | Medium | Low |

---

## Recommended Choice: Railway + GitHub Actions

### Why Railway + GitHub Actions?

1. **Best for Scrapers**: GitHub Actions provides reliable, free scheduled execution
2. **No Port Blocking**: Railway allows PostgreSQL connections
3. **Playwright Support**: Both platforms support headless browsers
4. **Separation of Concerns**: API always available, scrapers run on schedule
5. **Scalability**: Easy to upgrade Railway if needed
6. **Free Forever**: Both have permanent free tiers

### Implementation Steps

#### Step 1: Set Up Railway (Backend API)

1. **Sign up**: https://railway.app (GitHub login)
2. **Create Project**: "New Project" → "Deploy from GitHub repo"
3. **Select Repo**: Choose `medi-etat`
4. **Configure**:
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables**:
   ```
   DATABASE_URL=postgresql://postgres:[password]@[supabase-host]:5432/postgres
   FRONTEND_URL=https://medi-etat.vercel.app
   ```
6. **Deploy**: Railway auto-deploys on push

#### Step 2: Set Up GitHub Actions (Scrapers)

1. **Create Workflow**: `.github/workflows/scrape.yml`
   ```yaml
   name: Scrape Job Offers
   on:
     schedule:
       - cron: '0 2 * * *'  # Daily at 2 AM UTC (3 AM Polish time)
     workflow_dispatch:  # Manual trigger
   
   jobs:
     scrape:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-python@v4
           with:
             python-version: '3.9'
         - name: Install dependencies
           run: |
             cd backend
             pip install -r requirements.txt
             playwright install chromium
         - name: Run scrapers
           env:
             RAILWAY_API_URL: ${{ secrets.RAILWAY_API_URL }}
           run: |
             cd backend
             python -m app.services.refresh
             # Or trigger Railway API:
             # curl -X POST $RAILWAY_API_URL/api/admin/refresh
   ```

2. **Alternative**: Trigger Railway API endpoint
   ```yaml
   - name: Trigger refresh
     run: |
       curl -X POST ${{ secrets.RAILWAY_API_URL }}/api/admin/refresh
   ```

#### Step 3: Update Vercel Environment Variable

- Set `NEXT_PUBLIC_API_URL` to Railway URL: `https://your-app.railway.app`

---

## Migration Path (If You Outgrow Free Tier)

### Railway
- **Upgrade**: $5/month → $20/month (more resources)
- **Alternative**: Move to Koyeb, Render, or Fly.io

### GitHub Actions
- **Upgrade**: Private repos get 2000 min/month (usually enough)
- **Alternative**: Move scrapers to Railway cron or external cron service

### Supabase
- **Upgrade**: $25/month (8GB storage, 50GB bandwidth)
- **Alternative**: Self-hosted PostgreSQL, Neon, or PlanetScale

---

## Best Practices for Free Tier

### Railway
- Use environment variables for secrets
- Enable auto-deploy from GitHub
- Monitor credit usage (dashboard shows remaining)
- Use `railway logs` for debugging

### GitHub Actions
- Cache dependencies to save minutes
- Run scrapers in parallel if possible
- Use `workflow_dispatch` for manual triggers
- Set up notifications for failures

### Supabase
- Use connection pooling (Session Pooler)
- Monitor bandwidth usage
- Use indexes for performance
- Consider archiving old data

### General
- Keep code in GitHub (single source of truth)
- Use environment variables (never commit secrets)
- Test locally before deploying
- Monitor logs regularly

---

## Quick Start: Railway + GitHub Actions

### 1. Railway Setup (5 minutes)

```bash
# Install Railway CLI (optional)
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# Deploy
railway up
```

Or use Railway web dashboard (easier).

### 2. GitHub Actions Setup (10 minutes)

Create `.github/workflows/scrape.yml`:

```yaml
name: Daily Scrape

on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM UTC = 3 AM Polish time
  workflow_dispatch:

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          playwright install chromium
      - name: Trigger Railway refresh
        env:
          RAILWAY_API_URL: ${{ secrets.RAILWAY_API_URL }}
        run: |
          curl -X POST $RAILWAY_API_URL/api/admin/refresh
```

### 3. Update Environment Variables

**Railway:**
- `DATABASE_URL`: Supabase connection string
- `FRONTEND_URL`: Vercel URL

**GitHub Actions:**
- Add secret: `RAILWAY_API_URL` (your Railway API URL)

**Vercel:**
- `NEXT_PUBLIC_API_URL`: Railway API URL

---

## Conclusion

**Recommended Stack: Railway + GitHub Actions + Supabase + Vercel**

This combination provides:
- ✅ Free forever (with known limits)
- ✅ Reliable scheduled scraping
- ✅ No port blocking issues
- ✅ Playwright support
- ✅ Easy deployments
- ✅ Clear upgrade path

**Next Steps:**
1. Set up Railway account
2. Deploy backend to Railway
3. Set up GitHub Actions workflow
4. Update Vercel environment variable
5. Test end-to-end

Would you like me to help implement this stack?
