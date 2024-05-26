import pytest
from fastapi.testclient import TestClient
from embedding_api import app


@pytest.fixture(scope='session')
def test_client():  # Renamed to reflect its purpose
    """Setup a test client for the FastAPI application."""
    with TestClient(app) as client:
        yield client  # Yield the test client


# No need for a client fixture that depends on test_client in FastAPI
#@pytest.fixture(scope='class')
#def client(test_client):  # Depend on the test_client fixture
    """Provide a test client for each test class."""
#    yield test_client  # Yield the test client


  