# Greptile webhook observer + laptop-local repo handoff — 2026-07-02

## Context

During the estate-agents first real PR probe, the app repo lived on Rawan's laptop, not the Mac mini running Qayid. The GitHub repo was private, so unauthenticated GitHub API reads from the Mac mini returned `404`. Greptile was already added to the repo and was reviewing PR #1.

The correct posture was to treat the Mac mini as the **control plane**, not the app execution environment.

## Durable workflow lesson

When the app repo is not local to Qayid:

1. Do not assume Qayid can inspect the working tree, run Graphify, or read PR files locally.
2. Bind the GitHub repo and PR head SHA project-locally.
3. Use GitHub/Greptile events, user-supplied review output, or a webhook observer for PR signals.
4. Require Rawan to provide/sync Graphify artifacts from the laptop if Graphify runs there.
5. Keep the project-local PR probe as metadata-only until Greptile output and Graphify artifacts arrive.

## Webhook observer pattern

Use a temporary GitHub → sanitizer relay → Hermes delivery-only route for event-shape discovery.

Properties:

- GitHub HMAC required.
- Repo allowlist required.
- Event allowlist required.
- Sanitized metadata only.
- Delivery-only Telegram notification.
- No LLM.
- No GitHub comments or repo writes.
- No cron.

The relay must extract PR number/head SHA from multiple event shapes, because Greptile may appear through checks, reviews, review comments, issue comments, or statuses.

Extraction cases to support:

- `pull_request.number` and `pull_request.head.sha`
- PR issue comments via `issue.number`
- `check_run.pull_requests[]`
- `check_suite.pull_requests[]`
- `check_run.head_sha`
- `check_suite.head_sha`
- review/comment `pull_request_url`
- status `sha`

## Verification pattern

Before asking Rawan to add the GitHub webhook:

1. Check local Hermes webhook health.
2. Check relay `/health`.
3. Check public tunnel `/health`.
4. Send a signed synthetic event through the public tunnel and verify Hermes delivery.
5. Send a bad-signature event and verify `401 invalid_signature`.
6. Save project-local status with endpoint, event list, and verification result — never secrets.

## User action pattern

In GitHub repo settings, add webhook:

- Payload URL: the public relay `/github` endpoint.
- Content type: `application/json`.
- Secret: paste from local clipboard or secure channel; never print in chat.
- Events: select only needed events.

Useful selected events for Greptile observation:

- Pull requests
- Pull request reviews
- Pull request review comments
- Issue comments
- Check runs
- Check suites
- Statuses

Do not select "send me everything" for the first probe.
