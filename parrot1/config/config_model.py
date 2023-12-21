from typing import Optional

from pydantic import BaseModel

from parrot1.commons.models.language import Language


class ASRConfigs(BaseModel):
    type_or_size: str
    temperature: Optional[float] = 0.1
    prompt: Optional[str] = ""
    beam_size: Optional[int] = 5

    class Config:
        frozen: True


class LLMConfigs(BaseModel):
    type_or_size: str
    repo_id: Optional[str] = None

    class Config:
        frozen: True


class LLMParamsConfigs(BaseModel):
    temperature: Optional[float] = 0.2
    top_k: Optional[int] = 40
    top_p: Optional[float] = 0.9
    max_tokens: Optional[int] = 4096

    class Config:
        frozen: True


class ASRModelsConfigs(BaseModel):
    whisper: ASRConfigs
    faster_whisper: ASRConfigs

    class Config:
        frozen: True


class GenerativeModelsConfigs(BaseModel):
    chunking: Optional[LLMParamsConfigs]
    text_generation: Optional[LLMParamsConfigs]
    openai: LLMConfigs
    llama_cpp: LLMConfigs

    class Config:
        frozen: True


class ParrotConfigs(BaseModel):
    language: Optional[Language] = Language.IT.value
    asr_models: ASRModelsConfigs
    generative_models: GenerativeModelsConfigs

    class Config:
        frozen: True
