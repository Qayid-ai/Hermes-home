---
name: paired_programming
description: "Use when Rawan gives a feature to build, bug to fix, codebase problem to diagnose, or implementation plan to execute and wants Qayid/Codex 5.5 to pair with Claude Code Opus 4.8 High Effort through tmux until the work is verified."
version: 1.0.0
author: Qayid
license: MIT
metadata:
  hermes:
    tags: [pair-programming, codex, claude-code, opus, tmux, software-development]
    related_skills: [claude-code, codex, systematic-debugging, test-driven-development, github-pr-workflow]
---

# Paired Programming — Codex 5.5 + Claude Code Opus 4.8

## Overview

Use this skill when Rawan gives a coding task and wants Qayid/Codex 5.5 to work with Claude Code Opus 4.8 High Effort as a second senior engineer.

Qayid remains owner of the task. Claude is not the boss. Claude is the paired specialist used for high-context review, alternate reasoning, blindspot detection, implementation suggestions, and sometimes direct code edits when that is the right move.

The default pattern is:

1. Qayid scopes the task and inspects the repo.
2. Qayid starts Claude Code in an interactive tmux session using Opus 4.8 and High Effort.
3. Qayid gives Claude a file-output contract.
4. Claude writes complete analysis or patch guidance to `./outputs/<slug>.md`.
5. Qayid reads the file, challenges it, reconciles it with Codex's own reasoning, then implements or reviews the code.
6. Qayid verifies with tests, lint, build, reproduction steps, or targeted inspection.
7. Qayid reports the result to Rawan with what changed, what passed, and what risk remains.

Use `claude -p` when Anthropic subscription-based charging supports it and the task is a bounded one-shot analysis, review, or file-output job.

Keep the interactive tmux workflow as a first-class fallback and control-plane path. Use tmux for long-running work, approval-heavy work, multi-turn pairing, fragile TUI-only features such as `/effort ultracode`, or whenever print mode is degraded.

If Rawan explicitly asks for `ultracode`, do not rely on `claude -p --effort ultracode`; print mode may reject, downgrade, ignore, or time out on it. Use interactive tmux, set `/effort ultracode` inside the TUI, approve the effort switch if prompted, and use the file-output contract.

If the follow-up depends on a previous Claude Code source-mining chat, resume the original conversation with `claude --continue` from the same workdir instead of starting fresh. See `references/claude-ultracode-continuation.md`.

Rawan explicitly does not want the tmux/file-output workflow deleted because Anthropic may revert charging or behaviour again.

## When to Use

Use this when:

- Rawan asks to build a feature.
- Rawan asks to fix a bug.
- Rawan asks to debug a repo problem.
- The task is ambiguous and benefits from a second model's reasoning.
- The change is high-risk enough that independent review would catch mistakes.
- The repo is large or unfamiliar and context triage matters.
- Rawan explicitly says to use paired programming, Claude, Opus, or the pair workflow.

Do not use this for:

- Tiny one-line edits where Claude would add overhead.
- Public posting or client-facing publication without human review.
- Tasks where Rawan only wants a quick answer, not execution.
- Destructive git/database actions without explicit confirmation.
- Cross-client work where the active project is unclear.

## Ground Rules

Qayid owns safety and final judgment.

Claude may be wrong, stale, overconfident, or too broad. Treat its output as a senior review memo, not an instruction stream.

Never paste secrets into Claude. Never paste `.env` contents. Redact tokens, keys, private URLs, and client-identifying details unless Claude is working inside that exact client repo and the data is required.

Never push to `main`. Use PR workflow only.

Before commits, sync-check the branch and inspect the diff.

For destructive commands such as `rm -rf`, dropping databases, force-pushing, or deleting branches, stop and get explicit confirmation.

## Current External Guidance Captured

Research checked while creating this skill:

- Claude Code model configuration docs say the `opus` alias resolves to Opus 4.8 on the Anthropic API path, and Opus 4.8 requires Claude Code v2.1.154 or later. To pin the model, use `claude-opus-4-8`.
- Claude effort docs say `high` is the default high-capability setting and equivalent to omitting effort, but this workflow sets it explicitly for clarity.
- Claude effort docs say `xhigh` and `max` exist for supported models, but Rawan asked for High Effort, so use `high` unless he asks to escalate.
- Codex best-practice docs recommend prompts with Goal, Context, Constraints, and Done-when. Use that shape for both Codex's own plan and Claude's prompt.
- Codex best-practice docs recommend planning first for complex tasks, reusable repo guidance in `AGENTS.md`, and turning repeated workflows into skills. This skill is that reusable workflow.

