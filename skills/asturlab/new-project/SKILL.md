---
name: new-project
description: Scaffold a new project under ~/Vaults/asturlab/projects/ with the full four-folder structure, planning subfolder (8 files), and stub README. Use when creating any new project for AsturLAB or Rawan's work.
---

# new-project

Scaffolds a new project in the AsturLAB vault following the locked structure: four sub-folders (notes, sessions, research, communications), a planning subfolder with eight canonical files, and a stub README.

## When to use

Trigger 1 — explicit request. The user says any of:
- "create a new project called X"
- "scaffold project X"
- "/new-project X"
- "set up a new project for X"

Trigger 2 — implicit. The user describes work that clearly needs a new project folder and there isn't one yet.

## Confirmation is mandatory

Both triggers require explicit confirmation before scaffolding. Do NOT scaffold without it.

For trigger 1 (explicit), echo back the action:

> "About to scaffold new project `<name>` at `~/Vaults/asturlab/projects/<name>/`. This creates 12+ files and folders including the planning scaffold. Confirm?"

Wait for "yes", "go ahead", "confirm", "scaffold it" or equivalent before running the script.

For trigger 2 (implicit), propose first:

> "This sounds like a new project. Want me to scaffold one called `<suggested-name>`? It'll create the full folder structure under `projects/<suggested-name>/`."

Same confirmation discipline. Implicit creation without confirmation is forbidden. The user owns the decision to start a new project.

## Project name validation

Names must match `^[a-z][a-z0-9-]*$` — lowercase letters, digits, and hyphens only. Must start with a letter.

Valid: `estate-agents`, `khabeer-website`, `acme-cms`
Invalid: `Estate Agents`, `khabeer_site`, `2024-project`

If the user gives an invalid name, suggest a valid form and ask them to confirm the corrected name before scaffolding.

## How to invoke

After confirmation, run the scaffold script with the validated project name:

```bash
bash ${HERMES_SKILL_DIR}/scripts/scaffold-project.sh <project-name>
```

The script:
1. Refuses to overwrite an existing project folder
2. Creates the four-folder structure
3. Creates a stub README.md
4. Calls the planning scaffold for the eight planning files
5. Prints a tree of the result

## Project kickoff interview after scaffold or when a project already exists

When a project is new, urgent, or only partially understood, do **not** block work with an exhaustive discovery process. Run a short kickoff interview that creates usable drafts and explicit unknowns.

If the project folder already exists, **read-first, gap-fill, no clobber**:

1. Confirm the canonical slug.
2. Check whether `projects/<slug>/planning/` already contains canonical files.
3. Read existing planning files before proposing edits.
4. Preserve existing content.
5. Fill gaps or propose updates; never blindly regenerate planning docs.
6. Allow answers like `TBD`, `unknown`, and `research needed`.
7. Put unknowns and assumptions in `planning/risks.md` or the relevant file's unknowns section.
8. After planning updates, run/trigger the AsturLAB Brain loop so `brain/context/projects/<slug>.md` and `brain/context/current.md` are refreshed.

Use 8–12 high-signal questions, trimming when urgency is high:

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

Map answers:

| File | Input |
|---|---|
| `brief.md` | what/who, why now, urgent outcome |
| `scope.md` | done for immediate push, in/out of scope |
| `requirements.md` | must-do functions, constraints |
| `tech-plan.md` | stack, repo state, integrations, approach |
| `roadmap.md` | deadline, immediate milestone, next phases |
| `decisions.md` | locked decisions only |
| `next-actions.md` | immediate next 1–3 actions |
| `risks.md` | unknowns, assumptions, biggest risk |

When the project has external sources, establish a binding map early:

```text
Telegram topic <-> vault project slug <-> GitHub repo URL <-> Fathom meeting ID/URL <-> brain project card
```

For urgent work, run the manual interview first and harvest/update automation after the real project is unblocked.

## After scaffolding

Tell the user:
- The project folder location (`~/Vaults/asturlab/projects/<name>/`)
- That a Telegram channel/topic with the same name should be created for Rule 4 channel mapping to work (per Context Matrix in SOUL.md)
- Suggest the next action: open `planning/brief.md` and document the original ask

## Failure modes

- Project name invalid → don't run the script. Ask user for a valid name.
- Project folder already exists → script exits 1, surface this — do not overwrite, do not retry.
- Vault path missing → script exits 1, surface this — vault setup is broken.

Do not retry on failure. Surface the error to the user.
