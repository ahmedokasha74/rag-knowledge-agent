"""
Result-loading layer for the RAG Evaluation Dashboard.

Loads JSON evaluation results produced by the existing evaluation_runner
and normalises them into a consistent internal schema for the Streamlit UI.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


RESULTS_DIRECTORY = Path(__file__).resolve().parent.parent.parent / "evaluation" / "results"

METRIC_NAMES = [
    "faithfulness",
    "context_precision",
    "context_recall",
    "answer_relevancy",
]

METRIC_LABELS = {
    "faithfulness": "Faithfulness",
    "context_precision": "Context Precision",
    "context_recall": "Context Recall",
    "answer_relevancy": "Answer Relevancy",
}

PIPELINE_FILES = {
    "vector_rag": "vector_rag_results.json",
    "graph_rag": "graph_rag_results.json",
    "hybrid_rag": "hybrid_rag_results.json",
}

PIPELINE_LABELS = {
    "vector_rag": "Vector RAG",
    "graph_rag": "Graph RAG",
    "hybrid_rag": "Hybrid RAG",
}


@dataclass
class NormalisedSample:
    """A single evaluation sample in the normalised internal schema."""

    question: str = ""
    reference: str = ""
    response: str = ""
    category: str = ""
    retrieved_contexts: list[str] = field(default_factory=list)
    metrics: dict[str, float | None] = field(default_factory=dict)


@dataclass
class PipelineResults:
    """Complete evaluation results for one pipeline."""

    pipeline: str = ""
    label: str = ""
    loaded: bool = False
    error: str | None = None
    ragas_version: str = ""
    summary: dict[str, float | None] = field(default_factory=dict)
    samples: list[NormalisedSample] = field(default_factory=list)
    file_modified: float | None = None


def _safe_float(value: Any) -> float | None:
    """Convert a value to float, returning None for non-finite values."""
    if value is None:
        return None
    try:
        result = float(value)
        if result != result:  # NaN check
            return None
        return result
    except (TypeError, ValueError):
        return None


def _normalise_sample(raw: dict[str, Any]) -> NormalisedSample:
    """Normalise a single sample from the evaluation results JSON."""
    question = raw.get("user_input") or raw.get("question") or ""
    reference = raw.get("reference") or ""
    response = raw.get("response") or ""
    category = raw.get("category") or ""

    contexts = raw.get("retrieved_contexts", [])
    if not isinstance(contexts, list):
        contexts = []
    contexts = [str(c) for c in contexts if c]

    metric_scores = raw.get("metric_scores", {})
    if not isinstance(metric_scores, dict):
        metric_scores = {}

    metrics = {}
    for name in METRIC_NAMES:
        metrics[name] = _safe_float(metric_scores.get(name))

    return NormalisedSample(
        question=question,
        reference=reference,
        response=response,
        category=category,
        retrieved_contexts=contexts,
        metrics=metrics,
    )


def _load_single_result(pipeline_key: str) -> PipelineResults:
    """Load and normalise a single pipeline's result file."""
    label = PIPELINE_LABELS.get(pipeline_key, pipeline_key)
    filename = PIPELINE_FILES.get(pipeline_key)
    if not filename:
        return PipelineResults(
            pipeline=pipeline_key,
            label=label,
            error=f"Unknown pipeline key: {pipeline_key}",
        )

    filepath = RESULTS_DIRECTORY / filename
    if not filepath.exists():
        return PipelineResults(
            pipeline=pipeline_key,
            label=label,
            error=f"Result file not found: {filepath.name}",
        )

    try:
        file_size = filepath.stat().st_size
        if file_size == 0:
            return PipelineResults(
                pipeline=pipeline_key,
                label=label,
                error=f"Result file is empty: {filepath.name}",
            )

        file_modified = filepath.stat().st_mtime

        text = filepath.read_text(encoding="utf-8")
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return PipelineResults(
            pipeline=pipeline_key,
            label=label,
            error=f"Malformed JSON in {filepath.name}: {exc}",
        )
    except OSError as exc:
        return PipelineResults(
            pipeline=pipeline_key,
            label=label,
            error=f"Cannot read {filepath.name}: {exc}",
        )

    if not isinstance(data, dict):
        return PipelineResults(
            pipeline=pipeline_key,
            label=label,
            error=f"Unexpected JSON structure in {filepath.name}",
        )

    ragas_version = str(data.get("ragas_version", ""))

    raw_summary = data.get("summary", {})
    if not isinstance(raw_summary, dict):
        raw_summary = {}
    summary = {name: _safe_float(raw_summary.get(name)) for name in METRIC_NAMES}

    raw_samples = data.get("samples", [])
    if not isinstance(raw_samples, list):
        raw_samples = []

    samples = [_normalise_sample(s) for s in raw_samples if isinstance(s, dict)]

    return PipelineResults(
        pipeline=pipeline_key,
        label=label,
        loaded=True,
        ragas_version=ragas_version,
        summary=summary,
        samples=samples,
        file_modified=file_modified,
    )


class EvaluationResultsLoader:
    """Centralised loader for all pipeline evaluation results."""

    def __init__(self, results_dir: Path | None = None):
        self._results_dir = results_dir or RESULTS_DIRECTORY

    @property
    def results_directory(self) -> Path:
        return self._results_dir

    def load_vector_results(self) -> PipelineResults:
        return _load_single_result("vector_rag")

    def load_graph_results(self) -> PipelineResults:
        return _load_single_result("graph_rag")

    def load_hybrid_results(self) -> PipelineResults:
        return _load_single_result("hybrid_rag")

    def load_all(self) -> dict[str, PipelineResults]:
        return {
            "vector_rag": self.load_vector_results(),
            "graph_rag": self.load_graph_results(),
            "hybrid_rag": self.load_hybrid_results(),
        }

    def results_exist(self) -> dict[str, bool]:
        """Check which result files exist without fully loading them."""
        exists = {}
        for key, filename in PIPELINE_FILES.items():
            filepath = self._results_dir / filename
            exists[key] = filepath.exists() and filepath.stat().st_size > 0
        return exists

    def get_last_modified(self) -> float | None:
        """Return the most recent modification time across all result files."""
        latest = None
        for filename in PIPELINE_FILES.values():
            filepath = self._results_dir / filename
            if filepath.exists():
                mtime = filepath.stat().st_mtime
                if latest is None or mtime > latest:
                    latest = mtime
        return latest
