




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


TEST_DATABASE_URL = "sqlite:///./test.db"

FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")


engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=engine)




@pytest.fixture(scope="session")
def setup_db():
    Base.metadata.create_all(bind=engine)
    
    yield engine

    Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def mock_email():
    with patch("resend.Emails.send"):
        yield

@pytest.fixture(scope="session")
def client(setup_db):
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)