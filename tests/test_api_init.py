#test_api_init.py

from embeddings_api import  model_initialized

def test_model_initialization(client):

        # Wait for the model_initialized event
        model_initialized.wait(timeout=30)  # Adjust timeout as needed

        # Assertions
        assert model_initialized.is_set(), "set model initialization event for healthcheck"

        response = client.get('/healthcheck')  # Use the client fixture
        assert response.status_code == 200

