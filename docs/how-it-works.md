# How EPUB Translation Works

This guide explains the technical foundation of EPUB translation, making it accessible to anyone using AI code assistants.

---

## What is an EPUB?

**EPUB** (Electronic PUBlication) is the most common format for eBooks. At its core:

> **An EPUB is just a ZIP archive containing HTML files, CSS stylesheets, images, and metadata.**

Think of it like a website packaged into a single file. This simple fact makes EPUB translation possible!

---

## EPUB Anatomy

### Visual Structure

```
book.epub (ZIP archive)
│
├── mimetype                   # Must be first, tells readers "I'm an EPUB"
├── META-INF/
│   └── container.xml         # Points to content.opf
│
└── OEBPS/                    # Main content folder (name may vary)
    ├── content.opf           # Book metadata & manifest
    ├── toc.ncx              # Table of contents navigation
    │
    ├── Text/                 # Chapter files (XHTML)
    │   ├── chapter-1.xhtml
    │   ├── chapter-2.xhtml
    │   └── ...
    │
    ├── Styles/              # CSS stylesheets
    │   └── style.css
    │
    └── Images/              # Cover, illustrations
        ├── cover.jpg
        └── ...
```

**Note:** The content folder might be named `OEBPS`, `EPUB`, `OPS`, or `content` - all are valid!

---

## Key Files Explained

### 1. mimetype

```
application/epub+zip
```

- **Size:** Exactly 20 bytes
- **Purpose:** Identifies the file as EPUB to readers
- **Critical:** MUST be the first file in the ZIP
- **Critical:** MUST be uncompressed (ZIP storage level 0)

**Why it matters:** If this file is compressed or not first, many EPUB readers will reject the file!

### 2. META-INF/container.xml

```xml
<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>
```

- **Purpose:** Points readers to the package document (content.opf)
- **Translation:** Usually don't need to touch this file

### 3. content.opf (Package Document)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" xml:lang="en-GB">
    <metadata>
        <dc:title>Baneblade</dc:title>
        <dc:creator>Guy Haley</dc:creator>
        <dc:language>en-GB</dc:language>  <!-- CHANGE THIS! -->
        <meta property="dcterms:modified">2023-01-15T10:00:00Z</meta>
    </metadata>

    <manifest>
        <item id="chapter1" href="chapter-1.xhtml" media-type="application/xhtml+xml"/>
        <item id="css" href="style.css" media-type="text/css"/>
        <!-- ... all files listed ... -->
    </manifest>

    <spine>
        <itemref idref="chapter1"/>
        <!-- ... reading order ... -->
    </spine>
</package>
```

**What to translate:**
- `<dc:language>` - Change language code (e.g., `en-GB` → `cs-CZ`)
- Optionally: `<dc:title>` if translating the book title

**Don't change:**
- File paths in `<manifest>`
- Reading order in `<spine>`

### 4. toc.ncx (Navigation)

```xml
<navMap>
    <navPoint id="chapter1" playOrder="1">
        <navLabel>
            <text>Chapter 1</text>  <!-- TRANSLATE THIS -->
        </navLabel>
        <content src="chapter-1.xhtml"/>  <!-- DON'T CHANGE THIS -->
    </navPoint>
</navMap>
```

**What to translate:**
- `<text>` elements (chapter names)

**Don't change:**
- `src` attributes (file paths)
- `id` or `playOrder` attributes

### 5. Chapter Files (XHTML)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-GB">
<head>
    <title>Chapter 1</title>
    <link rel="stylesheet" href="../Styles/style.css"/>
</head>
<body>
    <h1>Chapter 1</h1>

    <p class="first-paragraph">
        The battle raged across the frozen wastes of Kalidar IV.
    </p>

    <p class="body-text">
        <span class="character-name">Cortein</span> gripped the controls
        of the mighty <em>Baneblade</em> tank as las-fire streaked past.
    </p>
</body>
</html>
```

**What to translate:**
- Text inside `<p>`, `<h1>`, `<span>`, etc.
- Change `xml:lang="en-GB"` to target language

