# Skool Community Audit Reference

Use this reference when auditing a creator's Skool community for a potential management, operations, or productized-service client.

## Core positioning

Do not pitch generic “community management.” Most creators hear that as posting, moderation, or admin work.

Better frame:

> Turn the community into an operating system that converts audience attention into activation, implementation, member wins, product signal, and paid-offer readiness.

For fast-growing free Skool groups, the likely problem is not acquisition. It is unstructured growth: members join, browse, fail to act, ask scattered questions, and churn mentally without the owner noticing.

## Research before audit

Check current platform docs and operator material before making claims. Useful Skool concepts:

- Community: categories, rules, moderation.
- Classroom: courses and unlock mechanisms.
- Calendar: live events, Skool Call, Go Live.
- Leaderboards: points, levels, gamification.
- Points: members gain points when others like their posts, comments, and replies. This rewards contribution, but only if the community culture rewards useful contribution rather than shallow engagement.

Current operator consensus worth testing against the page:

- Strong communities have a clear transformation promise.
- The Start Here/pinned onboarding flow is critical.
- Simple categories usually beat complex taxonomies, especially under early scale.
- Predictable weekly rhythms beat random posting bursts.
- Community value comes from member implementation and member-to-member help, not admin broadcasting alone.
- Recognition, wins, critique, and rituals create retention.
- Free communities need a visible but non-pushy path toward paid implementation, workshops, templates, services, or higher-touch offers.

## Public-surface audit checklist

Collect:

- Name and niche.
- Public promise/description.
- Member count.
- Online count and online percentage.
- Price/free/paid model.
- Admin/mod count.
- Owner profile and authority markers.
- External funnel: YouTube, Instagram, TikTok, LinkedIn, newsletter, products, sponsors.
- Directory snapshots such as Tools4Skool when available: created date, posts, courses, modules, historical member counts.
- Public contradictions: private vs public labels, stale directory data, changing member counts.

Interpretation questions:

- Is growth fast enough that operations are likely lagging behind audience inflow?
- Does the promise name a clear transformation or only a broad topic?
- Does the free group have an obvious business purpose?
- Is the owner likely the bottleneck?
- What does the external content already solve, and what should the community solve instead?

## Private/internal audit checklist

After the user authenticates in-browser, inspect:

### Onboarding

- Is there a pinned Start Here post?
- Does it include the community promise, how the group works, and first 3 actions?
- Are new members told where to introduce themselves, where to get help, and what to do first?
- Are intro posts replied to?
- Are join questions, welcome DMs, or onboarding prompts visible?

### Categories

- Are categories simple and action-oriented?
- Is there a clear place for questions/help?
- Is there a clear place for wins/results?
- Is there a clear place for feedback/critique?
- Are tool posts separated from implementation/results?
- Are there dead or redundant categories?

### Feed quality

- Recent post frequency.
- Comment depth.
- Number of unanswered questions.
- Whether owner/admin replies are timely.
- Whether members help each other.
- Whether posts are implementation-focused or mostly passive sharing.
- Whether good posts are pinned/featured/recycled.

### Classroom

Check whether the classroom maps to the creator's actual audience journey.

For AI video communities, likely paths include:

- AI video foundations.
- Ad creative workflow.
- Short film workflow.
- Character consistency.
- Prompting / shot direction.
- Dubbing and localization.
- Tool stack comparisons.
- Client delivery workflow.
- Troubleshooting library.

Empty or unstructured classrooms are a strong opportunity if the audience is already growing.

### Calendar and rituals

Look for recurring events:

- Weekly workflow teardown.
- Build-along session.
- Critique call.
- Tool-of-the-week lab.
- Member work showcase.
- Challenge deadline/review.
- “Fix my failed generation” clinic.

No rhythm means members have no reason to return on schedule.

### Leaderboard/gamification

Check whether levels unlock anything useful.

Good uses:

- Advanced workflow unlocks.
- Critique access.
- Featured member slots.
- Template/resource unlocks.
- Contributor recognition.

Bad signs:

- Levels exist but mean nothing.
- Shallow posts farm likes.
- No link between points and useful progress.

### Monetization readiness

Look for repeated demand signals:

- Questions asked again and again.
- Tools members are stuck on.
- Common workflow failures.
- Requests for templates, prompts, assets, feedback, or live help.
- Members trying to use the skill commercially.

Map these into potential offers:

- Paid workflow vault.
- Monthly critique room.
- Bootcamp/challenge.
- Templates/assets membership.
- Done-with-you setup.
- Consulting or implementation service.

## Authenticated inspection pattern

When the user has logged in through Rotunda/browser, prefer UI inspection first. If the rendered UI crashes, wedges, or hides data behind infinite scroll, use authenticated HTTP against the same session rather than giving up.

Safe pattern:

1. Keep access-boundary discipline: the user logs in themselves; never ask for credentials in chat.
2. Locate the active browser profile/session store only after the user confirms they are logged in.
3. Copy the browser cookie database to a temporary working path before reading it. Do not modify the live profile.
4. Build a `requests.Session()` from the Skool cookies and fetch relevant routes directly:
   - `/about`
   - `/community`
   - `/classroom`
   - `/calendar`
   - `/leaderboards`
   - `/members`
5. Parse the `__NEXT_DATA__` JSON from server-rendered HTML where present.
6. Redact tokens/cookies from all user-facing output.
7. Save only derived observations unless the user explicitly asks for raw exports.

Useful ratios and fields:

- Online rate = online members / total members.
- Posts per 100 members = total posts / total members * 100.
- Admin-to-member ratio = total members / admin count.
- Category concentration = posts per category/label.
- Classroom maturity = course/module count and whether it maps to the audience journey.
- Calendar maturity = recurring event count and cadence.
- Leaderboard maturity = level distribution and whether levels unlock meaningful value.
- Feed health = unanswered questions, median comments, member-to-member replies, owner response pattern, and whether top engagement comes from assets, wins, critique, or announcements.

Interpret the numbers commercially. A low post-to-member ratio, empty classroom, unused calendar, and single-admin bottleneck in a fast-growing group are not just “engagement issues”; they are the wedge for an operating-system offer: onboarding, content structure, weekly rituals, feedback loops, and product-signal reporting.

## Output structure

A useful audit for outreach should include:

1. One-sentence thesis.
2. Evidence from public/internal observations.
3. Highest-leverage opportunities.
4. Quick wins in 7 days.
5. 30-day operating cadence.
6. Monetization/product signal opportunities.
7. Suggested outreach message.

Avoid bloated generic advice. The owner should feel you understood their specific community and funnel.

## Outreach framing template

> I looked through [community name]. The growth signal is strong, but the bigger opportunity is converting that attention into member activation and visible wins.
>
> Right now I’d focus less on “more posts” and more on the operating system: onboarding, categories, weekly rituals, classroom structure, unanswered-question capture, and turning repeated member problems into content/product signals.
>
> I can send you a short teardown with specific improvements. Not a generic engagement audit — a practical plan for turning the group into an implementation engine around your content.

## Pitfalls

- Do not overstate private-community findings from public data.
- Do not ask the user to send passwords or credentials in chat.
- Do not confuse member count with community health.
- Do not pitch posting volume as the main value.
- Do not make the Skool mirror the creator's YouTube. The community should solve implementation, feedback, accountability, and peer support.
- Do not recommend monetization before the activation path is clear.
