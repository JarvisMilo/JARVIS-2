import pytest

from config import Config


def test_config_reads_local_defaults(monkeypatch):
    monkeypatch.delenv("JARVIS_LLM_MODEL", raising=False)
    monkeypatch.delenv("OLLAMA_HOST", raising=False)

    config = Config.from_env()

    assert config.llm_model == "llama3.2"
    assert config.ollama_host == "http://127.0.0.1:11434"


def test_config_reads_environment(monkeypatch):
    monkeypatch.setenv("JARVIS_LLM_MODEL", "test-model")
    monkeypatch.setenv("OLLAMA_HOST", "http://localhost:9999")

    config = Config.from_env()

    assert config.llm_model == "test-model"
    assert config.ollama_host == "http://localhost:9999"


def test_config_rejects_empty_model(monkeypatch):
    monkeypatch.setenv("JARVIS_LLM_MODEL", "")

    with pytest.raises(RuntimeError):
        Config.from_env()


def test_config_rejects_empty_ollama_host(monkeypatch):
    monkeypatch.setenv("OLLAMA_HOST", "")

    with pytest.raises(RuntimeError):
        Config.from_env()


def test_config_rejects_invalid_sample_rate(monkeypatch):
    monkeypatch.setenv("JARVIS_SAMPLE_RATE", "0")

    with pytest.raises(RuntimeError):
        Config.from_env()


def test_config_rejects_invalid_channels(monkeypatch):
    monkeypatch.setenv("JARVIS_CHANNELS", "0")

    with pytest.raises(RuntimeError):
        Config.from_env()


def test_config_rejects_invalid_max_record_seconds(monkeypatch):
    monkeypatch.setenv("JARVIS_MAX_RECORD_SECONDS", "-1")

    with pytest.raises(RuntimeError):
        Config.from_env()
