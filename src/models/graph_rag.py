from pydantic import BaseModel, Field
from typing import Optional


class QueryEntity(BaseModel):
    name: str = Field(
        description="Canonical name of the entity mentioned in the query."
    )

    type: Optional[str] = Field(
        default=None,
        description="Entity type when it can be determined."
    )


class RelationshipIntent(BaseModel):
    source_entity: Optional[str] = Field(
        default=None,
        description="Entity from which the relationship originates."
    )

    target_entity: Optional[str] = Field(
        default=None,
        description="Entity at the other end of the relationship."
    )

    relation: Optional[str] = Field(
        default=None,
        description=(
            "The relationship explicitly requested by the user. "
            "Use null when the user asks for an unspecified relationship."
        )
    )


class GraphQuery(BaseModel):
    query_type: str = Field(
        description=(
            "Type of graph query. "
            "Use ENTITY when the user asks about one entity itself. "
            "Use RELATIONSHIP when the user asks about a relationship "
            "between entities or about entities connected by a specific relation."
        )
    )

    entities: list[QueryEntity] = Field(
        default_factory=list
    )

    relationship_intent: Optional[RelationshipIntent] = None