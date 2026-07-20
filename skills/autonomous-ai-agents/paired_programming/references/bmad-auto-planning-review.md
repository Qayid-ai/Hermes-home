# BMAD + Opus Auto Planning/Review Pattern

Use this when Rawan asks for paired programming with BMAD planning, Opus involvement, and execution in the same session.

## Trigger signals

- User explicitly says `Use paired_programming` and asks to install/use BMAD.
- User wants BMAD questions, plan, and build executed together.
- User corrects that Opus should be on auto to avoid repeated permission prompts.
- The work combines product research, planning artifacts, UI/UX, implementation, and verification.

## Durable pattern

1. Install/scaffold tools in the project repo, not the Hermes repo.
2. Write concise research/brief files into the repo so Opus and BMAD have stable context.
3. Start Claude Code Opus through tmux with high effort and `--permission-mode auto` when the task requires many safe read/edit/test steps.
4. Still forbid destructive commands, secrets, pushes, `.env` reads, and compliance-unsafe claims in the prompt.
5. Use the file-output contract. Pane capture is only the control plane.
6. Prompt Opus to run BMAD-style questions internally:
   - user
   - pain
   - differentiator
   - MVP
   - risks
   - UX
   - architecture
   - stories
   - readiness
7. Tell Opus to answer from evidence where possible, make non-blocking assumptions explicitly, and only ask Rawan if a question blocks safe implementation.
8. Let Opus execute safe fixes after review, then require verification commands.
9. Qayid independently re-runs tests/lint/build and does visual/browser QA before final response.

## Pitfalls learned

- Without auto mode, BMAD/Opus planning sessions can stall on harmless read/list commands and waste the session.
- Long prompts pasted into Claude Code may still need a second explicit `C-m` after `tmux paste-buffer`.
- Do not wait forever for Opus narrative output if it already executed and verified useful fixes. Read the contracted file when available, but independently verify the repo state.
- If Firecrawl CLI requires auth, do not block or ask for credentials by default. Record that Firecrawl needs auth, use available web extraction/search as fallback, and label the limitation.
- For regulated domains, encode the data-license/compliance limitation directly in product copy and planning artifacts. Do not fake official table data.
