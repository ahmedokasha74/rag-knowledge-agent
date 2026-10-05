import pytest

from controllers.GraphRag.retrieval.query_entity_extractor import (
    QueryEntityExtractor,
)
from helpers.config import get_settings
from models.graph_rag import GraphQuery


class StructuredProvider:
    def __init__(self, result):
        self.result = result
        self.kwargs = None

    def generate_structured(self, **kwargs):
        self.kwargs = kwargs
        return self.result


def test_extractor_uses_graph_output_budget():
    provider = StructuredProvider(GraphQuery(query_type="ENTITY"))
    extractor = QueryEntityExtractor(provider)

    result = extractor.extract("What is Cloudify?")

    assert result.query_type == "ENTITY"
    assert provider.kwargs["max_output_tokens"] == (
        get_settings().GRAPH_EXTRACTION_MAX_TOKENS or 1024
    )


def test_extractor_reports_invalid_structured_output():
    extractor = QueryEntityExtractor(StructuredProvider(None))

    with pytest.raises(RuntimeError, match="no valid structured result"):
        extractor.extract("What is Cloudify?")