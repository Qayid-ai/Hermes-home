---
name: source-material-adaptation
description: Use when converting legitimately accessible external source material—courses, classrooms, skill packs, books, interviews, PDFs, agent workflows, or persona references—into private working notes, Hermes skills/profiles, AsturLAB operating doctrine, or project-ready templates without copying, bypassing access, or importing unsafe behavior.
version: 1.0.0
author: Qayid
license: MIT
metadata:
  hermes:
    tags: [source-material, extraction, adaptation, courses, personas, skills, asturlab, copyright, operations]
    related_skills: [ocr-and-documents, youtube-content, hermes-agent-skill-authoring, google-workspace]
---

# Source Material Adaptation

## Overview

Use this for the whole class of work where Rawan provides or points to source material and wants it extracted, understood, adapted, operationalised, or transformed into a Hermes-native asset.

Examples include:

- paid courses, Skool classrooms, memberships, and private training material;
- third-party AI skill packs, prompt packs, agent workflows, assistant templates, and tool ecosystems;
- books, PDFs, interviews, podcasts, biographies, transcripts, or public-figure material used to build an agent profile/persona;
- source-adjacent strategy libraries, worksheets, resource folders, templates, and schemas.

The shared job is not to copy the source. The job is to preserve its useful structure, separate durable operating patterns from packaging, and translate it into the right private working artifact with explicit boundaries.

## Core Rule

Preserve source structure before applying it.

Do not flatten a course into generic advice, install a skill pack because it is polished, or impersonate a public figure because the source is charismatic. Extract the operating system, label the risks, and adapt only what should survive in Qayid/Hermes/AsturLAB.

## Global Boundaries

1. **Legitimate access only.** Use material exposed through Rawan's account/session or public sources. Do not bypass paywalls, DRM, hidden APIs, access controls, private permissions, or platform restrictions.
2. **No redistribution.** Private extraction and operational application are allowed; creating shareable replicas of paid/copyrighted content is not.
3. **Separate raw extraction from application.** Keep source maps, lesson notes, cleaned frameworks, AsturLAB strategy, profile files, and public-facing outputs in separate files/folders.
4. **Do not copy protected voice or text.** Derive principles, structure, response protocols, and examples. Avoid long quoted passages and copied catchphrases.
5. **Public action requires review.** Posting, scheduling, sending, publishing, or installing integrations with external side effects needs explicit human approval.
6. **Respect workspace boundaries.** Client-identifying or source-adjacent detail stays in the relevant working repo/project folder until Rawan explicitly promotes a cleaned subset.

## Decision Router

### Paid course / classroom / membership

Use the paid-course path when the source is a course, classroom, Skool group, paid membership, private training program, or community with modules/lessons/resources.

Primary outputs:

- `source/course-map.md` — exact module/lesson/resource order and URLs;
- `source/resources-index.md` — attached worksheets, Drive files, PDFs, sheets, slides, folders, and statuses;
- `extraction/lessons/` — one file per lesson in sortable order;
- `outputs/` or `strategy/` — phase synthesis and application only after enough extraction exists.

Key rules:

- map the classroom first;
- preserve sequencing, repetition, exercises, examples, emotional framing, proof points, and transitions;
- keep named course/community work in its own repo/workspace by default;
- never treat a public sales page as the authenticated classroom;
- index attached resources as first-class material;
- label Drive/Docs/Sheets resources by actual state: exported, downloaded, folder_indexed, pending_oauth, or inaccessible.

Detailed references preserved from the former `paid-course-extraction` skill:

- `references/paid-course-extraction-legacy-skill.md`
- `references/skool-rotunda-course-map-and-resources.md`
- `references/skool-rotunda-course-routing.md`
- `references/skool-targeted-large-course-checkpointing.md`
- `references/skool-paid-community-audit-update.md`
- `references/google-workspace-scoped-oauth-for-course-resources.md`
- `references/google-drive-course-resource-exporter.md`
- `references/high-context-phase-synthesis.md`
- `references/doctrine-filtered-phase-synthesis.md`
- `references/cross-phase-doctrine-pass.md`
- `references/spreadsheet-resource-extraction-without-openpyxl.md`

### External skill pack / prompt pack / agent workflow

Use the external-pack path when the source is another agent's skills, prompts, workflows, schemas, references, MCP/runtime assumptions, or tool ecosystem.

Evaluation sequence:

1. Identify the native runtime and install assumptions.
2. Inventory package shape: skills, references, templates, schemas, scripts, memory/state, external keys, public-action surfaces.
3. Separate four layers: knowledge, pattern, capability, execution.
4. Apply AsturLAB boundaries: storage, client confidentiality, human review for public action, no global brand memory by default.
5. Decide integration path: read-only library, support files under an umbrella, selected Hermes-native skill, or native runtime only if explicitly requested.

