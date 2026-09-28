#!/usr/bin/env bash
# Lints the generated site in public/. Run ./scripts/build.sh first.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
python3 scripts/check.py
