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
        started = time.perf_counter()
        response = self.client.responses.create(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=user_text,
        )
        text = response.output_text.strip()
        print(f"🧠 LLM ({time.perf_counter() - started:.2f}s)")
        return text
