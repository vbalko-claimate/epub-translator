# Prompt 1: Setup Workspace

**For:** All AI assistants (Claude, Gemini, Cursor, GitHub Copilot, etc.)

Copy the text below and paste it into your AI assistant. Replace `[FILENAME.epub]`, `[SOURCE_LANG]`, and `[TARGET_LANG]` with your actual values.

---

## Prompt Text (Copy from here)

```
I need to translate an EPUB book from [SOURCE_LANG] to [TARGET_LANG].

**File:** [FILENAME.epub]

Please help me set up a workspace and identify the structure.

### Tasks:

1. **Create workspace directories:**
   ```bash
   mkdir -p epub_workspace/{original,translated,temp}
   ```

2. **Extract the EPUB** (it's a ZIP archive):
   ```bash
   unzip [FILENAME.epub] -d epub_workspace/original/
   ```

3. **Create working copy:**
   ```bash
   cp -r epub_workspace/original/* epub_workspace/translated/
   ```

4. **Identify the structure:**
   - Find chapter files (usually in `OEBPS/*.xhtml` or similar)
   - Locate `content.opf` (metadata file)
   - Locate `toc.ncx` (navigation file)
   - Find any Table of Contents XHTML file

5. **Analyze content:**
   - How many chapter files are there?
   - What's the file naming pattern? (chapter-1.xhtml, content-2.xhtml, etc.)
   - Are there files like "About the Author", "Prologue", "Epilogue"?
   - List all files that need translation

After extraction and analysis, show me:
- Complete list of chapter files to translate
- Location of metadata files (content.opf, toc.ncx)
- Any special files (TOC, author bio, etc.)
- Recommended translation order

**IMPORTANT:** We need to preserve:
- All HTML/XML structure
- CSS styling
- Images and media files
- Proper names and technical terms (we'll discuss which ones)
```

---

## Example Usage

**User Input:**
```
I need to translate an EPUB book from English to Czech.

File: baneblade.epub

[rest of prompt...]
```

**Expected AI Response:**
The AI should:
1. Execute the bash commands to extract the EPUB
2. Explore the directory structure
3. List all chapter files found
4. Identify metadata files
5. Provide a summary of what needs to be translated

## What This Accomplishes

- ✅ Creates organized workspace
- ✅ Preserves original file (backup)
- ✅ Identifies all translatable content
- ✅ Maps out the translation workflow
- ✅ Ready to start translating

## Next Step

After this prompt completes successfully, move to:
**→ [02-identify-chapters.md](02-identify-chapters.md)**
