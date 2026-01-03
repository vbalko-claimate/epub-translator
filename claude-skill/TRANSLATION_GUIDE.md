# EPUB Translation Best Practices

Guidelines for translating EPUB books while preserving quality, formatting, and readability.

## Core Translation Principles

### 1. Preserve Structure, Translate Content

**DO:**
- Translate text inside `<p>`, `<h1>`, `<span>`, etc.
- Keep all HTML tags exactly as they are
- Maintain CSS class names
- Preserve `id` attributes

**DON'T:**
- Change HTML tag structure
- Modify CSS class names
- Alter image paths or filenames
- Remove or add HTML elements

**Example:**
```xml
<!-- BEFORE -->
<p class="body-text" id="para-1">
    The <span class="character">captain</span> walked into the room.
</p>

<!-- AFTER (Czech translation) -->
<p class="body-text" id="para-1">
    <span class="character">Kapitán</span> vešel do místnosti.
</p>
```

### 2. Identify What NOT to Translate

#### Proper Names

Character names should typically stay in original language:
- ✅ "John walked..." → "John šel..."
- ❌ "John walked..." → "Jan šel..." (unless it's a common name with established translation)

**When to translate names:**
- Historical figures with established translations ("Napoleon" → "Napoleon")
- Common biblical/mythological names ("John the Baptist" → "Jan Křtitel")
- Generic titles ("The King" → "Král")

**When NOT to translate:**
- Unique character names in fiction
- Made-up fantasy/sci-fi names
- Author-created terminology

#### Place Names

**Translate if:**
- Real-world places with established translations ("London" → "Londýn" in Czech)
- Generic locations ("the capital city" → "hlavní město")

**Don't translate if:**
- Fictional places ("Hogwarts" stays "Hogwarts")
- Made-up planet/city names in sci-fi
- Author-created geography

#### Technical Terminology

**Genre-specific terms** often have no translation:
- Sci-fi: "hyperdrive", "photon torpedo", "warp speed"
- Fantasy: "mithril", "elfstone", "dragonfire"
- Historical: "samurai", "legionnaire", "centurion"

**Check with user** or research fanbase conventions:
- Warhammer 40k: "Baneblade", "lascannon" → keep in English
- Star Wars: "lightsaber" → "světelný meč" (Czech has translation)
- Star Trek: Varies by franchise tradition

### 3. Handle Chapter Structure

#### Chapter Titles

**Pattern-based translation:**
```
"Prologue" → "Prolog"
"Chapter 1" → "Kapitola 1"
"Chapter One" → "Kapitola první"
"Epilogue" → "Epilog"
"Interlude" → "Intermez" / "Mezihra"
```

**Custom chapter titles:**
```
"The Beginning" → "Začátek"
"Into the Storm" → "Do bouře"
```

**Preserve if:**
- Chapter has a proper name ("The Tale of Aragorn" → keep if part of title)
- Stylized formatting in title

### 4. Maintain Reading Flow

#### Dialogue Attribution

Keep natural language patterns:

**English:**
```
"Hello," he said.
"How are you?" she asked.
```

**Czech:**
```
"Ahoj," řekl.
"Jak se máš?" zeptala se.
```

**German:**
```
„Hallo", sagte er.
„Wie geht es dir?", fragte sie.
```

Notice: Quote marks and punctuation conventions vary by language!

#### Paragraph Structure

- Maintain paragraph breaks
- Keep emphasis (bold, italic) on same words
- Preserve line breaks in poetry/lyrics

### 5. Handle Special Content

#### Quoted Text

If book quotes other works (Bible, poetry, classics):
- Use **official translation** if it exists
- Cite translation in footnote if needed
- Keep original if no translation exists

#### Made-Up Languages

For constructed languages (Elvish, Klingon, etc.):
- **Keep untranslated**
- Translate any provided translation in the text
- Preserve pronunciation guides

#### Poetry/Songs

**Options:**
1. **Translate meaning** (lose rhythm/rhyme)
2. **Adapt as new poem** (preserve feeling, not literal)
3. **Keep original + add translation** (footnote or side-by-side)

Consult with user on preference.

### 6. Consistency is Key

#### Maintain Translation Glossary

For recurring terms, keep consistent:

| Original | Translation | Notes |
|----------|-------------|-------|
| "the captain" | "kapitán" | Character title |
| "ship's log" | "lodní deník" | Technical term |
| "warp speed" | "warp speed" | No translation (sci-fi) |

#### Character Name Spelling

If name appears 100 times, it must be:
- Spelled exactly same way every time
- Same capitalization
- Same formatting (italic, bold, etc.)

### 7. Preserve Formatting Elements

#### Text Styling

Maintain all emphasis:
```xml
<em>emphasized</em> → <em>zdůrazněno</em>
<strong>strong</strong> → <strong>silné</strong>
<span class="italic">italic</span> → <span class="italic">kurzíva</span>
```

#### Block Elements

```xml
<blockquote>
    Quote text
</blockquote>

<!-- Keep structure: -->

<blockquote>
    Přeložený citát
</blockquote>
```

### 8. Handle Metadata

#### Language Codes

Update to match target language:

```xml
<!-- Before -->
<body xml:lang="en-GB">

<!-- After (Czech) -->
<body xml:lang="cs-CZ">

<!-- After (German) -->
<body xml:lang="de-DE">
```

#### Navigation Labels

Translate consistently across:
- toc.ncx
- Table of Contents XHTML
- Chapter headings

All three should match!

## Quality Assurance

### Pre-Translation Checklist

- [ ] Identify book genre (affects terminology handling)
- [ ] List all proper names to preserve
- [ ] List all technical terms
- [ ] Check for special formatting (poetry, letters, etc.)
- [ ] Determine quote style for target language

### During Translation

- [ ] Process chapters in order
- [ ] Maintain glossary of terms
- [ ] Note any inconsistencies
- [ ] Mark unclear passages for review

### Post-Translation Checklist

- [ ] All chapter files translated
- [ ] Metadata updated (language codes)
- [ ] Navigation translated (toc.ncx)
- [ ] Table of contents translated
- [ ] Proper names consistent throughout
- [ ] No HTML tags broken
- [ ] Images still referenced correctly
- [ ] EPUB validates with no errors

### Validation Steps

1. **Structural validation:**
   ```bash
   unzip -t translated.epub
   ```

2. **Content check:**
   - Open in EPUB reader
   - Navigate through chapters
   - Check TOC links work
   - Verify images display

3. **Language check:**
   - Reader detects correct language
   - Hyphenation works (if supported)
   - Text flows naturally

## Common Pitfalls

### ❌ Over-Translation

**Problem:** Translating things that should stay in original

**Example:**
```
"John activated the hyperdrive"
❌ "Jan aktivoval nadsvětelný pohon"
✅ "John aktivoval hyperdrive"
```

**Fix:** When in doubt, keep technical/fantasy terms in original

### ❌ Breaking HTML

**Problem:** Changing tag structure during translation

**Example:**
```xml
<!-- Before -->
<p class="dialogue">
    <span class="speaker">John:</span> "Hello"
</p>

<!-- Wrong -->
<p class="dialogue">John: "Ahoj"</p>  <!-- Lost the span! -->

<!-- Right -->
<p class="dialogue">
    <span class="speaker">John:</span> "Ahoj"
</p>
```

### ❌ Inconsistent Terminology

**Problem:** Same term translated differently

**Example:**
- Chapter 1: "warp drive" → "warp pohon"
- Chapter 10: "warp drive" → "prostoročas pohon"

**Fix:** Keep glossary, search-replace at end if needed

### ❌ Losing Emphasis

**Problem:** Forgetting to maintain italic/bold

**Example:**
```
"The *Enterprise* flew through space"
❌ "Enterprise letěla vesmírem"  <!-- Lost italic -->
✅ "*Enterprise* letěla vesmírem"  <!-- Kept italic -->
```

## Advanced Techniques

### Batch Processing

For long books (20+ chapters):

1. **Translate in batches** of 5 chapters
2. **Validate each batch** before continuing
3. **Maintain running glossary** across batches
4. **Check consistency** at end

### Parallel Translation

If using AI assistants, can translate multiple chapters simultaneously:
- Provide **same glossary** to all instances
- **Number chapters clearly** to avoid confusion
- **Merge carefully**, checking for inconsistencies

### Version Control

Keep backups:
```
workspace/
├── original/       # Untouched source
├── wip/            # Work in progress
├── batch1/         # Chapters 1-10 (done)
├── batch2/         # Chapters 11-20 (done)
└── final/          # Complete translation
```

## Resources

### Translation Tools

- **Glossary builders:** Create term lists from text
- **EPUB editors:** Sigil, Calibre (for manual review)
- **Validators:** EPUBCheck (official validator)

### Language-Specific Guides

Consult language-specific style guides:
- Czech: ČSN 01 6910 (typography)
- German: Duden (orthography)
- French: Le bon usage (grammar)

### Community Resources

- Genre-specific wikis (for terminology)
- Fan translation forums
- Publisher style guides (if available)

## Getting Help

When stuck:

1. **Check official translations** (if book has one in target language)
2. **Ask native speakers** for term appropriateness
3. **Research fanbase conventions** for genre terms
4. **When in doubt, preserve original** and note for review

## Final Note

**Quality over speed:** It's better to:
- Spend extra time researching a term
- Preserve unusual formatting
- Maintain consistency

Than to rush and create:
- Broken HTML
- Lost formatting
- Inconsistent terminology

A good translation reads naturally while preserving the author's intent and the book's structure.
