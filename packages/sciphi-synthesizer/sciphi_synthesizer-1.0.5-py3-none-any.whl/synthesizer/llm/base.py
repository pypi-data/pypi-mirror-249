"""Base classes for language model providers."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, fields
from typing import Optional

from synthesizer.core import LLMProviderName


@dataclass
class LLMConfig(ABC):
    provider_name: LLMProviderName

    version: str = "0.1.0"

    @classmethod
    def create(cls, **kwargs):
        valid_keys = {f.name for f in fields(cls)}
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_keys}
        return cls(**filtered_kwargs)


@dataclass
class GenerationConfig(ABC):
    temperature: float = 0.1
    top_p: float = 1.0
    top_k: int = 100
    max_tokens_to_sample: int = 1_024
    model_name: Optional[str] = None
    do_stream: bool = False
    functions: Optional[list[dict]] = None
    skip_special_tokens: bool = False
    stop_token: Optional[str] = None
    num_beams: int = 1
    do_sample: bool = True
    # Additional args to pass to the generation config
    add_generation_kwargs: dict = field(default_factory=dict)


class LLM(ABC):
    """An abstract class to provide a common interface for LLMs."""

    def __init__(
        self,
    ) -> None:
        pass

    @abstractmethod
    def get_chat_completion(
        self, messages: list[dict[str, str]], config: GenerationConfig
    ) -> str:
        """Abstract method to get a chat completion from the provider."""
        pass

    @abstractmethod
    def get_instruct_completion(
        self, instruction: str, config: GenerationConfig
    ) -> str:
        """Abstract method to get an instruction completion from the provider."""
        pass
