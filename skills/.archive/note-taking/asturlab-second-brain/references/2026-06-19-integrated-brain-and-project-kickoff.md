# 2026-06-19 — Integrated AsturLAB Brain and project kickoff correction

## What changed

Rawan corrected the frame: the second brain is not a manual Knowledge Ops paperwork layer. It must be a private, autonomous, LLM-maintained brain/wiki that preserves and restores operational context across sessions, chats, and projects.

The current vault remains source truth. The top-level `brain/` is the compiled working-memory/context layer. Knowledge Ops is the control plane.

## Operational brain built

Live system:

```text
brain/
  BRAIN.md
  context/current.md
  context/projects/
  context/sessions/
  wiki/index.md
  wiki/log.md
  wiki/processed.md
  pages/
  raw/
  templates/
  scripts/brain_common.py
  scripts/load_context.py
  scripts/session_capture.py
  scripts/ingest_source.py
  scripts/dream.py
```

qmd collection `brain` indexes compiled content only and excludes `BRAIN.md`, `raw/**`, `wiki/log.md`, `wiki/processed.md`, `templates/**`, `scripts/**`, and `outputs/**`.

Verified loop:

```text
source change -> stale detected -> dream refresh -> context/wiki fresh -> qmd retrieval works
```

## Durable lessons

- Do not reject a top-level `brain/` merely because the vault exists. The mistake is an unsourced competing vault, not a compiled context/wiki layer.
- Optimize for time-to-context, not archival neatness.
- Brain-first for orientation; vault-source-first for authority.
- Routine writes under `brain/**` are autonomous. Vault source-truth edits still follow acknowledge/proposal gates.
- qmd retrieves; context cards orient.
- Knowledge Ops is control plane, not the product.

## Roadmap correction

Next phases should prioritize:

1. section markers and synthesis preservation: `AUTO-GENERATED`, `SYNTHESIS`, `HUMAN-NOTES`, `OPEN-LOOPS`, `REVIEW-QUEUE`
2. daily usability: real project cards, startup ritual, end-session capture
3. first real use on real work
4. GitHub connector
5. LLM synthesis engine
6. Fathom connector
7. cron orchestration
8. scale/backfill/metrics

## Project kickoff correction

For urgent/new projects, especially when a vault folder already exists:

- Work the project first; do not keep building infrastructure in isolation.
- Use the project as a real dogfood case for the brain.
- Read existing planning files first.
- Gap-fill only; never clobber.
- Use a short manual interview before creating a reusable skill/script.
- Allow `TBD`, `unknown`, and `research needed` to avoid friction.
- After the run, harvest the interview into a reusable class-level skill/script.

High-signal kickoff questions:

1. Are existing planning docs real, stale, or scaffold?
2. One sentence: what is this project and who is it for?
3. What urgent outcome/deadline drives this now?
4. What does done mean for this immediate push?
5. What is in scope vs out of scope for now?
6. What are the 3–5 must-do functions?
7. Hard constraints: stack, integrations, platform, budget, timeline?
8. What already exists: repo, designs, assets, prior work?
9. Rough approach or architecture?
10. What is blocked, unknown, or needs research?
11. Immediate next 1–3 actions?
12. Decisions already locked?
13. Biggest risk?

Map answers to `brief`, `scope`, `requirements`, `tech-plan`, `roadmap`, `decisions`, `next-actions`, and `risks`.

## Identity alignment risk

For projects connected across Telegram, vault, GitHub, Fathom, and brain, establish one canonical slug and binding map:

```text
Telegram topic <-> vault project slug <-> GitHub repo URL <-> Fathom meeting ID/URL <-> brain project card
```

Forbid auto-creating variant slugs during ingest/connectors.
