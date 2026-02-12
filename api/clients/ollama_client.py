import httpx
import time
import os


AVAILABLE_MODELS = [
    {"id": "llama3.2:3b", "size": "2.0GB", "tier": "Meta"},
    {"id": "qwen2.5:3b", "size": "1.9GB", "tier": "Alibaba"},
    {"id": "phi3.5:3.8b", "size": "2.2GB", "tier": "Microsoft"},
]

VALID_MODEL_IDS = {m["id"] for m in AVAILABLE_MODELS}


class OllamaClient:
    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.current_model = os.getenv("DEFAULT_MODEL", "llama3.2:3b")

    def get_current_model(self) -> str:
        return self.current_model

    def set_current_model(self, model_id: str):
        self.current_model = model_id

    async def generate(
        self,
        prompt: str,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> dict:
        model = model or self.current_model
        start = time.time()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.host}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                    },
                    "stream": False,
                },
                timeout=120.0,
            )
            response.raise_for_status()

        result = response.json()
        latency_ms = int((time.time() - start) * 1000)

        return {
            "response": result["response"],
            "model": model,
            "latency_ms": latency_ms,
            "tokens_generated": result.get("eval_count", 0),
        }

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.host}/api/tags", timeout=5.0)
                return resp.status_code == 200
        except httpx.HTTPError:
            return False


# Singleton instance
ollama = OllamaClient()
