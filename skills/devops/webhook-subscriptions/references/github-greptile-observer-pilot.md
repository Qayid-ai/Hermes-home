# GitHub + Greptile observer pilot notes

Use this as a concrete reference when wiring a sanitized GitHub webhook relay for Greptile PR steering.

## What the first real use proved

A delivery-only observer can prove this path without giving the agent repo write access:

```text
GitHub webhook
→ public tunnel
→ local sanitizer relay
→ Hermes dynamic webhook route
→ Telegram delivery-only notification
→ project-local audit log
```

The transport proof is not the steering proof. Metadata-only forwarding confirms that Greptile started/finished, but does not capture the review findings.

## Minimum relay behaviour

- Verify `X-Hub-Signature-256` before parsing semantics.
- Allowlist the exact repository.
- Allowlist only bounded events.
- Forward sanitized scalar fields only.
- Record a local NDJSON audit log outside chat.
- Keep Telegram delivery-only during observation.
- Do not post back to GitHub during the pilot.

## Event set used for observation

```text
ping
push
pull_request
pull_request_review
pull_request_review_comment
issue_comment
check_run
check_suite
status
```

If `Pushes` is selected in GitHub, the relay must also include `push` in its allowlist. Extract push head SHA from `payload.after`.

## Useful scalar fields to audit

```text
ts
event
delivery
repo
action
pr_number
head_sha
greptile_hint
review_state
comment_kind
check_name
check_app
status_context
check_status
conclusion
decision
http_status
hermes_status
```

`decision=forwarded` alone is too thin. It proves only transport.

## Correlation notes

- `pull_request` usually gives PR number and head SHA.
- `push` gives head SHA via `after`, but not PR number.
- `check_run` / `check_suite` may include PR number under `pull_requests[]`, but not always.
- When PR number is absent, correlate by head SHA.
- Greptile can show up as app slug/name/sender/check name containing `greptile`; keep this as a hint, not an authority.

## Done does not mean captured content

A Greptile-associated `check_run.completed`, `check_suite.completed`, or `pull_request` event can mean Greptile finished. It does not mean the relay captured:

- review body
- summary comment
- inline findings
- severity/confidence
- file/line comments

For a real steering report, fetch content through authenticated read-only GitHub/Greptile access, or add a bounded project-local capture path for content-bearing events and then redeliver the GitHub event.

## Redelivery workflow

After patching relay parsing:

1. Open GitHub webhook Recent Deliveries.
2. Find the relevant Greptile-looking delivery.
3. Redeliver it.
4. Inspect the local audit log.
5. Only then change event selection or make another PR.

This avoids test-commit churn.

## Watcher pitfall

Avoid watch patterns like:

```text
"decision":"forwarded"
```

They match every old forwarded entry and produce noisy backlog alerts.

Prefer:

```text
"greptile_hint":"true"
"event":"pull_request_review"
"event":"pull_request_review_comment"
"event":"issue_comment"
"decision":"invalid_signature"
"decision":"event_not_allowed"
"decision":"repo_not_allowed"
```
