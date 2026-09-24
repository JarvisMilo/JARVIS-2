from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


def _positive_int(name: str, default: int) -> int:
    raw = os.getenv(name, str(default)).strip()
    try:
        value = int(raw)
    except ValueError as exc:
        raise RuntimeError(f"{name} debe ser un entero positivo.") from exc
    if value <= 0:
        raise RuntimeError(f"{name} debe ser mayor que 0.")
    return value


def _non_empty(name: str, default: str) -> str:
    value = os.getenv(name, default).strip()
    if not value:
        raise RuntimeError(f"{name} no puede estar vacío.")
    return value


@dataclass(frozen=True)
class Config:
    llm_model: str = "llama3.2"
    ollama_host: str = "http://127.0.0.1:11434"
    stt_model: str = "base"
    tts_voice: str = "es_MX-ald-medium"
    voices_dir: str = "voices"
    sample_rate: int = 16000
    channels: int = 1
    max_record_seconds: int = 30

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            llm_model=_non_empty("JARVIS_LLM_MODEL", "llama3.2"),
            ollama_host=_non_empty("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/"),
            stt_model=_non_empty("JARVIS_STT_MODEL", "base"),
            tts_voice=_non_empty("JARVIS_TTS_VOICE", "es_MX-ald-medium"),
            voices_dir=_non_empty("JARVIS_VOICES_DIR", "voices"),
            sample_rate=_positive_int("JARVIS_SAMPLE_RATE", 16000),
            channels=_positive_int("JARVIS_CHANNELS", 1),
            max_record_seconds=_positive_int("JARVIS_MAX_RECORD_SECONDS", 30),
        )
