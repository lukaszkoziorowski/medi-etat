#!/bin/bash
# This script runs automatically when the service starts
# It installs Playwright browsers if not already installed

if [ ! -d "$HOME/.cache/ms-playwright" ]; then
    echo "Installing Playwright browsers (first run)..."
    python -m playwright install chromium --with-deps || python -m playwright install chromium
    echo "Playwright browsers installed."
fi
