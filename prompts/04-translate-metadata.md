# Prompt 4: Translate Metadata Files

**For:** All AI assistants

Use this for translating Table of Contents, About the Author, and other metadata files.

---

## Prompt Text (Copy from here)

**Replace placeholders:**
- `[METADATA_FILE.xhtml]` → e.g., `3-TOC.xhtml` or `7-Guy-Haley.xhtml`
- `[SOURCE_LANG]` / `[TARGET_LANG]` → language names
- `[SOURCE_CODE]` / `[TARGET_CODE]` → language codes

```
Translate this EPUB metadata file from [SOURCE_LANG] to [TARGET_LANG].

**File:** `epub_workspace/translated/OEBPS/[METADATA_FILE.xhtml]`

### Type-Specific Instructions:

#### If Table of Contents (TOC):
1. Read the file
2. Translate chapter/section titles:
   - "Contents" → "[TARGET equivalent]"
   - "Prologue" → "[TARGET equivalent]"
   - "Chapter 1" → "[TARGET equivalent] 1"
   - "Epilogue" → "[TARGET equivalent]"
   - "About the Author" → "[TARGET equivalent]"
3. Keep all `<a href="...">` links unchanged
4. Preserve all HTML structure
5. Change `xml:lang="[SOURCE_CODE]"` to `xml:lang="[TARGET_CODE]"`

#### If About the Author:
1. Read the file
2. Translate biographical text
3. **DO NOT translate:**
   - Author's name
   - Book titles (keep in quotes, original language)
   - Publisher names
   - URLs
4. Translate headings ("About the Author" → target language)
5. Change language attribute

#### If Book Introduction/Legend:
1. Read the file
2. Translate descriptive text
3. **Preserve:**
   - Universe-specific terminology
   - Proper names
   - Made-up words (if part of the fiction)
4. Change language attribute

### Critical Rules:

- **Preserve ALL HTML/XML tags**
- **Keep ALL attributes and CSS classes**
- **Don't change image paths or links**
- **Update xml:lang attribute**
- **Write translated file back to same location**

### Example (TOC):

**Before (English):**
```xml
<p class="toc-entry">
    <a href="chapter-1.xhtml">Chapter 1</a>
</p>
<p class="toc-entry">
    <a href="chapter-2.xhtml">Chapter 2</a>
</p>
```

**After (Czech):**
```xml
<p class="toc-entry">
    <a href="chapter-1.xhtml">Kapitola 1</a>
</p>
<p class="toc-entry">
    <a href="chapter-2.xhtml">Kapitola 2</a>
</p>
```

**Note:** Only the display text changed, `href` attributes stayed the same!

### Verification:

- [ ] All links still point to correct files
- [ ] Chapter numbering is correct
- [ ] HTML structure unchanged
- [ ] Language attribute updated
```

---

## Common Metadata Files

### Table of Contents (TOC)
- Usually named: `3-TOC.xhtml`, `toc.xhtml`, `contents.xhtml`
- Contains: List of chapters with links
- Translate: Chapter titles, headings
- Keep: All `href` attributes

### About the Author
- Usually named: `author.xhtml`, `[author-name].xhtml`, `about.xhtml`
- Contains: Author biography
- Translate: Bio text
- Keep: Author name, book titles, URLs

### Introduction/Legend
- Genre-specific intro (e.g., "What is Warhammer 40,000?")
- Translate: Explanatory text
- Keep: Proper nouns, universe terminology

### Title Page
- Usually just has book title and author
- Translate: Only if translating the book title itself
- Otherwise: Just change `xml:lang` attribute

## Next Steps

After translating metadata files:
**→ [05-update-config.md](05-update-config.md)** to update language codes in config files
