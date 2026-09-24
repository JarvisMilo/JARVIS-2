import time

import numpy as np
import sounddevice as sd


class AudioRecorder:
    def __init__(self, sample_rate: int = 16000, channels: int = 1):
        if sample_rate <= 0:
            raise ValueError("sample_rate debe ser mayor que 0.")
        if channels <= 0:
            raise ValueError("channels debe ser mayor que 0.")
        self.sample_rate = sample_rate
        self.channels = channels

    def record(self, seconds: int) -> np.ndarray:
        if seconds <= 0:
            raise ValueError("seconds debe ser mayor que 0.")

        frames = int(seconds * self.sample_rate)
        print(f"🎙️ Grabando durante {seconds}s...")
        started = time.perf_counter()

        try:
            audio = sd.rec(
                frames,
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32",
            )
            sd.wait()
        except Exception as exc:
            raise RuntimeError(
                "No se pudo capturar el micrófono. Revisa el dispositivo de entrada "
                "y los permisos de Windows."
            ) from exc

        elapsed = time.perf_counter() - started
        print(f"✓ Captura terminada ({elapsed:.2f}s)")
        return audio.reshape(-1)
