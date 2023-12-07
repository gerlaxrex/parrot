import logging
import os.path
from typing import Any, List, Optional

import huggingface_hub
from llama_cpp import Llama
from tqdm import tqdm

from parrot import PARROT_CACHED_MODELS
from parrot.commons.generative.base import BaseLLMModel


class LlamaCppModel(BaseLLMModel):
    def __init__(
        self,
        repo_id: str,
        model_size_or_type: str,
        client_or_model: Optional[Any] = None,
    ):
        super().__init__(model_size_or_type, client_or_model)
        self.__logger = logging.getLogger("LlamaCpp")
        self.repo_id = repo_id
        if self.client_or_model is None:
            # Download from hugging face
            model_path = PARROT_CACHED_MODELS / self.model_size_or_type
            if not os.path.exists(model_path):
                huggingface_hub.hf_hub_download(
                    repo_id=self.repo_id,
                    filename=self.model_size_or_type,
                    local_dir=PARROT_CACHED_MODELS,
                    local_dir_use_symlinks=False,
                )
            self.__logger.info(f"Loading model from {model_path}")
            self.client_or_model = Llama(
                model_path=model_path.as_posix(), verbose=False, n_ctx=4096
            )

    async def agenerate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("Not implemented. Use the generate method instead.")

    def generate(self, prompt: str, **kwargs) -> str:
        return self.client_or_model.create_completion(prompt=prompt, **kwargs)[
            "choices"
        ][0]["text"]

    def __call__(self, prompt: str, **kwargs) -> str:
        return self.generate(prompt, **kwargs)

    def generate_from_prompts(self, prompts: List[str], **kwargs) -> List[str]:
        return [self.generate(prompt, **kwargs) for prompt in tqdm(prompts)]