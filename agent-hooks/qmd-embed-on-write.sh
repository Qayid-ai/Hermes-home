#!/usr/bin/env bash
# qmd index-on-save hook.
# Fires on post_tool_call for write_file and patch (filtered by matcher in config.yaml).
# Reads JSON payload on stdin, checks if the written path is inside the vault.
# If so, runs qmd update (rescan filesystem) then qmd embed (vectorize new content)
# in the background. Non-blocking — agent turn never waits.
# Returns {} on stdout as required by the Hermes hook JSON wire protocol.
# Log output: ~/.hermes/logs/qmd-embed.log

payload="$(cat -)"
path=$(echo "$payload" | jq -r '.tool_input.path // empty')
# Resolve a relative path before the vault-prefix check. Hermes passes
# tool_input.path RAW (as the model emitted it — verified in source), and the
# file tools resolve relative paths against TERMINAL_CWD (file_tools.py:124),
# NOT the payload's .cwd field. Verified (2026-05-25, source): in a gateway
# session the payload .cwd is the gateway's launch dir (~/.hermes/hermes-agent),
# NOT the vault — so resolving against .cwd would compute the wrong path and
# wrongly SKIP. TERMINAL_CWD is inherited by this hook's process env (the hook
# is spawned with no env= override), so we read it directly here. Fallbacks:
# payload .cwd, then leave as-is. Absolute paths pass through unchanged.
# NOT canonicalizing (no realpath): path is only a vault-membership gate.
# Known limit: file tools actually check a per-task live cwd BEFORE
# TERMINAL_CWD; the hook can't see that in-process value, so a mid-session
# `cd` within a terminal task could still cause a benign skipped re-embed.
base="${TERMINAL_CWD:-$(echo "$payload" | jq -r '.cwd // empty')}"
if [[ -n "$path" && "$path" != /* && -n "$base" ]]; then
  path="${base%/}/$path"
fi

if [[ "$path" == /Users/batcave/Vaults/asturlab/* ]]; then
  (
    echo "--- $(date '+%Y-%m-%d %H:%M:%S') ---"
    /opt/homebrew/bin/qmd update && /opt/homebrew/bin/qmd embed
  ) >> ~/.hermes/logs/qmd-embed.log 2>&1 &
fi

printf '{}\n'
