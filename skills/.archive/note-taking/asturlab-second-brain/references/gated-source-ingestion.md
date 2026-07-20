# Gated multi-source ingestion for second-brain improvement work

Use this when Rawan asks for a second-brain/vault/memory-system improvement plan that depends on external sources and explicitly gates implementation behind approval.

## Durable pattern

- Treat source ingestion as evidence collection, not planning.
- Use a temporary workspace outside the vault for clones, transcripts, extracted zips, and notes.
- Process one source at a time.
- Write an ingestion note per source before opening the next source.
- Do not inspect or modify the target vault until all required source notes are complete, unless Rawan explicitly changes the gate.
- If using a second model/agent for ultracode review, make it an auditor only. Direct reading by Qayid remains mandatory.
- For GitHub repos, enumerate the tracked tree and read relevant files beyond the README: skills, prompts, configs, docs, source, scheduled jobs, ingestion code, maintenance code.
- For videos, retrieve transcripts and read them end-to-end. A title or description is not ingestion.
- For local ZIPs, verify the archive or extracted target path, then read the requested internal file fully.

## Ingestion note proof tokens

Each note should include concrete proof:

- transcript word count for videos
- repo commit and tracked file count for repos
- files read with paths and line counts for repos
- unzip path and line count for ZIP-contained files
- explicit `could not access` status when blocked

## Tool-cap / context-cap discipline

When the task is long:

- Maintain an explicit todo list.
- Keep source notes in stable temp paths.
- Update the todo immediately when each source note is complete.
- If stopped by tool-call or context limits, report exact source status, paths, and the next action. Do not synthesize prematurely.

## Pitfalls

- Do not use an already-loaded AsturLAB skill as evidence for the source analysis. It can guide workflow, but the claims must come from sources read in-session.
- Do not collapse source ingestion and synthesis. The plan comes only after all sources are read and noted.
- Do not turn scheduled distillation into an everything-harvester. For AsturLAB, scheduled jobs should be bounded and propose-before-write by default.
