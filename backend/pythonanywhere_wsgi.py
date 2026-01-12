# This file is used by PythonAnywhere to serve your FastAPI app
# Place this file in your PythonAnywhere web app directory

import sys
import os

# Add your project directory to the path
project_home = '/home/yourusername/medi-etat/backend'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Import the FastAPI app
from app.main import app

# Convert ASGI (FastAPI) to WSGI for PythonAnywhere
from app.wsgi_adapter import ASGI2WSGI

# PythonAnywhere expects a WSGI application
application = ASGI2WSGI(app)
