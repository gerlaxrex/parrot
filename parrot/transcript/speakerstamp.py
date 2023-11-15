from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True, slots=True)
class Speakerstamp:
    """A speakerstamp reports the speaker and the timestamp of the utterance"""

    speaker: str
    timestamp: timedelta
