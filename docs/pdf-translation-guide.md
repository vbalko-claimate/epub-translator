# PDF Translation Guide

Complete guide to translating PDF books using epub-translator with Claude Code.

---

## Overview

The PDF translation feature extends epub-translator to support **text-based PDF files** while preserving exact layout, fonts, and formatting. It uses the same glossary system and Claude Code subscription model as EPUB translation.

**Key Features:**
- ✅ Preserves layout, fonts, positions, and formatting
- ✅ Full glossary support (4 modes: PRESERVE, TRANSLATE, PRESERVE_WITH_GRAMMAR, CONTEXT)
- ✅ Parallel processing via Task subagents
- ✅ Automatic overflow detection and font size adjustment
- ✅ Comprehensive validation (integrity, glossary compliance, visual comparison)
- ✅ Works with Claude Code subscription (no API key needed)

**Limitations (MVP):**
- ⚠️ Text-based PDFs only (scanned PDFs not supported)
- ⚠️ Best for single-column layouts (multi-column support in Phase 2)
- ⚠️ Simple tables only (complex tables in Phase 2)
- ⚠️ Font fallback to Helvetica if Czech characters missing (custom fonts in Phase 3)

---

## Prerequisites

### 1. Python Dependencies

Install PDF-specific dependencies:

```bash
cd ~/.claude/skills/epub-translator/scripts
pip install -r requirements-pdf.txt
```

This installs:
- **PyMuPDF (fitz) 1.24+** - PDF extraction and rebuild
- **pdfplumber 0.11+** - Table detection (Phase 2)
- **pikepdf 8.0+** - PDF integrity validation

**Note:** No `anthropic` package needed - translation happens via Claude Code subscription!

### 2. Workspace Setup

Create the PDF workspace directory structure:

```bash
mkdir -p pdf_workspace/{original,extracted,translated,output,comparison}
```

**Directory structure:**
```
pdf_workspace/
├── original/         # Backup of original PDF
├── extracted/        # JSON files with text + coordinates
├── translated/       # JSON files with translations
├── output/          # Final translated PDF
└── comparison/      # Visual comparison screenshots (optional)
```

### 3. Glossary File (Recommended)

Reuse existing glossaries from EPUB translation:

```bash
ls glossaries/community/
# warhammer40k-en-cs.json
# Add your own glossaries here
```

See [Glossary System Guide](glossary-system.md) for details on creating glossaries.

---

## Quick Start

### 4-Step Workflow

```bash
# Step 1: Extract text with layout info
python scripts/pdf/extract_pdf.py book.pdf

# Step 2: Translate pages (via Claude Code Task subagents)
# Use prompts/pdf/02-translate-pages.md in Claude Code conversation

# Step 3: Rebuild PDF with translations
python scripts/pdf/rebuild_pdf.py book.pdf \
  -o pdf_workspace/output/book_translated.pdf

# Step 4: Validate translated PDF
python scripts/pdf/validate_pdf.py \
  pdf_workspace/output/book_translated.pdf \
  --original book.pdf \
  --glossary glossaries/warhammer40k-en-cs.json
```

**Detailed workflow with prompt templates:**
1. [01-extract-pdf.md](../prompts/pdf/01-extract-pdf.md)
2. [02-translate-pages.md](../prompts/pdf/02-translate-pages.md)
3. [03-rebuild-pdf.md](../prompts/pdf/03-rebuild-pdf.md)
4. [04-validate-pdf.md](../prompts/pdf/04-validate-pdf.md)

---

## Detailed Workflow

### Step 1: Extract PDF

**Purpose:** Extract text with coordinates, fonts, and metadata from PDF.

**Command:**
```bash
cd ~/.claude/skills/epub-translator/scripts/pdf
python extract_pdf.py /path/to/book.pdf
```

**Output:**
```
Extracting PDF: book.pdf
  Total pages: 50
  Output: pdf_workspace/extracted/

  ✓ Page   1: 15 blocks extracted
  ✓ Page   2: 18 blocks extracted
  ...
  ✓ Page  50: 17 blocks extracted

✓ Extraction complete!
  Pages: 50
  Blocks: 850
  Output: pdf_workspace/extracted/
```

**Generated files:**
```
pdf_workspace/extracted/
├── page_001.json
├── page_002.json
├── ...
└── page_050.json
```

