from collections.abc import Sequence

from controllers.BaseController import BaseController
from helpers.config import get_settings
from models.graph import Entity, GraphRetrievalResult, Relation

from langchain_neo4j import Neo4jGraph


class GraphRetriever(BaseController):
    """
    Retrieve entities and relationships from the Neo4j knowledge graph.
    """

    def __init__(self, config=None, graph=None):
        super().__init__()

        self.settings = config or get_settings()
        self.graph = graph or Neo4jGraph(
            url=self.settings.NEO4J_URI,
            username=self.settings.NEO4J_USER,
            password=self.settings.NEO4J_PASSWORD,
        )

    def retrieve(
        self,
        entity_names: str | Sequence[str],
        max_hops: int | None = None,
        max_results: int | None = None,
    ) -> GraphRetrievalResult:
        """
        Retrieve a graph neighborhood around one or more entity names.

        Args:
            entity_names: Entity name or names used as graph entry points.
            max_hops: Maximum number of relationship hops to traverse.
            max_results: Maximum number of entities returned.
        """
        names = self._normalize_entity_names(entity_names)
        if not names:
            return GraphRetrievalResult()

        hops = self._positive_int(
            max_hops,
            self.settings.GRAPH_RETRIEVAL_MAX_HOPS,
        )
        result_limit = self._positive_int(
            max_results,
            self.settings.GRAPH_RETRIEVAL_MAX_RESULTS,
        )

        node_rows = self.graph.query(
            f"""
            MATCH (root)
            WHERE toLower(root.id) IN $entity_names
            MATCH (root)-[*0..{hops}]-(node)
            RETURN DISTINCT node.id AS id,
                   node.type AS type,
                   properties(node) AS properties
            LIMIT $max_results
            """,
            params={
                "entity_names": [name.lower() for name in names],
                "max_results": result_limit,
            },
        )

        relation_rows = self.graph.query(
            f"""
            MATCH (root)
            WHERE toLower(root.id) IN $entity_names
            MATCH path=(root)-[*1..{hops}]-(neighbor)
            UNWIND relationships(path) AS relation
            RETURN DISTINCT startNode(relation).id AS source,
                   endNode(relation).id AS target,
                   type(relation) AS relation_type,
                   properties(relation) AS properties
            LIMIT $max_results
            """,
            params={
                "entity_names": [name.lower() for name in names],
                "max_results": result_limit,
            },
        )

        entities = []
        source_chunk_ids = set()
        for row in node_rows:
            properties = row.get("properties") or {}
            entities.append(
                Entity(
                    name=str(row["id"]),
                    type=str(row.get("type") or "Entity"),
                    description=properties.get("description"),
                )
            )
            for key in ("chunk_id", "source_chunk_id"):
                if properties.get(key):
                    source_chunk_ids.add(str(properties[key]))

        relations = [
            Relation(
                source=str(row["source"]),
                target=str(row["target"]),
                relation_type=str(row["relation_type"]),
                description=(row.get("properties") or {}).get("description"),
            )
            for row in relation_rows
            if row.get("source") and row.get("target")
        ]

        return GraphRetrievalResult(
            entities=entities,
            relations=relations,
            source_chunk_ids=sorted(source_chunk_ids),
        )

    def retrieve_by_entity(
        self,
        entity_name: str,
        max_hops: int | None = None,
        max_results: int | None = None,
    ) -> GraphRetrievalResult:
        """Retrieve a graph neighborhood around one entity."""
        return self.retrieve(
            entity_names=entity_name,
            max_hops=max_hops,
            max_results=max_results,
        )

    @staticmethod
    def _normalize_entity_names(
        entity_names: str | Sequence[str],
    ) -> list[str]:
        if isinstance(entity_names, str):
            entity_names = [entity_names]

        return [
            name.strip()
            for name in entity_names
            if isinstance(name, str) and name.strip()
        ]

    @staticmethod
    def _positive_int(value: int | None, default: int) -> int:
        selected = default if value is None else value
        if selected < 1:
            raise ValueError("Graph retrieval limits must be positive integers.")
        return selected
