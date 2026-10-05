"""
Individual pipeline page renderers.
"""

from __future__ import annotations

import streamlit as st

from app.components.metrics import render_metric_cards
from app.components.results import render_per_question_results
from app.components.results_loader import PipelineResults


def render_pipeline_page(results: PipelineResults) -> None:
    """Render a full pipeline evaluation page (Vector, Graph, or Hybrid)."""
    st.title(f"{results.label} Evaluation")

    if not results.loaded:
        st.error(
            f"⚠️ {results.label} results could not be loaded.\n\n"
            f"**Reason:** {results.error or 'Unknown error'}\n\n"
            "Run the evaluation or check the result files in "
            "`src/evaluation/results/`."
        )
        return

    # Summary info
    info_cols = st.columns([2, 1, 1])
    with info_cols[0]:
        if results.ragas_version:
            st.caption(f"RAGAS version: {results.ragas_version}")
    with info_cols[1]:
        st.metric("Evaluated Samples", len(results.samples))
    with info_cols[2]:
        if results.file_modified:
            from datetime import datetime
            ts = datetime.fromtimestamp(results.file_modified)
            st.caption(f"Last updated: {ts.strftime('%Y-%m-%d %H:%M')}")

    st.divider()

    # RAGAS Metrics overview
    st.subheader("RAGAS Metrics")
    render_metric_cards(results)

    st.divider()

    # Per-question results
    render_per_question_results(results)
