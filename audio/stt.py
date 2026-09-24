import time
from faster_whisper import WhisperModel


class SpeechToText:
    def __init__(self, model_size: str = "base"):
        print(f"⏳ Cargando STT: faster-whisper/{model_size}...")
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")

    def transcribe(self, audio) -> str:
        started = time.perf_counter()
        segments, _ = self.model.transcribe(audio, language="es", vad_filter=True)
        text = " ".join(segment.text.strip() for segment in segments).strip()
        elapsed = time.perf_counter() - started
        print(f"📝 STT ({elapsed:.2f}s): {text or '[sin texto]'}")
        return text
