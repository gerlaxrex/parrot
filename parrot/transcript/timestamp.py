"""A utility module for handling timestamps"""
from dataclasses import dataclass
from datetime import timedelta


def timedelta_to_millis(x: timedelta) -> int:
    """It converts a timedelta to rounded millis"""
    return round(x.total_seconds() * 1000)


@dataclass(slots=True)
class Speakerstamp:
    """A speakerstamp reports the speaker and the timestamp of the utterance"""

    speaker: str
    timestamp: tuple[int, int]
