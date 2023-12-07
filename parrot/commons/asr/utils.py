import numpy as np
from pydub import AudioSegment


def format_audio_onto_ndarray(audio_segment: AudioSegment) -> np.ndarray:
    return (
        np.frombuffer(audio_segment.raw_data, np.int16).flatten().astype(np.float32)
        / 32768.0
    )
