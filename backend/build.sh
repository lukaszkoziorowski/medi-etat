#!/bin/bash
set -e

echo "Installing Python dependencies (without Playwright)..."
echo "Using fully locked requirements-railway.txt with ALL transitive dependencies pinned..."

# Install ALL packages with --no-deps to completely prevent dependency resolution
# Since all dependencies are in the locked file, we install them all at once
# This tells pip: "Install these exact packages, don't check or resolve anything"
echo "Installing exact package versions (--no-deps prevents ALL resolution)..."
pip install --no-cache-dir --prefer-binary --no-deps -r requirements-railway.txt

echo "Build complete! (Playwright will be installed separately in GitHub Actions)"
