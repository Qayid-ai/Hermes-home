# Cross-phase doctrine pass

Use this after all phase/module synthesis files are complete and the user asks to move from phase-level extraction into doctrine-level synthesis, while still keeping paid-course material out of the vault.

## Purpose

Build one working synthesis from completed phase outputs that extracts the reusable operating system across the whole course.

This is not the final AsturLAB OS. It is an internal bridge artifact: source-course doctrine is separated from AsturLAB-safe doctrine before any promotion or client-facing rewrite.

## Inputs

Read the smallest sufficient set:

- `outputs/current-extraction-handoff.md`
- `source/course-map.md`
- `outputs/phase-*-synthesis.md`
- `source/attached-resources/manifest.json` only if a phase synthesis flags a resource gap that blocks the cross-phase read

Do not reopen all raw lessons, transcripts, PDFs, spreadsheets, or resource folders unless a phase synthesis has a concrete gap that blocks the pass. This prevents redoing extraction under the guise of synthesis.

## Output location

Write inside the course workspace only, usually:

`outputs/cross-phase-doctrine-pass.md`

Do not write to the vault. Do not ask about vault promotion when the user has already said not to promote. If promotion is mentioned in the output at all, state that promotion requires a separate future explicit instruction after a cleaned, source-safe subset exists.

## Required sections

- `Scope` — internal working synthesis, not vault doctrine and not public content
- `Source Boundary` — exact files inspected; explicitly state missing/unread expected files
- `Course-Level Operating Thesis` — recurring system across phases, not generic motivation
- `Sequence Logic` — why the phases appear in this order and what each cluster contributes
- `Reusable Mechanics Index` — cross-phase mechanics with inputs, artifacts, cadence, lead measures, review loop, recovery diagnostic, AsturLAB-safe translation, quarantine notes
- `Artifact Stack` — grouped by identity/standards, planning/campaigns, execution/day control, review/film study, emotion/recovery, environment/machines, peer/accountability
- `Cadence Stack` — daily through yearly, plus trigger-based cadences
- `Diagnostic Stack` — what the system checks first/second/third when performance slips
- `Doctrine To Keep`
- `Doctrine To Reframe`
- `Doctrine To Reject`
- `AsturLAB OS Implications — Draft Only`
- `Open Questions / Gaps`

## Doctrine filter

Keep mechanics that create agency:

- cadence
- artifacts
- explicit standards
- lead measures
- review loops
- peer accountability that increases agency
- recovery diagnostics
- concrete operating language
- sequencing and instructional design

Quarantine mechanics that create coercion or dependency:

- shame or punishment as enforcement
- public humiliation
- alpha/coward or beast/weakling binaries
- magical thinking and pseudo-scientific authority claims
- unfalsifiable self-blame
- dependency hooks around coach/community/program identity
- trauma excavation repurposed as motivation or content

Translation principle:

> Replace pain-based compliance with friction-based design.

## Verification

After generation:

1. Check the file exists and is non-empty with line/byte counts.
2. Spot-read the opening scope/source-boundary section.
3. Spot-read the ending open-questions section.
4. Patch any contradiction with the user's instruction, especially accidental vault-promotion prompts.
5. Update the local working handoff so the next session knows the cross-phase pass is complete.
6. Close any temporary Claude Code tmux session used for the pass.

## Common pitfall

A high-context agent may include a generic final question like "confirm whether to promote this to the vault" even when the user explicitly said not to promote. Do not pass that through unchanged. Patch it to reflect the current instruction: no promotion now; future promotion requires separate explicit approval.