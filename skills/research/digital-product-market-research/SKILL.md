---
name: digital-product-market-research
description: Use when researching, validating, or packaging revenue opportunities for digital products across mobile apps, creator storefronts, courses, downloads, templates, audits, and productized services. Combines live market/chart research with monetization design and checkout-ready offer assets.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [market-research, digital-products, monetization, mobile-apps, creator-store, productized-services]
    related_skills: [claude-design, humanizer]
---

# Digital Product Market Research

## Overview

Use this skill to turn market signals into a practical digital-product revenue test. The class includes mobile app opportunity scans, creator-store product lineups, paid/IAP/subscription pattern research, storefront offer copy, and low-ticket products that qualify buyers for higher-ticket implementation.

The default move is not to copy the current top chart or build a large course. The default move is to identify what people are already paying for, name the payment behavior, choose one buyer/pain, and package a small outcome-bound product or service that can be sold and fulfilled quickly.

Support references:

- `references/mobile-app-chart-sources.md` — live app chart sources and extraction patterns.
- `references/stan-store-revenue-research.md` — Stan Store capability, constraint, and offer research notes.

## When to Use

Use this when the user asks to:

- Research mobile app markets, top paid apps, top grossing/IAP apps, ASO signals, or app-store demand.
- Compare App Store, Google Play, Appfigures, Similarweb, Google Trends, or other public market surfaces.
- Research what can be sold on Stan Store, Gumroad, Payhip, Beacons, or link-in-bio commerce.
- Build a digital product lineup from AI/research/design/build skills.
- Design productized services, audits, validation reports, templates, downloads, lead magnets, checkout copy, or intake fields.
- Convert market research into a concrete first offer rather than a broad content plan.

Do not use this for public posting strategy unless the request is specifically for product assets or checkout copy.

## Core Principle

Separate three layers:

1. **Market signal** — rankings, trends, paid charts, grossing charts, customer-visible product categories, pricing, platform constraints.
2. **Payment behavior** — what the signal says people repeatedly pay for: specialist utility, status, workflow speed, entertainment, storage, coaching, business outcomes, implementation help.
3. **Offer design** — a narrow product, custom report, audit, booking, download, or template that can be fulfilled and tested.

Top charts are evidence, not strategy. Storefront features are constraints, not an excuse to build every product type.

## Market Research Workflow

1. Define scope explicitly:
   - Country/region, defaulting to US unless specified.
   - Platform: App Store, Google Play, Stan Store, Gumroad, Payhip, Beacons, Etsy-like marketplaces, or mixed.
   - Chart/product type: paid, grossing/IAP, free, subscriptions, downloads, courses, custom products, bookings.
   - Snapshot date/time.

2. Use official or primary sources first where available.
   - Apple Marketing Tools RSS is useful for top paid apps.
   - Platform docs are required before configuring storefront products.

3. Cross-check with public aggregators or rendered page text.
   - Appfigures and Similarweb are useful for app chart context.
   - Dynamic pages can require browser DOM text extraction.
   - Google Play may show reCAPTCHA; do not waste time fighting it when a public aggregator provides the same current chart.

4. Report signals compactly.
   - Use ranked lists rather than bloated tables on chat platforms.
   - Keep paid and grossing/IAP separate; they measure different monetization behavior.
   - Label Google Trends as trending search demand, not evergreen keyword volume.

5. Translate the signal into a product hypothesis.
   - State the buyer, pain, outcome, and why this market signal supports the idea.
   - Push back if the user is about to clone an incumbent without extracting the underlying payment behavior.

## Offer Design Workflow

1. Pick one buyer and one pain.
2. Choose the product type.
   - First-sale default: custom product/report or booking.
   - Later: template/download/course only after repeated manual delivery patterns.
3. Write the offer:
   - title, subtitle, who it is for, deliverables, price, turnaround, refund/delivery terms.
4. Define intake fields.
   - Ask only what is required to fulfill the product.
5. Create assets:
   - thumbnail, checkout/banner image, sample report/template, confirmation email, upsell CTA.
6. Test payment and delivery.
   - A store without Stripe/PayPal and a tested delivery path is not a revenue experiment.
