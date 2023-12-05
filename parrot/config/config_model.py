import enum
from typing import Optional

from pydantic import BaseModel


class Language(str, enum.Enum):
    EN = "en"
    IT = "it"


class ASRConfigs(BaseModel):
    model_type_or_size: str
    temperature: Optional[float] = 0.1
    prompt: Optional[str] = ""
    beam_size: Optional[int] = 5

    class Config:
        frozen: True


class LLMConfigs(BaseModel):
    model_type_or_size: str
    temperature: Optional[float] = 0.2

    class Config:
        frozen: True


class ASRModelsConfigs(BaseModel):
    whisper: ASRConfigs
    faster_whisper: ASRConfigs

    class Config:
        frozen: True


class GenerativeModelsConfigs(BaseModel):
    openai: LLMConfigs

    class Config:
        frozen: True


class ParrotConfigs(BaseModel):
    language: Optional[Language] = Language.IT
    asr_models: ASRModelsConfigs
    generative_models: GenerativeModelsConfigs

    class Config:
        frozen: True
