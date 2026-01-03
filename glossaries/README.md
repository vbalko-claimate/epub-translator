# Translation Glossaries

Translation dictionaries for controlling how terms are handled during EPUB translation.

---

## What are Glossaries?

Glossaries are files that tell the AI:
- **What to preserve** (never translate) - character names, technical terms
- **What to translate** (and to what) - using specific translations
- **How to handle grammar** - keeping foreign words but applying target language cases
- **Context rules** - different translations based on usage

**Why use them?**
- ✅ Consistency across all chapters
- ✅ Match official translations (Harry Potter, etc.)
- ✅ Control over terminology (sci-fi, fantasy universes)
- ✅ Reusable for book series

---

## Available Glossaries

### Community Glossaries

Pre-made translation dictionaries for popular book universes:

| Universe | Language Pair | Format | Terms | Status |
|----------|--------------|--------|-------|--------|
| **Warhammer 40,000** | EN → CS | JSON | 100+ | ✅ Complete |
| Harry Potter | EN → CS | CSV | Planned | 🚧 Coming soon |
| Lord of the Rings | EN → CS | TXT | Planned | 🚧 Coming soon |

**Path:** `glossaries/community/[universe]-[source]-[target].[format]`

---

### Your Own Glossaries

**Path:** `glossaries/` (root folder)

Create your own using:
- **[template.txt](template.txt)** - Start here! Copy and customize

**Naming convention:**
```
[book-name]-[source-lang]-[target-lang].[format]

Examples:
- baneblade-en-cs.txt
- harry-potter-1-en-de.json
- dune-en-fr.csv
```

---

## Quick Start

### 1. Using Existing Glossary (Claude Code)

```bash
# Use community glossary
claude "translate book.epub from English to Czech using glossary glossaries/community/warhammer40k-en-cs.json"

# Or use your own
claude "translate book.epub using glossary glossaries/my-book-en-cs.txt"
```

### 2. Creating Your Own Glossary

**Step 1: Copy template**
```bash
cp glossaries/template.txt glossaries/my-book-en-cs.txt
```

**Step 2: Edit the file**

Add your book's specific terms:
```
# Characters
PRESERVE: Harry Potter
PRESERVE: Hermione Granger

# Places
TRANSLATE: London → Londýn
PRESERVE: Hogwarts

# Technical
TRANSLATE: wand → hůlka
PRESERVE_WITH_GRAMMAR: broomstick
```

**Step 3: Use in translation**
```bash
claude "translate my-book.epub using glossary glossaries/my-book-en-cs.txt"
```

---

## Glossary Formats

### Format 1: TXT (Simple)

**Best for:** Quick glossaries, simple books

**Example:** `my-book-en-cs.txt`
```
# Character names
PRESERVE: John Smith
PRESERVE: Sarah Johnson

# Places
TRANSLATE: London → Londýn
TRANSLATE: Paris → Paříž

# Technical terms
PRESERVE_WITH_GRAMMAR: laser

# Context-dependent
CONTEXT: Chapter → "Kapitola" in headings, different in other contexts
```

### Format 2: JSON (Structured)

**Best for:** Large glossaries, complex rules, series

**Example:** `warhammer40k-en-cs.json`
```json
{
  "metadata": {
    "universe": "Warhammer 40,000",
    "source_language": "en",
    "target_language": "cs-CZ"
  },
  "factions": {
    "Space Marines": {
      "translation": "Vesmírní mariňáci",
      "mode": "translate"
    }
  },
  "weapons": {
    "bolter": {
      "translation": "bolter",
      "mode": "preserve_with_grammar",
      "declension": {
        "nominative": "bolter",
        "genitive": "bolteru"
      }
    }
  }
}
```

### Format 3: CSV (Spreadsheet)

**Best for:** Importing from Excel, sharing with teams

**Example:** `harry-potter-en-cs.csv`
```csv
term,translation,mode,notes
Harry Potter,Harry Potter,preserve,Character name
Hogwarts,Bradavice,translate,Official translation
Quidditch,Famfrpál,translate,Official translation
wand,hůlka,translate,
```

---

## Translation Modes

### PRESERVE

**Never translate** - keep original text exactly as-is

**Use for:**
- Fictional character names (Frodo, Katniss, Cortein)
- Made-up place names (Narnia, Westeros, Hogwarts)
- Brand names (Coca-Cola, iPhone)
- Invented terminology (lightsaber, TARDIS)

**Example:**
```
PRESERVE: Cortein

Input:  "Cortein gripped the controls."
Output: "Cortein sevřel ovládání."  ← Name unchanged
```

### TRANSLATE

**Always use specific translation** - replace with dictionary term

**Use for:**
- Real places with established names (London → Londýn)
- Common words with known translations (Chapter → Kapitola)
- Official terminology (Space Marine → Vesmírný mariňák)

**Example:**
```
TRANSLATE: Chapter → Kapitola

Input:  "Chapter 5"
Output: "Kapitola 5"  ← Always translated
```

### PRESERVE_WITH_GRAMMAR

