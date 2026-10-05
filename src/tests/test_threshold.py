import asyncio

from controllers.retrieval.RetrievalController import RetrievalController
from helpers.config import get_settings


async def main():

    config = get_settings()

    retrieval_controller = RetrievalController(
        config=config
    )

    queries = [
        "What is the uptime commitment for the Professional plan?",
        "What are the API rate limits?",
    ]

    await retrieval_controller.vector_db_provider.connect()

    try:
        for query in queries:

            print("\n" + "=" * 80)
            print(f"QUERY: {query}")
            print("=" * 80)

            results = await retrieval_controller.retrieve(
                query=query,
                collection_name="cloudify_documents",
                limit=10,
                score_threshold=0.0
            )

            print(f"Configured threshold: {config.SCORE_THRESHOLD}")
            print(f"Retrieved results: {len(results)}")

            for index, document in enumerate(results, start=1):

                metadata = getattr(document, "metadata", {}) or {}

                print(
                    f"{index}. "
                    f"Score: {document.score:.4f} | "
                    f"Source: {metadata.get('source', 'Unavailable')} | "
                    f"Chunk ID: {metadata.get('chunk_id', 'Unavailable')}"
                )
                print(f"Preview: {document.text[:200]}")

    finally:
        await retrieval_controller.vector_db_provider.disconnect()


if __name__ == "__main__":
    asyncio.run(main())