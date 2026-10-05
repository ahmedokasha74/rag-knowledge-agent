import argparse
from pathlib import Path

from langchain_core.documents import Document

from controllers.GraphRag.Neo4jGraphBuilder import Neo4jGraphBuilder
from controllers.reader import BaseReader


def main(max_chunks: int = 3):
    reader = BaseReader()
    documents = []

    for file_path in sorted(Path("data/documents").glob("*.md")):
        file_content = reader.get_file_content(str(file_path))
        raw_chunks = reader.process_file_content(
            file_content=file_content,
            chunk_size=1_200,
        )

        documents.extend(
            Document(
                page_content=chunk["text"],
                metadata={
                    **chunk["metadata"],
                    "source": str(file_path),
                    "chunk_id": f"{file_path.stem}-{index}",
                },
            )
            for index, chunk in enumerate(raw_chunks)
        )

    assert documents, "No Markdown document chunks were loaded."
    total_documents = len(documents)
    if max_chunks > 0:
        documents = documents[:max_chunks]

    print(f"Total documents/chunks: {total_documents}")
    print(f"Testing documents/chunks: {len(documents)}")

    builder = Neo4jGraphBuilder()
    graph_documents = builder.build_graph_from_documents(documents)

    assert len(graph_documents) == len(documents)
    assert any(graph_document.nodes for graph_document in graph_documents), (
        "No nodes were extracted."
    )
    assert any(
        graph_document.relationships for graph_document in graph_documents
    ), "No relationships were extracted."

    extracted_node_ids = {
        node.id
        for graph_document in graph_documents
        for node in graph_document.nodes
    }

    persisted_count = builder.graph.query(
        """
        MATCH (node)
        WHERE node.id IN $node_ids
        RETURN count(DISTINCT node.id) AS count
        """,
        params={
            "node_ids": list(extracted_node_ids)
        },
    )[0]["count"]

    assert persisted_count == len(extracted_node_ids), (
        "Not all extracted nodes were persisted in Neo4j."
    )

    print("Neo4jGraphBuilder test passed")
    print(f"Graph documents: {len(graph_documents)}")
    print(f"Nodes extracted and persisted: {persisted_count}")
    print(
        "Relationships extracted: "
        f"{sum(len(graph_document.relationships) for graph_document in graph_documents)}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test Neo4jGraphBuilder with Markdown document chunks."
    )
    parser.add_argument(
        "--max-chunks",
        type=int,
        default=3,
        help="Number of chunks to send to Groq; use 0 to process all chunks.",
    )
    args = parser.parse_args()
    main(max_chunks=args.max_chunks)
