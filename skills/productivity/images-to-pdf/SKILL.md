---
name: images-to-pdf
description: Use when the user sends multiple scan photos or image files and wants them combined into a single PDF in the exact received order, usually one full-page image per PDF page without cropping.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pdf, images, scans, documents, pymupdf]
    related_skills: [ocr-and-documents]
---

# Images to PDF

## Overview

Use this for one-off document assembly from photographed scans, screenshots, forms, receipts, IDs, or other image files.

The default output is one image per page, in the exact order received, fitted as large as possible onto the page without cropping. Preserve private content. Do not OCR, summarize, or repeat sensitive fields unless the user explicitly asks.

## When to Use

- User sends several images and asks for one PDF.
- User says the images are scans or copies.
- User needs the order preserved exactly.
- User wants full-page PDF pages without cropping.
- User wants a deliverable file, not instructions.

Do not use this for PDF text extraction. Use `ocr-and-documents` for reading or OCR.

## Privacy Rules

- Avoid describing private/legal/identity details back in chat.
- Keep the image list internal.
- Do not save task-specific image filenames, personal details, or document contents into memory or skills.
- The skill stores the procedure only.

## Workflow

1. Acknowledge the rule for ordering.
   - Tell the user to send images in order.
   - Tell them to say `done` when finished.

2. Track the image paths in exact message order.
   - Telegram image attachments arrive as local cache paths like `~/.hermes/image_cache/img_....jpg`.
   - If several images arrive in one message, preserve their listed order.

3. Ask only if page size or crop mode is materially unclear.
   - Default: A4.
   - Default: fit-to-page without cropping.
   - Default: preserve original image orientation by matching page orientation to the image.

4. Create the PDF with PyMuPDF on host Python when available.
   - `execute_code` may run in a sandbox without `fitz`; use `terminal` with `python3` if needed.
   - Do not install heavy OCR tools for simple image-to-PDF assembly.

5. Verify the PDF.
   - Confirm input image count.
   - Open the saved PDF with PyMuPDF and confirm `page_count` equals image count.
   - Report the output path and attach the PDF with `MEDIA:/absolute/path.pdf`.

## Reference Script

Use this script from `terminal`. Replace `image_paths` with the exact ordered paths from the conversation.

```bash
python3 - <<'PY'
from pathlib import Path
import fitz
import json

image_paths = [
    # '/Users/.../.hermes/image_cache/img_1.jpg',
    # '/Users/.../.hermes/image_cache/img_2.jpg',
]

missing = [p for p in image_paths if not Path(p).is_file()]
if missing:
    raise SystemExit(json.dumps({
        'status': 'missing_files',
        'count': len(missing),
        'missing': missing,
    }, indent=2))

A4_PORTRAIT = (595.275590551, 841.88976378)
A4_LANDSCAPE = (841.88976378, 595.275590551)

out_dir = Path('/Users/batcave/Downloads')
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / 'combined_scan_pages.pdf'

doc = fitz.open()
for img_path in image_paths:
    pix = fitz.Pixmap(img_path)
    img_w, img_h = pix.width, pix.height
    pix = None

    page_w, page_h = A4_LANDSCAPE if img_w > img_h else A4_PORTRAIT
    page = doc.new_page(width=page_w, height=page_h)

    scale = min(page_w / img_w, page_h / img_h)
    draw_w = img_w * scale
    draw_h = img_h * scale
    x0 = (page_w - draw_w) / 2
    y0 = (page_h - draw_h) / 2
    rect = fitz.Rect(x0, y0, x0 + draw_w, y0 + draw_h)

    page.insert_image(rect, filename=img_path, keep_proportion=True)

doc.save(str(out_path), garbage=4, deflate=True)
doc.close()

verified = fitz.open(str(out_path))
page_count = verified.page_count
verified.close()

print(json.dumps({
    'status': 'created',
    'output': str(out_path),
    'input_images': len(image_paths),
    'verified_pdf_pages': page_count,
    'file_size_mb': round(out_path.stat().st_size / (1024 * 1024), 2),
}, indent=2))
PY
```

## Output Defaults

- Save to `/Users/batcave/Downloads/combined_scan_pages.pdf` unless the user names a file.
- Use A4 page size unless the user asks for Letter or another size.
- Match each PDF page orientation to the image orientation.
- Fit image proportionally inside the page.
- No cropping.
- Center the image on the page.

## Common Pitfalls

1. **Losing order across batches.** Count pages after each batch if useful, but the source of truth is the path list in message order.

2. **Accidentally cropping scans.** Use `min(page_w / img_w, page_h / img_h)`, not `max(...)`.

3. **Using sandbox Python when it lacks dependencies.** If `execute_code` cannot import `fitz`, check host Python with `terminal`.

4. **Repeating sensitive document details.** For legal, identity, or family documents, acknowledge receipt without reading private content back into chat.

5. **Skipping verification.** Always reopen the final PDF and compare page count to input image count.

## Verification Checklist

- [ ] All image paths exist.
- [ ] Image count equals expected count.
- [ ] PDF was created at an absolute path.
- [ ] PDF opens successfully.
- [ ] PDF page count equals image count.
- [ ] Final response attaches the file with `MEDIA:/absolute/path.pdf`.