**JSON structure (example):**
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
      "flags": 16,
      "color": 0,
      "type": "heading"
    },
    {
      "text": "The battle raged across the frozen wastes...",
      "bbox": [72.0, 150.0, 520.0, 165.0],
      "font": "Times-Roman",
      "size": 12.0,
      "flags": 0,
      "color": 0,
      "type": "body"
    }
  ]
}
```

**Text classification:**
- `header` - Top 5% of page (running headers)
- `footer` - Bottom 5% of page (page numbers)
- `heading` - Large font (>14pt), short text
- `footnote` - Small font (<10pt), bottom 15% of page
- `body` - Everything else (main content)

---

### Step 2: Translate Pages

**Purpose:** Translate extracted text using Claude Code Task subagents with glossary support.

**Two approaches:**

#### Option A: Generate Prompt Helper (Recommended)

Use `translate_pdf.py` to generate ready-to-use Task subagent prompts:

```bash
python translate_pdf.py --generate-prompt \
  --pages 1-10 \
  --source en \
  --target cs \
  --glossary warhammer40k-en-cs.json
```

**Output:** Complete Task subagent prompt with glossary rules embedded.

Copy the output and use it with Task tool in Claude Code conversation.

#### Option B: Manual Prompt Creation

Use the template from [prompts/pdf/02-translate-pages.md](../prompts/pdf/02-translate-pages.md).

**Key steps:**
1. Split pages into batches (5-10 pages per subagent)
2. Create Task subagent for each batch
3. Each subagent:
   - Reads JSON files from `pdf_workspace/extracted/`
   - Translates text with glossary rules
   - Detects overflow (Czech text >10% longer)
   - Writes to `pdf_workspace/translated/`

**Example: Parallel Translation (50-page PDF)**

In Claude Code conversation:
```
Use Task tool 5 times in one message (parallel execution):

1. Translate pages 1-10 (subagent 1)
2. Translate pages 11-20 (subagent 2)
3. Translate pages 21-30 (subagent 3)
4. Translate pages 31-40 (subagent 4)
5. Translate pages 41-50 (subagent 5)
```

Each subagent receives the same prompt template with different page ranges.

**Glossary integration:**

Glossary rules are embedded in the Task subagent prompt:

```
GLOSSARY RULES:

PRESERVE (never translate):
  - Baneblade
  - Cortein
  - Leman Russ

TRANSLATE (use exact translations):
  - Chapter → Kapitola
  - Space Marines → Vesmírní mariňáci

PRESERVE_WITH_GRAMMAR (keep word, apply Czech grammar):
  - bolter → bolter/bolteru/bolterem
```

**Output validation:**

After subagents finish, verify translated files:

```bash
ls pdf_workspace/translated/
# page_001.json, page_002.json, ..., page_050.json

# Check first page
head -30 pdf_workspace/translated/page_001.json
```

Expected fields in each block:
- `original_text` - Original English text
- `translated_text` - Czech translation
- `overflow_warning` - true/false (if text too long)
- `suggested_size` - Reduced font size (if overflow detected)

---

### Step 3: Rebuild PDF

**Purpose:** Reconstruct PDF with translations using PyMuPDF redaction.

**Command:**
```bash
python rebuild_pdf.py book.pdf \
  -o pdf_workspace/output/book_translated.pdf \
  --translated-dir pdf_workspace/translated
```

**Process:**
1. Opens original PDF
2. For each page:
   - Loads translated JSON
   - Searches for original text in PDF
   - Adds redaction annotation (white box with translation)
   - Uses `suggested_size` if overflow detected
   - Applies redactions
3. Saves compressed translated PDF

**Output:**
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

✓ PDF rebuild complete!
  Pages processed: 50
  Blocks replaced: 850
  Overflow adjustments: 12
  Output: pdf_workspace/output/book_translated.pdf
```

**Overflow adjustments:**
- Czech text typically 15-20% longer than English
- If translated text doesn't fit in original bbox, font size reduced by 10-15%
- `⚠ X overflow adjustments` indicates how many blocks needed resizing

---

### Step 4: Validate PDF

**Purpose:** Verify translated PDF integrity, quality, and glossary compliance.

