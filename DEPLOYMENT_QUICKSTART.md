# Quick Start Deployment Guide (100% Free Forever)

## 🚀 Deploy in 20 Minutes - Completely Free Forever!

### Prerequisites
- GitHub account
- PythonAnywhere account: https://www.pythonanywhere.com (free signup, **permanently free tier**)
- Supabase account: https://supabase.com (free signup, **permanently free tier**)
- Vercel account: https://vercel.com (free signup, **permanently free tier**)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Create Database (Supabase - Free Forever)

1. **Sign up at Supabase:**
   - Go to https://supabase.com
   - Click "Start your project" (free tier)
   - Sign up with GitHub

2. **Create New Project:**
   - Click "New Project"
   - **Name**: `medi-etat`
   - **Database Password**: (save this securely!)
   - **Region**: Choose closest to you
   - **Plan**: Free (default)
   - Click "Create new project"
   - Wait 2-3 minutes for setup

3. **Get Database URL:**
   - Go to Project Settings → Database
   - Find "Connection string" → "URI"
   - Copy the connection string (looks like: `postgresql://postgres:[password]@[host]:5432/postgres`)
   - **Save this URL** - you'll need it in Step 3

### Step 3: Deploy Backend (PythonAnywhere - Free Forever)

1. **Sign up at PythonAnywhere:**
   - Go to https://www.pythonanywhere.com
   - Click "Beginner" → "Create a Beginner account" (free)
   - Sign up with email or GitHub

2. **Open Bash Console:**
   - After login, click "Bash" tab
   - You'll see a terminal
   - **Tip**: To paste commands, right-click in the terminal and select "Paste", or use `Cmd+V` (Mac) / `Ctrl+V` (Windows/Linux)

3. **Clone Your Repository:**
   ```bash
   cd ~
   git clone https://github.com/lukaszkoziorowski/medi-etat.git
   cd medi-etat/backend
   ```

4. **Create Virtual Environment:**
   ```bash
   python3.9 -m venv venv
   source venv/bin/activate
   ```

5. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note**: Don't use `--user` flag when inside a virtual environment. The venv isolates packages automatically.

