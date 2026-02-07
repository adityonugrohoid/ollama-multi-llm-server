import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

# Allow imports from the api/ directory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "api"))

from main import app  # noqa: E402


@pytest.fixture()
def client():
    """Provide a TestClient with Ollama calls mocked out."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def _reset_model():
    """Reset the current model before each test."""
    from clients.ollama_client import ollama

    ollama.set_current_model("llama3.2:3b")
    yield
