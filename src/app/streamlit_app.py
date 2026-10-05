"""Interactive Streamlit interface for the existing Cloudify RAG pipelines."""

from __future__ import annotations

import asyncio
import time
from collections.abc import Mapping

import streamlit as st

from controllers.GraphRag.graph_answer_generator import GraphAnswerGenerator
from controllers.GraphRag.retrieval.graph_context_builder import GraphContextBuilder
from controllers.GraphRag.retrieval.graph_retriever import GraphRetriever
from controllers.GraphRag.retrieval.query_entity_extractor import QueryEntityExtractor
from controllers.HybridRag.hybrid_rag_pipeline import HybridRagPipeline
from controllers.HybridRag.hybrid_retriever import HybridRetriever
from controllers.rag.RAGPipeline import RAGPipeline
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory

COLLECTION_NAME = "cloudify_documents"
MODES = ("Vector RAG", "Graph RAG", "Hybrid RAG")
MODE_DESCRIPTIONS = {
    "Vector RAG": "Semantic retrieval using Qdrant vector search.",
    "Graph RAG": "Relationship-based retrieval using Neo4j.",
    "Hybrid RAG": "Combines vector retrieval from Qdrant with graph retrieval from Neo4j.",
}
MODE_ICONS = {
    "Vector RAG": ":material/travel_explore:",
    "Graph RAG": ":material/account_tree:",
    "Hybrid RAG": ":material/hub:",
}

st.set_page_config(
    page_title="RAG Knowledge Agent",
    page_icon="🔎",
    layout="centered",
    initial_sidebar_state="expanded",
)


@st.cache_resource(show_spinner=False)
def get_pipelines():
    """Create the existing pipeline and graph components once per app process."""
    settings = get_settings()
    vector = RAGPipeline(config=settings)

    llm_factory = LLMProviderFactory(config=settings)
    graph_llm = llm_factory.create(provider=settings.GRAPH_EXTRACTION_BACKEND)
    graph_model = settings.GRAPH_EXTRACTION_MODEL_ID or settings.GENERATION_MODEL_ID
    if not graph_model:
        raise ValueError("No model is configured for Graph RAG.")
    graph_llm.set_generation_model(graph_model)

    extractor = QueryEntityExtractor(llm_provider=graph_llm)
    graph_retriever = GraphRetriever(config=settings)
    graph_context = GraphContextBuilder()
    graph_answer = GraphAnswerGenerator(llm_provider=graph_llm)
    hybrid = HybridRagPipeline(
        config=settings,
        hybrid_retriever=HybridRetriever(
            config=settings,
            vector_retriever=vector.retrieval_controller,
            graph_retriever=graph_retriever,
            query_entity_extractor=extractor,
        ),
    )
    return settings, vector, extractor, graph_retriever, graph_context, graph_answer, hybrid


async def run_vector(pipeline, settings, query: str, limit: int) -> dict:
    provider = pipeline.retrieval_controller.vector_db_provider
    await provider.connect()
    try:
        started = time.perf_counter()
        docs = await pipeline.retrieve(
            query=query,
            collection_name=COLLECTION_NAME,
            limit=limit,
            score_threshold=settings.SCORE_THRESHOLD,
        )
        retrieval_time = time.perf_counter() - started
        prompt = pipeline.build_prompt(query=query, retrieved_documents=docs)
        started = time.perf_counter()
        answer = await pipeline.generate(prompt=prompt)
        generation_time = time.perf_counter() - started
        return {
            "answer": answer,
            "documents": docs,
            "retrieval_time": retrieval_time,
            "generation_time": generation_time,
            "total_time": retrieval_time + generation_time,
        }
    finally:
        await provider.disconnect()


def run_graph(query, extractor, retriever, context_builder, answer_generator) -> dict:
    started = time.perf_counter()
    graph_query = extractor.extract(query)
    results = retriever.retrieve(graph_query)
    context = context_builder.build(results) or "No graph results retrieved."
    retrieval_time = time.perf_counter() - started
    started = time.perf_counter()
    answer = answer_generator.generate(query=query, context=context)
    generation_time = time.perf_counter() - started
    return {
        "answer": answer, "graph_context": context, "graph_query": graph_query,
        "retrieval_time": retrieval_time,
        "generation_time": generation_time,
        "total_time": retrieval_time + generation_time,
    }


async def run_hybrid(pipeline, settings, query: str, limit: int) -> dict:
    await pipeline.connect()
    try:
        started = time.perf_counter()
        result = await pipeline.query(
            query=query,
            collection_name=COLLECTION_NAME,
            limit=limit,
            score_threshold=settings.SCORE_THRESHOLD,
        )
        return {**result, "total_time": time.perf_counter() - started}
    finally:
        await pipeline.disconnect()


def field(item, key, default=None):
    return item.get(key, default) if isinstance(item, Mapping) else getattr(item, key, default)


def show_documents(documents) -> None:
    if not documents:
        st.caption("No documents met the retrieval threshold.")
        return
    for index, document in enumerate(documents, 1):
        score = field(document, "score")
        title = f"Document {index}"
        if score is not None:
            title += f" | Score {score:.3f}"
        with st.expander(title):
            if score is not None:
                st.caption(f"Similarity score: {score:.3f}")
            metadata = field(document, "metadata", {})
            source = field(document, "source")
            if source:
                st.caption(f"Source: {source}")
            if metadata:
                st.caption("Metadata")
                st.json(metadata)
            st.markdown(field(document, "text", str(document)))


