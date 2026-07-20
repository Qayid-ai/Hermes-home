---
name: asturlab-second-brain
description: "Use when Rawan asks to build, use, modify, audit, or automate the AsturLAB vault / second-brain / knowledge-ops system. Current doctrine: build an autonomous LLM-maintained brain/wiki for fast context recovery across sessions, chats, and projects; use Knowledge Ops as the control plane, not the main artifact; preserve project-local confidentiality and source grounding."
version: 2.0.0
author: Qayid
license: MIT
metadata:
  hermes:
    tags: [asturlab, second-brain, vault, knowledge-ops, obsidian, qmd, cron, memory]
    related_skills: [obsidian, qmd, hermes-agent, paired_programming, project-kickoff-interview]
---

# AsturLAB Second Brain / Knowledge Ops

## Current doctrine

Build an autonomous LLM-maintained AsturLAB brain/wiki that restores operational context fast across sessions, chats, and project returns. The second brain is not mainly an archive; its primary job is to minimize Qayid's time-to-context.

A scoped top-level `brain/` or equivalent compiled wiki layer is allowed and intended when building the full system. Do not reject it merely because the vault already has project folders. The earlier "no top-level brain" posture was an over-correction.

Use **Knowledge Ops** as the metadata/control plane, not the main artifact:

```text
/Users/batcave/Vaults/asturlab/asturlab/operations/knowledge-ops/
```

The intended split:

- `brain/` — LLM-maintained compiled wiki, context cards, session handoffs, current operating context, indexes, outputs.
- `projects/`, `asturlab/`, `research/`, `daily/` — raw/source-of-truth operational vault material.
- `knowledge-ops/` — controls, schemas, receipts, source-access gates, maintenance protocols.

Raw/project files remain source-of-truth. The brain/wiki is the compiled working memory that Qayid maintains and loads from.

## Trigger

Load this skill when Rawan asks about:

- second brain
- auto-memory
- vault intelligence
- Knowledge Ops
- E-compress
- ingest receipts
- Karpathy LLM Wiki pattern in AsturLAB
- Dream Sequence / E6 maintenance
- scheduled distillation
- source ingest into the vault
- qmd wiring for vault retrieval
- improving Qayid's memory/vault operating system

## Hard rules

1. **Autonomous context recovery is the product.** Optimize for Qayid regaining project/session context in 30-90 seconds, not for creating more manual filing work for Rawan.
2. **Scoped brain/wiki is allowed.** A top-level `brain/` or equivalent compiled layer is valid when it is the LLM-maintained context/wiki layer, not a competing unsourced vault.
3. **Knowledge Ops is control plane.** Do not mistake receipts, dry-runs, and maintenance reports for the full second brain.
4. **Auto-maintain the wiki/context layer.** The LLM should update wiki pages, project context cards, session handoffs, indexes, logs, and processed registries automatically within safe boundaries.
5. **Gate only risky boundary actions.** Require approval for deletion, publishing, cross-project abstraction, contract/scope-impacting claims, and external side effects; do not require Rawan to approve every routine context/wiki update.
6. **No aggressive harvester.** Automation must be bounded by approved source, cap, cursor/watermark, project binding, and audit output.
7. **Project-local confidentiality.** Client-identifying raw sources, transcripts, repo names, people, receipts, coverage registries, proposals, and logs live inside the relevant `projects/<name>/` folder or a project-local brain partition.
8. **Vault/source first.** Raw/project files remain source-of-truth. The brain/wiki is the compiled working memory. qmd helps retrieve; it does not replace source attribution.

## Context recovery layer

The brain must make new sessions and project returns cheap.

A full build should include:

```text
brain/
├── raw/
├── wiki/
│   ├── index.md
│   ├── log.md
│   └── processed.md
├── pages/
├── context/
│   ├── current.md
│   ├── projects/
│   └── sessions/
├── outputs/
└── scripts/
```

