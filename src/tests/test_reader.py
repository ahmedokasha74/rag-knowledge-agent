# # # # # # # from controllers.reader import BaseReader
# # # # # # # from controllers.chunking.ChunkingEnums import ChunkingType
# # # # # # # from controllers.chunking.ChunkingProviderFactory import ChunkingProviderFactory

# # # # # # # reader = BaseReader()
# # # # # # # chunking_provider = ChunkingProviderFactory.get_provider(ChunkingType.TOKEN)
# # # # # # # file_path = "data/documents/acceptable_use_policy.md"

# # # # # # # print("Extension:", reader.get_file_extension(file_path))
# # # # # # # print("Is allowed:", reader.is_file_type_allowed(file_path))

# # # # # # # loader = reader.get_file_loader(file_path)
# # # # # # # print("File loader:", loader)

# # # # # # # file_content = reader.get_file_content(file_path)
# # # # # # # print("Number of documents:", len(file_content))

# # # # # # # # chunks = reader.process_file_content(
# # # # # # # #     file_content=file_content,
# # # # # # # #     chunk_size=100,
# # # # # # # #     overlap_size=20,
# # # # # # # # )

# # # # # # # # print("Number of chunks:", len(chunks))
# # # # # # # # print("First chunk:")
# # # # # # # # print(chunks[0])

# # # # # # # # print("\nSecond chunk:")
# # # # # # # # print(chunks[1])
# # # # # # # chunks=chunking_provider.chunk(
# # # # # # #     documents=file_content,
# # # # # # #     chunk_size=100,
# # # # # # #     chunk_overlap=20
# # # # # # # )
# # # # # # # print("Number of chunks:", len(chunks))
# # # # # # # print("First chunk:")
# # # # # # # print(chunks[0])
# # # # # # from stores.llm.providers.GroqProvider import GroqProvider
# # # # # # from helpers.config import get_settings


# # # # # # settings = get_settings()

# # # # # # provider = GroqProvider(
# # # # # #     api_key=settings.GROQ_API_KEY,
# # # # # #     default_input_max_characters=settings.INPUT_DAFAULT_MAX_CHARACTERS or 4000,
# # # # # #     default_generation_max_output_tokens=settings.GENERATION_DAFAULT_MAX_TOKENS or 500,
# # # # # #     default_generation_temperature=settings.GENERATION_DAFAULT_TEMPERATURE or 0.1
# # # # # # )

# # # # # # provider.set_generation_model(
# # # # # #     settings.GENERATION_MODEL_ID or "openai/gpt-oss-20b"
# # # # # # )

# # # # # # response = provider.generate_text(
# # # # # #     prompt="Explain RAG in 2 simple sentences."
# # # # # # )

# # # # # # print("Response:")
# # # # # # print(response)
# # # # # from stores.llm.providers.CoHereProvider import CoHereProvider
# # # # # from stores.llm.LLMEnums import DocumentTypeEnum
# # # # # from helpers.config import get_settings


# # # # # settings = get_settings()

# # # # # provider = CoHereProvider(
# # # # #     api_key=settings.COHERE_API_KEY,
# # # # #     default_input_max_characters=(
# # # # #         settings.INPUT_DAFAULT_MAX_CHARACTERS or 4000
# # # # #     )
# # # # # )

# # # # # provider.set_embedding_model(
# # # # #     model_id=settings.EMBEDDING_MODEL_ID,
# # # # #     embedding_size=settings.EMBEDDING_MODEL_SIZE
# # # # # )

# # # # # text = "Cloudify provides a 14-day refund window for new subscriptions."

# # # # # embedding = provider.embed_text(
# # # # #     text=text,
# # # # #     document_type=DocumentTypeEnum.DOCUMENT
# # # # # )

# # # # # print("Embedding type:", type(embedding))
# # # # # print("Embedding size:", len(embedding))
# # # # # print("First 5 values:", embedding[:5])
# # # # from controllers.reader import BaseReader
# # # # from controllers.chunking.providers.SemanticChunker import SemanticChunker
# # # # from stores.llm.providers.CoHereProvider import CoHereProvider
# # # # from helpers.config import get_settings


# # # # settings = get_settings()

# # # # # Reader
# # # # reader = BaseReader()

# # # # file_path = "data/documents/acceptable_use_policy.md"

# # # # documents = reader.get_file_content(file_path)

