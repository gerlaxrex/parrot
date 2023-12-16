"""A utility module for handling Microsoft Stream transcripts"""
# pylint: disable=C0103
import re
from datetime import timedelta

from parrot1.audio.transcription.model import SpeakerStamp
from parrot1.utils.itertools import pairwise


try:
    import docx
    from pytimeparse2 import disable_dateutil, parse

    has_docx = True
except ImportError:
    has_docx = False


def timedelta_to_millis(x: timedelta) -> int:
    """It converts a timedelta to rounded millis"""
    return round(x.total_seconds() * 1000)


def speakerstamps(filepath: str, T: int) -> list[SpeakerStamp]:
    """It converts a Microsoft Stream .docx transcript to speakerstamps

    Parameters
    ----------
    filepath
        The transcript .docx filepath
    T
        The end of the trascript in millis

    Returns
    -------
        The speakerstamps
    """
    if not has_docx:
        message = "parrot1[docx] must be installed"
        raise ValueError(message)

    disable_dateutil()  # It ensures timedeltas over relativedeltas

    document = docx.Document(filepath)

    P = re.compile(
        r"\n(?P<speaker>[A-Za-z]+(?:\s+[A-Za-z]+)*)\s+(?P<timestamp>[0-9]+:[0-9]+)\n"
    )

    def parsing(x: docx.text.paragraph.Paragraph) -> tuple[str, int] | None:
        match = re.search(P, x.text)

        if not match:
            return None

        speaker = match.group("speaker")

        timestamp = match.group("timestamp")
        timestamp = parse(timestamp, as_timedelta=True)
        timestamp = timedelta_to_millis(timestamp)

        return speaker, timestamp

    M = [parsing(x) for x in document.paragraphs]
    M = [x for x in M if x is not None]

    if T < M[-1][1]:
        message = f"The transcript is longer than {T}"
        raise ValueError(message)

    M = M + [(None, T)]
    X = []

    for (speaker, s), (_, e) in pairwise(M):
        x = SpeakerStamp(transcript="", speaker=speaker, start=s, end=e)
        X.append(x)

    return X
