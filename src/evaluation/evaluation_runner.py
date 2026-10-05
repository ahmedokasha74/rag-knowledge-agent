import asyncio
import json
from pathlib import Path
from typing import Any

from controllers.GraphRag.graph_answer_generator import GraphAnswerGenerator
from controllers.GraphRag.retrieval.graph_context_builder import GraphContextBuilder
from controllers.GraphRag.retrieval.graph_retriever import GraphRetriever
from controllers.GraphRag.retrieval.query_entity_extractor import QueryEntityExtractor
from controllers.HybridRag.hybrid_answer_generator import HybridAnswerGenerator
from controllers.HybridRag.hybrid_rag_pipeline import HybridRagPipeline
from controllers.HybridRag.hybrid_retriever import HybridRetriever
from controllers.rag.RAGPipeline import RAGPipeline
from evaluation.datasets.rag_eval_dataset import build_reference_dataset
from evaluation.ragas_evaluator import RagasEvaluator
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory


COLLECTION_NAME = "cloudify_documents"
RESULTS_DIRECTORY = Path(__file__).parent / "results"
METRIC_DESCRIPTIONS = {
    "faithfulness": "How much of the answer is supported by retrieved context.",
    "context_precision": (
        "Whether relevant retrieved contexts are ranked before irrelevant ones."
    ),
    "context_recall": (
        "Whether retrieved contexts contain information needed by the reference."
    ),
    "answer_relevancy": "Whether the answer addresses the user's question.",
}
PIPELINE_OUTPUTS_PATH = RESULTS_DIRECTORY / "pipeline_outputs.json"


def _check_configuration(settings) -> None:
    if not settings.GENERATION_MODEL_ID:
        raise RuntimeError("GENERATION_MODEL_ID must be set for evaluation.")
    if not settings.EMBEDDING_MODEL_ID:
        raise RuntimeError("EMBEDDING_MODEL_ID must be set for evaluation.")

    backend_keys = {
        "GROQ": settings.GROQ_API_KEY,
        "OPENAI": settings.OPENAI_API_KEY,
        "COHERE": settings.COHERE_API_KEY,
    }
    generation_backend = settings.GENERATION_BACKEND.upper()
    embedding_backend = settings.EMBEDDING_BACKEND.upper()
    graph_backend = settings.GRAPH_EXTRACTION_BACKEND.upper()

    for purpose, backend in (
        ("generation", generation_backend),
        ("embedding", embedding_backend),
        ("graph extraction", graph_backend),
    ):
        if backend not in backend_keys:
            raise RuntimeError(
                f"Unsupported {purpose} backend for evaluation: {backend}."
            )
        if not backend_keys[backend]:
            raise RuntimeError(
                f"The {backend} API key is required for {purpose} evaluation."
            )


def _check_response(response: Any, system: str, query: str) -> str:
    if not isinstance(response, str) or not response.strip():
        raise RuntimeError(
            f"{system} returned an empty answer for query: {query}"
        )
    return response.strip()


def _graph_context(results: list[dict], context_builder: GraphContextBuilder) -> list[str]:
    relationship_context = context_builder.build(results)
    if relationship_context:
        return relationship_context.splitlines()

    entity_contexts = []
    for result in results:
        entity = result.get("entity")
        labels = result.get("labels", [])
        if entity:
            label_text = ", ".join(labels) if labels else "Entity"
            entity_contexts.append(f"{entity} ({label_text})")
    return entity_contexts


def _sample(
    case: dict[str, str],
    response: str,
    retrieved_contexts: list[str],
) -> dict[str, Any]:
    return {
        "user_input": case["user_input"],
        "question": case["user_input"],
        "category": case["category"],
        "retrieved_contexts": [
            context.strip()
            for context in retrieved_contexts
            if isinstance(context, str) and context.strip()
        ],
        "response": _check_response(response, "Pipeline", case["user_input"]),
        "reference": case["reference"],
    }


