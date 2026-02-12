#!/bin/bash
# Stop Phase 1 services (API + UI)
set -e

echo "Stopping Ollama Multi-LLM Server (Phase 1)..."
docker compose down

echo "Stopped API + UI containers."

