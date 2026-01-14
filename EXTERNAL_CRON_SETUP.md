# External Cron Job Setup for Koyeb

Since Koyeb doesn't support built-in cron jobs, we'll use an external cron service to trigger daily scrapes.

## Recommended: cron-job.org (Free, No Credit Card)

### Step 1: Create Account

1. Go to https://cron-job.org
2. Click **"Sign Up"** (top right)
3. Sign up with:
   - Email address
   - Password
   - **No credit card required** ✅
4. Verify your email (check inbox)

### Step 2: Create Cron Job

1. After logging in, you'll see the dashboard
2. Click **"Create cronjob"** button (green button, top right)

### Step 3: Configure Cron Job

Fill in the form:

**Basic Settings:**
- **Title**: `Medietat Daily Scrape` (or any name you prefer)
- **Address (URL)**: 
  ```
  https://contemporary-tera-limerik-490a0aa8.koyeb.app/api/admin/refresh
  ```
  (Replace with your actual Koyeb URL)

**Request Settings:**
- **Request Method**: Select **POST** (important!)
- **Request Body**: Leave empty
- **Request Headers**: Leave empty (or add if needed later)

**Schedule:**
- **Execution**: Select **"Daily"**
- **Time**: Set to **01:00** (1 AM UTC = 2 AM Polish time, 3 AM during DST)
- **Timezone**: UTC (default)

**Advanced Settings (Optional):**
- **Activate cronjob**: ✅ Checked (enabled)
- **Save responses**: Optional (useful for debugging)
- **Notifications**: Optional (email on failure)

### Step 4: Save and Test

1. Click **"Create cronjob"** button
2. The cron job will be created and scheduled
3. **Test it immediately**:
   - Click on your cron job in the list
   - Click **"Run now"** or **"Execute"** button
   - Check Koyeb logs to verify the scrape runs
   - Check `/api/jobs` endpoint to see if new data appears

### Step 5: Verify It Works

1. Wait for the scheduled time (or use "Run now")
2. Check Koyeb logs:
   - Go to Koyeb dashboard → Your service → Logs
   - Look for scrape activity and results
3. Check the API:
   - Visit `https://your-app.koyeb.app/api/jobs`
   - Verify new/updated job offers appear

## Alternative: EasyCron (Also Free)

If cron-job.org doesn't work for you:

1. Go to https://www.easycron.com
2. Sign up (free tier: 1 cron job)
3. Create cron job:
   - **Cron Job Name**: `Medietat Daily Scrape`
   - **URL**: `https://contemporary-tera-limerik-490a0aa8.koyeb.app/api/admin/refresh`
   - **HTTP Method**: POST
   - **Schedule**: `0 1 * * *` (1 AM UTC daily)
   - **Timezone**: UTC
4. Save and test

## Troubleshooting

### Cron Job Not Executing

1. **Check cron service logs**:
   - cron-job.org: Dashboard → Your cron job → "Executions" tab
   - Look for success/failure status
   - Check response codes (should be 200)

2. **Check Koyeb logs**:
   - Verify requests are reaching Koyeb
   - Look for any errors in the refresh process

3. **Test manually**:
   ```bash
   curl -X POST https://your-app.koyeb.app/api/admin/refresh
   ```
   If this works, the cron service should work too

### Wrong Time Zone

- **cron-job.org**: Set timezone to UTC, time to 01:00 (1 AM UTC = 2 AM Polish time)
- **EasyCron**: Use cron expression `0 1 * * *` with UTC timezone

### Authentication Issues

If you add authentication later:
- Add headers in cron service: `Authorization: Bearer YOUR_TOKEN`
- Or use query parameters: `?token=YOUR_TOKEN`

## Monitoring

### Check Cron Execution History

**cron-job.org:**
- Dashboard → Your cron job → "Executions" tab
- Shows last 100 executions with status codes

**EasyCron:**
- Dashboard → Your cron job → "Logs" tab
- Shows execution history

### Set Up Notifications

Both services allow email notifications:
- On failure
- On success (optional)
- Daily summary

## Schedule Details

**Current Schedule:**
- **Time**: 1 AM UTC
- **Polish Time**: 2 AM (winter), 3 AM (summer/DST)
- **Frequency**: Daily

**To Change Schedule:**
- **cron-job.org**: Edit cron job → Change time
- **EasyCron**: Edit cron job → Change cron expression

**Common Cron Expressions:**
- `0 1 * * *` - Daily at 1 AM UTC
- `0 2 * * *` - Daily at 2 AM UTC
- `0 0 * * *` - Daily at midnight UTC

## Security Considerations

1. **No Authentication**: Currently, `/api/admin/refresh` is public
   - Anyone with the URL can trigger a scrape
   - Consider adding authentication if needed

2. **Rate Limiting**: External cron services have rate limits
   - Free tier: Usually 1-2 requests per minute max
   - Daily schedule is well within limits

3. **URL Exposure**: The refresh endpoint URL is in the cron service
   - Keep your cron service account secure
   - Don't share the URL publicly

## Next Steps

After setting up the cron job:

1. ✅ Test it immediately ("Run now")
2. ✅ Verify it works (check Koyeb logs)
3. ✅ Wait for first scheduled run
4. ✅ Monitor for a few days
5. ✅ Update frontend to use Koyeb URL
6. ✅ Decommission Railway (after validation)

## Backup Option: GitHub Actions

If external cron services don't work, you can keep using GitHub Actions:

1. The existing `.github/workflows/scrape.yml` is still in the repo
2. Update `RAILWAY_API_URL` secret to `KOYEB_API_URL`
3. Point it to your Koyeb URL
4. It will run daily at 2 AM UTC

This provides redundancy if the external cron fails.
