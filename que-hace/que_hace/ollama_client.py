"""Cliente Ollama para extracción inteligente de shortcuts."""

import os
from typing import Optional

import aiohttp


class OllamaClient:
    """Cliente async para Ollama API con soporte para servidor remoto."""

    DEFAULT_HOST = "192.168.1.80"  # Servidor remoto .80
    DEFAULT_PORT = 11434
    DEFAULT_MODEL = "qwen2.5-coder:14b"

    def __init__(
        self,
        base_url: Optional[str] = None,
        model: str = DEFAULT_MODEL,
    ):
        """Inicializa el cliente Ollama.

        Args:
            base_url: URL base del servidor Ollama. Por defecto usa OLLAMA_HOST env var
                     o el servidor remoto 192.168.1.80:11434
            model: Modelo a usar para generación
        """
        if base_url:
            self.base_url = base_url
        else:
            # Prioridad: env var > default remoto
            host = os.getenv("OLLAMA_HOST", self.DEFAULT_HOST)
            port = os.getenv("OLLAMA_PORT", str(self.DEFAULT_PORT))
            self.base_url = f"http://{host}:{port}"

        self.model = model

    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 100,
    ) -> str:
        """Genera texto usando Ollama.

        Args:
            prompt: Prompt para el modelo
            system: Mensaje de sistema opcional
            temperature: Temperatura para generación (menor = más determinista)
            max_tokens: Máximo de tokens a generar

        Returns:
            Texto generado
        """
        payload: dict = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        if system:
            payload["system"] = system

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as response:
                if response.status != 200:
                    raise Exception(f"Ollama error {response.status}: {await response.text()}")

                data = await response.json()
                return data.get("response", "").strip()

    async def is_available(self) -> bool:
        """Verifica si Ollama está disponible."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/tags",
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as response:
                    return response.status == 200
        except Exception:
            return False

    async def list_models(self) -> list[str]:
        """Lista modelos disponibles en el servidor."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/tags") as response:
                    if response.status == 200:
                        data = await response.json()
                        return [model["name"] for model in data.get("models", [])]
        except Exception:
            pass
        return []
