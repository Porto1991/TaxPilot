#!/usr/bin/env bash
# TaxPilot one-command launcher (Mac/Linux).
# Usage:  ./start_taxpilot.sh          (chat offline; upload/analysis work)
#         ANTHROPIC_API_KEY=sk-ant-... ./start_taxpilot.sh   (full chat)
set -e
cd "$(dirname "$0")"

command -v python3 >/dev/null || { echo "ERROR: Python 3 is not installed (https://python.org)"; exit 1; }

if [ ! -d .venv ]; then
  echo "› Creating virtual environment and installing dependencies (first run only)..."
  python3 -m venv .venv
  ./.venv/bin/pip install -q -r requirements.txt
fi

if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "⚠ ANTHROPIC_API_KEY not set — the chat will show 'offline'. Upload & analysis still work."
fi

echo "› TaxPilot running at http://localhost:8000  (Ctrl+C to stop)"
( sleep 2 && (open http://localhost:8000 2>/dev/null || xdg-open http://localhost:8000 2>/dev/null) ) &
exec ./.venv/bin/python -m uvicorn app.main:app --port 8000
