#!/bin/bash
set -e

echo "Installing Python dependencies (without Playwright)..."
# Install all packages at once with optimizations
# Common transitive dependencies are pre-pinned in requirements-railway.txt to reduce backtracking
pip install --no-cache-dir --use-deprecated=legacy-resolver --prefer-binary -r requirements-railway.txt

echo "Build complete! (Playwright will be installed separately in GitHub Actions)"
