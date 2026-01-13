# Railway + GitHub Actions Setup Guide

This guide will help you migrate from PythonAnywhere to Railway + GitHub Actions.

## Prerequisites

- GitHub account (free)
- Railway account (free tier: https://railway.app)
- Supabase account (already set up)
- Vercel account (already set up)

## Step 1: Set Up Railway Account

1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign up with GitHub (recommended)
4. Authorize Railway to access your repositories

## Step 2: Deploy Backend to Railway

### Option A: Using Railway Dashboard (Recommended)

1. **Create New Project:**
   - In Railway dashboard, click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `medi-etat` repository
   - Click "Deploy Now"

2. **Configure Service (CRITICAL - Do This First!):**
   - After Railway creates the service, go to **Settings** tab
   - Scroll down to **"Root Directory"** section
   - **IMPORTANT**: Set Root Directory to: `backend`
   - This tells Railway to build from the `backend/` folder, not the repo root
   - Without this, Railway will see both `backend/` and `frontend/` and fail to detect the language
   - Click **"Save"**
   
3. **Configure Build Settings (Important for Playwright):**
   - Go to your service → "Settings" tab
   - Scroll to "Build Command"
   - Add this build command:
     ```bash
     pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium
     ```
   - Or leave it empty and Railway will auto-detect (but Playwright might need manual install)

4. **Add Environment Variables:**
   - Go to your service → "Variables" tab
   - Add these variables:
     ```
     DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
     FRONTEND_URL=https://medi-etat.vercel.app
     PORT=8000  # Railway sets this automatically, but good to have
     ```
   - Replace `[YOUR-PASSWORD]` with your Supabase password
   - Replace `[PROJECT-REF]` with your Supabase project reference (e.g., `bcwbndguvzwegaaqvlzq`)

5. **Deploy:**
   - Railway will automatically build and deploy
   - Wait for deployment to complete (2-3 minutes)
   - Note your Railway URL (e.g., `https://medi-etat-production.up.railway.app`)

### Option B: Using Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to project
cd backend
railway link

# Set environment variables
railway variables set DATABASE_URL="postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres"
railway variables set FRONTEND_URL="https://medi-etat.vercel.app"

# Deploy
railway up
```

## Step 3: Test Railway Deployment

1. **Check Health:**
   - Visit: `https://your-app.railway.app/health`
   - Should return: `{"status":"healthy"}`

2. **Test API:**
   - Visit: `https://your-app.railway.app/api/jobs?limit=10`
   - Should return job offers (or empty array if database is empty)

3. **Check Logs:**
   - In Railway dashboard → "Deployments" → Click latest deployment → "View Logs"
   - Look for: "Starting Medietat API..." and "Database initialized"

## Step 4: Set Up GitHub Actions

1. **Add Railway URL Secret:**
   - Go to your GitHub repo → "Settings" → "Secrets and variables" → "Actions"
   - Click "New repository secret"
   - Name: `RAILWAY_API_URL`
   - Value: Your Railway URL (e.g., `https://medi-etat-production.up.railway.app`)
   - Click "Add secret"

2. **Verify Workflow File:**
   - The workflow file `.github/workflows/scrape.yml` is already created
   - It will run daily at 2 AM UTC (3 AM Polish time)
   - You can also trigger it manually from GitHub Actions tab

3. **Test Workflow:**
   - Go to GitHub repo → "Actions" tab
   - Click "Daily Job Scrape" workflow
   - Click "Run workflow" → "Run workflow" (manual trigger)
   - Watch it execute and check Railway logs

## Step 5: Update Vercel Environment Variable

1. **Go to Vercel Dashboard:**
   - Select your `medi-etat` project
   - Go to "Settings" → "Environment Variables"

2. **Update API URL:**
   - Find or create: `NEXT_PUBLIC_API_URL`
   - Update value to: `https://your-app.railway.app`
   - Select all environments (Production, Preview, Development)
   - Click "Save"

3. **Redeploy:**
   - Go to "Deployments" tab
   - Click "..." on latest deployment → "Redeploy"
   - Or push a small change to trigger redeploy

## Step 6: Verify End-to-End

1. **Test Frontend:**
   - Visit: `https://medi-etat.vercel.app`
   - Open browser console (F12)
   - Check for: `API Base URL: https://your-app.railway.app`
   - Jobs should load (or show empty state if database is empty)

2. **Trigger Manual Refresh:**
   - Visit: `https://your-app.railway.app/api/admin/refresh`
   - Or use curl:
     ```bash
     curl -X POST https://your-app.railway.app/api/admin/refresh
     ```
   - Check response for scraping results

3. **Check Scheduled Scraping:**
   - Go to GitHub → "Actions" tab
   - Wait for next scheduled run (or trigger manually)
   - Verify it calls Railway API successfully

## Step 7: Clean Up PythonAnywhere (Optional)

Once Railway is working:

1. **Export Data (if needed):**
   - If you have data in PythonAnywhere's SQLite, export it
   - Or let the scrapers repopulate from scratch

2. **Delete PythonAnywhere Web App:**
   - Go to PythonAnywhere → "Web" tab
   - Delete your web app (optional, you can keep it as backup)

## Troubleshooting

### Railway Deployment Fails

1. **Check Build Logs:**
   - Railway dashboard → "Deployments" → Click failed deployment → "View Logs"
   - Look for error messages

2. **Common Issues:**
   - **Missing dependencies**: Check `requirements.txt` includes all packages
   - **Playwright install**: Railway will install Playwright automatically (configured in `railway.json`)
   - **Port binding**: Railway sets `$PORT` automatically, our `Procfile` uses it

### GitHub Actions Fails

1. **Check Workflow Logs:**
   - GitHub → "Actions" → Click failed workflow → Check logs

2. **Common Issues:**
   - **Missing secret**: Ensure `RAILWAY_API_URL` is set in GitHub secrets
   - **Wrong URL**: Verify Railway URL is correct (no trailing slash)
   - **Timeout**: Workflow has 30-minute timeout, should be enough

### Database Connection Issues

1. **Check Environment Variables:**
   - Railway dashboard → "Variables" tab
   - Verify `DATABASE_URL` is correct
   - Use Supabase direct connection (not pooler, Railway allows it)

2. **Test Connection:**
   - Railway dashboard → "Deployments" → "View Logs"
   - Look for: "Database initialized" (success) or connection errors

### CORS Issues

1. **Check Frontend URL:**
   - Railway → "Variables" → Verify `FRONTEND_URL` matches Vercel URL
   - Update if needed and redeploy

2. **Test CORS:**
   - Open browser console on Vercel site
   - Check for CORS errors
   - Railway CORS middleware should handle it

## Monitoring

### Railway

- **Logs**: Dashboard → "Deployments" → "View Logs"
- **Metrics**: Dashboard → "Metrics" tab (CPU, memory, requests)
- **Usage**: Dashboard → "Usage" tab (check remaining credit)

### GitHub Actions

- **Workflow Runs**: GitHub → "Actions" tab
- **Scheduled Runs**: Check "Daily Job Scrape" workflow history
- **Manual Trigger**: "Run workflow" button

## Cost Monitoring

### Railway Free Tier

- **Credit**: $5/month (500 hours)
- **Usage**: Check dashboard → "Usage" tab
- **Estimate**: ~$0.01/hour for small apps
- **Warning**: Railway will notify if you approach limits

### GitHub Actions Free Tier

- **Public repos**: Unlimited minutes
- **Private repos**: 2000 minutes/month
- **Usage**: GitHub → "Settings" → "Billing" → "Actions"

## Next Steps

1. ✅ Railway deployed and working
2. ✅ GitHub Actions workflow running
3. ✅ Vercel connected to Railway
4. ✅ Scheduled scraping active

**You're all set!** Your app is now running on a free-forever stack.

## Support

- **Railway Docs**: https://docs.railway.app
- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Railway Discord**: https://discord.gg/railway
- **Railway Status**: https://status.railway.app
