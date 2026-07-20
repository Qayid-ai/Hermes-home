# Provider quota and degraded Council runs

Use this when a Council/open-debate run produces blank voice files while the runner itself continues.

## Recognise the failure

Check each voice log and output file before calling the run clean.

Strong quota indicators:

- `ERROR: You've hit your usage limit`
- `try again at <time>`
- `RESOURCE_EXHAUSTED (code 429)`
- `Individual quota reached`
- `Too Many Requests`
- blank `outputs/<voice>-r<round>.md` with a non-empty provider log

Do not infer model quality from blank files caused by quota. Treat it as provider availability failure.

## Progress report format

When the user asks for progress, report:

- process/session id if still running
- run directory
- per-round voice state: pass / running / blank / quota-failed
- whether `quality_report.md`, `run.json`, and `outputs/synthesis.md` exist
- whether the debate is a clean Council or degraded

Say the caveat before the verdict.

## If Codex is quota-limited

If Codex gives a retry time, stop or pause the run if Codex is required for the decision. Rerun after the stated window. A Codex-missing strategic debate should not be treated as final unless the user explicitly accepts degraded output.

## If Antigravity is quota-limited

Antigravity `RESOURCE_EXHAUSTED` with a long reset window is not recoverable by immediate reruns. Do not burn Opus/Codex cycles repeatedly trying the same full Council.

Default action:

1. Report the Antigravity reset window.
2. Ask whether to wait for a true 3-voice Council or continue as a Codex+Opus debate.
3. If stopping, kill the background process and any leftover `council-*` tmux sessions tied to that run.
4. If continuing, label every synthesis as a two-voice debate, not a full Council.

## Final-answer caveat

If a synthesis exists but one voice failed every round, open with the unavailable notices and then give the synthesis. Do not let the final recommendation read as if three independent voices triangulated it.

Good phrasing:

> Antigravity was unavailable in all rounds due to provider quota. Codex and Opus both passed all rounds. This is a strong two-voice debate, not a clean three-voice Council.

## What to preserve

Preserve the handling pattern, not the transient quota state. Do not store claims like "Antigravity is broken" or "Codex quota is exhausted" in memory. Those expire.