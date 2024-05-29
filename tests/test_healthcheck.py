import pytest
from pytest_mock import mocker

def test_healthcheck_success(test_client, mocker):
  """Tests if the /healthcheck endpoint returns a healthy status."""

  # Mock the model_initialized flag to simulate an unhealthy state
  mock_model_initialized = mocker.patch("embedding_api.model_initialized", return_value=True)  

  response = test_client.get("/healthcheck")  # Use synchronous GET request

  assert response.status_code == 200
  assert response.json() == {"status": "healthy"}

def test_healthcheck_unhealthy(test_client, mocker):
  """Tests if the /healthcheck endpoint returns unhealthy when model is not initialized."""

  # Mock the model_initialized flag to simulate an unhealthy state
  mock_model_initialized = mocker.patch("embedding_api.model_initialized", return_value=False)  

  response = test_client.get("/healthcheck")

  assert response.status_code == 503
  assert response.json() == {"status": "unhealthy"}

  # Verify that the mock was called (optional)
  mock_model_initialized.is_set.assert_called_once()
