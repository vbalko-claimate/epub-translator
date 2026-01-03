# Prompt 6: Rebuild EPUB

**For:** All AI assistants

Final step: Compile the translated files back into a valid EPUB archive.

---

## Prompt Text (Copy from here)

**Replace placeholder:**
- `[OUTPUT_NAME]` → desired filename (e.g., `baneblade_czech.epub`)

```
Compile the translated files back into an EPUB archive.

**Output:** `[OUTPUT_NAME].epub`

### Critical: EPUB is ZIP with Specific Structure

EPUB archives require:
1. **mimetype** file MUST be first
2. **mimetype** file MUST be uncompressed (ZIP level 0)
3. Everything else can be compressed normally

### Commands to Execute:

**Step 1: Navigate to translated directory**
```bash
cd epub_workspace/translated
```

**Step 2: Remove any existing output file**
```bash
rm -f ../../[OUTPUT_NAME].epub
```

**Step 3: Add mimetype (UNCOMPRESSED, must be first!)**
```bash
zip -0 -X ../../[OUTPUT_NAME].epub mimetype
```

**Explanation:**
- `-0` = No compression (store only)
- `-X` = Exclude extra file attributes
- Must be added FIRST before anything else

**Step 4: Add META-INF directory**
```bash
zip -r ../../[OUTPUT_NAME].epub META-INF/
```

**Step 5: Add content directory (usually OEBPS)**
```bash
zip -r ../../[OUTPUT_NAME].epub OEBPS/
```

**Note:** If your content folder has a different name (EPUB, OPS, content), use that instead of OEBPS.

**Step 6: Return to main directory**
```bash
cd ../..
```

**Step 7: Verify the EPUB**
```bash
# Test ZIP integrity
unzip -t [OUTPUT_NAME].epub

# Show first 10 files
unzip -l [OUTPUT_NAME].epub | head -15
```

### Expected Output:

```
Archive:  baneblade_czech.epub
    testing: mimetype                 OK
    testing: META-INF/                OK
    testing: META-INF/container.xml   OK
    testing: OEBPS/                   OK
    testing: OEBPS/content.opf        OK
    testing: OEBPS/toc.ncx            OK
    testing: OEBPS/chapter-1.xhtml    OK
    ...
No errors detected in compressed data of baneblade_czech.epub.
```

**Good sign:** First file listed should be `mimetype`

### Verification Checklist:

- [ ] EPUB file created successfully
- [ ] ZIP integrity test passed
- [ ] `mimetype` is the first file
- [ ] File size is reasonable (similar to original)
- [ ] Can open in EPUB reader

### Test in Reader:

**macOS:**
```bash
open [OUTPUT_NAME].epub
```

**Windows:**
```bash
start [OUTPUT_NAME].epub
```

**Linux:**
```bash
xdg-open [OUTPUT_NAME].epub
```

Or use Calibre, Adobe Digital Editions, or any EPUB reader.

### What to Check in Reader:

1. **Cover displays** correctly
2. **Table of Contents** works
   - Click a chapter link
   - Should navigate to that chapter
3. **Chapter text** is translated
4. **Images** still display
5. **Formatting** preserved (bold, italic, etc.)
6. **Language** detected correctly (reader shows target language)

### If Something's Wrong:

**Problem:** Can't open EPUB
**Likely cause:** Incorrect ZIP structure (mimetype not first or compressed)
**Fix:** Redo Steps 3-5, ensuring mimetype is added first with `-0` flag

**Problem:** Table of Contents broken
**Likely cause:** toc.ncx not updated or has errors
**Fix:** Check that all `<content src="...">` links are correct

**Problem:** Missing chapters
**Likely cause:** Files weren't included in ZIP
**Fix:** Check that all XHTML files are in the OEBPS folder before zipping

**Problem:** Images don't display
**Likely cause:** Image paths changed during translation
**Fix:** Verify `<img src="...">` paths weren't modified

### Advanced Validation (Optional):

If you have EPUBCheck installed:
```bash
java -jar epubcheck.jar [OUTPUT_NAME].epub
```

This will catch any structural issues.

### Success!

If your EPUB:
- Opens in a reader
- Shows translated text
- Table of Contents works
- Images display

**You're done!** 🎉

Your translated EPUB is ready to read.
```

---

## Platform-Specific Notes

### macOS/Linux
The commands above work as-is. Make sure you have `zip` and `unzip` installed (usually pre-installed).

### Windows
Install zip/unzip via:
- Git Bash (comes with Git for Windows)
- WSL (Windows Subsystem for Linux)
- Or use 7-Zip with command-line interface

Windows PowerShell alternative:
```powershell
# Add mimetype uncompressed
Compress-Archive -Path "epub_workspace\translated\mimetype" -DestinationPath "output.zip" -CompressionLevel NoCompression

# Add other files (more complex, recommend using Git Bash instead)
```

## Troubleshooting

### ZIP Command Not Found
**Install zip:**
- Mac: `brew install zip` (if not present)
- Linux: `sudo apt-get install zip`
- Windows: Use Git Bash or WSL

### Permission Denied
```bash
chmod +x epub_workspace/translated/mimetype
```

### File Already Exists
Add `-f` to zip command to force:
```bash
zip -0 -X -f ../../output.epub mimetype
```

## Final Notes

**Backup original:** Always keep the original EPUB file. If something goes wrong, you can start over.

**Version control:** Consider numbering your outputs:
- `book_v1_czech.epub` (first attempt)
- `book_v2_czech_fixed.epub` (after corrections)

**Share your work:** If translating public domain books, consider sharing on:
- Project Gutenberg
- Archive.org
- Personal blog/website

---

**Congratulations!** You've successfully translated an EPUB book! 📚✨
