#!/bin/bash
# Daily brain maintenance: refresh stale compiled context, keep qmd index
# fresh, auto-commit brain changes. Silent on clean success (no Telegram
# noise); prints only when something needs attention.
set -u
VAULT="/Users/batcave/Vaults/asturlab"
cd "$VAULT" || { echo "brain-dream-daily: vault missing at $VAULT"; exit 1; }

WARN=""

# Refresh both project cards; estate-agents last so current.md points at the
# active client project.
OUT1=$(python3 brain/scripts/dream.py --refresh-stale --project asturlab-brain 2>&1) || WARN+="refresh asturlab-brain failed:
$OUT1
"
OUT2=$(python3 brain/scripts/dream.py --refresh-stale --project estate-agents 2>&1) || WARN+="refresh estate-agents failed:
$OUT2
"

# Surface synthesis pages whose sources changed — these need LLM review.
PENDING=$(grep -rl "synthesis-review: pending" brain/pages 2>/dev/null || true)
if [ -n "$PENDING" ]; then
  WARN+="synthesis review pending (sources changed under hand-written pages):
$PENDING
"
fi

# Keep qmd collections fresh regardless of which tool wrote the files.
if command -v qmd >/dev/null 2>&1; then
  qmd update >/dev/null 2>&1 && qmd embed >/dev/null 2>&1 || WARN+="qmd update/embed failed
"
fi

# Auto-commit the autonomous brain zone only. Never sweeps source-truth edits.
git add brain/ >/dev/null 2>&1
if ! git diff --cached --quiet 2>/dev/null; then
  git commit -q -m "dream: daily brain refresh $(date +%Y-%m-%d)" || WARN+="git commit failed
"
fi

if [ -n "$WARN" ]; then
  printf '🧠 Brain daily — attention needed\n%s' "$WARN"
fi
exit 0
