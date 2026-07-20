# 2026-06-19 correction — autonomous context recovery, not manual Knowledge Ops

## What happened

During the second-brain build, Qayid over-corrected toward confidentiality/control and under-built toward Rawan's stated product: an autonomous LLM-maintained wiki/brain that preserves operational context across sessions, chats, and project returns.

The built Knowledge Ops control plane is useful, but it is not the main artifact. It became too manual: receipts, dry-runs, proposals, and gates. Rawan pushed back that this sounded like manual maintenance from him.

## Corrected intent

The second brain exists to minimize Qayid's time-to-context.

Success looks like:

```text
new session -> Qayid knows where we are
new chat -> Qayid can load the right project state
old project return -> Qayid resumes from current truth without Rawan re-explaining
```

The system should be an active context recovery layer, not only an archive or governance process.

## Architecture correction

A scoped top-level `brain/` or equivalent compiled layer is allowed and likely needed.

Suggested shape:

```text
brain/
  raw/
  wiki/
    index.md
    log.md
    processed.md
  pages/
  context/
    current.md
    projects/
    sessions/
  outputs/
  scripts/
```

Key artifacts:

- `brain/context/current.md` — current operating context, active projects, open loops, recent changes, where to resume.
- `brain/context/projects/<project>.md` — project context card with current state, decisions, risks, next actions, entities, repos/Fathom/source bindings, citations.
- `brain/context/sessions/<date>-<topic>.md` — compact session handoff with decisions, changes, open loops, next resume action.
- `brain/wiki/*` — compiled LLM-maintained knowledge pages with source links.

Knowledge Ops remains the control plane:

```text
asturlab/operations/knowledge-ops/
```

It should hold protocols, schemas, receipts, access gates, and maintenance contracts. It is not the brain itself.

## Automation correction

Do not reject auto-fetch outright. Reject reckless auto-fetch.

Bad:

```text
pull everything -> summarize everything -> silently write global memory/wiki
```

Good:

```text
allowlisted source -> cursor/caps -> project binding -> E-compress -> auto-update scoped context/wiki -> audit/review surface
```

Routine context/wiki maintenance should be automatic. Approval should be reserved for risky boundary actions:

- deletion/archive
- publishing
- external side effects
- cross-project abstraction
- contract/scope-impacting claims
- uncertain confidentiality

## Pitfall to avoid

Do not treat qmd search as context. qmd retrieves. Context cards orient.

Do not make Rawan the maintenance loop. His role is source approval, correction, and high-risk boundary approval.
