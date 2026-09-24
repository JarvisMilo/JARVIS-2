from __future__ import annotations

import time
from typing import Protocol

from faster_whisper import WhisperModel


class STTProvider(Protocol):
    def transcribe(self, audio) -> str:
        ...


class FasterWhisperSTT:
    def __init__(self, model_size: str = "base") -> None:
        print(f"⏳ Cargando STT local: faster-whisper/{model_size}...")
        try:
            self.model = WhisperModel(
                model_size,
                device="cpu",
                compute_type="int8",
            )
        except Exception as exc:
            raise RuntimeError(
                "No se pudo cargar faster-whisper. La primera ejecución puede "
                "necesitar descargar el modelo. Revisa conexión y espacio en disco."
            ) from exc
        print("✓ STT listo")

    def transcribe(self, audio) -> str:
        started = time.perf_counter()
        try:
            segments, _ = self.model.transcribe(
                audio,
                language="es",
                vad_filter=True,
            )
            text = " ".join(
                segment.text.strip()
                for segment in segments
                if segment.text.strip()
            ).strip()
        except Exception as exc:
            raise RuntimeError("Falló la transcripción de audio.") from exc

        print(f"📝 STT ({time.perf_counter() - started:.2f}s): {text or '[sin texto]'}")
        return text