Core artifacts:

- `brain/context/current.md` — current operating context, active projects, recent changes, stale areas, open loops, where to resume.
- `brain/context/projects/<project>.md` — always-current project context card: current state, decisions, risks, next actions, people/entities, source bindings, repo/Fathom pointers, last updated.
- `brain/context/sessions/<date>-<topic>.md` — compact handoff from substantive sessions: what changed, what was decided, what remains open, next resume step, source/file pointers.
- `brain/wiki/index.md` and `brain/wiki/log.md` — navigation and chronological maintenance record.
- `brain/wiki/processed.md` — processed source/session registry.

Primary command pattern to support:

```text
load_context(project=<slug>)
```

Expected read order:

1. `brain/context/current.md`
2. `brain/context/projects/<slug>.md`
3. recent `brain/context/sessions/` entries linked to that project
4. project README/decisions/next-actions as source-of-truth check
5. qmd/session search only if the context card is stale or insufficient

Do not treat search as context. qmd retrieves; context cards orient.

## Current first-slice structure

The approved first slice adds a client-free metadata/control surface:

```text
asturlab/operations/knowledge-ops/
├── README.md
├── index.md
├── log.md
├── processed.md
└── maintenance/README.md
```

Purpose:

- `README.md` — operating manual and scope.
- `index.md` — client-free navigation map.
- `log.md` — append-only metadata log.
- `processed.md` — client-free registry template. Real client source coverage stays project-local.
- `maintenance/README.md` — E6 maintenance contract. Reports propose; they do not mutate.

## E-compress doctrine

E-compress is conditional source normalization before model synthesis or durable filing.

Use it for noisy inputs:

- HTML/web pages
- long transcripts
- tool dumps
- pasted exports
- noisy markdown

Skip it for already-clean human-authored notes unless a receipt is still useful.

E-compress may use local extraction, Firecrawl, qmd snippets, manual cleanup, or other tools. Record which extractor was used.

For client-confidential sources, prefer local extraction. Do not send client content to third-party extractors unless approved for that project.

## Ingest receipt and packet generator

Every explicit source ingest or E-compress pass should produce a receipt with metadata only:

```yaml
date: YYYY-MM-DD
type: ingest-receipt
scope: shareable | company-internal | project-local
source-kind: public-web | transcript | repo-activity | manual-note | tool-output
source-ref: <URL, file path, or opaque project-local ID>
source-hash: <sha256 when available>
extractor: local | firecrawl | qmd | manual | other
quality: clean | partial | failed
proposal-path: <where the review proposal lives, if any>
promoted-path: <where approved content landed, if any>
status: captured | proposed | promoted | rejected
confidentiality: project-local | company-internal | shareable
```

Global receipts must be client-free. Client-identifying receipts live project-local.

Operational generator:

```bash
python3 asturlab/operations/knowledge-ops/scripts/generate_ingest_packet.py \
  --scope shareable \
  --confidentiality shareable \
  --provenance public-web \
  --source-kind public-web \
  --topic example-topic \
  --source-ref 'https://example.com/source' \
  --extractor manual \
  --quality clean
```

For dry runs add `--dryrun`; outputs land under qmd-excluded `knowledge-ops/_dryrun/`.

The generator is fail-closed:

- no missing scope/confidentiality/provenance
- no default global routing
- project-local scope requires `--project` and writes under that project
- client/external provenance cannot be `shareable`
- project-local material cannot use remote extractors
- global packets are rejected if client-like data is detected
- packets contain source pointers/hashes only, not excerpts
- it creates receipt + proposal only; it never promotes

Verified 2026-06-18: positive synthetic public dry-run created receipt/proposal; negative global packet containing email/contract-like text was rejected with non-zero exit.

## Provenance labels

Use the vault README vocabulary where applicable:

- `manual`
- `public-web`
- `transcript`
- `repo-activity`
- `external-sync`
- `client-project`

