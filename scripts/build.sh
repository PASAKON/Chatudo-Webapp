#!/usr/bin/env bash
# Regenerates public/ from build/render.py + site.config.json.
# Stdlib-only Python 3, no network access needed.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
python3 build/render.py
