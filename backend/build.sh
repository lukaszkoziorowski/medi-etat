#!/bin/bash
set -e

echo "Installing Python dependencies (without Playwright)..."
echo "Using fully locked requirements-railway.txt with ALL transitive dependencies pinned..."

# Install ALL packages with --no-deps to prevent ANY dependency resolution
# This forces pip to install exact versions without checking compatibility
echo "Installing exact package versions (no dependency resolution)..."
pip install --no-cache-dir --prefer-binary --no-deps -r requirements-railway.txt

# Verify installation worked (some packages might fail silently with --no-deps)
# If critical packages are missing, pip will fail when importing
echo "Verifying installation..."
python -c "import fastapi, uvicorn, sqlalchemy, bs4, requests; print('✅ Core packages installed')" || {
    echo "⚠️  Some packages may need dependencies. Installing with minimal resolution..."
    # Fallback: install with legacy resolver (faster than new resolver)
    pip install --no-cache-dir --prefer-binary --use-deprecated=legacy-resolver -r requirements-railway.txt
}

echo "Build complete! (Playwright will be installed separately in GitHub Actions)"
