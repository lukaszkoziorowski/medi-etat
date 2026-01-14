#!/bin/bash
set -e

echo "Installing Python dependencies (without Playwright)..."
pip install --no-cache-dir -r requirements-railway.txt

echo "Build complete! (Playwright will be installed separately in GitHub Actions)"
