# PDF Translation - Step 4: Validate PDF

Validate the translated PDF for integrity, structure, and translation quality.

**Prerequisites:**
- Completed Step 3 (rebuild)
- Translated PDF in `pdf_workspace/output/`
- Original PDF for comparison

---

## Prompt Text (Copy from here)

I need to validate that the translated PDF is correct and high-quality.

**Original PDF:** `[FILENAME.pdf]`
**Translated PDF:** `pdf_workspace/output/[FILENAME]_translated.pdf`
**Glossary:** `glossaries/[YOUR_GLOSSARY].json` (optional)

## Step 4: Validate PDF

Please help me validate the translated PDF using automated checks.

### What to do:

1. **Run validation with all checks:**
   ```bash
   cd ~/.claude/skills/epub-translator/claude-skill/scripts/pdf
   python validate_pdf.py pdf_workspace/output/[FILENAME]_translated.pdf \
     --original [FILENAME.pdf] \
     --glossary glossaries/[YOUR_GLOSSARY].json \
     --visual "1,10,25,50"
   ```

   Or if running from project root:
   ```bash
   python claude-skill/scripts/pdf/validate_pdf.py \
     pdf_workspace/output/[FILENAME]_translated.pdf \
     --original [FILENAME.pdf] \
     --glossary glossaries/warhammer40k-en-cs.json \
     --visual "1,10,25,50"
   ```

2. **Expected validation checks:**

   **Check 1: PDF Integrity**
   - Can the PDF be opened?
   - Is it corrupted?
   - Page count

   **Check 2: Page Count**
   - Does translated PDF have same number of pages as original?
   - Critical: must match exactly

   **Check 3: Text Extraction**
   - Can text be extracted from all pages?
   - Tests 5 sample pages (evenly distributed)
   - Ensures PDF is not just images

   **Check 4: Glossary Compliance** (if glossary provided)
   - PRESERVE terms still in Czech text? (should remain)
   - TRANSLATE terms replaced? (source gone, target present)
   - Tests sample of 20 terms from each category

   **Check 5: Visual Comparison** (if --visual flag used)
   - Generates side-by-side screenshots
   - Original vs translated for specified pages
   - Saved to: `pdf_workspace/comparison/`
   - Manual review required

3. **Example output:**
   ```
   ============================================================
   PDF TRANSLATION VALIDATION
   ============================================================

   1. PDF Integrity Check
      Testing: pdf_workspace/output/book_translated.pdf
      ✓ PDF opens successfully
      ✓ Page count: 50

   2. Page Count Check
      Original: 50 pages
      Translated: 50 pages
      ✓ Page counts match

   3. Text Extraction Check
      ✓ Page 1: 1245 characters extracted
      ✓ Page 10: 1387 characters extracted
      ✓ Page 20: 1298 characters extracted
      ✓ Page 30: 1356 characters extracted
      ✓ Page 40: 1412 characters extracted
      ✓ Text extraction working

   4. Glossary Compliance Check
      Glossary: glossaries/warhammer40k-en-cs.json
      PRESERVE terms found: 19/20
      TRANSLATE applied: 18/20
      ✓ Glossary compliance good (>90%)

   5. Visual Comparison (Optional)
      Generating screenshots for pages: [1, 10, 25, 50]
      ✓ Page 1: page_001_original.png + page_001_translated.png
      ✓ Page 10: page_010_original.png + page_010_translated.png
      ✓ Page 25: page_025_original.png + page_025_translated.png
      ✓ Page 50: page_050_original.png + page_050_translated.png
      ✓ Screenshots saved to: pdf_workspace/comparison/

      Manual review: Compare original vs translated side-by-side

   ============================================================
   VALIDATION SUMMARY
   ============================================================

     Integrity            ✓ PASS
     Page Count           ✓ PASS
     Text Extraction      ✓ PASS
     Glossary Compliance  ✓ PASS
     Visual Comparison    ✓ PASS

   ============================================================
   ✓ All validations passed!
   ============================================================
   ```

