#test_model_init.py
import pytest
import asyncio
from embedding_api import model_initialized  # Import the event from your app module

@pytest.mark.asyncio
async def test_model_initialization():
    """Test model initialization."""

    # Wait for the model_initialized event
    try:
        await asyncio.wait_for(asyncio.to_thread(model_initialized.wait, 30), timeout=30)  # Adjust timeout as needed
    except asyncio.TimeoutError:
        assert False, "Model initialization event not set within timeout"

    # Assertions
    assert model_initialized.is_set(), "Model initialization event not set"