Core stance:

- Harvest structure; do not inherit behavior.
- Do not install first.
- Prefer durable class-level patterns over package identity.
- Quarantine global memory models, content factories, public posting/scheduling integrations, and API-key collecting behavior.

Detailed references preserved from the former `external-skill-pack-adaptation` skill:

- `references/external-skill-pack-adaptation-legacy-skill.md`
- `references/growthclaw-openclaw.md`

### Source-grounded persona / profile

Use the persona path when Rawan wants to build or refine a Hermes profile/persona from source material: a book, public interviews, YouTube videos, podcasts, biographies, or a named public figure.

Primary output:

- usually `~/.hermes/profiles/<profile-name>/SOUL.md`, edited only when Rawan explicitly asks to modify that profile.

Key rules:

- The goal is not impersonation; the goal is an operational profile.
- Separate style packaging from decision logic.
- Compare source modes instead of averaging them: book voice, interview voice, clip/social voice, etc.
- Let motivational theatre exist when Rawan wants engagement, but attach it to facts, accountability, concrete next actions, and safety boundaries.
- Do not claim to be a public figure or build the profile around copied catchphrases.
- If health, training, fasting, trauma, mental health, medicine, or religion are involved, include explicit safety overrides.

Detailed references preserved from the former `source-grounded-persona-profile` skill:

- `references/source-grounded-persona-profile-legacy-skill.md`
- `references/goggins-style-accountability.md`

## Common Workflow

1. **Classify the source.** Course, skill pack, profile/persona source, research library, or mixed package.
2. **Verify access and boundaries.** Public/private, paid/free, session state, workspace target, allowed outputs, and whether public actions are in scope.
3. **Map before synthesis.** Capture source structure, sequence, assets, and storage model before extracting conclusions.
4. **Extract into private working files.** Use sanitized maps and per-unit notes; avoid raw dumps of private JSON, account metadata, or copyrighted passages.
5. **Separate layers.** Raw source notes, cleaned frameworks, operational doctrine, Hermes skills/profiles, and AsturLAB strategy are different artifacts.
6. **Adapt selectively.** Keep what improves judgment, workflows, templates, diagnostics, or operating cadence. Reject what imports unsafe identity, storage, publishing, or dependency behavior.
7. **Verify the result.** Check links, resource statuses, file paths, profile command visibility, or skill package integrity depending on the output.

## Reference Output Format

When reporting an evaluation or extraction plan, use this shape:

```markdown
Verdict: <extract / harvest / port selected / install with approval / reject>

Source map:
- <source types and structure>

What I would preserve:
- <5-7 highest-value structures, patterns, resources, or protocols>

What I would reject or quarantine:
- <unsafe/noisy/copyright-sensitive/public-action items>

Best working artifact:
- <course workspace / read-only reference / Hermes skill / Hermes profile / project template>

First implementation:
1. <smallest useful action>
2. <verification>
3. <next gated action>
```

## Common Pitfalls

1. **Starting with application instead of structure.** Always map first.
2. **Installing before understanding.** Treat install scripts as evidence, not the default path.
3. **Equating access with permission to redistribute.** Keep extracted source material private.
4. **Letting public-action integrations sneak in.** Posting, sending, scheduling, publishing, and external API side effects need review.
5. **Flattening source identity into generic advice.** Preserve sequencing, design intent, and operating cadence before synthesis.
6. **Copying voice or catchphrases.** Derive a compliant operating profile instead.
7. **Writing raw platform payloads into notes.** Sanitize account/payment/API-key/group-switcher metadata and keep durable maps clean.
8. **Burying resources in summaries.** Treat worksheets, docs, sheets, slide decks, PDFs, folders, and templates as first-class indexed material.
9. **Promoting working doctrine too early.** Course/source-adjacent handoffs stay in the working repo until Rawan asks for promotion.
10. **Creating one-session micro-skills.** Add session-specific detail as `references/`, `templates/`, or `scripts/` under this umbrella.

## Verification Checklist

- [ ] Source class and target artifact identified
- [ ] Access is legitimate and no bypass is attempted
- [ ] Workspace/profile/skill target confirmed when side effects are involved
- [ ] Source structure mapped before synthesis
- [ ] Raw extraction, cleaned frameworks, and application outputs are separated
- [ ] Copyrighted/private material is not redistributed or over-quoted
- [ ] Public-action surfaces and integration risks are named
- [ ] Support files/resources are indexed with truthful statuses
- [ ] Any Hermes profile/skill edits are verified after writing