### What I need to know:

After validation, tell me:
- Did all checks pass?
- If glossary check failed, which terms were missing?
- Were visual comparison screenshots generated?
- Is the PDF ready for final review?

### Manual Quality Checks (Recommended)

After automated validation passes, perform manual spot checks:

1. **Open translated PDF in reader:**
   ```bash
   open pdf_workspace/output/[FILENAME]_translated.pdf
   ```

2. **Check these aspects:**
   - ✅ Text is readable and properly formatted
   - ✅ No overlapping text or cutoff words
   - ✅ Czech characters display correctly (á, č, ď, é, etc.)
   - ✅ Headings/titles translated appropriately
   - ✅ Headers/footers preserved (usually unchanged)
   - ✅ Page numbers intact
   - ✅ Layout matches original (compare side-by-side)

3. **Review visual comparison screenshots:**
   ```bash
   ls pdf_workspace/comparison/
   # page_001_original.png  page_001_translated.png
   # page_010_original.png  page_010_translated.png
   # ...

   open pdf_workspace/comparison/
   ```

   Compare original vs translated:
   - Layout should be nearly identical
   - Text positions should match
   - Font sizes may be slightly smaller (overflow adjustments)
   - Images/diagrams should be unchanged

4. **Spot-check glossary terms:**
   - Search for PRESERVE terms (e.g., "Baneblade", "Cortein") → should be unchanged
   - Search for TRANSLATE terms → English version should be gone, Czech present

5. **Check critical pages:**
   - First page (title, formatting)
   - Table of contents (if present)
   - Sample chapter (content quality)
   - Last page (completeness)

### Troubleshooting Validation Failures

**Integrity Check FAIL:**
- PDF is corrupted
- Re-run rebuild step
- Check if original PDF was valid

**Page Count Mismatch:**
- Rebuild script may have skipped pages
- Check for errors in rebuild output
- Verify all translated JSON files exist

**Text Extraction FAIL:**
- Some pages may be images (scanned content)
- MVP doesn't support scanned PDFs
- May need OCR (Phase 3 feature)

**Glossary Compliance <90%:**
- Translation subagents may have missed rules
- Check glossary file path is correct
- Review sample failures (which terms?)
- May need to re-translate affected pages

**Visual Comparison Issues:**
- Text overflow visible (text cut off or overlapping)
- Font too small/large
- Layout shifted
- May need manual adjustments or Phase 2 features

### Optional: Quick Validation (Skip Visual)

For faster validation without screenshots:

```bash
python validate_pdf.py pdf_workspace/output/book_translated.pdf \
  --original book.pdf \
  --glossary glossaries/warhammer40k-en-cs.json
```

This runs checks 1-4 only (skips visual comparison).

---

## After Completion

**If all validations pass:**
✅ **Translation complete!** Your PDF is ready to read.

**Output files:**
- `pdf_workspace/output/[FILENAME]_translated.pdf` - Translated book
- `pdf_workspace/comparison/` - Visual comparison screenshots (if generated)

**Next steps:**
- Share with beta readers for feedback
- Report any issues for Phase 2 improvements
- Consider contributing glossary to community

**If validation fails:**
- Review error messages
- Check troubleshooting section above
- Re-run failed step
- Ask for help with specific error details

---

## Success Criteria (MVP)

✅ **Minimum quality standards:**
- All 5 validation checks pass
- >90% glossary compliance
- Text readable without magnification
- No major layout breaks
- Czech characters display correctly

⚠️ **Known MVP limitations (acceptable):**
- Font size slightly smaller (overflow adjustments)
- Fallback to Helvetica font (if original font lacks Czech chars)
- <5% blocks may not be replaced (extraction issues)
- Simple single-column layouts work best

🎯 **Phase 2 improvements will handle:**
- Multi-column layouts
- Complex tables
- Custom font embedding
- Better overflow handling
- Visual layout refinements
