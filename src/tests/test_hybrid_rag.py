import asyncio
from pprint import pformat

from controllers.HybridRag.hybrid_rag_pipeline import HybridRagPipeline
from helpers.config import get_settings


QUERIES = [
    "What plans does Cloudify offer?",
    "What is the relationship between Cloudify and Professional?",
    "What is Cloudify?",
    "What are the permitted uses of Cloudify?",
]


def _display_vector_results(results):
    return [
        result.model_dump() if hasattr(result, "model_dump") else result
        for result in results
    ]


async def main():
    settings = get_settings()
    pipeline = HybridRagPipeline(config=settings)
    collection_name = "cloudify_documents"

    await pipeline.connect()
    try:
        for query in QUERIES:
            result = await pipeline.query(
                query=query,
                collection_name=collection_name,
                limit=5,
                score_threshold=settings.SCORE_THRESHOLD,
            )

            print("\n" + "=" * 80)
            print("USER:")
            print(query)

            print("\nVECTOR RESULTS:")
            print(pformat(_display_vector_results(result["vector_results"])))

            print("\nGRAPH RESULTS:")
            print(pformat(result["graph_results"]))

            print("\nCOMBINED CONTEXT:")
            print(result["combined_context"])

            print("\nFINAL ANSWER:")
            print(result["answer"])

        print("\n" + "=" * 80)
    finally:
        await pipeline.disconnect()


if __name__ == "__main__":
    asyncio.run(main())