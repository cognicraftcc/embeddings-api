#test_get_embeddings.py

from jose import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
import pytest

# Unit testing get_embeddings with mostly faked inputs
# Test standard function call
def test_get_embeddings_success(test_client, fake_model):

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

# Test when text value is an empty string
def test_get_embeddings_no_text_error(test_client, fake_model):

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
    payload_data = {"text": ""}


    # Send the POST request
    response = test_client.post("/get_embeddings", json=payload_data, headers=headers)
    response_data = response.json()
    print("Test Error Exception Details:")
    print(response_data["detail"])


    # TODO: Remove after solving exception issue FF-65
    if response_data["detail"] == "Unexpected error: 400: No text data received":
        pytest.xfail("Known issue with exception handling FF-65")
    
    # Assert the response status code
    assert response.status_code == 400
    # Assert error details
    assert response_data["detail"] == "No text data received"

# Test when no 'text' key in payload
def test_get_embeddings_no_text_key_error(test_client, fake_model):

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
    payload_data = {}


    # Send the POST request
    response = test_client.post("/get_embeddings", json=payload_data, headers=headers)
    response_data = response.json()
    print("Test Error Exception Details:")
    print(response_data["detail"])


    # TODO: Remove after solving exception issue FF-65
    if response_data["detail"] == "Unexpected error: 400: No text data received":
        pytest.xfail("Known issue with exception handling FF-65")
    
    # Assert the response status code
    assert response.status_code == 400
    # Assert error details
    assert response_data["detail"] == "No text data received"


# Test exception thrown in case of ConnectionError
def test_get_embeddings_connection_error(test_client, fake_model, monkeypatch):

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


    #Replace model.encode with fake function to throw exception
    def fake_encode(text):
        raise ConnectionError
    monkeypatch.setattr('embedding_api.model.encode', fake_encode)


    # Send the POST request
    response = test_client.post("/get_embeddings", json=payload_data, headers=headers)
    response_data = response.json()


    # Assert the response status code
    assert response.status_code == 500
    # Assert error details
    assert response_data["detail"] == "ConnectionError/BrokenPipeError: Unable to send response: "


# Test exception thrown in case of BrokenPipeError
def test_get_embeddings_broken_pipe(test_client, fake_model, monkeypatch):

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


    #Replace model.encode with fake function to throw exception
    def fake_encode(text):
        raise BrokenPipeError
    monkeypatch.setattr('embedding_api.model.encode', fake_encode)


    # Send the POST request
    response = test_client.post("/get_embeddings", json=payload_data, headers=headers)
    response_data = response.json()


    # Assert the response status code
    assert response.status_code == 500
    # Assert error details
    assert response_data["detail"] == "ConnectionError/BrokenPipeError: Unable to send response: "
