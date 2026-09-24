import pytest

from config import Config


def test_config_requires_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        Config.from_env()


def test_config_reads_environment(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("JARVIS_LLM_MODEL", "test-model")
    monkeypatch.setenv("JARVIS_TTS_VOICE", "test-voice")

    config = Config.from_env()

    assert config.openai_api_key == "test-key"
    assert config.llm_model == "test-model"
    assert config.tts_voice == "test-voice"


def test_config_rejects_invalid_sample_rate(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("JARVIS_SAMPLE_RATE", "0")

    with pytest.raises(RuntimeError):
        Config.from_env()


def test_config_rejects_empty_model(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("JARVIS_LLM_MODEL", "")

    with pytest.raises(RuntimeError):
        Config.from_env()
