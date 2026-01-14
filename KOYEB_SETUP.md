# Koyeb Deployment Setup Guide

This guide walks you through deploying the Medietat backend to Koyeb.

## Prerequisites

- GitHub account (free)
- Koyeb account (free tier: https://koyeb.com)
- Supabase account (already set up)
- Vercel account (already set up for frontend)

## Step 1: Create Koyeb Account

1. Go to https://koyeb.com
2. Click "Sign Up" (free tier)
3. Sign up with GitHub (recommended for easy integration)
4. Authorize Koyeb to access your repositories

## Step 2: Create New App

1. In Koyeb dashboard, click **"Create App"**
2. Select **"GitHub"** as source
3. Choose your `medi-etat` repository
4. Select the `main` branch
5. Click **"Next"**

## Step 3: Configure Service

### 3.1 Basic Settings

- **Name**: `medi-etat-api` (or your preferred name)
- **Type**: **Web Service** (for API)
- **Region**: Choose closest to your users (e.g., `fra` for Frankfurt)

### 3.2 Build Configuration

**Build Command:**
```bash
cd backend && pip install --no-cache-dir -r requirements-koyeb.txt && playwright install chromium --with-deps
```

**Run Command:**
```bash
cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Note**: Koyeb may auto-detect Python. If it does, verify these commands are correct.

### 3.3 Root Directory

- **Root Directory**: `backend`
  - This tells Koyeb to build from the `backend` directory
  - Important: Set this in the service settings

### 3.4 Environment Variables

Go to **"Environment Variables"** section and add:

```
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
FRONTEND_URL=https://medi-etat.vercel.app
PORT=8000
PYTHONUNBUFFERED=1
```

**Important**:
- Replace `[YOUR-PASSWORD]` with your Supabase database password
- Replace `[PROJECT-REF]` with your Supabase project reference (e.g., `bcwbndguvzwegaaqvlzq`)
- Use Supabase **Session Pooler** connection string (port 5432) for best compatibility

### 3.5 Cron Job Configuration

**Add Cron Job:**
1. In service settings, find **"Cron Jobs"** or **"Scheduled Tasks"** section
2. Click **"Add Cron Job"**
3. Configure:
   - **Schedule**: `0 1 * * *` (1 AM UTC = 2 AM Polish time, 3 AM during DST)
   - **Command**: `cd backend && python -m app.services.refresh_cli`
   - **Timezone**: UTC (default)

**Alternative**: If Koyeb doesn't support cron in dashboard, you may need to:
- Use Koyeb CLI to add cron
- Or use external cron service (EasyCron, cron-job.org) to call `/api/admin/refresh`

### 3.6 Resource Limits (Free Tier)

- **Memory**: 512 MB (default, sufficient for most cases)
- **CPU**: Shared (default)
- **Disk**: 1 GB (default, sufficient)

**Note**: If you encounter memory issues, you may need to:
- Optimize Playwright usage (close browser after each scrape)
- Split to 2 services (API + worker)

## Step 4: Deploy

1. Click **"Deploy"** or **"Create App"**
2. Koyeb will:
   - Clone your repository
   - Build the application
   - Install dependencies (including Playwright)
   - Start the service
3. Wait for deployment to complete (5-10 minutes for first build)
4. Note your Koyeb URL (e.g., `https://medi-etat-api-[your-org].koyeb.app`)

## Step 5: Verify Deployment

### 5.1 Check Health

Visit: `https://your-app.koyeb.app/health`

Should return: `{"status": "healthy"}`

### 5.2 Test API

Visit: `https://your-app.koyeb.app/api/jobs`

Should return job listings (may be empty initially)

### 5.3 Check Logs

1. Go to service dashboard
2. Click **"Logs"** tab
3. Verify:
   - No startup errors
   - Database connection successful
   - API is listening on correct port

### 5.4 Test Manual Refresh

```bash
curl -X POST https://your-app.koyeb.app/api/admin/refresh
```

Should trigger a refresh and return results.

## Step 6: Configure Cron Job

### Option A: Koyeb Built-in Cron (If Available)

1. Go to service settings
2. Find **"Cron Jobs"** section
3. Add cron job:
   - **Schedule**: `0 1 * * *`
   - **Command**: `cd backend && python -m app.services.refresh_cli`
   - **Working Directory**: `/app/backend` (verify in Koyeb docs)

### Option B: External Cron Service (If Koyeb Doesn't Support Cron)

1. Sign up for free cron service:
   - **EasyCron**: https://www.easycron.com (free tier: 1 job)
   - **cron-job.org**: https://cron-job.org (free tier: 1 job)

2. Configure cron job:
   - **URL**: `https://your-app.koyeb.app/api/admin/refresh`
   - **Method**: POST
   - **Schedule**: Daily at 1 AM UTC
   - **Headers**: None required (or add auth if needed)

### Option C: GitHub Actions (Fallback)

Keep the existing GitHub Actions workflow as backup:
- Runs daily at 2 AM UTC
- Calls Koyeb API endpoint
- Provides redundancy

## Step 7: Update Frontend (Vercel)

1. Go to Vercel dashboard
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Update `NEXT_PUBLIC_API_URL`:
   - Old: Railway URL
   - New: `https://your-app.koyeb.app`
5. Redeploy frontend (or wait for auto-deploy)

## Step 8: Monitor & Validate

### 8.1 Check Cron Execution

1. Wait for scheduled time (1 AM UTC)
2. Check Koyeb logs for:
   - `Starting scheduled job offer refresh (CLI)...`
   - `Refresh completed...`
   - Any errors

### 8.2 Verify Data Updates

1. Check database for new/updated offers
2. Verify timestamps match cron schedule
3. Confirm no duplicate scrapes

### 8.3 Monitor Resources

1. Check service metrics:
   - Memory usage (should be < 512 MB)
   - CPU usage
   - Request count
2. Watch for:
   - Memory spikes during scraping
   - Build failures
   - Timeout errors

## Troubleshooting

### Build Fails / Timeout

**Problem**: Playwright installation takes too long

**Solutions**:
1. Optimize build command:
   ```bash
   pip install --no-cache-dir -r requirements-koyeb.txt && \
   playwright install chromium --with-deps
   ```
2. Use lazy Playwright installation (install browsers on first use)
3. Consider Docker image with pre-installed Playwright

### Memory Issues

**Problem**: Service exceeds 512 MB RAM

**Solutions**:
1. Monitor memory usage during scrapes
2. Ensure Playwright browser is closed after each scrape
3. Split to 2 services (API + worker)

### Cron Not Executing

**Problem**: Cron job doesn't run

**Solutions**:
1. Verify cron configuration in Koyeb dashboard
2. Check logs for cron execution
3. Use external cron service as backup
4. Keep GitHub Actions workflow as fallback

### Database Connection Issues

**Problem**: Cannot connect to Supabase

**Solutions**:
1. Verify `DATABASE_URL` is correct
2. Use Session Pooler (port 5432) not Transaction Pooler
3. Check Supabase connection settings
4. Verify network access (Koyeb should support both IPv4/IPv6)

## Migration Checklist

- [ ] Koyeb account created
- [ ] Service created and configured
- [ ] Environment variables set
- [ ] Build command configured
- [ ] Run command configured
- [ ] Root directory set to `backend`
- [ ] Cron job configured (or external cron set up)
- [ ] Service deployed successfully
- [ ] Health check passes
- [ ] API endpoints work
- [ ] Manual refresh works
- [ ] Cron job executes (wait for scheduled time)
- [ ] Frontend updated with new API URL
- [ ] Monitoring set up
- [ ] Railway service decommissioned (after validation period)

## Rollback Plan

If issues occur:

1. **Keep Railway running** during migration
2. **Test Koyeb in parallel** for 1-2 weeks
3. **Switch traffic gradually**:
   - Update Vercel to point to Koyeb
   - Keep Railway as backup
4. **Monitor both services** for comparison
5. **Decommission Railway** only after full validation

## Support & Resources

- **Koyeb Docs**: https://www.koyeb.com/docs
- **Koyeb Status**: https://status.koyeb.com
- **Koyeb Community**: https://www.koyeb.com/community

## Next Steps

After successful deployment:

1. Monitor for 1-2 weeks
2. Optimize based on metrics
3. Set up error tracking (Sentry, etc.)
4. Document any Koyeb-specific quirks
5. Plan for scaling if needed
