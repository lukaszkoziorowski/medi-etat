#!/bin/bash
set -e

echo "Installing Python dependencies (without Playwright)..."
echo "Using fully locked requirements-railway.txt with ALL transitive dependencies pinned..."

# Use pip-sync from pip-tools - it's designed for locked requirements files
# It installs exact versions without any dependency resolution
echo "Installing pip-tools for pip-sync..."
pip install --quiet --no-cache-dir pip-tools

echo "Syncing packages to exact versions (no dependency resolution)..."
pip-sync --no-cache-dir requirements-railway.txt

echo "Build complete! (Playwright will be installed separately in GitHub Actions)"
