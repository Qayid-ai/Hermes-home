# Stale index entries after source file deletion

Session signal: QMD returned results for deleted vault inbox files even though the files were already gone from disk.

Durable lesson:
- A QMD search result is evidence of an indexed document, not proof the source file still exists.
- Before telling the user a file exists, verify the source path on disk with the vault/file tools when available.
- If the source file is gone but QMD still returns it, frame the problem as stale index cleanup, not another vault deletion.
- Preserve docids/URIs in the report so the cleanup target is unambiguous.

Recommended handling:
1. Search QMD for the suspected deleted filename/phrase.
2. Verify the file path on disk separately.
3. If QMD still has it but disk does not, say: "The vault file is gone; QMD has a stale indexed record."
4. Run or propose QMD maintenance only after checking the current local CLI help/status for the correct purge/reindex command. Do not invent a deletion command from memory.