# # # # # Cohere Embedding Provider
# # # # embedding_provider = CoHereProvider(
# # # #     api_key=settings.COHERE_API_KEY,
# # # #     default_input_max_characters=(
# # # #         settings.INPUT_DAFAULT_MAX_CHARACTERS or 4000
# # # #     )
# # # # )

# # # # embedding_provider.set_embedding_model(
# # # #     model_id=settings.EMBEDDING_MODEL_ID,
# # # #     embedding_size=settings.EMBEDDING_MODEL_SIZE
# # # # )

# # # # # Semantic Chunker
# # # # chunker = SemanticChunker(
# # # #     embedding_provider=embedding_provider
# # # # )

# # # # chunks = chunker.chunk(
# # # #     documents=documents,
# # # #     chunk_size=100,
# # # #     chunk_overlap=20
# # # # )

# # # # print("Number of semantic chunks:", len(chunks))

# # # # print("\nFirst chunk:")
# # # # print(chunks[0])

# # # # print("\nSecond chunk:")
# # # # print(chunks[1])
# # # from helpers.config import get_settings
# # # from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory


# # # async def main():

# # #     settings = get_settings()

# # #     vector_db_factory = VectorDBProviderFactory(
# # #         config=settings
# # #     )

# # #     vector_db = vector_db_factory.create(
# # #         provider=settings.VECTOR_DB_BACKEND
# # #     )

# # #     # 1. Connect
# # #     await vector_db.connect()

# # #     print("Connected to Qdrant")

# # #     # 2. Create collection
# # #     collection_name = "cloudify_documents"

# # #     created = await vector_db.create_collection(
# # #         collection_name=collection_name,
# # #         embedding_size=settings.EMBEDDING_MODEL_SIZE,
# # #         do_reset=True
# # #     )

# # #     print(f"Collection created: {created}")

# # #     # 3. Insert one vector
# # #     vector = [0.1] * settings.EMBEDDING_MODEL_SIZE

# # #     inserted = await vector_db.insert_one(
# # #         collection_name=collection_name,
# # #         text="Cloudify provides a 14-day refund period.",
# # #         vector=vector,
# # #         metadata={
# # #             "source": "refund_policy.md",
# # #             "chunk_id": 0
# # #         },
# # #         record_id="test-1"
# # #     )

# # #     print(f"Document inserted: {inserted}")

# # #     # 4. Search
# # #     results = await vector_db.search_by_vector(
# # #         collection_name=collection_name,
# # #         vector=vector,
# # #         limit=5
# # #     )

# # #     print("\nSearch results:")

# # #     for result in results:
# # #         print(f"Score: {result.score}")
# # #         print(f"Text: {result.text}")
# # #         print("-" * 50)

# # #     # 5. Disconnect
# # #     await vector_db.disconnect()

# # #     print("\nDisconnected from Qdrant")


# # # if __name__ == "__main__":

# # #     import asyncio

# # #     asyncio.run(main())
# # import asyncio
# # from pathlib import Path

# # from helpers.config import get_settings

# # from controllers.reader import BaseReader

# # from controllers.chunking.ChunkingProviderFactory import (
# #     ChunkingProviderFactory
# # )
# # from controllers.chunking.ChunkingEnums import ChunkingType

# # from stores.llm.LLMProviderFactory import LLMProviderFactory

# # from stores.vectordb.VectorDBProviderFactory import (
# #     VectorDBProviderFactory
# # )


# # async def main():

# #     settings = get_settings()

# #     # --------------------------------
# #     # 1. Initialize Reader
# #     # --------------------------------

# #     reader = BaseReader()

# #     file_path = Path(
# #         "data/documents/refund_policy.md"
# #     )

# #     print(f"Reading file: {file_path}")

# #     documents = reader.get_file_content(
# #         file_path=str(file_path)
# #     )

# #     print(f"Documents loaded: {len(documents)}")


# #     # --------------------------------
# #     # 2. Initialize Embedding Provider
# #     # --------------------------------

# #     llm_factory = LLMProviderFactory(
# #         config=settings
# #     )

# #     embedding_provider = llm_factory.create(
# #         provider=settings.EMBEDDING_BACKEND
# #     )

# #     embedding_provider.set_embedding_model(
# #         model_id=settings.EMBEDDING_MODEL_ID,
# #         embedding_size=settings.EMBEDDING_MODEL_SIZE
# #     )

# #     print("Embedding provider initialized")


