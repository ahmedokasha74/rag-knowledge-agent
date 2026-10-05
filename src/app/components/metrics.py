"""
Reusable metric display components for the Streamlit dashboard.
"""

from __future__ import annotations

import streamlit as st

from app.components.results_loader import (
    METRIC_LABELS,
    METRIC_NAMES,
    PipelineResults,
)


def render_metric_cards(results: PipelineResults) -> None:
    """Render the four RAGAS metrics as st.metric cards in a row."""
    cols = st.columns(4)
    for col, name in zip(cols, METRIC_NAMES):
        label = METRIC_LABELS[name]
        value = results.summary.get(name)
        display = f"{value:.4f}" if value is not None else "N/A"
        col.metric(label=label, value=display)


def render_comparison_table(all_results: dict[str, PipelineResults]) -> None:
    """Render a side-by-side metric comparison table."""
    import pandas as pd

    rows = []
    for name in METRIC_NAMES:
        row = {"Metric": METRIC_LABELS[name]}
        for key, results in all_results.items():
            if results.loaded:
                value = results.summary.get(name)
                row[results.label] = f"{value:.4f}" if value is not None else "N/A"
            else:
                row[results.label] = "—"
        rows.append(row)

    df = pd.DataFrame(rows)
    df = df.set_index("Metric")
    st.dataframe(df, use_container_width=True)


def render_comparison_chart(all_results: dict[str, PipelineResults]) -> None:
    """Render a grouped bar chart comparing all pipelines across metrics."""
    import pandas as pd

    chart_data = {}
    for key, results in all_results.items():
        if results.loaded:
            values = []
            for name in METRIC_NAMES:
                v = results.summary.get(name)
                values.append(v if v is not None else 0.0)
            chart_data[results.label] = values

    if not chart_data:
        st.info("No evaluation data available to chart.")
        return

    df = pd.DataFrame(
        chart_data,
        index=[METRIC_LABELS[n] for n in METRIC_NAMES],
    )
    st.bar_chart(df)
