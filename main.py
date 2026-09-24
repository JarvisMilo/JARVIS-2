from __future__ import annotations

import time
from enum import Enum

from audio import AudioRecorder
from config import Config
from llm import OpenAIResponsesLLM
from stt import FasterWhisperSTT
from tts import PiperTTS


class State(str, Enum):
    READY = "LISTO"
    LISTENING = "ESCUCHANDO"
    TRANSCRIBING = "TRANSCRIBIENDO"
    THINKING = "PENSANDO"
    SPEAKING = "HABLANDO"
    ERROR = "ERROR"


def set_state(state: State) -> None:
    print(f"▶ Estado: {state.value}")


def main() -> None:
    print("🔎 Comprobando configuración de JARVIS...")

    try:
        config = Config.from_env()
        print(f"✓ Modelo LLM: {config.llm_model}")
        print(f"✓ STT local: faster-whisper/{config.stt_model}")
        print(f"✓ TTS local: Piper/{config.tts_voice}")
        print(f"✓ Audio: {config.sample_rate} Hz, {config.channels} canal(es)")
        print(f"✓ PTT: barra espaciadora, máximo {config.max_record_seconds}s")

        recorder = AudioRecorder(config.sample_rate, config.channels)
        stt = FasterWhisperSTT(config.stt_model)
        brain = OpenAIResponsesLLM(config.openai_api_key, config.llm_model)
        tts = PiperTTS(config.tts_voice, config.voices_dir)
    except Exception as exc:
        print(f"❌ Error de inicialización: {exc}")
        print("JARVIS no se inició porque una dependencia del Nivel 1 no está lista.")
        return

    print("\n=== JARVIS 2 · NIVEL 1 · VOZ ===")
    print("Estado: LISTO")
    print("Mantén ESPACIO para hablar. Suelta ESPACIO para enviar.")
    print("Escribe 'salir' y pulsa Enter para apagar. Ctrl+C también detiene JARVIS.\n")

    while True:
        try:
            command = input("JARVIS > ")
            if command.strip().lower() in {"salir", "exit", "quit"}:
                print("JARVIS apagado.")
                break

            cycle_started = time.perf_counter()

            set_state(State.LISTENING)
            audio = recorder.record_push_to_talk(config.max_record_seconds)

            set_state(State.TRANSCRIBING)
            user_text = stt.transcribe(audio)
            if not user_text:
                set_state(State.READY)
                print("⚠️ No detecté voz. Intenta de nuevo.\n")
                continue

            set_state(State.THINKING)
            answer = brain.respond(user_text)

            set_state(State.SPEAKING)
            tts.speak(answer)

            set_state(State.READY)
            print(f"✓ Ciclo completo ({time.perf_counter() - cycle_started:.2f}s)\n")
        except KeyboardInterrupt:
            print("\n🛑 JARVIS detenido.")
            break
        except Exception as exc:
            set_state(State.ERROR)
            print(f"❌ Error en el ciclo: {exc}")
            print("El sistema sigue disponible. Intenta nuevamente.\n")
            set_state(State.READY)


if __name__ == "__main__":
    main()
