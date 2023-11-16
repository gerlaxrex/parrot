import os
from typing import List, Union

from pydub import AudioSegment

from parrot.audio.utils.file_utils import get_extension
from parrot.audio.utils.silence import split_on_silence


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
    :param max_time:
    :param audio:
    :return:
    """
    max_millis = max_time * 1000
    # Splits on silence
    audio_chunks, _ = split_on_silence(
        audio, min_silence_len=1000, silence_thresh=-40, padding=100
    )

    # Reassemble the split chunks on the max length defined
    reassembled_chunks = [audio_chunks[0]]
    for chunk in audio_chunks[1:]:
        if len(reassembled_chunks[-1]) < max_millis:
            reassembled_chunks[-1] += chunk
        else:
            reassembled_chunks.append(chunk)

    return reassembled_chunks
