"""
Per-question result display components.
"""

from __future__ import annotations

import streamlit as st

from app.components.results_loader import (
    METRIC_LABELS,
    METRIC_NAMES,
    NormalisedSample,
    PipelineResults,
)


def _is_graph_context(context: str) -> bool:
    """Heuristic: graph contexts contain arrow notation like --REL-->."""
    return "--" in context and "-->" in context


def render_sample_expander(
    sample: NormalisedSample,
    index: int,
    pipeline_key: str = "",
) -> None:
    """Render a single evaluation sample inside an expander."""
    label = f"Q{index + 1}: {sample.question[:80]}{'…' if len(sample.question) > 80 else ''}"
    with st.expander(label, expanded=False):
        st.markdown("**Question**")
        st.write(sample.question)

        st.markdown("**Reference Answer**")
        st.write(sample.reference)

        st.markdown("**Generated Answer**")
        st.write(sample.response)

        if sample.category:
            st.caption(f"Category: {sample.category}")

        # Context rendering varies by pipeline type
        if pipeline_key == "hybrid_rag":
            _render_hybrid_contexts(sample.retrieved_contexts)
        elif pipeline_key == "graph_rag":
            _render_graph_contexts(sample.retrieved_contexts)
        else:
            _render_vector_contexts(sample.retrieved_contexts)

        # Per-sample metrics
        st.markdown("**Metrics**")
        metric_cols = st.columns(4)
        for col, name in zip(metric_cols, METRIC_NAMES):
            value = sample.metrics.get(name)
            display = f"{value:.4f}" if value is not None else "N/A"
            col.metric(label=METRIC_LABELS[name], value=display)


def _render_vector_contexts(contexts: list[str]) -> None:
    """Render vector retrieval contexts."""
    st.markdown("**Retrieved Contexts**")
    if not contexts:
        st.info("No contexts were retrieved for this question.")
        return
    for i, ctx in enumerate(contexts, 1):
        st.markdown(f"**Context {i}**")
        st.text(ctx[:500] + ("…" if len(ctx) > 500 else ""))


def _render_graph_contexts(contexts: list[str]) -> None:
    """Render graph retrieval contexts with distinctive formatting."""
    st.markdown("**Graph Retrieved Context**")
    if not contexts:
        st.info("No graph contexts were retrieved for this question.")
        return
    for i, ctx in enumerate(contexts, 1):
        st.markdown(f"**Context {i}**")
        st.code(ctx, language="text")


def _render_hybrid_contexts(contexts: list[str]) -> None:
    """Render hybrid contexts, separating vector and graph contexts."""
    vector_contexts = [c for c in contexts if not _is_graph_context(c)]
    graph_contexts = [c for c in contexts if _is_graph_context(c)]

    st.markdown("**Vector Contexts**")
    if vector_contexts:
        for i, ctx in enumerate(vector_contexts, 1):
            st.markdown(f"**Context {i}**")
            st.text(ctx[:500] + ("…" if len(ctx) > 500 else ""))
    else:
        st.info("No vector contexts were retrieved.")

    st.markdown("**Graph Contexts**")
    if graph_contexts:
        for i, ctx in enumerate(graph_contexts, 1):
            st.markdown(f"**Context {i}**")
            st.code(ctx, language="text")
    else:
        st.info("No graph contexts were retrieved.")

    st.markdown("**Combined Context**")
    if contexts:
        combined = "\n---\n".join(contexts)
        st.text(combined[:1000] + ("…" if len(combined) > 1000 else ""))
    else:
        st.info("No combined context available.")


def render_per_question_results(results: PipelineResults) -> None:
    """Render all per-question expanders for a pipeline."""
    if not results.samples:
        st.info("No evaluation samples available.")
        return

    st.subheader(f"Per-Question Results ({len(results.samples)} samples)")
    for i, sample in enumerate(results.samples):
        render_sample_expander(sample, i, pipeline_key=results.pipeline)


def render_question_comparison(all_results: dict[str, PipelineResults]) -> None:
    """Render a cross-pipeline comparison for each question on the Overview page."""
    loaded = {k: v for k, v in all_results.items() if v.loaded and v.samples}
    if not loaded:
        st.info("No per-question data available for comparison.")
        return

    first_pipeline = next(iter(loaded.values()))
    num_questions = len(first_pipeline.samples)

    st.subheader("Question-Level Comparison")

    for q_idx in range(num_questions):
        # Use the question text from the first available pipeline
        question_text = first_pipeline.samples[q_idx].question if q_idx < len(first_pipeline.samples) else f"Question {q_idx + 1}"
        label = f"Q{q_idx + 1}: {question_text[:80]}{'…' if len(question_text) > 80 else ''}"

        with st.expander(label, expanded=False):
            st.markdown("**Question**")
            st.write(question_text)

            for key, results in loaded.items():
                if q_idx < len(results.samples):
                    sample = results.samples[q_idx]
                    st.markdown(f"**{results.label} Answer**")
                    st.write(sample.response)

            # Show reference from any pipeline
            for key, results in loaded.items():
                if q_idx < len(results.samples):
                    st.markdown("**Reference Answer**")
                    st.write(results.samples[q_idx].reference)
                    break