6. **Set Environment Variables:**
   - Go to "Files" tab
   - Navigate to `/home/yourusername/medi-etat/backend`
   - Click "New file" and name it `.env`
   - **In the file editor**, paste these two lines (replace placeholders with your actual values):
     ```
     DATABASE_URL=postgresql://postgres:[password]@[host]:5432/postgres
     FRONTEND_URL=https://your-app.vercel.app
     ```
   - Replace `[password]` with your Supabase database password
   - Replace `[host]` with your Supabase host (e.g., `db.xxxxx.supabase.co`)
   - Click "Save"
   - (We'll update FRONTEND_URL after deploying frontend)

7. **Create Web App:**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python 3.9
   - Click "Next" → "Next"

8. **Configure Web App:**
   - **Source code**: `/home/yourusername/medi-etat/backend`
   - **Working directory**: `/home/yourusername/medi-etat/backend`
   - **Virtualenv**: `/home/yourusername/medi-etat/backend/venv`
     - Enter this path in the "Virtualenv" field
     - **VERIFY this path is correct** - it should point to your venv directory
   - Click "WSGI configuration file" link
   - Replace contents with:
     ```python
     import sys
     import os
     
     project_home = '/home/yourusername/medi-etat/backend'
     if project_home not in sys.path:
         sys.path.insert(0, project_home)
     
     # Load environment variables from .env file
     from dotenv import load_dotenv
     load_dotenv(os.path.join(project_home, '.env'))
     
     # Import the FastAPI app
     from app.main import app
     
     # Convert ASGI (FastAPI) to WSGI for PythonAnywhere
     from app.wsgi_adapter import ASGI2WSGI
     
     # PythonAnywhere expects a WSGI application
     application = ASGI2WSGI(app)
     ```
   - **Important**: Replace `yourusername` with your actual PythonAnywhere username
   - Save the file

9. **Install Required Packages:**
   - Go to "Bash" tab
   - Run these commands:
   ```bash
   cd ~/medi-etat/backend
   source venv/bin/activate
   # Verify you're in the venv (should see (venv) in prompt)
   which python
   # Should show: /home/yourusername/medi-etat/backend/venv/bin/python
   
   # Install all packages
   pip install -r requirements.txt
   
   # Verify the adapter module exists
   python -c "from app.wsgi_adapter import ASGI2WSGI; print('SUCCESS: WSGI adapter available')"
   ```
   
   **Important**: Make sure you see `(venv)` in your prompt before running pip commands!

10. **Update requirements.txt:**
    - Add `python-dotenv` to `requirements.txt` if not already there

11. **Reload Web App:**
    - Go back to "Web" tab
    - Click green "Reload" button
    - Wait for reload

12. **Get Backend URL:**
    - Your URL will be: `https://yourusername.pythonanywhere.com`
    - **Save this URL**

13. **Initialize Database:**
   - Go to "Bash" tab
   ```bash
   cd ~/medi-etat/backend
   source venv/bin/activate
   python -c "from app.database import init_db; init_db()"
   ```
   - **No output is normal** - if there's no error, the database was initialized successfully
   - To verify, you can test the backend URL (next step)

### Step 4: Deploy Frontend (Vercel - Free Forever)

1. **Deploy:**
   - Go to https://vercel.com/dashboard
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Settings:
     - **Root Directory**: `frontend`
     - **Framework**: Next.js (auto-detected)
   - Environment Variable:
     - `NEXT_PUBLIC_API_URL` = `https://yourusername.pythonanywhere.com`
   - Click "Deploy"
   - **Copy the frontend URL** (e.g., `https://medi-etat.vercel.app`)

2. **Update Backend CORS:**
   - Go back to PythonAnywhere
   - "Files" tab → Edit `.env` file
   - Update `FRONTEND_URL` to your Vercel URL
   - "Web" tab → Click "Reload"

### Step 5: Test
Visit your Vercel URL - the app should be live! 🎉

## 📝 Updating After Changes

**Backend:**
```bash
# In PythonAnywhere Bash:
cd ~/medi-etat
git pull origin main
cd backend
source venv/bin/activate
pip install -r requirements.txt
# Then reload web app in "Web" tab
```

**Frontend:**
```bash
git push origin main  # Auto-deploys on Vercel
```

## 💰 Free Tier Limits (All Permanently Free!)

### PythonAnywhere Free Tier
- ✅ 1 web app
- ✅ 512MB disk space
- ✅ Limited CPU time (enough for testing)
- ✅ **No credit card required**
- ✅ **No expiration**
- ⚠️ Web app sleeps after 3 months of inactivity (just reload to wake)

### Supabase Free Tier
- ✅ 500MB database storage
- ✅ 2GB bandwidth/month
- ✅ Unlimited API requests
- ✅ **No credit card required**
- ✅ **No expiration**

### Vercel Free Tier
- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Automatic HTTPS
- ✅ **No credit card required**
- ✅ **No expiration**

## ⚠️ Important Notes

- **Web App Sleep**: PythonAnywhere free tier apps sleep after 3 months of inactivity. Just click "Reload" in Web tab to wake it up.
- **Playwright**: May not work on PythonAnywhere free tier. Consider using BeautifulSoup-only scrapers.
- **Database Size**: Supabase free tier has 500MB limit (plenty for testing).
- **CPU Limits**: PythonAnywhere free tier has CPU time limits, but sufficient for testing.

## 🆘 Troubleshooting

**Backend not responding?**
- Check if web app is running: PythonAnywhere → "Web" tab → Check status
- Click "Reload" if needed
- Check error logs: "Web" tab → "Error log" link

**Frontend can't connect?**
- Verify `NEXT_PUBLIC_API_URL` in Vercel environment variables
- Check `.env` file in PythonAnywhere has correct `FRONTEND_URL`
- Check CORS settings in backend code

**Database issues?**
- Verify `DATABASE_URL` in PythonAnywhere `.env` file
- Check Supabase dashboard → Database → Connection pooling
- Ensure database is initialized (Step 3.13)

**Import errors?**
- Make sure all dependencies are installed: `pip install -r requirements.txt` (inside activated venv)
- Check Python version matches (3.9)
- Verify virtual environment is activated (you should see `(venv)` in prompt)

## 📚 Full Documentation

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions.
