"""PostgreSQL database connection management."""
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError
import logging

from src.config import config
from src.models.base import Base

logger = logging.getLogger(__name__)

# Create engine
engine = create_engine(
    config.DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,
    max_overflow=10
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db() -> Session:
    """
    Get database session as context manager.
    
    Usage:
        with get_db() as db:
            # use db session
            pass
    
    Yields:
        SQLAlchemy Session
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def check_database_connection() -> bool:
    """
    Check if database connection is working.
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except OperationalError as e:
        logger.error(f"Database connection failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return False

def check_pgvector_extension() -> bool:
    """
    Check if pgvector extension is enabled.
    
    Returns:
        True if pgvector is enabled, False otherwise
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM pg_extension WHERE extname = 'vector'")
            )
            if result.fetchone():
                logger.info("pgvector extension: Enabled")
                return True
            else:
                logger.warning("pgvector extension: Not enabled - run 'CREATE EXTENSION vector;'")
                return False
    except Exception as e:
        logger.error(f"pgvector check failed: {e}")
        return False

def init_db():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
