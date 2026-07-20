---
name: external-skill-pack-adaptation
description: Use when evaluating, importing, or adapting third-party AI skill packs, prompt packs, agent workflows, or assistant templates into Qayid/Hermes for AsturLAB.
version: 1.0.0
author: Qayid
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [skills, adaptation, strategy, operations, vault, external-packages]
    related_skills: [hermes-agent, hermes-agent-skill-authoring]
---

# External Skill Pack Adaptation

## Overview

Use this when Rawan uploads or points to an external skill pack, prompt pack, agent workflow, GPT instruction set, OpenClaw/Claude/Codex package, or marketing/ops playbook and asks what Qayid can use from it.

The default failure mode is importing too much.

Do not treat a package as valuable because it is large, polished, or full of workflows. Most packages contain a small reusable core wrapped in noisy execution behaviour. Your job is to separate the durable class-level patterns from the package’s native identity, storage model, tool assumptions, and unsafe side effects.

## Core Rule

Harvest structure. Do not inherit behaviour.

A good adaptation gives Qayid better judgment, better questions, better workflows, or better templates.

A bad adaptation turns Qayid into the author’s agent, a content bot, a publisher, or a tool stack maintainer.

## Evaluation Sequence

1. **Identify native runtime and install assumptions.**
   - Hermes skill, OpenClaw skill, Claude skill, GPT instructions, shell scripts, MCP server, etc.
   - Do not install by default.
   - Treat install scripts as optional evidence, not the first action.

2. **Inventory the package shape.**
   - Skills/workflows.
   - References/knowledge files.
   - Schemas/templates.
   - Scripts/integrations.
   - Memory/state directories.
   - External keys and public-action surfaces.

3. **Separate four layers.**
   - Knowledge layer: references, frameworks, domain notes.
   - Pattern layer: decision loops, memory protocols, routing logic, quality gates.
   - Capability layer: skills worth porting into Hermes.
   - Execution layer: scripts, API keys, schedulers, send/post/publish integrations.

4. **Apply AsturLAB boundaries.**
   - Client-identifying detail stays inside the relevant project folder.
   - AsturLAB marketing/content folders are not Qayid’s default write target.
   - Public posting, sending, scheduling, or publishing requires human review.
   - If the package uses a global shared workspace, rewrite storage before adoption.

5. **Decide the integration path.**
   - Keep read-only if it is mainly references.
   - Port selected class-level skills if there is reusable procedure.
   - Add support files under an existing umbrella if details are package-specific.
   - Install the native runtime only when Rawan explicitly wants that runtime.

## What to Look For

Highest-value extractables:

- Well-written reference files.
- Schemas that can become AsturLAB project records.
- Memory protocols: read-before-write, append-only journals, freshness signals, context matrices.
- Diagnostic loops: scan state, identify constraint, recommend one next action.
- Quality gates: live-vs-estimated evidence, confidence labels, diff-before-overwrite.
- Narrow advisory workflows that improve strategy or operations.

Usually low-value or dangerous:

- Auto-chained “full team” workflows.
- Content factories.
- Public posting/scheduling/sending integrations.
- Global brand memory or shared campaign folders.
- API-key audit skills that nudge toward tool collecting.
- Runtime-specific installers when Hermes can port the useful logic directly.

## GrowthClaw/OpenClaw Case Study

The GrowthClaw package from this session is the model case. See `references/growthclaw-openclaw.md` for the condensed package-specific notes.

Useful:

- `positioning-angles/references/` as a read-only strategy library.
- `_vibe-system` memory protocol: profile vs append-only files, Context Matrix, freshness rules, live-vs-estimated signals.
- `positioning-angles` process as a Qayid-native positioning/offer pressure-test.
- `campaign-brief.schema.json` repurposed as an engagement/project record.
- `keyword-research` validation fragments as market-demand go/no-go checks.
- `stack-key-advisor` cost-discipline stance, generalized beyond marketing keys.

Reject/quarantine:

- Installing OpenClaw/GrowthClaw wholesale.
- `install.sh` creating a global `~/.openclaw/workspace/brand/`.
- ESP/social scheduling keys.
- Replicate creative generation as Qayid default.
- Content-production skills: SEO content, newsletters, email sequences, lead magnets, atomization, direct-response copy, brand voice.

Reason:

The package is mostly inert markdown, so the main risk is not malware. The main risk is identity, storage, and public-action behaviour. It would make Qayid act like a marketing publisher and write to a shared global brand store.

## Output Format

When reporting an evaluation to Rawan, use this shape:

```markdown
Verdict: <harvest / port selected / install / reject>

What I would use:
- <5-7 highest-value items>

What I would reject or quarantine:
- <unsafe/noisy items>

Best integration path:
- <read-only library / support files / Hermes-native skill / native runtime>

First implementation:
1. <smallest useful action>
2. <verification>
3. <next gated action>
```

Keep it practical. Do not write a generic software review.

## Common Pitfalls

1. **Installing before understanding.** Read the package shape first. Install only when the native runtime itself is the goal.
2. **Confusing security risk with behaviour risk.** A package can be inert and still wrong for Qayid because of identity, storage, or publishing assumptions.
3. **Creating narrow one-package skills.** Prefer a class-level adaptation skill with package-specific notes in `references/`.
4. **Importing global memory models.** Rewrite storage to AsturLAB/vault project boundaries before adoption.
5. **Letting content workflows invade Qayid.** Qayid can critique, scope, and draft when asked. Qayid does not become Khabeer or a public-content publisher.
6. **Overvaluing integrations.** Keys and tools are not strategy. Prefer minimum viable stack and explicit review gates.

## Verification Checklist

- [ ] Native runtime identified
- [ ] Package layers separated: knowledge, pattern, capability, execution
- [ ] Public-action surfaces named
- [ ] Storage model checked against vault/client-confidentiality rules
- [ ] Reusable class-level patterns extracted
- [ ] Install decision justified
- [ ] First implementation is small and verified