**Preserve:**
- ALL HTML tags (`<p>`, `<span>`, `<em>`)
- ALL CSS classes (`class="first-paragraph"`)
- ALL attributes
- Proper names (characters, places, technical terms)

---

## Why This Translation Method Works

### Traditional Translation Challenges

**Manual editing:**
- Open EPUB in Calibre/Sigil
- Edit each chapter by hand
- Easy to break formatting
- Slow and tedious

**Machine translation:**
- Google Translate loses formatting
- Proper names get translated incorrectly
- No context awareness
- Can't preserve HTML structure

### AI Code Assistant Advantages

✅ **Structure preservation:** AI reads XHTML, preserves tags, only translates text

✅ **Context awareness:** AI understands story context, genre conventions

✅ **Proper name detection:** AI can distinguish character names from common words

✅ **Batch processing:** Translate multiple chapters in parallel

✅ **Quality control:** AI maintains consistency across chapters

---

## Translation Workflow Overview

### Step 1: Extract

```bash
unzip book.epub -d workspace/
```

This unpacks the EPUB into its component files:
- Metadata (XML)
- Chapters (XHTML)
- Stylesheets (CSS)
- Images (JPG/PNG)

### Step 2: Identify Content

Scan the workspace to find:
- Which files are chapters? (contain story text)
- Which are metadata? (TOC, author bio)
- Which to skip? (copyright, promotional pages)

Example:
```
TRANSLATE:
✓ chapter-1.xhtml
✓ chapter-2.xhtml
✓ toc.xhtml

SKIP:
✗ copyright.xhtml
✗ backlist.xhtml
```

### Step 3: Translate Chapters

For each chapter file:

1. **Read** the XHTML file
2. **Translate** text content only
3. **Preserve** all HTML structure
4. **Update** language attribute
5. **Write** back to same location

**AI does this automatically** using prompts or Claude Skill!

### Step 4: Update Metadata

Update language codes:
- `content.opf`: Change `<dc:language>`
- `toc.ncx`: Translate navigation labels

### Step 5: Rebuild EPUB

```bash
cd workspace/
zip -0 -X ../translated.epub mimetype       # Add mimetype first, uncompressed
zip -r ../translated.epub META-INF OEBPS    # Add everything else
```

**Critical order:**
1. Add `mimetype` first with `-0` flag (no compression)
2. Add all other files normally

### Step 6: Validate

```bash
unzip -t translated.epub    # Test ZIP integrity
```

Then open in an EPUB reader to verify:
- Chapters display correctly
- Table of contents works
- Images show up
- Formatting preserved

---

## Common EPUB Variations

### Content Folder Names

| Folder Name | Frequency | Notes |
|-------------|-----------|-------|
| `OEBPS` | Most common | "Open eBook Publication Structure" |
| `OPS` | Common | Older standard abbreviation |
| `EPUB` | Sometimes | Publishers like simple names |
| `content` | Rare | Descriptive but non-standard |

**Solution:** Check `META-INF/container.xml` to find the actual folder name!

### EPUB Versions

- **EPUB 2.0:** Uses `toc.ncx` for navigation
- **EPUB 3.0:** Uses `nav.xhtml` (HTML5 navigation)
- **Hybrid:** Has both files for compatibility

**For translation:** Usually translate both navigation files if present.

### Chapter File Extensions

- `.xhtml` - Most common (EPUB 2 & 3)
- `.html` - Older or converted books
- `.xml` - Rare, but valid

**Solution:** Search for all: `find . -name "*.xhtml" -o -name "*.html" -o -name "*.xml"`

---

## File Encoding

EPUB files MUST use **UTF-8 encoding**. This is critical for international characters!

```xml
<?xml version="1.0" encoding="UTF-8"?>
```

**Why it matters:**
- Czech: á, č, ď, é, ě, í, ň, ó, ř, š, ť, ú, ů, ý, ž
- German: ä, ö, ü, ß
- French: à, â, é, è, ê, ë, î, ï, ô, ù, û, ü, ÿ
- Spanish: á, é, í, ñ, ó, ú, ü

UTF-8 handles ALL of these correctly. AI code assistants preserve UTF-8 automatically.

---

## Image and Media Handling

### Images

