from config import Config
from audio.audio import AudioRecorder
from audio.stt import SpeechToText
from audio.tts import TextToSpeech
from brain.llm import Brain


def main() -> None:
    print("🔎 Comprobando configuración...")
    config = Config.from_env()
    print(f"✓ Modelo LLM: {config.llm_model}")
    print(f"✓ STT local: faster-whisper/{config.stt_model}")
    print(f"✓ Audio: {config.sample_rate} Hz, {config.channels} canal(es)")

    recorder = AudioRecorder(
        sample_rate=config.sample_rate,
        channels=config.channels,
    )
    stt = SpeechToText(config.stt_model)
    brain = Brain(config.openai_api_key, config.llm_model)
    tts = TextToSpeech()

    print("\n=== JARVIS 2 · NIVEL 1 ===")
    print("Push-to-talk: pulsa Enter para hablar.")
    print("Escribe 'salir' y pulsa Enter para terminar.\n")

    while True:
        command = input(">>> ")
        if command.strip().lower() in {"salir", "exit", "quit"}:
            print("JARVIS apagado.")
            break

        audio = recorder.record(config.record_seconds)
        user_text = stt.transcribe(audio)

        if not user_text:
            print("No detecté voz. Intenta de nuevo.")
            continue

        answer = brain.respond(user_text)
        tts.speak(answer)


if __name__ == "__main__":
    main()
