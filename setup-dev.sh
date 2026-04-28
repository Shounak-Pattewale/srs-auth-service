#!/bin/bash
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "Setting up srs-auth development environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "$ROOT/venv" ]; then
    python3 -m venv "$ROOT/venv"
fi

source "$ROOT/venv/bin/activate"
pip install --upgrade pip
pip install -e ".[dev]"

echo "Done. Activate with: source venv/bin/activate"
