# Ollama Multi LLM Server

Multi-model inference API and playground powered by [Ollama](https://ollama.com). Serve, switch, compare, and benchmark 6 local LLMs through a unified FastAPI backend and Streamlit UI.

**Part of the [GenAI Portfolio Suite](https://github.com/adityonugrohoid) - Phase 1: Local LLM Serving.**

## Playground UI

**Generate** - Select any model from the dropdown, tune temperature and max tokens, and get responses with latency and token count metadata.

![Generate tab - model selection, parameter tuning, and response metadata](docs/images/multi_llm_playground.png)

**Compare Models** - Send the same prompt to multiple models side-by-side. Responses are displayed in columns for direct quality and speed comparison.

![Compare tab - side-by-side responses from llama3.2:1b, llama3.2:3b, and llama3.1:8b](docs/images/compare_models.png)

**Highlights:**
- **Model switcher** - dropdown with all 6 models (gemma2:2b through llama3.1:8b)
- **Parameter controls** - temperature (0.0-2.0) and max tokens (64-2048) sliders
- **Response metadata** - model name, latency in ms, and token count on every response
- **Multi-model comparison** - select 2+ models and compare outputs in parallel
- **Ollama status** - live connection indicator in the sidebar

## Features

- **Multi-model switching** - hot-swap between 6 models via API
- **Model comparison** - send the same prompt to multiple models side-by-side
- **Tiered model selection** - fast / balanced / quality tiers for different use cases
- **Performance benchmarking** - automated speed & throughput comparison
- **Interactive playground** - Streamlit UI for experimentation

## Architecture

```mermaid
graph LR
    A["Streamlit Playground :8501"] --> B["FastAPI API :8080"] --> C["Ollama :11434"]
```

## Available Models

| Model | Size | Tier | Use Case |
|-------|------|------|----------|
| `gemma2:2b` | 1.6 GB | Fast | Quick responses, simple queries |
| `llama3.2:1b` | 1.3 GB | Fast | Ultra-fast, edge deployment |
| `llama3.2:3b` | 2.0 GB | Balanced | General local inference (default) |
| `phi3:3.8b` | 2.2 GB | Balanced | Reasoning, code tasks |
| `mistral:7b` | 4.4 GB | Quality | Instruction-following |
| `llama3.1:8b` | 4.9 GB | Quality | Best quality, complex tasks |

## Quick Start

### Prerequisites

- Docker & Docker Compose
- NVIDIA GPU + drivers (optional; CPU fallback works)

### Start Services

```bash
./scripts/start.sh            # start Ollama + API + UI
./scripts/pull_models.sh      # download models into Ollama
```

| Service | URL |
|---------|-----|
| API | http://localhost:8080 |
| API Docs (Swagger) | http://localhost:8080/docs |
| Playground UI | http://localhost:8501 |
| Ollama | http://localhost:11434 |

## API Reference

### Models

```bash
# List all models
curl http://localhost:8080/models/

# Get current model
curl http://localhost:8080/models/current

# Switch model
curl -X POST http://localhost:8080/models/switch \
  -H "Content-Type: application/json" \
  -d '{"model_id": "mistral:7b"}'
```

### Inference

```bash
# Generate
curl -X POST http://localhost:8080/inference/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain Docker in one sentence", "max_tokens": 128}'

# Compare models
curl -X POST "http://localhost:8080/inference/compare?prompt=What+is+RAG&models=llama3.2:3b&models=mistral:7b"
```

### Health

```bash
curl http://localhost:8080/health
```

See [docs/API.md](docs/API.md) for the full API reference.

## Benchmarking

```bash
# Benchmark all models
python3 scripts/benchmark.py

# Benchmark specific models
python3 scripts/benchmark.py --models gemma2:2b llama3.2:3b mistral:7b

# Save results to JSON
python3 scripts/benchmark.py --output results.json
```

## Testing

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v
```

## Project Structure

```
ollama-multi-llm-server/
├── api/
│   ├── main.py                 # FastAPI application entry point
│   ├── routes/
│   │   ├── inference.py        # /inference/generate, /inference/compare
│   │   ├── models.py           # /models, /models/switch, /models/current
│   │   └── health.py           # /health
│   └── clients/
│       └── ollama_client.py    # Ollama HTTP wrapper + model registry
├── ui/
│   └── app.py                  # Streamlit model playground
├── scripts/
│   ├── pull_models.sh          # Download all 6 models
│   ├── benchmark.py            # Model speed comparison
│   └── start.sh                # Launch full stack
├── tests/
│   ├── conftest.py
│   └── test_inference.py       # 11 endpoint tests
├── requirements.txt                # All deps (unpinned), used by venv + Docker
├── docs/
│   ├── images/                     # Screenshots
│   ├── API.md
│   └── MODELS.md
├── docker-compose.yaml
└── LICENSE
```

## Tech Stack

- **LLM Runtime**: Ollama
- **Backend**: FastAPI + Python 3.12
- **UI**: Streamlit
- **HTTP Client**: httpx (async)
- **Infrastructure**: Docker Compose

## Author

**Adityo Nugroho** [github.com/adityonugrohoid](https://github.com/adityonugrohoid)

## License

[MIT](LICENSE)
