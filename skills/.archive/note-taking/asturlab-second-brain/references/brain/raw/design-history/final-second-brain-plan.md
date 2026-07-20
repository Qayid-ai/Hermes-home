# Final second-brain plan — June 2026 review

This reference condenses the final Opus/Qayid review of the AsturLAB second-brain / auto-memory build.

Primary outputs created during the session:

- `/Users/batcave/.hermes/hermes-agent/outputs/second-brain-research-and-upgrade-plan.md`
- `/Users/batcave/.hermes/hermes-agent/outputs/hermes-integration-addendum.md`
- `/Users/batcave/.hermes/hermes-agent/outputs/opus-final-second-brain-review.md`
- `/Users/batcave/.hermes/hermes-agent/outputs/final-second-brain-build-plan.md`

## Final call

Build only Phase 0 and Phase 1 first.

The valuable core is small:

- `brain/` inside `/Users/batcave/Vaults/asturlab/`
- strict 3-file `wiki/`
- flat `raw/pages/` with `domain:` frontmatter
- tier-1 session capture
- grep-first query
- manual Dream Sequence

Defer automation.

## Phase 0

Preflight and baseline:

- check Hermes/qmd/cron state
- remove accidental qmd collection `qayid-second-brain-research` only with approval
- create a scoped git baseline for the vault
- do not use `git add -A`
- verify War Room access or mark it inert
- verify `brain/` absence/emptiness
- verify rule-loading behavior rather than assuming subdirectory `AGENTS.md` injection

## Phase 1 structure

```text
/Users/batcave/Vaults/asturlab/brain/
├── AGENTS.md
├── wiki/
│   ├── index.md
│   ├── log.md
│   └── processed.md
└── raw/
    ├── sources/
    ├── session-notes/
    ├── pages/
    └── clients/
```

Do not add `outputs/`, qmd, cron, clients, War Room OS, or typed subfolders in Phase 1.

## Page frontmatter baseline

```yaml
---
title: <title>
type: concept | source-summary | synthesis | entity | query | operating-pattern
domain: asturlab | delivery | offers | sales | technical-patterns | tools | research | operating-systems | people
created: YYYY-MM-DD
updated: YYYY-MM-DD
compiled: YYYY-MM-DD
status: draft | reviewed
confidence: low | medium | high
sources:
  - <path-or-url>
source-vault:
  - <vault path if compiled from vault>
reviewed: false
---
```

## Important corrections from Opus

- Git recoverability was assumed but not true in practice. Baseline first.
- `qmd embed --collection brain` is not a valid command. qmd is deferred.
- Opus created a stray qmd collection during review. Clean it with approval before qmd work.
- Tier-2 auto-pages need lifecycle/quarantine. Phase 1 supports tier-1 capture only.
- The brain is lagging compiled knowledge, not current project status.
- Disable stock `llm-wiki` in Phase 1. Do not override yet.
- War Room path may be blocked by macOS TCC and is third-party paid-course IP. Inert hooks only.

## Phase 1 non-goals

Do not build:

- qmd collection/embed
- cron jobs
- client ingest
- full-vault bootstrap compile
- tier-2 auto-pages
- promotion into canonical project/operations files
- War Room OS
- stock `llm-wiki` override
- per-client ledgers
- physical typed folders

## Approval phrase

Rawan should say:

`go build phase 0 and phase 1`

Do not infer approval from discussion.
