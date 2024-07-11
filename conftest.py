import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from embedding_api import app
from threading import Event
import numpy as np

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
@pytest.fixture(scope='function')
def fake_model(monkeypatch):

  class fake_model:
    def encode(text):
      return np.array([0.1, 0.2, 0.3])
    
  #For unit testing purposes bypass model
  monkeypatch.setattr('embedding_api.model', fake_model)
  #Set fake model_initialized flag
  fake_event = Event()
  fake_event.set()
  monkeypatch.setattr('embedding_api.model_initialized', fake_event)
  yield
