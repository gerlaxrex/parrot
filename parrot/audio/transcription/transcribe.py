import io
import logging
import os.path
from typing import Union, List, Any

from openai import AsyncClient
from pydub import AudioSegment

from tqdm.asyncio import tqdm_asyncio as tqdm

from parrot.audio.extraction.audio_extraction import (
    get_audio_from_video,
    split_audio_for_size,
)

aclient = AsyncClient()

__logger = logging.getLogger(__file__)


async def transcribe_audio(audio: AudioSegment) -> str:
    buffer = io.BytesIO()
    buffer.name = "cucciolo.mp3"
    audio.export(buffer, format="mp3")
    transcription = await aclient.audio.transcriptions.create(
        file=buffer, model="whisper-1", language="it"
    )
    return transcription.text


async def transcribe_video_source(
    filepath: Union[str, os.PathLike], max_time: int = 3 * 60
) -> List[Any]:
    __logger.info(f"Transcribing video source at {filepath}")
    audio = get_audio_from_video(video_filename=filepath)
    audio_chunks = split_audio_for_size(audio, max_time=max_time)

    transcription_chunks = await tqdm.gather(
        *[transcribe_audio(ac) for ac in audio_chunks]
    )

    return transcription_chunks


