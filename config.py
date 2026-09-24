from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


def _positive_int(name: str, default: int) -> int:
    raw = os.getenv(name, str(default))
    try:
        value = int(raw)
    except ValueError as exc:
        raise RuntimeError(f"{name} debe ser un número entero positivo.") from exc
    if value <= 0:
        raise RuntimeError(f"{name} debe ser mayor que 0.")
    return value


@dataclass(frozen=True)
class Config:
    openai_api_key: str
    llm_model: str = "gpt-5.6"
    stt_model: str = "base"
    sample_rate: int = 16000
    channels: int = 1
    record_seconds: int = 6

    @classmethod
    def from_env(cls) -> "Config":
        key = os.getenv("OPENAI_API_KEY", "").strip()
        if not key:
            raise RuntimeError(
                "Falta OPENAI_API_KEY. Configúrala en PowerShell o en un archivo .env."
            )
        return cls(
            openai_api_key=key,
            llm_model=os.getenv("JARVIS_LLM_MODEL", "gpt-5.6").strip(),
            stt_model=os.getenv("JARVIS_STT_MODEL", "base").strip(),
            sample_rate=_positive_int("JARVIS_SAMPLE_RATE", 16000),
            channels=_positive_int("JARVIS_CHANNELS", 1),
            record_seconds=_positive_int("JARVIS_RECORD_SECONDS", 6),
        )
