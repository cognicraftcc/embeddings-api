#test_get_embeddings.py

from jose import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

# Test standard api call with real model
def test_get_embeddings_standard_call(test_client):

    # JWT token config
    SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    ALGORITHM = 'HS256'

    token_data={"sub": "12345"}
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    token_data.update({"exp": expire})
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    # Set headers with the token
    headers = {"Authorization": f"Bearer {token}"}

    # Prepare test data
    payload_data = {"text": "This is some test text"}

    # Send the POST request
    response = test_client.post("/get_embeddings", json=payload_data, headers=headers)
    response_data = response.json()

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response content (assuming expected structure)
    response_data = response.json()
    assert "user_id" in response_data
    assert "embeddings" in response_data
    assert "message" in response_data
    assert response_data["message"] == "Text embeddings"