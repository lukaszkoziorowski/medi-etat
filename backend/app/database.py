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
    # Railway and most platforms support both IPv4 and IPv6
    # PythonAnywhere free tier doesn't support IPv6, but Railway does
    try:
        parsed = urlparse(DATABASE_URL)
        hostname = parsed.hostname
        port = parsed.port
        
        # PythonAnywhere free tier is IPv4-only
        # Supabase direct connection is IPv6-only - MUST use pooler
        # Session Pooler (port 5432) is IPv4-compatible
        # Transaction Pooler (port 6543) may be blocked by PythonAnywhere
        if hostname and '.pooler.supabase.com' in hostname:
            # If using Transaction Pooler (6543), convert to Session Pooler (5432)
            # Session Pooler is IPv4-compatible and works on PythonAnywhere
            if port == 6543:
                # Convert Transaction Pooler to Session Pooler
                netloc_parts = parsed.netloc.split(':')
                if len(netloc_parts) >= 2:
                    # Replace port 6543 with 5432
                    netloc = ':'.join(netloc_parts[:-1]) + ':5432'
                else:
                    netloc = parsed.netloc + ':5432'
                
                DATABASE_URL = urlunparse((
                    parsed.scheme,
                    netloc,
                    parsed.path,
                    parsed.params,
                    parsed.query,
                    parsed.fragment
                ))
                # Re-parse after conversion
                parsed = urlparse(DATABASE_URL)
                hostname = parsed.hostname
                port = parsed.port
                import logging
                logging.getLogger(__name__).info(f"Converted Transaction Pooler (6543) to Session Pooler (5432) for IPv4 compatibility")
        
        # If using direct connection (IPv6-only), we MUST convert to Session Pooler
        if hostname and 'supabase.co' in hostname and '.pooler.' not in hostname:
            # Direct connection is IPv6-only and won't work on PythonAnywhere
            # Convert to Session Pooler (IPv4-compatible)
            username = parsed.username or ''
            if username and not username.startswith('postgres.'):
                # Extract project ref from hostname: db.xxx.supabase.co -> xxx
                project_ref = hostname.replace('db.', '').replace('.supabase.co', '')
                if project_ref:
                    # Convert to Session Pooler format
                    # Format: postgres.xxx:password@aws-1-eu-west-1.pooler.supabase.com:5432
                    pooler_hostname = hostname.replace('db.', 'aws-1-eu-west-1.pooler.').replace('.supabase.co', '.supabase.com')
                    pooler_username = f"postgres.{project_ref}"
                    
                    # Reconstruct netloc with pooler username and hostname
                    password = parsed.password or ''
                    if password:
                        auth = f"{pooler_username}:{password}"
                    else:
                        auth = pooler_username
                    
                    netloc = f"{auth}@{pooler_hostname}:5432"
                    
                    DATABASE_URL = urlunparse((
                        parsed.scheme,
                        netloc,
                        parsed.path,
                        parsed.params,
                        parsed.query,
                        parsed.fragment
                    ))
                    # Re-parse after conversion
                    parsed = urlparse(DATABASE_URL)
                    hostname = parsed.hostname
                    port = parsed.port
                    import logging
                    logging.getLogger(__name__).info(f"Converted direct connection to Session Pooler for IPv4 compatibility")
        
        # Try IPv4 resolution for all Supabase connections (direct or pooler)
        # PythonAnywhere free tier doesn't support IPv6 - MUST use IPv4
        if hostname and 'supabase' in hostname:
            # Check if hostname is already an IP address
            is_ip = False
            try:
                socket.inet_aton(hostname)  # Will raise exception if not an IP
                is_ip = True
            except socket.error:
                pass
            
            if not is_ip:
                # Not an IP, try to resolve to IPv4
                import logging
                logger = logging.getLogger(__name__)
                try:
                    # Force IPv4-only resolution (AF_INET = IPv4 only)
                    # This prevents IPv6 addresses from being returned
                    ip_addresses = socket.getaddrinfo(
                        hostname, 
                        port or 5432, 
                        socket.AF_INET,  # IPv4 only!
                        socket.SOCK_STREAM,
                        socket.IPPROTO_TCP
                    )
                    ipv4_address = None
                    for addr_info in ip_addresses:
                        if addr_info[0] == socket.AF_INET:  # IPv4
                            ipv4_address = addr_info[4][0]
                            break
                    
                    if ipv4_address:
                        # Replace hostname with IPv4 address in netloc
                        # Handle port in netloc properly
                        if ':' in parsed.netloc:
                            # netloc format: user:pass@host:port
                            parts = parsed.netloc.rsplit('@', 1)
                            if len(parts) == 2:
                                auth_part, host_port = parts
                                if ':' in host_port:
                                    host_part, port_part = host_port.rsplit(':', 1)
                                    netloc = f"{auth_part}@{ipv4_address}:{port_part}"
                                else:
                                    netloc = f"{auth_part}@{ipv4_address}:{port or 5432}"
                            else:
                                # No auth, just host:port
                                if ':' in parsed.netloc:
                                    netloc = parsed.netloc.replace(hostname, ipv4_address)
                                else:
                                    netloc = f"{ipv4_address}:{port or 5432}"
                        else:
                            # No port in netloc
                            if '@' in parsed.netloc:
                                # Has auth: user:pass@host
                                auth_part, host_part = parsed.netloc.rsplit('@', 1)
                                netloc = f"{auth_part}@{ipv4_address}:{port or 5432}"
                            else:
                                # Just hostname
                                netloc = f"{ipv4_address}:{port or 5432}"
                        
                        DATABASE_URL = urlunparse((
                            parsed.scheme,
                            netloc,
                            parsed.path,
                            parsed.params,
                            parsed.query,
                            parsed.fragment
                        ))
                        logger.info(f"Resolved {hostname} to IPv4: {ipv4_address}. New URL: {DATABASE_URL.split('@')[0]}@[REDACTED]")
                    else:
                        logger.warning(f"Could not find IPv4 address for {hostname}")
                except (socket.gaierror, OSError, ValueError) as e:
                    # If resolution fails, log error
                    import logging
                    logging.getLogger(__name__).error(f"Could not resolve {hostname} to IPv4: {e}. Connection will likely fail on PythonAnywhere.")
    except Exception as e:
        # If URL parsing fails, log and continue with original URL
        import logging
        logging.getLogger(__name__).error(f"Error parsing DATABASE_URL: {e}. Using as-is.")
    
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