Confidentiality values:

- `project-local`
- `company-internal`
- `shareable`

## Five operations, adapted for AsturLAB

### 1. Ingest

1. Identify scope: global, company-internal, or project-local.
2. Preserve raw source or pointer in the existing correct destination.
3. Run E-compress only if the source needs normalization.
4. Create an ingest receipt.
5. Produce a proposal if semantic changes are needed.
6. Promote only after approval or an existing explicit workflow allows it.
7. Update metadata logs/registries without client-identifying snippets.

### 2. Query / context recovery

1. For orientation, start with AsturLAB Brain context first: `brain/context/current.md`, then `brain/context/projects/<slug>.md` when the project is known.
2. For authority, verify against vault source files: project planning files, decisions, next-actions, transcripts, research, or repo notes.
3. Use qmd `brain` for compiled-context retrieval when deterministic cards are insufficient.
4. Use qmd vault collections for broader source retrieval when the brain card does not answer the question.
5. Use session search for conversation recall that has not yet been compiled into the brain.
6. Answer with citations to source files or compiled notes.
7. If the answer is worth preserving, update `brain/**` autonomously when it is routine context/wiki maintenance; use proposal-confirm only for source-truth changes or high-risk boundary actions.

### 3. E6 maintenance

Manual first.

E6 checks:

- stale inbox/research
- unprocessed sources
- orphan notes
- duplicates
- missing source pointers
- qmd/index coverage gaps
- frontmatter/status schema drift
- candidate promotions
- confidentiality risks
- contradictions and temporal supersessions

E6 outputs a proposal report. No deletion, archive, promotion, semantic rewrite, cron, or public posting without approval.

Status validation is type-scoped. Use the vault README schemas as source of truth; never use a permissive global status enum.

Validated E6 status mapping:

- planning types `brief | scope | requirements | tech-plan | roadmap | kanban | next-actions | decisions | risks` → `draft | active | locked`
- research types `source-capture | comparison | concept | competitor-profile | question | repo-scan` → `raw | processed | actionable`
- `ingest-receipt` → `captured | proposed | promoted | rejected`
- `meeting-transcript` → `raw | processed`
- project README by path `projects/<name>/README.md` → `active | paused | archived`
- rulebooks, daily files, and Knowledge Ops control files should not have `status`

Tolerated drift, not canonical schema:

- `session | session-wrap` may currently carry `saved | promoted | archived`
- `deep-mode-output | inbox-note` may currently carry old save-flow status values

Reports must show counts only: recognized-by-schema, tolerated-drift, nonconforming-status, unknown-type-with-status, unexpected-status-on-schema-less, and temporal-marker categories. Never print freeform status values, project slugs, paths, or excerpts in global E6 reports.

Temporal categories:

- `true_contradiction`
- `temporal_supersession`
- `temporal_evolution`
- `temporal_regression`
- `negation_artifact`
- `needs_human_review`

### 4. Scheduled distillation

Manual dry-run is operational; cron remains gated.

Use the manual dry-run generator before any scheduled version:

```bash
python3 asturlab/operations/knowledge-ops/scripts/generate_distillation_run.py \
  --source-kind public-watch-delta \
  --scope shareable \
  --confidentiality shareable \
  --topic example-delta \
  --source-ref 'public-watch:example' \
  --cursor-before cursor-001 \
  --cursor-after cursor-002 \
  --max-items 3 \
  --max-chars 1000 \
  --max-lookback-days 2
```

The generator is fail-closed:

- source kind is allowlisted: `greptile-pr-review-delta | graphify-architecture-delta | fathom-transcript-delta | repo-activity-delta | manual-delta | public-watch-delta`
- Greptile, Graphify, Fathom, and repo deltas require `project-local` scope
- cursor-before and cursor-after are required and must advance
- max-items, max-chars, and max-lookback-days are required and ceiling-clamped
- output is metadata-only and proposal-only
- no external API calls, no cron creation, no semantic promotion
- global outputs are rejected if client-like content is detected

