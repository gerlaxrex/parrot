"""A utility module for handling silence in audio signals"""
# pylint: disable=C0103
from collections import deque

import pydub
from pydub.silence import detect_nonsilent


def split_on_silence(
    segment: pydub.AudioSegment,
    min_silence_len: int = 1000,
    silence_thresh: int = -16,
    padding: int | bool = 100,
    seek_step: int = 1,
) -> tuple[list[pydub.AudioSegment], list[tuple[float, float]]]:
    """It splits an audio segment on silent sections

    Parameters
    ----------
    segment
        The original audio segment
    min_silence_len
        The minimum length of silence in millis for a split
    silence_thresh
        The silence threshold in dBFS
    padding
        The amount of silence chunks should be padded with

        It keeps the audio segment from sounding like it is abruptly cut off
    seek_step
        The step size in millis for iterating over the segment

    Returns
    -------
        The audio chunks and split ranges in millis
    """
    T = len(segment)

    if isinstance(padding, bool):
        padding = T if padding else 0

    R = deque(detect_nonsilent(segment, min_silence_len, silence_thresh, seek_step))

    Q = []

    while R:
        x = R.popleft()

        s = max(x[0] - padding, 0)
        e = min(x[1] + padding, T)

        x = (s, e)

        # It merges overlapping padding
        if Q and s < Q[-1][1]:
            s = Q[-1][0]
            e = max(Q[-1][1], e)

            Q[-1] = (s, e)

            continue

        Q.append(x)

    return [segment[s:e] for s, e in Q], Q
