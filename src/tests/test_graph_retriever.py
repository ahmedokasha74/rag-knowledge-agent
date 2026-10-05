from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory

from controllers.GraphRag.retrieval.query_entity_extractor import (
    QueryEntityExtractor,
)

from controllers.GraphRag.retrieval.graph_retriever import (
    GraphRetriever,
)


def main():

    # -----------------------------------------
    # 1. Load settings
    # -----------------------------------------

    settings = get_settings()

    # -----------------------------------------
    # 2. Create LLM provider
    # -----------------------------------------

    llm_factory = LLMProviderFactory(config=settings)

    llm_provider = llm_factory.create(
        provider=settings.GRAPH_EXTRACTION_BACKEND
    )

    model_id = (
        settings.GRAPH_EXTRACTION_MODEL_ID
        or settings.GENERATION_MODEL_ID
    )

    llm_provider.set_generation_model(model_id)

    # -----------------------------------------
    # 3. Create Query Entity Extractor
    # -----------------------------------------

    extractor = QueryEntityExtractor(
        llm_provider=llm_provider
    )

    # -----------------------------------------
    # 4. Create Graph Retriever
    # -----------------------------------------

    retriever = GraphRetriever(
        config=settings
    )

    # -----------------------------------------
    # 5. Test queries
    # -----------------------------------------

    queries = [
        "What plans does Cloudify offer?",
        "What is the relationship between Cloudify and Professional?",
        "What is connected to Cloudify?",
    ]

    for query in queries:

        print("\n" + "=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)

        # -----------------------------------------
        # Extract GraphQuery
        # -----------------------------------------

        graph_query = extractor.extract(query)

        print("\nGraph Query:")
        print(graph_query.model_dump_json(indent=2))

        # -----------------------------------------
        # Retrieve from Neo4j
        # -----------------------------------------

        results = retriever.retrieve(graph_query)

        print("\nNeo4j Results:")

        if not results:
            print("No results found.")
            continue

        for result in results:
            print(result)


if __name__ == "__main__":
    main()