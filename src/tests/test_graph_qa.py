from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory

from controllers.GraphRag.retrieval.query_entity_extractor import (
    QueryEntityExtractor
)

from controllers.GraphRag.retrieval.graph_retriever import (
    GraphRetriever
)

from controllers.GraphRag.retrieval.graph_context_builder import (
    GraphContextBuilder
)

from controllers.GraphRag.graph_answer_generator import (
    GraphAnswerGenerator
)


def main():

    settings = get_settings()

    # -------------------------
    # LLM
    # -------------------------

    llm_factory = LLMProviderFactory(config=settings)

    llm_provider = llm_factory.create(
        provider=settings.GRAPH_EXTRACTION_BACKEND
    )

    model_id = (
        settings.GRAPH_EXTRACTION_MODEL_ID
        or settings.GENERATION_MODEL_ID
    )

    llm_provider.set_generation_model(model_id)

    # -------------------------
    # Components
    # -------------------------

    extractor = QueryEntityExtractor(
        llm_provider=llm_provider
    )

    retriever = GraphRetriever(
        config=settings
    )

    context_builder = GraphContextBuilder()

    answer_generator = GraphAnswerGenerator(
        llm_provider=llm_provider
    )

    # -------------------------
    # Query
    # -------------------------

    queries = [
        "What plans does Cloudify offer?",
        "What is the relationship between Cloudify and Professional?",
        "What is connected to Cloudify?",
        "What is the Starter plan?",
        "What does Cloudify offer?",
    ]

    for query in queries:
        print("\n" + "=" * 60)
        print("USER:")
        print(query)

        graph_query = extractor.extract(query)

        print("\nGRAPH QUERY:")
        print(graph_query.model_dump_json(indent=2))

        results = retriever.retrieve(graph_query)

        print("\nRAW RESULTS:")
        for result in results:
            print(result)

        graph_context = context_builder.build(results)

        print("\nGRAPH CONTEXT:")
        print(graph_context)

        answer = answer_generator.generate(
            query=query,
            context=graph_context,
        )

        print("\nFINAL ANSWER:")
        print(answer)


if __name__ == "__main__":
    main()