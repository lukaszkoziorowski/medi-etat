"""
FastAPI application for Medietat job search engine.
"""
import os
import logging
import re
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.api import jobs, admin
from app.services.scheduler import start_scheduler, stop_scheduler

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
    - Automatic refresh scheduler startup
    - Cleanup on shutdown
    """
    # Startup
    logger.info("Starting Medietat API...")
    init_db()
    logger.info("Database initialized")
    
    # Start automatic refresh scheduler
    try:
        start_scheduler()
        logger.info("Automatic refresh scheduler started")
    except Exception as e:
        logger.error(f"Failed to start scheduler: {str(e)}", exc_info=True)
        # Continue even if scheduler fails - manual refresh still works
    
    yield
    
    # Shutdown
    logger.info("Shutting down Medietat API...")
    try:
        stop_scheduler()
        logger.info("Scheduler stopped")
    except Exception as e:
        logger.error(f"Error stopping scheduler: {str(e)}", exc_info=True)
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

