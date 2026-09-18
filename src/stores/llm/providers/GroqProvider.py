from ..LLMInterface import LLMInterface
from ..LLMEnums import GroqEnums

from groq import Groq
import logging


class GroqProvider(LLMInterface):

    def __init__(
        self,
        api_key: str,
        default_input_max_characters: int = 1000,
        default_generation_max_output_tokens: int = 2048,
        default_generation_temperature: float = 0.1
    ):

        self.api_key = api_key

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.enums = GroqEnums

        self.client = Groq(api_key=self.api_key)

        self.logger = logging.getLogger(__name__)

    # --------------------------------------------------
    # Model Configuration
    # --------------------------------------------------

    def set_generation_model(self, model_id: str):

        self.generation_model_id = model_id

    def set_embedding_model(
        self,
        model_id: str,
        embedding_size: int
    ):

        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    # --------------------------------------------------
    # Text Processing
    # --------------------------------------------------

    def process_text(self, text: str):

        return text.strip()

    # --------------------------------------------------
    # Generation
    # --------------------------------------------------

    def generate_text(
        self,
        prompt: str,
        chat_history: list = None,
        max_output_tokens: int = None,
        temperature: float = None
    ):

        if not self.client:

            self.logger.error(
                "Groq client was not initialized."
            )

            return None

        if not self.generation_model_id:

            self.logger.error(
                "Generation model was not set."
            )

            return None

        if chat_history is None:

            chat_history = []

        max_output_tokens = (
            max_output_tokens
            if max_output_tokens is not None
            else self.default_generation_max_output_tokens
        )

        temperature = (
            temperature
            if temperature is not None
            else self.default_generation_temperature
        )

        chat_history.append(
            self.construct_prompt(
                prompt=prompt,
                role=GroqEnums.USER.value
            )
        )

        try:

            response = self.client.chat.completions.create(
                model=self.generation_model_id,
                messages=chat_history,
                max_completion_tokens=max_output_tokens,
                temperature=temperature,
                include_reasoning=False,
                reasoning_effort="low"
            )

            print("\n" + "=" * 60)
            print("PROMPT SENT TO GROQ")
            print("=" * 60)
            print(chat_history[-1]["content"])
            print("=" * 60)

            if not response or not response.choices:

                self.logger.error(
                    "Error while generating text with Groq."
                )

                return None

            choice = response.choices[0]
            message = choice.message
            content = getattr(message, "content", None)

            if not content:

                print("finish_reason:", getattr(choice, "finish_reason", None))
                print("message:", message)
                print("content:", repr(content))
                print(
                    "reasoning:",
                    repr(getattr(message, "reasoning", None))
                )
                print("usage:", getattr(response, "usage", None))

                self.logger.error(
                    "Error while generating text with Groq."
                )

                return None

            return content

        except Exception as e:

            self.logger.exception(
                f"Error while generating text with Groq: {e}"
            )
            return None

    # --------------------------------------------------
    # Embedding
    # --------------------------------------------------

    def embed_text(
        self,
        text: str,
        document_type: str = None
    ):

        self.logger.warning(
            "GroqProvider does not support embeddings."
        )

        return None

    def embed_texts(
        self,
        texts: list[str],
        document_type: str = None
    ):

        return [
            self.embed_text(
                text=text,
                document_type=document_type
            )
            for text in texts
        ]

    # --------------------------------------------------
    # Prompt Construction
    # --------------------------------------------------

    def construct_prompt(
        self,
        prompt: str,
        role: str
    ):

        return {
            "role": role,
            "content": self.process_text(prompt)
        }