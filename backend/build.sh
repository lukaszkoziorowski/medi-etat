#!/bin/bash
set -e

echo "Installing Python dependencies (without Playwright)..."
# Use legacy resolver to avoid extensive backtracking with transitive dependencies
pip install --no-cache-dir --use-deprecated=legacy-resolver -r requirements-railway.txt

echo "Build complete! (Playwright will be installed separately in GitHub Actions)"
