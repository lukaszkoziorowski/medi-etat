#!/bin/bash
set -e

echo "Installing Python dependencies (without Playwright)..."
echo "Using fully locked requirements-railway.txt with ALL transitive dependencies pinned..."

# Install packages individually with --no-deps to ensure no resolution happens
# This completely bypasses pip's dependency resolver
echo "Installing packages one by one with --no-deps (no resolution)..."
while IFS= read -r line || [ -n "$line" ]; do
    # Skip empty lines
    [[ -z "${line// }" ]] && continue
    
    # Extract package name (handle == version)
    package=$(echo "$line" | sed 's/#.*$//' | xargs | cut -d'=' -f1-2)
    [[ -z "$package" ]] && continue
    
    echo "Installing $package..."
    pip install --no-cache-dir --prefer-binary --no-deps "$package" || {
        echo "Warning: Failed to install $package with --no-deps, trying normal install..."
        pip install --no-cache-dir --prefer-binary "$package"
    }
done < requirements-railway.txt

echo "Build complete! (Playwright will be installed separately in GitHub Actions)"
