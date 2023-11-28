import logging
import os
from typing import List, Union

from pydub import AudioSegment
from tqdm import tqdm

from parrot.audio.utils.file_utils import get_extension
from parrot.audio.utils.silence import split_on_silence


__logger = logging.getLogger(__name__)


def get_audio_from_video(video_filename: Union[str, os.PathLike]) -> AudioSegment:
    """
    Takes the audio from the video file
    :param video_filename: (Union[str, os.PathLike]) path to the video
    :return: (io.BytesIO) Audio bytes
    """
    audio = AudioSegment.from_file(video_filename, format=get_extension(video_filename))
    return audio


def split_audio_for_size(audio: AudioSegment, max_time: int = 60) -> List[AudioSegment]:
    """
    Splits the video in chunks, in order to retrieve the audio and feed it to OpenAI Whisper.
    :param max_time: The maximum time of a chunk. Used as an upper bound for reassembling smaller chunks.
    :param audio: The AudioSegment object to be splitted.
    :return: a List of AudioSegment representing the chunks of the recording.
    """
    max_millis = max_time * 1000
    __logger.debug(f"Using max chunk time {max_millis}")
    # Splits on silence
    audio_chunks, _ = split_on_silence(
        audio, min_silence_len=1000, silence_thresh=-40, padding=100
    )

    # Reassemble the split chunks on the max length defined
    reassembled_chunks = [audio_chunks[0]]
    for chunk in tqdm(audio_chunks[1:]):
        if len(reassembled_chunks[-1]) < max_millis:
            reassembled_chunks[-1] += chunk
        else:
            reassembled_chunks.append(chunk)
    __logger.info(
        f"Finished chunking audio. Obtained {len(reassembled_chunks)} from a recording "
        f"of {len(audio)//1000} seconds"
    )

    return reassembled_chunks
