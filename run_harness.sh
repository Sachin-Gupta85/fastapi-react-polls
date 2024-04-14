#!/usr/bin/env bash
# Test harness: runs the FastAPI backend tests (in-memory mongomock, no Mongo
# needed) and the React component tests. Requires python3 and node/npm.
set -euo pipefail
cd "$(dirname "$0")"

echo "== backend (pytest + mongomock) =="
python3 -m venv .venv 2>/dev/null || true
./.venv/bin/pip -q install -r server/requirements-dev.txt
( cd server && ../.venv/bin/python -m pytest -q )

echo "== frontend (vitest) =="
( cd client && npm install --silent && npm test )

echo "ALL TESTS PASSED ✅"
