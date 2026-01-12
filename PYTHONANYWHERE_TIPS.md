# PythonAnywhere Tips & Tricks

## How to Paste Commands in PythonAnywhere Bash

PythonAnywhere's web-based terminal can be tricky with pasting. Here are the methods:

### Method 1: Right-Click Paste (Easiest)
1. Copy your command (from this guide or anywhere)
2. Right-click in the PythonAnywhere Bash terminal
3. Select "Paste" from the context menu
4. Press Enter to execute

### Method 2: Keyboard Shortcuts
- **Mac**: `Cmd + V`
- **Windows/Linux**: `Ctrl + V` or `Ctrl + Shift + V`
- **Alternative**: `Shift + Insert` (works on most systems)

### Method 3: Type Manually
If pasting doesn't work, you can type commands manually. Most commands in the guide are short and simple.

## Common Issues

### Command Not Found
- Make sure you're in the right directory
- Check if you need to activate virtual environment: `source venv/bin/activate`
- Verify Python version: `python3.9 --version`

### Permission Denied
- Use `--user` flag with pip: `pip install --user package-name`
- Check file permissions: `ls -la`

### Web App Not Reloading
- Wait 30-60 seconds after clicking "Reload"
- Check error log in "Web" tab
- Verify WSGI configuration file is correct

### Can't Find Files
- Use `pwd` to see current directory
- Use `ls` to list files
- Use `cd ~` to go to home directory
- Use `cd ~/medi-etat/backend` to go to project directory

## Useful Commands

```bash
# See current directory
pwd

# List files
ls
ls -la  # Detailed list

# Change directory
cd ~                    # Home directory
cd ~/medi-etat/backend  # Project directory

# Activate virtual environment
source venv/bin/activate

# Check Python version
python3.9 --version

# Install package
pip install --user package-name

# Check if web app is running
# Go to "Web" tab and check status
```

## Editing Files

### Method 1: Web Editor (Recommended)
1. Click "Files" tab
2. Navigate to your file
3. Click on the file
4. Edit in the web editor
5. Click "Save"

### Method 2: Nano Editor (Terminal)
```bash
nano filename.py
# Edit the file
# Press Ctrl+X to exit
# Press Y to save
# Press Enter to confirm
```

### Method 3: Vim Editor (Advanced)
```bash
vim filename.py
# Press 'i' to enter insert mode
# Edit the file
# Press Esc to exit insert mode
# Type ':wq' and press Enter to save and quit
```

## Environment Variables

To set environment variables in PythonAnywhere:

1. **Create `.env` file** (Recommended):
   - Go to "Files" tab
   - Navigate to `/home/yourusername/medi-etat/backend`
   - Create new file named `.env`
   - Add variables:
     ```
     DATABASE_URL=your-database-url
     FRONTEND_URL=your-frontend-url
     ```

2. **Or set in WSGI file**:
   - Edit WSGI configuration file
   - Add: `os.environ['VARIABLE_NAME'] = 'value'`

## Reloading Web App

After making changes:
1. Go to "Web" tab
2. Click green "Reload" button
3. Wait 30-60 seconds
4. Check if it's running (green status)

## Checking Logs

1. **Error Logs**:
   - Go to "Web" tab
   - Click "Error log" link
   - See recent errors

2. **Server Logs**:
   - Go to "Web" tab
   - Click "Server log" link
   - See server activity

3. **Bash Output**:
   - Run commands in "Bash" tab
   - See output directly

## Disk Space

Check disk usage:
```bash
df -h
du -sh ~/medi-etat
```

Free tier has 512MB limit. If you run out:
- Delete old files: `rm old-file.txt`
- Clean Python cache: `find . -type d -name __pycache__ -exec rm -r {} +`
- Remove old virtual environments if you recreate them

## Need Help?

- PythonAnywhere Help: https://help.pythonanywhere.com
- Check error logs first
- Verify all environment variables are set
- Make sure virtual environment is activated
- Check Python version matches (3.9)
