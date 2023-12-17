from abc import ABC, abstractmethod
from typing import Optional, Any, List

from pydub import AudioSegment

from parrot1.audio.transcription.model import TimedTranscription
from parrot1.commons.models.language import Language


class BaseASRModel(ABC):
    def __init__(
        self,
        model_size_or_type: str,
        language: Optional[Language] = Language.IT,
        prompt: Optional[str] = "",
        temperature: Optional[float] = 0.2,
        beam_size: Optional[int] = 5,
        client_or_model: Any = None,
    ):
        super().__init__()
        self.model_size_or_type = model_size_or_type
        self.language = language
        self.prompt = prompt
        self.temperature = temperature
        self.beam_size = beam_size
        self.client_or_model = client_or_model

    @abstractmethod
    async def atranscribe(
        self, audio: AudioSegment, vtt: bool = False
    ) -> TimedTranscription:
        raise NotImplementedError("Abstract class. You should reimplement the method.")

    @abstractmethod
    def transcribe(self, audio: AudioSegment, vtt: bool = False) -> TimedTranscription:
        raise NotImplementedError("Abstract class. You should reimplement the method.")

    @abstractmethod
    def transcribe_chunks(
        self, audio_chunks: List[AudioSegment], vtt: bool = False
    ) -> List[TimedTranscription]:
        raise NotImplementedError("Abstract class. You should reimplement the method.")