**Command:**
```bash
python validate_pdf.py pdf_workspace/output/book_translated.pdf \
  --original book.pdf \
  --glossary glossaries/warhammer40k-en-cs.json \
  --visual "1,10,25,50"
```

**Validation checks:**

1. **PDF Integrity** - Can PDF be opened? Is it corrupted?
2. **Page Count** - Does translated PDF have same pages as original?
3. **Text Extraction** - Can text be extracted from all pages?
4. **Glossary Compliance** - Are PRESERVE/TRANSLATE rules applied correctly?
5. **Visual Comparison** - Side-by-side screenshots for manual review

**Output:**
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
   ...
   ✓ Text extraction working

4. Glossary Compliance Check
   Glossary: glossaries/warhammer40k-en-cs.json
   PRESERVE terms found: 19/20
   TRANSLATE applied: 18/20
   ✓ Glossary compliance good (>90%)

5. Visual Comparison (Optional)
   Generating screenshots for pages: [1, 10, 25, 50]
   ✓ Page 1: page_001_original.png + page_001_translated.png
   ...
   ✓ Screenshots saved to: pdf_workspace/comparison/

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

**Manual review:**

Open translated PDF:
```bash
open pdf_workspace/output/book_translated.pdf
```

Check:
- ✅ Text readable, properly formatted
- ✅ No overlapping text or cutoff words
- ✅ Czech characters display correctly (á, č, ď, é, ě, í, ň, ó, ř, š, ť, ú, ů, ý, ž)
- ✅ Layout matches original
- ✅ Glossary terms preserved/translated correctly

Compare screenshots:
```bash
open pdf_workspace/comparison/
```

View original vs translated side-by-side.

---

## How It Works

### PDF vs EPUB Differences

| Aspect | EPUB | PDF |
|--------|------|-----|
| **Format** | ZIP with XHTML files | Binary with coordinate-positioned text |
| **Text storage** | Semantic HTML tags | Raw text + bbox coordinates |
| **Layout** | Reflowable (responsive) | Fixed (exact positions) |
| **Fonts** | CSS font-family | Embedded font objects |
| **Complexity** | Simple (modify HTML) | Complex (preserve layout) |
| **Translation** | Replace HTML text | Redaction-based replacement |

### PyMuPDF Redaction Method

**Why redaction?**
- PyMuPDF's `add_redact_annot()` API designed for removing/replacing text
- Preserves exact coordinates (bbox)
- Handles fonts automatically
- Maintains PDF structure

**Process:**
```python
# 1. Search for original text
text_instances = page.search_for("Chapter 1")
# Returns: [Rect(72.0, 100.0, 200.0, 120.0)]

# 2. Add redaction annotation
page.add_redact_annot(
    rect=text_instances[0],
    text="Kapitola 1",        # Translation
    fontname="Times-Bold",    # Preserve font
    fontsize=18.0,            # Preserve size (or use suggested_size)
    fill=(1, 1, 1),           # White background (covers original)
    text_color=(0, 0, 0)      # Black text
)

# 3. Apply redaction (removes original, inserts translation)
page.apply_redactions()
```

**Fallback logic:**
1. Try exact text match
2. If not found, try first 3 words
3. If still not found, use bbox from JSON
4. If font missing, fallback to Helvetica

### Overflow Handling

**Problem:** Czech text 15-20% longer than English → doesn't fit in original bbox.

**Detection:**
```python
original_width = bbox[2] - bbox[0]  # bbox = [x0, y0, x1, y1]
font_size = block["size"]

# Estimate character widths (rough approximation)
original_chars = len("Chapter 1")  # 9
translated_chars = len("Kapitola 1")  # 10

original_estimated = original_chars * font_size * 0.5  # 81.0
translated_estimated = translated_chars * font_size * 0.5  # 90.0

if translated_estimated > original_width * 1.1:  # 10% threshold
    overflow_warning = True
    suggested_size = font_size * (original_width / translated_estimated) * 0.95
    # Reduce font size to fit, with 5% safety margin
```

**Solutions (priority order):**
1. **Reduce font size** (10-15%, barely noticeable)
2. **Use abbreviations** (from glossary, e.g., "Kap." for "Kapitola")
3. **Expand bbox** (if margin available) - Phase 2
4. **Flag for manual review** (if overflow >20%) - Phase 2

### Glossary System (Reused from EPUB)

