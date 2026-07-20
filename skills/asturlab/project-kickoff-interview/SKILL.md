---
name: project-kickoff-interview
description: "Manual project kickoff interview for AsturLAB projects: read existing docs first, fill scaffold/gaps without clobbering, bind repo/Fathom/brain identity, then refresh brain context and qmd."
version: 1.0.0
author: Qayid
license: MIT
metadata:
  hermes:
    tags: [asturlab, kickoff, project-planning, brain, vault]
    related_skills: [asturlab-second-brain, obsidian, qmd]
---

# Project Kickoff Interview

## Trigger

Use when starting or resuming an AsturLAB project and the project needs canonical planning/context before execution.

Use especially when:

- a project has scaffold planning files but no real content yet
- repo/Fathom/Telegram/vault/brain identity may split
- Rawan asks for a manual kickoff or project orientation
- the project is the first real use / field test of the brain workflow

## Hard rule

Do not build a reusable script before the real project run proves the workflow.

Run the manual interview first. Harvest skill/script improvements after.

## Read-first, gap-fill, no-clobber

1. Bind canonical identity:
   - Telegram topic
   - vault slug: `projects/<slug>`
   - brain card: `brain/context/projects/<slug>.md`
   - GitHub repo URL, if any
   - Fathom/transcript URL/title/ID, if any
2. Check whether planning files exist.
3. If they exist, read the smallest sufficient set before writing.
4. Treat planning docs as source-truth.
5. If files are scaffold/empty, fill them.
6. If files already contain real content, preserve it and propose changes instead of overwriting.
7. Capture `TBD` explicitly. Never hide unknowns.
8. Do not lock scope, contract, payment, or client-impacting decisions without explicit confirmation.

## Minimal read order

Announce each read before opening vault files.

For project kickoff:

1. `projects/<slug>/README.md` if it exists.
2. `projects/<slug>/AGENTS.md`.
3. `planning/brief.md`.
4. `planning/scope.md`.
5. `planning/requirements.md`.
6. `planning/tech-plan.md`.
7. `planning/roadmap.md`.
8. `planning/decisions.md`.
9. `planning/next-actions.md`.
10. `planning/risks.md`.

Read `kanban.md` only if execution state matters.

## Interview questions

Ask 8-12 high-signal questions. `TBD` is acceptable.

1. One sentence: what is this project and who is it for?
2. What urgent outcome is needed now, and by what deadline?
3. What must be true for this immediate push to count as done?
4. What is definitely in scope now?
5. What is explicitly out of scope now?
6. What are the 3-5 functional things the product must do?
7. Hard constraints: stack, integrations, hosting, auth, budget, timeline, client preferences?
8. Current state: code, designs, assets, data, credentials, docs, prior work?
9. Architecture guess: how should it work, even roughly?
10. Unknowns/blockers: what needs repo inspection, research, or client input?
11. Locked decisions: what should not be relitigated?
12. Biggest risk: what is most likely to go wrong?

## Answer-to-file mapping

| Answer | Destination |
|---|---|
| what/who, why-now, urgent outcome | `brief.md` |
| done-for-this-push, in scope, out of scope | `scope.md` |
| functional musts, non-functional needs, constraints | `requirements.md` |
| stack, repo state, integrations, architecture, approach | `tech-plan.md` |
| deadline, immediate milestone, next phases | `roadmap.md` |
| locked decisions only | `decisions.md` |
| immediate concrete actions | `next-actions.md` |
| unknowns, assumptions, biggest risks | `risks.md` |
| repo/Fathom/canonical slug/project-specific cautions | `AGENTS.md` |

## Write rules

Before writing outside `brain/**`, announce destination and what is being saved.

Planning files:

- preserve existing real content
- fill scaffold sections when they are empty
- use `draft` for brief/scope/requirements/tech-plan unless explicitly locked
- append decisions newest-first
- record only real locked decisions in `decisions.md`
- use dates where known; use `TBD` where unknown
- add source links and provenance when useful
- keep client-identifying content project-local

Brain files:

- routine updates under `brain/**` can be autonomous
- brain is compiled context, not source-truth
- if brain conflicts with planning files, planning files win

## Brain refresh sequence

Verify actual script names and flags before running. Do not invent flags.

Current known commands:

```bash
python3 brain/scripts/session_capture.py \
  --project <slug> \
  --topic <slug>-kickoff \
  --summary '<brief source-grounded summary>'

python3 brain/scripts/dream.py --refresh-stale --project <slug>

/usr/bin/time -p python3 brain/scripts/load_context.py --project <slug> --status-only

qmd update && qmd embed
```

Then query qmd brain context.

When using qmd structured queries, quote hyphenated slugs in `lex` queries and remove hyphens in `vec` queries. Some parsers treat `estate-agents`-style hyphens as negation in semantic query fields.

## Acceptance tests

- `load_context.py --project <slug> --status-only` returns `fresh` in under 90 seconds.
- `brain/context/projects/<slug>.md` exists.
- The brain project card cites planning files as sources.
- `brain/context/current.md` reflects the active project if appropriate.
- qmd can retrieve the project context from the `brain` collection.
- No variant project slug was created.
- Planning files were not clobbered.
- Scope remains draft unless explicitly locked.

## Pitfalls

- Building kickoff automation before doing the real manual kickoff.
- Treating scaffold files as if they contain real planning.
- Overwriting source-truth planning files without reading first.
- Recording guesses as decisions.
- Creating multiple slugs for one project because repo/Fathom names differ.
- Letting generated brain context become more authoritative than source files.
- Leaving genesis-era/test wording in brain-generated context during real project use.
