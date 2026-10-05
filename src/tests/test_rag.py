import asyncio

from helpers.config import get_settings
from controllers.rag.RAGPipeline import RAGPipeline


QUERIES = [
    "What is Cloudify's refund policy?",
    "Can I get a refund for an annual subscription?",
    "What support and SLA commitments does Cloudify provide for Enterprise customers?",
    "What is the uptime commitment for the Professional plan?",
    "How long does Cloudify retain customer data?",
    "What happens when Cloudify experiences a service outage?",
    "What are the API rate limits?",
    "What are the support response times for different plans?",
    "Can I cancel my subscription at any time?",
    "What is Cloudify's employee vacation policy?",
]


async def main():
    settings = get_settings()

    rag = RAGPipeline(config=settings)

    collection_name = "cloudify_documents"

    await rag.retrieval_controller.vector_db_provider.connect()

    try:
        for index, query in enumerate(QUERIES, start=1):

            print("\n")
            print("=" * 80)
            print(f"TEST {index}")
            print("=" * 80)

            print(f"\nQuery:")
            print(query)

            # --------------------------------------------------
            # 1. Retrieval
            # --------------------------------------------------

            retrieved_documents = await rag.retrieve(
                query=query,
                collection_name=collection_name,
                limit=5,
                score_threshold=0.60        
            )

            print("\n" + "-" * 80)
            print("RETRIEVED DOCUMENTS")
            print("-" * 80)

            if not retrieved_documents:
                print("No documents retrieved.")

            for i, document in enumerate(retrieved_documents, start=1):

                print(f"\n[Document {i}]")

                print(f"Score: {document.score}")

                print("\nText:")
                print(document.text[:500])

            # --------------------------------------------------
            # 2. Augmentation
            # --------------------------------------------------

            prompt = rag.build_prompt(
                query=query,
                retrieved_documents=retrieved_documents
            )

            print("\n" + "-" * 80)
            print("AUGMENTED PROMPT")
            print("-" * 80)

            print(prompt)

            # --------------------------------------------------
            # 3. Generation
            # --------------------------------------------------

            answer = await rag.generate(prompt=prompt)

            print("\n" + "-" * 80)
            print("FINAL ANSWER")
            print("-" * 80)

            if answer:
                print(answer)
            else:
                print("Generation returned None.")

            print("\n" + "=" * 80)
    finally:
        await rag.retrieval_controller.vector_db_provider.disconnect()


if __name__ == "__main__":
    asyncio.run(main())