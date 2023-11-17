"""A utility module for handling timestamps"""
from dataclasses import dataclass
from datetime import timedelta


@dataclass(slots=True)
class Speakerstamp:
    """A speakerstamp reports the speaker and the timestamp of the utterance"""

    speaker: str
    timestamp: tuple[timedelta, timedelta]
