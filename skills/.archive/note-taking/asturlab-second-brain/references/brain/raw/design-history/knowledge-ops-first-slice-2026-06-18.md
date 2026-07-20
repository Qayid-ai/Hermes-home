# Knowledge Ops first slice and E6 scrub lesson — 2026-06-18

## What changed

AsturLAB second-brain work was routed into the existing vault rather than a parallel `brain/` or `knowledge-base/` tree.

Canonical control surface:

```text
/Users/batcave/Vaults/asturlab/asturlab/operations/knowledge-ops/
```

This folder is a client-free metadata/procedure layer only. It is not the system of record for project truth.

## Opus review loop

For structural vault work, keep Opus in the loop as a reviewer, not an uncontrolled mutator.

Useful pattern:

1. Qayid prepares the proposed change or draft.
2. Send Opus a narrow prompt with read-only constraints.
3. Require Opus to write its review to `/tmp/.../outputs/<slug>.md`.
4. Read that file directly.
5. Apply only the reviewed changes yourself.
6. Re-run verification and, if needed, send a final review prompt.

Do not let the reviewer spawn broad agents or write into the vault unless Rawan explicitly approves that scope.

## qmd fail-safe lesson

`knowledge-ops/` sits under the indexed `asturlab` collection root, so qmd originally indexed it. That was safe while the files were templates, but fail-open for future receipts.

Fix applied in:

```text
/Users/batcave/.config/qmd/index.yml
```

```yaml
collections:
  asturlab:
    path: /Users/batcave/Vaults/asturlab/asturlab
    pattern: "**/*.md"
    ignore:
      - "operations/knowledge-ops/**"
```

Verification outcome:

- `qmd update` removed 5 active Knowledge Ops docs.
- `asturlab` collection dropped from 15 to 10 docs.
- `qmd ls asturlab | grep knowledge-ops` returned no active docs.
- `mcp_qmd_status` showed 36 total docs and 0 embeddings needed.

## E6 confidentiality scrub lesson

First E6 draft leaked too much by printing freeform `status:` strings and project slugs. Opus caught it.

Rule: global/client-free maintenance reports must use counts and categories only.

Do not include:

- verbatim freeform frontmatter values
- project slugs that identify clients or products
- transcript titles
- repo names tied to a client
- raw excerpts
- proposal paths revealing project/client identity

Safe replacement shape:

```text
Top-level status fields: 28
Recognized enum values: 21
Non-conforming/freeform values: 7
Temporal markers: temporal_supersession_or_regression=2, temporal_evolution=1, primary_version_marker=4
Client-identifying data present in this report: no
```

## E6 report contract

A complete E6 report should include:

- checks run
- confidence
- risk
- explicit client-identifying-data line
- qmd/index health
- holding-pen threshold and counts
- frontmatter/status conformity
- temporal marker counts
- duplicate rough scan
- weak-link/orphan rough scan
- source-pointer rough scan
- coverage arithmetic
- proposal-only next actions
- automation gate state

Cron remains closed until two consecutive scrubbed, contract-complete manual E6 passes.

## Known false positives to suppress in E6 #2

- `AGENTS.md` and `README.md` are rulebooks; do not flag them for missing frontmatter.
- Repeated canonical filenames across projects (`README.md`, `AGENTS.md`, `planning/brief.md`, etc.) inflate duplicate-title counts. Treat them as expected unless exact content duplicates exist.
- Weak-link/orphan scans are heuristic unless they fully understand Obsidian wikilinks, relative links, and implicit project structure.
