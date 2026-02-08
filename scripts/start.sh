#!/bin/bash
# Start the API + UI stack (requires Phase 0 Ollama runtime)
set -e

# Check Ollama is running
if ! docker ps --format '{{.Names}}' | grep -q '^ollama$'; then
    echo "ERROR: Ollama container not running."
    echo "Start Phase 0 first: cd ~/projects/ollama-runtime && ./scripts/start.sh"
    exit 1
fi

echo "Using existing Ollama container (Phase 0)..."
echo "Starting Multi-LLM Inference Server..."
docker compose up -d --build

echo ""
echo "Waiting for services to be ready..."
sleep 5

echo ""
echo "Services:"
echo "  API:      http://localhost:1080"
echo "  API docs: http://localhost:1080/docs"
echo "  UI:       http://localhost:1501"
echo "  Ollama:   http://localhost:11434  (from Phase 0: ollama-runtime)"
echo ""
echo "To pull models: ./scripts/pull_models.sh"
echo "To view logs:   docker compose logs -f"
echo "To stop:        docker compose down"
echo "See PORT_CONFIGURATION.md for port details."
