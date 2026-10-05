#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PATH="${HOME}/.local/bin:${PATH}"
cd "$PROJECT_ROOT"

PYTHONPATH=src uv run streamlit run src/app/streamlit_app.py \
    --server.headless true \
    --server.port 8501 \
    --server.address 0.0.0.0
