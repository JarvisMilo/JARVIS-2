def test_core_modules_import():
    import audio
    import config
    import llm
    import main
    import stt
    import tts


def test_audio_recorder_rejects_invalid_sample_rate():
    from audio import AudioRecorder
    import pytest

    with pytest.raises(ValueError):
        AudioRecorder(sample_rate=0)


def test_audio_recorder_rejects_invalid_channels():
    from audio import AudioRecorder
    import pytest

    with pytest.raises(ValueError):
        AudioRecorder(channels=0)


def test_llm_rejects_empty_input():
    from llm import OllamaLLM
    import pytest

    llm = OllamaLLM.__new__(OllamaLLM)

    with pytest.raises(ValueError):
        llm.respond("   ")


def test_tts_ignores_empty_text():
    from tts import PiperTTS

    tts = PiperTTS.__new__(PiperTTS)
    assert tts.speak("   ") is None
