---
name: source-grounded-persona-profile
description: Create or update Hermes agent profiles from source material such as books, PDFs, interviews, and transcripts without cloning copyrighted text or unsafe personas.
version: 1.0.0
created_by: agent
---

# Source-grounded persona profile

Use this when Rawan asks to build or refine a Hermes profile/persona from source material: a book, public interviews, YouTube videos, podcasts, biographies, or a named public figure.

The goal is not impersonation.

The goal is an operational profile: voice, principles, boundaries, protocols, and escalation rules.

## Core rule

Separate **style packaging** from **decision logic**.

The persona may sound intense, formal, warm, analytical, theatrical, or confrontational. The operating system underneath must stay safe, useful, and grounded.

For motivational profiles, theatre is allowed when the user wants engagement. It must be attached to facts and action. No speeches without a rep.

## Workflow

1. Confirm the target use case.

Ask what the profile is for only if it changes the design: fitness accountability, sales coach, writing editor, research analyst, spiritual reminder, etc.

2. Gather source material.

Use the smallest sufficient set:

- PDFs/books: extract text and inspect structure first.
- YouTube/podcasts: prefer long-form interviews with transcripts over short clip farms.
- Existing profile files: inspect `~/.hermes/profiles/<name>/SOUL.md` before editing.

3. Build a source map.

Capture source types, not raw dumps:

- book/PDF: page count, extraction quality, table of contents, chapter themes.
- videos: title/source, duration, transcript availability, approximate transcript size.
- interviews: voice differences between contexts.

4. Derive, do not copy.

Extract:

- Voice profile.
- Operating principles.
- Response protocols.
- Escalation triggers.
- Safety boundaries.
- Banned behaviours.
- Example response patterns.

Do not copy passages or catchphrases from copyrighted books, paid material, or public figures.

5. Write the profile.

For Hermes profiles, `SOUL.md` is usually the right target:

`~/.hermes/profiles/<profile-name>/SOUL.md`

Use `cross_profile=true` only when Rawan explicitly asked to edit that profile.

6. Verify.

After writing:

- Read the first section back.
- Check `hermes profile show <name>` if available.
- Report what changed and how to run it.

## Voice analysis pattern

Compare source modes instead of averaging them.

Example categories:

- Book voice: formal, reflective, structured, philosophical.
- Interview voice: conversational, explanatory, story-led.
- Clip/social voice: compressed, theatrical, high-intensity.

Set one as the default and define when the others are allowed.

Do not let the loudest source dominate by default. Public clip voice is often an attention hook, not the full operating personality.

## Accountability profile pattern

For a strict accountability agent, include:

- Facts-first check-in.
- Constraint vs excuse separation.
- One weak point named plainly.
- One next action.
- Proof requirement.
- Safety override for injury, illness, sleep debt, family duty, religious obligations, and crisis signals.

Suggested check-in fields:

- Sleep.
- Body/injury/illness.
- Training or habit target.
- Food or recovery.
- Work output.
- Avoided thing faced.
- Religious/family obligations when relevant.

## Safety rules

If the persona touches health, training, fasting, trauma, mental health, medicine, or religion, add explicit boundaries.

The profile must not:

- diagnose;
- prescribe extreme training or fasting;
- shame injury, illness, trauma, or religious duty;
- encourage unsafe overtraining;
- impersonate a public figure as if it is that person;
- quote long copyrighted passages.

The profile should switch from theatre to sober guidance when risk appears.

## User preference from Rawan

Rawan may want motivational theatre because it makes the profile more engaging. Do not flatten that into sterile coaching. Keep the theatre, but make it serve the system: facts, accountability, safe constraints, and a concrete next rep.

If Rawan asks for direct impersonation of a public figure or copied catchphrases, even for personal use, hold the line: do not make the profile claim to be the person and do not build the operating voice on copied catchphrases. Then act, not just refuse: translate the request into a stronger compliant fictional trainer/coach in the same energy lane, with first-person pressure, original catchphrases, harsher check-ins, drill-mode escalation, and a clear disclaimer that it is not the real person.

Naming matters. If the profile name itself keeps pulling the design toward celebrity cosplay, suggest renaming the profile to an original operating identity, but do not force the rename before improving the profile.

When the user says the celebrity-inspired framing is for personal motivation, treat the motivational theatre as a legitimate engagement requirement. Keep the legal/identity boundary, but increase intensity and fun immediately if the profile is already authorized for editing.

## References

- `references/goggins-style-accountability.md` — session note on building the `david-goggins` profile from *Never Finished* plus long-form YouTube interviews.
