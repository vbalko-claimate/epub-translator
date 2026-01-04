---
name: book-translator
description: Translates EPUB books between languages while preserving formatting, structure, and metadata. Use when translating eBooks, EPUB files, or when user asks to translate a book. Handles proper names, technical terms, and chapter structure preservation.
allowed-tools: Read, Write, Bash, Glob, Grep, Task
---

# Book Translator

Automatically translate EPUB books while preserving all formatting, structure, and metadata.

## Quick Start

**CRITICAL: When user provides a book file, START IMMEDIATELY - do NOT ask for confirmation or repeat information they already gave you.**

### Automatic Workflow

**When user says:** `"translate [FILE] from [SOURCE_LANG] to [TARGET_LANG]"`

**You IMMEDIATELY:**

1. **Extract EPUB** (run `./scripts/extract.sh`)
2. **Start translation** (launch Task subagents)
3. **Rebuild EPUB** (run `./scripts/rebuild.sh`)
4. **Report completion**

**DO NOT:**
- ❌ Ask for file name again (user already provided it)
- ❌ Ask for languages again (user already specified them)
- ❌ Display summary tables before starting
- ❌ Wait for confirmation

**DO:**
- ✅ Start extraction immediately
- ✅ Use glossary if available for the book's universe
- ✅ Launch parallel Task subagents for translation
- ✅ Report progress as you work

### Format Detection

**The skill automatically detects file format:**

1. **EPUB files** (.epub extension):
   - Directly use EPUB translation workflow

2. **PDF files** (.pdf extension):
   - Auto-convert to EPUB using `scripts/convert_pdf_to_epub.py`
   - Then proceed with EPUB translation workflow

**Example user requests:**
- "translate book.epub from Czech to English" → Direct EPUB workflow
- "translate book.pdf from Czech to English" → Auto-converts to EPUB first

### EPUB Workflow (Auto-Execute)

1. **Extract EPUB** → `./scripts/extract.sh <book.epub>`
2. **Check for glossary** → Load if available (e.g., warhammer40k-en-cs.json)
3. **Identify chapters** → Find XHTML files in `OEBPS/`
4. **Translate chapters** → Launch Task subagents (2 chapters each, 5-10 agents in parallel)
5. **Update metadata** → Change language codes
6. **Rebuild EPUB** → `./scripts/rebuild.sh <output.epub>`

### PDF Support (via EPUB Conversion)

**Workflow:** PDF → EPUB → Translate → EPUB

PDFs are automatically converted to EPUB format, then translated using the existing EPUB workflow.

**Prerequisites:**
- None! Pure Python solution (auto-installs ALL dependencies on first run)

**Usage:**
```bash
# Manual conversion (optional - skill does this automatically)
python scripts/convert_pdf_to_epub.py book.pdf

# Then translate the EPUB (existing workflow)
claude "translate book.epub from Czech to English"
```

**Quality Notes:**
- ✅ Works well for text-heavy PDFs (novels, simple books)
- ⚠️ Layout changes: PDF is fixed-layout, EPUB is reflowable
- ⚠️ Chapter detection is automatic but may need manual verification
- ⚠️ Complex layouts (multi-column, tables) may simplify
- ❌ Not suitable for scanned PDFs (requires OCR first)

**What gets preserved:**
- Text content (100%)
- Basic formatting (bold, italic)
- Embedded images (JPEG, PNG, GIF, TIFF)
  - Automatically extracted and embedded in EPUB
  - Placed at end of each chapter
  - Small decorative images (<100x100px) filtered out
- Chapters (heuristic detection)

**What gets lost:**
- Fixed page layout
- Exact fonts
- Page numbers
- Headers/footers (usually removed)
- Multi-column layouts

**When to use this:**
- You have a PDF and want an EPUB translation
- Layout preservation is not critical
- Content quality matters more than exact formatting

**When NOT to use this:**
- You need to preserve exact PDF layout
- Multi-column academic papers (reading order may be wrong)
- Image-heavy or design-focused PDFs

## Glossary Support 📚

**Users can provide translation glossaries** to control how terms are handled:

### When to Use Glossaries

✅ **Use glossary when:**
- Book has many proper names (fantasy, sci-fi)
- Series with established terminology (Harry Potter, Warhammer 40k)
- User wants specific translation choices
- Existing official translation exists (match it!)

### Glossary Formats Supported

