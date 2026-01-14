#!/usr/bin/env python3
"""
Generate a fully locked requirements-railway.txt file.
This pins ALL transitive dependencies to prevent pip backtracking.
"""
import subprocess
import sys
import os

def main():
    print("🔧 Installing pip-tools...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip-tools"])
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install pip-tools: {e}")
        sys.exit(1)
    
    print("📦 Compiling requirements-railway.txt from requirements.in...")
    print("   This will pin ALL transitive dependencies to exact versions...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "piptools", "compile",
            "--output-file=requirements-railway.txt",
            "--no-header",
            "--no-emit-index-url",
            "--strip-extras",
            "requirements.in"
        ])
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to compile requirements: {e}")
        sys.exit(1)
    
    if os.path.exists("requirements-railway.txt"):
        print("")
        print("✅ Generated requirements-railway.txt with ALL dependencies pinned!")
        print("📝 Next steps:")
        print("   1. Review the generated file")
        print("   2. Commit it: git add backend/requirements-railway.txt && git commit -m 'Lock all dependencies'")
        print("   3. Push: git push origin main")
        print("   4. Railway will use locked versions (no backtracking, fast builds!)")
    else:
        print("❌ requirements-railway.txt was not generated")
        sys.exit(1)

if __name__ == "__main__":
    main()
