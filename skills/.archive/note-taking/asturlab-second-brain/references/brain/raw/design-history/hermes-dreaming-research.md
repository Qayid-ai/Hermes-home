# Hermes Dreaming Research — June 2026

## Why this exists

Rawan challenged an overly narrow interpretation of “Dreaming” as second-brain maintenance. The corrected model is broader.

## Core correction

Dreaming in a Hermes/AsturLAB context should mean **offline consolidation for the agent and operation**, not just wiki linting.

Second-brain hygiene is one branch. It is not the whole concept.

## Source signals checked

### Hermes primitives

Hermes does not currently expose a built-in `/dream` primitive in the checked docs/skill material.

Hermes has the components to implement Dreaming:

- cron jobs
- session search
- persistent memory
- skills
- qmd / vault search
- file writes
- background agents / tmux Claude Code when needed
- profile isolation

### Anthropic Dreams pattern

Anthropic's managed-agent Dreams docs describe an asynchronous pass that reads:

- an existing memory store
- 1–100 past session transcripts

It produces a separate output memory store with:

- duplicates merged
- stale or contradicted entries replaced with newer values
- new insights extracted from sessions
- reorganized memory content

Important safety posture: the input store is not modified. The output is reviewable and discardable.

### Karpathy LLM Wiki pattern

Karpathy-style LLM Wiki dream/lint is narrower:

- ingest backlog
- contradictions
- stale claims
- duplicate pages
- orphan pages
- missing sources
- index/log/processed consistency

This is **wiki dreaming**, not full agent dreaming.

## Recommended AsturLAB Dream layers

### 1. Memory consolidation

Review recent sessions, memory entries, user profile, repeated corrections, stale memories, duplicate memories, and missed durable facts.

Output:

- proposed memory adds
- proposed memory replacements
- proposed memory removals

Default: confirmation-required unless clearly safe and already permitted by the active memory rules.

### 2. Skill consolidation

Review repeated workflows, tool quirks, failures overcome, procedures that should become skills, stale skills, and missing pitfalls.

Output:

- proposed new skills
- proposed skill patches
- stale skill warnings
- “this should have been a skill” findings

This is Hermes-native and should be treated as first-class.

### 3. Brain / knowledge consolidation

Run the Karpathy-style checks over the AsturLAB brain:

- raw source backlog
- duplicate pages
- contradictions
- stale claims
- weak citations
- orphan pages
- missing links
- unreviewed captures
- index/log/processed consistency

Output:

- Dream report
- safe nav/bookkeeping updates
- semantic edits as proposals

### 4. Operational consolidation

Review execution patterns across sessions:

- slipping commitments
- overlarge plans
- recurring bottlenecks
- client/project friction
- where Qayid failed to push back
- where cron/accountability should exist
- what should be escalated into War Room OS

Output:

- proposed operating changes
- suggested cron changes
- recurring bottlenecks
- chief-of-staff findings

## War Room distinction

War Room OS is separate from Dreaming.

War Room OS creates strategy, cadence, scorecards, and daily/weekly/monthly accountability crons.

Dreaming audits what the agent and operation learned from what actually happened.

They should eventually interact:

- War Room says what should happen.
- Crons keep execution aligned.
- Dreaming asks what changed, what was learned, and what the system should update.

## Build guidance

Manual Dream first. Cron later.

A manual Dream report should be structured like:

```text
Dream Report
├── Memory findings
├── Skill findings
├── Brain findings
├── Operational findings
└── Proposed writes
```

Auto-write only low-risk artifacts:

- Dream report file
- log entry
- regenerated navigation/index files where already allowed

Confirmation-required:

- memory changes
- skill creation/patches
- strategic changes
- project decisions
- client-related consolidation
- cron creation
- semantic brain page edits

## Pitfall

Do not answer future “Dreaming with Hermes” questions by defaulting to second-brain maintenance. Start from the four-layer consolidation model, then narrow if the user explicitly asks about the brain/wiki layer.
