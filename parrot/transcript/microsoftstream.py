"""A utility module for handling Microsoft Stream transcripts"""

import re
from concurrent import futures

from parrot.transcript.timestamp import Speakerstamp
from parrot.utils.itertools import pairwise


try:
    import docx
    from pytimeparse2 import disable_dateutil, parse

    has_docx = True
except ImportError:
    has_docx = False


def speakerstamps(filepath: str, T: int, max_workers: int = 1) -> list[Speakerstamp]:
    """It converts a Microsoft Stream .docx transcript to speakerstamps"""
    if not has_docx:
        message = "parrot[docx] must be installed"
        raise ValueError(message)

    disable_dateutil()  # It ensures timedeltas over relativedeltas

    document = docx.Document(filepath)

    P = re.compile(
        r"\n(?P<speaker>[A-Za-z]+(?:\s+[A-Za-z]+)*)\s+(?P<timestamp>[0-9]+:[0-9]+)\n"
    )

    def inner(x: docx.text.paragraph.Paragraph) -> tuple[str, timedelta] | None:
        match = re.search(P, x.text)

        if not match: return None

        speaker = match.group("speaker")

        timestamp = match.group("timestamp")
        timestamp = parse(timestamp, as_timedelta=True)

        return speaker, timestamp

    with futures.ThreadPoolExecutor(max_workers) as executor:
        M = [executor.map(inner, x) for x in document.paragraphs]
        M = [x for x in M if x is not None]

    M = M + [(None, T)]
    X = []

    for (speaker, s), (_, e) in pairwise(M):
        x = Speakerstamp(speaker, (s, e))
        X.append(x)

    return X
