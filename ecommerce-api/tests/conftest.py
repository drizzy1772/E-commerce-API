




from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base
from fastapi.testclient import TestClient
from app.database import get_db
from app.main import app
import pytest
from unittest.mock import patch
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")


engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False)




@pytest.fixture(scope="session")
def setup_db():
    import asyncio
    async def init():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    asyncio.get_event_loop().run_until_complete(init())
    yield
    async def drop():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    asyncio.get_event_loop().run_until_complete(drop())

@pytest.fixture(autouse=True)
def mock_email():
    with patch("resend.Emails.send"):
        yield

@pytest.fixture(scope="session")
def client(setup_db):
    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)