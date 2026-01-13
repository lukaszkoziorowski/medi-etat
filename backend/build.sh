#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Playwright browser..."
playwright install chromium
playwright install-deps chromium

echo "Build complete!"
