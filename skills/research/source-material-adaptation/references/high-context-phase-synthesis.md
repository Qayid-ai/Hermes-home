# High-context phase synthesis for extracted courses

Use this after the classroom map, lesson files, transcripts, and attached-resource manifest exist.

## When to use

Use high-context synthesis when the course is too large for one careful pass, or when Rawan explicitly wants the coach's operating system preserved before AsturLAB application.

Do not synthesize all lessons in one flat pass unless the course is small. Large courses should be handled by phase/module ranges.

## Recommended contract

For each phase range, create a prompt file under the working repo, for example:

`extraction/phase-synthesis/phase-0-1-claude-prompt.md`

The prompt should include:

- the exact lesson range and purpose;
- the ordered lesson file paths;
- cleaned transcript text or concise lesson extracts;
- attached-resource manifest entries relevant to those lessons;
- explicit instruction to preserve sequence, repetition, and instructional design;
- explicit instruction not to produce public-facing copy or motivational mush;
- an output path under `./outputs/<slug>.md`.

## Claude Code interactive path

When using Claude Code interactively for subscription/high-context work, use the `claude-code` skill's file-output contract:

- start a tmux session in the working repo;
- submit prompts with `C-m`;
- use pane captures only for login, trust prompts, approval prompts, progress, and `WRITTEN ...` status;
- require Claude to write the final synthesis to `./outputs/<slug>.md`;
- read the markdown file directly as the source of truth.

## Output shape

A useful phase synthesis should produce:

- phase purpose and role in the full course;
- lesson-by-lesson progression;
- repeated concepts and language;
- frameworks, rituals, and operating cadence;
- worksheet/resource interpretation, not just links;
- failure modes the coach is warning against;
- what this phase changes in behaviour;
- private AsturLAB application notes kept separate from raw extraction.

## Pitfalls

- Do not let a high-context model flatten the course into generic principles.
- Do not combine unrelated phases just to save orchestration time.
- Do not treat transcripts as complete if worksheets, PDFs, Docs, or Sheets are part of the lesson.
- Do not scrape the Claude Code pane as the final synthesis. The pane is a control plane; the file is the answer.
- Do not produce public marketing material from paid course extraction. Keep outputs private and operational.
