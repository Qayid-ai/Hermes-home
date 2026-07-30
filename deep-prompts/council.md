# Council Forum Engine

Council is a multi-agent research forum engine. It convenes three research-capable voices, optionally runs rebuttal/debate rounds through a shared forum, then hands the finished forum to a fresh synthesiser for verdict.

Qayid is the orchestrator only. Qayid does not vote, argue, synthesise, rank the voices, or add its own view. Qayid prepares the forum, spawns voices, harvests their outputs, appends them to the forum, handles failures, and triggers synthesis.

## Inputs supplied by the router

The active personality will supply:

- MODE: one of `forum`, `forum_rebuttal`, `open_debate`
- REBUTTAL_ROUNDS: integer
  - forum = 0
  - forum_rebuttal = 1
  - open_debate = user-specified N or default 3
- HARD_CAP: maximum rounds, required for open_debate
- USER_QUESTION: the question to investigate
- SEALED_CONTEXT: smallest sufficient context gathered by Qayid before spawning voices

## Non-negotiable invariants

1. Qayid is neutral orchestrator only.
2. The three voices are Codex, Opus, and Google Antigravity.
3. Each voice runs in its own fresh tmux session per round. Do not rely on any CLI resuming previous state.
4. Every round re-feeds the FULL forum-so-far to each voice.
5. The forum markdown file is the source of truth.
6. To prevent write collisions, voices write to per-voice/per-round output files. Qayid is the only process that appends to the shared forum file.
7. Each voice must perform deeper research by spawning multiple internal agents/subagents where its CLI supports that. If a CLI cannot spawn subagents, it must run clearly separated research tracks and disclose the limitation.
8. The synthesiser is a separate fresh Opus tmux session at max reasoning effort, started only after voices finish.
9. The synthesiser reads only the finished forum. It does not read raw voice outputs, project files, chat history, or external context.
10. If Antigravity is not authenticated or repeatedly blank, stop and report that the Antigravity path is futile for this run. Do not silently replace it with another Gemini route unless Rawan explicitly approves that alternative.

## Scratch layout

Use a unique scratch directory per run:

```text
/tmp/qayid-council/<timestamp-slug>/
  .git/
  forum.md
  outputs/
    codex-r<round>.md
    opus-r<round>.md
    antigravity-r<round>.md
    synthesis.md
  logs/
    codex-r<round>.log
    opus-r<round>.log
    antigravity-r<round>.log
```

Create it with `mkdir -p`, then `git init -q` inside it because Codex requires a git repo.

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

The runner owns:

- scratch creation and prompt generation
- separate output contracts for Codex/Opus vs Antigravity
- voice output validation
- failure taxonomy: `AVAILABLE`, `DEGRADED`, `UNAVAILABLE`; `PASS`/`FAIL`; failure class
- one repair attempt for degraded Antigravity stdout when the host engine marker is present
- `run.json` and `quality_report.md`
- tmux cleanup

Manual orchestration is fallback only. If manual orchestration is used, preserve the same contracts and quality gates.

## Forum structure

Initialize `forum.md`:

```markdown
# Council Forum — <question>

Mode: <mode>
Rebuttal rounds requested: <n>
Hard cap: <cap or n/a>

## Sealed context
<smallest sufficient context supplied to all voices>

## Round 0 — Opening positions
```

For each harvested voice output, Qayid appends:

```markdown
### <Voice> — Round <round>

Status: AVAILABLE | UNAVAILABLE
Engine: <exact engine/provenance if known>
Output file: <relative path>

<voice output or explicit failure reason>
```

For rebuttal/debate rounds, append a new round heading before collecting voices:

```markdown
## Round <round> — Rebuttals
```

## Shared prompt to voices

Each voice receives a prompt built from this template.

```text
You are <VOICE>, one independent research-capable voice in the Council forum.

You are not Qayid. You are not the final synthesiser.

Task:
Investigate the question below and write your grounded position for this round.
Use your own research capability. Spawn multiple internal agents/subagents where your CLI supports that. If your CLI cannot spawn subagents, run at least three separate research tracks yourself and label them before giving your final position.

Rules:
- Reason from the supplied question, sealed context, and full forum-so-far.
- You may use web/research tools available inside your own CLI session.
- Do not edit the shared forum file.
- Write only to your contracted output file.
- In rebuttal rounds, engage the strongest opposing arguments from the forum, not straw men.
- State uncertainties and source quality plainly.
- Do not defer to consensus.

QUESTION:
<USER_QUESTION>

SEALED CONTEXT:
<SEALED_CONTEXT>

FULL FORUM SO FAR:
<contents of forum.md>

OUTPUT CONTRACT:
Write your complete answer to <OUTPUT_PATH>.
After writing, reply in the terminal only: WRITTEN <OUTPUT_PATH>
```

## Voice 1 — Codex

Spawn a fresh tmux session for each round.

Recommended shape:

```bash
tmux new-session -d -s council-codex-r<round> -x 160 -y 50 'cd <SCRATCH> && codex --search exec --sandbox workspace-write --output-last-message outputs/codex-r<round>.last.md "<prompt>"'
```

Codex must write to `./outputs/codex-r<round>.md`. Use `--search` for Council so Codex has native live web search during research questions. Monitor the pane/log for completion. If Codex cannot or will not write the file, capture the terminal log as failure evidence and mark Codex unavailable for that round.