Verified 2026-06-19: positive public-watch global dry-run passed; positive synthetic project-local Fathom dry-run passed; global client-like delta failed closed; Fathom delta with shareable scope failed closed.

Verified 2026-06-29: `generate_distillation_run.py` now actually allows `greptile-pr-review-delta` and `graphify-architecture-delta` as project-local-only source kinds, matching this doctrine. Temp-vault tests proved positive report generation for both, refusal when routed globally/company-internal, and refusal of `--schedule`.

When cron is eventually approved, scheduled distillation must:

- use bounded sources only, e.g. Fathom transcript deltas or PR activity deltas
- have caps, cursors/watermarks, source allowlists, and project bindings
- write raw/source pointers and routine compiled context/wiki updates automatically inside the correct scope
- update `brain/context/current.md`, project context cards, session handoffs, index/log/processed when safe
- route project material project-local
- emit an audit/review surface for what changed
- require approval only for risky boundary actions: deletion, publishing, cross-project abstraction, contract/scope-impacting claims, external side effects, or uncertain confidentiality
- require separate approval before cron creation

### 5. Promotion

Promotion is not saving.

Saving records material in a holding destination. Promotion extracts durable claims/actions/decisions into canonical files.

Promotion remains proposal-before-write unless a specific workflow already authorizes the write.

## Claude / paired-programming rule

For high-risk or structural changes, keep Claude Code Opus in the loop through the paired-programming skill.

Use file-output contracts in `/tmp` or another scoped workspace. Let Claude review plans and diffs. Do not give Claude broad uncontrolled write access to the vault unless Rawan explicitly asks and the scope is safe.

Claude may use multiple agents when the task justifies it, but not by default. Multi-agent review is useful for source absorption or broad audits; it is overkill for small rulebook edits.

## qmd posture

qmd is already indexing vault collections. Treat qmd as retrieval support.

Before adding or changing qmd collections, verify current qmd status. Do not create scratch collections or reindex broad client surfaces without approval.

The `brain` qmd collection is now operational. It indexes compiled brain content only:

```yaml
brain:
  path: /Users/batcave/Vaults/asturlab/brain
  pattern: "**/*.md"
  ignore:
    - "BRAIN.md"
    - "raw/**"
    - "wiki/log.md"
    - "wiki/processed.md"
    - "templates/**"
    - "scripts/**"
    - "outputs/**"
```

Verified 2026-06-19: `qmd update` indexed 6 compiled brain docs, `qmd embed` embedded them, `qmd query brain 'autonomous brain context recovery Qayid'` returned compiled brain pages/context. Raw, templates, scripts, outputs, BRAIN.md, wiki log, and processed are excluded.

`knowledge-ops/` is a special case. Because it sits under `asturlab/`, qmd indexed it in the `asturlab` collection by default. That was acceptable while the files were client-free templates only, but fail-open for future ingest receipts.

The qmd fail-safe is now applied in `/Users/batcave/.config/qmd/index.yml`:

```yaml
collections:
  projects:
    path: /Users/batcave/Vaults/asturlab/projects
    pattern: "**/*.md"
    ignore:
      - "**/knowledge-ops/**"
  asturlab:
    path: /Users/batcave/Vaults/asturlab/asturlab
    pattern: "**/*.md"
    ignore:
      - "operations/knowledge-ops/**"
```

This was reviewed with Opus and verified on 2026-06-18: `qmd update` keeps active docs at 36 and `qmd ls asturlab` no longer shows `operations/knowledge-ops`. The projects ignore prevents future project-local ingest metadata from adding qmd noise. If the config is rebuilt later, preserve both ignore rules. Run `qmd embed` only if status says embeddings are needed.

## Greptile + Graphify PR steering posture

