#!/usr/bin/env bash
# Verifie en ~20 s que le studio marche dans cette session : rendu d'une page test (1 s, brouillon) + mesures.
# Usage : bash studio/verifier.sh   (depuis la racine du depot)
set -euo pipefail
cd "$(dirname "$0")"
command -v ffmpeg >/dev/null || { echo "ffmpeg absent"; exit 1; }
python3 -c "import playwright" 2>/dev/null || pip install --quiet --break-system-packages playwright
python3 -m playwright install chromium >/dev/null 2>&1 || true
T=$(mktemp -d)
python3 studio.py rendre exemples/page_test.html "$T/test.mp4" --fin 1 --brouillon
python3 studio.py mesures "$T/test.mp4"
rm -rf "$T"
echo "STUDIO OK"
