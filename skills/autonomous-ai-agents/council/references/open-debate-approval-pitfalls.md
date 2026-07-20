# Council open-debate approval pitfalls

Session learning from testing the configured `council_open_debate` path.

## Personality naming

`council_debate` may not exist as a configured personality. Check config/personality names before running. In this session the debate path was `council_open_debate`, mapped to the runner's `--mode open_debate`.

## Open debate is heavier than rebuttal

`open_debate` with 3 rebuttal rounds can run for a long time, especially when Opus launches deep Claude Code subagents each round. Use background execution with notifications and active progress checks. Expect Opus to take the longest and to continue writing after other voices finish.

## Claude Code approval prompts inside Opus subagents

Fetch/Bash approvals can appear inside Claude Code subagent UI, not only the top-level Opus pane. The watcher may see text like:

- `Claude wants to fetch content from ...`
- `Do you want to allow Claude to fetch this content?`
- `Do you want to proceed?`
- Bash approvals for narrow `/tmp` analysis, e.g. spreadsheet inspection with `python3 -c` or installing `openpyxl`.

In this UI, sending `1 C-m` is not always enough. Sometimes `1` queues as typed input and needs a separate explicit carriage return. Robust watcher logic should support a two-step submit fallback: send `1`, then after a short delay send `C-m`, and verify the prompt cleared.

## What to encode in the runner

- Detect Fetch/Bash approval prompts in the full pane, including subagent sections.
- Prefer safe approvals only for read/research operations: Fetch, local `/tmp` inspection, Python spreadsheet reads.
- Never auto-approve destructive shell commands, writes outside the run dir/tmp, credential access, or public posting.
- After approval, verify progress by checking that the prompt text disappeared or that the subagent status changed.
- If approval remains visible, submit `C-m` explicitly once before declaring a stall.

## Quality interpretation

If a round has output files for Codex/Opus/Antigravity but final synthesis is missing, do not summarise as final Council output. Say it is an interim position and capture which rounds/voices completed.
