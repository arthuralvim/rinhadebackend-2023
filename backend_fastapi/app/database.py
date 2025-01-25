import os

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from app import settings

global_settings = settings.get_settings()


engine = create_async_engine(
    global_settings.asyncpg_url.unicode_string(),
    pool_size=int(os.getenv("DB_POOL", 300)),
    max_overflow=int(os.getenv("DB_POOL_OVERFLOW", 50)),
    future=True, echo=False,
)

# expire_on_commit=False will prevent attributes from being expired
# after commit.
AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


# Dependency
async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        yield session
