"""
Database connection and session management.
"""
import os
import socket
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from urllib.parse import urlparse, urlunparse

from app.models import Base

# Get database URL from environment variable (for production) or use SQLite (for local)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./medi-etat.db")

# Convert postgres:// to postgresql:// for SQLAlchemy compatibility
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Determine if we're using SQLite or PostgreSQL
is_sqlite = DATABASE_URL.startswith("sqlite")

if is_sqlite:
    # SQLite configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # Needed for SQLite
        poolclass=StaticPool,  # SQLite doesn't support connection pooling
        echo=False,  # Set to True for SQL query logging during development
    )
else:
    # PostgreSQL configuration
    # PythonAnywhere free tier doesn't support IPv6 connections
    # We need to resolve the hostname to IPv4 and use that in the connection string
    parsed = urlparse(DATABASE_URL)
    hostname = parsed.hostname
    
    # Resolve hostname to IPv4 address
    try:
        # Get all IP addresses for the hostname
        ip_addresses = socket.getaddrinfo(hostname, None, socket.AF_INET, socket.SOCK_STREAM)
        # Prefer IPv4 (AF_INET)
        ipv4_address = None
        for addr_info in ip_addresses:
            if addr_info[0] == socket.AF_INET:  # IPv4
                ipv4_address = addr_info[4][0]
                break
        
        if ipv4_address:
            # Replace hostname with IPv4 address in connection string
            netloc = parsed.netloc.replace(hostname, ipv4_address)
            DATABASE_URL = urlunparse((
                parsed.scheme,
                netloc,
                parsed.path,
                parsed.params,
                parsed.query,
                parsed.fragment
            ))
            logger = __import__('logging').getLogger(__name__)
            logger.info(f"Resolved {hostname} to IPv4: {ipv4_address}")
    except Exception as e:
        # If resolution fails, try original URL
        logger = __import__('logging').getLogger(__name__)
        logger.warning(f"Could not resolve {hostname} to IPv4: {e}. Using original URL.")
    
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=5,  # Connection pool size
        max_overflow=10,  # Max overflow connections
        echo=False,
        connect_args={
            "connect_timeout": 10,
        },
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database - create all tables."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """
    Dependency for FastAPI to get database session.
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
