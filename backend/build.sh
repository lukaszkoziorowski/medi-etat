#!/bin/bash
set -e

echo "Installing Python dependencies (without Playwright)..."
echo "Using fully locked requirements-railway.txt with ALL transitive dependencies pinned..."

# Install packages directly from locked file
# All versions are exact, so pip should not need to resolve
# Use --no-deps to prevent any dependency resolution attempts
echo "Installing exact package versions (no dependency resolution)..."
pip install --no-cache-dir --prefer-binary --no-deps -r requirements-railway.txt 2>/dev/null || {
    # If --no-deps fails (expected for some packages), install normally
    # But use --use-deprecated=legacy-resolver to speed up if resolution is needed
    echo "Installing with dependency resolution (should be minimal with locked file)..."
    pip install --no-cache-dir --prefer-binary --use-deprecated=legacy-resolver -r requirements-railway.txt
}

echo "Build complete! (Playwright will be installed separately in GitHub Actions)"
