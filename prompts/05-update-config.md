# Prompt 5: Update Configuration Files

**For:** All AI assistants

Update language codes in EPUB metadata and navigation files.

---

## Prompt Text (Copy from here)

**Replace placeholders:**
- `[SOURCE_CODE]` → e.g., `en-GB`, `en-US`
- `[TARGET_CODE]` → e.g., `cs-CZ`, `de-DE`, `fr-FR`

```
Update the EPUB configuration files to reflect the target language.

### File 1: content.opf (Package Document)

**Location:** `epub_workspace/translated/OEBPS/content.opf`

1. Read the file
2. Find the `<dc:language>` element(s)
3. Change from `[SOURCE_CODE]` to `[TARGET_CODE]`

**Example:**
```xml
<!-- Before -->
<dc:language>en-GB</dc:language>
<dc:language>en-US</dc:language>

<!-- After (for Czech translation) -->
<dc:language>cs-CZ</dc:language>
```

**Important:** There might be multiple `<dc:language>` tags. Replace ALL of them with a single target language code.

4. Save the file

### File 2: toc.ncx (Navigation Control)

**Location:** `epub_workspace/translated/OEBPS/toc.ncx`

1. Read the file
2. Find all `<navLabel><text>` elements
3. Translate the navigation labels:

**Pattern to find and replace:**

```xml
<!-- Prologue -->
<navLabel><text>Prologue</text></navLabel>
→
<navLabel><text>[TARGET equivalent]</text></navLabel>

<!-- Chapters -->
<navLabel><text>Chapter 1</text></navLabel>
→
<navLabel><text>[TARGET equivalent] 1</text></navLabel>

<!-- Epilogue -->
<navLabel><text>Epilogue</text></navLabel>
→
<navLabel><text>[TARGET equivalent]</text></navLabel>
```

**Common translations:**
- **Czech:**
  - Prologue → Prolog
  - Chapter → Kapitola
  - Epilogue → Epilog

- **German:**
  - Prologue → Prolog
  - Chapter → Kapitel
  - Epilogue → Epilog

- **French:**
  - Prologue → Prologue
  - Chapter → Chapitre
  - Epilogue → Épilogue

- **Spanish:**
  - Prologue → Prólogo
  - Chapter → Capítulo
  - Epilogue → Epílogo

4. **DO NOT change:**
   - `<content src="...">` attributes
   - `id` attributes
   - `playOrder` attributes
   - Any other navigation structure

5. Save the file

### Verification:

After updating both files, verify:
- [ ] content.opf has correct language code
- [ ] toc.ncx labels are translated
- [ ] All XML structure is intact
- [ ] Navigation still works (links unchanged)

### Test Command:

```bash
# Verify XML is still valid
xmllint --noout epub_workspace/translated/OEBPS/content.opf
xmllint --noout epub_workspace/translated/OEBPS/toc.ncx
```

If no errors, the files are valid XML!
```

---

## Language Code Reference

| Language | Code | Prologue | Chapter | Epilogue |
|----------|------|----------|---------|----------|
| English (UK) | en-GB | Prologue | Chapter | Epilogue |
| English (US) | en-US | Prologue | Chapter | Epilogue |
| Czech | cs-CZ | Prolog | Kapitola | Epilog |
| German | de-DE | Prolog | Kapitel | Epilog |
| French | fr-FR | Prologue | Chapitre | Épilogue |
| Spanish (Spain) | es-ES | Prólogo | Capítulo | Epílogo |
| Italian | it-IT | Prologo | Capitolo | Epilogo |
| Polish | pl-PL | Prolog | Rozdział | Epilog |
| Russian | ru-RU | Пролог | Глава | Эпилог |
| Japanese | ja-JP | プロローグ | 章 | エピローグ |

## Common Issues

**Issue:** Multiple language codes in content.opf
**Question:** Should I keep all of them?
**Answer:** No, replace with single target language code. EPUB readers use the first one anyway.

**Issue:** toc.ncx has custom chapter titles ("The Beginning", "Into Darkness")
**Question:** Should I translate these?
**Answer:** Yes! Translate custom titles just like regular chapter text.

**Issue:** Some chapters are numbered with Roman numerals (Chapter I, Chapter II)
**Question:** Keep Roman numerals?
**Answer:** Usually yes. Translate "Chapter" but keep "I", "II", "III", etc.

## Next Steps

After updating config files:
**→ [06-rebuild-epub.md](06-rebuild-epub.md)** to compile the translated EPUB
