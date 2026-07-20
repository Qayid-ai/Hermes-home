---
name: ask_hormozi
description: Use when Rawan wants ACQ/Alex Hormozi-style business growth advice by querying his ChatGPT custom GPT through Rotunda, especially for offers, leads, ads, hooks, sales, pricing, retention, scaling, recruiting, fast cash, or constraint diagnosis.
version: 1.0.0
author: Qayid
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [business, growth, hormozi, acq, chatgpt, rotunda, advisor]
    related_skills: [hermes-agent]
---

# Ask Hormozi

## Overview

This skill routes business-growth questions to Rawan's Alex Hormozi / ACQ-style custom GPT in ChatGPT using Rotunda.

Use it as an external business advisor, not as a replacement for judgment. The GPT's role is to produce ACQ/Hormozi-style diagnosis and assets. Qayid's role is to operate the browser, retrieve the answer, and then apply pushback where needed.

Do not pretend the custom GPT was consulted unless Rotunda actually queried it and returned an answer.

## When to Use

Use this skill when Rawan asks to "ask Hormozi", "ask_hormozi", "use the Hormozi GPT", or brings a problem in any of these areas:

- Offer creation and Grand Slam Offer design
- Core promise, pricing, bonuses, guarantees, urgency, scarcity, risk reversal
- Lead generation, outreach, referrals, lead magnets, nurture, follow-up
- Advertising and creative strategy
- Hooks, messaging, positioning, naming, headlines, angles
- Sales process, setter/closer scripts, objection handling, no-show recovery
- Pricing, payment plans, recurring revenue, AOV, LTV, cash collection
- Retention, onboarding, customer success, churn, testimonials
- Scaling operations across product, marketing, sales, CS, IT, recruiting, HR, finance
- Team scorecards, hiring funnels, onboarding, training, accountability cadence
- Fast cash, reactivation, referral pushes, dead lead revival, pipeline recovery
- Constraint diagnosis from metrics

Don't use this skill for:

- Legal, tax, accounting, medical, or religious rulings
- Public posting or publishing without explicit human review
- Generic motivation when there is no business problem
- Requests that need confidential client details placed outside the active project context

## Default Operating Contract

Before querying the GPT, collect the smallest sufficient business context.

Best input fields:

- Business / product:
- Target customer:
- Current offer:
- Price / payment model:
- Lead source:
- Leads generated:
- Calls booked:
- Show rate:
- Close rate:
- Cash collected:
- Gross margin:
- Churn / retention:
- Fulfilment bottleneck:
- Current constraint:
- Time horizon:
- Assets needed:

If Rawan gives enough context, do not ask for all fields. Act with what is available and label missing assumptions.

## Rotunda Workflow

Rotunda is Firefox/Juggler-based. Do not use Hermes native `browser_*` CDP tools for this skill. Use the Rotunda CLI.

### 1. Verify Rotunda

```bash
uvx rotunda version
```

If missing or stale:

```bash
uvx rotunda fetch
uvx rotunda version
```

### 2. Create or reuse a Rotunda profile

Use a stable profile name so ChatGPT login persists:

```bash
uvx rotunda agent new-profile --name ask-hormozi
```

If the profile already exists, reuse it. Do not delete it just to start clean.

Create a context:

```bash
uvx rotunda agent new-context ask-hormozi
```

The command prints a page index. Store it as `<page>` for the session.

### 3. Navigate to the GPT

Preferred source for the URL:

1. Use this saved GPT URL by default:

```text
https://chatgpt.com/g/g-68a4af16ec44819181861f608aea1a30-acq-ai-lite-unofficial-inspired-by-alex-hormozi
```

2. If Rawan later provides a replacement URL, update this skill.
3. `ASK_HORMOZI_GPT_URL` may override the saved URL for testing.

Do not guess which public GPT is correct from search results.

Navigate with the saved URL directly unless intentionally testing an override:

```bash
uvx rotunda agent navigate <page> "https://chatgpt.com/g/g-68a4af16ec44819181861f608aea1a30-acq-ai-lite-unofficial-inspired-by-alex-hormozi"
uvx rotunda agent describe <page>
```

Only use `$ASK_HORMOZI_GPT_URL` when it is explicitly set for a replacement/test URL.

If ChatGPT requires login, stop and ask Rawan to complete login in the visible Rotunda window/profile. Do not bypass access controls. Do not ask for passwords or tokens.

If the page accepts a prompt but returns `We are sorry, but you do not have access to GPT interactions.`, treat that as an unauthenticated/unauthorised ChatGPT state. Ask Rawan to log in through the Rotunda profile, then create a fresh Rotunda context under the same `ask-hormozi` profile before retrying. The old agent page can go stale after browser login even when the visible window is logged in.

Fresh-context retry pattern:

```bash
uvx rotunda agent new-context ask-hormozi
uvx rotunda agent describe <new-page>
uvx rotunda agent navigate <new-page> "https://chatgpt.com/g/g-68a4af16ec44819181861f608aea1a30-acq-ai-lite-unofficial-inspired-by-alex-hormozi"
```
After Rawan logs in, create a fresh context under the same `ask-hormozi` profile and use the newest live GPT page from `new-context` output. Do not keep driving an old `page_*` handle if `describe` returns only the one-line page summary or `Target page, context or browser has been closed`.

