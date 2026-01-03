# Example Translation Session

**Step-by-step walkthrough of translating a small EPUB book**

This transcript shows a complete translation session using the universal prompt templates.
Works with ANY AI code assistant (Claude Code, Claude.ai, Gemini, Cursor, etc.).

---

## Book Details

- **Title:** The Little Prince (Le Petit Prince)
- **Author:** Antoine de Saint-Exupéry
- **Original:** French
- **Source for this demo:** English edition
- **Target:** Spanish
- **Chapters:** 27 short chapters
- **Time:** ~2 hours

---

## Session Start

**User:**
```
I have an EPUB book called "little-prince.epub" and I want to translate it
from English to Spanish. Can you help me?
```

**AI Assistant:**
```
I'd be happy to help you translate the EPUB! Let's start by extracting and
analyzing the book structure. I'll need to:

1. Extract the EPUB (it's a ZIP archive)
2. Identify the chapter files
3. Set up a workspace
4. Translate the content
5. Rebuild the EPUB

Let me begin by extracting the EPUB.
```

---

## Step 1: Workspace Setup (5 minutes)

**AI Assistant:**
```bash
# Create workspace directories
mkdir -p epub_workspace/{original,translated,temp}

# Extract EPUB to original folder
unzip little-prince.epub -d epub_workspace/original/

# Copy to translated folder (working copy)
cp -r epub_workspace/original/* epub_workspace/translated/

# Analyze structure
find epub_workspace/translated -name "*.xhtml" | sort
```

**Output:**
```
epub_workspace/translated/OEBPS/Text/
├── cover.xhtml
├── titlepage.xhtml
├── chapter-01.xhtml
├── chapter-02.xhtml
├── chapter-03.xhtml
├── ... (chapters 04-26)
├── chapter-27.xhtml
├── about.xhtml
└── copyright.xhtml
```

**AI Assistant:**
```
I found 31 XHTML files total:
- 27 chapter files (chapter-01.xhtml through chapter-27.xhtml)
- 1 cover file (skip - just an image)
- 1 title page (optional to translate)
- 1 about page (author bio - should translate)
- 1 copyright page (skip - legal text)

We'll translate:
✓ 27 chapters
✓ About the Author page
✓ Optionally: Title page

Skip:
✗ Cover
✗ Copyright

Ready to proceed? I'll need you to tell me about any proper names to preserve.
```

**User:**
```
Yes, let's proceed. The main character is "the little prince" (el principito in Spanish).
Other characters: "the fox" (el zorro), "the rose" (la rosa), "the snake" (la serpiente).
Keep the author name "Antoine de Saint-Exupéry" as is.
Planet names like "Asteroid B-612" should stay in English.
```

---

## Step 2: First Chapter Translation (10 minutes)

**User:**
```
Let's translate the first chapter as a test. The file is:
epub_workspace/translated/OEBPS/Text/chapter-01.xhtml
```

**AI Assistant:**
```
I'll translate Chapter 1 from English to Spanish now.

Reading the file...
```

**File content (excerpt):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
    <title>Chapter 1</title>
    <link rel="stylesheet" href="../Styles/style.css"/>
</head>
<body>
    <h1>Chapter 1</h1>

    <p class="first">Once when I was six years old I saw a magnificent picture
    in a book about the primeval forest called <em>True Stories</em>.</p>

    <p>It showed a boa constrictor swallowing an animal. Here is a copy of
    the drawing:</p>

    <div class="image">
        <img src="../Images/boa-eating.jpg" alt="Boa eating"/>
    </div>
