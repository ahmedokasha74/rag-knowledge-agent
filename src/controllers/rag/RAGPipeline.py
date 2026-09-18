from controllers.retrieval.RetrievalController import (
    RetrievalController
)

from stores.llm.LLMProviderFactory import (
    LLMProviderFactory
)

from controllers.BaseController import BaseController


class RAGPipeline(BaseController):

    def __init__(self, config):

        super().__init__()

        self.config = config

        # Retrieval
        self.retrieval_controller = RetrievalController(
            config=self.config
        )

        # Generation Provider
        llm_factory = LLMProviderFactory(
            config=self.config
        )

        self.generation_provider = llm_factory.create(
            provider=self.config.GENERATION_BACKEND
        )

        self.generation_provider.set_generation_model(
            model_id=self.config.GENERATION_MODEL_ID
        )

    async def retrieve(
        self,
        query: str,
        collection_name: str,
        limit: int = 5
    ):

        return await self.retrieval_controller.retrieve(
            query=query,
            collection_name=collection_name,
            limit=limit
        )

    def build_prompt(
        self,
        query: str,
        retrieved_documents: list
    ):

        context_parts = []

        for index, document in enumerate(
            retrieved_documents,
            start=1
        ):
            context_parts.append(
                f"""
[Context {index}]
{document.text}
"""
            )

        context = "\n".join(context_parts)

        prompt = f"""
You are a knowledgeable assistant for Cloudify.

Your task is to answer the user's question using the
provided knowledge base context.

Instructions:
1. Use only the information provided in the context.
2. Do not use external knowledge or make assumptions.
3. If the context does not contain enough information to
   answer the question, say that the information is not
   available in the knowledge base.
4. Do not invent policies, rules, dates, prices, or other facts.
5. Give a clear and concise answer.
6. When multiple context sections are relevant, combine
   their information into one coherent answer.
7. If the context contains conflicting information, explicitly
   mention the conflict instead of choosing one arbitrarily.

Knowledge Base Context:
-----------------------
{context}
-----------------------

User Question:
{query}

Answer:
"""

        return prompt

    async def generate(
        self,
        prompt: str
    ):

        return self.generation_provider.generate_text(
            prompt=prompt
        )

    async def query(
    self,
    query: str,
    collection_name: str,
    limit: int = 5
):
        retrieved_documents = await self.retrieve(
            query=query,
            collection_name=collection_name,
            limit=limit,
            score_threshold=self.config.VECTOR_DB_SCORE_THRESHOLD
        )

        prompt = self.build_prompt(
            query=query,
            retrieved_documents=retrieved_documents
        )

        print("\n" + "=" * 60)
        print("AUGMENTED PROMPT")
        print("=" * 60)
        print(prompt)

        answer = await self.generate(prompt=prompt)

        return answer