**Zero changes needed!** Same glossary files work for PDF translation.

**4 modes:**

1. **PRESERVE** - Never translate (proper nouns, brand names)
   ```json
   "Cortein": {"mode": "preserve"}
   ```
   → English: "Cortein" → Czech: "Cortein" ✓

2. **TRANSLATE** - Use specific translation
   ```json
   "Chapter": {"mode": "translate", "translation": "Kapitola"}
   ```
   → English: "Chapter 1" → Czech: "Kapitola 1" ✓

3. **PRESERVE_WITH_GRAMMAR** - Keep word, apply target language grammar
   ```json
   "bolter": {"mode": "preserve_with_grammar", "declension": {...}}
   ```
   → English: "with a bolter" → Czech: "s bolterem" ✓

4. **CONTEXT** - Decide based on usage (rare, for ambiguous terms)
   ```json
   "marine": {"mode": "context", "note": "Space Marine = preserve, naval marine = translate"}
   ```

**Loading glossary:**
```python
# Supports JSON, TXT, CSV formats
glossary = load_glossary("glossaries/warhammer40k-en-cs.json")

# Embedded in Task subagent prompt
prompt = generate_subagent_prompt(
    pages="1-10",
    glossary_path="glossaries/warhammer40k-en-cs.json"
)
# → Includes formatted glossary rules in prompt
```

---

## Cost Estimation

**Per-book cost (Claude Code subscription model):**

**Example: 300-page PDF**

**Token usage:**
- Input: ~3,000 tokens/page × 300 = 900K tokens
- Output: ~3,500 tokens/page × 300 = 1,050K tokens

**Claude Sonnet 4.5 pricing:**
- Input: $3 per 1M tokens
- Output: $15 per 1M tokens

**Total cost:**
- (900K × $3/M) + (1,050K × $15/M) = **$18.45**

**Optimization strategies:**
1. **Use Claude Haiku for simple pages** → $8-12 total
2. **Batch pages efficiently** (5-10 per subagent) → fewer overhead tokens
3. **Reuse glossary across books** → no re-learning terms

**Comparison:**
- EPUB (Baneblade, 31 chapters): ~$6
- PDF (300 pages): ~$18 (more layout overhead)

**Note:** With Claude Code subscription, you're already paying for usage - these are estimates of incremental cost.

---

## Troubleshooting

### Extraction Issues

**Problem: "No text blocks extracted" or very few blocks**

**Causes:**
- Scanned PDF (images, not text) → MVP doesn't support OCR
- Corrupted PDF
- Protected/encrypted PDF

**Solutions:**
1. Check if PDF has selectable text (open in reader, try to select text)
2. Try: `pdftotext book.pdf` (if empty output → scanned PDF)
3. For scanned PDFs: Use OCR tool first (Tesseract) → Phase 3 feature

---

**Problem: Text classification wrong (body text marked as header)**

**Cause:** Classification heuristics too simplistic (based on position/font size only).

**Solution:**
- Manually edit extracted JSON if needed
- Phase 2 will improve classification with ML

---

### Translation Issues

**Problem: Glossary rules not applied**

**Causes:**
- Glossary path incorrect
- Glossary format invalid
- Task subagent didn't receive glossary rules

**Solutions:**
1. Verify glossary file exists:
   ```bash
   ls glossaries/warhammer40k-en-cs.json
   ```
2. Validate JSON format:
   ```bash
   python -m json.tool glossaries/warhammer40k-en-cs.json
   ```
3. Check Task subagent prompt includes glossary section
4. Re-run translation with corrected prompt

---

**Problem: Some blocks not translated**

**Causes:**
- Type="header" or "footer" (skipped by design)
- Translation subagent error (check subagent output)
- JSON file missing `translated_text` field

**Solutions:**
1. Check subagent output for errors
2. Manually inspect JSON:
   ```bash
   grep -L "translated_text" pdf_workspace/translated/*.json
   ```
3. Re-run translation for affected pages

---

### Rebuild Issues

**Problem: "No translation found" warnings**

**Cause:** Translated JSON files missing or misnamed.

**Solution:**
```bash
# Check translated files exist
ls pdf_workspace/translated/page_*.json | wc -l
# Should match number of pages

# Check naming pattern
ls pdf_workspace/translated/ | head -5
# Should be: page_001.json, page_002.json, etc.
```

