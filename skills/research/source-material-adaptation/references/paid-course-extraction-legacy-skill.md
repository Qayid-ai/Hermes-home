---
name: paid-course-extraction
description: Extract and organise legitimately accessible paid course/classroom material, especially Skool classrooms, into a local working repo before strategy or vault promotion.
version: 1.0.0
created_by: agent
---

# Paid course extraction

Use this when Rawan wants to extract, map, summarise, or operationalise a paid course, Skool classroom, membership, or private training material he legitimately has access to.

The goal is to preserve the course's operating system in order before applying it to AsturLAB.

Each course is different. Treat the coach's sequencing, repetition, examples, worksheets, comments, and pacing as intentional until proven otherwise. Do not flatten the course into generic business advice.

Do not jump to strategy before the classroom map exists.

## Core rules

1. Legitimate access only.

Use only material exposed through Rawan's account/session. Do not bypass access controls, paywalls, DRM, hidden APIs, or private permissions.

2. No redistribution.

The extraction is for private analysis and operational application. Do not produce shareable replicas of paid content.

3. Preserve order.

Lesson order matters. Extract the classroom/module/lesson sequence before synthesising.

4. Preserve instructional design.

For every module and lesson, capture why it appears where it appears. Track prerequisites, repeated concepts, emotional framing, exercises, examples, proof points, and transitions. The coach's structure is data, not packaging.

5. Separate raw extraction from application.

Keep course notes, cleaned frameworks, and AsturLAB strategy in separate files/folders.

6. No vault writes until ready.

If Rawan says not to commit to the vault yet, create a working repo outside the vault and keep all intermediate material there. Do not save the behaviour as memory unless he asks.

## Recommended workspace

For AsturLAB business strategy extraction, use a local repo such as:

`~/Documents/War Room`

Suggested structure:

- `README.md` — scope, ground rules, and folder map.
- `source/course-map.md` — exact module/lesson order and URLs.
- `extraction/lesson-template.md` — reusable lesson extraction template.
- `extraction/lessons/` — one file per lesson in order.
- `strategy/asturlab-application.md` — only after enough extraction is complete.
- `implementation/` — SOPs, templates, rituals, planning changes, rollout plan.

Do not commit unless Rawan asks. Initialising a repo is fine if requested, but leave files uncommitted by default.

## Extraction sequence

Reference workflow for Skool + Rotunda course mapping and attached-resource extraction: `references/skool-rotunda-course-map-and-resources.md`.

For Skool communities that have introduced a paid option or changed from free/community-only toward monetisation, use `references/skool-paid-community-audit-update.md` before updating client-facing docs. Re-check live public page data, compare against the previous audit baseline, avoid overclaiming hidden paid-tier details, and shift the offer toward recurring community engagement/retention unless Rawan explicitly wants a one-off sprint.

For large targeted Skool subsets, use the staged/checkpointed workflow in `references/skool-targeted-large-course-checkpointing.md`: exact target list first, sanitized course map second, rendered lesson-page pass with per-lesson checkpointing third, captions/resources after that.

When course resources include private Google Drive, Docs, or Sheets links, use the scoped OAuth workflow in `references/google-workspace-scoped-oauth-for-course-resources.md` before marking those resources complete. For large mixed Drive exports with folders and binary files, use the resumable exporter pattern in `references/google-drive-course-resource-exporter.md`.

1. Create/verify workspace outside the vault if requested.

For named course/community extractions, default to a separate repo/workspace named after the course or community, such as `~/Documents/<slug>/`. Do not bury it under a broader workspace like `War Room` unless Rawan explicitly asks for that. If Rawan corrects the workspace boundary, move it immediately, verify the old path is gone, and keep files uncommitted unless asked.

2. Get access context.

Ask for the Skool/classroom URL or which browser/session already has access. Use browser interaction where needed. Prefer Rotunda if available and suitable because Rawan prefers it for web interaction.

For credentialed course access, never ask Rawan to paste credentials into chat. Open the target page, then hand off login cleanly:

- If the Hermes native browser opens a visible local window, tell Rawan to log in there manually and report when done.
- If the native browser session is not directly shareable from Telegram, say so plainly instead of pretending the user can access it.
- If login/session continuity matters, prefer a Rotunda profile/context that Rawan can authenticate manually, then operate only inside that authenticated context.
- After login, refresh and verify access before extracting. If still on a public/about page, capture only public facts and mark classroom extraction as pending.

2.5. For Skool via Rotunda, verify and route from exposed page data.

Skool course cards may show as `aria-disabled`/sortable in automation even when the user has access. Do not conclude the course is locked from click failure alone.

Use Rotunda's legitimate page extraction path:

