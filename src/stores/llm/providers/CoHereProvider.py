from ..LLMInterface import LLMInterface
from ..LLMEnums import CoHereEnums, DocumentTypeEnum

import cohere
import logging


class CoHereProvider(LLMInterface):

    def __init__(
        self,
        api_key: str,
        default_input_max_characters: int = 1000,
        default_generation_max_output_tokens: int = 1000,
        default_generation_temperature: float = 0.1
    ):

        self.api_key = api_key

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = (
            default_generation_max_output_tokens
        )
        self.default_generation_temperature = (
            default_generation_temperature
        )

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.enums = CoHereEnums

        self.client = cohere.Client(
            api_key=self.api_key
        )

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

        return text[:self.default_input_max_characters].strip()

    # --------------------------------------------------
    # Text Generation
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
                "Cohere client was not initialized."
            )

            return None

        if not self.generation_model_id:

            self.logger.error(
                "Generation model for Cohere was not set."
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

        try:

            response = self.client.chat(
                model=self.generation_model_id,
                chat_history=chat_history,
                message=self.process_text(prompt),
                temperature=temperature,
                max_tokens=max_output_tokens
            )

            if not response or not response.text:

                self.logger.error(
                    "Error while generating text with Cohere."
                )

                return None

            return response.text

        except Exception as e:

            self.logger.exception(
                f"Cohere generation error: {e}"
            )

            return None

    # --------------------------------------------------
    # Embedding - Single Text
    # --------------------------------------------------

    def embed_text(
        self,
        text: str,
        document_type: str = None
    ):

        embeddings = self.embed_texts(
            texts=[text],
            document_type=document_type
        )

        if not embeddings:

            return None

        return embeddings[0]

    # --------------------------------------------------
    # Embedding - Multiple Texts
    # --------------------------------------------------

    def embed_texts(
        self,
        texts: list[str],
        document_type: str = None
    ):

        if not self.client:

            self.logger.error(
                "Cohere client was not initialized."
            )

            return None

        if not self.embedding_model_id:

            self.logger.error(
                "Embedding model for Cohere was not set."
            )

            return None

        input_type = CoHereEnums.DOCUMENT.value

        if document_type in (
            DocumentTypeEnum.QUERY,
            DocumentTypeEnum.QUERY.value
        ):

            input_type = CoHereEnums.QUERY.value

        processed_texts = [
            self.process_text(text or "") or " "
            for text in texts
        ]

        if not processed_texts:

            return []

        embeddings = []

        batch_size = 96

        try:

            for batch_start in range(
                0,
                len(processed_texts),
                batch_size
            ):

                batch = processed_texts[
                    batch_start:batch_start + batch_size
                ]

                response = self.client.embed(
                    model=self.embedding_model_id,
                    texts=batch,
                    input_type=input_type,
                    embedding_types=["float"]
                )

                if (
                    not response
                    or not response.embeddings
                    or not response.embeddings.float
                ):

                    self.logger.error(
                        "Error while embedding text with Cohere."
                    )

                    return None

                embeddings.extend(
                    response.embeddings.float
                )

            return embeddings

        except Exception as e:

            self.logger.exception(
                f"Cohere embedding error: {e}"
            )

            return None

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
            "text": self.process_text(prompt)
        }