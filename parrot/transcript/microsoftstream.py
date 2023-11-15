"""A utility module for handling Microsoft Stream transcripts"""

import re

from parrot.transcript.speakerstamp import Speakerstamp


try:
    import docx
    from pytimeparse2 import parse

    has_docx = True
except ImportError:
    has_docx = False


def speakerstamps(filepath: str) -> list[Speakerstamp]:
    """It converts a Microsoft Stream .docx transcript to speakerstamps

    Any speakerstamp reports the speaker and the timestamp of the utterance
    """
    if not has_docx:
        raise ValueError(
            "No python-docx module found. Have you tried running parrot[docx]?"
        )

    document = docx.Document(filepath)

    P = re.compile(
        r"\n(?P<speaker>[A-Za-z]+(?:\s+[A-Za-z]+)*)\s+(?P<timestamp>[0-9]+:[0-9]+)\n"
    )

    X = []

    for x in document.paragraphs:
        match = re.search(P, x.text)

        if not match:
            continue

        speaker = match.group("speaker")

        timestamp = match.group("timestamp")
        timestamp = parse(timestamp, as_timedelta=True)

        x = Speakerstamp(speaker, timestamp)

        X.append(x)

    return X
