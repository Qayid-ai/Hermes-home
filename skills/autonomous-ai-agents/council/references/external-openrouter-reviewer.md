# External OpenRouter reviewer for degraded Council runs

Use this when a full Council run is degraded by a missing voice, but the user explicitly wants an extra independent check rather than another full rerun.

## What this is

A one-off external reviewer reads the finished `forum.md` and `quality_report.md` from a Council run, then writes an independent review to `outputs/<model>-oneoff.md`.

It is **not** a Council voice replacement.

Do not present it as Antigravity, Codex, Opus, or a full Council synthesis. Label it as an external review.

## When to use

- A Council run has a complete forum from at least one or two core voices.
- Another voice is unavailable due quota or provider failure.
- The user asks to “run Gemini”, “get another model’s verdict”, or “test with OpenRouter”.
- Rerunning the full Council would waste quota or repeat a known provider failure.

## Known working OpenRouter model slug

- `google/gemini-3.5-flash`

Verify current model IDs with OpenRouter before hardcoding a new one. OpenRouter model names move.

## Prompt shape

The external reviewer prompt should include:

1. The original question.
2. The relevant operating constraints.
3. The quality report.
4. The full `forum.md`.
5. A clear role boundary: “You are NOT Codex, NOT Opus, NOT Antigravity, and NOT the previous synthesiser.”
6. Required output:
   - verdict
   - confidence
   - key reason
   - strongest objection
   - exact next test
   - branch conditions if the answer depends on an unknown fact

## Output contract

Write:

- `outputs/<model>-oneoff.md`
- `outputs/<model>-oneoff.meta.json`

Metadata should include:

- model slug
- HTTP/API status
- provider response ID if available
- token usage
- cost if available
- output path

Never print or save API keys. If an error body accidentally echoes secrets, redact before surfacing it.

## Reporting rule

When returning the result to Rawan:

- State that it is an external one-off review.
- State the model slug.
- State cost if known.
- Give the verdict and delta versus the Council synthesis.
- Do not bury degraded-Council caveats.

## Vault-save routing

If the underlying Council synthesis has already been saved to operations research, save the one-off review beside it and update the index as **External review**, not **Primary**.

Example destination:

`asturlab/operations/operations_research/YYYY-MM-DD-NN-<model>-<topic>-review.md`

The review can support or challenge a primary Council answer, but it should not silently replace it.