# Skool + Rotunda course map and resources extraction

Use this reference when extracting a legitimately accessible Skool classroom through a Rotunda-authenticated session.

## Durable workflow

1. Verify authenticated classroom access.

Use Rotunda page commands to confirm the page title and DOM show member navigation/classroom content, not the public about page. Public-page signs include `LOG IN`, `JOIN`, and only marketing/about content.

2. If course cards are hard to click, use the exposed route data.

Skool course cards can render with `aria-disabled=true` or block automation clicks even when the user has access. Extract the page HTML and parse `__NEXT_DATA__` instead of fighting the click target.

Relevant fields seen in Skool page data:

- `props.pageProps.allCourses[]`
- `props.pageProps.course.course`
- `props.pageProps.course.children[]`
- course `metadata.title`
- course `name` — often the route slug used in `/classroom/<course-slug>`
- module `id` — used as `?md=<module-id>`
- module `metadata.title`

3. Build the course map from data, not visible DOM only.

For each set/phase and module, preserve:

- section order;
- lesson order;
- lesson title;
- URL `/classroom/<course-slug>?md=<module-id>`;
- module id;
- pending fields for content type and captions/transcripts.

4. Do not dump raw Skool rich-text JSON into the course map.

Skool lesson descriptions often contain `[v2]` JSON/rich text. The course map should stay clean. Put raw or rendered lesson extraction in lesson files, not in the map.

5. Treat resources as their own extraction surface.

Create a resources index separate from the course map. For each lesson, capture attached Google Docs, Sheets, Slides, Drive files, and Drive folders.

Recommended files:

- `source/resources-index.md` — human-readable per-lesson index.
- `source/attached-resources/manifest.md` — export/download status.
- `source/attached-resources/manifest.json` — machine-readable status.
- `source/attached-resources/` — exported docs/sheets when access allows.

6. Do both resource passes.

First pass: parse resource links from the course tree in `__NEXT_DATA__`.

Second pass: visit every lesson URL and extract/parse that lesson page, because Skool may expose lesson-specific resources only after the lesson is selected.

7. Classify resource links.

Common types:

- Google Sheet / worksheet: `docs.google.com/spreadsheets`
- Google Doc / worksheet: `docs.google.com/document`
- Google Slides / deck: `docs.google.com/presentation`
- Google Drive file: `drive.google.com/file`
- Google Drive folder: `drive.google.com/drive/folders`

8. Export only what is legitimately accessible.

Without Hermes Google OAuth, try public Google-native exports only:

- Docs: `/document/d/<id>/export?format=txt`
- Sheets: `/spreadsheets/d/<id>/export?format=csv`
- Slides: `/presentation/d/<id>/export/pdf`

Do not save HTML sign-in or access-denied pages as extracted resources. If a resource requires Google auth, mark it pending.

Drive files and Drive folders usually need either Google API auth or manual browser access. Index them lesson-by-lesson instead of pretending they were extracted.

9. Verify before reporting.

Before final output:

- scan generated files for credential/payment leakage;
- count visited lessons, lessons with resource links, unique resource URLs, exported files, pending files, and pending folders;
- spot-check the map starts and ends at the expected lesson counts;
- report limitations plainly.

## Pitfalls

- Do not treat Skool card click failure as lack of access. Check page data first.
- Do not flatten worksheets into lesson summaries. The worksheets are part of the course product.
- Do not store public/about-page facts as if classroom access was verified.
- Do not use Google Drive export attempts to bypass permissions. Public-link export only, otherwise pending.
- Do not claim Drive files/folders are extracted when only indexed.
