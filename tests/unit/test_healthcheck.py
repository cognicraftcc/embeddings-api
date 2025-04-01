import pytest
from threading import Event

def test_healthcheck_success(test_client, monkeypatch):
  """
  Tests if the /healthcheck endpoint returns a healthy status when the 
  model is initialized.
  """

  #Set fake event
  fake_event = Event()
  fake_event.set()

  #For testing purposes bypass model and replace with fake event flag
  monkeypatch.setattr('embedding_api.model_initialized', fake_event)

  response = test_client.get("/healthcheck")  # Use synchronous GET request

  assert response.status_code == 200
  assert response.json() == {"status": "healthy"}

def test_healthcheck_unhealthy(test_client, monkeypatch):
  """
  Tests if the /healthcheck endpoint returns unhealthy when the
  model is not initialized.
  """

  #Set fake event
  fake_event = Event()

  #For testing purposes bypass model and replace with fake event flag
  monkeypatch.setattr('embedding_api.model_initialized', fake_event)
  
  response = test_client.get("/healthcheck")

  assert response.status_code == 503
  assert response.json() == {"status": "unhealthy"}
