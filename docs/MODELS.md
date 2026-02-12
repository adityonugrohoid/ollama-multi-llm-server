# Model Guide

## Available Models

All models are 3B-class Q4_K_M quantized for consistent performance and minimal resource usage.

| Family    | Model         | Parameters | Size   | Best For                              |
|-----------|--------------|-----------|--------|---------------------------------------|
| Meta      | `llama3.2:3b`  | 3B        | 2.0 GB | General-purpose inference (default)   |
| Alibaba   | `qwen2.5:3b`   | 3B        | 1.9 GB | Multilingual, structured output       |
| Microsoft | `phi3.5:3.8b`  | 3.8B      | 2.2 GB | Reasoning, code generation            |

## Choosing a Model

| Scenario              | Recommended    | Why                                  |
|-----------------------|----------------|--------------------------------------|
| Development / testing | `llama3.2:3b`  | Default -- general-purpose, reliable |
| Multilingual tasks    | `qwen2.5:3b`   | Strongest multilingual support       |
| Code generation       | `phi3.5:3.8b`  | Strong at structured/code tasks      |
| Benchmarking          | All three      | Compare across model families        |

## Hardware Requirements

All models run via Ollama and benefit from GPU acceleration but fall back to CPU.

| Setup | RAM Needed | Models You Can Run |
|-------|------------|-------------------|
| 8 GB RAM (CPU) | 8 GB | All three models |
| GPU with 8 GB VRAM | 8 GB | All three models (fast) |
