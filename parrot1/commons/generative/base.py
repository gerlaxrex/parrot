from abc import ABC, abstractmethod
from typing import Any, List, Optional


class BaseLLMModel(ABC):
    def __init__(
        self,
        model_size_or_type: str,
        client_or_model: Optional[Any] = None,
    ):
        super().__init__()
        self.model_size_or_type = model_size_or_type
        self.client_or_model = client_or_model

    @abstractmethod
    async def agenerate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("Abstract class. You should reimplement the method.")

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("Abstract class. You should reimplement the method.")

    @abstractmethod
    async def generate_from_prompts(self, prompts: List[str], **kwargs) -> List[str]:
        raise NotImplementedError("Abstract class. You should reimplement the method.")

    @abstractmethod
    def __call__(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("Abstract class. You should reimplement the method.")
