"""
Database connection and session management.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

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
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=5,  # Connection pool size
        max_overflow=10,  # Max overflow connections
        echo=False,
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
