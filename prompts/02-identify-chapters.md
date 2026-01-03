# Prompt 2: Identify Chapters

**For:** All AI assistants

Use this prompt after completing workspace setup to get a detailed breakdown of what to translate.

---

## Prompt Text (Copy from here)

```
Now that the EPUB is extracted, help me identify and organize the chapters for translation.

**Workspace:** `epub_workspace/translated/`

### Tasks:

1. **List all XHTML chapter files:**
   ```bash
   find epub_workspace/translated -name "*.xhtml" -type f | sort
   ```

2. **For each file, determine:**
   - Is it a chapter? (contains story content)
   - Is it metadata? (TOC, author bio, legal, etc.)
   - Should it be translated or skipped?

3. **Read the first few lines of each file** to identify:
   - File type (chapter, prologue, epilogue, TOC, etc.)
   - Chapter number or title
   - Language attribute (xml:lang)

4. **Create a translation checklist** organized as:

   **Priority 1 - Main Story:**
   - [ ] Prologue (if present)
   - [ ] Chapter 1: [filename]
   - [ ] Chapter 2: [filename]
   - [...list all chapters...]
   - [ ] Epilogue (if present)

   **Priority 2 - Metadata:**
   - [ ] Table of Contents: [filename]
   - [ ] About the Author: [filename]
   - [ ] Book Introduction/Legend: [filename]

   **Skip - Don't Translate:**
   - Copyright page
   - License page
   - Publisher info
   - Newsletter signup
   - Backlist (other books by author)

5. **Identify proper names** that should be preserved:
   - Read through the first chapter
   - List character names
   - List place names
   - List technical/fantasy terms unique to this book

### Output Format:

Please provide:
1. Total number of files to translate
2. Organized checklist (as shown above)
3. Estimated translation workload (small/medium/large)
4. List of proper names to preserve (from sample chapter)
```

---

## Example Expected Output

```
📊 EPUB Translation Analysis
══════════════════════════════════════

📁 Structure:
  - Total XHTML files: 51
  - Story chapters: 31 files
  - Metadata files: 3 files
  - Skip (legal/promo): 17 files

📚 Priority 1 - Main Story (31 files):
  ✓ 6-40k-Content.xhtml (Prologue)
  ✓ 6-40k-Content-2.xhtml (Chapter 1)
  ✓ 6-40k-Content-3.xhtml (Chapter 2)
  ... [continues]
  ✓ 6-40k-Content-50.xhtml (Epilogue)

📄 Priority 2 - Metadata (3 files):
  ✓ 3-TOC.xhtml (Table of Contents)
  ✓ 5-40k-Legend.xhtml (Warhammer 40k Introduction)
  ✓ 7-Guy-Haley.xhtml (About the Author)

🚫 Skip - Don't Translate (17 files):
  - 2-40k-Backlist.xhtml (Promotional)
  - 11-40k-Legal.xhtml (Copyright)
  - 12-eBook-license.xhtml (License)
  ... [etc]

🏷️ Proper Names to Preserve (from Chapter 1):
  Characters: Cortein, Brasslock, Hannick
  Places: Mars, Kalidar IV, Paragon
  Ships/Units: Mars Triumphant, Baneblade
  Technical: lascannon, vox, augur, Emperor, Omnissiah

📊 Workload Estimate: MEDIUM-LARGE
  - 31 chapters × ~15 min each = ~8 hours
  - 3 metadata files × ~10 min = ~30 min
  - Total: ~8-9 hours
```

## Next Step

After identifying all chapters, proceed to:
**→ [03-translate-chapter.md](03-translate-chapter.md)** to start translating
