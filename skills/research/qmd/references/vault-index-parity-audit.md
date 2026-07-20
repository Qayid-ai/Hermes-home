# Vault ↔ QMD index parity audit

Use when the user asks whether QMD matches a vault or whether deleted files are still searchable.

Pattern from session:
1. Compare QMD's configured collections against the live vault files, not the entire vault by default.
2. For each configured collection, run `qmd ls <collection>` and parse `qmd://...` URIs.
3. Walk the corresponding vault folder for `**/*.md` and convert each path to the expected `qmd://<collection>/<relative-path>` URI.
4. Diff both sets:
   - live vault minus QMD = missing from index
   - QMD minus live vault = stale indexed record
5. If the only mismatch is `README.md` / `AGENTS.md` shown as lowercase `readme.md` / `agents.md`, verify with `qmd get` using both cases before calling it stale. QMD may normalise URIs while still resolving the real source file correctly.
6. Also compare against the whole vault when the user says "whole vault". Report files outside configured collection roots separately; they are not QMD mismatches unless QMD is intended to index them.
7. Run `qmd update` to remove stale records, then verify with `qmd ls`, exact `qmd search`, MCP query if relevant, and vector search if stale chunks are the concern.

Reporting standard:
- Say "matches the configured QMD collections" when QMD and the configured roots match.
- Separately list vault files outside QMD's configured collections.
- Do not imply QMD indexes archive/root files unless `qmd collection list/show` proves that it does.