For project-control automation, Greptile and Graphify are first-class source surfaces.

Use them together when the goal is PR steering, not just code review:

- Greptile supplies PR review findings, review status/comments, and whole-repo review context.
- Graphify supplies local architecture graph artifacts (`GRAPH_REPORT.md`, `graph.json`, `graph.html`) that Qayid can compare against project direction.
- Qayid synthesizes both against project source-truth planning docs and brain context.

Do not drop Graphify merely because Greptile maps the codebase internally. Greptile's map is primarily internal to its review workflow; Graphify is the inspectable local architecture artifact.

Correct build order:

1. Manual no-write probe after access is granted.
2. Project-local PR steering report.
3. Two useful manual runs.
4. Webhook automation for immediacy, or cron fallback if webhooks are unavailable.

Manual probe support now exists:

```bash
python3 asturlab/operations/knowledge-ops/scripts/generate_pr_steering_probe.py \
  --project estate-agents \
  --repo-ref 'https://github.com/RawMal/admin-estate-agent-portal' \
  --pr-number <number> \
  --head-sha <sha> \
  --greptile-ref <review-or-event-ref> \
  --graphify-report-path <path-to-GRAPH_REPORT.md> \
  --graphify-commit-sha <sha> \
  --max-items 25 \
  --max-chars 20000 \
  --max-lookback-days 14
```

It writes metadata-only project-local probe reports under `projects/<project>/knowledge-ops/reports/pr-steering/`, refuses repo writes/cron/promotion flags, checks the project source allowlist, hashes Graphify artifacts without printing excerpts, and never calls external APIs. Verified 2026-06-29 in a temp vault with positive and refusal tests.

When there is only one active repo, do not over-generalize into a multi-source framework. Treat the first PR as the pilot run: verify the actual app repo path first, confirm the branch is not `main`, then after push consume Greptile's completed review and Graphify artifacts for the same PR head SHA. Ask only for the local repo path, PR URL/number, and Graphify artifact path.

Do not repeatedly trigger `@greptileai` from cron. Prefer Greptile auto-review, then have Qayid detect completed review output and run/read Graphify for the same PR head SHA.

If the app repo lives on Rawan's laptop rather than the Mac mini, treat Qayid as the control plane: bind the PR URL/head SHA project-locally, consume GitHub/Greptile signals through webhook or user-supplied review output, and require Rawan to provide/sync Graphify artifacts from the laptop before claiming architecture analysis. Do not assume a local worktree exists.

For the temporary observation route, use GitHub → HMAC sanitizer relay → Hermes delivery-only Telegram route. The relay must extract PR number/head SHA from `pull_request`, PR issue comments, `check_run.pull_requests[]`, `check_suite.pull_requests[]`, review/comment PR URLs, status payloads, and `push.after` when push events are selected. Verify with a signed synthetic event and a bad-signature `401` before asking Rawan to add the GitHub webhook. Save endpoint/status project-local; never save secrets.

For the first real PR steering run, do not stop at metadata. Add bounded project-local capture for whitelisted Greptile fields (`check_run.output.title/summary/text`, `review.body`, `comment.body`, PR title), store a content hash, and use GitHub Recent Deliveries → Redeliver to replay the real completion event after relay improvements. Generate the steering report only after capturing the actual Greptile output. If Greptile reports success with zero comments, say that clearly and still gate merge on laptop-local build/lint/runtime checks when the repo lives off-machine.

See `references/2026-06-24-greptile-graphify-pr-steering.md` for the detailed pattern, routing, allowlist fields, and failure modes.

See `references/2026-07-02-greptile-webhook-observer.md` for the session-specific observer relay, laptop-local repo handoff, verification pattern, and bounded Greptile output capture lesson.

See `references/2026-07-03-greptile-webhook-capture.md` for the successful PR #2 capture pilot: redelivery, bounded check-output capture, noisy watcher fix, push allowlist pitfall, and merge-gating lesson when Qayid lacks the local worktree.