**Format 1: Simple TXT**
```
PRESERVE: Character Name
TRANSLATE: Term → Translation
PRESERVE_WITH_GRAMMAR: technical_term
CONTEXT: word → explanation
```

**Format 2: JSON** (structured)
```json
{
  "preserve": ["Name1", "Name2"],
  "translate": {"source": "target"},
  "modes": {...}
}
```

**Format 3: CSV**
```csv
term,translation,mode,notes
Name,Name,preserve,Character
London,Londýn,translate,Real place
```

### How to Load Glossary

**User provides glossary:**
```
User: "translate book.epub from English to Czech using glossary warhammer40k-en-cs.json"
```

**Skill workflow:**
1. Check if glossary file mentioned
2. If found in `glossaries/` folder → load it
3. Parse glossary rules:
   - PRESERVE terms → never translate
   - TRANSLATE terms → use specified translation
   - PRESERVE_WITH_GRAMMAR → keep but apply target language grammar
   - CONTEXT → decide based on usage
4. Pass glossary to ALL translation subagents
5. Apply consistently across all chapters

### Community Glossaries

**Pre-made glossaries available:**
- `glossaries/community/warhammer40k-en-cs.json` (Warhammer 40,000)
- `glossaries/community/harrypotter-en-cs.csv` (Harry Potter official)
- `glossaries/community/lotr-en-cs.txt` (Lord of the Rings)
- `glossaries/template.txt` (template for users to create their own)

**If user mentions a known universe:**
```
User: "translate this Warhammer 40k book"
Skill: Automatically check for glossaries/community/warhammer40k-en-cs.json
```

### Creating Glossary On-The-Fly

**If no glossary provided:**
```
Skill workflow:
1. Ask user: "Do you want me to analyze the first chapter and create a glossary?"
2. If yes:
   - Read first chapter
   - Identify proper names, places, technical terms
   - Generate glossary file
   - Ask user to review/approve
   - Save to glossaries/[book-name]-[source]-[target].txt
   - Use for translation
```

**Template for on-the-fly generation:**
```
Read first chapter of: epub_workspace/translated/OEBPS/chapter-1.xhtml

Identify:
1. Character names (capitalized, recurring)
2. Place names (locations, planets, cities)
3. Organization names (companies, military units)
4. Technical terms (weapons, devices, special vocabulary)
5. Titles/ranks (Emperor, Captain, Lord, etc.)

For each term, decide:
- PRESERVE (fictional names, made-up terms)
- TRANSLATE (real places, common words with translations)
- PRESERVE_WITH_GRAMMAR (technical terms to keep but decline)

Output as: glossaries/[book-slug]-[source]-[target].txt
```

## Core Principles

### Always Preserve ✅
- **Proper names** (characters, places, ships, organizations)
- **Technical/genre terms** specific to the book's universe
- **HTML/XML structure** (tags, attributes, CSS classes)
- **Images and media** files
- **CSS styling** and formatting

### Always Translate 📝
- **Narrative text** (dialogue, descriptions, narration)
- **Chapter titles** ("Chapter 1" → target language equivalent)
- **TOC entries** (Table of Contents labels)
- **Metadata** ("About the Author", "Prologue" → "Prolog", "Epilogue" → "Epilog")

## Workflow

### Step 1: Setup Workspace

```bash
./scripts/extract.sh book.epub
```

This creates:
```
epub_workspace/
├── original/    # Backup (never modify)
├── translated/  # Working copy
└── temp/        # Temporary files
```

### Step 2: Analyze Structure

Use Glob and Read tools to identify:
- Chapter files: `epub_workspace/translated/OEBPS/*.xhtml`
- Metadata files: `content.opf`, `toc.ncx`
- TOC file: Usually `3-TOC.xhtml` or similar

**Example identification:**
```bash
# Find all chapter XHTML files
ls epub_workspace/translated/OEBPS/*.xhtml | grep -E "chapter|content"
```

### Step 3: Translate Chapters (CRITICAL: Use Subagents!)

⚠️ **CRITICAL FOR CONTEXT MANAGEMENT:**

EPUB translation REQUIRES using Task subagents. DO NOT attempt to translate chapters directly in the main conversation. Each chapter is ~3,000-8,000 tokens, and books have 20-50+ chapters. This would exceed context limits.

**ALWAYS use the Task tool with subagent_type="general-purpose" for EACH chapter.**