- `uvx rotunda agent pages <profile>` to identify the page.
- `uvx rotunda agent reload <page>` and `uvx rotunda agent describe <page>` to verify login state.
- `uvx rotunda agent extract --format html --output <tmp.html> <page>` to capture rendered HTML.
- Parse `#__NEXT_DATA__` for `props.pageProps.allCourses` / `props.pageProps.course`.
- Prefer course `name`/slug for route construction: `https://www.skool.com/<group>/classroom/<course-name>`.
- Then open individual modules with `?md=<module-id>`.

Sanitise aggressively when using `__NEXT_DATA__`. It can include account email, payment metadata, all joined groups, public keys, and other irrelevant private state. The durable map should contain only course title, course slug/id, module title/order/id/URL, and extraction status. Do not paste raw JSON into notes.

See `references/skool-rotunda-course-routing.md` for the route-discovery pattern.

3. Map the classroom first.

Capture:

- community/course name;
- module names;
- lesson names;
- exact order;
- URLs;
- content type: video, text, download, quiz, template, post;
- whether captions/transcripts/downloads are available.

For Skool classrooms, if course cards are visible but automation clicks fail or the card appears disabled, do not assume access is missing. Extract the authenticated page HTML and parse `__NEXT_DATA__` for `allCourses`, course `name` route slugs, set/module trees, and module IDs. Build lesson URLs as `/classroom/<course-slug>?md=<module-id>` when exposed by the logged-in page data.

Keep the course map clean. Skool rich-text descriptions can contain raw `[v2]` JSON; do not dump that JSON into `source/course-map.md`. Lesson text, resources, and raw extraction belong in lesson files or resource indexes.

4. Extract lesson-by-lesson.

For each lesson, capture:

- metadata;
- core teaching;
- frameworks;
- step-by-step process;
- checklists;
- attached documents, worksheets, sheets, slides, PDFs, Drive folders, and templates;
- templates/tools mentioned;
- warnings/failure modes;
- business application notes;
- items to revisit;

Treat attached documents, worksheets, slide decks, Drive files, and resource folders as first-class course material. Create a separate `source/resources-index.md` and, where legitimate access allows, an `source/attached-resources/` folder with a manifest. Do a rendered-page pass across every lesson, not only the initial course-tree parse, because Skool may expose resources only after a lesson is selected. Mark Google Drive files/folders as indexed/pending unless they are actually downloaded or exported.

5. Use transcripts/captions when available.

If video captions/transcripts are legitimately exposed, extract them. If not, note transcript unavailable and ask before doing heavier audio transcription.

For Skool lessons with Vimeo `videoLink` values exposed in authenticated `__NEXT_DATA__`, test captions before audio transcription:

```bash
uvx yt-dlp --list-subs 'https://vimeo.com/<id>/<hash>'
uvx yt-dlp --skip-download --write-subs --sub-langs all --sub-format vtt -o 'extraction/transcripts/vtt/<order>-<title>.%(ext)s' 'https://vimeo.com/<id>/<hash>'
```

Pitfall: Vimeo may list auto-generated English as `en-x-autogen`, but `--write-auto-subs --sub-langs en.*` can still report “no subtitles”. Use normal `--write-subs --sub-langs all` first. This downloads caption files only, not videos.

6. Clean into frameworks.

After raw extraction, create cleaned summaries and reusable operating components. Keep them linked back to lesson order.

For large courses, synthesize by phase/module range with a high-context model instead of one flat pass. Use `references/high-context-phase-synthesis.md` for the phase prompt shape and Claude Code file-output contract.

For doctrine-heavy courses, use `references/doctrine-filtered-phase-synthesis.md` to preserve the course's operating system while separating usable mechanics from coercive or pseudo-scientific motivation devices.

After all phase-level synthesis outputs are complete and the user asks for a cross-phase doctrine pass, use `references/cross-phase-doctrine-pass.md`. That pass should read the completed phase outputs, build the reusable mechanics/artifact/cadence/diagnostic indexes, keep source-course doctrine separate from AsturLAB-safe doctrine, and stay inside the working repo unless the user explicitly approves vault promotion.

For multi-phase synthesis, start a fresh Claude Code session per phase/module range unless continuity genuinely requires one long context. Give the fresh session the previous phase's synthesis file only as continuity/prerequisite context, not as material to re-summarize. This prevents later phases from being flattened by earlier-phase context and keeps phase-specific worksheets/resources in focus.

If the job may exceed the current context window, maintain a concise in-workspace handoff such as `outputs/current-extraction-handoff.md` with extraction counts, completed outputs, active phase, blockers, and next step. Keep paid-course source-adjacent handoffs in the working repo until Rawan explicitly promotes durable doctrine into the vault.

When `.xlsx` resources are present, inspect workbook structure even if `openpyxl` is unavailable. Use the stdlib ZIP/XML extraction pattern in `references/spreadsheet-resource-extraction-without-openpyxl.md` before marking spreadsheet resources as unread.

7. Only then strategise.

