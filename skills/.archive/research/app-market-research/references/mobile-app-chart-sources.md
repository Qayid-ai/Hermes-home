# Mobile app chart sources and extraction patterns

Session-derived notes from a US app-market snapshot on 2026-05-29.

## Apple App Store

Official Apple Marketing Tools RSS is the cleanest source for top paid apps.

Example:

```text
https://rss.applemarketingtools.com/api/v2/us/apps/top-paid/5/apps.json
```

Observed payload fields:

- `feed.updated`
- `feed.country`
- `feed.results[].name`
- `feed.results[].artistName`
- `feed.results[].url`

The attempted `top-grossing` Apple RSS endpoint returned 404 in this session, so use Appfigures or another chart surface for grossing/IAP unless an official current endpoint is found.

## Google Play

Direct Google Play chart URLs can show reCAPTCHA in extraction tools:

```text
https://play.google.com/store/apps/collection/topselling_paid?hl=en_US&gl=US
https://play.google.com/store/apps/collection/topgrossing?hl=en_US&gl=US
```

Do not fight the CAPTCHA. Use public chart aggregators or browser-visible pages.

## Appfigures

Useful public chart pages:

```text
https://app.appfigures.com/top-apps/ios-app-store/united-states/iphone/top-overall
https://app.appfigures.com/top-apps/google-play/united-states/top-overall
```

The page includes Free, Paid, and Grossing sections in visible text. Browser console extraction works well:

```js
const lines = document.body.innerText.split('\n').map(s => s.trim()).filter(Boolean);
lines.slice(lines.findIndex(s => s === 'Grossing'), lines.findIndex(s => s === 'Grossing') + 40);
```

For paid sections:

```js
const lines = document.body.innerText.split('\n').map(s => s.trim()).filter(Boolean);
lines.slice(lines.findIndex(s => s === 'Paid'), lines.findIndex(s => s === 'Paid') + 25);
```

## Similarweb

Useful for Android paid chart context:

```text
https://www.similarweb.com/top-apps/google/top-paid/
```

In the 2026-05-29 session it exposed a US Google Play paid apps ranking with usage rank, app, publisher, category, and store rank.

## Google Trends

Live Trending Now page:

```text
https://trends.google.com/trending?geo=US
```

Use browser snapshot or DOM text extraction. Capture:

- query
- approximate search volume, e.g. `50K+`
- growth percentage if visible
- start time
- active/inactive status
- related terms if useful

Label this as **trending demand**, not evergreen keyword volume.

## Reporting pattern

For Telegram, avoid pipe tables. Use ranked lists:

- App Store — paid
- App Store — grossing/IAP
- Google Play — paid
- Google Play — grossing/IAP
- Google Trends — trending searches

Then add a short synthesis of payment behavior, not a long essay.