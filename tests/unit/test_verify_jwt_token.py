from jose import jwt
from datetime import datetime, timedelta, timezone
from embedding_api import verify_jwt_token
from fastapi import HTTPException
import pytest

# Test verify_jwt_token given expected input args
def test_verify_jwt_token_success():

    # JWT token config
    SECRET_KEY = 'TEST_KEY'
    ALGORITHM = 'HS256'

    token_data={"sub": "12345"}
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    token_data.update({"exp": expire})
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    payload = verify_jwt_token(token, SECRET_KEY)
    
    assert payload["sub"] == "12345"

# Test verify_jwt_token given expired token
def test_verify_jwt_token_expired_token():

    # JWT token config
    SECRET_KEY = 'TEST_KEY'
    ALGORITHM = 'HS256'

    token_data={"sub": "12345"}
    expire = datetime.now(timezone.utc) + timedelta(minutes=-15)
    token_data.update({"exp": expire})
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as e_info:
        verify_jwt_token(token, SECRET_KEY)
    
    assert e_info.value.status_code == 400
    assert e_info.value.detail == 'Invalid token: Signature has expired.'


# Test verify_jwt_token given a token encrypted with wrong key
def test_verify_jwt_token_invalid_token():

    # JWT token config
    SECRET_KEY = 'TEST_KEY'
    ALGORITHM = 'HS256'

    token_data={"sub": "12345"}
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    token_data.update({"exp": expire})
    token = jwt.encode(token_data, "BAD_KEY", algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as e_info:
        verify_jwt_token(token, SECRET_KEY)
    
    assert e_info.value.status_code == 400
    assert e_info.value.detail == 'Invalid token: Signature verification failed.'