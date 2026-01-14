#!/bin/bash
set -e

echo "Installing Python dependencies (without Playwright)..."
# Using fully locked requirements-railway.txt with ALL transitive dependencies pinned
# No dependency resolution needed - pip just installs exact versions (fast!)
pip install --no-cache-dir --prefer-binary -r requirements-railway.txt

echo "Build complete! (Playwright will be installed separately in GitHub Actions)"
