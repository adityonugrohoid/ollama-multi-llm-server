#!/bin/bash
# Restart Phase 1 services (API + UI)
set -e

echo "Restarting Ollama Multi-LLM Server (Phase 1)..."
docker compose down
docker compose up -d --build

echo "Restarted API + UI containers."

