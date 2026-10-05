from controllers.BaseController import BaseController
from helpers.config import get_settings
from langchain_neo4j import Neo4jGraph
from models.graph_rag import GraphQuery


class GraphRetriever(BaseController):

    def __init__(self, config=None):
        super().__init__()

        self.settings = config or get_settings()

        self.graph = Neo4jGraph(
            url=self.settings.NEO4J_URI,
            username=self.settings.NEO4J_USER,
            password=self.settings.NEO4J_PASSWORD,
        )

    def retrieve(self, graph_query: GraphQuery):

        if graph_query.query_type == "ENTITY":
            return self._retrieve_entity(graph_query)

        if graph_query.query_type == "RELATIONSHIP":
            return self._retrieve_relationship(graph_query)

        return []

    # ---------------------------------------------------------
    # ENTITY RETRIEVAL
    # ---------------------------------------------------------

    def _retrieve_entity(self, graph_query: GraphQuery):

        results = []

        for entity in graph_query.entities:

            query = """
            MATCH (n)
            WHERE toLower(n.id) = toLower($entity_name)

            RETURN
                n.id AS entity,
                labels(n) AS labels

            LIMIT 20
            """

            result = self.graph.query(
                query,
                params={
                    "entity_name": entity.name,
                },
            )

            results.extend(result)

        return results

    # ---------------------------------------------------------
    # RELATIONSHIP ROUTER
    # ---------------------------------------------------------

    def _retrieve_relationship(self, graph_query: GraphQuery):

        intent = graph_query.relationship_intent

        if not intent:
            return []

        # source + target
        if intent.source_entity and intent.target_entity:
            return self._retrieve_between_entities(
                source=intent.source_entity,
                target=intent.target_entity,
            )

        # source + relation
        if intent.source_entity and intent.relation:
            return self._retrieve_by_relation(
                source=intent.source_entity,
                relation=intent.relation,
            )

        # source only
        if intent.source_entity:
            return self._retrieve_connected_entities(
                source=intent.source_entity,
            )

        return []

    # ---------------------------------------------------------
    # RELATIONSHIP BETWEEN TWO ENTITIES
    # ---------------------------------------------------------

    def _retrieve_between_entities(
        self,
        source: str,
        target: str,
    ):

        query = """
        MATCH (a)-[r]->(b)
        WHERE
            toLower(a.id) = toLower($source)
            AND toLower(b.id) = toLower($target)

        RETURN
            a.id AS source,
            type(r) AS relation,
            b.id AS target

        LIMIT 20

        UNION

        MATCH (a)<-[r]-(b)
        WHERE
            toLower(a.id) = toLower($source)
            AND toLower(b.id) = toLower($target)

        RETURN
            a.id AS source,
            type(r) AS relation,
            b.id AS target

        LIMIT 20
        """

        return self.graph.query(
            query,
            params={
                "source": source,
                "target": target,
            },
        )

    # ---------------------------------------------------------
    # SOURCE + SPECIFIC RELATION
    # ---------------------------------------------------------

    def _retrieve_by_relation(
        self,
        source: str,
        relation: str,
    ):

        normalized_relation = relation.strip().upper()

        query = """
        MATCH (a)-[r]->(b)

        WHERE
            toLower(a.id) = toLower($source)
            AND toUpper(type(r)) = $relation

        RETURN
            a.id AS source,
            type(r) AS relation,
            b.id AS target

        LIMIT 20
        """

        return self.graph.query(
            query,
            params={
                "source": source,
                "relation": normalized_relation,
            },
        )

    # ---------------------------------------------------------
    # ALL RELATIONSHIPS OF ENTITY
    # ---------------------------------------------------------

    def _retrieve_connected_entities(
        self,
        source: str,
    ):

        query = """
        MATCH (a)-[r]-(b)

        WHERE toLower(a.id) = toLower($source)

        RETURN
            a.id AS source,
            type(r) AS relation,
            b.id AS target

        LIMIT 20
        """

        return self.graph.query(
            query,
            params={
                "source": source,
            },
        )