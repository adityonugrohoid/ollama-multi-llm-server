from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.models import router as models_router
from routes.inference import router as inference_router
from routes.health import router as health_router

app = FastAPI(
    title="Multi-LLM Inference Server",
    description="Multi-model inference API powered by Ollama",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(models_router)
app.include_router(inference_router)
app.include_router(health_router)


@app.get("/")
async def root():
    return {
        "service": "Multi-LLM Inference Server",
        "docs": "/docs",
        "health": "/health",
    }
