from controllers.BaseController import BaseController

from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import (
    VectorDBProviderFactory
)

from models.db_schemes import RetrievedDocument


class RetrievalController(BaseController):

    def __init__(self, config):

        super().__init__()

        self.config = config

        # Embedding Provider
        llm_factory = LLMProviderFactory(
            config=self.config
        )

        self.embedding_provider = llm_factory.create(
            provider=self.config.EMBEDDING_BACKEND
        )

        self.embedding_provider.set_embedding_model(
            model_id=self.config.EMBEDDING_MODEL_ID,
            embedding_size=self.config.EMBEDDING_MODEL_SIZE
        )

        # Vector DB
        vector_db_factory = VectorDBProviderFactory(
            config=self.config
        )

        self.vector_db_provider = vector_db_factory.create(
            provider=self.config.VECTOR_DB_BACKEND
        )

    async def retrieve(
            self,
            query: str,
            collection_name: str,
            limit: int = 10,
            score_threshold: float = None
        ) -> list[RetrievedDocument]:

            # 1. Convert query to embedding
            query_vector = self.embedding_provider.embed_text(
                text=query,
                document_type="query"
            )

            if not query_vector:
                return []

            # 2. Search vector database
            results = await self.vector_db_provider.search_by_vector(
                collection_name=collection_name,
                vector=query_vector,
                limit=limit
            )

            if score_threshold is None:
                score_threshold = self.config.VECTOR_DB_SCORE_THRESHOLD

            # 3. Apply similarity threshold
            filtered_results = [
                document
                for document in results
                if document.score >= score_threshold
            ]

            return filtered_results

    