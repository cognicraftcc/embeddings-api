from jose import jwt
from datetime import datetime, timedelta, timezone
import os
from embedding_api import get_jwt_token, verify_jwt_token
from fastapi import HTTPException, Request
from starlette.types import Scope
from starlette.datastructures import Headers
import pytest

# Test verify_jwt_token given expected input args
def test_get_jwt_token_success():
    token = "TEST_TOKEN"

    # Mock request
    # https://stackoverflow.com/a/67513232
    mock_header = Headers({"Authorization": f"Bearer {token}"})
    r = Request(scope={
        "type": "http",
        "headers": mock_header.raw
        })
    
    r_token = get_jwt_token(r)
    
    assert r_token == "TEST_TOKEN"

# Test verify_jwt_token given no auth token header
def test_get_jwt_token_no_auth_header():

    # Mock request
    # https://stackoverflow.com/a/67513232
    mock_header = Headers({"TEST": f"HEADER"})
    r = Request(scope={
        "type": "http",
        "headers": mock_header.raw
        })

    with pytest.raises(HTTPException) as e_info:
        get_jwt_token(r)
    
    assert e_info.value.status_code == 401
    assert e_info.value.detail == 'Not authenticated'

# Test verify_jwt_token given invalid auth header format
def test_get_jwt_token_invalid_auth_header():

    # Mock request
    # https://stackoverflow.com/a/67513232
    mock_header = Headers({"Authorization": f"TEST"})
    r = Request(scope={
        "type": "http",
        "headers": mock_header.raw
        })

    with pytest.raises(HTTPException) as e_info:
        get_jwt_token(r)
    
    assert e_info.value.status_code == 401
    assert e_info.value.detail == 'Not authenticated'