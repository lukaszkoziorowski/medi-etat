"""
FastAPI application for Medietat job search engine.
"""
import os
import logging
import re
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.database import init_db
from app.api import jobs, admin
# Note: APScheduler removed - using Koyeb cron jobs instead

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    
    Handles:
    - Database initialization
    - Cleanup on shutdown
    
    Note: Scheduled refreshes are handled by Koyeb cron jobs,
    not by an in-process scheduler.
    """
    # Startup
    logger.info("Starting Medietat API...")
    init_db()
    logger.info("Database initialized")
    logger.info("Scheduled refreshes are handled by Koyeb cron jobs")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Medietat API...")
    logger.info("Shutdown complete")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Medietat API",
    description="Job search engine API for medical professionals in Poland",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware - allow frontend to call API
# Get frontend URL from environment variable or use localhost for development
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Build allowed origins list
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://medi-etat.vercel.app",  # Production Vercel deployment
]

# Add FRONTEND_URL to list if not already there
if FRONTEND_URL and FRONTEND_URL not in ALLOWED_ORIGINS:
    ALLOWED_ORIGINS.append(FRONTEND_URL)

# Use CORS middleware with regex pattern to allow all Vercel preview URLs
# Vercel preview URLs can have various patterns, so we allow all .vercel.app domains
# Also allow all origins in development/production to avoid redirect issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins to avoid CORS issues (can be restricted later for security)
    allow_credentials=False,  # Must be False when allow_origins=["*"]
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"],  # Explicitly allow common headers
    expose_headers=["*"],
)

# Add explicit CORS headers middleware as fallback (in case CORSMiddleware doesn't work in WSGI)
class CORSHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Explicitly add CORS headers
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, HEAD"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept, Origin, X-Requested-With"
        response.headers["Access-Control-Expose-Headers"] = "*"
        return response

app.add_middleware(CORSHeaderMiddleware)


# Include API routers
app.include_router(jobs.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Medietat API is running",
        "version": "0.1.0",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


# Note: FastAPI CORS middleware handles OPTIONS automatically
# No need for explicit OPTIONS handler - it was causing 405 errors

