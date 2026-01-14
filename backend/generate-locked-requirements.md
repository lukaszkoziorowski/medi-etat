# Generate Locked Requirements File

## Problem
Pip is backtracking through multiple versions of packages trying to find compatible versions, causing build timeouts.

## Solution
Generate a fully locked `requirements-railway.txt` with ALL transitive dependencies pinned to exact versions.

## Steps

1. **Activate your virtual environment:**
   ```bash
   cd backend
   source venv/bin/activate  # or: python -m venv venv && source venv/bin/activate
   ```

2. **Run the compile script:**
   ```bash
   bash compile-requirements.sh
   ```

3. **Review the generated file:**
   ```bash
   cat requirements-railway.txt
   ```
   You should see ALL dependencies with exact versions pinned (e.g., `fastapi==0.104.1`, `starlette==0.27.0`, etc.)

4. **Commit and push:**
   ```bash
   git add requirements-railway.txt
   git commit -m "Lock all dependencies to prevent pip backtracking"
   git push origin main
   ```

5. **Railway will automatically use the locked file** - no more backtracking!

## What This Does

- `pip-compile` reads `requirements.in` (top-level dependencies)
- Resolves ALL transitive dependencies
- Generates `requirements-railway.txt` with EVERY package pinned to exact versions
- Pip then just installs exact versions (no resolution needed = fast!)

## Alternative: Manual Generation

If the script doesn't work, you can also:

```bash
pip install pip-tools
pip-compile --output-file=requirements-railway.txt requirements.in
```