**Why subagents are mandatory:**
1. **Context isolation:** Each chapter translation happens in fresh context
2. **Parallel processing:** Translate 5-10 chapters simultaneously
3. **Memory preservation:** Main conversation stays clean for coordination
4. **Error recovery:** If one chapter fails, others continue

**Model Selection (Hybrid Approach):**

💡 **Use different models for different complexity levels:**

**Use Haiku (fast & cheap) for:**
- ✅ Regular chapter content (majority of book)
- ✅ Straightforward narrative text
- ✅ Simple dialogue
- ✅ Books without complex glossaries
- 💰 **Cost:** ~90% cheaper than Sonnet
- ⚡ **Speed:** Faster translation

**Use Sonnet (high quality) for:**
- ✅ Table of Contents (TOC) - needs perfect formatting
- ✅ Metadata files (content.opf, toc.ncx) - structure-critical
- ✅ First chapter (sets translation tone/quality baseline)
- ✅ Complex chapters with heavy glossary usage
- ✅ Technical/poetic sections requiring nuance
- 🎯 **Quality:** Better at preserving proper names and structure

**Recommended strategy:**
1. **TOC, metadata, Chapter 1** → Sonnet (quality baseline)
2. **Chapters 2-N** → Haiku (bulk translation)
3. **Final chapter/epilogue** → Sonnet (strong finish)

**How to specify model:**
```
Task(
    subagent_type="general-purpose",
    prompt="Translate chapters 2-3...",
    model="haiku",  # or "sonnet"
    description="Translate chapters 2-3"
)
```

**Workflow:**

**Step 3a: Launch parallel subagents (5-10 at once)**

**Example: Hybrid model approach for 30-chapter book**

```
Use Task tool to launch multiple agents IN PARALLEL:

WAVE 1 (Critical sections - use Sonnet):
- Agent 1: Translate TOC + metadata (model="sonnet")
- Agent 2: Translate Chapter 1 (model="sonnet") - sets quality baseline

WAVE 2 (Bulk chapters - use Haiku for cost savings):
- Agent 3: Translate chapters 2-3 (model="haiku")
- Agent 4: Translate chapters 4-5 (model="haiku")
- Agent 5: Translate chapters 6-7 (model="haiku")
- Agent 6: Translate chapters 8-9 (model="haiku")
- Agent 7: Translate chapters 10-11 (model="haiku")
... continue with Haiku for chapters 12-29 ...

WAVE 3 (Final section - use Sonnet for strong finish):
- Agent N: Translate Chapter 30 + Epilogue (model="sonnet")
```

**Cost savings example:**
- Old approach (all Sonnet): 30 chapters × $X = $30X
- Hybrid approach: 3 Sonnet + 27 Haiku ≈ $3X + $3X = $6X
- **Savings: ~80% cost reduction** with minimal quality impact

**Step 3b: Prompt template for EACH subagent:**

```
Translate these EPUB chapters from [SOURCE_LANG] to [TARGET_LANG].

Files:
- epub_workspace/translated/OEBPS/[CHAPTER_1.xhtml]
- epub_workspace/translated/OEBPS/[CHAPTER_2.xhtml]

CRITICAL RULES:

1. Read each XHTML file using Read tool
2. Translate ONLY text inside <p>, <h1>, <h2>, <span> tags
3. PRESERVE ALL HTML/XML tags and attributes exactly as-is
4. Change xml:lang="[source]" to xml:lang="[target]" in EACH file
5. Use Edit tool for translations (NOT Write - preserve structure!)

[IF GLOSSARY PROVIDED, INCLUDE THIS SECTION:]
========== GLOSSARY RULES ==========

Read glossary file: [GLOSSARY_PATH]

Apply these translation rules:

PRESERVE (never translate):
[LIST FROM GLOSSARY - PRESERVE ENTRIES]

TRANSLATE (always use these exact translations):
[LIST FROM GLOSSARY - TRANSLATE ENTRIES]

PRESERVE_WITH_GRAMMAR (keep word, apply target language grammar):
[LIST FROM GLOSSARY - PRESERVE_WITH_GRAMMAR ENTRIES]
Example: "bolter" → "bolter" (nominative), "bolteru" (genitive), "bolterem" (instrumental)

CONTEXT-DEPENDENT (check usage before translating):
[LIST FROM GLOSSARY - CONTEXT ENTRIES]
Example: "Chapter" → "Kapitola" in headings, "Řád" when referring to military organization

========== END GLOSSARY ==========

[IF NO GLOSSARY, USE GENERIC RULES:]
DO NOT TRANSLATE (proper names):
[LIST CHARACTER NAMES]
[LIST PLACE NAMES]
[LIST TECHNICAL TERMS]

DO TRANSLATE:
- "Chapter X" → "[target language] X"
- "Prologue" → "[target equivalent]"
- "Epilogue" → "[target equivalent]"
- All narrative text, dialogue, descriptions

Example preservation:
<p class="Body-Text">Cortein gripped the Baneblade controls...</p>
→
<p class="Body-Text">Cortein sevřel ovládání Baneblade...</p>

Note: "Cortein" and "Baneblade" stay in English!

After translating both chapters, report completion.
```

