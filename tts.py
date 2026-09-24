from __future__ import annotations

import subprocess
import sys
import time
import wave
from pathlib import Path
from typing import Protocol

import sounddevice as sd


class TTSProvider(Protocol):
    def speak(self, text: str) -> None:
        ...


class PiperTTS:
    def __init__(self, voice: str, voices_dir: str) -> None:
        self.voice = voice
        self.voices_dir = Path(voices_dir)
        self.voices_dir.mkdir(parents=True, exist_ok=True)
        self.model_path = self.voices_dir / f"{voice}.onnx"

        print(f"⏳ Preparando TTS local: Piper/{voice}...")
        self._ensure_voice()
        try:
            from piper import PiperVoice
            self.voice_model = PiperVoice.load(str(self.model_path))
        except Exception as exc:
            raise RuntimeError(
                f"No se pudo cargar la voz de Piper '{voice}'. "
                "Comprueba que el modelo .onnx y su .onnx.json existan en "
                f"'{self.voices_dir}'."
            ) from exc
        print("✓ TTS listo")

    def _ensure_voice(self) -> None:
        config_path = self.voices_dir / f"{self.voice}.onnx.json"
        if self.model_path.exists() and config_path.exists():
            return

        print("⬇️ Voz de Piper no encontrada. Descargándola una sola vez...")
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "piper.download_voices",
                    "--data-dir",
                    str(self.voices_dir),
                    self.voice,
                ],
                check=True,
            )
        except Exception as exc:
            raise RuntimeError(
                "No se pudo descargar la voz de Piper. Revisa tu conexión a Internet."
            ) from exc

        if not self.model_path.exists() or not config_path.exists():
            raise RuntimeError(
                f"Piper terminó la descarga, pero no apareció la voz '{self.voice}'."
            )

    def speak(self, text: str) -> None:
        if not text.strip():
            return

        started = time.perf_counter()
        print(f"🔊 JARVIS: {text}")

        output = self.voices_dir / "_jarvis_tts.wav"
        try:
            with wave.open(str(output), "wb") as wav_file:
                self.voice_model.synthesize_wav(text, wav_file)

            with wave.open(str(output), "rb") as wav_file:
                sample_rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                frames = wav_file.readframes(wav_file.getnframes())

            import numpy as np

            dtype = {1: np.int8, 2: np.int16, 4: np.int32}.get(sample_width)
            if dtype is None:
                raise RuntimeError(f"Formato WAV no compatible: {sample_width} bytes por muestra.")

            audio = np.frombuffer(frames, dtype=dtype)
            if channels > 1:
                audio = audio.reshape(-1, channels)

            sd.play(audio, samplerate=sample_rate)
            sd.wait()
        except Exception as exc:
            raise RuntimeError("Falló la síntesis o reproducción TTS con Piper.") from exc
        finally:
            try:
                output.unlink(missing_ok=True)
            except OSError:
                pass

        print(f"✓ TTS ({time.perf_counter() - started:.2f}s)")
