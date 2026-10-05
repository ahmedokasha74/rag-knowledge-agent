class GraphAnswerGenerator:

    def __init__(self, llm_provider):
        self.llm_provider = llm_provider

    def generate(self, query: str, context: str) -> str:

        prompt = f"""
You are an answer generation component in a GraphRAG system.

Answer the user's question using only the provided graph context.

Rules:
- Use only information supported by the graph context.
- Do not invent relationships or entities.
- If the context does not contain enough information, say so.
- Give a concise and direct answer.

USER QUESTION:
{query}

GRAPH CONTEXT:
{context}

ANSWER:
"""

        return self.llm_provider.generate_text(
            prompt=prompt,
            temperature=0,
        )