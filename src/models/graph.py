from typing import List, Optional

from pydantic import BaseModel, Field


class Entity(BaseModel):
    """
    A single entity extracted from a document chunk.
    The entity name is used as the canonical key when stored in Neo4j.
    """

    name: str = Field(
        ...,
        description="Canonical entity name used as the unique key in Neo4j."
    )

    type: str = Field(
        ...,
        description=(
            "Entity type or category, such as Plan, Policy, Feature, "
            "Team, Product, Service, or Person."
        )
    )

    description: Optional[str] = Field(
        default=None,
        description="Short description of the entity grounded in the source text."
    )


class Relation(BaseModel):
    """
    A directed relationship between two extracted entities.
    """

    source: str = Field(
        ...,
        description="Name of the source entity. Must match an Entity.name."
    )

    target: str = Field(
        ...,
        description="Name of the target entity. Must match an Entity.name."
    )

    relation_type: str = Field(
        ...,
        description=(
            "Relationship type in UPPER_SNAKE_CASE, such as "
            "REQUIRES, INCLUDES, APPLIES_TO, COVERED_BY, or DEPENDS_ON."
        )
    )

    description: Optional[str] = Field(
        default=None,
        description="Short explanation of the relationship grounded in the source text."
    )


class ExtractionResult(BaseModel):
    """
    Structured result produced by the entity and relation extraction step.
    """

    entities: List[Entity] = Field(default_factory=list)
    relations: List[Relation] = Field(default_factory=list)


class GraphChunk(BaseModel):
    """
    Extraction result associated with its original document chunk.
    """

    chunk_id: str = Field(
        ...,
        description="Unique identifier of the source chunk."
    )

    document_source: str = Field(
        ...,
        description="Original document source or filename."
    )

    text: str = Field(
        ...,
        description="Original chunk text from which the graph data was extracted."
    )

    entities: List[Entity] = Field(default_factory=list)

    relations: List[Relation] = Field(default_factory=list)


class GraphRetrievalResult(BaseModel):
    """
    Result returned by graph retrieval.
    """

    entities: List[Entity] = Field(default_factory=list)

    relations: List[Relation] = Field(default_factory=list)

    source_chunk_ids: List[str] = Field(default_factory=list)