```xml
<img src="../Images/cover.jpg" alt="Book cover"/>
```

**Translation rule:** DON'T change image paths!

If the image contains text (like a map with labels), you might need to:
1. Extract image
2. Edit in image editor
3. Replace file (keep same filename)

### Fonts

EPUBs can embed custom fonts. Usually in:
- `OEBPS/Fonts/`
- Referenced in CSS

**Translation rule:** Leave fonts alone unless adding language-specific font (rare).

---

## Why ZIP Order Matters

**EPUB specification requires:**

```
1. mimetype (uncompressed)
2. META-INF/
3. Everything else
```

**Wrong order example:**
```
Archive: book.epub
  META-INF/container.xml
  mimetype                  ← TOO LATE!
  OEBPS/content.opf
```

**Result:** Many readers will reject this EPUB!

**Correct approach:**
```bash
# Step 1: Add mimetype FIRST with -0 (no compression)
zip -0 -X book.epub mimetype

# Step 2: Add everything else
zip -r book.epub META-INF OEBPS
```

The `-0` flag means "store only, don't compress".

---

## Language Codes Reference

### ISO 639-1 (Language) + ISO 3166-1 (Country)

| Language | Code | Example |
|----------|------|---------|
| English (UK) | `en-GB` | British spelling |
| English (US) | `en-US` | American spelling |
| Czech | `cs-CZ` | Čeština |
| German | `de-DE` | Deutsch |
| French | `fr-FR` | Français |
| Spanish (Spain) | `es-ES` | Español |
| Spanish (Latin America) | `es-MX` | Mexico variant |
| Italian | `it-IT` | Italiano |
| Polish | `pl-PL` | Polski |
| Russian | `ru-RU` | Русский |
| Japanese | `ja-JP` | 日本語 |
| Chinese (Simplified) | `zh-CN` | 简体中文 |
| Chinese (Traditional) | `zh-TW` | 繁體中文 |

**Where to update:**
- `content.opf`: `<dc:language>` element
- All XHTML files: `<html xml:lang="...">` attribute

---

## Real-World Example

**Book:** Baneblade by Guy Haley (Warhammer 40,000 novel)

**Stats:**
- Original size: 1.2 MB
- Pages: ~300
- Chapters: 31
- Total XHTML files: 51 (chapters + metadata + legal)
- Files translated: 34 (31 chapters + 3 metadata)
- Files skipped: 17 (copyright, promotional)

**Translation time:**
- Manual (estimated): 40-60 hours
- With AI assistant: ~2 hours
- Speedup: **20-30x faster**

**Quality:**
- All proper names preserved (Cortein, Baneblade, Mars Triumphant)
- Technical terms kept (lascannon, vox, augur)
- Formatting intact (italics, bold, paragraph structure)
- Navigation working (clickable TOC)

---

## Technical Constraints

### What AI Can Do

✅ Translate natural language text
✅ Preserve HTML/XML structure
✅ Maintain CSS classes and IDs
✅ Detect and preserve proper names
✅ Handle batch processing
✅ Validate output structure

### What AI Can't Do (without help)

❌ Translate text embedded in images
❌ Handle DRM-protected EPUBs
❌ Change book cover graphics
❌ Modify CSS styling (unless instructed)
❌ Guess which proper names to preserve (needs guidance)

---

## Validation Methods

### 1. ZIP Integrity

```bash
unzip -t book.epub
```

Output should be:
```
Archive:  book.epub
    testing: mimetype                 OK
    testing: META-INF/                OK
    testing: META-INF/container.xml   OK
    ...
No errors detected in compressed data of book.epub.
```

### 2. XML Validation

```bash
xmllint --noout OEBPS/content.opf
xmllint --noout OEBPS/toc.ncx
```

No output = valid XML!

### 3. EPUBCheck (Optional)

Official EPUB validator:

```bash
java -jar epubcheck.jar book.epub
```

Checks:
- File structure
- Metadata validity
- Broken links
- Accessibility

Download: https://github.com/w3c/epubcheck

### 4. Reader Test

Open in actual EPUB reader:
- **macOS:** Books.app
- **Windows:** Calibre, Adobe Digital Editions
- **Linux:** Calibre, FBReader
- **iOS:** Apple Books
- **Android:** Google Play Books

