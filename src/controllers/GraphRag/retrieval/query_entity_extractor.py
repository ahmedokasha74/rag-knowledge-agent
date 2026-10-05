from controllers.BaseController import BaseController
from helpers.config import get_settings
from models.graph_rag import GraphQuery
from stores.llm.LLMInterface import LLMInterface


class QueryEntityExtractor(BaseController):

    def __init__(self, llm_provider: LLMInterface):
        super().__init__()
        self.llm_provider = llm_provider
        self.settings = get_settings()

    def extract(self, query: str) -> GraphQuery:
        prompt = f"""
Extract graph-search intent from this user query. Do not answer it.

Set query_type to ENTITY only when asking what one entity is. Use
RELATIONSHIP for relations, connected entities, or relations between two entities.
Extract only explicitly mentioned entities. Set relationship_intent.source_entity
to the relationship's source when clear, target_entity to a named second entity,
and relation to a clearly requested relation type. Use null when unknown.
Do not invent entities or relations.

Examples:
- What is Cloudify? -> ENTITY, Cloudify
- What plans does Cloudify offer? -> RELATIONSHIP, source Cloudify, relation OFFERS
- What is the relationship between Cloudify and Professional? -> RELATIONSHIP,
  source Cloudify, target Professional, relation null

User query: {query}
"""

        result = self.llm_provider.generate_structured(
            prompt=prompt,
            response_model=GraphQuery,
            temperature=0,
            max_output_tokens=(
                self.settings.GRAPH_EXTRACTION_MAX_TOKENS or 1024
            ),
        )

        if result is None:
            raise RuntimeError(
                "Graph query extraction returned no valid structured result "
                f"for query {query!r}. Check the LLM response and set "
                "GRAPH_EXTRACTION_MAX_TOKENS to a value large enough for the model."
            )

        return result