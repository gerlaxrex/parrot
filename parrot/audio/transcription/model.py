from typing import List

from pydantic import BaseModel


class TimedPiece(BaseModel):
    transcript: str
    start: int
    end: int


class TimedTranscription(BaseModel):
    text: str
    pieces: List[TimedPiece]
