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
    # Supabase connection strings may resolve to IPv6, so we need to force IPv4
    parsed = urlparse(DATABASE_URL)
    hostname = parsed.hostname
    
    # Try to resolve hostname to IPv4 address
    # If the hostname is a Supabase direct connection, we should use the pooler instead
    if hostname and 'supabase.co' in hostname and '.pooler.' not in hostname:
        # Use Supabase connection pooler (uses IPv4 and is more reliable)
        # Replace direct connection with pooler connection
        # Format: db.xxx.supabase.co -> db.xxx.supabase.co:6543 (pooler port)
        # Or use: aws-0-[region].pooler.supabase.com:6543
        # For now, try resolving to IPv4 first
        try:
            # Force IPv4 resolution
            ip_addresses = socket.getaddrinfo(hostname, None, socket.AF_INET, socket.SOCK_STREAM)
            ipv4_address = None
            for addr_info in ip_addresses:
                if addr_info[0] == socket.AF_INET:  # IPv4
                    ipv4_address = addr_info[4][0]
                    break
            
            if ipv4_address:
                # Replace hostname with IPv4 address
                netloc = parsed.netloc.replace(hostname, ipv4_address)
                DATABASE_URL = urlunparse((
                    parsed.scheme,
                    netloc,
                    parsed.path,
                    parsed.params,
                    parsed.query,
                    parsed.fragment
                ))
                import logging
                logging.getLogger(__name__).info(f"Resolved {hostname} to IPv4: {ipv4_address}")
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Could not resolve {hostname} to IPv4: {e}")
    
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
