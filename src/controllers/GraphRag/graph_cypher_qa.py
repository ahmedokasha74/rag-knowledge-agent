from controllers.BaseController import BaseController
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory

from langchain_core.prompts import PromptTemplate
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain


class GraphCypherQA(BaseController):

    def __init__(self, config=None):
        super().__init__()

        self.settings = config or get_settings()

        # =========================================================
        # LLM Provider
        # =========================================================

        self.llm_factory = LLMProviderFactory(
            config=self.settings
        )

        self.llm_provider = self.llm_factory.create(
            provider=self.settings.GRAPH_EXTRACTION_BACKEND
        )

        model_id = (
            self.settings.GRAPH_EXTRACTION_MODEL_ID
            or self.settings.GENERATION_MODEL_ID
        )

        if not model_id:
            raise ValueError(
                "No generation model configured."
            )

        self.llm_provider.set_generation_model(
            model_id
        )

        # =========================================================
        # Chat Model
        # =========================================================

        self.chat_model = self.llm_provider.get_chat_model()

        # =========================================================
        # Neo4j
        # =========================================================

        self.graph = Neo4jGraph(
            url=self.settings.NEO4J_URI,
            username=self.settings.NEO4J_USER,
            password=self.settings.NEO4J_PASSWORD,
        )

        # =========================================================
        # Few-Shot Examples
        # =========================================================

        self.cypher_examples = [
            {
                "question": "What plans does Cloudify offer?",
                "cypher": """
MATCH (c {id: "Cloudify"})-[:OFFERS]->(p)
RETURN p.id
"""
            },
            {
                "question": (
                    "What is the relationship between "
                    "Cloudify and Professional?"
                ),
                "cypher": """
MATCH (a {id: "Cloudify"})-[r]-(b {id: "Professional"})
RETURN a.id, type(r), b.id
"""
            },
            {
                "question": "What is connected to Cloudify?",
                "cypher": """
MATCH (c {id: "Cloudify"})-[r]-(n)
RETURN c.id, type(r), n.id
"""
            },
        ]

        # =========================================================
        # Cypher Prompt
        # =========================================================

        self.cypher_prompt = PromptTemplate(
            input_variables=[
                "schema",
                "question",
            ],
            template="""
You are an expert Neo4j Cypher developer.

Your task is to generate ONE read-only Cypher query
that answers the user's question.

Use ONLY the labels, relationships, and properties
available in the provided Neo4j schema.

Important rules:

1. Entity names are stored in the `id` property.
2. Do NOT use `name` unless it exists in the schema.
3. Do NOT invent node properties.
4. Do NOT invent relationship types.
5. Use the relationship types exactly as they appear
   in the schema.
6. Generate a read-only query only.
7. Do not use CREATE, DELETE, SET, MERGE, DROP,
   REMOVE, or other write operations.
8. Return ONLY the Cypher query.
9. Prefer simple Cypher queries.
10. When matching entities by their canonical name,
    use the `id` property.

------------------------------------------------------------
EXAMPLES
------------------------------------------------------------

Example 1:

Question:
What plans does Cloudify offer?

Cypher:
MATCH (c {{id: "Cloudify"}})-[:OFFERS]->(p)
RETURN p.id


Example 2:

Question:
What is the relationship between Cloudify and Professional?

Cypher:
MATCH (a {{id: "Cloudify"}})-[r]-(b {{id: "Professional"}})
RETURN a.id, type(r), b.id


Example 3:

Question:
What is connected to Cloudify?

Cypher:
MATCH (c {{id: "Cloudify"}})-[r]-(n)
RETURN c.id, type(r), n.id

------------------------------------------------------------
SCHEMA
------------------------------------------------------------

{schema}

------------------------------------------------------------
USER QUESTION
------------------------------------------------------------

{question}

------------------------------------------------------------
CYPHER
------------------------------------------------------------
"""
        )

        # =========================================================
        # Graph Cypher QA Chain
        # =========================================================

        self.chain = GraphCypherQAChain.from_llm(
            llm=self.chat_model,
            graph=self.graph,
            cypher_prompt=self.cypher_prompt,
            verbose=True,
            allow_dangerous_requests=True,
        )

    # =============================================================
    # Public API
    # =============================================================

    def ask(self, query: str):

        return self.chain.invoke(
            {
                "query": query
            }
        )