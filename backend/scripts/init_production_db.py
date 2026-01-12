#!/usr/bin/env python3
"""
Initialize production database schema.
Run this after deploying to Render to set up the database tables.
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import init_db

if __name__ == "__main__":
    print("Initializing database schema...")
    try:
        init_db()
        print("✓ Database schema initialized successfully!")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        sys.exit(1)
