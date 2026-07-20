---
name: council
description: "Council forum engine: Codex + Opus + Antigravity research voices, shared forum, optional rebuttals, fresh Opus synthesis."
version: 2.0.0
author: Qayid
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Council, Forum, Multi-Agent, Codex, Opus, Antigravity, Deep-Mode]
    related_skills: [claude-code, codex, hermes-agent]
---

# Council Forum Engine

Use this when Rawan asks for Council, forum, rebuttal, or open debate deep mode.

Council convenes three research-capable voices:

- Codex via tmux.
- Opus via the proven Claude Code tmux file-output workflow.
- Google Antigravity via the host `~/.local/bin/agy` path, wrapped by `~/agy-container/antigravity_ask_host.sh`.

Qayid is neutral orchestrator only. Qayid does not vote, argue, synthesise, or add its own view.

## Entry points

Configured personalities:

- `/personality council` — default router. Chooses mode from the request.
- `/personality council_forum` — 0 rebuttal rounds.
- `/personality council_rebuttal` — 1 rebuttal round.
- `/personality council_open_debate` — N capped rounds. Defaults to 3, hard cap 5.

All four route to the same engine prompt:

`~/.hermes/deep-prompts/council.md`

Do not build separate implementations for each mode.

## Core invariants

1. Qayid is orchestrator only.
2. One shared markdown forum file is the source of truth.
3. Voices do not append directly to the forum. They write per-round output files. Qayid appends to prevent write collisions.
4. Every round starts a fresh tmux session for each voice.
5. Every round re-feeds the full forum-so-far to each voice.
6. The synthesiser is a fresh Opus tmux session with max effort, created after the voices finish.
7. The synthesiser reads only the finished forum.
8. Antigravity must be Antigravity. Gemini CLI fallback is not acceptable as that voice.

## Preferred execution path

Use the runner unless Rawan explicitly asks for manual orchestration:

```bash
~/.hermes/scripts/council_run.py \
  --mode <forum|forum_rebuttal|open_debate> \
  --rebuttal-rounds <n> \
  --hard-cap <cap-or-n/a> \
  --question "<USER_QUESTION>" \
  --sealed-context "<SEALED_CONTEXT>"
```

The runner creates scratch, generates prompts, applies per-engine output contracts, validates outputs, writes `run.json` and `quality_report.md`, and cleans up tmux sessions.

Known runner hardening from live use:

- The process-failure validator must stay line-oriented. Do not fail a substantive strategic answer just because it uses words like "failed market" or "execution error" in analysis.
- Opus can finish Claude Code research agents and write its contracted file shortly after Codex/Antigravity finish. Before harvesting, give Opus an extra grace wait if `outputs/opus-r<round>.md` is still missing but the tmux session is alive.
- Claude Code Fetch approval wording varies by version. Watch for `Fetch`, `Claude wants to fetch content from`, and `Do you want to allow Claude to fetch this content?`; approve safe research fetches with option `1` only, not broad per-domain grants.
- Claude Code subagent approval UI may queue `1` as typed input without submitting. Use a robust selector: send the option digit literally, then send `C-m` as a separate keypress, then send one extra `C-m` if the pane still shows the queued option or `Press up to edit queued messages`.
- Safe Bash approvals inside Opus subagents must remain narrow: only read/research operations under `/tmp` or the Council scratch dir, such as `python3 -c`/`openpyxl` spreadsheet inspection. Do not auto-approve destructive shell, credential reads, git mutation, public posting, or writes outside scratch/tmp.
- Open debate is materially heavier than forum/rebuttal. Use background execution, active progress checks, and do not call the answer final until synthesis exists. If final synthesis is missing, report it as interim with completed rounds/voices.
- Provider quota/rate-limit failures can produce blank voice files while the overall runner keeps going. During live progress checks, inspect `logs/<voice>-r<round>.log` for quota/rate-limit text and verify each expected `outputs/<voice>-r<round>.md` is non-blank before calling a debate "clean". If a strategic decision depends on that voice, pause/rerun after the provider's retry window instead of treating the degraded run as final.
- Antigravity quota exhaustion is not a recoverable same-session Council failure. If host Antigravity logs `RESOURCE_EXHAUSTED`, `Individual quota reached`, `429`, or a reset window, do not keep launching full Council reruns unless the user explicitly wants a degraded Codex+Opus debate. Surface the reset window, stop/kick leftover tmux sessions if aborting, and label any final answer as a two-voice debate, not a full Council.
- On user progress checks, report voice-by-round status plainly: which outputs exist, which are blank, whether `quality_report.md`/`run.json`/`outputs/synthesis.md` exist, and whether provider quota makes the run non-clean. Do not bury availability caveats after the recommendation.
- `council_debate` may not be configured. Check actual personality names first; the tested debate path is `council_open_debate` with `--mode open_debate`.
- See `references/open-debate-approval-pitfalls.md` for the full approval-stall pattern and safe auto-approval boundaries.
- See `references/provider-quota-and-degraded-runs.md` for the degraded-run handling pattern from live Council use.
- See `references/external-openrouter-reviewer.md` for the pattern where a non-Council OpenRouter model reviews a degraded Council forum as an explicitly labelled external review, not a replacement voice.

