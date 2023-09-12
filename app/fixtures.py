import pytest
from httpx import AsyncClient

from sqlalchemy.ext.asyncio import async_sessionmaker
from app.database import engine
from app.main import app
from app.models.base import Base
from sqlalchemy import text
from app.redis import get_redis


@pytest.fixture(
    scope="session",
    params=[
        pytest.param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop"),
    ],
)
def anyio_backend(request):
    return request.param


@pytest.fixture
def pessoa_():
    return {
        "nome": "bruce wayne da silva",
        "apelido": "batman",
        "nascimento": "1979-04-20",
    }


@pytest.fixture()
async def engine_():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "pg_trgm";'))
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture()
async def db_session(engine_):
    async with engine_.begin() as conn:
        AsyncSessionFactory = async_sessionmaker(
            engine,
            autoflush=False,
            expire_on_commit=False,
        )
        async with AsyncSessionFactory() as session:
            # logger.debug(f"ASYNC Pool: {engine.pool.status()}")
            yield session

        await conn.rollback()


@pytest.fixture()
async def redis():
    r = await get_redis()
    await r.flushdb()
    yield r


@pytest.fixture(scope="session")
async def client() -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url="http://testserver/",
        headers={"Content-Type": "application/json"},
    ) as test_client:
        app.state.redis = await get_redis()
        yield test_client
