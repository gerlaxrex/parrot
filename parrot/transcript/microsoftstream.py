"""A utility module for handling Microsoft Stream transcripts"""
# pylint: disable=C0103
import re

from parrot.transcript.timestamp import Speakerstamp, timedelta_to_millis
from parrot.utils.itertools import pairwise


try:
    import docx
    from pytimeparse2 import disable_dateutil, parse

    has_docx = True
except ImportError:
    has_docx = False


def speakerstamps(filepath: str, T: int) -> list[Speakerstamp]:
    """It converts a Microsoft Stream .docx transcript to speakerstamps"""
    if not has_docx:
        message = "parrot[docx] must be installed"
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

    M = M + [(None, T)]
    X = []

    for (speaker, s), (_, e) in pairwise(M):
        x = Speakerstamp(speaker, (s, e))
        X.append(x)

    return X