Manual orchestration is fallback only. If manual orchestration is used, preserve the same contracts and quality gates.

## Scratch layout

Use a unique run directory under:

`/tmp/qayid-council/<timestamp-slug>/`

Expected files:

```text
forum.md
outputs/codex-r<round>.md
outputs/opus-r<round>.md
outputs/antigravity-r<round>.md
outputs/synthesis.md
logs/*.log
```

Initialize with `git init -q` because Codex requires a git repo.

## Antigravity host path

Council uses the host Antigravity binary, not the Docker container. The wrapper runs `agy --sandbox --model "Gemini 3.1 Pro (High)" --print` by default, so print-mode generation remains stdout-based while terminal restrictions and a high-reasoning Antigravity model are enabled. Override with `ANTIGRAVITY_MODEL` only when explicitly testing another Antigravity model:

```bash
~/agy-container/antigravity_ask_host.sh "<prompt>" council-antigravity-r<round> > ./outputs/antigravity-r<round>.md 2> ./logs/antigravity-r<round>.log
```

Success requires:

- non-blank stdout
- stderr contains `[ENGINE: antigravity-host]`
- no Gemini CLI fallback

The Docker `agy-live` container can authenticate but fail generation with `tls: bad record MAC` under OrbStack/Docker networking. Do not use `qayid_ask.sh` for Council because it can fall back to Gemini CLI.

If host Antigravity fails, stop and report the failure to Rawan unless he explicitly says to continue without that voice.

## Antigravity Docker diagnostic policy

This is diagnostic only. It is not the Council execution path.

Before running Antigravity:

```bash
~/agy-container/start_agy_live.sh
~/agy-container/agy_health.sh
```

Exit meanings:

- `0`: proceed.
- `1`: auth invalid. Stop and tell Rawan interactive login is needed.
- `2`: authenticated but liveness blank/TLS-degraded. Try the Antigravity-only workaround path. Do not use Gemini CLI fallback.
- `3`: prerequisite failure. Stop and report the missing prerequisite.

Current known issue on this machine: health can return `TLS-DEGRADED` while auth is valid. The goal is to find an Antigravity-only workaround, not to substitute Gemini CLI.

## Voice contracts

Use the exact contracts in `~/.hermes/deep-prompts/council.md`.

Codex and Antigravity run in fresh tmux sessions per round.

Codex must be launched with `codex --search exec --sandbox workspace-write` inside the scratch directory. `--search` is a top-level Codex flag, not an `exec` subcommand flag; it enables Codex live web search for Council research questions. The default `codex exec` can run as read-only and then fail to create `./outputs/codex-r<round>.md`.

Antigravity must use a different output contract from Codex/Opus. The wrapper redirects Antigravity stdout into `./outputs/antigravity-r<round>.md`, so do **not** tell Antigravity to inspect files, write files, or say `WRITTEN`. Tell it to return only the final markdown position on stdout. Reject outputs that are mostly tool narration (`I will read...`, `I will check...`, `I will write...`) or only `WRITTEN` plus fragments.

Opus uses the `claude-code` skill pattern:

- interactive `claude` in tmux
- launch with `--permission-mode acceptEdits` inside the isolated Council scratch directory to reduce approval prompts for contracted output writes
- allow Claude's `deep-research` Skill for Opus voices; the runner watches the tmux pane and narrowly approves only Council-scratch prompts: folder trust for `/tmp/qayid-council` or `/private/tmp/qayid-council`, the `deep-research` Skill prompt, Web Search prompts, and Fetch prompts during deep research
- watch Opus concurrently while Codex/Antigravity run; do not wait for other voices first or Opus can sit blocked on an approval prompt for minutes
- do not redirect Claude stdout/stderr to a file; keep it attached to the tmux pane or the interactive session can become invisible/stalled
- do not use `--dangerously-skip-permissions` as the default for Council; use narrow approval watching first
- submit via `C-m`
- final answer from output file only
- pane is control-plane only

## Failure policy

Codex or Opus can be marked unavailable for a round and the forum can continue.

Antigravity auth/prereq/liveness failure should stop and return to Rawan unless a true Antigravity-only workaround is available.

If a wrapper falls back to Gemini CLI, preserve the output as diagnostic evidence only. Do not count it as the Antigravity voice.
