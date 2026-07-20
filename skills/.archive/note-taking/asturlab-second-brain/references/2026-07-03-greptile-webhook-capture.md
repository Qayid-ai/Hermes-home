# 2026-07-03 — Greptile webhook output capture pilot

## Context

Project: `estate-agents`.
Repo: `RawMal/admin-estate-agent-portal`.
Repo worktree lived on Rawan's laptop, not the Mac mini. Qayid/Mac mini acted as the control plane only.

Goal: prove GitHub → sanitizer relay → Hermes delivery-only route could observe Greptile PR review completion and capture enough bounded data for a project-local steering report.

## What worked

The receiver path was proven:

```text
GitHub webhook
→ Cloudflare tunnel
→ HMAC sanitizer relay
→ Hermes delivery-only webhook route
→ Telegram notification
```

GitHub `ping`, `push`, `pull_request`, `check_run`, and `check_suite` deliveries reached the relay.

Greptile completion was observed on `check_run.completed` with app slug/name matching Greptile. Redelivering the completion event after relay improvements produced bounded check output capture.

Captured real Greptile output for PR #2:

```text
Greptile has reviewed the Pull Request.

8 files reviewed, 0 comments added.
```

Conclusion was `success`.

## Relay lessons

Do not stop at metadata-only forwarding. For PR steering, the relay needs two layers:

1. **Audit metadata** for every accepted/rejected delivery:
   - event
   - delivery id
   - repo
   - action
   - PR number
   - head SHA
   - sender
   - check name/app/status/conclusion
   - review state
   - comment kind
   - decision: forwarded / invalid_signature / event_not_allowed / repo_not_allowed / hermes_forward_failed

2. **Bounded content capture** only for Greptile/content-bearing events:
   - `check_run.output.title`
   - `check_run.output.summary`
   - `check_run.output.text`
   - `review.body`
   - `comment.body`
   - PR title

Never save the raw GitHub payload for this pilot. Store capture JSON project-local under the PR steering report area and include a content hash.

## Event-shape pitfalls

- If GitHub webhook UI includes `Pushes`, the relay must allow `push` and use `payload.after` as the pushed SHA.
- `check_run`/`check_suite` may carry PR number under `pull_requests[]`; extract from there.
- Some done-phase Greptile events may only prove completion, not include body text.
- Use GitHub Recent Deliveries → Redeliver to replay the exact completion event after improving the relay. Do not create another PR just to retest relay parsing.
- Watchers that trigger on every `"decision":"forwarded"` are too noisy. Watch for `greptile_hint=true`, review/comment events, and failure decisions instead.

## Secret-handling lesson

Do not print webhook secrets into chat, even under direct user pressure. Telegram deletion is not credential hygiene. Safer alternatives:

- copy the secret to local clipboard
- provide the local secret file path
- provide a terminal command that prints only the specific secret locally
- rotate the secret

## Merge-gating lesson

Greptile success is not full merge clearance when the repo is not locally available to Qayid.

If the repo is on Rawan's laptop, a steering report can say "Proceed from Greptile side" only. It must still gate merge on laptop-local checks: clean branch, exact HEAD SHA, build/lint/tests/runtime checks, and database/Supabase safety where relevant.
