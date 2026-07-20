# Doctrine-filtered phase synthesis for paid courses

Use this when a paid course is being extracted not just for summaries, but to convert its operating system into AsturLAB doctrine without importing coercive or pseudo-scientific mechanics.

## When to use

Use after the raw course map, lesson files, transcripts, and first-class resources are extracted.

Best fit:

- high-ticket coaching programmes;
- performance/business doctrine courses;
- courses with strong motivational language, identity work, accountability rituals, community pressure, or worksheet-heavy implementation systems;
- phase/module-by-phase/module synthesis where flattening the whole course into one generic summary would lose sequence and cadence.

## Phase-by-phase contract

For each phase/module range, synthesize only that phase deeply.

Inputs:

- `source/course-map.md` for global position;
- the relevant `extraction/lessons/<range>.md` files;
- attached worksheets, PDFs, slides, spreadsheets, folders, and resource indexes for that same range;
- previous phase synthesis files only as prerequisite context, not as material to re-summarize.

Output:

- one markdown file under `outputs/phase-<n>-synthesis.md`;
- scope and lesson range;
- placement in the course sequence;
- resource inventory and what was actually inspected;
- operating mechanics extracted from transcripts and resources;
- cadence/artifacts/standards/lead measures/review loops/peer accountability/recovery diagnostics;
- exact coach language where needed, quoted briefly;
- contradictions, risk flags, and dependency mechanics;
- AsturLAB translation split into `Useful as-is`, `Useful after reframing`, and `Reject / avoid`.

## Doctrine filter

Keep:

- cadence;
- artifacts;
- explicit standards;
- lead measures;
- review loops;
- peer accountability that increases agency;
- recovery diagnostics;
- concrete operating language;
- worksheets that expose a reusable system;
- sequencing, repetition, and instructional design.

Quarantine:

- shame as a control mechanism;
- punishment rituals;
- public humiliation;
- alpha/coward or beast/weakling binaries;
- magical thinking and Law-of-Attraction framing;
- pseudo-scientific authority claims;
- unfalsifiable self-blame;
- dependency hooks such as social exposure, identity capture, fear-based retention, forced jargon, or coach/community reliance;
- trauma excavation repurposed as motivation or content.

Translation principle:

> Replace pain-based compliance with friction-based design.

Do not merely delete the coercive surface language. Extract the legitimate mechanism underneath, then rebuild it as a lower-coercion system: environment design, visible artifacts, default cadence, short feedback loops, and clear recovery paths.

## Resource-first rule

Do not treat worksheets, slides, spreadsheets, PDFs, and Drive folders as footnotes to the videos.

For each phase, explicitly inspect phase-specific resources before writing the synthesis. If a resource cannot be read, state why. If a transcript says one thing and a worksheet operationalises it differently, the worksheet may be the truer operating system.

## High-context agent workflow

For large phases, use a high-context agent with a file-output contract rather than relying on chat scrollback.

Required contract:

- run from the course workspace;
- produce `./outputs/<phase-slug>.md`;
- read relevant lesson files and resources directly;
- never paste credentials or raw private page state into the prompt;
- do not write public-facing content;
- preserve source/course distinctions.

Preferred pattern for Claude Code:

- fresh tmux/agent session per phase;
- submit the prompt with `C-m`;
- approve only bounded file reads/writes/scripts required for resource inspection;
- inspect the produced file with `wc`, `stat`, and spot reads before marking the phase complete;
- use pane capture only for status/errors/approval prompts, not as the source of truth.

## Handoff between context windows

When the job may exceed one conversation window, maintain a concise working handoff inside the course workspace, e.g. `outputs/current-extraction-handoff.md`.

The handoff should include:

- workspace path;
- extraction counts: modules, resources, transcripts;
- completed phase outputs;
- active agent/session name if relevant;
- current phase and lesson range;
- blockers;
- next phase;
- critical decisions and filters.

Keep this handoff out of the vault until Rawan explicitly promotes durable doctrine. Paid-course source-adjacent material belongs in the working repo by default.
