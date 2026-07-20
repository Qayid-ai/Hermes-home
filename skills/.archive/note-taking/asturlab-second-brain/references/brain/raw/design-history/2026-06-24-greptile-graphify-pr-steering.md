# 2026-06-24 — Greptile + Graphify PR steering automation

## Context

Rawan corrected the automation priority for the AsturLAB second-brain roadmap: Greptile and Graphify are more important live-use sources than Fathom for the immediate project-control loop.

Active project at time of correction: `estate-agents`.

Key project source surfaces:

- Greptile: PR review, whole-repo indexing, review comments/status, custom review context, MCP access.
- Graphify: local architecture/code graph artifacts already used by Rawan on the codebase and PR.
- Project planning docs: source-truth steering reference.
- Brain: compiled orientation and safe summary layer.

## Decision

Keep Graphify in scope even though Greptile maps the codebase internally.

Reason: Greptile's repo graph is primarily used inside Greptile's PR-review system. Graphify gives Rawan/Qayid a local, inspectable artifact (`GRAPH_REPORT.md`, `graph.json`, `graph.html`) that can be compared against project intent, architecture direction, and second-brain context.

Use the two tools for different jobs:

| Surface | Role |
|---|---|
| Greptile | PR review findings: bugs, security, logic, data/model issues, review status/comments |
| Graphify | Local architecture and dependency signals: drift, hotspots, structural implications |
| Qayid | Steering synthesis against source-truth planning docs and brain context |

## Correct build order

Do not start with cron.

First build a manual, no-write probe after access is granted:

1. Verify Greptile access without exposing credentials.
2. Verify the repo is enabled/indexed in Greptile.
3. Fetch PR review status/comments for the allowlisted repo/PR.
4. Verify Graphify artifacts exist or run Graphify locally against the checked-out PR/repo.
5. Compare Greptile + Graphify signals against project planning docs.
6. Emit a project-local PR steering report.
7. Only then consider webhook or cron automation.

Webhook is the right target for "immediately after Greptile review". Cron is a fallback polling layer, not the primary design.

## Manual PR steering report shape

Target output:

```markdown
# PR Steering Report — <project> PR #<number>

## Verdict
Proceed / Fix first / Stop and rethink

## Greptile blockers

## Graphify architecture signals

## Project-plan drift

## Database / data-model risk

## Deployment risk

## Required fixes

## Brain/project updates proposed
```

## Routing

Keep client-identifying repo and PR artifacts project-local:

```text
projects/<project>/knowledge-ops/source-access/source-allowlist.md
projects/<project>/knowledge-ops/reports/pr-steering/
projects/<project>/knowledge-ops/reports/pr-steering/<date>-pr-<number>-<sha>.md
projects/<project>/knowledge-ops/graphify/<pr-or-sha>/
```

Global Knowledge Ops may store only metadata: generic source kind, counts, hashes, opaque IDs, and readiness status.

Brain may store a compact compiled summary after the report is produced. Brain is not source truth.

## Allowlist fields

Minimum allowlist fields for this class:

```yaml
project: <slug>
repo: <owner/repo>
remote: github
source-kind: greptile-pr-review | graphify-architecture-report
confidentiality: project-local
allowed-operation: read-only-probe | no-write-delta | proposal-only-delta
pr-number: <number or TBD>
base-branch: <branch>
head-ref: <branch or sha>
head-sha-cursor: <sha or TBD>
greptile-review-id: <opaque id or TBD>
graphify-artifact-path: <project-local path or TBD>
max-items: <n>
max-chars: <n>
max-lookback-days: <n>
```

## Failure modes

- Treating Greptile's internal repo map as a substitute for a local architecture artifact.
- Running Graphify on the wrong checkout/head SHA.
- Re-triggering Greptile repeatedly from cron and creating noise/cost.
- Letting Graphify output become source truth rather than a signal.
- Comparing PRs against stale planning docs.
- Writing Greptile/Graphify findings into global Knowledge Ops with client identifiers.
- Croning before two useful manual probe runs prove the signal.
- Confusing "review completed" with "safe to merge". Qayid still decides against project plan/risk.

## Automation target

After proof:

```text
GitHub PR opened/updated
  -> Greptile auto-review runs
  -> Qayid detects completed Greptile review
  -> Qayid runs/reads Graphify for the same head SHA
  -> Qayid emits project-local steering report
  -> Qayid updates brain summary if safe
  -> Telegram summary to Rawan
```

If webhooks are not enabled, use a bounded cron poller as fallback:

- poll open allowlisted PRs every 5–10 minutes
- skip already-processed head SHAs
- never post `@greptileai` repeatedly
- stay project-local
- no source-truth edits without approval
