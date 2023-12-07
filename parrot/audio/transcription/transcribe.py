import importlib.util
import logging
import os.path
from typing import Union, List

from parrot.audio.transcription.model import TimedTranscription

from parrot import PARROT_CACHED_MODELS
from parrot.commons.asr.base import BaseASRModel
from parrot.commons.asr.faster_whisper import FasterWhisper
from parrot.commons.asr.openai_whisper import OpenaiWhisper
from parrot.config.config import PARROT_CONFIGS

from parrot.audio.extraction.audio_extraction import (
    get_audio_from_video,
    split_audio_for_size,
)

__logger = logging.getLogger(__file__)

s = importlib.util.find_spec(name="faster_whisper")

has_faster_whisper = s is not None


def get_client(use_faster_whisper: bool = False) -> Union[BaseASRModel, None]:
    if os.getenv("OPENAI_API_KEY") is None and not use_faster_whisper:
        __logger.warning(
            "OPENAI_API_KEY is not set but you're trying to use the OpenAI Apis."
            "The model choice will fallback to faster-whisper automatically."
        )
    if os.getenv("OPENAI_API_KEY") is not None and not use_faster_whisper:
        return OpenaiWhisper(
            model_size_or_type=PARROT_CONFIGS.asr_models.whisper.model_type_or_size,
            language=PARROT_CONFIGS.language,
            temperature=PARROT_CONFIGS.asr_models.whisper.temperature,
            prompt=PARROT_CONFIGS.asr_models.whisper.prompt,
        )
    elif has_faster_whisper:
        cache_root = PARROT_CACHED_MODELS
        __logger.info(f"Using cache folder at {cache_root.as_posix()}")
        os.makedirs(cache_root, exist_ok=True)
        return FasterWhisper(
            model_size_or_type=PARROT_CONFIGS.asr_models.faster_whisper.model_type_or_size,
            language=PARROT_CONFIGS.language,
            prompt=PARROT_CONFIGS.asr_models.faster_whisper.prompt,
            temperature=PARROT_CONFIGS.asr_models.faster_whisper.temperature,
            beam_size=PARROT_CONFIGS.asr_models.faster_whisper.beam_size,
            download_root=cache_root,
        )
    else:
        __logger.error(
            "The faster-whisper package was not installed. Try fixing it by doing pip install parrot[faster-whisper]."
            "If not present, you cannot use a free ASR model such Whisper. "
            "Please set the OPENAI_API_KEY environment variable."
        )
        return None


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

    if client is not None:
        transcription_chunks = client.transcribe_chunks(audio_chunks, vtt)
    else:
        raise RuntimeError("No available method for ASR is possible.")

    return transcription_chunks