**Keep the word but apply target language grammar**

**Use for:**
- Technical terms adopted into language
- Foreign words that need case endings (Czech, German, Russian)

**Example:**
```
PRESERVE_WITH_GRAMMAR: bolter

Input:  "He fired the bolter."
Output: "Vystřelil z bolteru."  ← "bolter" → "bolteru" (genitive)

Input:  "The bolter jammed."
Output: "Bolter se zasekl."  ← "bolter" (nominative, unchanged)
```

### CONTEXT

**Decide based on usage** - different translations in different situations

**Use for:**
- Words with multiple meanings
- Terms used differently in different contexts

**Example:**
```
CONTEXT: Chapter → "Kapitola" in headings, "Řád" for military units

Input:  "Chapter 5"
Output: "Kapitola 5"  ← Heading context

Input:  "The Ultramarines Chapter"
Output: "Řád Ultramariňáků"  ← Military context
```

---

## Community Glossaries Detail

### Warhammer 40,000 (English → Czech)

**File:** `community/warhammer40k-en-cs.json`

**Coverage:**
- ✅ Factions (Space Marines, Imperial Guard, Chaos, etc.)
- ✅ Military units (Ultramarines, Blood Angels, etc.)
- ✅ Weapons (bolter, lascannon, plasma gun, etc.)
- ✅ Vehicles (Baneblade, Leman Russ, etc.)
- ✅ Titles & Ranks (Emperor, Primarch, Captain, etc.)
- ✅ Technology (vox, augur, servitor, etc.)
- ✅ Religious terms (Omnissiah, Machine God, etc.)
- ✅ Places (Terra, Mars, Warp, etc.)
- ✅ Common phrases ("For the Emperor!", etc.)

**Based on:**
- Official Black Library Czech translations
- Czech Warhammer 40k Wiki
- Community consensus from Czech fans

**Total terms:** 100+

**Usage:**
```bash
claude "translate baneblade.epub from English to Czech using glossary glossaries/community/warhammer40k-en-cs.json"
```

---

## Building Glossaries

### Method 1: Manual (Small Books)

1. Read first chapter
2. Note all:
   - Character names
   - Place names
   - Technical terms
   - Repeated phrases
3. Decide translation approach for each
4. Write to TXT file using template

**Time:** ~30 minutes

### Method 2: AI-Assisted (Large Books)

Use this prompt:

```
I need to create a translation glossary for translating this EPUB from English to Czech.

Please read the first chapter and identify:

1. Character names (people, animals, sentient beings)
2. Place names (cities, countries, planets, buildings)
3. Organization names (companies, military units, groups)
4. Technical terms (weapons, devices, special vocabulary)
5. Titles and ranks

For each term, suggest whether to:
- PRESERVE (keep in English)
- TRANSLATE (provide Czech translation)
- PRESERVE_WITH_GRAMMAR (keep but allow Czech cases)

Format output as TXT glossary file.

Chapter file: epub_workspace/original/OEBPS/chapter-1.xhtml
```

**Time:** ~10 minutes

### Method 3: Extract from Existing Translation

If a translation already exists, extract its dictionary:

```
I have two versions of the same book:
- Original: book-english.epub
- Translation: book-czech.epub

Please compare them and create a glossary showing how terms were translated.

Focus on:
1. Character names (how were they handled?)
2. Place names (translated or preserved?)
3. Technical terminology
4. Common phrases

Output format: CSV
```

**Time:** ~15 minutes

---

## Validation

Validate your glossary before using:

```bash
# Check syntax
./scripts/validate-glossary.sh glossaries/my-book.txt

# Output:
# ✓ Format: TXT
# ✓ Syntax: Valid
# ✓ Entries: 47 terms
# Glossary validation complete!
```

---

## Contributing

**Add your glossaries to the community collection!**

1. Create high-quality glossary for popular universe
2. Base on official translations where available
3. Document sources in metadata
4. Submit pull request to `glossaries/community/`

**Guidelines:**
- Include at least 50 terms
- Provide metadata (sources, version, author)
- Test with actual translation
- Add README entry

---

## FAQ

**Q: Do I need a glossary?**

A: No, but recommended for:
- Fantasy/sci-fi books (many proper names)
- Book series (consistency across volumes)
- Matching official translations
- Technical books (specialized terminology)

**Q: Can I use multiple glossaries?**

A: Currently one per translation. For series, create one master glossary.

**Q: What if a term isn't in the glossary?**

A: AI will decide based on context and general translation rules.

**Q: Can I edit glossaries after translation starts?**

A: Yes, but only affects remaining chapters. Already translated chapters won't change.

**Q: How do I share glossaries?**

A: Commit to this repository or share the file directly. JSON/CSV are most portable.

---

## Resources

- **[Glossary System Documentation](../docs/glossary-system.md)** - Complete guide
- **[Template File](template.txt)** - Start here for custom glossaries
- **[Warhammer 40k Example](community/warhammer40k-en-cs.json)** - See advanced features

---

**Happy translating!** 📚✨
