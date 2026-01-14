#!/bin/bash
set -e

echo "Installing Python dependencies (without Playwright)..."
echo "Using fully locked requirements-railway.txt with ALL transitive dependencies pinned..."

# Strategy: Install packages in two passes to avoid dependency resolution
# First, install all packages with --no-deps (no resolution at all)
# Then verify and install any missing dependencies if needed

echo "Installing all packages with --no-deps (no dependency resolution)..."
if pip install --no-cache-dir --prefer-binary --no-deps -r requirements-railway.txt 2>&1 | grep -q "ERROR"; then
    echo "⚠️  Some packages failed with --no-deps, trying without it..."
    # If --no-deps fails, install normally but with legacy resolver
    pip install --no-cache-dir --prefer-binary --use-deprecated=legacy-resolver -r requirements-railway.txt
else
    echo "✅ All packages installed with --no-deps (no resolution performed)"
fi

echo "Build complete! (Playwright will be installed separately in GitHub Actions)"
