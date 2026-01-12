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
# Vercel preview URLs can have various patterns:
# - https://medi-etat-*.vercel.app
# - https://medi-etat-*-koziorowskilukaszs-projects.vercel.app
# - https://*.vercel.app (catch-all for any Vercel deployment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Explicit origins
    allow_origin_regex=r"https://.*\.vercel\.app",  # Allow ALL Vercel deployments (preview and production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