**Important:** If glossary is provided, pass the SAME glossary to EVERY subagent for consistency!

**Step 3c: Validate Each Translation (CRITICAL!)**

⚠️ **MANDATORY VALIDATION AFTER EACH SUBAGENT:**

After EVERY Task subagent completes, you MUST validate the translation using the validation script.

**Why validation is critical:**
- Task subagents can fail silently
- Partial translations create broken EPUBs
- Detects Czech text that wasn't translated
- Enables automatic retry on failure

**Validation workflow:**

```bash
# After Task subagent finishes translating chapter(s), run:
python3 scripts/validate_translation.py epub_workspace/translated/OEBPS/chap_001.xhtml 1.0

# Exit code 0 = SUCCESS (< 1% Czech characters)
# Exit code 1 = FAILED (>= 1% Czech characters - needs retry)
```

**Complete validation procedure:**

1. **After each Task completes, validate ALL files it translated:**
   ```bash
   # If agent translated chapters 2-3:
   python3 scripts/validate_translation.py epub_workspace/translated/OEBPS/chap_002.xhtml
   python3 scripts/validate_translation.py epub_workspace/translated/OEBPS/chap_003.xhtml
   ```

2. **Check exit codes:**
   - Exit code 0 → ✅ Translation valid, mark todo as completed
   - Exit code 1 → ❌ Translation failed, needs retry

3. **Handle failures:**
   ```
   IF validation fails:
       1. Retry SAME Task subagent (up to 2 retries total)
       2. Use SAME prompt and model
       3. Validate again after retry
       4. If still fails after 2 retries → STOP and report error to user
   ```

4. **Report status clearly:**
   ```
   ✅ Chapter 2: PASS (0.00% Czech)
   ✅ Chapter 3: PASS (0.01% Czech)
   ❌ Chapter 5: FAILED (8.2% Czech) - retrying...
   ```

**Example validation in practice:**

```
User request: Translate chapters 2-5

Step 1: Launch Task subagent for chapters 2-3
Step 2: Wait for completion
Step 3: Validate chapters 2-3:
    $ python3 scripts/validate_translation.py epub_workspace/translated/OEBPS/chap_002.xhtml
    chap_002.xhtml: PASS: 0.00% Czech characters

    $ python3 scripts/validate_translation.py epub_workspace/translated/OEBPS/chap_003.xhtml
    chap_003.xhtml: FAILED: 5.2% Czech characters (threshold: 1.0%)

Step 4: Chapter 3 failed → Retry Task subagent for chapter 3 only
Step 5: Validate again:
    $ python3 scripts/validate_translation.py epub_workspace/translated/OEBPS/chap_003.xhtml
    chap_003.xhtml: PASS: 0.02% Czech characters

Step 6: All validated → Continue to chapters 4-5
```

**CRITICAL RULES:**
- ❌ NEVER proceed to Step 4 (metadata) until ALL chapters validated
- ❌ NEVER rebuild EPUB with failed validations
- ✅ ALWAYS validate EVERY chapter translated by subagents
- ✅ ALWAYS retry failed chapters (max 2 retries)
- ✅ ALWAYS report validation results to user

**Step 3d: Monitor progress**

Use TodoWrite to track translation AND validation:
```
[✓] Chapters 1-2 (Agent 1) - completed + validated
[✓] Chapters 3-4 (Agent 2) - completed + validated
[in_progress] Chapters 5-6 (Agent 3) - translating...
[pending] Chapters 7-8 (Agent 4)
...
```

Mark completed ONLY after validation passes.

**Step 3e: Handle large books (30+ chapters)**

For very large books:
1. Process in waves of 10 chapters (5 agents × 2 chapters each)
2. Wait for wave to complete before starting next
3. Validate a sample chapter from each wave
4. Continue until all chapters done