## Source access posture

Before any live Greptile, Graphify, GitHub, or Fathom connector, use the source-access contract:

```text
asturlab/operations/knowledge-ops/source-access/README.md
```

Local-only readiness checker:

```bash
python3 asturlab/operations/knowledge-ops/scripts/check_source_access.py
```

Rules:

- credentials never go in the vault
- never ask Rawan to paste tokens into chat or vault files
- checker reports presence by name only, never values
- no token files, `.env`, keychains, browser cookies, or credential stores are read
- global Knowledge Ops may store only opaque IDs, counts, hashes, and readiness status
- client-identifying GitHub/Fathom source bindings live project-local
- GitHub/Fathom live probes are separate gated slices after user-side auth setup
- first live probe must be read-only, one source, allowlisted, capped, cursor-bounded, and no-write
- cron remains gated by later-day E6 plus explicit approval

Verified 2026-06-19: local checker found git present, `gh` missing, no git credential helper, no Fathom CLI/env hint; live probe flags are refused by design.

## Common pitfalls

- Treating Knowledge Ops receipts/reports as the product. They are controls; the product is autonomous context recovery and an LLM-maintained brain/wiki.
- Blocking a scoped `brain/` because the vault already exists. The danger is an unsourced competing brain, not a compiled context/wiki layer.
- Making Rawan approve every routine context/wiki update. Gate risky boundary actions; automate safe context maintenance.
- Optimizing for archival safety over time-to-context. The main success metric is whether Qayid can resume a project/session quickly and accurately.
- Putting client-identifying project paths in global Knowledge Ops or global brain pages.
- Treating E-compress as a new standalone product instead of a thin source-type-specific normalization step.
- Treating qmd search results as canonical truth.
- Running cron before a manual dry run proves the workflow.
- Making the E6 report mutate files.
- Using `git add -A` in the vault; there are often pre-existing untracked files.
- Confusing War Room OS with the second-brain/Knowledge Ops foundation.

## Verification checklist

Before calling a build slice done:

- [ ] Top-level `brain/` is treated as the intended autonomous compiled context/wiki layer, not rejected as a competing vault.
- [ ] `brain/**` routine context/wiki writes are allowed autonomously; vault source-truth edits still follow acknowledge/proposal gates.
- [ ] Rulebook edits preserve README = structure and AGENTS = behaviour.
- [ ] Knowledge Ops files contain no client identifiers or snippets.
- [ ] Git status shows only intended paths for the slice.
- [ ] qmd status is checked if retrieval/index claims are made.
- [ ] Claude review is reconciled if paired programming was requested.
- [ ] The skill itself no longer points to old NotebookLM/no-brain assumptions.
- [ ] For project kickoff work, existing planning files are read first and gap-filled; never clobber scaffold or real content blindly.

## Reference

See `references/2026-06-19-integrated-brain-and-project-kickoff.md` for the integrated `brain/` build, the qmd brain collection scope, the roadmap correction, and the urgent-project kickoff lesson: read-first, gap-fill, no clobber, first real use on real work before harvesting a reusable skill.

See `references/2026-06-19-autonomous-context-recovery-correction.md` for the correction that the product is autonomous context recovery and an LLM-maintained brain/wiki, not manual Knowledge Ops paperwork.

See `references/knowledge-ops-first-slice-2026-06-18.md` for the session-specific first-slice implementation notes: the `brain`→`Knowledge Ops` rename, qmd fail-open lesson, client-free registry rule, and Opus review gates.

See `references/e6-status-schema-and-schema-reconciliation-2026-06-18.md` for the E6 status-validation bug, corrected type-scoped schema mapping, schema reconciliation proposal, and the reminder that Knowledge Ops/E6 is foundation work — not the full completed second brain.

See `references/final-second-brain-plan.md` for the detailed phase plan from the June 2026 review.
