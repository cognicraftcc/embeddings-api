import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from embedding_api import app
from pytest_mock import mocker


@pytest.fixture(scope='session')
def test_client():
    """Setup a synchronous test client for the FastAPI application."""
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope='session')
async def async_test_client():
  """Setup an asynchronous test client for the FastAPI application."""
  async with AsyncClient(app=app, base_url="http://test") as client:
    yield client

# Fixture to mock the model's encode method
@pytest.fixture
def mock_model(mocker):
    mocker.patch("embedding_api.model.encode", return_value=[0.1, 0.2, 0.3])

