




from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

from unittest.mock import patch
import pytest

@pytest.fixture(autouse=True)
def mock_email():
    with patch("resend.Emails.send"):
        yield