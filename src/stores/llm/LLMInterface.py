from abc import ABC, abstractmethod
import json
import logging
from typing import TypeVar

from pydantic import BaseModel, ValidationError


StructuredOutput = TypeVar("StructuredOutput", bound=BaseModel)

class LLMInterface(ABC):

    @abstractmethod
    def set_generation_model(self, model_id: str):#بتجيب ال id بتاع الموديل اللي عايز تستخدمه في توليد النصوص
        pass

    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        pass#بتجيب ال id بتاع الموديل اللي عايز تستخدمه في توليد النصوص وكمان حجم ال embedding اللي عايز تستخدمه

    @abstractmethod
    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None,
                            temperature: float = None):
        pass#بتجيب ال prompt اللي عايز تولد منه النصوص وكمان ال chat_history لو فيه و max_output_tokens لو عايز تحدد عدد الكلمات اللي عايز تولدها و temperature لو عايز تتحكم في تنوع النصوص اللي بتتولد

    def generate_structured(
        self,
        prompt: str,
        response_model: type[StructuredOutput],
        chat_history: list = None,
        max_output_tokens: int = None,
        temperature: float = None,
    ) -> StructuredOutput | None:
        """Generate JSON and validate it against a Pydantic response model.

        This builds on ``generate_text`` so every provider created by the
        existing factory has the same structured-output contract.
        """
        schema = json.dumps(response_model.model_json_schema(), ensure_ascii=False)
        structured_prompt = (
            "Return only a JSON object that validates against this JSON Schema. "
            "Do not use Markdown fences or add explanatory text.\n\n"
            f"JSON Schema:\n{schema}\n\n"
            f"Task:\n{prompt}"
        )

        response = self.generate_text(
            prompt=structured_prompt,
            chat_history=chat_history,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
        )

        if response is None:
            return None

        try:
            return response_model.model_validate_json(response)
        except (ValidationError, ValueError) as error:
            logger = getattr(self, "logger", logging.getLogger(__name__))
            logger.exception(
                "Structured LLM response did not match %s: %s",
                response_model.__name__,
                error,
            )
            return None

    @abstractmethod
    def embed_text(self, text: str, document_type: str = None):
        pass#بتجيب النص اللي عايز تحول ل embedding وكمان نوع ال document لو عايز تحدد نوع ال document اللي بتستخدمه في توليد ال embedding

    @abstractmethod
    def embed_texts(self, texts: list[str], document_type: str = None):
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        pass#بتجيب ال prompt اللي عايز تولد منه النصوص وكمان ال role اللي عايز تحدده في ال chat_history زي user او assistant او system

    def graph_transformer(self, documents):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not support graph extraction."
        )