# Claude Code ultracode + continuation notes

Use this when Rawan asks for paired programming with `ultracode`, or when a follow-up audit/review needs the context from an earlier Claude Code research session.

## Durable lessons

- `ultracode` is a Claude Code **interactive TUI effort setting**. Set it inside the TUI with `/effort ultracode`, then approve the confirmation if prompted.
- Do not assume `claude -p --effort ultracode` works. Print mode may reject, downgrade, ignore, or time out on that effort level. If the user explicitly asked for ultracode, use interactive tmux.
- If a previous Claude Code chat has the needed source-mining/context, do **not** start a clean chat unless there is a reason. Start Claude in the same workdir with `claude --continue`, then set `/effort ultracode`, then send the follow-up prompt.
- Use pane capture only for status and approvals. The final result still needs a file-output contract, e.g. `./outputs/<slug>.md` or an explicit absolute output path.
- Long pasted prompts may appear in the TUI but not submit. Always capture the pane and, if it is sitting at the prompt, send a second `C-m`.
- When Claude writes to a file, verify the file exists and read it back before telling Rawan the work is done.

## Minimal pattern

```bash
SESSION="<slug>"
WORK="/path/to/original/workdir"
tmux new-session -d -s "$SESSION" -x 180 -y 60 "cd '$WORK' && claude --continue"
sleep 5
tmux send-keys -t "$SESSION" '/effort ultracode' C-m
# approve the effort switch if Claude prompts
tmux send-keys -t "$SESSION" C-m
```

Then paste a self-contained follow-up prompt with a file-output contract and send an explicit second `C-m` if needed.

## When not to use continuation

- The previous chat was contaminated with irrelevant or confidential context for another client/project.
- The user wants a clean independent review.
- The previous workdir no longer contains the source bundle/output files the chat references.
