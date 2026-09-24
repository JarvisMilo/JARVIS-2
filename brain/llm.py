import time

from openai import OpenAI


SYSTEM_PROMPT = """Eres JARVIS, un asistente personal de IA.
Responde en español salvo que el usuario pida otro idioma.
Sé claro, breve y útil.
En este Nivel 1 no tienes herramientas para ejecutar acciones del sistema:
solo puedes conversar.
"""


class Brain:
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def respond(self, user_text: str) -> str:
        if not user_text.strip():
            raise ValueError("No se puede enviar una entrada vacía al LLM.")

        started = time.perf_counter()
        try:
            response = self.client.responses.create(
                model=self.model,
                instructions=SYSTEM_PROMPT,
                input=user_text,
            )
            text = response.output_text.strip()
        except Exception as exc:
            raise RuntimeError(
                "Falló la respuesta del LLM. Revisa la API key, el modelo y la conexión."
            ) from exc

        if not text:
            raise RuntimeError("El LLM devolvió una respuesta vacía.")

        print(f"🧠 LLM ({time.perf_counter() - started:.2f}s)")
        return text
