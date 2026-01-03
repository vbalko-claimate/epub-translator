---
name: epub-translator
description: Translates EPUB books between languages while preserving formatting, structure, and metadata. Use when translating eBooks, EPUB files, or when user asks to translate a book. Handles proper names, technical terms, and chapter structure preservation.
allowed-tools: Read, Write, Bash, Glob, Grep, Task
---

# EPUB Translator

Automatically translate EPUB books while preserving all formatting, structure, and metadata.

## Quick Start

When the user asks to translate an EPUB book:

1. **Extract EPUB** → `./scripts/extract.sh <book.epub>`
2. **Check for glossary** → Load translation dictionary if user provides one
3. **Identify content** → Find chapter files in `OEBPS/` directory
4. **Translate chapters** → Use Task subagents for parallel processing with glossary
5. **Update metadata** → Change language codes in `content.opf` and `toc.ncx`
6. **Rebuild EPUB** → `./scripts/rebuild.sh <output.epub>`

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

**Workflow:**

**Step 3a: Launch parallel subagents (5-10 at once)**

```
Use Task tool to launch multiple agents IN PARALLEL:
- Agent 1: Translate chapters 1-2
- Agent 2: Translate chapters 3-4
- Agent 3: Translate chapters 5-6
- Agent 4: Translate chapters 7-8
- Agent 5: Translate chapters 9-10
```

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

**Step 3c: Monitor progress**

Use TodoWrite to track:
```
[ ] Chapters 1-2 (Agent 1) - in_progress
[ ] Chapters 3-4 (Agent 2) - in_progress
[ ] Chapters 5-6 (Agent 3) - in_progress
...
```

Mark completed as subagents finish.

**Step 3d: Handle large books (30+ chapters)**

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

## Reference Documentation

- **[REFERENCE.md](REFERENCE.md)** - Complete EPUB specification and structure
- **[TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md)** - Detailed translation best practices
- **[../docs/troubleshooting.md](../docs/troubleshooting.md)** - Extended troubleshooting guide

## Example Session

```
User: "Translate this EPUB from English to Czech: baneblade.epub"