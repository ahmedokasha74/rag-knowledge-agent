from collections.abc import Mapping

from controllers.GraphRag.retrieval.graph_context_builder import (
    GraphContextBuilder,
)


class HybridContextBuilder:
    def __init__(self, graph_context_builder=None):
        self.graph_context_builder = (
            graph_context_builder or GraphContextBuilder()
        )

    @staticmethod
    def _value(item, key, default=None):
        if isinstance(item, Mapping):
            return item.get(key, default)
        return getattr(item, key, default)

    def build(
        self,
        vector_results: list,
        graph_results: list[dict],
    ) -> dict[str, str]:
        vector_lines = []
        for index, result in enumerate(vector_results, start=1):
            text = self._value(result, "text", "")
            score = self._value(result, "score")
            metadata = self._value(result, "metadata")
            score_label = f" | score: {score:.4f}" if score is not None else ""
            vector_lines.append(f"[Vector Result {index}{score_label}]\n{text}")
            if metadata:
                vector_lines.append(f"Metadata: {metadata}")

        vector_context = "\n\n".join(vector_lines)
        if not vector_context:
            vector_context = "No vector results retrieved."

        graph_lines = []
        for result in graph_results:
            entity = self._value(result, "entity")
            labels = self._value(result, "labels", [])
            if entity:
                label_text = ", ".join(labels) if labels else "Entity"
                graph_lines.append(f"{entity} ({label_text})")

        relationship_context = self.graph_context_builder.build(graph_results)
        if relationship_context:
            graph_lines.append(relationship_context)

        graph_context = "\n".join(graph_lines)
        if not graph_context:
            graph_context = "No graph results retrieved."

        combined_context = (
            "VECTOR CONTEXT:\n"
            "----------------\n"
            f"{vector_context}\n\n"
            "GRAPH CONTEXT:\n"
            "--------------\n"
            f"{graph_context}"
        )

        return {
            "vector_context": vector_context,
            "graph_context": graph_context,
            "combined_context": combined_context,
        }