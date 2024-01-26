import asyncio
import logging
from typing import Any, List, Optional

import tiktoken
from openai import AsyncClient
from tqdm.asyncio import tqdm_asyncio as tqdm

from parrot1.commons.generative.base import BaseLLMModel


class OpenaiGPTModel(BaseLLMModel):
    def __init__(self, model_size_or_type: str, client_or_model: Optional[Any] = None):
        super().__init__(model_size_or_type, client_or_model)
        self.__logger = logging.getLogger("OpenaiGPT")
        if self.client_or_model is None:
            self.client_or_model = AsyncClient()

    async def agenerate(self, prompt: str, **kwargs) -> str:
        response = await self.client_or_model.completions.create(
            model=self.model_size_or_type, prompt=prompt, **kwargs
        )
        return response.choices[0].text

    def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("Not implemented. Use the agenerate method instead.")

    def __call__(self, prompt: str, **kwargs) -> str:
        return asyncio.run(asyncio.create_task(self.agenerate(prompt, **kwargs)))

    async def generate_from_prompts(self, prompts: List[str], **kwargs) -> List[str]:
        responses = await tqdm.gather(
            *[
                self.client_or_model.completions.create(
                    model=self.model_size_or_type, prompt=prompt, **kwargs
                )
                for prompt in prompts
            ]
        )

        return [response.choices[0].text for response in responses]

    async def count_tokens(self, prompt: str, **kwargs) -> int:
        encoding = tiktoken.encoding_for_model(self.model_size_or_type)
        return len(encoding.encode(prompt))
