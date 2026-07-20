---
name: app-market-research
description: Research mobile app market rankings, paid/IAP charts, ASO signals, and trend demand across App Store, Google Play, Google Trends, Appfigures, Similarweb, and other chart aggregators. Use for app/playground ideation, top paid/grossing app snapshots, mobile monetization pattern scans, and app-store opportunity research.
---

# App Market Research

Use this when Rawan asks for current mobile app market data, especially:

- top paid apps
- top grossing / IAP / subscription apps
- App Store vs Google Play comparisons
- Google Trends / keyword demand snapshots
- ASO or competitor ranking research
- playground app ideation based on market signals

## Default stance

Do not treat top charts as product strategy by themselves.

Top paid charts usually reveal willingness to pay for specialist tools, games, utilities, creative workflows, and learning products. Top grossing charts usually reveal repeat-payment loops: AI subscriptions, video/entertainment subscriptions, storage, shopping, dating, games, and social attention.

Give Rawan the data first. Then name the market pattern. Push back if he is about to copy incumbents instead of extracting the payment behavior.

## Workflow

1. Define the market scope explicitly.
   - Country: default to US unless the user asks otherwise.
   - Store: App Store, Google Play, or both.
   - Chart type: paid, grossing, free, category-specific.
   - Timestamp the snapshot.

2. Use official sources first where they exist.
   - Apple has official Marketing Tools RSS feeds for top paid apps.
   - Google Play direct pages may trigger reCAPTCHA; do not waste time fighting it if a public chart aggregator gives the same current chart.

3. Cross-check with chart aggregators.
   - Appfigures is useful for free/paid/grossing tabs and often exposes visible rankings in page text.
   - Similarweb is useful for Android paid rankings and category/publisher context.
   - Sensor Tower may require access; use public excerpts only unless credentials are explicitly available.

4. For dynamic pages, use browser DOM extraction.
   - Navigate with the browser.
   - Use `document.body.innerText` from browser console to extract visible ranking sections.
   - Slice around labels like `Paid`, `Grossing`, `Free`, or known app names.

5. For Google Trends, prefer the live Trending Now page when API/RSS endpoints are unavailable.
   - Capture region, time window, trend term, approximate search volume, and whether it is active.
   - Label it as trending search demand, not evergreen keyword volume.

6. Return results in compact ranked lists.
   - Avoid tables on Telegram.
   - Include source names and snapshot time.
   - Separate `paid` from `grossing/IAP`; they measure different behaviors.

## Pitfalls

- Do not merge paid apps with grossing apps. Upfront purchase and IAP/subscription monetization are different signals.
- Do not call Google Trends `top keywords` unless it is actually keyword volume. The Trending Now page is trend demand, not stable SEO/ASO search volume.
- Do not over-trust a single aggregator when the result is surprising. Cross-check with at least one other source or the store surface.
- Do not record transient access failures as durable facts. If Google Play blocks scraping, the durable lesson is the fallback path through aggregators and browser-visible text.
- Do not make the output long to look serious. Rawan wants the usable signal.

## Source notes

See `references/mobile-app-chart-sources.md` for known useful chart URLs and extraction patterns.