</body>
</html>
```

**AI Assistant:**
```
Translating now... Here's the translated version:
```

**Translated file:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es-ES">
<head>
    <title>Capítulo 1</title>
    <link rel="stylesheet" href="../Styles/style.css"/>
</head>
<body>
    <h1>Capítulo 1</h1>

    <p class="first">Una vez, cuando tenía seis años, vi una imagen magnífica
    en un libro sobre la selva virgen llamado <em>Historias Verdaderas</em>.</p>

    <p>Mostraba una boa constrictora tragándose un animal. Aquí está una copia
    del dibujo:</p>

    <div class="image">
        <img src="../Images/boa-eating.jpg" alt="Boa comiendo"/>
    </div>
</body>
</html>
```

**AI Assistant:**
```
Changes made:
✓ "Chapter 1" → "Capítulo 1"
✓ xml:lang="en" → xml:lang="es-ES"
✓ Translated narrative text to Spanish
✓ Preserved HTML structure (all tags, classes, IDs)
✓ Image path unchanged: "../Images/boa-eating.jpg"
✓ Alt text translated: "Boa eating" → "Boa comiendo"
✓ CSS link preserved

File written back to: epub_workspace/translated/OEBPS/Text/chapter-01.xhtml

Shall I continue with the remaining 26 chapters?
```

**User:**
```
Yes! Can you translate chapters 2-10 in parallel to save time?
```

---

## Step 3: Batch Translation (1 hour)

**AI Assistant:**
```
I'll use the Task tool to launch multiple translation agents in parallel.
This will translate chapters 2-10 simultaneously.

Launching agents...
```

**Agent 1:** Translating chapters 2-4
**Agent 2:** Translating chapters 5-7
**Agent 3:** Translating chapters 8-10

```
All agents completed successfully!

Progress: 10/27 chapters translated

Shall I continue with chapters 11-27?
```

**User:**
```
Yes, continue with the rest!
```

**AI Assistant:**
```
Launching agents for chapters 11-27...
```

**Agent 4:** Translating chapters 11-15
**Agent 5:** Translating chapters 16-20
**Agent 6:** Translating chapters 21-25
**Agent 7:** Translating chapters 26-27

```
All chapters translated! ✓

Progress: 27/27 chapters complete

Now let's translate the metadata files.
```

---

## Step 4: Metadata Translation (15 minutes)

### About the Author

**AI Assistant:**
```
Reading epub_workspace/translated/OEBPS/Text/about.xhtml...
```

**Original:**
```xml
<h1>About the Author</h1>

<p><strong>Antoine de Saint-Exupéry</strong> (1900-1944) was a French
writer and aviator. He is best known for his novella <em>The Little Prince</em>
and for his lyrical aviation writings.</p>

<p>Saint-Exupéry was a successful commercial pilot before World War II.
During the war, he joined the Free French Forces. He disappeared during a
reconnaissance mission in 1944.</p>
```

**Translated:**
```xml
<h1>Sobre el Autor</h1>

<p><strong>Antoine de Saint-Exupéry</strong> (1900-1944) fue un
escritor y aviador francés. Es más conocido por su novela corta
<em>El Principito</em> y por sus escritos líricos sobre aviación.</p>

<p>Saint-Exupéry fue un exitoso piloto comercial antes de la Segunda
Guerra Mundial. Durante la guerra, se unió a las Fuerzas Francesas Libres.
Desapareció durante una misión de reconocimiento en 1944.</p>
```

**AI Assistant:**
```
Changes:
✓ "About the Author" → "Sobre el Autor"
✓ Author name PRESERVED: "Antoine de Saint-Exupéry"
✓ "The Little Prince" → "El Principito"
✓ Biographical text translated
✓ xml:lang updated to "es-ES"

File saved!
```

### Table of Contents

**AI Assistant:**
```
Reading epub_workspace/translated/OEBPS/Text/toc.xhtml...

Translating navigation labels...
```

**Original:**
```xml
<nav epub:type="toc">
    <h1>Contents</h1>
    <ol>
        <li><a href="chapter-01.xhtml">Chapter 1</a></li>
        <li><a href="chapter-02.xhtml">Chapter 2</a></li>
        <li><a href="chapter-03.xhtml">Chapter 3</a></li>
        <!-- ... -->
        <li><a href="chapter-27.xhtml">Chapter 27</a></li>
    </ol>
</nav>
```

