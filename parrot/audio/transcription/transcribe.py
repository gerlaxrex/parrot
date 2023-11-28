import io
import logging
import os.path
from typing import Union, List

from openai import AsyncClient
from pydub import AudioSegment
import numpy as np
from parrot.audio.transcription.model import (
    TimedTranscription,
    TimedPiece,
)

from tqdm.asyncio import tqdm_asyncio as tqdm
from parrot.audio.utils.file_utils import get_model_cache_directory

from parrot.audio.extraction.audio_extraction import (
    get_audio_from_video,
    split_audio_for_size,
)

__logger = logging.getLogger(__file__)

try:
    from faster_whisper import WhisperModel

    has_faster_whisper = True
except Exception:
    has_faster_whisper = False


def get_client(
    use_faster_whisper: bool = False
) -> Union[AsyncClient, WhisperModel, None]:
    if os.getenv("OPENAI_API_KEY") is None and not use_faster_whisper:
        __logger.warning(
            "OPENAI_API_KEY is not set but you're trying to use the OpenAI Apis."
            "The model choice will fallback to faster-whisper automatically."
        )
    if os.getenv("OPENAI_API_KEY") is not None and not use_faster_whisper:
        return AsyncClient()
    elif has_faster_whisper:
        cache_root = get_model_cache_directory()
        __logger.info(f"Saving model at {cache_root.as_posix()}")
        os.makedirs(cache_root, exist_ok=True)
        return WhisperModel(model_size_or_path="small", download_root=cache_root)
    else:
        __logger.error(
            "The faster-whisper package was not installed. Try by doing pip install parrot[faster-whisper]."
            "If not present, you cannot use a free ASR model such Whisper. "
            "Please set the OPENAI_KEY_API environment variable."
        )
        return None


async def atranscribe_audio(
    aclient: AsyncClient, audio: AudioSegment
) -> TimedTranscription:
    buffer = io.BytesIO()
    buffer.name = "cucciolo.mp3"
    audio.export(buffer, format="mp3")
    transcription = await aclient.audio.transcriptions.create(
        file=buffer, model="whisper-1", language="it"
    )
    return TimedTranscription(text=transcription.text, pieces=[])


def transcribe_audio(
    model: WhisperModel, audio: AudioSegment, vtt: bool = False
) -> TimedTranscription:
    def format_audio_onto_ndarray(audio_segment: AudioSegment) -> np.ndarray:
        return (
            np.frombuffer(audio_segment.raw_data, np.int16).flatten().astype(np.float32)
            / 32768.0
        )

    audio_array = format_audio_onto_ndarray(audio)

    segments, _ = model.transcribe(audio_array, language="it", beam_size=5)

    segments = list(segments)

    text = " ".join(s.text for s in segments)
    pieces = []
    if vtt:
        pieces = [
            TimedPiece(transcript=s.text, start=s.start, end=s.end) for s in segments
        ]
    return TimedTranscription(text=text, pieces=pieces)


async def transcribe_video_source(
    filepath: Union[str, os.PathLike],
    max_time: int = 3 * 60,
    transcript: str = None,
    vtt: bool = False,
    use_faster_whisper: bool = False,
) -> List[TimedTranscription]:
    __logger.info(f"Transcribing video source at {filepath}")
    audio = get_audio_from_video(video_filename=filepath)
    audio_chunks = split_audio_for_size(audio, max_time=max_time)

    # Get the right model
    client = get_client(use_faster_whisper)

    if isinstance(client, AsyncClient):
        transcription_chunks = await tqdm.gather(
            *[atranscribe_audio(client, ac) for ac in audio_chunks]
        )
    elif isinstance(client, WhisperModel):
        transcription_chunks = [
            transcribe_audio(client, ac, vtt=vtt) for ac in audio_chunks
        ]
    else:
        raise RuntimeError("No available method for ASR is possible.")

    return transcription_chunks
