# Model Guide

## Model Tiers

### Fast Tier (< 1 second response)

| Model | Parameters | Size | Best For |
|-------|-----------|------|----------|
| `gemma2:2b` | 2B | 1.6 GB | Quick responses, simple Q&A, prototyping |
| `llama3.2:1b` | 1B | 1.3 GB | Ultra-fast responses, latency-critical use cases |

### Balanced Tier (1–3 second response)

| Model | Parameters | Size | Best For |
|-------|-----------|------|----------|
| `phi3:3.8b` | 3.8B | 2.2 GB | Reasoning, code generation, structured output |
| `llama3.2:3b` | 3B | 2.0 GB | General-purpose inference |

### Quality Tier (3–10 second response)

| Model | Parameters | Size | Best For |
|-------|-----------|------|----------|
| `mistral:7b` | 7B | 4.4 GB | Instruction-following, nuanced answers |
| `llama3.1:8b` | 8B | 4.9 GB | Highest quality, complex multi-step tasks |

## Choosing a Model

| Scenario | Recommended | Why |
|----------|-------------|-----|
| Development / testing | `gemma2:2b` | Default – fast and light for dev  |
| Demos / presentations | `llama3.1:8b` | Best output quality |
| Benchmarking latency | `gemma2:2b` | Fastest response times |
| Code generation | `phi3:3.8b` | Strong at structured/code tasks |
| General Q&A | `mistral:7b` | Excellent instruction-following |
| Resource-constrained | `llama3.2:1b` | Smallest memory footprint |

## Hardware Requirements

All models run via Ollama and benefit from GPU acceleration but fall back to CPU.

| Setup | RAM Needed | Models You Can Run |
|-------|------------|-------------------|
| 8 GB RAM (CPU) | 8 GB | Fast tier only |
| 16 GB RAM (CPU) | 16 GB | Fast + Balanced tiers |
| GPU with 8 GB VRAM | 8 GB | Fast + Balanced tiers (fast) |
| GPU with 16 GB VRAM | 16 GB | All tiers (recommended) |
