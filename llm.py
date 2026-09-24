from __future__ import annotations

import time
from typing import Protocol

from ollama import Client


SYSTEM_PROMPT = """Eres JARVIS, un asistente personal de IA.
Responde en español salvo que el usuario pida otro idioma.
Sé claro, breve y útil.
En el Nivel 1 solo conversas: no tienes herramientas para ejecutar acciones del sistema.
"""


class LLMProvider(Protocol):
    def respond(self, user_text: str) -> str:
        ...


class OllamaLLM:
    def __init__(self, host: str, model: str) -> None:
        self.client = Client(host=host)
        self.model = model

    def respond(self, user_text: str) -> str:
        if not user_text.strip():
            raise ValueError("No se puede enviar una entrada vacía al LLM.")

        started = time.perf_counter()
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_text},
                ],
            )
            text = response.message.content.strip()
        except Exception as exc:
            raise RuntimeError(
                f"Falló Ollama con el modelo '{self.model}'. "
                "Comprueba que Ollama esté instalado, ejecutándose y que el modelo exista."
            ) from exc

        if not text:
            raise RuntimeError("Ollama devolvió una respuesta vacía.")

        print(f"🧠 LLM local/Ollama ({time.perf_counter() - started:.2f}s)")
        return text
