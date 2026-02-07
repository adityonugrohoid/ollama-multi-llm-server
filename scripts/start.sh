#!/bin/bash
# Start the full stack: Ollama + API + UI

set -e

echo "Starting Multi-LLM Inference Server..."
docker compose up -d --build

echo ""
echo "Waiting for services to be ready..."
sleep 5

echo ""
echo "Services:"
echo "  API:      http://localhost:8080"
echo "  API docs: http://localhost:8080/docs"
echo "  UI:       http://localhost:8501"
echo "  Ollama:   http://localhost:11434"
echo ""
echo "To pull models: ./scripts/pull_models.sh"
echo "To view logs:   docker compose logs -f"
echo "To stop:        docker compose down"
