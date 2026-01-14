#!/bin/bash
# Script to compile requirements.in into a locked requirements-railway.txt
# This pins all transitive dependencies to prevent pip backtracking
# Run this locally: bash compile-requirements.sh

set -e

echo "Installing pip-tools..."
pip install pip-tools

echo "Compiling requirements-railway.txt from requirements.in..."
pip-compile --output-file=requirements-railway.txt requirements.in

echo "✅ Generated requirements-railway.txt with all dependencies pinned"
echo "Commit this file and Railway will use the locked versions (no backtracking!)"
