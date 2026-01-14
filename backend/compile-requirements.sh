#!/bin/bash
# Script to compile requirements.in into a locked requirements-railway.txt
# This pins ALL transitive dependencies to prevent pip backtracking
# Run this locally: cd backend && bash compile-requirements.sh

set -e

echo "🔧 Installing pip-tools..."
pip install --upgrade pip-tools

echo "📦 Compiling requirements-railway.txt from requirements.in..."
echo "   This will pin ALL transitive dependencies to exact versions..."
pip-compile \
  --output-file=requirements-railway.txt \
  --no-header \
  --no-emit-index-url \
  --strip-extras \
  requirements.in

echo ""
echo "✅ Generated requirements-railway.txt with ALL dependencies pinned!"
echo "📝 Next steps:"
echo "   1. Review the generated file"
echo "   2. Commit it: git add backend/requirements-railway.txt && git commit -m 'Lock all dependencies'"
echo "   3. Push: git push origin main"
echo "   4. Railway will use locked versions (no backtracking, fast builds!)"
