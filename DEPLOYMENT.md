# Free Deployment Guide for Medietat (100% Free Forever)

This guide will help you deploy the Medietat project to **permanently free** hosting services for testing and collaboration.

## Deployment Stack (All Free Forever!)

- **Backend**: PythonAnywhere (Free Tier - **No expiration**)
- **Frontend**: Vercel (Free Tier - **No expiration**)
- **Database**: Supabase PostgreSQL (Free Tier - **No expiration**)

## Why This Stack?

- ✅ **PythonAnywhere**: Truly free forever, no credit card required, 1 web app, 512MB disk
- ✅ **Supabase**: Free PostgreSQL forever, 500MB storage, 2GB bandwidth/month
- ✅ **Vercel**: Free forever for Next.js, unlimited deployments, 100GB bandwidth/month

## Prerequisites

1. GitHub account (free)
2. PythonAnywhere account (free) - [Sign up here](https://www.pythonanywhere.com) - **No credit card required**
3. Supabase account (free) - [Sign up here](https://supabase.com) - **No credit card required**
4. Vercel account (free) - [Sign up here](https://vercel.com) - **No credit card required**

## Step 1: Prepare Your Repository

Make sure your code is pushed to GitHub:

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

## Step 2: Create PostgreSQL Database on Supabase

### 2.1 Sign Up and Create Project

1. Go to [Supabase](https://supabase.com)
2. Click "Start your project" (free tier)
3. Sign up with GitHub (easiest)
4. Click "New Project"
5. Configure:
   - **Name**: `medi-etat`
   - **Database Password**: Create a strong password (save it!)
   - **Region**: Choose closest to you
   - **Plan**: Free (default)
6. Click "Create new project"
7. Wait 2-3 minutes for database setup

### 2.2 Get Database Connection String

1. In Supabase Dashboard, go to **Project Settings** → **Database**
2. Scroll to "Connection string" section
3. Select "URI" tab
4. Copy the connection string (looks like: `postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres`)
5. **Save this URL** - you'll need it for backend deployment

## Step 3: Deploy Backend to PythonAnywhere

### 3.1 Sign Up for PythonAnywhere

1. Go to [PythonAnywhere](https://www.pythonanywhere.com)
2. Click "Beginner" → "Create a Beginner account"
3. Sign up with email or GitHub
4. Verify your email if required
5. Log in to your account

### 3.2 Clone Your Repository

1. In PythonAnywhere dashboard, click **"Bash"** tab
2. You'll see a terminal console
3. **Tip**: To paste commands, right-click in the terminal and select "Paste", or use `Cmd+V` (Mac) / `Ctrl+V` (Windows/Linux)
4. Clone your repository:
   ```bash
   cd ~
   git clone https://github.com/yourusername/medi-etat.git
   cd medi-etat/backend
   ```
   Replace `yourusername` with your GitHub username

### 3.3 Set Up Virtual Environment

```bash
python3.9 -m venv venv
source venv/bin/activate
```

### 3.4 Install Dependencies

```bash
pip install -r requirements.txt
```

**Important**: Don't use `--user` flag when inside a virtual environment. The venv isolates packages automatically. Using `--user` inside a venv will cause an error.

### 3.5 Create Environment File

1. Click **"Files"** tab in PythonAnywhere
2. Navigate to `/home/yourusername/medi-etat/backend`
3. Click **"New file"**
4. Name it `.env`
5. **In the file editor**, paste these two lines (plain text, no backticks):
   ```
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@[HOST]:5432/postgres
   FRONTEND_URL=https://placeholder.vercel.app
   ```
   - Replace `[YOUR-PASSWORD]` with your Supabase database password
   - Replace `[HOST]` with your Supabase host (e.g., `db.xxxxx.supabase.co`)
   - Or use the full connection string from Step 2.2
   - We'll update `FRONTEND_URL` after deploying frontend
6. Click **"Save"**

### 3.6 Create Web App

1. Click **"Web"** tab
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Select **Python 3.9**
5. Click **"Next"** → **"Next"**

### 3.7 Configure Web App

1. Set **Source code**: `/home/yourusername/medi-etat/backend`
   - Replace `yourusername` with your PythonAnywhere username
2. Set **Working directory**: `/home/yourusername/medi-etat/backend`
3. Set **Virtualenv**: `/home/yourusername/medi-etat/backend/venv`
   - Enter this path in the "Virtualenv" field
   - Replace `yourusername` with your PythonAnywhere username
4. Click **"WSGI configuration file"** link (near the top)
4. Replace the entire file content with:
   ```python
   import sys
   import os
   
   # Add project directory to path
   project_home = '/home/yourusername/medi-etat/backend'
   if project_home not in sys.path:
       sys.path.insert(0, project_home)
   
   # Load environment variables from .env file
   from dotenv import load_dotenv
   load_dotenv(os.path.join(project_home, '.env'))
   
   # Import FastAPI app
   from app.main import app
   
   # Convert ASGI (FastAPI) to WSGI for PythonAnywhere
   from app.wsgi_adapter import ASGI2WSGI
   
   # PythonAnywhere expects WSGI application
   application = ASGI2WSGI(app)
   ```
   
   **Important**: Replace `yourusername` with your actual PythonAnywhere username
5. **Important**: Replace `yourusername` with your actual PythonAnywhere username
6. Click **"Save"** (or scroll down and click the green "Reload" button)

### 3.8 Install Required Packages

Go back to **"Bash"** tab:
```bash
cd ~/medi-etat/backend
source venv/bin/activate
pip install -r requirements.txt
```

This will install all dependencies including:
- `python-dotenv` (for loading .env file)
- `uvicorn` (ASGI server for FastAPI)
- All other required packages

**Note**: The WSGI adapter is included in the codebase (`app/wsgi_adapter.py`), so no additional package is needed.

**Note**: Make sure your virtual environment is activated (you should see `(venv)` in your prompt).

**Important**: If you see errors about missing packages, make sure you're in the activated virtual environment and run `pip install -r requirements.txt` again.

### 3.9 Reload Web App

1. Go to **"Web"** tab
2. Click the green **"Reload"** button
3. Wait for reload (30-60 seconds)

### 3.10 Get Backend URL

Your backend URL will be: `https://yourusername.pythonanywhere.com`

**Save this URL** - you'll need it for frontend deployment.

### 3.11 Initialize Database

1. Go to **"Bash"** tab
2. Run:
   ```bash
   cd ~/medi-etat/backend
   source venv/bin/activate
   python -c "from app.database import init_db; init_db()"
   ```

**Note**: The function doesn't print a success message - if there's no error, it worked! The tables were created silently. You can verify by testing the backend (next step).

### 3.12 Test Backend

Visit: `https://yourusername.pythonanywhere.com/health`

You should see: `{"status":"healthy"}`

## Step 4: Deploy Frontend to Vercel

### 4.1 Deploy via Vercel Dashboard

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure the project:
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `.next` (auto-detected)
5. Add Environment Variable:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: Your PythonAnywhere backend URL from Step 3.10 (e.g., `https://yourusername.pythonanywhere.com`)
6. Click "Deploy"
7. Wait for deployment (1-2 minutes)
8. **Copy the frontend URL** (e.g., `https://medi-etat.vercel.app`)

### 4.2 Update Backend CORS Settings

1. Go back to PythonAnywhere
2. Click **"Files"** tab
3. Navigate to `/home/yourusername/medi-etat/backend`
4. Edit `.env` file
5. Update `FRONTEND_URL` to your Vercel frontend URL:
   ```
   FRONTEND_URL=https://medi-etat.vercel.app
   ```
6. Save the file
7. Go to **"Web"** tab
8. Click **"Reload"** button

## Step 5: Test Your Deployment

1. Visit your Vercel frontend URL
2. The app should load and connect to your PythonAnywhere backend
3. Test the job listings and filters

## Updating Your Deployment

### Backend Updates

1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```
3. In PythonAnywhere:
   - Go to **"Bash"** tab
   - Run:
     ```bash
     cd ~/medi-etat
     git pull origin main
     cd backend
     source venv/bin/activate
     pip install -r requirements.txt
     ```
   - Go to **"Web"** tab
   - Click **"Reload"**

### Frontend Updates

1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```
3. Vercel will automatically detect changes and redeploy

## Troubleshooting

### Backend Not Responding

- **Web App Sleep**: PythonAnywhere free tier apps sleep after 3 months of inactivity. Click "Reload" in Web tab to wake it up.
- **Check Status**: PythonAnywhere → "Web" tab → Check if web app is running
- **Check Logs**: PythonAnywhere → "Web" tab → "Error log" link
- **Check Health**: Visit `https://yourusername.pythonanywhere.com/health`

### Frontend Can't Connect to Backend

- Verify `NEXT_PUBLIC_API_URL` is set correctly in Vercel
- Check `.env` file in PythonAnywhere has correct `FRONTEND_URL`
- Check CORS settings in backend code
- Verify backend is running: Visit backend URL directly

### Database Issues

- Verify `DATABASE_URL` in PythonAnywhere `.env` file
- Check Supabase dashboard → Database → Connection pooling
- Ensure database schema is initialized (Step 3.11)
- Test connection in Supabase dashboard → SQL Editor

### Import Errors

- Make sure all dependencies are installed: `pip install -r requirements.txt` (inside activated venv)
- Check Python version matches (3.9)
- Verify virtual environment is activated (you should see `(venv)` in prompt)
- Check error logs in PythonAnywhere Web tab

### Playwright Issues

- Playwright may not work on PythonAnywhere free tier (limited system dependencies)
- Scrapers using Playwright might need to be disabled or use alternative methods
- Consider using BeautifulSoup-only scrapers for deployment
- Check error logs for specific Playwright errors

### Web App Reload Issues

- Wait 30-60 seconds after clicking Reload
- Check error log for specific errors
- Verify WSGI configuration file is correct
- Ensure all environment variables are set

## Free Tier Limitations

### PythonAnywhere Free Tier (Permanently Free!)
- ✅ 1 web app
- ✅ 512MB disk space
- ✅ Limited CPU time (sufficient for testing)
- ✅ **No credit card required**
- ✅ **No expiration date**
- ⚠️ Web app sleeps after 3 months of inactivity (just reload to wake)

### Supabase Free Tier (Permanently Free!)
- ✅ 500MB database storage
- ✅ 2GB bandwidth/month
- ✅ Unlimited API requests
- ✅ **No credit card required**
- ✅ **No expiration date**

### Vercel Free Tier (Permanently Free!)
- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ **No credit card required**
- ✅ **No expiration date**

## Next Steps (When Ready for Production)

When you're ready to move beyond free tier:

1. **Upgrade PythonAnywhere**: Paid plans remove CPU limits, more disk space, always-on apps
2. **Upgrade Supabase**: More storage, bandwidth, and features
3. **Monitoring**: Add error tracking (Sentry free tier)
4. **CI/CD**: Already handled by Vercel auto-deploy

## Support

- PythonAnywhere Docs: https://help.pythonanywhere.com
- Supabase Docs: https://supabase.com/docs
- Vercel Docs: https://vercel.com/docs
- Project Issues: Check GitHub issues

## Quick Reference

```bash
# Backend updates (in PythonAnywhere Bash)
cd ~/medi-etat
git pull origin main
cd backend
source venv/bin/activate
pip install -r requirements.txt
# Then reload in Web tab

# Frontend
git push origin main  # Auto-deploys on Vercel
```
