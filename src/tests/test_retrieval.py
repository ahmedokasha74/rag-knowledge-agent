import asyncio

from helpers.config import get_settings
from controllers.retrieval.RetrievalController import RetrievalController


async def main():

    settings = get_settings()

    retrieval = RetrievalController(
        config=settings
    )

    await retrieval.vector_db_provider.connect()

    try:

        query = (
            "What support and SLA commitments does Cloudify "
            "provide for Enterprise customers?"
        )

        results = await retrieval.retrieve(
            query=query,
            collection_name="cloudify_documents",
            limit=5
        )

        print("\n" + "=" * 60)
        print("QUERY")
        print("=" * 60)
        print(query)

        print("\n" + "=" * 60)
        print("RETRIEVED DOCUMENTS")
        print("=" * 60)

        for index, document in enumerate(results, start=1):

            print(f"\nResult {index}")
            print("-" * 40)
            print(f"Score: {document.score}")
            print(f"Text:\n{document.text}")

    finally:

        await retrieval.vector_db_provider.disconnect()


if __name__ == "__main__":
    asyncio.run(main())