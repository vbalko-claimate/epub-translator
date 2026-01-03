# PDF Translation - Step 2: Translate Pages

Translate extracted PDF pages using Claude Code Task subagents with glossary support.

**Prerequisites:**
- Completed Step 1 (extraction)
- Glossary file ready (optional but recommended)

---

## Prompt Text (Copy from here)

I need to translate the extracted PDF pages from [SOURCE_LANGUAGE] to [TARGET_LANGUAGE].

**Extracted pages:** `pdf_workspace/extracted/page_001.json` to `page_NNN.json`
**Glossary:** `glossaries/[YOUR_GLOSSARY].json` (if applicable)

## Step 2: Translate Pages

Please help me translate the extracted pages using Task subagents for parallel processing.

### What to do:

1. **Generate subagent prompt (optional helper):**
   ```bash
   cd ~/.claude/skills/epub-translator/scripts/pdf
   python translate_pdf.py --generate-prompt \
     --pages 1-10 \
     --source en \
     --target cs \
     --glossary warhammer40k-en-cs.json
   ```

   This outputs a ready-to-use prompt for the Task tool.

2. **Or manually create Task subagents:**

   Split pages into batches (5-10 pages per subagent for optimal performance):
   - Batch 1: Pages 1-10
   - Batch 2: Pages 11-20
   - Batch 3: Pages 21-30
   - etc.

3. **For each batch, use Task tool with this prompt:**

```
Translate PDF pages [START]-[END] from [SOURCE_LANG] to [TARGET_LANG].

FILES TO TRANSLATE:
  - pdf_workspace/extracted/page_001.json
  - pdf_workspace/extracted/page_002.json
  - ... (list all pages in batch)

OUTPUT DIRECTORY: pdf_workspace/translated/

WORKFLOW:

1. For each page JSON file:
   a) Use Read tool to load: pdf_workspace/extracted/page_XXX.json
   b) For each block in "blocks" array:
      - Read the "text" field
      - Translate it from [SOURCE_LANG] to [TARGET_LANG]
      - Apply glossary rules (see below)
      - Check if translated text is longer than original (overflow detection)
      - Add two new fields:
        * "original_text": original text
        * "translated_text": your translation
      - If overflow >10%, add:
        * "overflow_warning": true
        * "suggested_size": reduced font size
   c) Use Write tool to save: pdf_workspace/translated/page_XXX.json

2. Skip translation for blocks where type is "header" or "footer" (copy text as-is)

3. Preserve ALL metadata: bbox, font, size, flags, color, type

GLOSSARY RULES:

[If using glossary, paste rules here - use translate_pdf.py --generate-prompt to auto-generate this section]

PRESERVE (never translate):
  - Baneblade
  - Cortein
  - Leman Russ
  - (etc.)

TRANSLATE (use exact translations):
  - Chapter → Kapitola
  - Space Marines → Vesmírní mariňáci
  - (etc.)

PRESERVE_WITH_GRAMMAR (keep word, apply Czech grammar):
  - bolter → bolter/bolteru/bolterem
  - (etc.)

OVERFLOW DETECTION:

For each block, estimate if translated text will fit in bbox:

```python
original_width = bbox[2] - bbox[0]  # bbox is [x0, y0, x1, y1]
font_size = block["size"]

# Rough character width estimation
original_estimated = len(original_text) * font_size * 0.5
translated_estimated = len(translated_text) * font_size * 0.5

if translated_estimated > original_width * 1.1:  # 10% overflow threshold
    block["overflow_warning"] = true
    # Suggest reduced font size (maintain aspect ratio)
    block["suggested_size"] = font_size * (original_width / translated_estimated) * 0.95
```

JSON OUTPUT FORMAT:

Preserve exact structure, add translation fields:

```json
{
  "page_num": 1,
  "width": 595.32,
  "height": 841.92,
  "blocks": [
    {
      "text": "Chapter 1",
      "original_text": "Chapter 1",
      "translated_text": "Kapitola 1",
      "bbox": [72.0, 100.0, 200.0, 120.0],
      "font": "Times-Bold",
      "size": 18.0,
      "flags": 16,
      "color": 0,
      "type": "heading",
      "overflow_warning": false
    },
    {
      "text": "The battle raged across the frozen wastes of Kalidar IV.",
      "original_text": "The battle raged across the frozen wastes of Kalidar IV.",
      "translated_text": "Bitva zuřila přes zmrzlé pustiny Kalidar IV.",
      "bbox": [72.0, 150.0, 520.0, 165.0],
      "font": "Times-Roman",
      "size": 12.0,
      "flags": 0,
      "color": 0,
      "type": "body",
      "overflow_warning": false
    }
  ]
}
```

CRITICAL:
- Use Read tool to load JSON (not Bash cat)
- Use Write tool to save JSON (not Bash echo)
- Preserve exact JSON structure (all original fields)
- Apply glossary rules strictly
- Report progress after each page: "✓ Page X: Y blocks translated"
```

### What I need to know:

After translation, tell me:
- How many pages were translated successfully?
- Were there any overflow warnings?
- Sample of translated content (show first few blocks from page 1)

### Example: Launching multiple subagents in parallel

For a 50-page PDF, create 5 subagents processing 10 pages each:

```
Use Task tool 5 times (in one message for parallel execution):
1. Task(prompt="Translate pages 1-10...", subagent_type="general-purpose")
2. Task(prompt="Translate pages 11-20...", subagent_type="general-purpose")
3. Task(prompt="Translate pages 21-30...", subagent_type="general-purpose")
4. Task(prompt="Translate pages 31-40...", subagent_type="general-purpose")
5. Task(prompt="Translate pages 41-50...", subagent_type="general-purpose")
```

Each subagent works independently, dramatically reducing total time.

---

## After Completion

Once translation is complete and all subagents finish, proceed to:
**→ [03-rebuild-pdf.md](03-rebuild-pdf.md)**
