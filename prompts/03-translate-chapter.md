# Prompt 3: Translate Chapter

**For:** All AI assistants

Use this template for EACH chapter you want to translate. Repeat for every chapter file.

⚠️ **IMPORTANT - Context Management:**

Books can have 20-50+ chapters. Each chapter uses significant context (3,000-8,000 tokens). To avoid context overflow:

**Best practices:**
1. **Translate 1-2 chapters per conversation** - Don't try to do all 31 chapters in one session!
2. **Start new chat sessions** after every 5-10 chapters
3. **For AI with parallel processing** (Claude Code, Cursor): Open multiple sessions simultaneously
4. **Use separate browser tabs/windows** for different chapter batches

**Recommended workflow:**
- Session 1: Chapters 1-5
- Session 2: Chapters 6-10
- Session 3: Chapters 11-15
- Continue until done

This prevents "out of context" errors and maintains translation quality.

---

## Prompt Text (Copy from here)

**Replace these placeholders:**
- `[CHAPTER_FILE.xhtml]` → actual filename (e.g., `6-40k-Content-2.xhtml`)
- `[SOURCE_LANG]` → source language (e.g., `English`)
- `[TARGET_LANG]` → target language (e.g., `Czech`)
- `[SOURCE_LANG_CODE]` → code (e.g., `en-GB`)
- `[TARGET_LANG_CODE]` → code (e.g., `cs-CZ`)
- `[PROPER_NAMES]` → comma-separated list of names to preserve

```
Translate this EPUB chapter from [SOURCE_LANG] to [TARGET_LANG].

**File:** `epub_workspace/translated/OEBPS/[CHAPTER_FILE.xhtml]`

### Critical Rules:

1. **Read the XHTML file first** using your file reading capability

2. **Translate ONLY text content** inside these tags:
   - `<p>...</p>`
   - `<h1>...</h1>`, `<h2>...</h2>`, etc.
   - `<span>...</span>` (text only, not class names!)
   - `<div>...</div>` (text only)

3. **PRESERVE exactly as-is:**
   - ALL HTML/XML tags (`<p>`, `<span>`, `<div>`, etc.)
   - ALL attributes (`class="..."`, `id="..."`, etc.)
   - ALL CSS class names
   - ALL image paths (`<img src="...">`)
   - ALL anchor links (`<a href="...">`)

4. **Change language attribute:**
   - Find: `xml:lang="[SOURCE_LANG_CODE]"`
   - Replace with: `xml:lang="[TARGET_LANG_CODE]"`

5. **GLOSSARY RULES** (if using a glossary file):

   If you have a glossary file (recommended for consistency), follow these rules:

   **PRESERVE (never translate):**
   [List terms from your glossary marked as PRESERVE]
   Example: Cortein, Bannick, Baneblade, lascannon

   **TRANSLATE (always use these exact translations):**
   [List terms from glossary with their translations]
   Example: Chapter → Kapitola, Space Marine → Vesmírný mariňák

   **PRESERVE_WITH_GRAMMAR (keep word, apply target language grammar):**
   [List terms that keep the word but get case endings]
   Example: bolter → bolter/bolteru/bolterem (apply Czech cases)

   **CONTEXT-DEPENDENT:**
   [List terms that change based on usage]
   Example: "Chapter" → "Kapitola" in headings, "Řád" when referring to military organizations

   **OR if no glossary, use generic rules:**

   **DO NOT translate these proper names:**
   [PROPER_NAMES]

6. **DO translate:**
   - "Chapter X" → "[TARGET_LANG equivalent] X"
   - "Prologue" → "[TARGET_LANG equivalent]"
   - "Epilogue" → "[TARGET_LANG equivalent]"
   - All narrative text, dialogue, descriptions

7. **Preserve formatting:**
   - If text is in `<em>` or `<i>`, keep it italicized
   - If text is in `<strong>` or `<b>`, keep it bold
   - Maintain paragraph structure exactly

8. **Write the translated file back** to the same location

### Example:

**Before (English):**
```xml
<p class="Body-Text" id="para-5">
    <span class="character-name">John</span> walked through
    <span class="place">London</span> at midnight.
</p>
```

**After (Czech):**
```xml
<p class="Body-Text" id="para-5">
    <span class="character-name">John</span> procházel
    <span class="place">Londýnem</span> o půlnoci.
</p>
```

**Note:** "John" preserved (character name), "London" → "Londýnem" (real place, has Czech translation)

### Verification:

After translating, verify:
- [ ] File saved successfully
- [ ] All HTML tags intact
- [ ] No broken XML structure
- [ ] Proper names preserved
- [ ] Language code updated
```

---

## Tips for Efficient Translation

### Batch Processing

If your AI supports parallel processing, you can translate multiple chapters simultaneously:

1. Open multiple chat sessions
2. Use the same prompt template for each
3. Just change the filename for each chapter
4. Provide same list of proper names to all sessions

### Using Glossaries (Highly Recommended!)

For books with many proper names or to match official translations:

1. **Create glossary file** (or use community glossary):
   - See `glossaries/template.txt` for format
   - Pre-made glossaries: `glossaries/community/`
   - Example: `glossaries/community/warhammer40k-en-cs.json`

2. **Load glossary before translating:**
   ```
   Read glossary file: glossaries/my-book-en-cs.txt

   Apply these rules when translating chapters:
   - PRESERVE: [list from glossary]
   - TRANSLATE: [list with translations]
   - PRESERVE_WITH_GRAMMAR: [list]
   ```

3. **Use SAME glossary for ALL chapters** (consistency!)

4. **Benefits:**
   - ✅ Consistent terminology across all chapters
   - ✅ No need to repeat proper names list
   - ✅ Reusable for sequels
   - ✅ Match official translations

**See:** `../docs/glossary-system.md` for complete guide

### Progress Tracking

Keep a checklist:
```
Chapters Translated:
[x] Chapter 1 (6-40k-Content-2.xhtml)
[x] Chapter 2 (6-40k-Content-3.xhtml)
[ ] Chapter 3 (6-40k-Content-5.xhtml)
...

Glossary: Using glossaries/warhammer40k-en-cs.json
```

### Quality Check

After translating 5-10 chapters, do a spot check:
- Open one translated file
- Verify HTML structure is intact
- Check that proper names weren't translated
- Confirm language attribute was changed

## Common Issues

**Issue:** AI translates proper names
**Fix:** Be more explicit in the prompt:
```
CRITICAL: These are character names, do NOT translate:
- John (character, not the biblical name)
- Mars Triumphant (ship name)
- Emperor (title in this universe, keep as-is)
```

**Issue:** HTML tags get broken
**Fix:** Remind the AI:
```
IMPORTANT: Use the Edit tool or Write tool carefully.
Do NOT manually type the HTML - copy the exact structure.
Only change the text between tags.
```

## Next Steps

After translating all chapters:
**→ [04-translate-metadata.md](04-translate-metadata.md)** for TOC and metadata files
