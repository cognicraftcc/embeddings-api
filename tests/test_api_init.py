#test_api_init.py
from embedding_api import  model_initialized

import pytest
import asyncio

# Assuming model_initialized is an asyncio.Event
model_initialized = asyncio.Event()

# Simulated function to initialize the model
async def initialize_model():
    await asyncio.sleep(1)  # Simulate some async initialization process
    model_initialized.set()

@pytest.mark.asyncio
async def test_model_initialization():
    """Test model initialization."""

    # Simulate initializing the model
    asyncio.create_task(initialize_model())

    # Wait for the model_initialized event
    try:
        await asyncio.wait_for(model_initialized.wait(), timeout=30)  # Adjust timeout as needed
    except asyncio.TimeoutError:
        assert False, "Model initialization event not set within timeout"

    # Assertions
    assert model_initialized.is_set(), "Model initialization event not set"