**Context management strategy:**
- Never read full chapter content in main conversation
- Use subagents for ALL file read/write operations
- Main conversation only coordinates and tracks progress

### Step 4: Update Metadata

**File:** `epub_workspace/translated/OEBPS/content.opf`

Change:
```xml
<dc:language>en-GB</dc:language>
<!-- to -->
<dc:language>cs-CZ</dc:language>  <!-- adjust for target language -->
```

**File:** `epub_workspace/translated/OEBPS/toc.ncx`

Translate navigation labels:
```xml
<navLabel><text>Prologue</text></navLabel>
<navLabel><text>Chapter 1</text></navLabel>
<navLabel><text>Epilogue</text></navLabel>

<!-- to -->

<navLabel><text>Prolog</text></navLabel>
<navLabel><text>Kapitola 1</text></navLabel>
<navLabel><text>Epilog</text></navLabel>
```

**File:** TOC XHTML (usually `3-TOC.xhtml`)

Translate table of contents entries using same approach as chapters.

### Step 5: Translate Metadata Files

If present, translate:
- **About the Author** (`7-Guy-Haley.xhtml` or similar)
- **Book introduction/legend** (genre-specific intro)
- **Title page** (only change `xml:lang` attribute)

### Step 6: Rebuild EPUB

```bash
./scripts/rebuild.sh translated_book.epub
```

This compiles everything back into a valid EPUB archive.

**⚠️ CRITICAL: Automatic Verification**

The rebuild script now includes automatic verification:
1. **File size check** - Warns if files haven't changed from original
2. **Content directory detection** - Handles OEBPS/, EPUB/, OPS/ automatically
3. **Rebuild verification** - Compares workspace vs final EPUB
4. **Checksum validation** - Ensures translated content is actually in EPUB

**If verification fails:**
```
✗ Rebuild verification FAILED

The rebuilt EPUB does NOT match the workspace!

Possible causes:
  1. Translation agents didn't save files properly
  2. Wrong workspace directory used
  3. Files were reverted after translation
```

**Fix:**
1. Check that translation agents used Write/Edit tools (not just Read)
2. Verify files in `epub_workspace/translated/OEBPS/` or `EPUB/` are actually translated
3. Compare file sizes between workspace and original
4. Re-run translation if needed

### Step 7: Validate

```bash
./scripts/validate.sh translated_book.epub
```

Check:
- ZIP integrity
- All files present
- No corrupted XHTML

## Best Practices

### Identifying Proper Names

Ask the user or infer from context:
- Character names (recurring capitalized words)
- Place names (locations, planets, cities)
- Organization names (military units, companies)
- Ship/vehicle names (often italicized)
- Made-up terminology specific to the genre

**Example for Warhammer 40k:**
- Characters: Cortein, Brasslock, Bannick
- Places: Kalidar IV, Mars, Paragon
- Units: Baneblade, Leman Russ, Imperial Guard
- Terminology: lascannon, bolter, Emperor, Omnissiah

### Handling Long Books

For books with 20+ chapters:
- Process in batches of 5 chapters
- Mark todo items for tracking progress
- Validate after each batch

### Progress Tracking

Use TodoWrite to track:
```
[ ] Extract EPUB
[ ] Translate Chapters 1-10
[ ] Translate Chapters 11-20
[ ] Translate metadata
[ ] Update language codes
[ ] Rebuild EPUB
[ ] Validate
```

## Utility Scripts

Located in `./scripts/` directory:

| Script | Purpose | Usage |
|--------|---------|-------|
| `extract.sh` | Extract EPUB to workspace | `./extract.sh book.epub` |
| `rebuild.sh` | Compile translated EPUB | `./rebuild.sh output.epub` |
| `validate.sh` | Check EPUB integrity | `./validate.sh book.epub` |
| `validate_translation.py` | Validate chapter translation completeness | `python3 validate_translation.py chap_001.xhtml [threshold]` |

## Common Issues

### Issue: XML Parsing Errors
**Cause:** Broken HTML tags during translation
**Fix:** Use Edit tool with exact string matching, never Write tool for partial file updates

### Issue: EPUB Won't Open
**Cause:** Incorrect rebuild order (mimetype must be first and uncompressed)
**Fix:** Use provided `rebuild.sh` script - it handles this correctly

### Issue: TOC Not Updating
**Cause:** Forgot to translate `toc.ncx` navigation file
**Fix:** Find and translate all `<text>` elements in `toc.ncx`