def show_context(mode: str, result: dict) -> None:
    with st.expander("Retrieved context", icon=":material/search:"):
        if mode == "Vector RAG":
            st.markdown(f"**:blue[:material/travel_explore: Vector context]** | {len(result.get('documents', []))} documents retrieved")
            show_documents(result.get("documents", []))
        elif mode == "Graph RAG":
            st.markdown("**:violet[:material/account_tree: Graph context]**")
            graph_query = result.get("graph_query")
            if graph_query:
                st.markdown("**Extracted graph query**")
                intent = graph_query.relationship_intent
                st.write(f"Query type: {graph_query.query_type}")
                if intent:
                    if intent.source_entity:
                        st.write(f"Source entity: {intent.source_entity}")
                    if intent.relation:
                        st.write(f"Relationship: {intent.relation}")
                    st.write(f"Target: {intent.target_entity or 'Not specified'}")
                elif graph_query.entities:
                    st.write("Entities: " + ", ".join(entity.name for entity in graph_query.entities))
            st.markdown("**Graph context**")
            st.code(result.get("graph_context", "No graph results retrieved."), language="text")
        else:
            vector_results = result.get("vector_results", [])
            graph_context = result.get("graph_context", "No graph results retrieved.")
            relationships = [line for line in graph_context.splitlines() if " --" in line and "--> " in line]
            st.markdown(f"**:blue[:material/travel_explore: Vector context]** | {len(vector_results)} documents retrieved")
            show_documents(vector_results)
            st.markdown(f"**:violet[:material/account_tree: Graph context]** · {len(relationships)} relationships retrieved")
            st.code(result.get("graph_context", "No graph results retrieved."), language="text")


def error_message(exc: Exception) -> str:
    message = str(exc).lower()
    if any(term in message for term in ("api key", "authentication", "unauthorized", "401")):
        return "The configured language model or embedding provider could not authenticate. Check its environment configuration."
    if any(term in message for term in ("qdrant", "collection", "vector")):
        return "The vector knowledge base is unavailable. Check that Qdrant is running and the `cloudify_documents` collection exists."
    if any(term in message for term in ("neo4j", "bolt", "serviceunavailable")):
        return "The graph knowledge base is unavailable. Check that Neo4j is running and its connection settings are correct."
    if isinstance(exc, (ValueError, TypeError)):
        return f"This question could not be processed: {exc}"
    return "The RAG request failed. Check the configured model and knowledge base services, then try again."


def render_message(message: dict) -> None:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(message["content"])
            return
        details = message.get("details")
        mode = message.get("rag_mode") or (details[0] if details else None)
        if mode:
            st.markdown(f"**{MODE_ICONS[mode]} {mode}**")
        st.markdown(message["content"])
        if details:
            _, result = details
            show_context(mode, result)
            show_performance(result)


def show_performance(result: dict) -> None:
    metrics = []
    if "retrieval_time" in result:
        metrics.append(f"Retrieval: {result['retrieval_time']:.2f}s")
    if "generation_time" in result:
        metrics.append(f"Generation: {result['generation_time']:.2f}s")
    if "total_time" in result:
        metrics.append(f"Total: {result['total_time']:.2f}s")
    if metrics:
        st.caption(":material/bolt: " + " | ".join(metrics))


def main() -> None:
    st.session_state.setdefault("messages", [])
    with st.sidebar:
        st.title("RAG Knowledge Agent")
        mode = st.radio("RAG Mode", MODES, index=0)
        st.caption(MODE_DESCRIPTIONS[mode])
        st.markdown("**Knowledge Base**")
        st.caption("Cloudify Knowledge Base")
        limit = st.number_input("Retrieved documents", min_value=1, max_value=20, value=5, step=1)
        if st.button("Clear chat", icon=":material/delete_sweep:", width="stretch"):
            st.session_state.messages = []
            st.rerun()

    st.title("RAG Knowledge Agent")
    st.caption("Ask questions about your knowledge base using Vector RAG, Graph RAG, or Hybrid RAG.")
    for message in st.session_state.messages:
        render_message(message)

    query = st.chat_input("Ask something about the knowledge base...")
    if not query:
        return
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
    try:
        with st.chat_message("assistant"):
            with st.spinner("Retrieving relevant knowledge and generating an answer..."):
                settings, vector, extractor, graph_retriever, graph_context, graph_answer, hybrid = get_pipelines()
                if mode == "Vector RAG":
                    result = asyncio.run(run_vector(vector, settings, query, int(limit)))
                elif mode == "Graph RAG":
                    result = run_graph(query, extractor, graph_retriever, graph_context, graph_answer)
                else:
                    result = asyncio.run(run_hybrid(hybrid, settings, query, int(limit)))
            answer = result.get("answer") or "The knowledge base did not return an answer."
            st.markdown(f"**{MODE_ICONS[mode]} {mode}**")
            st.markdown(answer)
            show_context(mode, result)
            show_performance(result)
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "rag_mode": mode,
            "details": (mode, result),
        })
    except Exception as exc:
        message = error_message(exc)
        st.error(message)
        st.session_state.messages.append({"role": "assistant", "content": message})


if __name__ == "__main__":
    main()