Apply to AsturLAB after the course's structure is visible. Challenge cherry-picking. The useful asset is usually the full operating cadence, not one attractive tactic.

## Lesson file naming

Use sortable names:

`extraction/lessons/001-module-name--lesson-name.md`

Keep names concise and filesystem-safe.

## Lesson template

```markdown
# <Lesson title>

## Metadata

- Module:
- Lesson:
- Order:
- URL:
- Content type:
- Transcript/captions available:
- Extraction date:

## Placement in the course

- What came before:
- What this lesson appears to unlock:
- What it likely prepares for:
- Why this sequence may matter:

## Core teaching

## Detailed notes

Capture the lesson in order. Do not compress too early.

## Frameworks

## Steps / process

## Exercises / assignments

## Checklists

## Tools / templates mentioned

## Examples / stories / demonstrations

## Repeated language / emphasis

Capture short identifying phrases and concepts. Do not copy long copyrighted passages.

## Warnings / failure modes

## Assumptions behind the lesson

## Business application notes

Keep this section separate from extraction. Do not let AsturLAB interpretation distort the raw lesson.

## Exact items to revisit
```

## Pitfalls

- Do not start with “how AsturLAB should use this” before the course map exists.
- Do not silently save to the vault when Rawan asked for a working repo.
- Do not place a named course/community extraction inside a broader workspace after Rawan has framed it as separate. Use a course/community-named repo by default and verify any move.
- Do not turn paid material into public-facing content.
- Do not bypass access controls to fetch videos, files, or transcripts.
- Do not over-summarise early. Extraction first, synthesis second.
- Do not treat a public sales/about page as the course. Capture public facts separately, mark authenticated classroom access as pending, and wait for a legitimate logged-in session.
- Do not ask for passwords or 2FA codes. Use manual browser login handoff only.
- Do not treat Skool automation click failure as lack of access. Parse authenticated page data before asking the user to click around.
- Do not let raw Skool `[v2]` rich-text JSON pollute the course map. Clean map first, raw lesson extraction elsewhere.
- Do not bury worksheets and attached docs inside lesson summaries. Index them separately and preserve lesson association.
- Do not claim Google Drive files/folders were extracted when they were only indexed. Use explicit statuses: exported, downloaded, folder_indexed, pending_oauth, or inaccessible.
- Do not request Gmail, Calendar, Contacts, or broad Workspace permissions for course resource extraction when Drive, Docs, and Sheets are sufficient.
- Do not treat Google OAuth consent as proof that Drive/Docs/Sheets APIs are enabled in the Google Cloud project. Verify with a small API call; if `accessNotConfigured` appears, have the user enable the relevant APIs and retry after propagation.
- Do not run large Google Drive resource exports as final-write-only scripts. Add per-resource checkpointing so foreground timeouts do not discard completed exports.
- Normalize Google resource URLs before de-duplicating. Docs/Sheets links often repeat the same file ID with different tabs/headings/fragments; dedupe by file ID while preserving all lesson references, otherwise you will export the same file dozens of times.
- Do not assume nested Drive folders are duplicate material. Index and compare child IDs before skipping them.
- Do not treat Skool card click failures as proof that access is blocked. Skool may expose legitimate course/module data in `__NEXT_DATA__` even when the rendered card is automation-disabled.
- Do not write raw Skool page data into course notes. Sanitise account, payment, group-switcher, API-key, and unrelated community metadata before saving.
- Do not batch a dense course into one giant synthesis if the course is resource-heavy. Use phase/module passes and fresh high-context sessions so each phase's worksheets, transcripts, and sequence stay visible.
- Do not import a coach's coercive motivation mechanics just because the underlying operating cadence is useful. Separate artifacts, standards, lead measures, reviews, and diagnostics from shame, punishment, public humiliation, alpha/coward framing, magical thinking, unfalsifiable self-blame, and dependency hooks.
- Do not treat paid-course handoffs as vault-ready doctrine. Keep working-state handoffs inside the course workspace until Rawan explicitly asks to promote durable lessons.
- Do not let a generated cross-phase pass ask for vault promotion when the user already said not to promote. Patch the output to state the active boundary: no promotion now; future promotion requires a separate explicit instruction after a cleaned, source-safe subset exists.
- Do not mark `.xlsx` resources as unread just because `openpyxl` is unavailable. `.xlsx` is ZIP/XML; recover sheet names, shared strings, worksheet labels, and workbook-only operational details with the stdlib parser reference.
- Do not let Claude Code over-parallelize PDF/OCR probing inside the TUI. For small final phases or fragile sessions, pre-extract PDFs/XLSX/text yourself into a temporary context file, then give Claude the clean resource extract plus transcripts. If the TUI hits socket/thinking-block errors after many parallel probes, kill the phase session and restart with a tighter contract instead of trying to recover the corrupted pane.
