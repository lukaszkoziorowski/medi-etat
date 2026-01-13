#!/bin/bash
set -e

echo "Installing Playwright browser (this may take a few minutes)..."
playwright install chromium --with-deps || playwright install chromium
echo "Playwright installation complete!"
