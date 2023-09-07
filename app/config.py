import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


def get_db_uri() -> str:
    if bool(os.environ.get("TESTING")):
        return os.environ.get("TEST_DATABASE_URL")

    return os.environ.get("DATABASE_URL")


engine = create_engine(get_db_uri(), pool_pre_ping=True, pool_size=32, max_overflow=64)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
