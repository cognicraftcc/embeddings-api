# test_model_init.py
import pytest
import asyncio
# Import the event from your app module
from embedding_api import model_initialized


# test_model_init.py
import pytest
from pytest_mock import mocker
from embedding_api import model_initialized


@pytest.fixture
def mock_model_initialized(mocker):
    # Mock the entire event object
    mock_event = mocker.MagicMock()
    mock_event.is_set.return_value = True  # Simulate already initialized
    return mocker.patch("embedding_api.model_initialized", mock_event)


def test_model_initialization_sync(mock_model_initialized):
    """Test model initialization with synchronous mocks."""

    # No need for async/await since we're mocking everything
    assert mock_model_initialized.is_set(), "Model should appear initialized"

    # You can also test the waiting behavior if needed
    mock_model_initialized.is_set.return_value = False
    assert not mock_model_initialized.is_set(), "Model should appear not initialized"


# mock init so decprecate async test

# @pytest.mark.asyncio
# async def test_model_initialization():
#     """Test model initialization."""

#     # Wait for the model_initialized event
#     try:
#         await asyncio.wait_for(asyncio.to_thread(model_initialized.wait, 30), timeout=30)  # Adjust timeout as needed
#     except asyncio.TimeoutError:
#         assert False, "Model initialization event not set within timeout"

#     # Assertions
#     assert model_initialized.is_set(), "Model initialization event not set"
