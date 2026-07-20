# QMD collection ignore / exclusion pattern

Use this when an indexed collection contains a subfolder that should not be searchable in that collection.

## Pattern

Edit `~/.config/qmd/index.yml` and add `ignore:` as a sibling of `path`, `pattern`, and `context`:

```yaml
collections:
  asturlab:
    path: /Users/batcave/Vaults/asturlab/asturlab
    pattern: "**/*.md"
    ignore:
      - "operations/knowledge-ops/**"
    context:
      "": "Collection context..."
```

The ignore pattern is relative to the collection `path`, not the filesystem root.

## Verification sequence

```bash
cp ~/.config/qmd/index.yml ~/.config/qmd/index.yml.bak.pre-ignore.$(date +%Y%m%d-%H%M%S)
qmd collection show asturlab
qmd update
qmd status
qmd ls asturlab | grep -i 'knowledge-ops' || echo 'PASS: excluded folder has no active docs'
qmd ls asturlab | grep -E 'operations|expected-retained-subfolder'
```

Expected result after adding an ignore to a previously indexed folder:

- `qmd update` reports the ignored docs as `removed` for that collection.
- `qmd status` active doc count drops accordingly.
- `qmd ls <collection>` no longer shows ignored paths.
- `qmd embed` is only needed if `qmd status` reports embeddings needed.

## Source-code finding from qmd 2.1.0

The qmd CLI reads the live YAML config on update and passes `yamlCol?.ignore` into the indexing path. The indexing code sets `fast-glob` `cwd` to the collection path and applies `ignore` there. After scanning, qmd deactivates active docs not seen in the scan, so ignored docs are pruned rather than merely ignored for future additions.

## AsturLAB lesson

`asturlab/operations/knowledge-ops/` is a client-free control surface. It is intentionally excluded from the shared `asturlab` collection so future receipts/reports cannot accidentally become semantically searchable outside their intended scope. If procedure search is needed later, create a separate dedicated collection rather than folding control metadata into the company collection.