# #     # --------------------------------
# #     # 3. Chunk Documents
# #     # --------------------------------

# #     chunker = ChunkingProviderFactory.get_provider(
# #         chunking_type=ChunkingType.SEMANTIC,
# #         embedding_provider=embedding_provider
# #     )

# #     chunks = chunker.chunk(
# #         documents=documents,
# #         chunk_size=512,
# #         chunk_overlap=50
# #     )

# #     print(f"Chunks created: {len(chunks)}")


# #     # --------------------------------
# #     # 4. Create Embeddings
# #     # --------------------------------

# #     texts = [
# #         chunk.page_content
# #         for chunk in chunks
# #     ]

# #     print("Creating embeddings...")

# #     vectors = embedding_provider.embed_texts(
# #         texts=texts
# #     )

# #     print(f"Vectors created: {len(vectors)}")
# #     print(f"Vector dimension: {len(vectors[0])}")


# #     # --------------------------------
# #     # 5. Initialize Vector DB
# #     # --------------------------------

# #     vector_db_factory = VectorDBProviderFactory(
# #         config=settings
# #     )

# #     vector_db = vector_db_factory.create(
# #         provider=settings.VECTOR_DB_BACKEND
# #     )

# #     await vector_db.connect()

# #     print("Connected to Qdrant")


# #     # --------------------------------
# #     # 6. Create Collection
# #     # --------------------------------

# #     collection_name = "cloudify_documents"

# #     await vector_db.create_collection(
# #         collection_name=collection_name,
# #         embedding_size=settings.EMBEDDING_MODEL_SIZE,
# #         do_reset=True
# #     )

# #     print(
# #         f"Collection ready: {collection_name}"
# #     )


# #     # --------------------------------
# #     # 7. Prepare Metadata
# #     # --------------------------------

# #     metadata = []

# #     for index, chunk in enumerate(chunks):

# #         metadata.append({
# #             "source": file_path.name,
# #             "chunk_id": index
# #         })


# #     # --------------------------------
# #     # 8. Store in Qdrant
# #     # --------------------------------

# #     print("Storing chunks in Qdrant...")

# #     inserted = await vector_db.insert_many(
# #         collection_name=collection_name,
# #         texts=texts,
# #         vectors=vectors,
# #         metadata=metadata,
# #         record_ids=[
# #             f"{file_path.stem}-{index}"
# #             for index in range(len(chunks))
# #         ]
# #     )

# #     print(f"Inserted successfully: {inserted}")


# #     # --------------------------------
# #     # 9. Disconnect
# #     # --------------------------------

# #     await vector_db.disconnect()

# #     print("Disconnected from Qdrant")


# # if __name__ == "__main__":

# #     asyncio.run(main())
# import asyncio

# from helpers.config import get_settings
# from controllers.retrieval.RetrievalController import RetrievalController


# async def main():

#     settings = get_settings()

#     retrieval_controller = RetrievalController(
#         config=settings
#     )

#     await retrieval_controller.vector_db_provider.connect()

#     query = "What is Cloudify's refund policy?"

#     results = await retrieval_controller.retrieve(
#         query=query,
#         collection_name="cloudify_documents",
#         limit=5
#     )

#     print(f"\nQuery: {query}")
#     print(f"Number of results: {len(results)}\n")

#     for index, result in enumerate(results, start=1):

#         print(f"Result {index}")
#         print(f"Score: {result.score}")
#         print(f"Text: {result.text}")
#         print("-" * 60)

#     await retrieval_controller.vector_db_provider.disconnect()


# if __name__ == "__main__":
#     asyncio.run(main())
import asyncio

from helpers.config import get_settings
from controllers.rag.RAGPipeline import RAGPipeline


async def main():

    settings = get_settings()

    rag = RAGPipeline(
        config=settings
    )

    # Connect to Qdrant
    await rag.retrieval_controller.vector_db_provider.connect()

    query = "What is Cloudify's refund policy?"

    # RAG Query
    answer = await rag.query(
        query=query,
        collection_name="cloudify_documents",
        limit=5
    )

    print("\n" + "=" * 60)
    print("QUERY")
    print("=" * 60)
    print(query)

    print("\n" + "=" * 60)
    print("ANSWER")
    print("=" * 60)
    print(answer)

    # Disconnect
    await rag.retrieval_controller.vector_db_provider.disconnect()


if __name__ == "__main__":
    asyncio.run(main())