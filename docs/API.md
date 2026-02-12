# API Reference

Base URL: `http://localhost:8080`

Interactive docs: `http://localhost:8080/docs`

## Endpoints

### `GET /`

Root endpoint returning service info.

**Response:**
```json
{
  "service": "Multi-LLM Inference Server",
  "docs": "/docs",
  "health": "/health"
}
```

---

### `GET /health`

Health check for the API and Ollama connectivity.

**Response:**
```json
{
  "status": "healthy",
  "api": "ok",
  "ollama": "connected",
  "current_model": "llama3.2:3b"
}
```

`status` is `"healthy"` when Ollama is reachable, `"degraded"` otherwise.

---

### `GET /models/`

List all available models with the current selection.

**Response:**
```json
{
  "models": [
    {"id": "gemma2:2b", "size": "1.6GB", "tier": "fast"},
    {"id": "llama3.2:1b", "size": "1.3GB", "tier": "fast"},
    {"id": "phi3:3.8b", "size": "2.2GB", "tier": "balanced"},
    {"id": "llama3.2:3b", "size": "2.0GB", "tier": "balanced"},
    {"id": "mistral:7b", "size": "4.4GB", "tier": "quality"},
    {"id": "llama3.1:8b", "size": "4.9GB", "tier": "quality"}
  ],
  "current": "gemma2:2b"
}
```

---

### `GET /models/current`

Get the currently active model.

**Response:**
```json
{"model": "llama3.2:3b"}
```

---

### `POST /models/switch`

Switch the active model.

**Request body:**
```json
{"model_id": "mistral:7b"}
```

**Response:**
```json
{"status": "switched", "model": "mistral:7b"}
```

**Errors:**
- `400` — invalid model ID

---

### `POST /inference/generate`

Generate text using the current or a specified model.

**Request body:**
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `prompt` | string | *required* | Input prompt |
| `model` | string | *current model* | Override model |
| `temperature` | float | 0.7 | Sampling temperature |
| `max_tokens` | int | 512 | Max tokens to generate |

**Response:**
```json
{
  "response": "Generated text...",
  "model": "llama3.2:3b",
  "latency_ms": 1523,
  "tokens_generated": 87
}
```

**Errors:**
- `400` — invalid model ID
- `502` — Ollama unreachable or generation error

---

### `POST /inference/compare`

Compare responses from multiple models on the same prompt.

**Query parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `prompt` | string | *required* | Input prompt |
| `models` | list[string] | `["llama3.2:3b", "mistral:7b"]` | Models to compare |

**Response:**
```json
{
  "prompt": "What is RAG?",
  "comparisons": [
    {
      "response": "RAG is...",
      "model": "llama3.2:3b",
      "latency_ms": 800,
      "tokens_generated": 45
    },
    {
      "response": "RAG stands for...",
      "model": "mistral:7b",
      "latency_ms": 2100,
      "tokens_generated": 92
    }
  ]
}
```

**Errors:**
- `400` — one or more invalid model IDs
