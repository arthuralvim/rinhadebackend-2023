import os
from functools import lru_cache

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    asyncpg_url: PostgresDsn = (
        os.environ.get("TEST_DATABASE_URL")
        if bool(os.environ.get("TESTING"))
        else os.environ.get("DATABASE_URL")
    )
    redis_url: RedisDsn = os.getenv("REDIS_URL")
    redis_default_expiration: int = 60 * 60 * 24


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
