from unittest.mock import AsyncMock, patch


# ── Model endpoints ──────────────────────────────────────────────────────────


def test_list_models(client):
    resp = client.get("/models/")
    assert resp.status_code == 200
    data = resp.json()
    assert "models" in data
    assert "current" in data
    assert len(data["models"]) == 6


def test_get_current_model(client):
    resp = client.get("/models/current")
    assert resp.status_code == 200
    assert resp.json()["model"] == "llama3.2:3b"


def test_switch_model(client):
    resp = client.post("/models/switch", json={"model_id": "mistral:7b"})
    assert resp.status_code == 200
    assert resp.json()["model"] == "mistral:7b"

    resp = client.get("/models/current")
    assert resp.json()["model"] == "mistral:7b"


def test_switch_to_invalid_model(client):
    resp = client.post("/models/switch", json={"model_id": "nonexistent:1b"})
    assert resp.status_code == 400


# ── Inference endpoints ──────────────────────────────────────────────────────


MOCK_GENERATE_RETURN = {
    "response": "A neural network is a computational model.",
    "model": "llama3.2:3b",
    "latency_ms": 150,
    "tokens_generated": 12,
}


@patch(
    "routes.inference.ollama.generate",
    new_callable=AsyncMock,
    return_value=MOCK_GENERATE_RETURN,
)
def test_generate(mock_gen, client):
    resp = client.post(
        "/inference/generate",
        json={"prompt": "Hello", "max_tokens": 64},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["response"] == MOCK_GENERATE_RETURN["response"]
    assert data["model"] == "llama3.2:3b"
    assert "latency_ms" in data
    mock_gen.assert_called_once()


def test_generate_invalid_model(client):
    resp = client.post(
        "/inference/generate",
        json={"prompt": "Hello", "model": "bad:model"},
    )
    assert resp.status_code == 400


@patch(
    "routes.inference.ollama.generate",
    new_callable=AsyncMock,
    return_value=MOCK_GENERATE_RETURN,
)
def test_compare_models(mock_gen, client):
    resp = client.post(
        "/inference/compare",
        params={"prompt": "Hello", "models": ["llama3.2:3b", "mistral:7b"]},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["prompt"] == "Hello"
    assert len(data["comparisons"]) == 2
    assert mock_gen.call_count == 2


def test_compare_invalid_model(client):
    resp = client.post(
        "/inference/compare",
        params={"prompt": "Hello", "models": ["llama3.2:3b", "fake:1b"]},
    )
    assert resp.status_code == 400


# ── Health endpoint ──────────────────────────────────────────────────────────


@patch(
    "routes.health.ollama.health_check",
    new_callable=AsyncMock,
    return_value=True,
)
def test_health_ok(mock_hc, client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert data["ollama"] == "connected"


@patch(
    "routes.health.ollama.health_check",
    new_callable=AsyncMock,
    return_value=False,
)
def test_health_degraded(mock_hc, client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "degraded"


# ── Root endpoint ────────────────────────────────────────────────────────────


def test_root(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "service" in resp.json()
