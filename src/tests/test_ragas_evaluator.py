import asyncio
import math
from types import SimpleNamespace

import pytest
from pydantic import BaseModel

from evaluation.ragas_evaluator import (
    NO_CONTEXT,
    RagasEvaluator,
)


class FakeLLMProvider:
    def __init__(self):
        self.last_kwargs = None

    def generate_structured(self, prompt, response_model, **kwargs):
        self.last_kwargs = kwargs
        return response_model.model_construct()


class FakeEmbeddingProvider:
    pass


class FakeStructuredResponse(BaseModel):
    value: str | None = None


def make_evaluator():
    return RagasEvaluator(
        llm_provider=FakeLLMProvider(),
        embedding_provider=FakeEmbeddingProvider(),
    )


def test_ragas_evaluator_loads_requested_metrics():
    evaluator = make_evaluator()

    assert evaluator.ragas_version == "0.4.3"
    assert list(evaluator.metrics) == [
        "faithfulness",
        "context_precision",
        "context_recall",
        "answer_relevancy",
    ]


def test_empty_context_is_explicit_for_ragas():
    rows = RagasEvaluator._validate_rows(
        [
            {
                "user_input": "What is Cloudify?",
                "retrieved_contexts": [],
                "response": "Cloudify is a platform.",
                "reference": "Cloudify is a SaaS company.",
            }
        ]
    )

    assert rows[0]["retrieved_contexts"] == [NO_CONTEXT]


def test_invalid_answer_is_reported():
    with pytest.raises(ValueError, match="response"):
        RagasEvaluator._validate_rows(
            [
                {
                    "user_input": "What is Cloudify?",
                    "retrieved_contexts": [],
                    "response": " ",
                    "reference": "Cloudify is a SaaS company.",
                }
            ]
        )


def test_provider_llm_adapter_rejects_empty_structured_output():
    class EmptyProvider:
        last_generation_error = (
            "429 rate limit reached on tokens per day (TPD); retry after 5m."
        )

        def generate_structured(self, prompt, response_model, **kwargs):
            return None

    evaluator = RagasEvaluator(
        llm_provider=EmptyProvider(),
        embedding_provider=FakeEmbeddingProvider(),
    )
    with pytest.raises(RuntimeError, match=r"token-per-day limit \(TPD\)"):
        evaluator.llm.generate("Evaluate this answer.", response_model=dict)


def test_provider_llm_adapter_uses_evaluation_output_budget():
    provider = FakeLLMProvider()
    evaluator = RagasEvaluator(
        llm_provider=provider,
        embedding_provider=FakeEmbeddingProvider(),
    )

    evaluator.llm.generate(
        "Evaluate this answer.",
        response_model=FakeStructuredResponse,
    )

    assert provider.last_kwargs["max_output_tokens"] == 1024


def test_non_finite_metric_scores_become_json_null():
    scores = RagasEvaluator._json_safe_scores(
        {
            "faithfulness": 0.75,
            "context_recall": math.nan,
        }
    )

    assert scores == {
        "faithfulness": 0.75,
        "context_recall": None,
    }


def test_evaluate_builds_dataset_and_returns_metric_summary():
    evaluator = make_evaluator()

    class FakeMetric:
        async def ascore(self, **kwargs):
            assert kwargs["user_input"] == "What is Cloudify?"
            return SimpleNamespace(value=0.8)

    evaluator.metrics = {"faithfulness": FakeMetric()}
    result = asyncio.run(
        evaluator.evaluate(
            [
                {
                    "user_input": "What is Cloudify?",
                    "retrieved_contexts": ["Cloudify is a SaaS company."],
                    "response": "Cloudify is a SaaS company.",
                    "reference": "Cloudify is a SaaS company.",
                }
            ]
        )
    )

    assert result["summary"] == {"faithfulness": 0.8}
    assert result["scores"] == [{"faithfulness": 0.8}]


def test_evaluate_resumes_completed_metric_scores():
    evaluator = make_evaluator()

    class MustNotRunMetric:
        async def ascore(self, **kwargs):
            raise AssertionError("completed metric was called again")

    evaluator.metrics = {"faithfulness": MustNotRunMetric()}
    result = asyncio.run(
        evaluator.evaluate(
            [
                {
                    "user_input": "What is Cloudify?",
                    "retrieved_contexts": ["Cloudify is a SaaS company."],
                    "response": "Cloudify is a SaaS company.",
                    "reference": "Cloudify is a SaaS company.",
                }
            ],
            completed_scores=[{"faithfulness": 0.9}],
        )
    )

    assert result["scores"] == [{"faithfulness": 0.9}]


def test_evaluate_scores_samples_sequentially():
    evaluator = make_evaluator()
    active = 0
    peak_active = 0

    class ConcurrentMetric:
        async def ascore(self, **kwargs):
            nonlocal active, peak_active
            active += 1
            peak_active = max(peak_active, active)
            await asyncio.sleep(0.01)
            active -= 1
            return SimpleNamespace(value=0.7)

    evaluator.metrics = {"faithfulness": ConcurrentMetric()}
    rows = [
        {
            "user_input": f"Question {index}?",
            "retrieved_contexts": ["Grounded context."],
            "response": "Grounded answer.",
            "reference": "Grounded reference.",
        }
        for index in range(5)
    ]
    progress = []
    result = asyncio.run(
        evaluator.evaluate(
            rows,
            progress_callback=lambda done, total: progress.append((done, total)),
        )
    )

    assert peak_active == 1
    assert progress[-1] == (5, 5)
    assert len(result["scores"]) == 5


def test_provider_llm_adapter_retries_rate_limits(monkeypatch):
    class RateLimitedProvider(FakeLLMProvider):
        def __init__(self):
            super().__init__()
            self.calls = 0
            self.last_generation_error = None

        def generate_structured(self, prompt, response_model, **kwargs):
            self.calls += 1
            if self.calls == 1:
                self.last_generation_error = (
                    "429 rate limit reached. Please try again in 4.305s."
                )
                return None
            return response_model.model_construct()

    waits = []
    monkeypatch.setattr("evaluation.ragas_evaluator.time.sleep", waits.append)
    provider = RateLimitedProvider()
    evaluator = RagasEvaluator(
        llm_provider=provider,
        embedding_provider=FakeEmbeddingProvider(),
    )

    result = evaluator.llm.generate(
        "Evaluate this answer.",
        response_model=FakeStructuredResponse,
    )

    assert isinstance(result, FakeStructuredResponse)
    assert provider.calls == 2
    assert waits == [4.305]


def test_provider_llm_adapter_does_not_retry_daily_rate_limit(monkeypatch):
    class DailyLimitedProvider(FakeLLMProvider):
        def __init__(self):
            super().__init__()
            self.calls = 0
            self.last_generation_error = (
                "429 rate limit reached on tokens per day (TPD). "
                "Please try again in 6m18s."
            )

        def generate_structured(self, prompt, response_model, **kwargs):
            self.calls += 1
            return None

    waits = []
    monkeypatch.setattr("evaluation.ragas_evaluator.time.sleep", waits.append)
    provider = DailyLimitedProvider()
    evaluator = RagasEvaluator(
        llm_provider=provider,
        embedding_provider=FakeEmbeddingProvider(),
    )

    with pytest.raises(RuntimeError, match=r"token-per-day limit \(TPD\)"):
        evaluator.llm.generate(
            "Evaluate this answer.",
            response_model=FakeStructuredResponse,
        )

    assert provider.calls == 1
    assert waits == []