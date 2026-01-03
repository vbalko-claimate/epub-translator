# Troubleshooting Guide

Common issues encountered during EPUB translation and how to fix them.

---

## Table of Contents

- [Extraction Issues](#extraction-issues)
- [Translation Problems](#translation-problems)
- [Rebuild Errors](#rebuild-errors)
- [Validation Failures](#validation-failures)
- [Reader Compatibility](#reader-compatibility)
- [File Structure Issues](#file-structure-issues)
- [Encoding Problems](#encoding-problems)
- [AI Assistant Specific](#ai-assistant-specific)

---

## Extraction Issues

### Error: "unzip: command not found"

**Platform:** macOS/Linux

**Cause:** ZIP utilities not installed (rare on macOS, more common on minimal Linux)

**Fix:**

**macOS:**
```bash
# unzip is pre-installed, check if Homebrew overrode it
which unzip
# Should show: /usr/bin/unzip

# If missing, reinstall via Homebrew
brew install unzip
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt-get update
sudo apt-get install unzip
```

**Linux (RedHat/CentOS):**
```bash
sudo yum install unzip
```

---

### Error: "Archive: book.epub End-of-central-directory signature not found"

**Cause:** File is corrupt or not actually an EPUB

**Diagnosis:**
```bash
# Check file type
file book.epub
# Should show: "Zip archive data"

# Check file size
ls -lh book.epub
# Should be > 0 bytes
```

**Fixes:**

1. **Re-download the EPUB** - file may have been corrupted during download

2. **Check if it's DRM-protected:**
   ```bash
   unzip -l book.epub | grep -i "rights\|drm\|encryption"
   ```
   If you see DRM-related files, the EPUB is protected and can't be extracted normally.

3. **Try alternative extraction:**
   ```bash
   # On macOS
   ditto -xk book.epub workspace/

   # On Linux
   7z x book.epub -o workspace/
   ```

---

### Extracted Files Show Weird Characters

**Cause:** Filename encoding issues (rare)

**Example:**
```
chapter-1.xhtml  ← OK
chap�ter-2.xhtml ← BAD
```

**Fix:**
```bash
# Extract with UTF-8 encoding
unzip -O UTF-8 book.epub -d workspace/

# On macOS, use:
ditto -xk book.epub workspace/
```

---

## Translation Problems

### AI Translates Proper Names

**Problem:** Character names like "John Smith" become "Jan Kovář" (Czech translation)

**Example:**
```xml
<!-- WRONG -->
<p><span class="character-name">Jan Kovář</span> walked into the room.</p>

<!-- CORRECT -->
<p><span class="character-name">John Smith</span> walked into the room.</p>
```

**Fix:**

Add explicit instructions to your prompt:

```
CRITICAL: DO NOT TRANSLATE these proper names:
- John Smith (character name, not a common person)
- Mars Triumphant (spaceship name)
- Emperor (title in this universe, capitalized)

These are FICTIONAL names specific to this book.
Keep them EXACTLY as written in the original.
```

**Prevention:** Create a list of proper names BEFORE translating:
1. Read first chapter
2. Note all character names, place names, ship names
3. Add to prompt template
4. Use same list for all chapters

---

### HTML Tags Got Broken

**Problem:** AI removed or modified HTML structure

**Example:**
```xml
<!-- ORIGINAL -->
<p class="first-paragraph">Text here.</p>

<!-- BROKEN -->
<p>Text here.</p>  ← Missing class attribute!

<!-- OR -->
Text here.  ← Missing <p> tag entirely!
```

**Diagnosis:**
```bash
# Compare structure
diff <(grep -o '<[^>]*>' workspace/original/OEBPS/chapter-1.xhtml) \
     <(grep -o '<[^>]*>' workspace/translated/OEBPS/chapter-1.xhtml)
```

**Fix:**

1. **Re-translate the chapter** with stricter instructions:
   ```
   CRITICAL: You MUST preserve the EXACT HTML structure.

   Do NOT:
   - Remove any HTML tags
   - Remove any attributes (class, id, etc.)
   - Change tag types (<p> to <div>, etc.)
   - Remove closing tags

   Only change the TEXT between tags.
   ```

2. **Manual fix** (if just one or two chapters):
   - Open original and translated files side-by-side
   - Copy the HTML structure from original
   - Paste translated text back into proper tags

---

### Language Attribute Not Changed

**Problem:** File still shows `xml:lang="en-GB"` instead of `xml:lang="cs-CZ"`

**Impact:** eBook readers might not display correct fonts or use wrong spell-checker

**Fix:**

**Single file:**
```bash
# Replace in-place (macOS)
sed -i '' 's/xml:lang="en-GB"/xml:lang="cs-CZ"/g' workspace/translated/OEBPS/chapter-1.xhtml

# Replace in-place (Linux)
sed -i 's/xml:lang="en-GB"/xml:lang="cs-CZ"/g' workspace/translated/OEBPS/chapter-1.xhtml
```

**All XHTML files:**
```bash
find workspace/translated -name "*.xhtml" -exec sed -i '' 's/xml:lang="en-GB"/xml:lang="cs-CZ"/g' {} \;
```

**Manual:** Search and replace in each file using your editor

---

### Special Characters Broken

**Problem:** Accented characters display as `Ã©` instead of `é`

**Cause:** File saved with wrong encoding (not UTF-8)

**Example:**
```
Good: "Café"
Bad:  "CafÃ©"
```

**Diagnosis:**
```bash
file -I workspace/translated/OEBPS/chapter-1.xhtml
# Should show: charset=utf-8
```

**Fix:**

1. **Re-save with UTF-8:**
   ```bash
   iconv -f ISO-8859-1 -t UTF-8 chapter-1.xhtml > chapter-1-fixed.xhtml
   mv chapter-1-fixed.xhtml chapter-1.xhtml
   ```

2. **Verify XML declaration:**
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   ```
   Make sure it says `UTF-8`, not `ISO-8859-1` or `ASCII`

3. **AI re-translation:** Ask AI to ensure UTF-8 encoding:
   ```
   When saving the translated file, ensure it uses UTF-8 encoding.
   The XML declaration must be:
   <?xml version="1.0" encoding="UTF-8"?>
   ```

---

### Inconsistent Terminology

**Problem:** Same term translated differently across chapters

**Example:**
- Chapter 1: "spaceship" → "kosmická loď"
- Chapter 5: "spaceship" → "vesmírná loď"
- Chapter 10: "spaceship" → "hvězdná loď"

**Fix:**

1. **Create a glossary** before translating:
   ```
   Official Translations:
   - spaceship → kosmická loď
   - laser cannon → laserové dělo
   - command deck → velitelský můstek
   ```

2. **Include in every chapter prompt:**
   ```
   Use these EXACT translations for technical terms:
   - "spaceship" MUST be translated as "kosmická loď" (not other variants)
   - "laser cannon" MUST be translated as "laserové dělo"
   ```

3. **Post-processing search/replace:**
   ```bash
   # Find inconsistencies
   grep -n "vesmírná loď\|hvězdná loď" workspace/translated/OEBPS/*.xhtml

   # Replace with standardized term
   find workspace/translated/OEBPS -name "*.xhtml" -exec sed -i '' 's/vesmírná loď/kosmická loď/g' {} \;
   ```

---

## Rebuild Errors

### Error: "zip error: Nothing to do!"

**Cause:** No mimetype file found, or running zip from wrong directory

**Diagnosis:**
```bash
# Check current directory
pwd
# Should be inside: workspace/translated/

# Check mimetype exists
ls -la mimetype
# Should show: -rw-r--r-- 1 user group 20 Jan 1 12:00 mimetype
```

**Fix:**
```bash
# Navigate to correct directory
cd workspace/translated/

# Verify mimetype exists and has correct content
cat mimetype
# Output should be exactly: application/epub+zip

# If missing, create it:
echo -n "application/epub+zip" > mimetype

# Try zip again
zip -0 -X ../../output.epub mimetype
```

---

### Error: "zip warning: name not matched"

**Cause:** Trying to add files/folders that don't exist

**Example:**
```bash
zip -r output.epub OEBPS/
# zip warning: name not matched: OEBPS/
```

**Diagnosis:**
```bash
# List actual folders
ls -la
# Check if OEBPS exists, or is it named differently (OPS, EPUB, content)?
```

**Fix:**

1. **Find the actual content folder:**
   ```bash
   find . -name "content.opf" -type f
   # Output: ./OPS/content.opf
   # So folder is "OPS", not "OEBPS"
   ```

2. **Use correct folder name:**
   ```bash
   zip -r ../../output.epub OPS/  # Not OEBPS!
   ```

3. **Or check container.xml:**
   ```bash
   cat META-INF/container.xml | grep full-path
   # Shows: full-path="OPS/content.opf"
   # Use: OPS
   ```

---

### EPUB File Size Too Large or Too Small

**Problem:** Translated EPUB is 10MB when original was 1MB (or vice versa)

**Diagnosis:**
```bash
# Compare sizes
ls -lh original.epub translated.epub
# original.epub:   1.2M
# translated.epub: 12M  ← Problem!

# Check compression
unzip -lv translated.epub | head -20
# Look at "Ratio" column - should be ~40-60% for text files
```

**Causes & Fixes:**

**Too large:**
1. **Mimetype compressed by mistake:**
   ```bash
   unzip -lv translated.epub | head -1
   # Check mimetype line - should show "Stored" not "Defl:N"
   ```
   Fix: Rebuild, ensuring mimetype uses `-0` flag

2. **Added unnecessary files:**
   ```bash
   unzip -l translated.epub | grep -E "\.DS_Store|thumbs.db|desktop.ini"
   ```
   Fix: Remove before zipping:
   ```bash
   find workspace/translated -name ".DS_Store" -delete
   ```

**Too small:**
1. **Missing files:**
   ```bash
   # Compare file counts
   unzip -l original.epub | wc -l
   unzip -l translated.epub | wc -l
   # Should be similar numbers
   ```
   Fix: Ensure all folders are included in zip command

---

### Error: "zip error: Invalid command arguments (short option 'X' not supported)"

**Cause:** Using wrong version of zip (Windows zip.exe vs Unix zip)

**Platform:** Windows (Git Bash / WSL conflict)

**Fix:**

**Git Bash:**
```bash
# Use Git Bash's zip
/usr/bin/zip -0 -X output.epub mimetype
```

**WSL:**
```bash
# Install proper zip
sudo apt-get install zip

# Use it
zip -0 -X output.epub mimetype
```

**PowerShell (alternative):**
```powershell
# Create EPUB using Compress-Archive (less reliable)
# Better: Use Git Bash or WSL
```

---

## Validation Failures

### Error: "unzip -t" Shows Errors

**Example output:**
```
Archive:  book.epub
    testing: mimetype                 OK
    testing: META-INF/container.xml   bad CRC 4a3b2c1d  (should be 9f8e7d6c)
```

**Cause:** File corrupted during zip process or transfer

**Fix:**

1. **Rebuild from scratch:**
   ```bash
   cd workspace/translated
   rm -f ../../output.epub
   zip -0 -X ../../output.epub mimetype
   zip -r ../../output.epub META-INF OEBPS
   ```

2. **Verify source files are intact:**
   ```bash
   xmllint --noout OEBPS/content.opf
   # Should output nothing if valid
   ```

3. **Try alternative zip:**
   ```bash
   # Use 7-Zip on Windows
   7z a -tzip -mx=0 output.epub mimetype
   7z a -tzip output.epub META-INF OEBPS
   ```

---

### EPUBCheck Errors

**Tool:** https://github.com/w3c/epubcheck

**Common errors:**

#### Error: "Mimetype file entry is missing or is not the first file"

**Fix:**
```bash
# Rebuild with correct order
cd workspace/translated
rm ../../output.epub
zip -0 -X ../../output.epub mimetype  # FIRST!
zip -r ../../output.epub META-INF OEBPS  # Then everything else
```

#### Error: "Mimetype contains wrong type"

**Check mimetype content:**
```bash
cat workspace/translated/mimetype
# Should be EXACTLY: application/epub+zip
# No newlines, no spaces!
```

**Fix:**
```bash
echo -n "application/epub+zip" > workspace/translated/mimetype
# The -n flag prevents adding a newline
```

#### Error: "OPF-002: Prefix must be declared"

**Cause:** Using custom namespace prefix without declaration

**Example problem:**
```xml
<meta property="custom:rating">5</meta>  ← "custom" not declared
```

**Fix:** Declare prefix in `<package>` tag:
```xml
<package ... prefix="custom: http://example.com/custom/">
```

Or remove custom metadata.

#### Error: "RSC-005: File not found"

**Cause:** Manifest references file that doesn't exist

**Example:**
```xml
<item id="chapter10" href="chapter-10.xhtml" .../>
```
But `chapter-10.xhtml` was deleted or renamed.

**Fix:**

1. **Find missing files:**
   ```bash
   # Extract manifest URLs
   grep 'href=' workspace/translated/OEBPS/content.opf | grep -o 'href="[^"]*"'
   ```

2. **Check if files exist:**
   ```bash
   # For each href, verify file exists
   ls workspace/translated/OEBPS/chapter-10.xhtml
   ```

3. **Remove from manifest** or **restore file**

---

## Reader Compatibility

### Can't Open EPUB in Apple Books (macOS/iOS)

**Symptoms:**
- Double-click does nothing
- "Cannot open file" error
- Book opens but shows blank pages

**Diagnosis:**
```bash
# Check file extension
file output.epub
# Should show: Zip archive data

# Test with epubcheck
java -jar epubcheck.jar output.epub
```

**Fixes:**

1. **Ensure .epub extension:**
   ```bash
   mv output.zip output.epub
   ```

2. **Fix mimetype issue** (most common):
   Rebuild ensuring mimetype is first and uncompressed

3. **Check XML validity:**
   ```bash
   xmllint --noout workspace/translated/OEBPS/*.xhtml
   # Any errors? Fix the XML
   ```

4. **Try alternative reader first:**
   ```bash
   # Test in Calibre
   open -a "calibre" output.epub

   # Or Adobe Digital Editions
   ```

---

### Table of Contents Doesn't Work

**Symptoms:**
- TOC displays but clicking chapters does nothing
- "Chapter 1" link goes to wrong page
- Some chapters missing from TOC

**Cause 1: Broken Links**

**Diagnosis:**
```bash
# Check toc.ncx
grep '<content src=' workspace/translated/OEBPS/toc.ncx

# Verify each file exists
ls workspace/translated/OEBPS/chapter-1.xhtml
```

**Fix:** Ensure `src` attributes point to real files

**Cause 2: Translated File Paths (WRONG!)**

**Example problem:**
```xml
<!-- ORIGINAL -->
<content src="chapter-1.xhtml"/>

<!-- WRONG - translated the filename! -->
<content src="kapitola-1.xhtml"/>
```

**Fix:** Change back to original filename:
```xml
<content src="chapter-1.xhtml"/>
```

**Cause 3: Anchor Links Broken**

**Example:**
```xml
<content src="chapter-1.xhtml#section2"/>
```
But `#section2` ID doesn't exist in the file.

**Fix:** Verify anchor exists:
```bash
grep 'id="section2"' workspace/translated/OEBPS/chapter-1.xhtml
```

---

### Images Don't Display

**Symptoms:**
- Broken image icons
- Alt text shows instead of image
- Some images work, others don't

**Diagnosis:**
```bash
# Check image paths in XHTML
grep '<img' workspace/translated/OEBPS/chapter-1.xhtml

# Verify images exist
ls workspace/translated/OEBPS/Images/
```

**Cause 1: Path Changed During Translation**

**Example:**
```xml
<!-- ORIGINAL -->
<img src="../Images/map.jpg" alt="Map"/>

<!-- WRONG - path translated! -->
<img src="../Obrázky/map.jpg" alt="Map"/>
```

**Fix:** Revert to original path:
```xml
<img src="../Images/map.jpg" alt="Map"/>
```

**Cause 2: Images Not Included in Manifest**

**Check manifest:**
```bash
grep 'map.jpg' workspace/translated/OEBPS/content.opf
```

If missing, add:
```xml
<item id="image-map" href="Images/map.jpg" media-type="image/jpeg"/>
```

**Cause 3: Images Not Zipped**

**Verify:**
```bash
unzip -l output.epub | grep -i images
```

If missing, re-zip including Images folder:
```bash
cd workspace/translated
zip -r ../../output.epub OEBPS/Images/
```

---

### Formatting Lost (No Bold/Italic)

**Symptoms:**
- All text appears plain
- No bold, italic, or special fonts
- Paragraphs run together

**Cause 1: CSS Not Linked**

**Check XHTML:**
```xml
<head>
    <link rel="stylesheet" href="../Styles/style.css"/>  ← This line!
</head>
```

**Fix:** Ensure CSS link is present and path is correct

**Cause 2: CSS File Missing**

**Verify:**
```bash
ls workspace/translated/OEBPS/Styles/style.css
unzip -l output.epub | grep style.css
```

**Fix:** Ensure CSS is included in zip:
```bash
zip -r output.epub OEBPS/Styles/
```

**Cause 3: HTML Tags Removed**

**Example:**
```xml
<!-- ORIGINAL -->
<p>He said <em>emphatically</em> that...</p>

<!-- BROKEN -->
<p>He said emphatically that...</p>  ← Lost <em> tag!
```

**Fix:** Re-translate chapter with strict structure preservation

---

## File Structure Issues

### META-INF/container.xml Points to Wrong Location

**Error in reader:** "Cannot find OPF file"

**Diagnosis:**
```bash
cat workspace/translated/META-INF/container.xml | grep full-path
# Shows: full-path="OEBPS/content.opf"

# But actual location is:
find workspace/translated -name content.opf
# Shows: workspace/translated/OPS/content.opf  ← Different folder!
```

**Fix:**

Edit `container.xml`:
```xml
<rootfile full-path="OPS/content.opf" media-type="application/oebps-package+xml"/>
```

---

### Duplicate IDs in Manifest

**EPUBCheck error:** "Duplicate ID 'chapter1'"

**Example:**
```xml
<manifest>
    <item id="chapter1" href="chapter-1.xhtml" .../>
    <item id="chapter1" href="prologue.xhtml" .../>  ← Same ID!
</manifest>
```

**Fix:** Make IDs unique:
```xml
<manifest>
    <item id="prologue" href="prologue.xhtml" .../>
    <item id="chapter1" href="chapter-1.xhtml" .../>
</manifest>
```

---

### Extra Files in EPUB

**Problem:** macOS .DS_Store or Windows thumbs.db in EPUB

**Diagnosis:**
```bash
unzip -l output.epub | grep -E "\.DS_Store|thumbs\.db|desktop\.ini"
```

**Prevention:**
```bash
# Clean before zipping
find workspace/translated -name ".DS_Store" -delete
find workspace/translated -name "thumbs.db" -delete
find workspace/translated -name "desktop.ini" -delete
```

**Fix existing EPUB:**
```bash
# Remove from archive
zip -d output.epub "*.DS_Store"
zip -d output.epub "*/thumbs.db"
```

---

## Encoding Problems

### UTF-8 BOM Issues

**Problem:** File has UTF-8 BOM (Byte Order Mark) causing parsing errors

**Diagnosis:**
```bash
hexdump -C workspace/translated/OEBPS/chapter-1.xhtml | head -1
# If starts with "ef bb bf" → UTF-8 BOM present
```

**Fix:**
```bash
# Remove BOM
sed -i '1s/^\xEF\xBB\xBF//' workspace/translated/OEBPS/chapter-1.xhtml

# Or use tail trick
tail -c +4 chapter-1.xhtml > chapter-1-nobom.xhtml
mv chapter-1-nobom.xhtml chapter-1.xhtml
```

---

### Mixed Encodings

**Problem:** Some files UTF-8, others ISO-8859-1

**Diagnosis:**
```bash
find workspace/translated -name "*.xhtml" -exec file -I {} \;
# Should all show: charset=utf-8
```

**Fix:**
```bash
# Convert all to UTF-8
find workspace/translated -name "*.xhtml" -exec sh -c '
    iconv -f ISO-8859-1 -t UTF-8 "$1" > "$1.tmp" && mv "$1.tmp" "$1"
' sh {} \;
```

---

## AI Assistant Specific

### Context Limit Reached / Out of Memory

**Error messages:**
- "Maximum context length exceeded"
- "Context window full"
- "I need to summarize our conversation"
- AI stops responding mid-translation
- Incomplete chapter outputs

**Cause:** Books are LARGE. A 300-page novel has:
- 31 chapters × 3,000-8,000 tokens/chapter = 93,000-248,000 tokens
- Most AI assistants have context limits:
  - Claude Sonnet: 200K tokens
  - Claude Haiku: 200K tokens
  - ChatGPT-4: 128K tokens
  - Gemini Pro: 32K tokens (older) / 1M tokens (newer)

**Solutions:**

**Solution 1: Use Subagents (Claude Code ONLY)**

If using Claude Code CLI, the skill AUTOMATICALLY handles this:
```bash
claude "translate book.epub from English to Czech"
```

The skill launches separate Task subagents for each chapter. Each subagent has its own fresh context, so no limit issues.

**Solution 2: Batch Processing (Manual Workflow)**

For web-based AI or other assistants:

**DON'T do this:**
```
Session 1: Translate all 31 chapters ❌
(You'll run out of context around chapter 10-15)
```

**DO this:**
```
Session 1 (new chat): Chapters 1-5 ✓
Session 2 (new chat): Chapters 6-10 ✓
Session 3 (new chat): Chapters 11-15 ✓
Session 4 (new chat): Chapters 16-20 ✓
Session 5 (new chat): Chapters 21-25 ✓
Session 6 (new chat): Chapters 26-31 ✓
```

Each session stays under context limits!

**Solution 3: Parallel Sessions**

Open **multiple browser tabs/windows** simultaneously:

- Tab 1: Translate chapters 1-5
- Tab 2: Translate chapters 6-10
- Tab 3: Translate chapters 11-15
- Tab 4: Translate chapters 16-20
- Tab 5: Translate chapters 21-25

All run in parallel → Finish in ~1-2 hours instead of 5-6 hours!

**Solution 4: Reduce Chapter Size**

For very long chapters (10,000+ words), split into sections:

```
Translate the FIRST HALF of chapter-15.xhtml:
- From beginning to <p id="mid-point">

Then in next message:
Translate the SECOND HALF of chapter-15.xhtml:
- From <p id="mid-point"> to end
```

**Solution 5: Use Larger Context Models**

If available:
- Claude Opus 4: 200K tokens
- Gemini 1.5 Pro: 1M tokens (can handle entire book!)
- GPT-4 Turbo: 128K tokens

Gemini 1.5 Pro with 1M context could theoretically translate entire book in one go!

**Prevention:**

Add this to your workflow:
```
Chapter translation checklist:
[ ] Chapters 1-5 (Session 1)
[ ] Chapters 6-10 (Session 2)
[ ] Chapters 11-15 (Session 3)
...

Mark sessions as complete to track progress across multiple chats.
```

**For Claude Code users:**

The skill handles this automatically! Just run:
```bash
claude "translate book.epub from English to Spanish"
```

And it will:
1. Launch 5-10 subagents in parallel
2. Each subagent translates 1-2 chapters
3. No context limits because each agent is independent
4. Finish in ~30-60 minutes

---

### Claude Code: "Tool blocked by hook"

**Error:** Pre-prompt hook or tool hook blocking file writes

**Fix:**

1. **Check hooks:**
   ```bash
   cat ~/.claude/settings/settings.json | grep -A5 hooks
   ```

2. **Temporarily disable:**
   Edit settings.json and comment out hooks

3. **Adjust hook permissions** for workspace directory

---

### Context Limit Reached

**Error:** "Maximum context length exceeded"

**Symptoms:**
- AI stops mid-translation
- Incomplete chapter output
- "I need to break this into smaller chunks" messages

**Solutions:**

1. **Translate in batches:**
   ```
   Translate chapters 1-5 first.
   Then chapters 6-10.
   Etc.
   ```

2. **Use smaller context per file:**
   - Don't include entire file analysis in each prompt
   - Just translate, don't summarize

3. **Switch to larger context model:**
   - Claude Opus (200K context)
   - GPT-4 Turbo (128K context)

---

### AI Keeps Adding Extra Explanations

**Problem:** AI adds comments or explanations to the XHTML

**Example:**
```xml
<p>Translated text here.</p>
<!-- Translated from: "Original text here" -->  ← AI added this!
```

**Fix:**

Add to prompt:
```
CRITICAL: Do NOT add any comments, explanations, or notes to the file.
Only write the translated XHTML with NO additional content.
The output file should contain ONLY the translated text and original structure.
```

---

## Platform-Specific Issues

### macOS: "Operation not permitted"

**Cause:** macOS file permission or SIP (System Integrity Protection)

**Fix:**
```bash
# Check permissions
ls -la workspace/

# Grant full disk access to Terminal:
# System Preferences → Security & Privacy → Full Disk Access → Add Terminal

# Or change ownership:
sudo chown -R $(whoami) workspace/
```

---

### Windows: Path Length Limit

**Error:** "The filename or extension is too long"

**Cause:** Windows 260-character path limit

**Fix:**

1. **Shorten workspace path:**
   ```bash
   # Bad:  C:\Users\VeryLongUsername\Documents\Projects\epub-translator\workspace\translated\
   # Good: C:\epub\workspace\translated\
   ```

2. **Enable long paths (Windows 10+):**
   - Group Policy: Enable "Enable Win32 long paths"
   - Or Registry:
     ```
     HKLM\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled = 1
     ```

---

### Linux: Permission Denied

**Cause:** Workspace created with root permissions

**Fix:**
```bash
# Check ownership
ls -la workspace/
# Should show your username, not root

# Fix ownership
sudo chown -R $(whoami):$(whoami) workspace/
```

---

## Emergency Recovery

### Start Over from Scratch

If everything is broken:

```bash
# 1. Backup current attempt
mv epub_workspace epub_workspace_backup_$(date +%Y%m%d)

# 2. Re-extract original EPUB
mkdir -p epub_workspace/{original,translated,temp}
unzip original.epub -d epub_workspace/original/
cp -r epub_workspace/original/* epub_workspace/translated/

# 3. Start translation again
# Use lessons learned from first attempt!
```

---

### Recover from Partial Translation

**Scenario:** Translated 15/31 chapters, then something broke

**Recovery:**

1. **Identify completed chapters:**
   ```bash
   # List translated files (check language attribute)
   grep -l 'xml:lang="cs-CZ"' workspace/translated/OEBPS/*.xhtml > done.txt
   ```

2. **List remaining:**
   ```bash
   # Files still showing English
   grep -l 'xml:lang="en-GB"' workspace/translated/OEBPS/*.xhtml > todo.txt
   ```

3. **Continue from where you left off:**
   - Translate files in todo.txt
   - Don't re-translate done.txt files

---

## Getting Help

If this guide doesn't solve your problem:

1. **Check EPUBCheck output:**
   ```bash
   java -jar epubcheck.jar output.epub > errors.txt 2>&1
   cat errors.txt
   ```
   Specific error codes are Google-able!

2. **Compare with original:**
   ```bash
   # Structure comparison
   diff -qr epub_workspace/original/OEBPS epub_workspace/translated/OEBPS
   ```

3. **Validate individual files:**
   ```bash
   xmllint --noout workspace/translated/OEBPS/content.opf
   xmllint --noout workspace/translated/OEBPS/toc.ncx
   xmllint --noout workspace/translated/OEBPS/chapter-1.xhtml
   ```

4. **GitHub Issues:**
   Report bugs or ask for help:
   https://github.com/[your-username]/epub-translator/issues

5. **EPUB Community:**
   - https://www.mobileread.com/forums/
   - EPUB subreddit: r/epub

---

## Prevention Checklist

Use this before each translation project:

- [ ] Backup original EPUB
- [ ] Test unzip on original (ensure not corrupt)
- [ ] Identify proper names BEFORE translating
- [ ] Create terminology glossary for consistency
- [ ] Translate 1-2 chapters first as test
- [ ] Validate test chapters before doing all 31
- [ ] Keep original workspace as reference
- [ ] Use version control (git) for translated files
- [ ] Test final EPUB in multiple readers

---

## Quick Reference: Common Fixes

| Problem | Quick Fix Command |
|---------|------------------|
| Mimetype wrong | `echo -n "application/epub+zip" > mimetype` |
| Wrong language code | `sed -i 's/en-GB/cs-CZ/g' *.xhtml` |
| Missing files in zip | `zip -r output.epub OEBPS/` |
| Extra .DS_Store | `find . -name ".DS_Store" -delete` |
| Broken XML | `xmllint --noout file.xhtml` (to diagnose) |
| Encoding wrong | `iconv -f ISO-8859-1 -t UTF-8 file > file.new` |
| EPUB won't open | Rebuild from scratch (see above) |

---

*When in doubt, start from a fresh extraction and translate systematically!* 🔧
