from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory

from controllers.GraphRag.retrieval.query_entity_extractor import (
    QueryEntityExtractor,
)


def main():
    settings = get_settings()

    # Create LLM provider
    llm_factory = LLMProviderFactory(config=settings)

    llm_provider = llm_factory.create(
        provider=settings.GRAPH_EXTRACTION_BACKEND
    )

    # Set model
    model_id = (
        settings.GRAPH_EXTRACTION_MODEL_ID
        or settings.GENERATION_MODEL_ID
    )

    llm_provider.set_generation_model(model_id)

    # Create extractor
    extractor = QueryEntityExtractor(
        llm_provider=llm_provider
    )

    # Test query
    query = "What plans does Cloudify offer?"

    # Real LLM call
    result = extractor.extract(query)

    print("\nQuery:")
    print(query)

    print("\nExtracted Entities:")

    for entity in result.entities:
        print(f"- {entity.name} | {entity.type}")


if __name__ == "__main__":
    main()