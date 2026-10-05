from pathlib import Path

from langchain_core.documents import Document

from controllers.GraphRag.graph_extractor import GraphExtractor
from controllers.reader import BaseReader


def main():

    # ==========================================
    # 1. Read and chunk a real document
    # ==========================================

    file_path = "data/documents/refund_policy.md"

    reader = BaseReader()
    documents = reader.get_file_content(file_path=file_path)
    raw_chunks = reader.process_file_content(
        file_content=documents,
        chunk_size=1_200,
    )

    documents = [
        Document(
            page_content=chunk["text"],
            metadata={
                **chunk["metadata"],
                "chunk_id": f"{Path(file_path).stem}-{index}",
                "source": file_path,
            },
        )
        for index, chunk in enumerate(raw_chunks)
    ]

    print(f"Number of chunks: {len(documents)}")

    # ==========================================
    # 2. Inspect the actual DataChunk
    # ==========================================

    print("\n========== FIRST CHUNK ==========")

    first_chunk = documents[0]

    # print("Text:")
    # print(first_chunk.text)

    # print("\nMetadata:")
    # print(first_chunk.metadata)

    # ==========================================
    # 3. Create GraphExtractor
    # ==========================================

    extractor = GraphExtractor()

    # ==========================================
    # 4. Extract graph documents
    # ==========================================

    graph_documents = extractor.extract(documents)

    # ==========================================
    # 5. Display results
    # ==========================================

    print("\n\n========================================")
    print("GRAPH EXTRACTION RESULTS")
    print("========================================")

    for index, graph_document in enumerate(graph_documents, start=1):

        print(f"\n========== GRAPH CHUNK {index} ==========")

        print(f"Source: {graph_document.source.metadata.get('source', 'unknown')}")

        print("\nEntities:")

        for entity in graph_document.nodes:
            print(
                f"  - {entity.id} "
                f"[{entity.type}]"
            )

            if entity.properties:
                print(
                    f"    Properties: {entity.properties}"
                )

        print("\nRelations:")

        for relation in graph_document.relationships:
            print(
                f"  - "
                f"{relation.source.id} "
                f"--[{relation.type}]--> "
                f"{relation.target.id}"
            )

            if relation.properties:
                print(
                    f"    Description: {relation.properties}"
                )


if __name__ == "__main__":
    main()