---

**Problem: "Could not redact block" warnings**

**Causes:**
- Original text not found in PDF (extraction error)
- Text split across multiple spans in PDF
- Special characters mismatch

**Solutions:**
- Usually affects <5% of blocks (acceptable for MVP)
- Phase 2 will improve text matching
- Manually fix critical blocks if needed

---

**Problem: Czech characters display as boxes or garbled**

**Cause:** Original font doesn't support Czech characters (á, č, ď, é, ě, í, ň, ó, ř, š, ť, ú, ů, ý, ž).

**Solution:**
- Script automatically falls back to Helvetica (built-in, has Czech)
- Phase 3 will add custom font embedding
- For MVP: Acceptable trade-off (readability over font consistency)

---

### Validation Issues

**Problem: Glossary compliance <90%**

**Causes:**
- PRESERVE terms were translated (rule violation)
- TRANSLATE terms not replaced (rule not applied)

**Solutions:**
1. Check which terms failed:
   ```bash
   # Extract full text from translated PDF
   pdftotext pdf_workspace/output/book_translated.pdf -

   # Search for PRESERVE terms
   grep "Baneblade" book_translated.txt  # Should exist

   # Search for TRANSLATE source terms
   grep "Chapter" book_translated.txt  # Should NOT exist (should be "Kapitola")
   ```
2. If <50% compliance: Re-run translation with corrected glossary
3. If 50-90%: Manually review failures, may be edge cases

---

**Problem: Visual comparison shows layout shifts**

**Causes:**
- Overflow >20% (text significantly longer)
- Font fallback changed spacing
- Multi-column layout misdetected (MVP limitation)

**Solutions:**
- Review overflow warnings in rebuild output
- Phase 2 will improve overflow handling
- For critical pages: Manual adjustments or abbreviations

---

## Limitations & Future Phases

### MVP Limitations (Current)

⚠️ **Scanned PDFs:** Not supported (requires OCR)
⚠️ **Multi-column layouts:** May have reading order issues
⚠️ **Complex tables:** Cell boundaries may break
⚠️ **Font embedding:** Fallback to Helvetica if Czech chars missing
⚠️ **Text overflow >20%:** May require manual adjustments
⚠️ **Images with text overlays:** Text not translated

### Phase 2 Features (Planned)

🎯 **Layout detection:** Multi-column, tables, headers/footers (sklearn clustering)
🎯 **Better overflow:** Expand bbox if margin available, smart abbreviations
🎯 **Table support:** pdfplumber integration for cell-by-cell translation
🎯 **Visual validation:** Automated screenshot diff highlighting

### Phase 3 Features (Future)

🎯 **Font embedding:** Custom fonts with full Czech character support
🎯 **Code/math detection:** Auto-preserve technical content
🎯 **OCR support:** Scanned PDF translation via Tesseract
🎯 **Batch automation:** Entire book in one command
🎯 **Quality reports:** Detailed translation quality metrics

---

## Best Practices

### 1. Glossary Preparation

- **Reuse existing glossaries** from EPUB translations
- **Test on first 10 pages** before translating entire book
- **Community glossaries** available in `glossaries/community/`
- **Contribute back** your glossaries for others

### 2. Page Batching

- **5-10 pages per subagent** for optimal performance
- **Parallel processing** dramatically reduces total time (5 subagents × 10 pages = 50 pages in ~same time as 10 pages)
- **Monitor progress** from each subagent to catch errors early

### 3. Quality Checks

- **Always validate** with all 5 checks before considering complete
- **Manual spot checks** on first/last pages and random samples
- **Visual comparison** for layout-critical books (technical, illustrated)
- **Beta readers** for final quality confirmation

### 4. Backup Strategy

```bash
# Before starting, backup original
cp book.pdf pdf_workspace/original/book_original.pdf

# After validation, backup translated
cp pdf_workspace/output/book_translated.pdf pdf_workspace/output/book_translated_final.pdf
```

### 5. Iterative Improvement

- **Start simple:** Translate 10 pages, validate, refine glossary
- **Scale up:** Translate 50 pages, check quality
- **Full book:** Once confident in workflow
- **Feedback loop:** Contribute improvements, glossaries, issue reports

---

## Examples

### Example 1: Simple Novel (Single-Column)

