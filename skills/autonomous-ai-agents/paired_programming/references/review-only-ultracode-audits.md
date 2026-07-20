# Review-only ultracode audits

Use this when Rawan asks for an Opus/Claude Code ultracode review of a plan, architecture, vault/system design, or Hermes integration before approving a build.

## Pattern

1. Reuse the original Claude Code research conversation when continuity matters:
   - start in the same workdir
   - run `claude --continue`
   - if Claude offers full context vs summary, prefer summary when durable files already hold the evidence
   - set `/effort ultracode` inside the TUI
2. Create a compact review bundle instead of pasting the whole chat:
   - prior plan file paths
   - addenda/audit outputs
   - new decisions from the current chat
   - hard constraints and explicit non-build scope
3. Require file output:
   - `./outputs/<slug>.md` or `/tmp/<task>/<slug>.md`
   - final terminal reply only: `WRITTEN <path>`
4. Read the file directly and synthesize your own final plan. Do not outsource judgment.

## Side-effect guard

Review-only prompts are not enough. Claude subagents may still run state-changing tools while "verifying".

For infrastructure or vault/Hermes audits, explicitly forbid:

- `qmd collection add/remove` unless the task is cleanup with approval
- cron create/update/remove
- Hermes config writes
- skill edits
- git commits/pushes
- package installs
- vault writes
- deletion or migration commands

Tell Claude to use read-only probes first:

- list/status commands
- read-only filesystem checks
- grep/search
- `git status`, not commits
- qmd status/list, not collection mutation

After the audit, independently verify state that Claude may have touched.

If a side effect happened:

1. disclose it plainly
2. classify whether cleanup is destructive/state-changing
3. get approval if cleanup changes shared/tool state
4. add it to the final plan as a Phase 0 cleanup item

## Concrete lesson from second-brain review

During the AsturLAB second-brain final review, an Opus ultracode subagent accidentally ran `qmd collection add` with no path. It defaulted to the current workdir and created a stray qmd collection named `qayid-second-brain-research` with 669 files.

Correct response:

- do not hide it
- do not clean it in a review-only phase without approval
- include `qmd collection remove qayid-second-brain-research` as an explicit approved cleanup step before future qmd work

The durable lesson is not that qmd is unsafe. The durable lesson is that review-only Claude prompts need explicit state-mutation bans and post-review state verification.