### Issue: Partial Translation (Mixed Languages in EPUB)
**Symptom:** Final EPUB contains mix of source and target language (e.g., English + Czech)
**Cause:** Task subagent failed silently or didn't complete translation
**Detection:** Use validation script after EACH translation:
```bash
python3 scripts/validate_translation.py epub_workspace/translated/OEBPS/chap_003.xhtml
# Output: "FAILED: 5.2% Czech characters (threshold: 1.0%)"
```
**Fix:**
1. **Immediately after Task subagent completes**, validate translation:
   ```bash
   python3 scripts/validate_translation.py <chapter_file>
   ```
2. If validation fails (exit code 1):
   - Retry the SAME Task subagent with SAME prompt
   - Validate again after retry
   - Max 2 retries before reporting error to user
3. **NEVER proceed to next chapter** until current one validates
4. **NEVER rebuild EPUB** until ALL chapters validate

**Prevention:**
- Follow Step 3c validation workflow (mandatory)
- Validate EVERY chapter after Task subagent
- Track validation status in TodoWrite
- Stop immediately if validation fails after 2 retries

### Issue: Rebuilt EPUB Contains Original Text (Not Translated)
**Symptom:** Workspace files are translated, but final EPUB contains original language
**Cause:** Translation agents didn't save files, or rebuild used wrong directory
**Detection:** Rebuild verification will catch this automatically
**Fix:**
1. Check workspace files: `ls -lh epub_workspace/translated/OEBPS/*.xhtml` or `EPUB/*.xhtml`
2. Compare sizes to original: `ls -lh epub_workspace/original/OEBPS/*.xhtml`
3. If sizes are identical, translation didn't happen - re-run translation
4. If sizes differ but EPUB is wrong, check:
   - Translation agents used Edit/Write tools (not just Read)
   - Agents saved to correct paths (epub_workspace/translated/...)
   - No errors in agent logs
5. Manually verify rebuild: `./scripts/verify_rebuild.sh <epub_file>`

**Prevention:** The rebuild script now automatically detects this issue and warns you

## Reference Documentation

- **[REFERENCE.md](REFERENCE.md)** - Complete EPUB specification and structure
- **[TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md)** - Detailed translation best practices
- **[../docs/troubleshooting.md](../docs/troubleshooting.md)** - Extended troubleshooting guide
- **[../docs/glossary-system.md](../docs/glossary-system.md)** - Glossary system

## Example Session

```
User: "Translate this EPUB from English to Czech: baneblade.epub"

Skill: [IMMEDIATELY starts - no questions asked]
1. ✓ Extracting EPUB: baneblade.epub
2. ✓ Found 31 chapters
3. ✓ Checking for glossary: warhammer40k-en-cs.json found!
4. ✓ Using hybrid model approach (Haiku + Sonnet)

   Wave 1 - Critical sections (Sonnet):
   ✓ Agent 1: TOC + metadata (model=sonnet)
   ✓ Validating: TOC (PASS: 0.00% Czech)
   ✓ Agent 2: Chapter 1 - Prologue (model=sonnet)
   ✓ Validating: Chapter 1 (PASS: 0.00% Czech)

   Wave 2 - Bulk chapters (Haiku for cost savings):
   ✓ Agent 3: Chapters 2-6 (model=haiku)
   ✓ Validating: Chapters 2-6 (all PASS)
   ✓ Agent 4: Chapters 7-11 (model=haiku)
   ✓ Validating: Chapters 7-11 (all PASS)
   ⚠ Agent 5: Chapters 12-16 (model=haiku)
   ❌ Validating: Chapter 14 FAILED (3.2% Czech) - retrying...
   ✓ Retry: Chapter 14 (PASS: 0.01% Czech)
   ✓ Agent 6-7: Chapters 17-29 (model=haiku)
   ✓ Validating: Chapters 17-29 (all PASS)

   Wave 3 - Final section (Sonnet):
   ✓ Agent 8: Chapter 30 + Epilogue (model=sonnet)
   ✓ Validating: Chapter 30, Epilogue (all PASS)

5. ✓ All 31 chapters translated and validated
6. ✓ Updating metadata (en-GB → cs-CZ)
7. ✓ Rebuilding EPUB: baneblade_cs.epub
8. ✓ Verifying rebuild integrity

Done! Your book is ready: baneblade_cs.epub
✅ Translation: 31/31 chapters validated (100%)
💰 Cost savings: ~80% vs all-Sonnet approach
```