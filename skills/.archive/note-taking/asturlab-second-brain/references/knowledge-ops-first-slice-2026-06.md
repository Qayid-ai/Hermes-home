# Knowledge Ops first slice — June 2026

## Durable lesson

The AsturLAB second-brain work should strengthen the existing vault, not create a parallel `knowledge-base/` or top-level `brain/` folder.

In the AsturLAB rulebooks, **Brain** already refers to the NotebookLM Brain. For vault-side metadata/control, use **Knowledge Ops**:

```text
/Users/batcave/Vaults/asturlab/asturlab/operations/knowledge-ops/
```

## Implemented first slice

Vault rulebooks were updated to add:

- system-of-record lookup: vault first, session search for conversation recall, NotebookLM Brain as semantic fallback
- E-compress as conditional preprocessing, not a standalone subsystem
- ingest receipt schema
- provenance and confidentiality labels
- proposal-first automation gates
- client-free global metadata rule

Knowledge Ops scaffold:

```text
asturlab/operations/knowledge-ops/
├── README.md
├── index.md
├── log.md
├── processed.md
└── maintenance/README.md
```

## Critical naming correction

Do not use `brain/` for this metadata/control surface.

Claude Opus caught this during review: `brain-first` and `operations/brain/` collide with NotebookLM Brain terminology and could route future sessions toward external semantic search instead of the vault as source of record.

Use:

- `Knowledge Ops`
- `system-of-record lookup`
- `vault-first lookup`

Avoid:

- `brain-first lookup`
- top-level `brain/`
- `asturlab/operations/brain/`
- standalone `knowledge-base/`

## Confidentiality invariant

`asturlab/operations/knowledge-ops/` is stricter than the rest of `operations/`:

- metadata only
- client-free
- no client project folder paths if the slug identifies the client
- no meeting excerpts
- no transcript snippets
- no repo names that identify clients

Project-specific receipts, logs, and coverage registries live project-local.

## qmd follow-up

qmd indexes `knowledge-ops/` under the `asturlab` collection because it sits under `asturlab/`.

This is acceptable while the folder contains only client-free templates and procedures. Before the first real receipt lands, add a qmd ignore/exclusion for one of:

```text
asturlab/operations/knowledge-ops/
asturlab/operations/knowledge-ops/receipts/
```

The goal is to make the client-free invariant fail-safe instead of discipline-only.

## Claude pairing pattern used

For this vault rulebook work, Claude Code Opus ultracode was useful at two gates:

1. pre-edit review of the proposed slice
2. post-edit final review of diff + new files + rewritten skill

Claude caught:

- `brain` naming collision
- Context Matrix belongs in SOUL, not AGENTS
- global registries in `operations/` must not contain project slugs that identify clients
- qmd indexing is acceptable now but needs an exclusion before real receipts

Keep Claude in the loop for future structural slices, but constrain it with file-output contracts and read-only scope unless direct editing is explicitly approved.
