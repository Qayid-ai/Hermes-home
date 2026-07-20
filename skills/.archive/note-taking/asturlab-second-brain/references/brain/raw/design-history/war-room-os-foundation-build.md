# War Room OS foundation build pattern

Session-derived operating pattern for building the AsturLAB War Room OS alongside, but separate from, Dreaming/brain work.

## Core distinction

- Dreaming is a Hermes consolidation loop: memory, skills, brain, qmd/search posture, and operational learning.
- War Room OS is the operating cadence: strategy extraction, daily/weekly/monthly accountability, scorecards, dry runs, and eventually crons.
- War Room OS may move earlier than deeper brain automation when execution cadence is the bottleneck.
- Do not collapse either system into the other.

## Manual-first build sequence

Use small slices. Each slice needs explicit proposal before writing files.

1. Preflight:
   - inspect vault git state
   - inspect Hermes/qmd/cron state
   - check whether `brain/` exists
   - check War Room source path access without reading course contents unless needed
   - propose the exact first build slice before writing files
2. Create or verify a dedicated non-main branch.
3. Write a RED acceptance test for the slice before writing docs/templates.
4. Run the RED test and confirm it fails for the expected missing artifact.
5. Use Claude Code only as a reviewer or pair, not as final authority.
6. Write the smallest docs/templates needed for the slice.
7. Run all relevant acceptance tests.
8. Verify no cron jobs were created and qmd collection state was not changed unless explicitly approved.
9. Commit with path-scoped staging only.

## War Room OS landing zone

Preferred path:

```text
/Users/batcave/Vaults/asturlab/asturlab/operations/asturlab-os/
```

Initial foundation shape:

```text
asturlab/operations/asturlab-os/
├── AGENTS.md
├── README.md
├── source-handling.md
├── manual-cadence.md
├── dry-runs/README.md
├── templates/
│   ├── daily-dry-run.md
│   ├── weekly-dry-run.md
│   ├── monthly-dry-run.md
│   └── dry-run-log-template.md
└── tests/
    ├── acceptance_slice1.py
    └── acceptance_slice2.py
```

## Gates

- No cron jobs until manual protocols have passed at least one real dry run.
- No semantic brain/strategy/memory changes without confirmation.
- No source extraction until IP-handling and target artifact are explicit.
- Templates are allowed before real logs. Actual dry-run logs need real operating context from Rawan; do not fabricate.
- Course/source structure may inform the OS, but do not copy proprietary wording into git-tracked docs.

## Git discipline

- Never build this on `main`.
- Use a dedicated branch for the slice.
- Never `git add -A` in the vault.
- Stage explicit paths only.
- Verify the latest commit only contains target files.
- Existing dirty/untracked vault material outside the target path must remain untouched.

## Claude Code pairing pattern

For vault-sensitive reviews, prefer a sealed `/tmp/...` working directory containing only the prompt/context needed for the review and `./outputs/<slug>.md`.

Claude is a reviewer. Qayid owns final judgment, applies corrections, and verifies tests.
