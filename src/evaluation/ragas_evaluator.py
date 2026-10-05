import asyncio
import importlib
import importlib.metadata
import math
import re
import sys
import time
import types
from copy import deepcopy
from collections.abc import Mapping, Sequence
from statistics import mean
from typing import Any


NO_CONTEXT = "No context was retrieved for this question."


def _install_optional_vertex_compatibility() -> None:
    """Bridge RAGAS's legacy optional Vertex type import on LC Community 0.4+."""
    module_name = "langchain_community.chat_models.vertexai"
    try:
        importlib.import_module(module_name)
    except ModuleNotFoundError as error:
        if error.name != module_name:
            raise
        module = types.ModuleType(module_name)
        module.ChatVertexAI = type("ChatVertexAI", (), {})
        sys.modules[module_name] = module


class RagasEvaluator:
    def __init__(self, llm_provider, embedding_provider):
        try:
            _install_optional_vertex_compatibility()
            from ragas.embeddings.base import BaseRagasEmbedding
            from ragas.dataset_schema import EvaluationDataset, SingleTurnSample
            from ragas.llms.base import InstructorBaseRagasLLM
            from ragas.metrics.collections import (
                AnswerRelevancy,
                ContextPrecisionWithReference,
                ContextRecall,
                Faithfulness,
            )
        except ModuleNotFoundError as error:
            if error.name == "ragas":
                raise RuntimeError(
                    "RAGAS is not installed. Run `uv sync` to install the project dependencies."
                ) from error
            raise RuntimeError(
                f"RAGAS could not load a required dependency: {error.name}. "
                "Check the locked RAGAS/LangChain versions."
            ) from error
        except ImportError as error:
            raise RuntimeError(
                "The installed RAGAS release does not expose the required "
                "EvaluationDataset and production RAG metrics."
            ) from error

        self._evaluation_dataset_type = EvaluationDataset
        self._single_turn_sample_type = SingleTurnSample

        class ProviderRagasLLM(InstructorBaseRagasLLM):
            def generate(self, prompt, response_model):
                max_retries = 3
                for attempt in range(max_retries + 1):
                    response = llm_provider.generate_structured(
                        prompt=prompt,
                        response_model=response_model,
                        temperature=0,
                        max_output_tokens=1024,
                    )
                    if response is not None:
                        return response

                    provider_error = getattr(
                        llm_provider,
                        "last_generation_error",
                        None,
                    )
                    if not provider_error or "429" not in provider_error:
                        break
                    if "TPD" in provider_error.upper():
                        break
                    if attempt == max_retries:
                        break

                    wait_match = re.search(
                        r"try again in\s+([0-9.]+)\s*(s|sec|seconds|m|min|minutes)",
                        provider_error,
                        re.IGNORECASE,
                    )
                    wait_seconds = 2**attempt
                    if wait_match:
                        wait_seconds = float(wait_match.group(1))
                        if wait_match.group(2).lower().startswith("m"):
                            wait_seconds *= 60
                        if wait_seconds > 60:
                            break
                    wait_seconds = max(wait_seconds, 1)
                    time.sleep(wait_seconds)

                if response is None:
                    provider_error = getattr(
                        llm_provider,
                        "last_generation_error",
                        None,
                    )
                    details = (
                        f" Provider error: {provider_error}"
                        if provider_error
                        else ""
                    )
                    if provider_error and "TPD" in provider_error.upper():
                        raise RuntimeError(
                            "Groq's token-per-day limit (TPD) has been reached. "
                            "Evaluation stopped without retrying; wait for the "
                            "provider's stated reset window or configure a different "
                            f"evaluation LLM.{details}"
                        )
                    raise RuntimeError(
                        "The configured LLM failed to return structured output "
                        f"for a RAGAS metric.{details}"
                    )
                return response

            async def agenerate(self, prompt, response_model):
                return await asyncio.to_thread(
                    self.generate,
                    prompt,
                    response_model,
                )

        class ProviderRagasEmbedding(BaseRagasEmbedding):
            def embed_text(self, text, **kwargs):
                vector = embedding_provider.embed_text(
                    text=text,
                    document_type="query",
                )
                if not vector:
                    raise RuntimeError(
                        "The configured embedding provider returned an empty vector."
                    )
                return vector

            async def aembed_text(self, text, **kwargs):
                return await asyncio.to_thread(self.embed_text, text, **kwargs)

            def embed_texts(self, texts, **kwargs):
                vectors = embedding_provider.embed_texts(
                    texts=texts,
                    document_type="query",
                )
                if vectors is None or len(vectors) != len(texts):
                    raise RuntimeError(
                        "The configured embedding provider failed to embed "
                        "RAGAS evaluation text."
                    )
                return vectors

            async def aembed_texts(self, texts, **kwargs):
                return await asyncio.to_thread(self.embed_texts, texts, **kwargs)

        self.llm = ProviderRagasLLM()
        self.embeddings = ProviderRagasEmbedding()
        self.metrics = {
            "faithfulness": Faithfulness(llm=self.llm),
            "context_precision": ContextPrecisionWithReference(
                llm=self.llm,
                name="context_precision",
            ),
            "context_recall": ContextRecall(llm=self.llm),
            "answer_relevancy": AnswerRelevancy(
                llm=self.llm,
                embeddings=self.embeddings,
            ),
        }
        self.ragas_version = importlib.metadata.version("ragas")
        self.max_concurrent_samples = 1

    @staticmethod
    def _validate_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
        if not rows:
            raise ValueError("Cannot evaluate an empty dataset.")

        normalized = []
        for index, row in enumerate(rows):
            if not isinstance(row, Mapping):
                raise ValueError(f"Evaluation sample {index} must be a mapping.")
            for field in ("user_input", "response", "reference"):
                value = row.get(field)
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(
                        f"Evaluation sample {index} has an empty or invalid {field}."
                    )

            contexts = row.get("retrieved_contexts")
            if not isinstance(contexts, list) or any(
                not isinstance(context, str) for context in contexts
            ):
                raise ValueError(
                    f"Evaluation sample {index} retrieved_contexts must be a list of strings."
                )

            normalized.append(
                {
                    "user_input": row["user_input"],
                    "retrieved_contexts": contexts or [NO_CONTEXT],
                    "response": row["response"],
                    "reference": row["reference"],
                }
            )
        return normalized

    async def evaluate(
        self,
        rows: Sequence[Mapping[str, Any]],
        completed_scores: Sequence[Mapping[str, float | None]] | None = None,
        checkpoint_callback=None,
        progress_callback=None,
    ) -> dict[str, Any]:
        normalized_rows = self._validate_rows(rows)
        dataset = self._evaluation_dataset_type(
            samples=[
                self._single_turn_sample_type(**row)
                for row in normalized_rows
            ]
        )
        score_rows = [
            dict(scores) for scores in (completed_scores or [])
        ]
        if len(score_rows) > len(dataset.samples):
            raise ValueError(
                "Saved evaluation scores contain more samples than the dataset."
            )
        score_rows.extend(
            {} for _ in range(len(dataset.samples) - len(score_rows))
        )
        semaphore = asyncio.Semaphore(self.max_concurrent_samples)
        completed_count = sum(
            len(scores) == len(self.metrics)
            for scores in score_rows
        )

        async def score_sample(sample_index, sample):
            nonlocal completed_count
            sample_data = sample.to_dict()
            async with semaphore:
                sample_scores = score_rows[sample_index]
                for name, metric in self.metrics.items():
                    if name in sample_scores:
                        continue
                    metric_input = self._metric_input(name, sample_data)
                    try:
                        score = await metric.ascore(**metric_input)
                    except Exception as error:
                        raise RuntimeError(
                            f"RAGAS metric '{name}' failed for sample "
                            f"{sample_index} ({sample_data['user_input']}): {error}"
                        ) from error
                    sample_scores[name] = score.value
                    score_rows[sample_index] = self._json_safe_scores(sample_scores)
                    if checkpoint_callback is not None:
                        checkpoint_callback(deepcopy(score_rows))

                score_rows[sample_index] = self._json_safe_scores(sample_scores)
                completed_count += 1
                if progress_callback is not None:
                    progress_callback(completed_count, len(dataset.samples))

        tasks = [
            asyncio.create_task(score_sample(index, sample))
            for index, sample in enumerate(dataset.samples)
            if len(score_rows[index]) < len(self.metrics)
        ]
        try:
            await asyncio.gather(*tasks)
        except Exception:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            raise

        metric_names = list(self.metrics)
        summary = {
            name: self._mean_score([row.get(name) for row in score_rows])
            for name in metric_names
        }
        return {
            "ragas_version": self.ragas_version,
            "metrics": metric_names,
            "summary": summary,
            "scores": score_rows,
        }

    @staticmethod
    def _metric_input(name: str, sample: Mapping[str, Any]) -> dict[str, Any]:
        if name in ("faithfulness", "answer_relevancy"):
            fields = ("user_input", "response", "retrieved_contexts")
            if name == "answer_relevancy":
                fields = ("user_input", "response")
        else:
            fields = ("user_input", "retrieved_contexts", "reference")
        return {field: sample[field] for field in fields}

    @staticmethod
    def _json_safe_scores(scores: Mapping[str, Any]) -> dict[str, float | None]:
        result = {}
        for name, value in scores.items():
            numeric_value = float(value) if value is not None else math.nan
            result[name] = (
                numeric_value if math.isfinite(numeric_value) else None
            )
        return result

    @staticmethod
    def _mean_score(values: list[float | None]) -> float | None:
        valid_values = [value for value in values if value is not None]
        return mean(valid_values) if valid_values else None