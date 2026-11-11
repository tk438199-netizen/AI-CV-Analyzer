from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL

DATABASE_URL = "sqlite:///./cv_analyzer.db"

# Create Engine

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create Session

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create Base

Base = declarative_base()


# Database Dependency

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()

