# E6 status schema and schema reconciliation — 2026-06-18

## Context

During the AsturLAB second-brain / Knowledge Ops build, E6 #2 exposed a status-validation defect: the report claimed type-scoped status validation, but every status-bearing file used fallback validation. Opus caught this as a real defect.

Root cause: the validator mapped planning types as `planning-brief`, etc., while the vault README schema uses bare planning types: `brief`, `scope`, `requirements`, `tech-plan`, `roadmap`, `kanban`, `next-actions`, `decisions`, `risks`.

## Validated status audit method

Use the vault README schemas as source of truth. Never use a permissive global status enum.

Mapping:

- planning types `brief | scope | requirements | tech-plan | roadmap | kanban | next-actions | decisions | risks` → `draft | active | locked`
- research types `source-capture | comparison | concept | competitor-profile | question | repo-scan` → `raw | processed | actionable`
- `ingest-receipt` → `captured | proposed | promoted | rejected`
- `meeting-transcript` → `raw | processed`
- project README by path `projects/<name>/README.md` → `active | paused | archived`
- rulebooks, daily files, and Knowledge Ops control files should not have `status`

Tolerated drift, not canonical schema:

- `session | session-wrap` may currently carry `saved | promoted | archived`
- `deep-mode-output | inbox-note` may currently carry old save-flow status values

Report counts only:

- status-bearing files checked
- type resolution engaged
- unknown-type-with-status
- recognized by documented schema
- tolerated drift
- nonconforming status fields
- unexpected status on schema-less/rulebook types
- temporal-marker categories

Never print freeform status values, project slugs, paths, or excerpts in global Knowledge Ops reports.

## Verification signal

The corrected status-only dry audit resolved `28/28` status-bearing files and `unknown-type-with-status = 0`, proving type resolution engaged. It found 8 nonconforming statuses instead of E6 #2's 7, proving stricter validation caught a real false negative.

## Schema reconciliation decision

Opus recommended a narrow hybrid proposal:

- Add optional `status: saved | promoted | archived` to session schemas.
- Add optional `status: saved | promoted | archived` to inbox deep-mode output schemas.
- Do not silently canonize `inbox-note` from one file.
- Do not add operations-research lifecycle schema yet.
- Do not use `superseded` as a status value; supersession is a relationship/lifecycle marker.
- Defer operations-research migration to a separate company-local proposal.

## Full second-brain build status lesson

Do not mistake the Knowledge Ops/E6 foundation for the complete second brain.

Foundation completed or validated:

- Knowledge Ops metadata/control surface
- qmd exclusion fail-safe for Knowledge Ops
- manual E6 reporting and Opus gates
- type-scoped status validation
- schema reconciliation proposal

Still ahead before the system is complete:

- source-ingestion receipt workflow
- project-local client receipts/registries
- bounded scheduled distillation proposal packets
- later-day full E6 gate over changed/aged content
- explicit approval before any cron

When Rawan asks whether the full second brain is still on track, answer honestly: yes for the foundation, not complete yet. Then name the remaining layers.
