from controllers.GraphRag.retrieval.graph_retriever import GraphRetriever
from controllers.GraphRag.retrieval.query_entity_extractor import (
    QueryEntityExtractor,
)
from controllers.retrieval.RetrievalController import RetrievalController
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory


class HybridRetriever:
    """Coordinates the existing vector and manual graph retrievers."""

    def __init__(
        self,
        config=None,
        vector_retriever=None,
        graph_retriever=None,
        query_entity_extractor=None,
    ):
        self.config = config or get_settings()
        self.vector_retriever = vector_retriever or RetrievalController(
            config=self.config
        )
        self.graph_retriever = graph_retriever or GraphRetriever(
            config=self.config
        )

        if query_entity_extractor is None:
            llm_factory = LLMProviderFactory(config=self.config)
            graph_llm = llm_factory.create(
                provider=self.config.GRAPH_EXTRACTION_BACKEND
            )
            model_id = (
                self.config.GRAPH_EXTRACTION_MODEL_ID
                or self.config.GENERATION_MODEL_ID
            )
            if not model_id:
                raise ValueError(
                    "No model configured for graph query extraction."
                )
            graph_llm.set_generation_model(model_id)
            query_entity_extractor = QueryEntityExtractor(
                llm_provider=graph_llm
            )

        self.query_entity_extractor = query_entity_extractor

    async def connect(self):
        await self.vector_retriever.vector_db_provider.connect()

    async def disconnect(self):
        await self.vector_retriever.vector_db_provider.disconnect()

    async def retrieve(
        self,
        query: str,
        collection_name: str,
        limit: int = 5,
        score_threshold: float | None = None,
    ) -> dict:
        if score_threshold is None:
            score_threshold = self.config.SCORE_THRESHOLD

        vector_results = await self.vector_retriever.retrieve(
            query=query,
            collection_name=collection_name,
            limit=limit,
            score_threshold=score_threshold,
        )

        graph_query = self.query_entity_extractor.extract(query)
        graph_results = self.graph_retriever.retrieve(graph_query)

        return {
            "vector_results": vector_results,
            "graph_results": graph_results,
        }