#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${HERMES_FIRECRAWL_ENV_FILE:-$HOME/.hermes/.env}"

read_env_key() {
  local key="$1"
  [[ -f "$ENV_FILE" ]] || return 0
  python3 - "$ENV_FILE" "$key" <<'PY'
import sys
from pathlib import Path
path = Path(sys.argv[1])
key = sys.argv[2]
for line in path.read_text(errors='ignore').splitlines():
    s = line.strip()
    if not s or s.startswith('#') or '=' not in s:
        continue
    k, v = s.split('=', 1)
    k = k.strip()
    if k.startswith('export '):
        k = k[len('export '):].strip()
    if k == key:
        v = v.strip().strip('"').strip("'")
        print(v)
        break
PY
}

if [[ -z "${FIRECRAWL_API_KEY:-}" ]]; then
  FIRECRAWL_API_KEY="$(read_env_key FIRECRAWL_API_KEY)"
  export FIRECRAWL_API_KEY
fi

if [[ -z "${FIRECRAWL_API_URL:-}" ]]; then
  FIRECRAWL_API_URL="$(read_env_key FIRECRAWL_API_URL)"
  if [[ -n "$FIRECRAWL_API_URL" ]]; then
    export FIRECRAWL_API_URL
  fi
fi

if [[ -z "${FIRECRAWL_API_KEY:-}" && -z "${FIRECRAWL_API_URL:-}" ]]; then
  echo "FIRECRAWL_API_KEY or FIRECRAWL_API_URL is required for firecrawl-mcp" >&2
  exit 1
fi

exec npx -y firecrawl-mcp