**Translated:**
```xml
<nav epub:type="toc">
    <h1>Contenido</h1>
    <ol>
        <li><a href="chapter-01.xhtml">Capítulo 1</a></li>
        <li><a href="chapter-02.xhtml">Capítulo 2</a></li>
        <li><a href="chapter-03.xhtml">Capítulo 3</a></li>
        <!-- ... -->
        <li><a href="chapter-27.xhtml">Capítulo 27</a></li>
    </ol>
</nav>
```

**AI Assistant:**
```
Changes:
✓ "Contents" → "Contenido"
✓ "Chapter X" → "Capítulo X" (all 27 entries)
✓ href attributes PRESERVED (links unchanged!)
✓ xml:lang updated

Metadata translation complete!
```

---

## Step 5: Configuration Update (10 minutes)

**AI Assistant:**
```
Now I need to update the language codes in the EPUB configuration files.

Updating content.opf...
```

**File: epub_workspace/translated/OEBPS/content.opf**

**Before:**
```xml
<metadata>
    <dc:title>The Little Prince</dc:title>
    <dc:creator>Antoine de Saint-Exupéry</dc:creator>
    <dc:language>en</dc:language>
    <dc:publisher>Public Domain</dc:publisher>
</metadata>
```

**After:**
```xml
<metadata>
    <dc:title>El Principito</dc:title>
    <dc:creator>Antoine de Saint-Exupéry</dc:creator>
    <dc:language>es-ES</dc:language>
    <dc:publisher>Public Domain</dc:publisher>
</metadata>
```

**AI Assistant:**
```
Changes to content.opf:
✓ <dc:language>en</dc:language> → <dc:language>es-ES</dc:language>
✓ <dc:title> translated (optional): "The Little Prince" → "El Principito"
✓ Author name preserved

Updating toc.ncx navigation file...
```

**File: epub_workspace/translated/OEBPS/toc.ncx**

**Before:**
```xml
<navMap>
    <navPoint id="ch01" playOrder="1">
        <navLabel><text>Chapter 1</text></navLabel>
        <content src="Text/chapter-01.xhtml"/>
    </navPoint>
    <!-- ... more chapters ... -->
</navMap>
```

**After:**
```xml
<navMap>
    <navPoint id="ch01" playOrder="1">
        <navLabel><text>Capítulo 1</text></navLabel>
        <content src="Text/chapter-01.xhtml"/>
    </navPoint>
    <!-- ... more chapters ... -->
</navMap>
```

**AI Assistant:**
```
Changes to toc.ncx:
✓ Navigation labels translated: "Chapter" → "Capítulo"
✓ File paths PRESERVED (src attributes unchanged)
✓ IDs and playOrder preserved

Configuration update complete!
```

---

## Step 6: Rebuild EPUB (5 minutes)

**AI Assistant:**
```
Now I'll rebuild the EPUB with the translated content.

Important: EPUB requires:
1. mimetype file MUST be first
2. mimetype file MUST be uncompressed

Executing rebuild commands...
```

```bash
# Navigate to translated directory
cd epub_workspace/translated/

# Remove any existing output
rm -f ../../little-prince-spanish.epub

# Step 1: Add mimetype (UNCOMPRESSED, FIRST!)
zip -0 -X ../../little-prince-spanish.epub mimetype

# Step 2: Add META-INF
zip -r ../../little-prince-spanish.epub META-INF/

# Step 3: Add OEBPS (content folder)
zip -r ../../little-prince-spanish.epub OEBPS/

# Return to main directory
cd ../..
```

