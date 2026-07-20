# Google Drive course resource exporter pattern

Use this when a paid-course extraction has many Google Drive file/folder links and the normal public export pass only handled Docs/Sheets.

## When it applies

- The user has legitimate access to the course and has granted scoped Google OAuth.
- The resource index contains mixed `drive.google.com/file/d/...`, `docs.google.com/document/d/...`, `docs.google.com/spreadsheets/d/...`, `drive/folders/...`, or `open?id=...` URLs.
- Worksheets/docs/slides/folder contents must be treated as first-class course material.

## OAuth/API sequence

1. Request only the scopes needed for the extraction:
   - `https://www.googleapis.com/auth/drive`
   - `https://www.googleapis.com/auth/spreadsheets`
   - `https://www.googleapis.com/auth/documents`
2. After OAuth consent succeeds, verify the API is enabled with a small Drive query.
3. If the query returns `accessNotConfigured`, OAuth worked but the Google Cloud project APIs are disabled. Ask the user to enable Drive API, Sheets API, and Docs API for the OAuth project.
4. Treat “partial auth” warnings about Gmail/Calendar/Contacts as expected when they were intentionally excluded.

## Exporter behaviour

Build a resumable exporter rather than doing one-off CLI calls.

Required behaviour:

- Parse file IDs from all common URL shapes:
  - `/file/d/<id>`
  - `/document/d/<id>`
  - `/spreadsheets/d/<id>`
  - `/presentation/d/<id>`
  - `/drive/folders/<id>`
  - `open?id=<id>`
- Fetch Drive metadata first.
- For Google-native files, export to durable local formats:
  - Docs → `.txt`
  - Sheets → `.xlsx` when preserving workbook structure matters, `.csv` only for simple sheets
  - Slides → `.pdf`
  - Drawings → `.png`
- For binary files, download directly.
- For folders, write a folder index JSON and export direct children.
- If a folder child is itself a folder, index it and check whether its contents are already exported elsewhere before recursing.
- Store each result back into the manifest with explicit statuses such as `exported`, `folder_indexed`, `api_error_403`, or `inaccessible`.

## Resumability rule

Long Drive exports can exceed a 10-minute foreground command ceiling because of large PDFs or slow Google-native exports.

Do not rely on final-write-only output.

Checkpoint after each top-level resource and each folder child:

- Rewrite `manifest.json` with completed entries plus the untouched tail.
- Rewrite `folder-children-manifest.json` after every child export.
- Create a pre-API backup once, for example `manifest.before-drive-api.json`.

This prevents a timeout from losing hundreds of completed exports.

## Verification

Before telling the user the resource layer is complete, verify:

- Top-level manifest status counts sum to the original resource count.
- Folder-child manifest status counts are known.
- Error count is zero or every error has a clear status.
- Local file count and approximate byte total are reported.
- Any nested folders are checked for unexported unique children, not assumed to be duplicates.

## Pitfalls

- Do not call the extraction complete just because OAuth succeeded. API enablement is separate.
- Do not bury folder contents as footnotes. Folder children are course material.
- Do not assume nested folders are duplicates. Check IDs.
- Do not hard-code Gmail/Calendar/Contacts scopes for course resources.
- Do not rerun a large exporter without checkpointing.
