"""Basic tests for API endpoints."""
from unittest.mock import AsyncMock, patch


def test_list_models(client):
    """List models endpoint."""
    resp = client.get("/models/")
    assert resp.status_code == 200
    assert "models" in resp.json()


def test_get_current_model(client):
    """Get current model endpoint."""
    resp = client.get("/models/current")
    assert resp.status_code == 200
    assert "model" in resp.json()


@patch("routes.inference.ollama.generate", new_callable=AsyncMock, return_value={
    "response": "Test response",
    "model": "llama3.2:3b",
    "latency_ms": 150,
    "tokens_generated": 12,
})
def test_generate(mock_gen, client):
    """Generate endpoint."""
    resp = client.post("/inference/generate", json={"prompt": "Hello"})
    assert resp.status_code == 200
    assert "response" in resp.json()


@patch("routes.health.ollama.health_check", new_callable=AsyncMock, return_value=True)
def test_health(mock_hc, client):
    """Health endpoint."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"
