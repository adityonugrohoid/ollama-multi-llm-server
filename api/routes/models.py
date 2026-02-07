from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from clients.ollama_client import ollama, AVAILABLE_MODELS, VALID_MODEL_IDS

router = APIRouter(prefix="/models", tags=["models"])


class ModelSelection(BaseModel):
    model_id: str


@router.get("/")
async def list_models():
    """List all available models with current selection."""
    return {
        "models": AVAILABLE_MODELS,
        "current": ollama.get_current_model(),
    }


@router.post("/switch")
async def switch_model(selection: ModelSelection):
    """Switch the active model for inference."""
    if selection.model_id not in VALID_MODEL_IDS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model. Choose from: {sorted(VALID_MODEL_IDS)}",
        )
    ollama.set_current_model(selection.model_id)
    return {"status": "switched", "model": selection.model_id}


@router.get("/current")
async def get_current_model():
    """Get the currently active model."""
    return {"model": ollama.get_current_model()}
