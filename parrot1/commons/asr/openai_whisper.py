import asyncio
import io
import logging
from typing import Optional, Any, List

from pydub import AudioSegment

from tqdm.asyncio import tqdm_asyncio

from parrot1.audio.transcription.model import TimedTranscription
from parrot1.commons.asr.base import BaseASRModel
from parrot1.commons.models.language import Language
from openai import AsyncClient


class OpenaiWhisper(BaseASRModel):
    def __init__(
        self,
        model_size_or_type: str,
        language: Optional[Language] = Language.IT,
        prompt: Optional[str] = "",
        temperature: Optional[float] = 0.2,
        beam_size: Optional[int] = 5,
        client_or_model: Any = None,
    ):
        super().__init__(
            model_size_or_type,
            language,
            prompt,
            temperature,
            beam_size,
            client_or_model,
        )
        if self.client_or_model is None:
            self.client_or_model = AsyncClient()
        self.__logger = logging.getLogger("OpenaiWhisper")

    async def atranscribe(
        self, audio: AudioSegment, vtt: bool = False
    ) -> TimedTranscription:
        buffer = io.BytesIO()
        buffer.name = "cucciolo.mp3"
        audio.export(buffer, format="mp3")
        self.__logger.debug("Started transcription")
        transcription = await self.client_or_model.audio.transcriptions.create(
            file=buffer,
            model=self.model_size_or_type,
            language=self.language,
            prompt=self.prompt,
            temperature=self.temperature,
        )
        self.__logger.debug("Finished transcription")
        return TimedTranscription(text=transcription.text, pieces=[])

    def transcribe(self, audio: AudioSegment, vtt: bool = False):
        pass

    def transcribe_chunks(
        self, audio_chunks: List[AudioSegment], vtt: bool = False
    ) -> List[TimedTranscription]:
        transcription_chunks = asyncio.run(
            tqdm_asyncio.gather(*[self.atranscribe(ac, vtt=vtt) for ac in audio_chunks])
        )

        return transcription_chunks
