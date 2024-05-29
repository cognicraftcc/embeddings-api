#test_get_embeddings.py
import pytest
from pytest_mock import mocker

'''
@pytest.mark.asyncio
async def test_process_data_success(async_test_client, mock_model):
    token = "test_token"  # Assume a valid token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "text": "test text"
    }

    async with async_test_client as client:  # Access the yielded client object
        response = await client.post("/get_embeddings", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Text embeddings"
    assert isinstance(response.json()["embeddings"], list)
'''

# Test function using the test_client fixture
def test_get_embeddings_success(test_client,mock_model):
    # Simulate a valid JWT token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNjk3NjU2NSwianRpIjoiYmI1MjAyMWUtZDEwYy00N2U3LTk0NDYtZWVkOTZmYTdhNGRiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEyMzQ1IiwibmJmIjoxNzE2OTc2NTY1LCJjc3JmIjoiNDRmNGIxN2YtYTJkZS00ZDFjLWFlMTQtMWNiZDk3ZDYwYTNjIiwiZXhwIjoxNzE2OTc3NDY1fQ.GWXDggORUxjpzQFP6IrLrr3NuSW40SlGbHEOuN8DMzo"  # Replace with a valid token structure

    # Set headers with the token
    headers = {"Authorization": f"Bearer {token}"}

    # Prepare test data
    data = {"text": "This is some test text"}

    # Patch model.encode within the test function
    # mock_encode = mocker.patch.object("embedding_api.model", "encode", return_value=[0.1, 0.2, 0.3])


    # Send the POST request
    response = test_client.post("/get_embeddings", json=data, headers=headers)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response content (assuming expected structure)
    response_data = response.json()
    assert "user_id" in response_data
    assert "embeddings" in response_data
    assert "message" in response_data
    assert response_data["message"] == "Text embeddings"

    