## Preflight Checklist

Before starting Claude:

1. Identify the active repo and task scope.
2. Check git branch/status.
3. Read the repo's `AGENTS.md`, `CLAUDE.md`, or equivalent project instructions if present or auto-injected.
4. Identify test/build/lint commands from docs, package scripts, Makefile, pyproject, or CI.
5. Reproduce the bug if it is a bugfix task.
6. Decide whether Claude should:
   - Review and advise only.
   - Produce an implementation plan.
   - Directly edit files.
   - Review Codex's changes after implementation.

Pushback point: if the requirement is vague, ask one specific clarifying question before spinning Claude. Claude cannot rescue a badly specified target; it will just make the ambiguity look productive.

## Context Hygiene Before Starting a Build

If a thread has accumulated planning debate, corrections, research, or roadmap churn, do not start a substantial build in that same conversation by default.

For build work, prefer a clean session with a compact kickoff containing:

- the corrected distinctions and decisions
- active repo/vault path
- required pairing mode
- safety constraints
- first preflight steps
- test-gated acceptance criteria

This is especially important when Rawan has corrected the frame mid-thread. Do not drag the correction history into the implementation context. Preserve the distilled facts and start clean.

Example kickoff shape:

```text
We are building <system>.
Important distinctions:
- <corrected concept A>
- <separate concept B>
Use paired programming with Claude Code Opus 4.8 through tmux.
Set /effort ultracode inside the Claude TUI.
Use file-output contract: ./outputs/<slug>.md.
Qayid owns final judgment and verification.
Test-gated build only.
Start with preflight:
1. Inspect git state.
2. Inspect relevant system state.
3. Check expected paths/access.
4. Propose exact first build slice before writing files.
```

Pushback rule: a clean session is not avoidance. It is context hygiene. Use it when implementation quality would suffer from stale debate context.

## Start Claude Code in tmux

Use the project root as the working directory.

Prefer a unique session name:

```bash
slug="paired-$(date +%Y%m%d-%H%M%S)"
tmux new-session -d -s "$slug" -x 160 -y 50 'mkdir -p outputs && claude --model claude-opus-4-8 --effort high'
```

If `claude-opus-4-8` is not accepted but docs/version indicate alias support, use:

```bash
tmux new-session -d -s "$slug" -x 160 -y 50 'mkdir -p outputs && claude --model opus --effort high'
```

If the TUI is already open, switch inside it:

```text
/model claude-opus-4-8
/effort high
```

When Rawan asks for ultracode, switch inside the TUI and approve the confirmation prompt:

```text
/effort ultracode
```

Treat `ultracode` as interactive-only unless current Claude Code docs prove print mode supports it. Do not fake it with a stale CLI flag.

```bash
claude --version
claude auth status --text
claude update
```

Do not print auth tokens or environment values.

## Handle Claude Code Dialogs

Use pane capture as a control plane only:

```bash
tmux capture-pane -t "$slug" -p -S -120
```

Workspace trust dialog:

```bash
tmux send-keys -t "$slug" C-m
```

Bypass permissions dialog, only if using a bypass mode:

```bash
tmux send-keys -t "$slug" Down
sleep 0.3
tmux send-keys -t "$slug" C-m
```

Default paired programming should not start with full permission bypass. Use normal permissions unless the task and repo are trusted and Rawan has allowed broad edits.

## Submit the Pair Prompt

Use `tmux paste-buffer` for long prompts, then send `C-m`.

Prompt structure:

