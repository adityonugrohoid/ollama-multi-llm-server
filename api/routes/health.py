from fastapi import APIRouter

from clients.ollama_client import ollama

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """Check API and Ollama connectivity."""
    ollama_ok = await ollama.health_check()
    return {
        "status": "healthy" if ollama_ok else "degraded",
        "api": "ok",
        "ollama": "connected" if ollama_ok else "unreachable",
        "current_model": ollama.get_current_model(),
    }