**Output:**
```
  adding: mimetype (stored 0%)
  adding: META-INF/ (stored 0%)
  adding: META-INF/container.xml (deflated 33%)
  adding: OEBPS/ (stored 0%)
  adding: OEBPS/content.opf (deflated 52%)
  adding: OEBPS/toc.ncx (deflated 64%)
  adding: OEBPS/Text/ (stored 0%)
  adding: OEBPS/Text/chapter-01.xhtml (deflated 58%)
  adding: OEBPS/Text/chapter-02.xhtml (deflated 61%)
  ... (25 more chapters)
  adding: OEBPS/Styles/style.css (deflated 45%)
  adding: OEBPS/Images/ (stored 0%)
  adding: OEBPS/Images/cover.jpg (deflated 2%)
  ...
```

**AI Assistant:**
```
EPUB rebuilt successfully!

Output file: little-prince-spanish.epub

Let me verify the integrity...
```

---

## Step 7: Validation (5 minutes)

**AI Assistant:**
```bash
# Test ZIP integrity
unzip -t little-prince-spanish.epub
```

**Output:**
```
Archive:  little-prince-spanish.epub
    testing: mimetype                 OK
    testing: META-INF/                OK
    testing: META-INF/container.xml   OK
    testing: OEBPS/                   OK
    testing: OEBPS/content.opf        OK
    testing: OEBPS/toc.ncx            OK
    testing: OEBPS/Text/chapter-01.xhtml  OK
    testing: OEBPS/Text/chapter-02.xhtml  OK
    ... (all files)
No errors detected in compressed data of little-prince-spanish.epub.
```

**AI Assistant:**
```
✓ ZIP integrity test PASSED

Checking file structure...
```

```bash
# Verify mimetype is first
unzip -l little-prince-spanish.epub | head -5
```

**Output:**
```
Archive:  little-prince-spanish.epub
  Length      Date    Time    Name
---------  ---------- -----   ----
       20  01-03-2026 14:32   mimetype
        0  01-03-2026 14:32   META-INF/
```

**AI Assistant:**
```
✓ mimetype is first file
✓ Correct order maintained

Comparing file sizes...
```

```bash
ls -lh little-prince*.epub
```

**Output:**
```
-rw-r--r--  1 user  staff   856K Jan  3 14:10 little-prince.epub
-rw-r--r--  1 user  staff   892K Jan  3 14:32 little-prince-spanish.epub
```

**AI Assistant:**
```
File sizes:
Original (English): 856 KB
Translated (Spanish): 892 KB

Slight increase is normal (Spanish text often longer than English).

All validation checks passed! ✓

The translated EPUB is ready to use.
```

---

## Step 8: Testing in Reader (5 minutes)

**User:**
```
Can you help me open it in a reader to test?
```

**AI Assistant:**
```
Sure! On macOS, you can open it in Apple Books:
```

```bash
open little-prince-spanish.epub
```

**What to check in the reader:**

1. **Cover displays** correctly
   - ✓ Cover image appears

2. **Table of Contents** works
   - ✓ Click "Capítulo 1" → navigates to Chapter 1
   - ✓ All 27 chapters listed as "Capítulo 1-27"

3. **Chapter text** is translated
   - ✓ Opening line: "Una vez, cuando tenía seis años..."
   - ✓ Proper Spanish grammar and syntax

4. **Proper names** preserved
   - ✓ "Antoine de Saint-Exupéry" not translated
   - ✓ "Asteroid B-612" stays in English

5. **Images** display
   - ✓ Boa eating illustration appears
   - ✓ All chapter illustrations intact

6. **Formatting** preserved
   - ✓ Bold, italic text maintained
   - ✓ Paragraph structure correct
   - ✓ Chapter headings styled properly

7. **Language** detected
   - ✓ Reader shows "Spanish" as book language
   - ✓ Dictionary lookup uses Spanish

**User:**
```
Everything looks perfect! The translation is great and the formatting is intact.
```

---

## Session Summary

**Total time:** ~2 hours

