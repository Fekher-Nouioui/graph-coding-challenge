"""Database connection and session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from src.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL, # Use the config.py settings to retrieve the DATABASE_URL
    pool_pre_ping=True,  # Verify connections before using them
    echo=False,  # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency function to get database session.

    Yields:
        SQLAlchemy Session object

    Usage in FastAPI:
        @app.get("/endpoint")
        def endpoint(db: Session = Depends(get_db)):
            # Use db here
            pass
    """
    db = SessionLocal() # Gets connection from engine's session pool pool
    try:
        yield db
    finally:
        db.close()