**Check:**
- Cover displays
- TOC works (clicking chapters navigates correctly)
- Text is translated
- Images display
- Formatting preserved (bold, italic)

---

## Troubleshooting Common Issues

### Issue: Can't Open EPUB

**Likely cause:** Mimetype not first or compressed

**Fix:**
```bash
# Rebuild with correct order
cd workspace/
rm -f ../book.epub
zip -0 -X ../book.epub mimetype
zip -r ../book.epub META-INF OEBPS
```

### Issue: Broken Table of Contents

**Likely cause:** Changed file paths in `toc.ncx`

**Fix:** Verify `<content src="...">` attributes match actual filenames

### Issue: Images Missing

**Likely cause:** Image paths changed during translation

**Fix:** Check `<img src="...">` paths weren't modified

### Issue: Formatting Lost

**Likely cause:** HTML tags removed or modified

**Fix:** Compare translated file structure to original, ensure tags match

---

## Advanced Topics

### Handling Footnotes

Footnotes use `<a>` tags with anchors:

```xml
<p>This is a sentence.<a href="#footnote1" id="ref1">1</a></p>

<!-- Later in file -->
<div class="footnotes">
    <p id="footnote1">
        <a href="#ref1">1.</a> This is the footnote text.
    </p>
</div>
```

**Translation:**
- Translate the footnote text
- Keep `href` and `id` attributes unchanged

### Poetry and Special Formatting

```xml
<div class="poem">
    <p class="stanza">
        Roses are red,<br/>
        Violets are blue,<br/>
        EPUBs are cool,<br/>
        And so are you.
    </p>
</div>
```

**Translation:**
- Translate the verses
- Preserve `<br/>` tags for line breaks
- Keep CSS classes for styling

### Multiple Languages in Same Book

Some books have mixed languages:

```xml
<p>He said "<span xml:lang="fr-FR">Bonjour</span>" to the shopkeeper.</p>
```

**Translation approach:**
- Translate the English parts
- Keep the French `<span>` as-is
- Preserve `xml:lang` attributes

---

## Performance Optimization

### Parallel Translation

**Single chapter:** ~5-10 minutes
**Sequential (31 chapters):** ~3-5 hours
**Parallel (5 chapters at once):** ~1-2 hours

Use AI subagents to translate multiple chapters simultaneously!

### Context Management

Long chapters might exceed AI context limits:

**Solutions:**
1. Split very long chapters into sections
2. Use AI with larger context windows
3. Process chapter in chunks (first half, second half)

### Cost Estimation

**Claude Sonnet 4.5:**
- Input: $3 per million tokens
- Output: $15 per million tokens

**Average chapter:**
- Input: ~8,000 tokens (reading XHTML)
- Output: ~10,000 tokens (writing translation)
- Cost: ~$0.15 per chapter

**Full book (31 chapters):** ~$5-10

---

## Further Reading

**EPUB Specifications:**
- EPUB 3.3: https://www.w3.org/TR/epub-33/
- EPUB 2.0: http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm

**Validation Tools:**
- EPUBCheck: https://github.com/w3c/epubcheck
- EPUB Validator (online): http://validator.idpf.org/

**EPUB Editors:**
- Sigil (free, open source): https://sigil-ebook.com/
- Calibre (free, library + editor): https://calibre-ebook.com/

**XML/XHTML:**
- XML Specification: https://www.w3.org/XML/
- XHTML1: https://www.w3.org/TR/xhtml1/

---

## Summary

**What you learned:**

1. EPUB = ZIP archive with HTML/XML files
2. Translation preserves structure, changes text only
3. Critical: mimetype must be first and uncompressed
4. Update language codes in metadata
5. AI code assistants automate the tedious parts
6. Validation ensures quality output

**Why it works:**

- AI understands HTML structure
- AI has language context
- AI can follow preservation rules
- Batch processing speeds up workflow

**Next steps:**

- Try translating a small EPUB first
- Use prompt templates or Claude Skill
- Validate output thoroughly
- Share your results!

---

*Happy translating!* 📚✨
