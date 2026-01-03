# PDF Translation - Step 3: Rebuild PDF

Rebuild the PDF with translations while preserving layout, fonts, and formatting.

**Prerequisites:**
- Completed Step 2 (translation)
- All translated JSON files in `pdf_workspace/translated/`
- Original PDF file

---

## Prompt Text (Copy from here)

I need to rebuild the PDF with Czech translations while preserving the original layout.

**Original PDF:** `[FILENAME.pdf]`
**Translated pages:** `pdf_workspace/translated/page_001.json` to `page_NNN.json`
**Output:** `pdf_workspace/output/[FILENAME]_translated.pdf`

## Step 3: Rebuild PDF

Please help me rebuild the PDF using the PyMuPDF redaction-based replacement method.

### What to do:

1. **Run the rebuild script:**
   ```bash
   cd ~/.claude/skills/epub-translator/claude-skill/scripts/pdf
   python rebuild_pdf.py [FILENAME.pdf] \
     --output pdf_workspace/output/[FILENAME]_translated.pdf \
     --translated-dir pdf_workspace/translated
   ```

   Or if running from project root:
   ```bash
   python claude-skill/scripts/pdf/rebuild_pdf.py [FILENAME.pdf] \
     -o pdf_workspace/output/[FILENAME]_translated.pdf
   ```

2. **Expected process:**
   - Opens original PDF
   - For each page:
     - Loads translated JSON
     - Searches for original text in PDF
     - Adds redaction annotation (removes original, inserts translation)
     - Applies font size adjustments for overflow warnings
     - Applies all redactions
   - Saves translated PDF with compression

3. **Monitor output:**
   ```
   Rebuilding PDF with translations
     Original: book.pdf
     Translations: pdf_workspace/translated
     Output: pdf_workspace/output/book_translated.pdf

   Processing 50 pages...

     ✓ Page   1:   15 blocks replaced
     ✓ Page   2:   18 blocks replaced
     ✓ Page   3:   20 blocks replaced (⚠ 2 overflow adjustments)
     ...
     ✓ Page  50:   17 blocks replaced

   ✓ PDF rebuild complete!
     Pages processed: 50
     Blocks replaced: 850
     Overflow adjustments: 12
     Output: pdf_workspace/output/book_translated.pdf
   ```

### What I need to know:

After rebuild, tell me:
- How many pages were processed?
- How many text blocks were replaced?
- Were there any overflow adjustments? (indicates font size was reduced)
- Output file path

### Technical Details (How it Works)

**PyMuPDF Redaction Method:**

1. **Text Search:** Find original text in PDF by exact match
   ```python
   text_instances = page.search_for("Chapter 1")
   # Returns: [Rect(72.0, 100.0, 200.0, 120.0)]
   ```

2. **Add Redaction:** Mark area for replacement
   ```python
   page.add_redact_annot(
       rect=text_instances[0],
       text="Kapitola 1",
       fontname="Times-Bold",
       fontsize=18.0,
       fill=(1, 1, 1),      # White background
       text_color=(0, 0, 0)  # Black text
   )
   ```

3. **Apply Redaction:** Remove original, insert translation
   ```python
   page.apply_redactions()
   ```

**Font Handling:**
- Preserves original font from JSON metadata
- Fallback to Helvetica ("helv") if font not available
- Handles Czech characters (á, č, ď, é, ě, í, ň, ó, ř, š, ť, ú, ů, ý, ž)

**Overflow Handling:**
- If `overflow_warning: true` in JSON, uses `suggested_size` instead of original `size`
- Reduces font size by ~10-15% to fit longer Czech text
- Maintains readability while preserving layout

**Fallback Search:**
- If exact text match not found, searches for first 3 words
- If still not found, uses bbox coordinates from JSON

### Troubleshooting

**Problem: "No translation found" for some pages**
- Check that translated JSON files exist in `pdf_workspace/translated/`
- Ensure page numbering is correct (page_001.json, page_002.json, etc.)

**Problem: "Could not redact block" warnings**
- Some text may not be found in PDF (extracted incorrectly)
- Usually affects <5% of blocks
- Can be ignored for MVP, fixed in Phase 2

**Problem: Czech characters display as boxes/garbled**
- Font doesn't support Czech characters
- Script automatically falls back to Helvetica
- Phase 3 will add custom font embedding

**Problem: Text overlaps or overflows margins**
- Czech text significantly longer than English (>20%)
- Overflow detection should have flagged in Step 2
- May need manual adjustment or abbreviations

---

## After Completion

Once rebuild is complete, proceed to:
**→ [04-validate-pdf.md](04-validate-pdf.md)**
