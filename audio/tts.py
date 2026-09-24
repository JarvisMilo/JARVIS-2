import time
import pyttsx3


class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 175)

    def speak(self, text: str) -> None:
        started = time.perf_counter()
        print(f"🔊 JARVIS: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        print(f"✓ TTS ({time.perf_counter() - started:.2f}s)")