A logged-in page usually shows a profile menu/profile image and no `Log in` CTA. If the page accepts a prompt but returns `We are sorry, but you do not have access to GPT interactions.`, treat that as an unauthenticated/unauthorised ChatGPT state. Stop and ask Rawan to log in through the Rotunda profile, then retry in the same profile.

### 4. Submit the prompt

Construct the prompt with this wrapper:

```text
You are being used as Rawan's ACQ/Hormozi-style business growth operator.

Task:
<Rawan's exact question/problem>

Known context:
<business metrics, offer, customer, price, funnel, retention, bottleneck, constraints>

Output requirements:
1. Identify the single most likely constraint.
2. Explain why that is the constraint using the numbers/context.
3. Give the highest-leverage move first.
4. Provide practical assets if relevant: offer stack, scripts, hooks, ads, sales flow, retention plan, hiring scorecard, or 30-day plan.
5. Include what to cut or ignore.
6. If numbers are missing, state the minimum numbers needed and still give the best provisional move.
7. Be blunt. No motivational filler.
```

Use `describe` to find the message box ref, then fill/type and submit:

```bash
uvx rotunda agent fill <page> <message-box-ref> "<prompt>"
uvx rotunda agent press <page> <message-box-ref> Enter
```

For long prompts, prefer a compact wrapper. Rotunda `fill` can time out on long multiline ChatGPT prompts even when the page is healthy. If that happens, retry with a shorter prompt that preserves the business facts and requested output shape; do not conclude ChatGPT failed from the fill timeout alone.

If Enter inserts a newline instead of sending, use the visible Send button ref from `describe`:

```bash
uvx rotunda agent click <page> <send-button-ref>
```

### 5. Wait and extract the answer

Poll until generation is done. Prefer an explicit completion signal such as `Response complete`; otherwise wait until the stop-generation button disappears, then extract:

```bash
uvx rotunda agent describe <page>
uvx rotunda agent extract <page>
```

If extraction cuts off mid-answer, run `describe` once more and extract again after completion.

Return the custom GPT's answer clearly labelled as:

```text
Hormozi GPT output:
...
```

Then add a short Qayid check below it:

```text
Qayid check:
- What I trust:
- What I don't trust:
- First action:
```

Keep the Qayid check short. Do not bury the GPT output under commentary.

## Output Rules

- Do not claim the answer is from Alex Hormozi personally. It is from Rawan's ChatGPT custom GPT.
- Do not cite or reproduce copyrighted book/manual text unless the GPT outputs it and the use is limited to short snippets necessary for the answer.
- Do not leak client-identifying details into prompts unless Rawan explicitly accepts that risk and the prompt stays inside the legitimate ChatGPT session.
- If client details are not needed, abstract them: industry, role, price point, funnel metrics.
- If the GPT answer is generic, challenge it. Ask a sharper follow-up with numbers or constraints before returning a weak answer.
- If Rotunda fails, report the exact failure and fall back to Qayid's own analysis only if Rawan wants a non-GPT answer.

## Fast Prompt Template

```text
Ask the ACQ/Hormozi business operator GPT this:

Business:
Customer:
Offer:
Price:
Lead source:
Current numbers:
Problem:
Time horizon:
Asset needed:

Diagnose the constraint, give the highest-leverage move, and produce the practical asset. No fluff.
```

For session-tested Rotunda/ChatGPT details, stale-page recovery, login cues, and prompt submission pitfalls, see `references/rotunda-chatgpt-session-notes.md`.

## Common Pitfalls

1. **Guessing the GPT URL.** There are many Hormozi-like GPTs. Use the exact one Rawan has access to.
2. **Using native browser tools.** Rotunda is not CDP. Use `uvx rotunda agent ...`.
3. **Assuming a visible login refreshes the agent page.** After Rawan logs into the visible Rotunda window, create a fresh `ask-hormozi` context and use the new live page. Old page refs may be closed/stale.
4. **Long prompt fill timeouts.** If `rotunda agent fill` times out on a long prompt, retry with a shorter prompt or fill then submit via the visible send button ref from `describe`. Verify with `extract`; do not assume failure or success from the fill exit alone.
5. **Stopping at a generic GPT answer.** If the output is broad advice, run one sharper follow-up before returning it.
4. **Forgetting Qayid's role.** The GPT gives ACQ-style advice. Qayid still challenges bad assumptions and translates the output into action.
5. **Over-collecting context.** If Rawan gives enough to proceed, proceed. Missing numbers can be listed as assumptions.
6. **Credential mishandling.** Never ask for ChatGPT credentials. Rawan logs in through Rotunda manually if needed.

## Verification Checklist

- [ ] `ask_hormozi` skill loaded before use
- [ ] Rotunda CLI used, not native CDP browser tools
- [ ] Exact GPT URL used or requested
- [ ] ChatGPT access is legitimate and authenticated by Rawan
- [ ] Prompt includes business context and output requirements
- [ ] GPT output extracted after generation completes
- [ ] Weak/generic answer challenged with a follow-up
- [ ] Final response separates `Hormozi GPT output` from `Qayid check`
