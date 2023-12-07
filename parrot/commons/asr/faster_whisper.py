import logging
import os
from typing import Optional, Any, List

from pydub import AudioSegment
from tqdm import tqdm
from parrot import PARROT_CACHED_MODELS
from parrot.audio.transcription.model import TimedTranscription, TimedPiece
from parrot.commons.asr.base import BaseASRModel
from parrot.commons.asr.utils import format_audio_onto_ndarray
from parrot.commons.models.language import Language

try:
    from faster_whisper import WhisperModel

    has_faster_whisper = True
except ImportError:
    has_faster_whisper = False


class FasterWhisper(BaseASRModel):
    def __init__(
        self,
        model_size_or_type: str,
        language: Optional[Language] = Language.IT,
        prompt: Optional[str] = "",
        temperature: Optional[float] = 0.2,
        beam_size: Optional[int] = 5,
        client_or_model: Any = None,
        download_root: os.PathLike = None,
    ):
        super().__init__(
            model_size_or_type,
            language,
            prompt,
            temperature,
            beam_size,
            client_or_model,
        )
        self.__logger = logging.getLogger("FasterWhisper")
        if self.client_or_model is None:
            if has_faster_whisper:
                self.client_or_model = WhisperModel(
                    model_size_or_path=self.model_size_or_type,
                    download_root=download_root or PARROT_CACHED_MODELS,
                )
            else:
                self.__logger.error(
                    "The faster-whisper package was not installed. Try fixing it by doing pip install parrot[faster-whisper]."
                    "If not present, you cannot use a free ASR model such Whisper. "
                    "Alternatively, set the OPENAI_API_KEY environment variable."
                )

    async def atranscribe(
        self, audio: AudioSegment, vtt: bool = False
    ) -> TimedTranscription:
        pass

    def transcribe(self, audio: AudioSegment, vtt: bool = False) -> TimedTranscription:
        audio_array = format_audio_onto_ndarray(audio)

        segments, _ = self.client_or_model.transcribe(
            audio_array,
            language=self.language,
            beam_size=self.beam_size,
            temperature=self.temperature,
            initial_prompt=self.prompt,
        )

        segments = list(segments)

        text = " ".join(s.text for s in segments)
        pieces = []
        if vtt:
            pieces = [
                TimedPiece(transcript=s.text, start=s.start, end=s.end)
                for s in segments
            ]
        return TimedTranscription(text=text, pieces=pieces)

    def transcribe_chunks(
        self, audio_chunks: List[AudioSegment], vtt: bool = False
    ) -> List[TimedTranscription]:
        transcription_chunks = [
            self.transcribe(ac, vtt=vtt) for ac in tqdm(audio_chunks)
        ]

        return transcription_chunks
