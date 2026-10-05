#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PATH="${HOME}/.local/bin:${PATH}"
cd "$PROJECT_ROOT"

PYTHONPATH=src uv run python - <<'PY'
from streamlit.testing.v1 import AppTest

app = AppTest.from_file("src/app/streamlit_app.py", default_timeout=10).run()
assert not app.exception, app.exception
assert len(app.chat_input) == 1
assert app.sidebar.radio[0].options == ["Vector RAG", "Graph RAG", "Hybrid RAG"]
print("Streamlit app smoke test passed.")
PY
