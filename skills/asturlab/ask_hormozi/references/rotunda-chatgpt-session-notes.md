# Rotunda ChatGPT custom GPT session notes

Session-derived notes for driving Rawan's ACQ/Hormozi ChatGPT custom GPT through Rotunda.

## Exact GPT URL

```text
https://chatgpt.com/g/g-68a4af16ec44819181861f608aea1a30-acq-ai-lite-unofficial-inspired-by-alex-hormozi
```

## Proven flow

1. Create/reuse profile:

```bash
uvx rotunda agent new-profile --name ask-hormozi
uvx rotunda agent new-context ask-hormozi
```

2. Use the newest live GPT page from `new-context` output. If multiple pages are listed, prefer the newest page whose URL is the GPT URL and whose `describe` output includes the composer.

3. Navigate with a default URL plus optional env override:

```bash
GPT_URL="${ASK_HORMOZI_GPT_URL:-https://chatgpt.com/g/g-68a4af16ec44819181861f608aea1a30-acq-ai-lite-unofficial-inspired-by-alex-hormozi}"
uvx rotunda agent navigate <page> "$GPT_URL"
uvx rotunda agent describe <page>
```

4. Login state check:

- Logged out may show `Log in`, `Sign up for free`, and can return `We are sorry, but you do not have access to GPT interactions.` after prompt submit.
- Logged in showed profile/menu elements and GPT sidebar entries.
- If Rawan logs in through the visible Rotunda app, create a fresh context before retrying. Old page handles can go stale.

5. Submit prompt:

```bash
uvx rotunda agent fill <page> <textbox-ref> "<compact prompt>"
uvx rotunda agent press <page> <textbox-ref> Enter
```

If `fill` times out on a long multiline prompt, retry with a shorter prompt before declaring failure. A compact prompt successfully submitted in the test.

6. Completion/extract:

Poll `describe` until `Response complete` appears or the stop-generation button disappears. If the first `extract` is mid-answer, describe/extract again.

## Known ChatGPT page cues from the successful test

- Textbox ref label: `Chat with ChatGPT`.
- Successful logged-in session title: `ChatGPT - ACQ AI Lite (Unofficial) inspired by Alex Hormozi`.
- Successful response included heading: `ACQ AI Lite (Unofficial) inspired by Alex Hormozi said:`.

## Pitfall

Do not use the native Hermes browser tools for this skill. Rotunda is the requested browser path and is Juggler-based, not CDP.