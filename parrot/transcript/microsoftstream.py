"""A utility module for handling Microsoft Stream transcripts"""

import re
from concurrent import futures

from parrot.transcript.speakerstamp import Speakerstamp


try:
    import docx
    from pytimeparse2 import disable_dateutil, parse

    has_docx = True
except ImportError:
    has_docx = False


def speakerstamps(filepath: str, max_workers: int = 1) -> list[Speakerstamp]:
    """It converts a Microsoft Stream .docx transcript to speakerstamps"""
    if not has_docx:
        message = "parrot[docx] must be installed"
        raise ValueError(message)

    disable_dateutil()  # It ensures timedeltas over relativedeltas

    document = docx.Document(filepath)

    P = re.compile(
        r"\n(?P<speaker>[A-Za-z]+(?:\s+[A-Za-z]+)*)\s+(?P<timestamp>[0-9]+:[0-9]+)\n"
    )

    def inner(x: docx.text.paragraph.Paragraph) -> Speakerstamp | None:
        match = re.search(P, x.text)

        if not match: return None

        speaker = match.group("speaker")

        timestamp = match.group("timestamp")
        timestamp = parse(timestamp, as_timedelta=True)

        return Speakerstamp(speaker, timestamp)

    with futures.ThreadPoolExecutor(max_workers) as executor:
        X = [executor.map(inner, x) for x in document.paragraphs]
        X = [x for x in X if x is not None]

    return X
