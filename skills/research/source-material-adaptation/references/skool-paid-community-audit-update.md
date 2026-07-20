# Skool paid-community audit update pattern

Use this when a Skool community owner has changed the offer, added a paid option, or shifted from free/community-only toward monetisation, and Rawan needs client-facing docs updated.

## Pattern

1. Re-check the live Skool public/about page first.

Useful public `__NEXT_DATA__` fields often include:

- `currentGroup.metadata.totalMembers`
- `currentGroup.metadata.totalPosts`
- `currentGroup.metadata.totalOnlineMembers`
- `currentGroup.metadata.numCourses`
- `currentGroup.metadata.numModules`
- `currentGroup.metadata.freeBenefits`
- `currentGroup.metadata.recurringInterval`
- `currentGroup.metadata.tabs`
- `currentGroup.updatedAt`

2. Compare against the previous audit baseline.

The useful sales evidence is usually the delta:

- member growth;
- post growth;
- whether classroom moved from empty to active;
- whether calendar/classroom/map tabs are visible;
- whether the community now exposes monthly recurrence;
- whether free benefits have become clearer.

3. Do not overclaim paid-tier details from public data.

Skool public HTML may expose `recurringInterval` and `freeBenefits` while hiding exact paid-tier price and paid benefits. State the limitation plainly and mark authenticated verification pending.

4. Update the commercial framing.

If the community has introduced paid access, the pitch should usually move from “classroom buildout” or “30-day sprint” to:

- monthly community growth and engagement retainer;
- recurring Skool operations support;
- monthly member activation cycle;
- paid/free community conversion support;
- community momentum system.

The classroom is secondary. It supports retention and conversion. It is not the main offer.

## Client-facing angle

Recommended line:

> You’ve already got attention and a growing Skool. We help turn that into month-by-month community momentum: member activation, weekly engagement rituals, content-to-discussion loops, paid/free pathway clarity, and classroom improvements only where they support retention.

Avoid:

- “30-day sprint” when Rawan wants recurring monthly payment;
- “classroom buildout” when community engagement is the real value;
- “community management” when it sounds like low-value moderation/admin.

## Verification checklist

Before finalising docs, verify:

- file exists and opens or can be parsed;
- evidence pack contains only sanitized selected fields, not raw Skool account/payment/session data;
- paid price/benefits are labelled unknown unless authenticated data clearly exposes them;
- the offer language says monthly/recurring, not one-off sprint.