7. Warm-launch before broad outreach.
8. Productize only from evidence.

## Mobile App Market Subsection

For app-market scans:

- Separate App Store paid, App Store grossing/IAP, Google Play paid, Google Play grossing/IAP, and trend demand.
- Use source names and snapshot time.
- Interpret categories: utilities, games, creative tools, learning, AI subscriptions, entertainment, storage, shopping, dating, and social attention have different payment mechanics.
- Do not merge upfront purchase data with recurring/IAP revenue data.

See `references/mobile-app-chart-sources.md` for exact URLs and DOM extraction snippets.

## Creator Store / Productized Service Subsection

For creator storefronts:

- Avoid leading with generic prompt packs, huge Canva/template bundles, PLR/MRR resale packs, broad “make money with AI” guides, or unspecific AI image prompt lists.
- Prefer vertical-specific kits, outcome-bound reports, audits, feasibility sprints, implementation checklists, workflow packs, and paid calls.
- For AsturLAB-style work, the strong default lineup is: free readiness checklist, low-ticket feasibility report, validation sprint, teardown, automation audit, scope blueprint, and build consultation.
- Custom products and bookings are often stronger first tests than passive downloads because they prove demand and create implementation upsell paths.

See `references/stan-store-revenue-research.md` for Stan-specific capability and constraint notes.

## Creator Community / Skool Audit Subsection

Use this when researching a creator's Skool/community as a potential management or growth client. Do not pitch generic “community management.” Frame the work around the creator's actual business engine: audience activation, implementation, retention, product research, and paid-offer readiness.

Workflow:

1. Research what makes a strong community first, using platform docs and current operator sources.
2. Inspect the public surface: positioning, promise, member count, online count, price, admin count, owner profile, external funnel, and directory snapshots.
3. If the community is private, stop at the access boundary and ask the user to authenticate in-browser. Never ask them to send credentials in chat.
4. After login, inspect internal surfaces: Start Here/onboarding, categories, pinned posts, feed quality, unanswered questions, classroom, calendar, leaderboard, members/admins, rules, wins, and recurring rituals.
5. Translate observations into a client-useful audit: quick wins, structural gaps, operating cadence, monetization path, and why the owner should care.
6. Keep the pitch specific. Strong angle: “your audience is growing; the community needs an operating system that turns attention into activation, member wins, and paid-product signal.”

See `references/skool-community-audit.md` for the checklist and pitch framing.

## Output Pattern

A good answer usually includes:

- Scope and timestamp.
- Source list.
- Compact ranked findings or product examples.
- Monetization pattern summary.
- Recommended first offer or experiment.
- Checkout-ready assets if requested: title, subtitle, description, price, deliverables, intake fields, confirmation email, upsell CTA.
- Explicit uncertainties and items to re-check before launch.

## Common Pitfalls

1. **Confusing charts with strategy.** Rankings show payment behavior; they do not define the product to copy.
2. **Mixing paid and grossing charts.** Upfront purchase and IAP/subscription mechanics differ.
3. **Over-trusting one aggregator.** Cross-check surprising results or label them as single-source.
4. **Treating trends as stable search volume.** Google Trends Trending Now is live demand, not ASO keyword volume.
5. **Building the course first.** Courses are slow and trust-heavy; start with a paid manual outcome unless the audience already exists.
6. **Selling AI as the value.** Buyers pay for business outcomes, not generic “AI”.
7. **Skipping checkout reality.** Payment, intake, delivery, and confirmation must be tested before claiming a product is launched.
8. **No upsell path.** Low-ticket products should qualify the buyer for implementation, scope, or consulting.

## Verification Checklist

- [ ] Scope, region, platform, chart/product type, and timestamp stated.
- [ ] Sources checked and named.
- [ ] Paid vs grossing/IAP/subscription signals kept separate.
- [ ] Platform constraints re-checked before configuration.
- [ ] Buyer and pain narrowed to one clear first experiment.
- [ ] Offer has deliverables, price, turnaround, intake, and terms.
- [ ] Payment and delivery path identified or tested.
- [ ] Output distinguishes evidence, interpretation, and recommendation.
