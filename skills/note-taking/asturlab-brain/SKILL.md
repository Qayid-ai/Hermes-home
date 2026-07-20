---
name: asturlab-brain
description: "Use when Rawan asks to use, maintain, extend, or audit the AsturLAB second brain (brain/ in the asturlab vault): context recovery, ingest, query, session capture, Dream, wiki pages, or the brain cron loop. This is the clean v3 skill describing the FINAL operating system only."
version: 3.0.0
author: Qayid
license: MIT
metadata:
  hermes:
    tags: [asturlab, second-brain, brain, vault, obsidian, qmd, dream, memory]
    related_skills: [obsidian, qmd, project-kickoff-interview, paired_programming]
---

# AsturLAB Brain — Operating System (v3)

The second brain exists to **minimize time-to-context**: new session → know where we are in ≤90s; new chat → load the right project state; project return → resume from current truth without Rawan re-explaining. It is an active context-recovery layer, not an archive.

Vault: `/Users/batcave/Vaults/asturlab`. Rules of record: vault `README.md` (structure), vault `AGENTS.md` (behaviour), `brain/BRAIN.md` (brain manual). Compiled overview: `brain/pages/concepts/second-brain-architecture.md`.

## Layers

| Layer | Path | Role |
|---|---|---|
| Source truth | `projects/`, `asturlab/`, `research/`, `daily/`, `inbox/` | Authoritative documents; never overridden by the brain |
| Brain | `brain/` | Qayid-private, autonomous, LLM-maintained compiled layer |
| Control plane | `asturlab/operations/knowledge-ops/` | Receipts, gates, confidentiality contracts — not the product |
| Session history | Hermes `session_search` | Conversations not yet compiled |

`brain/` layout: `context/{current.md,projects/,sessions/}` (cards + handoffs), `pages/{concepts,operations,projects,sources}/` (knowledge), `wiki/{index,log,processed}.md` (the **single live** TOC, event log, and processed registry for the whole vault), `raw/` (brain-private sources incl. `design-history/`), `outputs/` (dream reports), `scripts/`.

## Startup ritual (every new session/chat/project return)

```bash
python3 brain/scripts/load_context.py --current
python3 brain/scripts/load_context.py --project <slug>   # if a project is in focus
```

If the loader reports STALE: `python3 brain/scripts/dream.py --refresh-stale --project <slug>`. Brain-first for orientation; verify against vault source files before side effects.

## The five operations

1. **Ingest** ("add this"): preserve/copy the source under `brain/raw/<area>/`, then write a real synthesis page in `brain/pages/` (format below). `scripts/ingest_source.py --source <path> --title <t>` gives the mechanical fallback; prefer LLM-written pages.
2. **Query** ("what do I know about X"): read `wiki/index.md`, search pages + qmd `brain` collection, answer **with citations** to pages/sources. If the answer produced new durable insight, write it back as a page ("save that").
3. **Session capture** ("save this session" / end-of-session wrap): `scripts/session_capture.py --project <slug> --topic <t> --summary <s>` — writes a handoff, refreshes the project card + `current.md`, registers + logs.
4. **Dream** ("run dream"): `scripts/dream.py --lint --report` for the health pass; `--refresh-stale` for freshness. Prompted Dream sessions may also cover the other three consolidation layers (memory, skills, operational) — see `brain/pages/concepts/dream-sequence.md`.
5. **Bookkeeping**: every ingest/capture appends `wiki/log.md` and registers in `wiki/processed.md` (idempotent by entry id). `wiki/index.md` is updated on every new page.

## Page format (non-negotiable)

```markdown
---
type: brain-wiki-page
project: <slug or asturlab-brain>
generated: <iso>
sources:
  - <vault-relative path>
source-fingerprint: <computed via brain_common.source_fingerprint>
---

# Title

<!-- SYNTHESIS:BEGIN -->
LLM-written synthesis. [[wikilinks]] to related pages. Dense, cited, current.
<!-- SYNTHESIS:END -->

## Source links
- `<path>`
```

- Content inside `SYNTHESIS` markers is **protected**: `dream.py --refresh-stale` never rewrites it. When sources change, it re-stamps freshness and sets `synthesis-review: pending` — the LLM then re-reads the changed sources, updates the synthesis if needed, and sets `synthesis-review: reviewed`.
- Session handoffs (`brain-session-handoff`) are historical records: never regenerated, never "stale".
- Every claim in a page must be traceable to a listed source.

## Write rules

Routine `brain/**` writes are autonomous — no proposal/confirm, no acknowledge-before-save. Approval is required only for: deleting/archiving source truth; publishing/outbound side effects; moving client facts into global doctrine; client-identifying details outside project-local or brain-private scope; contract/scope/payment decisions; broadening source allowlists. Outside `brain/**`, vault `AGENTS.md` save rules apply (acknowledge-before-save, S2 for manual saves).

## The autonomous loop (live since 2026-07-04)

Two Hermes cron jobs, both `--no-agent` scripts (deterministic, no LLM, no tool approvals), delivered to Telegram:

- **brain-dream-daily** (`30 7 * * *`, `~/.hermes/scripts/brain-dream-daily.sh`): refresh-stale for both project cards (estate-agents last = active focus), `qmd update && qmd embed`, auto-commit `brain/`. Silent when clean; messages only when synthesis review is pending or something failed.
- **brain-dream-weekly** (`0 9 * * 1`, `~/.hermes/scripts/brain-dream-weekly.sh`): full lint + written report (`brain/outputs/dream-report-<date>.md`), inbox ageing, research raw/actionable counts, git hygiene. Always messages (heartbeat).

Rules: keep these scripts thin and deterministic; semantic fixes (synthesis review, contradiction resolution, page merges) are LLM work done in-session, proposed when they touch source truth. Do not add LLM cron jobs without separate approval (`approvals.cron_mode: deny` stands).

## Retrieval order

1. `brain/context/current.md` + project card — orientation.
2. Vault source files — authority (system of record).
3. `session_search` — discussions not yet compiled.
4. qmd (`brain` + other collections) — search when deterministic cards aren't enough. qmd retrieves; cards orient.

## Confidentiality

Client-identifying details stay inside `projects/<name>/` or brain-private scope. Global knowledge-ops files are metadata-only (paths, hashes, counts, opaque IDs). Never write client identifiers into `asturlab/{branding,content,marketing}`, `research/`, `inbox/`, `daily/`, or any output that leaves the project folder. See `brain/pages/operations/knowledge-ops-control-plane.md`.

## Anti-drift rules (learned the hard way — see brain/pages/concepts/scope-drift-lessons.md)

1. The **original task source governs scope**. If Rawan references a prior message/timestamp, retrieve that exact message and let it rule; a later mixed phrase never overrides it.
2. **Content over machinery.** When tempted to build governance/scripts/relays, check: does the brain have the *knowledge* this machinery would manage? Build the content first.
3. **Phase honesty.** Presence checks are not operational proof. A phase is done only when the named operation actually ran (real query with citations, real Dream audit, real capture).
4. **Park, don't abandon.** A new urgent track doesn't cancel a standing build — write the resume point into `brain/context/current.md` open loops before switching.
5. Rawan is **never the maintenance loop** — his role is source approval, correction, and boundary approvals.

## Related systems (not this skill's scope)

- War Room OS: deferred, separate fresh build — `brain/pages/operations/war-room-os.md`.
- PR steering loop (estate-agents): `brain/pages/projects/estate-agents-pr-steering.md`.
- Design history and the superseded v2 doctrine: `brain/raw/design-history/` (vault) and `~/.hermes/skills/.archive/note-taking/asturlab-second-brain/`.
