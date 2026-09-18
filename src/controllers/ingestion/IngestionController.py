from pathlib import Path

from controllers.BaseController import BaseController
from controllers.reader import BaseReader
from controllers.chunking.ChunkingProviderFactory import (
    ChunkingProviderFactory
)
from controllers.chunking.ChunkingEnums import ChunkingType

from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import (
    VectorDBProviderFactory
)


class IngestionController(BaseController):

    def __init__(self, config):

        super().__init__()

        self.config = config

        # --------------------------------------------------
        # Reader
        # --------------------------------------------------

        self.reader = BaseReader()

        # --------------------------------------------------
        # Embedding Provider
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Chunker
        # --------------------------------------------------

        self.chunker = ChunkingProviderFactory.get_provider(
            chunking_type=ChunkingType.SEMANTIC,
            embedding_provider=self.embedding_provider
        )

        # --------------------------------------------------
        # Vector Database
        # --------------------------------------------------

        vector_db_factory = VectorDBProviderFactory(
            config=self.config
        )

        self.vector_db_provider = vector_db_factory.create(
            provider=self.config.VECTOR_DB_BACKEND
        )

    # --------------------------------------------------
    # Ingest Directory
    # --------------------------------------------------

    async def ingest_directory(
        self,
        directory_path: str,
        collection_name: str,
        do_reset: bool = False
    ):

        directory = Path(directory_path)

        # Find all Markdown files
        files = list(
            directory.glob("*.md")
        )

        if not files:
            raise ValueError(
                f"No markdown files found in: {directory_path}"
            )

        print(
            f"Found {len(files)} files"
        )

        # Connect to Vector DB
        await self.vector_db_provider.connect()

        try:

            # --------------------------------------------------
            # Create Collection
            # --------------------------------------------------

            await self.vector_db_provider.create_collection(
                collection_name=collection_name,
                embedding_size=self.config.EMBEDDING_MODEL_SIZE,
                do_reset=do_reset
            )

            # --------------------------------------------------
            # Process Each File
            # --------------------------------------------------

            for file_path in files:

                print("\n" + "=" * 60)
                print(
                    f"Processing: {file_path.name}"
                )
                print("=" * 60)

                # --------------------------------------------------
                # Read
                # --------------------------------------------------

                documents = self.reader.get_file_content(
                    file_path=str(file_path)
                )

                if not documents:

                    print(
                        "No documents loaded."
                    )

                    continue

                print(
                    f"Documents loaded: {len(documents)}"
                )

                # --------------------------------------------------
                # Chunk
                # --------------------------------------------------

                chunks = self.chunker.chunk(
                    documents=documents,
                    chunk_size=self.config.FILE_DEFAULT_CHUNK_SIZE,
                    chunk_overlap=50
                )

                print(
                    f"Chunks created: {len(chunks)}"
                )

                # --------------------------------------------------
                # Extract Text
                # --------------------------------------------------

                texts = [
                    chunk.page_content
                    for chunk in chunks
                ]

                # --------------------------------------------------
                # Embedding
                # --------------------------------------------------

                print(
                    "Creating embeddings..."
                )

                vectors = self.embedding_provider.embed_texts(
                    texts=texts,
                    document_type="document"
                )

                print(
                    f"Vectors created: {len(vectors)}"
                )

                # --------------------------------------------------
                # Metadata
                # --------------------------------------------------

                metadata = [
                    {
                        "source": file_path.name,
                        "chunk_id": index
                    }
                    for index in range(
                        len(chunks)
                    )
                ]

                # --------------------------------------------------
                # Record IDs
                # --------------------------------------------------

                record_ids = [
                    f"{file_path.stem}-{index}"
                    for index in range(
                        len(chunks)
                    )
                ]

                # --------------------------------------------------
                # Store in Vector DB
                # --------------------------------------------------

                print(
                    "Storing chunks in Qdrant..."
                )

                inserted = await self.vector_db_provider.insert_many(
                    collection_name=collection_name,
                    texts=texts,
                    vectors=vectors,
                    metadata=metadata,
                    record_ids=record_ids
                )

                print(
                    f"Inserted successfully: {inserted}"
                )

        finally:

            # --------------------------------------------------
            # Disconnect
            # --------------------------------------------------

            await self.vector_db_provider.disconnect()

            print(
                "\nDisconnected from Qdrant"
            )