```text
You are being controlled through interactive Claude Code by Qayid.
You are pairing with Codex 5.5 on Rawan's task.

Model/effort target: Claude Opus 4.8, High Effort.

Do not rely on terminal-visible output as the final answer.
Write your complete final answer to ./outputs/<slug>.md.
Rules:
- Create or overwrite that file.
- The markdown file is the source of truth.
- Do not include ANSI/UI text.
- If you need to ask a question, write it to the file under "Question".
- After writing the file, reply in the terminal only: WRITTEN ./outputs/<slug>.md

Task
<Rawan's exact task>

Context
- Repo: <path>
- Branch/status summary: <brief>
- Relevant files already inspected by Qayid: <files>
- Error/output/reproduction: <brief or none>
- Project instructions: follow AGENTS.md/CLAUDE.md in this repo.

Constraints
- Do not read secrets or .env files.
- Do not push to main.
- Do not perform destructive commands.
- Keep scope tight. Do not refactor unrelated areas.
- If editing, preserve existing style and architecture.

Done when
- <behavioral acceptance criteria>
- <test/lint/build command expected to pass>
- <manual verification if relevant>

What I need from you
1. Restate the real problem in one paragraph.
2. Identify the likely files and risks.
3. Propose the smallest viable implementation path.
4. Flag assumptions and missing information.
5. If you edit code, list exactly what changed and what verification you ran.
6. If you do not edit code, provide patch-level guidance precise enough for Codex/Qayid to implement.
7. Include a "Review Against Codex" section: what Codex/Qayid is likely to miss.
```

Submit:

```bash
tmux load-buffer /tmp/pair-prompt.txt
tmux paste-buffer -t "$slug"
tmux send-keys -t "$slug" C-m
```

After pasting, capture the pane and confirm Claude started working. Long prompts sometimes paste without submission.

## Working Modes

See also:

- `references/bmad-auto-planning-review.md` for the BMAD + Opus auto-mode pattern used when planning, research, implementation review, safe fixes, and verification happen in one session.
- `references/claude-ultracode-continuation.md` for the Claude Code `/effort ultracode` + `claude --continue` pattern when a follow-up audit needs the original chat context.

### Mode A — Claude as planner/reviewer

Use when the repo is sensitive, the task is ambiguous, or Qayid should do the edits.

Claude writes analysis and implementation guidance only. Qayid implements.

Best for:

- Client repos.
- High-risk production code.
- Security/auth/payment changes.
- First pass on unfamiliar code.

### Mode A2 — Claude as BMAD planner/reviewer in auto mode

Use when Rawan explicitly asks for paired programming plus BMAD planning/review/execution, or when the task requires many safe reads, edits, and verification commands.

Start Claude Code with Opus high effort and auto permission mode:

```bash
slug="bmad-auto-$(date +%Y%m%d-%H%M%S)"
tmux new-session -d -s "$slug" -x 160 -y 50 'cd /path/to/project && mkdir -p outputs && claude --model claude-opus-4-8 --effort high --permission-mode auto'
```

Still constrain the prompt:

- no destructive commands
- no secrets or `.env` reads
- no pushes or commits unless explicitly requested
- no fake compliance claims or fabricated regulated data
- file-output contract required

Tell Claude to run BMAD questions internally, answer from the brief/research, make non-blocking assumptions, and only raise a blocking question if safe implementation truly depends on it. Let it implement safe fixes after review, but Qayid must independently verify tests/lint/build and inspect the UI before final response.

Do not confuse auto mode with permission bypass. Auto mode reduces harmless approval stalls; it does not remove Qayid's safety responsibility.

### Mode B — Claude as implementer

Use when the task is contained and the repo allows agent edits.

Claude may edit files and run tests. Qayid still reviews diff and verifies independently.

Best for:

- Tests.
- Internal tools.
- Low-risk feature branches.
- Mechanical refactors with clear scope.

### Mode C — Claude as independent reviewer after Codex changes

Use after Qayid/Codex implements.

Prompt Claude to review `git diff` or the changed files and write `./outputs/<slug>-review.md`.

Ask specifically for:

- correctness bugs
- missed edge cases
- security issues
- race conditions
- type errors
- missing tests
- overbroad scope

Then reconcile findings. Do not blindly apply every suggestion.

## Reconciliation Protocol

When Claude's output is ready:

1. Read `./outputs/<slug>.md` with `read_file`.
2. Compare Claude's plan to Codex/Qayid's own understanding.
3. Mark each Claude claim as:
   - Adopt
   - Reject
   - Verify first
   - Needs Rawan clarification
4. Implement the adopted path.
5. Run verification.
6. If verification fails, debug systematically. Use Claude again only after giving it the new failure data.

