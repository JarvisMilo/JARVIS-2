import time

import pyttsx3


class TextToSpeech:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 175)
        except Exception as exc:
            raise RuntimeError("No se pudo inicializar el sistema TTS de Windows.") from exc

    def speak(self, text: str) -> None:
        if not text.strip():
            return

        started = time.perf_counter()
        print(f"🔊 JARVIS: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as exc:
            raise RuntimeError("Falló la reproducción de voz.") from exc

        print(f"✓ TTS ({time.perf_counter() - started:.2f}s)")
