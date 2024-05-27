#test_get_embeddings.py
import pytest

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