#!/bin/bash
# Weekly Dream health report: full wiki lint + vault hygiene summary,
# delivered to Telegram every run (weekly heartbeat).
set -u
VAULT="/Users/batcave/Vaults/asturlab"
cd "$VAULT" || { echo "brain-dream-weekly: vault missing at $VAULT"; exit 1; }

echo "🧠 Weekly Dream report — $(date +%Y-%m-%d)"
echo

# Full lint with written report (brain/outputs/dream-report-<date>.md).
python3 brain/scripts/dream.py --lint --report 2>&1 | sed -n '1,25p'
echo

# Inbox ageing (README excluded). Inbox should trend to zero.
INBOX_COUNT=$(find inbox -name "*.md" ! -name "README.md" | wc -l | tr -d ' ')
echo "inbox: ${INBOX_COUNT} unprocessed item(s)"
if [ "$INBOX_COUNT" -gt 0 ]; then
  find inbox -name "*.md" ! -name "README.md" -exec basename {} \; | sort | head -5
fi

# Research holding pen: raw/actionable items awaiting processing or linking.
RAW=$(grep -rl "^status: raw" research 2>/dev/null | wc -l | tr -d ' ')
ACT=$(grep -rl "^status: actionable" research 2>/dev/null | wc -l | tr -d ' ')
echo "research: ${RAW} raw, ${ACT} actionable"

# Git hygiene: brain/ auto-commits daily; anything else uncommitted is
# source-truth edits awaiting a human-reviewed commit.
UNCOMMITTED=$(git status --porcelain | wc -l | tr -d ' ')
LAST_COMMIT=$(git log -1 --format="%ad %s" --date=short)
echo "git: ${UNCOMMITTED} uncommitted change(s); last commit: ${LAST_COMMIT}"

exit 0
