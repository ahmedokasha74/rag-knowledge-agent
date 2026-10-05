from pathlib import Path
import sys


# Allow this file to be run directly from the repository root, e.g.
# ``uv run python src/tests/test_graph_transformer.py``.
SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from langchain_core.documents import Document

from controllers.reader import BaseReader
from helpers.config import get_settings
from models.db_schemes import DataChunk
from stores.llm.LLMProviderFactory import LLMProviderFactory


def main():

    settings = get_settings()

    # -----------------------------------------
    # 1. Read + chunk document
    # -----------------------------------------

    file_path = "data/documents/refund_policy.md"
    reader = BaseReader()
    source_documents = reader.get_file_content(file_path=file_path)
    raw_chunks = reader.process_file_content(
        file_content=source_documents,
        chunk_size=1_200,
    )

    data_chunks = [
        DataChunk(
            text=chunk["text"],
            metadata={
                **chunk["metadata"],
                "chunk_id": f"{Path(file_path).stem}-{index}",
                "source": file_path,
            },
        )
        for index, chunk in enumerate(raw_chunks)
    ]

    print(f"Number of chunks: {len(data_chunks)}")

    # -----------------------------------------
    # 2. Convert DataChunk -> LangChain Document
    # -----------------------------------------

    documents = [
        Document(
            page_content=chunk.text,
            metadata=chunk.metadata
        )
        for chunk in data_chunks
    ]

    # -----------------------------------------
    # 3. Create LLM Provider
    # -----------------------------------------

    llm_factory = LLMProviderFactory(config=settings)
    llm_provider = llm_factory.create(
        provider=settings.GRAPH_EXTRACTION_BACKEND,
    )
    if llm_provider is None:
        raise ValueError(
            "Unsupported GRAPH_EXTRACTION_BACKEND: "
            f"{settings.GRAPH_EXTRACTION_BACKEND}"
        )

    model_id = (
        settings.GRAPH_EXTRACTION_MODEL_ID
        or settings.GENERATION_MODEL_ID
    )
    if not model_id:
        raise ValueError(
            "Set GRAPH_EXTRACTION_MODEL_ID or GENERATION_MODEL_ID in .env."
        )

    llm_provider.set_generation_model(model_id)

    # -----------------------------------------
    # 4. Transform chunks -> GraphDocuments
    # -----------------------------------------

    graph_documents = llm_provider.graph_transformer(
        documents
    )

    print(
        f"Number of graph documents: "
        f"{len(graph_documents)}"
    )

    # -----------------------------------------
    # 5. Inspect result
    # -----------------------------------------

    for index, graph_document in enumerate(graph_documents):

        print("\n" + "=" * 60)
        print(f"GRAPH DOCUMENT {index + 1}")
        print("=" * 60)

        print("\nNODES:")

        for node in graph_document.nodes:

            print(
                f"  - {node.id} "
                f"[{node.type}]"
            )

            if node.properties:
                print(
                    f"    Properties: "
                    f"{node.properties}"
                )

        print("\nRELATIONSHIPS:")

        for relation in graph_document.relationships:

            print(
                f"  - {relation.source.id}"
                f" --[{relation.type}]--> "
                f"{relation.target.id}"
            )


if __name__ == "__main__":
    main()