**Book:** 200-page fantasy novel, single-column layout

**Workflow:**
```bash
# Extract
python extract_pdf.py fantasy_novel.pdf

# Translate (20 subagents × 10 pages)
# Use prompts/pdf/02-translate-pages.md in Claude Code

# Rebuild
python rebuild_pdf.py fantasy_novel.pdf -o pdf_workspace/output/fantasy_novel_cs.pdf

# Validate
python validate_pdf.py pdf_workspace/output/fantasy_novel_cs.pdf \
  --original fantasy_novel.pdf \
  --visual "1,50,100,150,200"
```

**Time:** ~30-45 minutes (mostly translation)
**Cost:** ~$12 (Claude Sonnet 4.5)
**Quality:** Excellent (simple layout, MVP handles well)

---

### Example 2: Warhammer 40K Novel (Glossary-Heavy)

**Book:** 300-page sci-fi with extensive terminology

**Glossary:** `warhammer40k-en-cs.json` (150+ terms)

**Workflow:**
```bash
# Extract
python extract_pdf.py warhammer_book.pdf

# Generate prompts with glossary
python translate_pdf.py --generate-prompt \
  --pages 1-10 \
  --glossary warhammer40k-en-cs.json > batch1_prompt.txt

# Use generated prompt in Task tool (repeat for all batches)

# Rebuild
python rebuild_pdf.py warhammer_book.pdf -o pdf_workspace/output/warhammer_book_cs.pdf

# Validate with glossary
python validate_pdf.py pdf_workspace/output/warhammer_book_cs.pdf \
  --original warhammer_book.pdf \
  --glossary warhammer40k-en-cs.json \
  --visual "1,100,200,300"
```

**Time:** ~45-60 minutes
**Cost:** ~$18
**Quality:** Very good (glossary ensures consistency)
**Glossary compliance:** >95%

---

## FAQ

**Q: Can I translate scanned PDFs?**
A: Not in MVP. Scanned PDFs require OCR (Optical Character Recognition) which is planned for Phase 3.

**Q: Why does the translation cost more than EPUB?**
A: PDF has more metadata overhead (coordinates, fonts, layout info) → more tokens per page. Typical: $18 for 300-page PDF vs $6 for 300-page EPUB.

**Q: Can I use my existing EPUB glossaries for PDF?**
A: Yes! Glossary system is identical → 100% compatible.

**Q: What if my PDF has tables?**
A: Simple tables work in MVP. Complex tables with merged cells may need Phase 2 (pdfplumber integration).

**Q: How do I handle multi-column academic papers?**
A: MVP may have reading order issues. Phase 2 adds multi-column detection. For now: Extract, manually reorder blocks in JSON if needed.

**Q: Can I customize font sizes manually?**
A: Yes. Edit `suggested_size` in translated JSON before rebuild step.

**Q: What if validation fails?**
A: See [Troubleshooting](#troubleshooting) section. Most issues can be fixed by re-running specific steps.

**Q: Can I contribute my glossaries?**
A: Absolutely! Submit to `glossaries/community/` via GitHub.

---

## Getting Help

**Issues & Bug Reports:**
- GitHub: [epub-translator issues](https://github.com/anthropics/claude-code/issues)

**Community:**
- Share glossaries in `glossaries/community/`
- Contribute improvements via pull requests

**Documentation:**
- [Glossary System Guide](glossary-system.md)
- [How It Works](how-it-works.md) (includes PDF section)
- [Context Management](context-management.md)

---

## Summary

**MVP PDF Translation (Current):**
- ✅ Text-based PDFs with layout preservation
- ✅ Full glossary support (PRESERVE, TRANSLATE, PRESERVE_WITH_GRAMMAR, CONTEXT)
- ✅ Parallel processing via Task subagents
- ✅ Automatic overflow handling (font size reduction)
- ✅ Comprehensive validation (5 checks)
- ✅ Claude Code subscription (no API key)
- ✅ Cost: ~$12-20 per 300-page book

**Best for:**
- Single-column novels
- Standard fonts
- Simple layouts
- Glossary-heavy content

**Workflow:**
1. Extract → 2. Translate (Task subagents) → 3. Rebuild → 4. Validate

**Quality:** Very good for MVP scope, excellent with Phase 2/3 improvements.

Happy translating! 🎉
