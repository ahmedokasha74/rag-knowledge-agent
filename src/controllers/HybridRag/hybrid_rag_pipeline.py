from controllers.HybridRag.hybrid_answer_generator import HybridAnswerGenerator
from controllers.HybridRag.hybrid_context_builder import HybridContextBuilder
from controllers.HybridRag.hybrid_retriever import HybridRetriever


class HybridRagPipeline:
    def __init__(
        self,
        config=None,
        hybrid_retriever=None,
        context_builder=None,
        answer_generator=None,
    ):
        self.hybrid_retriever = hybrid_retriever or HybridRetriever(
            config=config
        )
        self.context_builder = context_builder or HybridContextBuilder()
        self.answer_generator = answer_generator or HybridAnswerGenerator(
            config=config
        )

    async def connect(self):
        await self.hybrid_retriever.connect()

    async def disconnect(self):
        await self.hybrid_retriever.disconnect()

    async def query(
        self,
        query: str,
        collection_name: str,
        limit: int = 5,
        score_threshold: float | None = None,
    ) -> dict:
        retrieval_results = await self.hybrid_retriever.retrieve(
            query=query,
            collection_name=collection_name,
            limit=limit,
            score_threshold=score_threshold,
        )
        contexts = self.context_builder.build(
            vector_results=retrieval_results["vector_results"],
            graph_results=retrieval_results["graph_results"],
        )
        answer = self.answer_generator.generate(
            query=query,
            vector_context=contexts["vector_context"],
            graph_context=contexts["graph_context"],
        )

        return {
            "query": query,
            **retrieval_results,
            **contexts,
            "answer": answer,
        }