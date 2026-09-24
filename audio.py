from __future__ import annotations

import time
from dataclasses import dataclass
from threading import Event, Lock
from typing import Protocol

import numpy as np
import sounddevice as sd
from pynput import keyboard


class AudioProvider(Protocol):
    def record_push_to_talk(self, max_seconds: int) -> np.ndarray:
        ...


@dataclass
class AudioRecorder:
    sample_rate: int = 16000
    channels: int = 1

    def __post_init__(self) -> None:
        if self.sample_rate <= 0:
            raise ValueError("sample_rate debe ser mayor que 0.")
        if self.channels <= 0:
            raise ValueError("channels debe ser mayor que 0.")

    def record_push_to_talk(self, max_seconds: int) -> np.ndarray:
        if max_seconds <= 0:
            raise ValueError("max_seconds debe ser mayor que 0.")

        pressed = Event()
        released = Event()
        lock = Lock()
        chunks: list[np.ndarray] = []
        frames_limit = int(max_seconds * self.sample_rate)
        captured_frames = 0
        started = time.perf_counter()

        def on_press(key: keyboard.Key | keyboard.KeyCode) -> None:
            if key == keyboard.Key.space:
                with lock:
                    if not pressed.is_set():
                        pressed.set()

        def on_release(key: keyboard.Key | keyboard.KeyCode) -> None:
            if key == keyboard.Key.space:
                released.set()

        print("🎙️ Mantén presionada la BARRA ESPACIADORA para hablar.")

        try:
            with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
                pressed.wait()
                print("▶ Estado: ESCUCHANDO")

                def callback(indata, frames, _time, status) -> None:
                    nonlocal captured_frames
                    if status:
                        print(f"⚠️ Audio: {status}", flush=True)
                    remaining = frames_limit - captured_frames
                    if remaining <= 0:
                        released.set()
                        return
                    data = indata[:remaining].copy()
                    chunks.append(data.reshape(-1))
                    captured_frames += len(data)

                with sd.InputStream(
                    samplerate=self.sample_rate,
                    channels=self.channels,
                    dtype="float32",
                    callback=callback,
                    blocksize=0,
                ):
                    while not released.wait(0.05):
                        if captured_frames >= frames_limit:
                            released.set()

                listener.stop()
        except Exception as exc:
            raise RuntimeError(
                "No se pudo capturar el micrófono. Revisa el dispositivo de entrada, "
                "los permisos de Windows y que pynput pueda escuchar el teclado."
            ) from exc

        if not chunks:
            raise RuntimeError("No se capturó audio. Mantén ESPACIO pulsado mientras hablas.")

        audio = np.concatenate(chunks).astype(np.float32, copy=False)
        elapsed = time.perf_counter() - started
        print(f"✓ Captura terminada ({len(audio) / self.sample_rate:.2f}s, {elapsed:.2f}s)")
        return audio
