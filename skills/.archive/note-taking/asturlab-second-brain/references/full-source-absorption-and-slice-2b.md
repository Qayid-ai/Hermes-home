# Full Source Absorption + Slice 2b Gate

Session reference from the June 17 second-brain build review.

## Trigger

Use this reference when Rawan asks whether all second-brain sources were fully absorbed, or asks Qayid + Opus to review how to use source material to build the optimal AsturLAB brain.

## Source absorption standard

Do not claim "fully absorbed" from a prior summary alone.

A valid source-absorption review should:

1. Inventory the source families and verify local availability.
2. Package a bounded review bundle with the exact source paths and manifest.
3. Include full transcripts where transcript content matters.
4. Include selected high-signal docs/source files for large repos rather than pretending the whole repo was read.
5. Ask Opus to separate:
   - adopt now
   - defer
   - reject/quarantine
6. Require a file-output contract.
7. Persist the Opus review outside `/tmp` before cleanup.
8. Reconcile Opus output with Qayid judgment before touching the vault.

Important wording: "high-signal selected docs/source were absorbed" is honest. "entire gbrain/OpenHuman/Hermes repos were absorbed" is usually false unless every relevant file was actually read.

## Review bundle shape

Recommended bundle content:

- full YouTube transcripts relevant to the prompt
- GrowthClaw/OpenClaw source docs if used
- prior Opus/research plan
- current `brain/AGENTS.md`
- current `brain/wiki/index.md`
- current `brain/wiki/log.md`
- current `brain/wiki/processed.md`
- current compiled brain pages under review
- selected gbrain docs/skills for compiled truth, source attribution, ingest, query, maintain, test-before-bulk
- selected OpenHuman docs/source for token compression, memory sources, prompt injection, transcript ingest, deterministic dedupe
- selected Hermes docs/source for memory, session search, cron, MCP, tools, prompt builder

Redact secrets automatically. Never include `.env`, auth files, credential files, or private client material unless the task explicitly requires it and the destination is fenced.

## Key architectural findings to preserve

The current AsturLAB brain should be treated as an honest toy until it proves more than one loop.

The next quality leap is not Dream, qmd, cron, or War Room. It is idempotent ingest.

Gate 0 before further build:

- make the existing proof safe in git
- separate War Room deletion from brain proof work
- avoid root `.bak` clutter entering commits
- keep brain-slice changed paths scoped to `brain/**`

Slice 2b:

- canonicalize source paths
- add `source_hash` to `wiki/processed.md`
- use deterministic content-addressed dedupe
- scope NEW detection to `raw/sources/` only
- never scan `raw/clients/` by default
- fix `second-brain-scope.md` as the page template before copying the pattern
- normalize `wiki/log.md` headings
- create a small proof set of pages from varied sources
- replace tautological query tests with retrieval-selection tests

## Deterministic dedupe lesson

OpenHuman's useful transfer is the discipline, not the engine:

- normalize content: trim, lowercase, collapse whitespace
- hash deterministically, e.g. FNV-1a 64-bit shortened to 12 hex chars
- dedupe exact-after-normalization
- do not use semantic dedupe for source identity, because semantic recall can hide legitimate updates

Adopt this in the markdown ledger as `source_hash`. Do not port a whole Rust/DB pipeline.

## Page model reminder

Compiled pages need two zones:

1. Compiled Truth — rewritten current synthesis, cited claim by claim.
2. Evidence / Timeline — append-only, reverse chronological, dated evidence bullets.

Keep progress/status/SHAs/file counts out of compiled truth. Those belong in logs/ledgers/session notes, not durable pages.

## Pitfalls

- Do not treat a 40–60KB Opus plan as a build backlog.
- Do not run qmd or create cron during Phase 1/2 proof work.
- Do not let War Room files leak into a brain slice.
- Do not call source absorption complete when only a summary was read.
- Do not write content pages into `wiki/`.
- Do not copy full third-party transcripts or paid-course text into git-tracked compiled pages; point and abstract.
