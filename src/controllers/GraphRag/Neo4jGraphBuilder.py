from controllers.BaseController import BaseController
from controllers.GraphRag.graph_extractor import GraphExtractor
from helpers.config import get_settings

from langchain_core.documents import Document
from langchain_neo4j import Neo4jGraph


class Neo4jGraphBuilder(BaseController):

    def __init__(self, config=None):
        super().__init__()

        self.settings = config or get_settings()

        self.graph = Neo4jGraph(
            url=self.settings.NEO4J_URI,
            username=self.settings.NEO4J_USER,
            password=self.settings.NEO4J_PASSWORD,
        )

    def build_graph_from_documents(
        self,
        documents: list[Document],
    ):
        graph_extractor = GraphExtractor()

        graph_documents = graph_extractor.extract(
            documents
        )

        self.graph.add_graph_documents(
            graph_documents,
            include_source=True,
            baseEntityLabel=True,
        )

        return graph_documents