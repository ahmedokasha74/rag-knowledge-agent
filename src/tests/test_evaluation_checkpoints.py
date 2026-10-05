from evaluation import evaluation_runner


def test_pipeline_outputs_are_persisted_and_reused(tmp_path, monkeypatch):
    output_path = tmp_path / "pipeline_outputs.json"
    monkeypatch.setattr(evaluation_runner, "PIPELINE_OUTPUTS_PATH", output_path)
    cases = [
        {
            "user_input": "What is Cloudify?",
            "reference": "Cloudify is a SaaS company.",
            "category": "entity",
        }
    ]
    samples = {
        system: [
            {
                "user_input": cases[0]["user_input"],
                "reference": cases[0]["reference"],
                "retrieved_contexts": ["Cloudify is a SaaS company."],
                "response": "Cloudify is a SaaS company.",
            }
        ]
        for system in ("vector_rag", "graph_rag", "hybrid_rag")
    }

    evaluation_runner._save_collected_samples(samples)

    assert evaluation_runner._load_collected_samples(cases) == samples


def test_metric_scores_are_persisted_and_reused(tmp_path, monkeypatch):
    results_directory = tmp_path / "results"
    monkeypatch.setattr(evaluation_runner, "RESULTS_DIRECTORY", results_directory)
    samples = [{"user_input": "What is Cloudify?"}]
    scores = [{"faithfulness": 0.8}]

    evaluation_runner._save_metric_progress("vector_rag", samples, scores)

    assert evaluation_runner._load_metric_progress("vector_rag", samples) == scores