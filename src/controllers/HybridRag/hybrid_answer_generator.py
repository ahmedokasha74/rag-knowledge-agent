from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory


class HybridAnswerGenerator:
    def __init__(self, config=None, llm_provider=None):
        self.config = config or get_settings()

        if llm_provider is None:
            llm_factory = LLMProviderFactory(config=self.config)
            llm_provider = llm_factory.create(
                provider=self.config.GENERATION_BACKEND
            )
            model_id = self.config.GENERATION_MODEL_ID
            if not model_id:
                raise ValueError("No generation model configured.")
            llm_provider.set_generation_model(model_id)

        self.llm_provider = llm_provider

    def generate(
        self,
        query: str,
        vector_context: str,
        graph_context: str,
    ) -> str:
        prompt = f"""
You are a knowledge assistant for Cloudify.

Answer the user's question using ONLY the evidence below. The context has
two evidence sources:
- VECTOR CONTEXT: semantic search results from source documents.
- GRAPH CONTEXT: structured entities and relationships from Neo4j.

Use either or both sources when relevant. Do not invent information. If the
evidence does not contain enough information, say that it is not available.
If the sources conflict, state that clearly rather than choosing arbitrarily.

USER QUESTION:
{query}

VECTOR CONTEXT:
{vector_context}

GRAPH CONTEXT:
{graph_context}

ANSWER:
"""
        return self.llm_provider.generate_text(
            prompt=prompt,
            temperature=0,
        )