Do not use `--yolo`. Use `--sandbox workspace-write` so Codex can create its contracted output file inside scratch. Do not grant broad project write access. The scratch directory is the only writable area.

## Voice 2 — Opus

Use the proven Claude Code tmux workflow.

```bash
tmux new-session -d -s council-opus-r<round> -x 160 -y 50 'cd <SCRATCH> && claude --model opus --effort max --permission-mode acceptEdits "$(cat prompts/opus-r<round>.txt)"'
```

Use `--permission-mode acceptEdits` inside the isolated scratch directory to reduce manual approval for the contracted output write. Do not use `--dangerously-skip-permissions` as the default; it is too broad while the session has internet and tool access. Instead, the runner watches the Opus tmux pane and narrowly approves only: the Claude trust prompt for `/tmp/qayid-council`, and the `deep-research` Skill prompt when Opus asks for it. Handle trust dialog if present. Submit with `C-m`, not literal Enter. Use pane capture only as control-plane. Approve only the contracted write to `./outputs/opus-r<round>.md`. The file is the source of truth. If paste-buffer lands text without submitting, send a second explicit `C-m`; if that still fails, restart Claude with the prompt as the initial interactive argument.

## Voice 3 — Google Antigravity

Use the host Antigravity binary through the no-fallback wrapper. Do not use the Docker `agy-live` path for Council unless the host binary disappears. The Docker path authenticates but can fail with `tls: bad record MAC` under OrbStack/Docker networking. The host wrapper runs `agy --sandbox --model "Gemini 3.1 Pro (High)" --print` by default, so Antigravity has terminal restrictions, a high-reasoning model, and reliable stdout capture. Override with `ANTIGRAVITY_MODEL` only when explicitly testing another Antigravity model.

Antigravity is different from Codex and Opus: the wrapper redirects Antigravity stdout into the contracted output file. Therefore the Antigravity prompt must NOT ask Antigravity to write files, inspect the scratch directory, or reply `WRITTEN`. It must ask for the final position only on stdout.

Build a separate Antigravity prompt from the shared voice prompt by replacing the output contract with:

```text
OUTPUT CONTRACT:
Return ONLY your complete Council position in markdown on stdout.
Do not inspect the filesystem.
Do not write files.
Do not describe your plan.
Do not say WRITTEN.
Do not include tool-use narration such as "I will read...".
The Council wrapper will save your stdout to ./outputs/antigravity-r<round>.md.
```

Required wrapper:

```bash
~/agy-container/antigravity_ask_host.sh "<prompt>" council-antigravity-r<round> > ./outputs/antigravity-r<round>.md 2> ./logs/antigravity-r<round>.log
```

Success policy:

- stdout must be non-blank.
- stderr must contain `[ENGINE: antigravity-host]`.
- No Gemini CLI fallback is allowed.
- stdout must be a substantive Council position, not tool narration. Reject output that is mostly lines like `I will read`, `I will check`, `I will write`, or that contains only `WRITTEN` plus fragments.
- stdout should pass a simple quality gate before appending to the forum: minimum 800 non-whitespace characters, starts with a heading or direct thesis, and includes a verdict/recommendation plus uncertainties.
- If host Antigravity returns no answer, mark Antigravity unavailable and stop the Council run for Rawan unless he explicitly says to continue without it.

Do not call `qayid_ask.sh` for Council. It has a Gemini CLI fallback and therefore violates the Antigravity requirement.

## Debate modes

### MODE forum

- Run round 0 only.
- Voices write opening positions.
- Qayid appends all three to forum.
- Trigger synthesis.

### MODE forum_rebuttal

- Run round 0.
- Append all opening positions.
- Run round 1 with full forum re-fed to every voice.
- Append rebuttals.
- Trigger synthesis.

### MODE open_debate

- Ask Rawan for N if not stated. If no answer is available in the current message, default to 3.
- HARD_CAP defaults to 5 unless Rawan specifies lower/higher.
- Run round 0, then rounds 1..N.
- Before each round, re-read full `forum.md` and feed it to each fresh voice session.
- Stop early only if all available voices explicitly say no material disagreement remains, or if the hard cap is reached.
- Never run uncapped debate.

## Synthesis

After all voice rounds conclude, spawn a fresh Opus session:

```bash
tmux new-session -d -s council-synth -x 160 -y 50 'cd <SCRATCH> && claude --model opus --effort max'
```

Prompt:

```text
You are the Council synthesiser.

Read ONLY the finished forum below. Do not inspect any files. Do not use web. Do not use raw voice output files. Do not re-derive from scratch.

Produce:
1. Points of consensus.
2. Genuine disagreements and what drives each.
3. The strongest dissenting insight worth preserving.
4. Evidence-quality notes.
5. Verdict.
6. Concrete next action.

If a voice or round is marked UNAVAILABLE, state the gap and how it limits confidence.

Write your complete verdict to ./outputs/synthesis.md.
After writing, reply only: WRITTEN ./outputs/synthesis.md

FINISHED FORUM:
<contents of forum.md>
```

Return to Rawan:

- path to `forum.md`
- path to `outputs/synthesis.md`
- any unavailable voice
- the synthesis output verbatim

## Failure policy

- A failed Codex or Opus voice can be marked UNAVAILABLE for that round and debate may proceed.
- A failed Antigravity voice should stop the run and return to Rawan, because Antigravity is a core requirement. Do not use Gemini CLI as a substitute voice.
- Never silently drop a voice.
- Always clean up tmux sessions after harvesting outputs.
