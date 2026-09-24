import time

from audio.audio import AudioRecorder
from audio.stt import SpeechToText
from audio.tts import TextToSpeech
from brain.llm import Brain
from config import Config


def main() -> None:
    print("🔎 Comprobando configuración...")

    try:
        config = Config.from_env()
        print(f"✓ Modelo LLM: {config.llm_model}")
        print(f"✓ STT local: faster-whisper/{config.stt_model}")
        print(f"✓ Audio: {config.sample_rate} Hz, {config.channels} canal(es)")
        print(f"✓ Duración de captura: {config.record_seconds}s")

        recorder = AudioRecorder(config.sample_rate, config.channels)
        stt = SpeechToText(config.stt_model)
        brain = Brain(config.openai_api_key, config.llm_model)
        tts = TextToSpeech()
    except Exception as exc:
        print(f"❌ Error de inicialización: {exc}")
        return

    print("\n=== JARVIS 2 · NIVEL 1 · VOZ ===")
    print("Estado: LISTO")
    print("Pulsa Enter para grabar.")
    print("Escribe 'salir' y pulsa Enter para terminar.\n")

    while True:
        command = input("JARVIS > ")
        if command.strip().lower() in {"salir", "exit", "quit"}:
            print("JARVIS apagado.")
            break

        started = time.perf_counter()
        try:
            print("▶ Estado: ESCUCHANDO")
            audio = recorder.record(config.record_seconds)

            print("▶ Estado: TRANSCRIBIENDO")
            user_text = stt.transcribe(audio)
            if not user_text:
                print("⚠️ No detecté voz. Intenta de nuevo.\n")
                continue

            print("▶ Estado: PENSANDO")
            answer = brain.respond(user_text)

            print("▶ Estado: HABLANDO")
            tts.speak(answer)

            print(f"✓ Ciclo completo ({time.perf_counter() - started:.2f}s)\n")
        except KeyboardInterrupt:
            print("\nJARVIS detenido.")
            break
        except Exception as exc:
            print(f"❌ Error en el ciclo: {exc}")
            print("El sistema sigue disponible. Intenta nuevamente.\n")


if __name__ == "__main__":
    main()
