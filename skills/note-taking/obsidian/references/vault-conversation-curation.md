# Vault conversation curation example

Use this when the user asks to move useful information from a past Hermes conversation into the Obsidian/AsturLAB vault.

## Pattern

The user may ask for “our conversations from <date>” but then narrow the scope after seeing proposed destinations. Treat that correction as authoritative.

Good flow:

1. Search session history for the date/topic.
2. Identify candidate themes.
3. Propose destination files before writing.
4. If the user narrows scope, update the plan and write only that scope.
5. Save curated notes, not raw transcripts.
6. Verify the created files exist by reading the first lines.

## What to preserve

Preserve:

- Research findings.
- Decision framing.
- Comparisons.
- Architecture stance.
- User-requested sections verbatim or lightly cleaned.
- Actionable conclusions.

Omit unless explicitly requested:

- Tool calls.
- Commands run.
- Session mechanics.
- Credential/config values.
- Transient setup state.
- Adjacent threads from the same date that the user excluded.

## Example from May 24 cockpit conversation

User wanted the Chainlit/Hermes cockpit material saved but not the Claude Code conversation.

Final split:

- `inbox/2026-05-24-chainlit-cockpit-features-id-take.md`
  - Only the “Features I’d take” section.
  - Treated as a raw ideation fragment worth keeping separate.

- `research/2026-05-24-hermes-command-centre-gui-research.md`
  - GUI shortlist.
  - Chainlit/Hermes cockpit framing.
  - Cockpit modules.
  - Update-proof architecture.
  - What not to build.
  - MVP order.
  - Preferred v1.

Rejected scope:

- Claude Code interactive/tmux conversation.

Lesson:

Do not assume all useful-looking material from the same day should be saved. The user’s scope boundaries matter more than completeness.