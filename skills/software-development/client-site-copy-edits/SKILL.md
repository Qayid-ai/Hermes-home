---
name: client-site-copy-edits
description: Fast workflow for small copy/data changes in client website repos from screenshots or brief requests. Use when Rawan asks for a quick text/name/content change on a client site and expects the repo to be edited and verified, not just explained.
---

# Client Site Copy Edits

Use this for small client website changes: review names, testimonials, headings, CTA copy, metadata, or simple data/content edits.

## Workflow

1. Identify the repo before editing.
   - If the request mentions a site/client but not a path, search likely repo locations first.
   - On macOS, `mdfind` is often faster than broad filesystem scans:
     - `mdfind "kMDItemFSName == '*CLIENT_OR_SITE_KEYWORD*'cd" | head -50`
   - Avoid broad `find /Users/...` or full `search_files` over home when Spotlight can narrow it.

2. Load project context.
   - Check for `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, or similar project files.
   - Treat client context as confidential.
   - Do not reuse details in public content.

3. Check git state before changing files.
   - Run `git status --short` and `git branch --show-current`.
   - Do not overwrite or remove unrelated untracked files.
   - If on `main`, create a short branch for the edit unless the user explicitly asked otherwise.

4. Locate the exact text.
   - Use `search_files` for the literal name/text and close variants.
   - If the screenshot truncates the text, search the visible full or partial string.
   - Prefer editing the source data/component, not built assets.

5. Make the smallest possible edit.
   - Use `patch` for a targeted replacement.
   - Keep punctuation exactly as requested.
   - Do not refactor surrounding code during a copy edit.

6. For small image/icon replacements.
   - Save the supplied image under an appropriate public/static path rather than linking to ephemeral upload/cache paths.
   - If the display target is a circular avatar or tiny icon, crop to a square first and center the actual subject, not the whole photo.
   - `ffmpeg` works well when Pillow/ImageMagick are unavailable:
     - `ffmpeg -y -i INPUT.jpg -vf "crop=W:H:X:Y,scale=512:512" -q:v 2 public/images/name.jpg`
   - Use `sips -g pixelWidth -g pixelHeight FILE` or `file FILE` to verify dimensions.
   - Use `vision_analyze` on the cropped asset before wiring it in when subject positioning matters.
   - After wiring it in, generate a preview and verify visually that the image appears in the intended UI, not just that the file exists.
   - If screenshots are only for chat preview, copy them to a temp/previews directory before final delivery and remove preview PNGs from the repo so they do not pollute `git status`.

7. Verify.
   - Re-search for the old and new string.
   - Run the repo's minimum verification command from project context, usually `npm run build` for Vite/React marketing sites.
   - Check `git diff` and `git status --short` before final response.

8. If Rawan asks for a preview screenshot.
   - Start the local dev server with the repo command, usually `npm run dev -- --host 127.0.0.1`, as a tracked background process.
   - Check readiness with `curl -sI http://127.0.0.1:5173` or the logged dev-server URL.
   - If the browser tool fails because Chrome is unavailable, use Playwright directly from Hermes:
     - `const { chromium } = require('/Users/batcave/.hermes/hermes-agent/node_modules/playwright');`
   - Use a mobile viewport when the request/screenshot is mobile, e.g. `{ width: 390, height: 844, deviceScaleFactor: 2, isMobile: true }`.
   - Scroll to the relevant section by role/text, then verify the target text is actually visible in the screenshot. DOM text existing is not enough; check bounding boxes or use `vision_analyze`.
   - Save the screenshot inside the repo or a temp path and return it with `MEDIA:/absolute/path.png`.

## Response format

Keep the final response short:

- State the exact change.
- State the file changed.
- State the verification result.
- Mention unrelated existing dirty/untracked files only if present.

## Pitfalls

- Skill names may be unqualified in this Hermes install even when the displayed list groups them by category. If `skill_view('github:...')` fails, retry with the bare skill name.
- Do not run destructive cleanup to remove unrelated files.
- Do not commit, push, or open a PR unless Rawan asks.
