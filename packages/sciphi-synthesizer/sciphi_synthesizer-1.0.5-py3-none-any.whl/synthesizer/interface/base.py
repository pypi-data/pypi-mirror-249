"""A module which defines interface abstractions for various LLM providers."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type

from synthesizer.core import LLMProviderName, RAGProviderName
from synthesizer.llm import LLM, GenerationConfig, LLMConfig


@dataclass
class LLMProviderConfig:
    """A dataclass to hold the configuration for a provider."""

    provider_name: LLMProviderName
    llm_class: Type["LLMInterface"]


class LLMInterface(ABC):
    """An abstract class to provide a common interface for LLM providers."""

    provider_name: LLMProviderName

    def __init__(
        self,
        config: LLMConfig,
    ) -> None:
        self.config = config

    @property
    @abstractmethod
    def model(self) -> LLM:
        """Property to get the instance of LLM."""
        pass

    @abstractmethod
    def get_completion(
        self, prompt: str, generation_config: GenerationConfig
    ) -> str:
        """Abstract method to get a completion from the provider."""
        pass

    def get_batch_completion(
        self, prompts: List[str], generation_config: GenerationConfig
    ) -> List[str]:
        """Get a batch of completions from the provider."""
        return [
            self.get_completion(prompt, generation_config)
            for prompt in prompts
        ]

    @abstractmethod
    def get_chat_completion(
        self, conversation: List[dict], generation_config: GenerationConfig
    ) -> str:
        """Abstract method to get a completion from the provider."""
        pass


@dataclass
class RAGProviderConfig(ABC):
    """An abstract class to hold the configuration for a RAG provider."""

    provider_name: RAGProviderName
    max_context: int = 2_048
    api_base: Optional[str] = None
    api_key: Optional[str] = None


@dataclass
class RagResult(ABC):
    context: str
    meta_data: Optional[List[Dict[str, str]]] = None


class RAGInterface(ABC):
    """An abstract class to provide a common interface for RAG providers."""

    provider_name: RAGProviderName
    RAG_DISABLED_MESSAGE: str = "Not Available."

    def __init__(
        self,
        config: RAGProviderConfig,
    ) -> None:
        self.config = config

    @abstractmethod
    def get_rag_context(self, query: str) -> RagResult:
        """Get the context for a given query."""
        pass


class InterfaceManager(ABC):
    """An abstract class to provide a common interface for interface managers."""

    provider_registry: dict[Any, Any] = {}

    @staticmethod
    @abstractmethod
    def register_provider(
        provider: Type[Any],
    ) -> Type[Any]:
        """Registers a provider with the interface manager."""
        pass

    @staticmethod
    @abstractmethod
    def get_interface(
        provider_name: Any,
        config: Any,
        *args,
        **kwargs,
    ) -> Any:
        """Gets an interface based on the given provider and model name."""
        pass

    @staticmethod
    @abstractmethod
    def get_interface_from_args(
        provider_name: Any,
        *args,
        **kwargs,
    ) -> Any:
        """Gets an interface based on the given provider and model name."""
        pass
