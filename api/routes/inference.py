from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from clients.ollama_client import ollama, VALID_MODEL_IDS

router = APIRouter(prefix="/inference", tags=["inference"])


class GenerateRequest(BaseModel):
    prompt: str
    model: str | None = None
    temperature: float = 0.7
    max_tokens: int = 512


class GenerateResponse(BaseModel):
    response: str
    model: str
    latency_ms: int
    tokens_generated: int


@router.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """Generate text using the current or specified model."""
    if request.model and request.model not in VALID_MODEL_IDS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model. Choose from: {sorted(VALID_MODEL_IDS)}",
        )

    try:
        result = await ollama.generate(
            prompt=request.prompt,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Ollama error: {e}")

    return GenerateResponse(**result)


@router.post("/compare")
async def compare_models(
    prompt: str = Query(..., description="The prompt to send to each model"),
    models: list[str] = Query(
        default=["llama3.2:3b", "qwen2.5:3b"],
        description="Models to compare",
    ),
):
    """Compare responses from multiple models side-by-side."""
    for m in models:
        if m not in VALID_MODEL_IDS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid model '{m}'. Choose from: {sorted(VALID_MODEL_IDS)}",
            )

    results = []
    for model in models:
        try:
            result = await ollama.generate(prompt=prompt, model=model)
            results.append(result)
        except Exception as e:
            results.append({
                "response": f"Error: {e}",
                "model": model,
                "latency_ms": 0,
                "tokens_generated": 0,
            })

    return {"prompt": prompt, "comparisons": results}
