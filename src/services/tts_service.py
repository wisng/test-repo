import io
import numpy as np
from typing import Tuple
from f5_tts.api import F5TTS


class TTSService:
    def __init__(self):
        self.f5tts = F5TTS()
        print("Successfully loaded F5TTS model")

    def process_audio(
        self,
        reference_path: str,
        text: str,
        speed: float = 1.0,
        cross_fade: float = 0.15,
        ref_text: str = ""
    ) -> Tuple[int, np.ndarray]:
        """Process TTS request with thread-safe model inference"""
        print("Processing audio...")

        with open(reference_path, "rb") as f:
            audio_bytes = f.read()

        audio_io = io.BytesIO(audio_bytes)
        return self.process_tts_request(
            audio_io,
            text,
            speed=speed,
            cross_fade_duration=cross_fade,
            ref_text=ref_text
        )

    def process_tts_request(
        self,
        audio_io: io.BytesIO,
        text_to_generate: str,
        speed: float = 1.0,
        cross_fade_duration: float = 0.15,
        ref_text: str = ""
    ) -> tuple[int, np.ndarray]:
        try:
            # Process audio directly from memory
            audio_io.seek(0)
            print("Processing TTS request...")
            print("Starting inference...")
            final_wave, final_sample_rate, _ = self.f5tts.infer(
                audio_io,
                ref_text,
                text_to_generate,
                cross_fade_duration=cross_fade_duration,
                speed=speed
            )
            print("Successfully processed TTS request")
            return final_sample_rate, final_wave
        except Exception as e:
            raise RuntimeError(f"Error processing TTS request: {str(e)}")


tts_service = TTSService()
