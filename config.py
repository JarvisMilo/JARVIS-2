from dataclasses import dataclass
import os


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
        key = os.getenv("OPENAI_API_KEY", "")
        if not key:
            raise RuntimeError(
                "Falta OPENAI_API_KEY. Configúrala en PowerShell antes de ejecutar JARVIS."
            )
        return cls(
            openai_api_key=key,
            llm_model=os.getenv("JARVIS_LLM_MODEL", "gpt-5.6"),
            stt_model=os.getenv("JARVIS_STT_MODEL", "base"),
            sample_rate=int(os.getenv("JARVIS_SAMPLE_RATE", "16000")),
            record_seconds=int(os.getenv("JARVIS_RECORD_SECONDS", "6")),
        )
