# Spreadsheet resource extraction without openpyxl

Use this when paid-course resources include `.xlsx` workbooks and Python packages like `openpyxl` are unavailable.

## Why

Course worksheets often hide useful structure in workbook tabs, shared strings, and grid labels. Do not mark an `.xlsx` as unread just because `openpyxl` is missing. `.xlsx` files are ZIP archives containing XML and can be inspected with Python stdlib.

## Pattern

1. Treat the workbook as a ZIP file.
2. Read `xl/sharedStrings.xml` for text labels.
3. Read `xl/workbook.xml` for sheet names.
4. Read `xl/_rels/workbook.xml.rels` to map sheet relationship IDs to worksheet XML paths.
5. Read `xl/worksheets/sheet*.xml` and resolve shared-string cell values.
6. Capture:
   - sheet names;
   - visible labels and instructions;
   - tab-specific worksheet structure;
   - scoring columns;
   - checkboxes / weekday grids / action logs;
   - hidden operational steps that were not mentioned in the video transcript.

## Minimal parser shape

```python
import zipfile, xml.etree.ElementTree as ET, re

NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
REL = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'

def dump_xlsx(path):
    z = zipfile.ZipFile(path)
    names = z.namelist()

    shared = []
    if 'xl/sharedStrings.xml' in names:
        root = ET.fromstring(z.read('xl/sharedStrings.xml'))
        for si in root.findall(f'{NS}si'):
            shared.append(''.join(t.text or '' for t in si.iter(f'{NS}t')))

    wb = ET.fromstring(z.read('xl/workbook.xml'))
    sheets = [(s.get('name'), s.get(REL)) for s in wb.iter(f'{NS}sheet')]

    relroot = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
    rels = {r.get('Id'): r.get('Target') for r in relroot}

    for sheet_name, rid in sheets:
        target = rels.get(rid, '')
        target = target.lstrip('/') if target.startswith('/') else 'xl/' + target
        if target not in names:
            continue
        sroot = ET.fromstring(z.read(target))
        print('\n=== SHEET:', sheet_name, '===')
        for row in sroot.iter(f'{NS}row'):
            cells = []
            for c in row.findall(f'{NS}c'):
                ref = c.get('r', '')
                typ = c.get('t')
                v = c.find(f'{NS}v')
                val = ''
                if v is not None:
                    val = shared[int(v.text)] if typ == 's' else (v.text or '')
                else:
                    inline = c.find(f'{NS}is')
                    if inline is not None:
                        val = ''.join(t.text or '' for t in inline.iter(f'{NS}t'))
                if val.strip():
                    cells.append(f'{ref}:{val.strip()}')
            if cells:
                print(' | '.join(cells))
```

## What to watch for

In course extraction, workbook-only tabs may contain operational material not obvious from filenames or lesson transcripts. Examples include mid-week check-ins, scoring tables, outreach scripts, auto-calculated scorecards, and hidden setup instructions.

Do not overclaim formulas if the parser only extracted labels and shared strings. Say "structure recovered from workbook XML" unless formulas and computed cells were inspected too.