Do not let Claude create a second vague plan after a failure. Feed it the exact failing command, stack trace, changed files, and hypothesis.

## Verification Discipline

Always verify before final response unless impossible.

Good verification examples:

```bash
git status --short
git diff --stat
git diff
npm test
npm run lint
npm run build
python -m pytest
ruff check .
```

Use the repo's actual commands, not generic ones, once discovered.

If full test suites are too slow, run targeted tests first and state that full verification was not run.

## Final Response Shape to Rawan

Keep it short:

- What changed.
- What passed.
- What Claude contributed.
- What remains risky or unverified.
- The output file path if useful.

Do not dump Claude's whole answer unless Rawan asks.

## Common Pitfalls

1. Treating Claude as the final authority. It is a second brain, not a supervisor.
2. Scraping final output from tmux pane. Always use `./outputs/<slug>.md`.
3. Forgetting to send the second `C-m` after paste-buffer.
4. Starting Claude without checking branch/status.
5. Letting Claude broaden scope into unrelated cleanup.
6. Running both Codex and Claude on the same files without reconciliation; this creates merge confusion.
7. Using permission bypass by default. Do not hand out broad write access casually.
8. Asking Claude to solve an unclear product requirement. Clarify with Rawan first.
9. Hiding uncertainty. If verification is partial, say so.
10. Leaving tmux sessions running. Kill them when done.
11. Assuming "review-only" prompts prevent side effects. Claude subagents/tools may still run state-changing commands during audits. For infrastructure reviews, explicitly ban stateful commands (`qmd collection add/remove`, config writes, cron creates, git commits, package installs), ask Claude to use read-only probes first, and verify live state afterward. If a review creates a side effect, disclose it and clean it only with approval.
12. Completing a paired build before Opus has validated it when the kickoff or user expectation says Opus should validate/build with Qayid. In those sessions, run Claude review before calling the slice done, not after the user asks where Opus is.
13. Letting Claude Code's `ultracode` dynamic workflows/subagents expand a focused review. Unless Rawan explicitly asked for multi-agent review, reject or stop workflow prompts and narrow Claude back to the contracted file-output review.
14. When Rawan asks to keep Claude Code "constantly in the loop" and says it may create multiple agents, treat that as permission for **review gates and justified multi-agent analysis**, not uncontrolled vault/repo writes. Use Claude at pre-edit and post-edit gates, require file-output contracts, and keep subagents read-only or `/tmp`-scoped unless direct editing is explicitly approved.
15. Stopping an exhaustive Opus source-absorption run too early. If Rawan explicitly asks for full source absorption or "you and Opus review all sources," dynamic workflows are allowed when constrained to the supplied bundle and no-write rules. Wait for the contracted file, persist it outside `/tmp`, then reconcile before any repo/vault writes.
16. Starting a new Claude window/session when Rawan explicitly says to continue the existing tmux session. First inspect the existing pane, do not submit stale typed prompts, and only use a new window if Rawan approves or the existing pane is unusable. Claude Code may display stale prompt text after an output; verify whether it is real active input before acting. A harmless single-character type/delete can distinguish stale display from active input, but never press Enter until the pane is safe and relevant.

See `references/review-only-ultracode-audits.md` for the final-review pattern and side-effect guard.

## Cleanup

After reading and verifying Claude's output:

```bash
tmux kill-session -t "$slug"
```

If the session is worth preserving for an ongoing task, leave it running intentionally and mention the tmux session name.

## Verification Checklist

- [ ] Active repo and branch confirmed.
- [ ] Project instructions respected.
- [ ] Claude launched through the right mode: tmux for `ultracode`, continuation, approvals, or long-running work; `claude -p` only for bounded one-shot work.
- [ ] Claude model target is Opus 4.8.
- [ ] Claude effort target is High.
- [ ] File-output contract used.
- [ ] Claude output read from `./outputs/<slug>.md`.
- [ ] Codex/Qayid reconciled Claude's advice instead of blindly following it.
- [ ] Code diff inspected.
- [ ] Tests/lint/build or targeted verification run.
- [ ] No secrets exposed.
- [ ] No push to main.
- [ ] Tmux session cleaned up or intentionally left running.