def _save_results(system_name: str, samples: list[dict], evaluation: dict) -> Path:
    RESULTS_DIRECTORY.mkdir(parents=True, exist_ok=True)
    rows = []
    for sample, scores in zip(samples, evaluation["scores"], strict=True):
        rows.append({**sample, "metric_scores": scores})

    payload = {
        "system": system_name,
        "ragas_version": evaluation["ragas_version"],
        "metric_descriptions": METRIC_DESCRIPTIONS,
        "summary": evaluation["summary"],
        "samples": rows,
    }
    result_path = RESULTS_DIRECTORY / f"{system_name}_results.json"
    result_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False),
        encoding="utf-8",
    )
    return result_path


def _atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    temporary_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False),
        encoding="utf-8",
    )
    temporary_path.replace(path)


def _load_collected_samples(
    cases: list[dict[str, str]],
) -> dict[str, list[dict[str, Any]]] | None:
    if not PIPELINE_OUTPUTS_PATH.exists():
        return None
    try:
        payload = json.loads(PIPELINE_OUTPUTS_PATH.read_text(encoding="utf-8"))
        samples = payload["pipeline_samples"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        return None
    if not isinstance(samples, dict):
        return None

    system_names = ("vector_rag", "graph_rag", "hybrid_rag")
    for system_name in system_names:
        system_samples = samples.get(system_name)
        if not isinstance(system_samples, list) or len(system_samples) != len(cases):
            return None
        for case, sample in zip(cases, system_samples, strict=True):
            if not isinstance(sample, dict):
                return None
            if (
                sample.get("user_input") != case["user_input"]
                or sample.get("reference") != case["reference"]
            ):
                return None
    return samples


def _save_collected_samples(samples: dict[str, list[dict[str, Any]]]) -> None:
    _atomic_write_json(
        PIPELINE_OUTPUTS_PATH,
        {"pipeline_samples": samples},
    )


def _load_metric_progress(
    system_name: str,
    samples: list[dict[str, Any]],
) -> list[dict[str, float | None]] | None:
    progress_path = RESULTS_DIRECTORY / f"{system_name}_progress.json"
    if not progress_path.exists():
        return None
    try:
        payload = json.loads(progress_path.read_text(encoding="utf-8"))
        if payload.get("sample_keys") != [
            sample["user_input"] for sample in samples
        ]:
            return None
        scores = payload["scores"]
        if len(scores) != len(samples):
            return None
        return scores
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        return None


def _save_metric_progress(
    system_name: str,
    samples: list[dict[str, Any]],
    scores: list[dict[str, float | None]],
) -> None:
    progress_path = RESULTS_DIRECTORY / f"{system_name}_progress.json"
    _atomic_write_json(
        progress_path,
        {
            "system": system_name,
            "sample_keys": [sample["user_input"] for sample in samples],
            "scores": scores,
        },
    )


def _print_results(system_name: str, evaluation: dict, result_path: Path) -> None:
    print(f"\n{system_name.replace('_', ' ').upper()}")
    print("-" * len(system_name))
    for metric_name, score in evaluation["summary"].items():
        rendered_score = f"{score:.4f}" if score is not None else "N/A"
        description = METRIC_DESCRIPTIONS.get(metric_name, "RAG quality metric.")
        print(f"{metric_name}: {rendered_score}")
        print(f"  {description}")
    print(f"Saved: {result_path}")


async def run_evaluation() -> None:
    settings = get_settings()
    _check_configuration(settings)
    cases = build_reference_dataset()
    if not cases:
        raise ValueError("The evaluation dataset contains no samples.")

    vector_pipeline = RAGPipeline(config=settings)
    vector_retriever = vector_pipeline.retrieval_controller
    llm_factory = LLMProviderFactory(config=settings)
    graph_llm = llm_factory.create(settings.GRAPH_EXTRACTION_BACKEND)
    graph_model_id = (
        settings.GRAPH_EXTRACTION_MODEL_ID or settings.GENERATION_MODEL_ID
    )
    graph_llm.set_generation_model(graph_model_id)

    query_extractor = QueryEntityExtractor(llm_provider=graph_llm)
    graph_retriever = GraphRetriever(config=settings)
    graph_context_builder = GraphContextBuilder()
    graph_answer_generator = GraphAnswerGenerator(llm_provider=graph_llm)

    hybrid_retriever = HybridRetriever(
        config=settings,
        vector_retriever=vector_retriever,
        graph_retriever=graph_retriever,
        query_entity_extractor=query_extractor,
    )
    hybrid_pipeline = HybridRagPipeline(
        hybrid_retriever=hybrid_retriever,
        answer_generator=HybridAnswerGenerator(
            config=settings,
            llm_provider=vector_pipeline.generation_provider,
        ),
    )
    evaluator = RagasEvaluator(
        llm_provider=vector_pipeline.generation_provider,
        embedding_provider=vector_retriever.embedding_provider,
    )

    pipeline_samples: dict[str, list[dict[str, Any]]] = {
        "vector_rag": [],
        "graph_rag": [],
        "hybrid_rag": [],
    }

    cached_samples = _load_collected_samples(cases)
    try:
        if cached_samples is not None:
            pipeline_samples = cached_samples
            print(f"Reusing saved pipeline outputs from {PIPELINE_OUTPUTS_PATH}")
        else:
            await vector_retriever.vector_db_provider.connect()
            try:
                for case in cases:
                    query = case["user_input"]

                    vector_documents = await vector_pipeline.retrieve(
                        query=query,
                        collection_name=COLLECTION_NAME,
                        limit=5,
                        score_threshold=settings.SCORE_THRESHOLD,
                    )
                    vector_prompt = vector_pipeline.build_prompt(
                        query=query,
                        retrieved_documents=vector_documents,
                    )
                    vector_response = await vector_pipeline.generate(vector_prompt)
                    pipeline_samples["vector_rag"].append(
                        _sample(
                            case,
                            vector_response,
                            [document.text for document in vector_documents],
                        )
                    )

                    graph_query = query_extractor.extract(query)
                    graph_results = graph_retriever.retrieve(graph_query)
                    graph_contexts = _graph_context(
                        graph_results,
                        graph_context_builder,
                    )
                    graph_response = graph_answer_generator.generate(
                        query=query,
                        context="\n".join(graph_contexts)
                        or "No graph results retrieved.",
                    )
                    pipeline_samples["graph_rag"].append(
                        _sample(case, graph_response, graph_contexts)
                    )

                    hybrid_result = await hybrid_pipeline.query(
                        query=query,
                        collection_name=COLLECTION_NAME,
                        limit=5,
                        score_threshold=settings.SCORE_THRESHOLD,
                    )
                    hybrid_contexts = [
                        document.text
                        for document in hybrid_result["vector_results"]
                    ]
                    hybrid_contexts.extend(
                        _graph_context(
                            hybrid_result["graph_results"],
                            graph_context_builder,
                        )
                    )
                    pipeline_samples["hybrid_rag"].append(
                        _sample(case, hybrid_result["answer"], hybrid_contexts)
                    )

                    print(f"Collected pipeline outputs: {query}")
            finally:
                await vector_retriever.vector_db_provider.disconnect()
            _save_collected_samples(pipeline_samples)

        for system_name, samples in pipeline_samples.items():
            print(f"\nEvaluating {system_name.replace('_', ' ')} ({len(samples)} samples)...")
            completed_scores = _load_metric_progress(system_name, samples)
            if completed_scores is not None:
                print(f"Resuming saved metric scores for {system_name}.")
            evaluation = await evaluator.evaluate(
                samples,
                completed_scores=completed_scores,
                checkpoint_callback=lambda scores: _save_metric_progress(
                    system_name,
                    samples,
                    scores,
                ),
                progress_callback=lambda completed, total: print(
                    f"{system_name}: evaluated {completed}/{total} samples"
                ),
            )
            result_path = _save_results(system_name, samples, evaluation)
            (RESULTS_DIRECTORY / f"{system_name}_progress.json").unlink(
                missing_ok=True
            )
            _print_results(system_name, evaluation, result_path)
    finally:
        graph = graph_retriever.graph
        if hasattr(graph, "close"):
            graph.close()


def main() -> None:
    try:
        asyncio.run(run_evaluation())
    except Exception as error:
        raise SystemExit(f"RAG evaluation failed: {error}") from error


if __name__ == "__main__":
    main()