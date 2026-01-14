#!/bin/bash
set -e

echo "Installing Python dependencies (without Playwright)..."
# Install packages with optimizations for faster builds
pip install --no-cache-dir --use-deprecated=legacy-resolver --prefer-binary -r requirements-railway.txt

echo "Build complete! (Playwright will be installed separately in GitHub Actions)"
