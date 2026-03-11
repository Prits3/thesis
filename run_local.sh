#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip >/dev/null
pip install -r requirements.txt

export APP_HOST="127.0.0.1"
export PORT="8501"

echo "Starting app at http://127.0.0.1:8501"
python app.py
