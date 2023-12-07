import logging
import importlib.util
import os
from typing import List, Union

from parrot import PARROT_CACHED_MODELS
from parrot.audio.transcription.model import TimedTranscription

from parrot.commons.generative.base import BaseLLMModel
from parrot.commons.generative.llamacpp import LlamaCppModel
from parrot.commons.generative.openai_gpt import OpenaiGPTModel
from parrot.config.config import PARROT_CONFIGS

from parrot.recap.tasks import ParrotTask, resolve_prompt_from_task

imp_llama_cpp = importlib.util.find_spec(name="llama_cpp")

has_llama_cpp = imp_llama_cpp is not None

__logger = logging.getLogger(__name__)


def get_client(use_llama_cpp: bool = False) -> Union[BaseLLMModel, None]:
    if not use_llama_cpp:
        if os.getenv("OPENAI_API_KEY") is not None:
            return OpenaiGPTModel(
                model_size_or_type=PARROT_CONFIGS.generative_models.openai.model_type_or_size
            )
        else:
            __logger.error(
                "OPENAI_API_KEY is not set but you're trying to use the OpenAI Apis."
            )
            return None
    else:
        if has_llama_cpp:
            cache_root = PARROT_CACHED_MODELS
            __logger.info("Using llama_cpp model")
            __logger.info(f"Using cache folder at {cache_root.as_posix()}")
            os.makedirs(cache_root, exist_ok=True)
            return LlamaCppModel(
                repo_id=PARROT_CONFIGS.generative_models.llama_cpp.repo_id,
                model_size_or_type=PARROT_CONFIGS.generative_models.llama_cpp.model_type_or_size,
            )
        else:
            __logger.error(
                "The llama-cpp-python package was not installed. Try fixing it by doing pip install parrot[llama-cpp]."
            )
            return None


def generate_chunks(client: BaseLLMModel, texts: List[str]) -> List[str]:
    prompt = resolve_prompt_from_task(
        ParrotTask.CHUNK, language=PARROT_CONFIGS.language
    )

    summaries = client.generate_from_prompts(
        prompts=[prompt.format(text=text) for text in texts],
        max_tokens=400,
        temperature=0.15,
    )

    return summaries


def generate_final_result(
    texts: List[TimedTranscription],
    task: ParrotTask = ParrotTask.RECAP,
    use_llama_cpp: bool = False,
) -> str:
    prompt = resolve_prompt_from_task(task, language=PARROT_CONFIGS.language)
    client = get_client(use_llama_cpp)

    summaries = generate_chunks(client, [t.text for t in texts])

    recap = client(
        prompt=prompt.format(texts="\n\n".join(summaries)),
        max_tokens=750,
        temperature=0.25,
    )

    return recap
