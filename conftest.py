import pytest
from embeddings_api import app


@pytest.fixture(scope='session')
def test_client():  # Renamed to reflect its purpose
    """Setup a test client for the Flask application."""
    with app.test_client() as test_client:
        yield test_client  # Yield the test client


@pytest.fixture(scope='class')
def client(test_client):  # Depend on the test_client fixture
    """Provide a test client for each test class."""
    yield test_client  # Yield the test client
