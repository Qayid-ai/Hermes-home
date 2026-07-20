# Second-brain improvement source-review pattern — 2026-06-18

Use this reference when Rawan asks to improve the AsturLAB vault/second-brain system from multiple external sources before planning or building.

## Durable lesson

Do not let the Karpathy/LLM-Wiki pattern seduce you into creating a parallel `knowledge-base/`. The right move for AsturLAB is to strengthen the existing vault as the system of record.

Build toward:

- deterministic E-compress before model/vault ingestion
- raw / clean / proposal / promoted state separation
- processed registry for idempotency
- proposal-only scheduled distillation
- visible E6 maintenance reports
- context matrix for what each workflow reads and must not read
- qmd as retrieval support, not the compiled knowledge layer

## Source-ingestion gate

For multi-source improvement tasks:

1. Use a temp workspace outside the vault.
2. Read one source at a time.
3. Produce one ingestion note per source before opening the next.
4. For GitHub repos, enumerate the file tree and read relevant source/docs/skills/prompts, not just README.
5. For videos, retrieve and read the full transcript.
6. If a source is inaccessible, stop and ask.
7. Do not inspect or modify the target vault until all source notes are complete.
8. Only after all source notes exist, inspect the current vault and synthesize a plan.
9. Show the plan and wait for `go` before building.

## Ingestion note format

```markdown
### Source N — Name
- Type / how I accessed it:
- Proof of full read:
- Key mechanisms / patterns:
- Directly implementable for my system:
- Deliberately skipping, and why:
```

## Cross-source synthesis template

After ingestion, produce:

- coverage table with proof tokens
- cross-source agreements/conflicts
- deduplicated feature list tagged by source
- mapping to current AsturLAB vault: changes / additions / left alone
- explicit Karpathy adopt/adapt/skip section
- inaccessible sources and workaround, if any
- plan gate asking for `go`

## Specific conclusions from the 2026-06-18 run

Sources reviewed:

- YouTube Hermes memory + LLM Wiki transcript
- YouTube Karpathy companion build-prompt transcript
- `tinyhumansai/openhuman`
- `garrytan/gbrain`
- GrowthClaw `_vibe-system/SKILL.md`
- Karpathy Appendix B prompt/essay
- Rawan Appendix A requirements

Consensus:

- raw sources and compiled knowledge must be separate
- ingestion is a pipeline, not a save
- automation must be bounded and idempotent
- maintenance must be visible and proposal-first
- context should be scoped deliberately

Main implementation direction:

- do not replace the vault
- add/strengthen E-compress, registries, logs, context matrix, maintenance skill, scheduled-distillation skill
- default all scheduled work to proposal packets for Rawan review

## Pitfalls

- Do not call selected high-signal file reading “whole repo absorption” unless every relevant file class was actually read.
- Do not let Claude Code dynamic workflows duplicate direct ingestion unless explicitly useful and bounded.
- Do not turn tool-access failures into permanent negative rules. If a ZIP/folder is missing, ask for it or use a precise file check.
- Do not build cron before the manual ingest/state/maintenance path exists.
- Do not silently write client-identifying details into shared cross-project locations.
