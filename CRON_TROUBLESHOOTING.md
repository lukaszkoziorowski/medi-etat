# Cron Job Troubleshooting Guide

## Quick Diagnostic Steps

### 1. Check What Error You're Getting

**In cron-job.org:**
- Go to Dashboard → Your cron job → "Executions" tab
- Click on the failed execution
- Check:
  - **Status Code** (should be 200)
  - **Response Body** (should show JSON with scrape results)
  - **Error Message** (if any)

**Common Status Codes:**
- `200` = Success ✅
- `404` = URL not found ❌
- `500` = Server error ❌
- `Timeout` = Request took too long ❌
- `Connection refused` = Can't reach server ❌

### 2. Verify the URL is Correct

Your Koyeb URL should be:
```
https://contemporary-tera-limerik-490a0aa8.koyeb.app/api/admin/refresh
```

**Check:**
- No trailing slash
- `/api/admin/refresh` (not `/api/admin/refresh/`)
- `https://` (not `http://`)
- Correct domain

### 3. Test Manually First

Before fixing the cron job, test the endpoint manually:

```bash
curl -X POST https://contemporary-tera-limerik-490a0aa8.koyeb.app/api/admin/refresh
```

**Expected Response:**
```json
{
  "status": "success",
  "sources_processed": 10,
  "sources_failed": 0,
  "new_offers": 5,
  "updated_offers": 3,
  ...
}
```

**If this works:** The endpoint is fine, the issue is with cron service configuration
**If this fails:** The endpoint has an issue, check Koyeb logs

### 4. Check Koyeb Logs

1. Go to Koyeb dashboard → Your service → Logs
2. Look for:
   - Incoming POST requests to `/api/admin/refresh`
   - Any error messages
   - Scrape activity

**If you see the request but it fails:**
- Check for Python errors
- Check for database connection issues
- Check for scraper errors

**If you don't see the request:**
- The cron service isn't reaching Koyeb
- Check URL, firewall, or network issues

## Common Issues and Fixes

### Issue 1: 404 Not Found

**Symptoms:**
- Status code: 404
- Error: "Not Found"

**Causes:**
- Wrong URL
- Missing `/api/admin/refresh` path
- Trailing slash issue

**Fix:**
- Verify URL: `https://contemporary-tera-limerik-490a0aa8.koyeb.app/api/admin/refresh`
- Remove any trailing slashes
- Test with curl first

### Issue 2: 405 Method Not Allowed

**Symptoms:**
- Status code: 405
- Error: "Method Not Allowed"

**Causes:**
- Using GET instead of POST
- Wrong HTTP method

**Fix:**
- In cron-job.org: Set **Request Method** to **POST**
- In EasyCron: Set **HTTP Method** to **POST**

### Issue 3: 500 Internal Server Error

**Symptoms:**
- Status code: 500
- Error: "Internal Server Error"

**Causes:**
- Scraper error
- Database connection issue
- Python exception

**Fix:**
1. Check Koyeb logs for detailed error
2. Test manually with curl to see error message
3. Common issues:
   - Database connection timeout
   - Scraper timeout
   - Missing Playwright browsers
   - Memory issues

### Issue 4: Timeout

**Symptoms:**
- Status: Timeout
- Error: "Request timeout" or "Connection timeout"

**Causes:**
- Scraping takes too long (> 30 seconds)
- Network issues
- Cron service timeout too short

**Fix:**
1. **Increase timeout in cron service:**
   - cron-job.org: Settings → Timeout (set to 300 seconds / 5 minutes)
   - EasyCron: Increase timeout in settings

2. **Optimize scraping:**
   - Some scrapers might be slow
   - Check Koyeb logs to see which scraper is slow

3. **Test manually:**
   ```bash
   curl -X POST --max-time 300 https://your-app.koyeb.app/api/admin/refresh
   ```

### Issue 5: Connection Refused / Can't Reach Server

**Symptoms:**
- Status: Connection refused
- Error: "Could not connect"

**Causes:**
- Koyeb service is down
- Wrong URL/domain
- Network/firewall blocking

**Fix:**
1. Check Koyeb service status:
   - Visit: `https://contemporary-tera-limerik-490a0aa8.koyeb.app/health`
   - Should return: `{"status": "healthy"}`

2. Verify service is running:
   - Koyeb dashboard → Service status should be "Running"

3. Check URL is correct

### Issue 6: CORS Error (Less Likely)

**Symptoms:**
- Status: CORS error
- Error: "CORS policy" or "Access-Control-Allow-Origin"

**Causes:**
- Cron service making preflight OPTIONS request
- CORS middleware blocking

**Fix:**
- Usually not an issue (server-to-server)
- If it happens, check CORS settings in `backend/app/main.py`

## Step-by-Step Debugging

### Step 1: Test Endpoint Manually

```bash
curl -v -X POST https://contemporary-tera-limerik-490a0aa8.koyeb.app/api/admin/refresh
```

**Check:**
- Does it return 200?
- Does it return JSON?
- How long does it take?

### Step 2: Check Cron Service Configuration

**cron-job.org:**
- URL: `https://contemporary-tera-limerik-490a0aa8.koyeb.app/api/admin/refresh`
- Method: **POST** (not GET!)
- Timeout: 300 seconds (5 minutes)
- Headers: None (unless needed)

**EasyCron:**
- URL: Same as above
- HTTP Method: **POST**
- Timeout: 300 seconds
- Headers: None

### Step 3: Check Cron Service Logs

**cron-job.org:**
- Dashboard → Your cron job → "Executions"
- Click on failed execution
- Check:
  - Request sent?
  - Response received?
  - Status code?
  - Response body?

### Step 4: Check Koyeb Logs

**Koyeb Dashboard:**
- Service → Logs
- Look for:
  - POST request to `/api/admin/refresh`
  - Any errors
  - Scrape activity

### Step 5: Verify Response Format

The endpoint should return JSON like:
```json
{
  "status": "success",
  "sources_processed": 10,
  "sources_failed": 0,
  "new_offers": 5,
  "updated_offers": 3,
  "inactivated_offers": 1,
  "errors": [],
  "source_results": {...}
}
```

If you see this, the endpoint works! The cron service should accept 200 status.

## Quick Fixes

### Fix 1: Wrong HTTP Method

**Problem:** Using GET instead of POST

**Fix:**
- cron-job.org: Edit cron job → Request Method → Select **POST**
- EasyCron: Edit cron job → HTTP Method → Select **POST**

### Fix 2: Wrong URL

**Problem:** URL has typo or wrong path

**Fix:**
- Verify: `https://contemporary-tera-limerik-490a0aa8.koyeb.app/api/admin/refresh`
- Copy-paste directly from browser (after testing manually)
- Remove any trailing slashes

### Fix 3: Timeout Too Short

**Problem:** Scraping takes longer than cron service timeout

**Fix:**
- cron-job.org: Settings → Timeout → Set to 300 (5 minutes)
- EasyCron: Settings → Timeout → Set to 300

### Fix 4: Service Not Running

**Problem:** Koyeb service is stopped or sleeping

**Fix:**
- Check Koyeb dashboard → Service status
- Should be "Running" (not "Stopped" or "Sleeping")
- Restart service if needed

## Still Not Working?

If none of these fixes work:

1. **Share the exact error message** from cron service
2. **Share the status code** from cron service logs
3. **Share Koyeb logs** around the time of failure
4. **Test manually** and share the result

This will help identify the specific issue.