**Tasks completed:**
1. ✅ Extracted EPUB (5 min)
2. ✅ Analyzed structure (5 min)
3. ✅ Translated 27 chapters (1 hour with parallel processing)
4. ✅ Translated metadata (15 min)
5. ✅ Updated configuration (10 min)
6. ✅ Rebuilt EPUB (5 min)
7. ✅ Validated output (5 min)
8. ✅ Tested in reader (5 min)

**Files translated:** 29 (27 chapters + about + TOC)

**Quality:**
- Structure preservation: 100%
- Proper names preserved: 100%
- Formatting intact: 100%
- Translation quality: High (native-level Spanish)

**Cost:** ~$3-4 (using Claude API)

---

## Alternative Workflow: Using Claude Skill

If using Claude Code CLI with the EPUB Translator skill installed:

**User:**
```
translate this EPUB from English to Spanish: little-prince.epub
```

**Claude Code (with skill):**
```
I'll translate this EPUB for you!

Using EPUB Translator skill...

1. Extracting EPUB ✓
2. Identifying chapters (found 27) ✓
3. Translating chapters in parallel... ⏳
   - Chapters 1-9 ✓
   - Chapters 10-18 ✓
   - Chapters 19-27 ✓
4. Translating metadata ✓
5. Updating configuration ✓
6. Rebuilding EPUB ✓
7. Validating ✓

Done! Output: little-prince-spanish.epub

Translation summary:
- 27 chapters translated
- 2 metadata files updated
- Language: en → es-ES
- Time: ~30 minutes (with parallel processing)
- Quality: Validated ✓

Your translated EPUB is ready!
```

**Note:** Claude Skill automates the entire process, reducing time from ~2 hours to ~30 minutes!

---

## Tips for Your Own Translation

1. **Start with a test chapter** - Verify quality before translating all chapters

2. **Create a proper names list** - Write down characters, places, technical terms FIRST

3. **Use parallel processing** - Translate multiple chapters at once to save time

4. **Validate frequently** - Check structure after every 10 chapters, don't wait until the end

5. **Test in multiple readers** - Try Apple Books, Calibre, Adobe Digital Editions

6. **Keep original workspace** - Don't delete the extracted files, they're your backup

7. **Document your decisions** - Note why you translated certain terms a specific way

8. **Post-edit if needed** - AI is 95% accurate, quick review catches the last 5%

---

## Common Questions

**Q: Can I translate to multiple languages at once?**

A: Yes! Create separate workspaces:
```bash
epub_workspace_spanish/
epub_workspace_french/
epub_workspace_german/
```

Translate each independently. Same source EPUB, different targets.

---

**Q: What if I find a mistake after rebuilding?**

A: Easy fix:
1. Navigate to `epub_workspace/translated/OEBPS/Text/`
2. Edit the XHTML file directly
3. Re-run the rebuild commands
4. New EPUB will have your corrections

---

**Q: Can I skip certain chapters?**

A: Absolutely! Just don't translate them. For example:
- Skip foreword/preface
- Skip promotional sections
- Only translate chapters you want

---

**Q: How do I share the translated EPUB?**

A: Important:
- ✅ Personal use: OK
- ✅ Share with friends/family: Usually OK (check local laws)
- ❌ Sell or publish commercially: Requires copyright permission
- ✅ Public domain books: Free to share

Always respect copyright!

---

## Next Steps

Now that you've seen the workflow, try it yourself!

**Beginner:** Start with a short story (~1 chapter)
**Intermediate:** Try a novel (10-30 chapters)
**Advanced:** Translate a technical book or series

**Resources:**
- [README.md](../README.md) - Main documentation
- [Prompt templates](../prompts/) - Copy-paste prompts for each step
- [How It Works](../docs/how-it-works.md) - EPUB technical details
- [Troubleshooting](../docs/troubleshooting.md) - Fix common issues

---

**Happy translating!** 📚✨

*Questions? Open an issue on GitHub!*
