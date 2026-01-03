# PDF Translation - Step 1: Extract PDF

Extract text with layout information from PDF for translation.

**Prerequisites:**
- Python 3.7+ installed
- PyMuPDF library installed (`pip install PyMuPDF`)

---

## Prompt Text (Copy from here)

I need to translate a PDF book from [SOURCE_LANGUAGE] to [TARGET_LANGUAGE].

**File:** `[FILENAME.pdf]`

## Step 1: Extract PDF

Please help me extract text with layout information from this PDF using the extraction script.

### What to do:

1. **Run the extraction script:**
   ```bash
   cd ~/.claude/skills/epub-translator/scripts/pdf
   python extract_pdf.py /path/to/[FILENAME.pdf]
   ```

   Or if running from project root:
   ```bash
   python scripts/pdf/extract_pdf.py [FILENAME.pdf]
   ```

2. **Expected output:**
   - Creates directory: `pdf_workspace/extracted/`
   - Generates JSON files: `page_001.json`, `page_002.json`, etc.
   - Each JSON contains text blocks with coordinates, fonts, sizes

3. **Verify extraction:**
   ```bash
   ls pdf_workspace/extracted/
   # Should show: page_001.json, page_002.json, ...

   # Check first page structure
   head -20 pdf_workspace/extracted/page_001.json
   ```

### What I need to know:

After extraction, tell me:
- How many pages were extracted?
- What's the file naming pattern?
- Sample structure (show first few blocks from page 1)

### Example output format:

```json
{
  "page_num": 1,
  "width": 595.32,
  "height": 841.92,
  "blocks": [
    {
      "text": "Chapter 1",
      "bbox": [72.0, 100.0, 200.0, 120.0],
      "font": "Times-Bold",
      "size": 18.0,
      "type": "heading"
    },
    {
      "text": "The battle raged...",
      "bbox": [72.0, 150.0, 520.0, 165.0],
      "font": "Times-Roman",
      "size": 12.0,
      "type": "body"
    }
  ]
}
```

---

## After Completion

Once extraction is complete, proceed to:
**→ [02-translate-pages.md](02-translate-pages.md)**
