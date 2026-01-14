#!/bin/bash
set -e

echo "=========================================="
echo "Installing Python dependencies (without Playwright)..."
echo "Using fully locked requirements-railway.txt"
echo "=========================================="

# Verify we're using the correct requirements file
if [ ! -f "requirements-railway.txt" ]; then
    echo "ERROR: requirements-railway.txt not found!"
    exit 1
fi

echo "Installing ALL packages with --no-deps (NO dependency resolution)..."
echo "This prevents pip from looking at multiple versions"

# Install all packages at once with --no-deps
# This completely prevents dependency resolution
pip install --no-cache-dir --prefer-binary --no-deps -r requirements-railway.txt

echo "=========================================="
echo "Build complete! (Playwright installed separately in GitHub Actions)"
echo "=========================================="
