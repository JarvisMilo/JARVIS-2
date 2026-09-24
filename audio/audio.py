import time
import numpy as np
import sounddevice as sd


class AudioRecorder:
    def __init__(self, sample_rate: int = 16000, channels: int = 1):
        self.sample_rate = sample_rate
        self.channels = channels

    def record(self, seconds: int) -> np.ndarray:
        frames = int(seconds * self.sample_rate)
        print(f"🎙️ Grabando durante {seconds}s...")
        started = time.perf_counter()
        audio = sd.rec(
            frames,
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32",
        )
        sd.wait()
        elapsed = time.perf_counter() - started
        print(f"✓ Captura terminada ({elapsed:.2f}s)")
        return audio.reshape(-1)
