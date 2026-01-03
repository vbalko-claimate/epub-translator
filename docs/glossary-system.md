# Glossary System for EPUB Translation

**How to handle proper names, terminology, and existing translation dictionaries**

---

## The Problem

Different books need different translation approaches:

**Example 1: Realistic Fiction**
```
"John walked through London to meet Sarah at the British Museum."

Should translate to Czech as:
"John šel přes Londýn, aby se setkal se Sarah v Britském muzeu."

- "John", "Sarah" → PRESERVE (character names)
- "London" → TRANSLATE to "Londýn" (real place, has Czech name)
- "British Museum" → TRANSLATE to "Britské muzeum"
```

**Example 2: Fantasy (Warhammer 40k)**
```
"The Space Marine fired his bolter at the Chaos cultist."

Should translate to Czech as:
"Vesmírný mariňák vystřelil z bolteru na chaotického kultistu."

- "Space Marine" → TRANSLATE to "Vesmírný mariňák" (official Czech term)
- "bolter" → PRESERVE as "bolter" (or use genitive "bolteru")
- "Chaos" → TRANSLATE to "Chaos" or "chaotický" (depends on context)
```

**Example 3: Existing Translation**
```
Harry Potter books already have official Czech translation:
- "Hogwarts" → "Bradavice" (official)
- "Quidditch" → "Famfrpál" (official)
- "Muggle" → "Mudla" (official)

You want to USE these existing translations for consistency!
```

---

## Solution: Glossary Files

Create a **glossary file** before translating that tells the AI:
1. What to preserve (never translate)
2. What to translate (and to what)
3. What to decide based on context

---

## Glossary Format

### Format 1: Simple TXT (Easiest)

**File: `glossaries/baneblade-en-cs.txt`**

```
# Character names - PRESERVE
PRESERVE: Cortein
PRESERVE: Bannick
PRESERVE: Vorkosigen
PRESERVE: Meggen

# Places - PRESERVE (fictional)
PRESERVE: Kalidar IV
PRESERVE: Paragon

# Military units - PRESERVE
PRESERVE: Baneblade
PRESERVE: Mars Triumphant

# Technical terms - PRESERVE
PRESERVE: lascannon
PRESERVE: vox
PRESERVE: augur
PRESERVE: servitor

# Real places - TRANSLATE
TRANSLATE: Mars → Mars
TRANSLATE: Earth → Země

# Titles - CONTEXT BASED
CONTEXT: Emperor → Keep capitalized "Emperor" (refers to God-Emperor)
CONTEXT: Chapter → Translate to "Kapitola" in headings, preserve in "Space Marine Chapter"

# Common terms - TRANSLATE
TRANSLATE: Chapter → Kapitola
TRANSLATE: Prologue → Prolog
TRANSLATE: Epilogue → Epilog
```

**How to use:**
```
Translate this chapter using the glossary file: glossaries/baneblade-en-cs.txt

Read the glossary first, then apply rules during translation.
```

---

### Format 2: JSON (Structured)

**File: `glossaries/warhammer40k-en-cs.json`**

```json
{
  "metadata": {
    "universe": "Warhammer 40,000",
    "source_language": "en",
    "target_language": "cs",
    "version": "1.0",
    "author": "Community",
    "notes": "Based on official Black Library Czech translations where available"
  },
  "preserve": [
    {
      "term": "Space Marine",
      "note": "Translate to 'Vesmírný mariňák' but preserve when used as proper noun",
      "translation": "Vesmírný mariňák",
      "mode": "translate"
    },
    {
      "term": "Baneblade",
      "note": "Tank type, always preserve",
      "mode": "preserve"
    },
    {
      "term": "bolter",
      "note": "Weapon type, preserve but use Czech grammar (bolteru, bolterem)",
      "translation": "bolter",
      "mode": "preserve_with_grammar"
    },
    {
      "term": "Emperor",
      "note": "When capitalized and referring to the God-Emperor, keep as 'Emperor'",
      "context": "capitalized",
      "mode": "preserve"
    },
    {
      "term": "Chapter",
      "translations": {
        "as_unit": "Řád",
        "as_heading": "Kapitola"
      },
      "mode": "context"
    }
  ],
  "translate": [
    {
      "source": "Prologue",
      "target": "Prolog"
    },
    {
      "source": "Epilogue",
      "target": "Epilog"
    },
    {
      "source": "Chapter",
      "target": "Kapitola",
      "context": "when used in chapter headings only"
    }
  ]
}
```

**How to use:**
```
Translate using glossary: glossaries/warhammer40k-en-cs.json

Parse the JSON and apply:
- preserve[] terms → never translate
- translate[] terms → always use specified translation
- Check "mode" field for special handling
```

---

### Format 3: CSV (Easy Import/Export)

**File: `glossaries/harrypotter-en-cs.csv`**

```csv
term,translation,mode,context,notes
Harry Potter,Harry Potter,preserve,,Character name
Hermione Granger,Hermione Grangerová,preserve_with_grammar,,Use Czech surname declension
Hogwarts,Bradavice,translate,,Official Czech translation
Quidditch,Famfrpál,translate,,Official Czech translation
Muggle,mudla,translate,,Official Czech translation (lowercase!)
Dumbledore,Brumbál,translate,,Official Czech translation
Voldemort,Voldemort,preserve,,Keep original
Ministry of Magic,Ministerstvo kouzel,translate,,Official translation
Chapter,Kapitola,translate,headings_only,
Prologue,Prolog,translate,,
```

**How to use:**
```
Translate using CSV glossary: glossaries/harrypotter-en-cs.csv

Read CSV line by line:
- mode=preserve → keep original
- mode=translate → use translation column
- mode=preserve_with_grammar → keep but allow Czech declension
- Check context column for special rules
```

---

## Translation Modes Explained

### Mode 1: PRESERVE (Never Translate)

**Use for:**
- Fictional character names (Frodo, Katniss, Cortein)
- Made-up place names (Narnia, Westeros, Kalidar IV)
- Invented terminology (lightsaber, TARDIS, vox)
- Brand names (Coca-Cola, iPhone)

**Example:**
```
Source: "Cortein gripped the controls."
Glossary: PRESERVE: Cortein
Result: "Cortein sevřel ovládání."  ← Name unchanged
```

---

### Mode 2: TRANSLATE (Always Use Dictionary)

**Use for:**
- Real places with established translations (London → Londýn)
- Common words (Chapter → Kapitola)
- Official terminology (Space Marine → Vesmírný mariňák)

**Example:**
```
Source: "The Space Marine fired his weapon."
Glossary: TRANSLATE: Space Marine → Vesmírný mariňák
Result: "Vesmírný mariňák vystřelil ze své zbraně."
```

---

### Mode 3: PRESERVE_WITH_GRAMMAR (Keep Word, Apply Grammar)

**Use for:**
- Technical terms that need Czech case endings
- Foreign words adopted into Czech

**Example:**
```
Source: "He fired the bolter."
Glossary: PRESERVE_WITH_GRAMMAR: bolter
Result: "Vystřelil z bolteru."  ← "bolter" → "bolteru" (genitive case)

Source: "The bolter jammed."
Result: "Bolter se zasekl."  ← Nominative, unchanged
```

**How AI handles this:**
- Keep the root word (bolter)
- Add Czech case endings (-u, -em, -ů, etc.)
- Follow Czech grammar rules

---

### Mode 4: CONTEXT (Decide Based on Usage)

**Use for:**
- Words with multiple meanings
- Terms used differently in different contexts

**Example:**
```
Term: "Chapter"

Context 1 (heading): "Chapter 5"
Glossary: CONTEXT: Chapter → "Kapitola" when in headings
Result: "Kapitola 5"

Context 2 (military): "The Ultramarines Chapter"
Glossary: CONTEXT: Chapter → "Řád" when referring to Space Marine organization
Result: "Řád Ultramariňáků"
```

**How AI decides:**
- Check surrounding words
- Look at capitalization
- Analyze sentence structure
- Apply most appropriate translation

---

## Using Glossaries with AI

### Claude Code Skill (Automatic)

**File: `my-book-glossary.txt`**
```
PRESERVE: Cortein
PRESERVE: Baneblade
TRANSLATE: Chapter → Kapitola
TRANSLATE: Mars → Mars
```

**Command:**
```bash
claude "translate book.epub from English to Czech using glossary my-book-glossary.txt"
```

**Skill will:**
1. Read glossary file
2. Parse rules
3. Pass to all translation subagents
4. Apply consistently across all chapters

---

### Manual Workflow (Any AI)

**Step 1: Create glossary file**

Use provided templates or create your own.

**Step 2: Include in prompt**

```
Translate this chapter from English to Czech.

File: epub_workspace/translated/OEBPS/chapter-1.xhtml

Use this glossary:

PRESERVE (never translate):
- Cortein (character name)
- Baneblade (tank type)
- lascannon (weapon)
- vox (communication device)

TRANSLATE (always use these):
- Chapter → Kapitola
- Prologue → Prolog
- Mars → Mars (planet, same in Czech)

PRESERVE_WITH_GRAMMAR (keep word, apply Czech cases):
- bolter → bolter/bolteru/bolterem/etc.

Now translate the chapter following these rules exactly.
```

**Step 3: Repeat for all chapters**

Copy same glossary into each chapter's prompt for consistency.

---

## Community Glossaries (Pre-Made)

### Warhammer 40,000 (English → Czech)

**File: `glossaries/community/warhammer40k-en-cs.json`**

Based on official Black Library translations + community consensus:

```json
{
  "factions": {
    "Space Marines": "Vesmírní mariňáci",
    "Imperial Guard": "Imperiální garda",
    "Chaos": "Chaos",
    "Orks": "Orkové"
  },
  "weapons": {
    "bolter": "bolter",
    "lascannon": "lascannon",
    "plasma gun": "plazmová puška"
  },
  "vehicles": {
    "Baneblade": "Baneblade",
    "Leman Russ": "Leman Russ",
    "Chimera": "Chimera"
  },
  "titles": {
    "Emperor": "Císař",
    "Primarch": "Primarch",
    "Chapter Master": "Velmistr řádu"
  }
}
```

[Full file included in repository]

---

### Harry Potter (English → Czech)

**File: `glossaries/community/harrypotter-en-cs.csv`**

Based on official Albatros Media translations:

```csv
term,translation,notes
Hogwarts,Bradavice,Official
Quidditch,Famfrpál,Official
Muggle,mudla,Official (lowercase)
Dumbledore,Brumbál,Official
Snape,Snape,Preserved
Hermione,Hermiona,Official spelling
Gryffindor,Nebelvír,Official
Slytherin,Zmijozel,Official
Hufflepuff,Mrzimor,Official
Ravenclaw,Havraspár,Official
```

[Full file included in repository]

---

### Lord of the Rings (English → Czech)

**File: `glossaries/community/lotr-en-cs.txt`**

Based on official translations:

```
# Characters - Official Czech names
TRANSLATE: Frodo → Frodo (unchanged)
TRANSLATE: Gandalf → Gandalf (unchanged)
TRANSLATE: Aragorn → Aragorn (unchanged)
TRANSLATE: Gollum → Glum (official Czech)

# Places - Official translations
TRANSLATE: Middle-earth → Středozem
TRANSLATE: The Shire → Kraj
TRANSLATE: Mordor → Mordor (unchanged)
TRANSLATE: Rivendell → Roklinec

# Races
TRANSLATE: Hobbit → Hobit
TRANSLATE: Elf → Elf
TRANSLATE: Dwarf → Trpaslík
TRANSLATE: Orc → Ork

# Items
TRANSLATE: The One Ring → Jeden prsten
TRANSLATE: Sting → Žihadlo
```

[Full file included in repository]

---

## Creating Your Own Glossary

### Method 1: Manual (For Small Books)

**Step 1: Read first chapter**

Note all:
- Character names
- Place names
- Technical terms
- Repeated phrases

**Step 2: Decide translation approach**

For each term:
- Real place? → TRANSLATE (London → Londýn)
- Character name? → PRESERVE (John → John)
- Technical term? → Check if translation exists

**Step 3: Create TXT file**

```
# Characters
PRESERVE: John Smith
PRESERVE: Sarah Johnson

# Places
TRANSLATE: London → Londýn
TRANSLATE: British Museum → Britské muzeum

# Common
TRANSLATE: Chapter → Kapitola
```

---

### Method 2: AI-Assisted (For Large Books)

**Use this prompt:**

```
I need to create a glossary for translating this EPUB from English to Czech.

Please read the first chapter and identify:

1. Character names (people, animals, sentient beings)
2. Place names (cities, countries, planets, buildings)
3. Organization names (companies, military units, groups)
4. Technical terms (weapons, devices, special vocabulary)
5. Titles and ranks

For each term, suggest whether to:
- PRESERVE (keep in English)
- TRANSLATE (provide Czech translation)
- PRESERVE_WITH_GRAMMAR (keep but allow Czech case endings)

Format output as TXT glossary file.

Chapter file: epub_workspace/original/OEBPS/chapter-1.xhtml
```

**AI will generate:**

```
# GENERATED GLOSSARY
# Book: [Title]
# Source: English
# Target: Czech

# Characters (18 found)
PRESERVE: Cortein
PRESERVE: Bannick
PRESERVE: Vorkosigen
...

# Places (7 found)
PRESERVE: Kalidar IV (fictional planet)
TRANSLATE: Mars → Mars (real planet, same name)
...

# Technical terms (23 found)
PRESERVE_WITH_GRAMMAR: lascannon
PRESERVE_WITH_GRAMMAR: bolter
PRESERVE: vox
...

# Common terms
TRANSLATE: Chapter → Kapitola
TRANSLATE: Prologue → Prolog
```

**Step 2: Review and adjust**

- Check AI suggestions
- Add missing terms
- Fix incorrect categorizations
- Add context notes

**Step 3: Save and use**

Save as `glossaries/my-book-glossary.txt`

---

### Method 3: Extract from Existing Translation

**If a book already has a translation, extract its dictionary:**

**Prompt:**

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

Output format: CSV with columns [original, translation, category, notes]
```

**AI will generate:**

```csv
original,translation,category,notes
Harry Potter,Harry Potter,character,Preserved
Hermione Granger,Hermiona Grangerová,character,First name adapted; surname with Czech ending
Hogwarts,Bradavice,place,Translated
Quidditch,Famfrpál,term,Creative Czech translation
Muggle,mudla,term,Lowercase in Czech
Dumbledore,Brumbál,character,Fully translated name
```

**Save as:** `glossaries/extracted-harrypotter-en-cs.csv`

---

## Advanced: Multi-Book Series

**Problem:** Translating a 5-book series, need consistency!

**Solution:** One master glossary for entire series

**File: `glossaries/hunger-games-trilogy-en-cs.json`**

```json
{
  "series": "The Hunger Games Trilogy",
  "books": ["The Hunger Games", "Catching Fire", "Mockingjay"],
  "consistency_critical": true,

  "characters": {
    "Katniss Everdeen": {
      "translation": "Katniss Everdeen",
      "mode": "preserve",
      "first_appearance": "Book 1, Chapter 1"
    },
    "Peeta Mellark": {
      "translation": "Peeta Mellark",
      "mode": "preserve"
    },
    "President Snow": {
      "translation": "Prezident Snow",
      "mode": "translate_title_only",
      "note": "Translate 'President', keep 'Snow'"
    }
  },

  "places": {
    "Panem": {
      "translation": "Panem",
      "mode": "preserve",
      "note": "Fictional nation, no translation"
    },
    "District 12": {
      "translation": "Dvanáctý distrikt",
      "mode": "translate"
    },
    "The Capitol": {
      "translation": "Kapitol",
      "mode": "translate"
    }
  },

  "terms": {
    "Mockingjay": {
      "translation": "Drozdajka",
      "mode": "translate",
      "note": "Official Czech translation, critical for consistency"
    },
    "Tribute": {
      "translation": "Tribut",
      "mode": "translate"
    },
    "Reaping": {
      "translation": "Žeň",
      "mode": "translate",
      "note": "Specific ceremonial term"
    }
  }
}
```

**Usage:**

```bash
# Book 1
claude "translate hunger-games-1.epub from English to Czech using glossaries/hunger-games-trilogy-en-cs.json"

# Book 2 (same glossary!)
claude "translate catching-fire.epub from English to Czech using glossaries/hunger-games-trilogy-en-cs.json"

# Book 3 (same glossary!)
claude "translate mockingjay.epub from English to Czech using glossaries/hunger-games-trilogy-en-cs.json"
```

**Result:** Perfect consistency across all 3 books!

---

## Glossary Validation

**Check glossary quality before using:**

### Validation Script

**File: `scripts/validate-glossary.sh`**

```bash
#!/bin/bash
# Validate glossary file syntax

GLOSSARY="$1"

if [ ! -f "$GLOSSARY" ]; then
    echo "❌ File not found: $GLOSSARY"
    exit 1
fi

echo "Validating glossary: $GLOSSARY"

# Check file extension
EXT="${GLOSSARY##*.}"

case "$EXT" in
    txt)
        echo "✓ Format: TXT"
        # Check syntax
        grep -E "^(PRESERVE|TRANSLATE|CONTEXT|PRESERVE_WITH_GRAMMAR):" "$GLOSSARY" > /dev/null
        if [ $? -eq 0 ]; then
            echo "✓ Syntax: Valid"
        else
            echo "❌ Syntax: No valid rules found"
            exit 1
        fi
        ;;
    json)
        echo "✓ Format: JSON"
        # Validate JSON
        python3 -m json.tool "$GLOSSARY" > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "✓ Syntax: Valid JSON"
        else
            echo "❌ Syntax: Invalid JSON"
            exit 1
        fi
        ;;
    csv)
        echo "✓ Format: CSV"
        # Check CSV headers
        head -1 "$GLOSSARY" | grep "term,translation,mode" > /dev/null
        if [ $? -eq 0 ]; then
            echo "✓ Headers: Valid"
        else
            echo "⚠️  Headers: Missing or incorrect"
        fi
        ;;
    *)
        echo "❌ Unsupported format: .$EXT"
        echo "   Supported: .txt, .json, .csv"
        exit 1
        ;;
esac

# Count entries
if [ "$EXT" = "txt" ]; then
    COUNT=$(grep -c "^PRESERVE\|^TRANSLATE" "$GLOSSARY")
elif [ "$EXT" = "csv" ]; then
    COUNT=$(($(wc -l < "$GLOSSARY") - 1))  # Minus header
elif [ "$EXT" = "json" ]; then
    COUNT="(JSON - use jq to count)"
fi

echo "✓ Entries: $COUNT terms"
echo ""
echo "Glossary validation complete!"
```

**Usage:**
```bash
chmod +x scripts/validate-glossary.sh
./scripts/validate-glossary.sh glossaries/my-book.txt
```

---

## Tips & Best Practices

### 1. Start Small, Expand Later

**First pass:**
```
PRESERVE: Main character names (5-10)
TRANSLATE: Chapter → Kapitola
```

**After 5 chapters, expand:**
```
+ Add place names found
+ Add technical terms discovered
+ Add recurring phrases
```

**By end of book:**
- Complete glossary with 50-100+ terms
- Ready to reuse for sequels!

---

### 2. Use Comments

```
# Main protagonist - appears 500+ times
PRESERVE: Katniss Everdeen

# Minor character - only in chapters 5-7
PRESERVE: Effie Trinket

# IMPORTANT: This is the God-Emperor, not a generic emperor!
# Keep capitalized to distinguish from regular emperors
CONTEXT: Emperor → Keep as "Emperor" when capitalized
```

---

### 3. Version Control

```
glossaries/
├── warhammer40k-en-cs-v1.0.json  (stable)
├── warhammer40k-en-cs-v1.1.json  (added tank types)
├── warhammer40k-en-cs-v2.0.json  (major update)
└── warhammer40k-en-cs-latest.json → warhammer40k-en-cs-v2.0.json (symlink)
```

Use latest for new translations, older versions for consistency with previous work.

---

### 4. Share with Community

If you create a good glossary for a popular book/universe:

1. Save to `glossaries/community/[universe]-[source]-[target].json`
2. Add README explaining sources (official translations, fan consensus)
3. Contribute to repository via pull request
4. Others can benefit!

---

## Example: Complete Workflow with Glossary

**Scenario:** Translating "Baneblade" (Warhammer 40k) from English to Czech

**Step 1: Create glossary**

```bash
# Use AI to generate initial glossary
claude "analyze first chapter of baneblade.epub and create translation glossary"

# AI outputs: glossaries/baneblade-en-cs.txt
```

**Step 2: Review and edit**

```txt
# Generated glossary - REVIEWED by human

# Characters
PRESERVE: Cortein
PRESERVE: Bannick
PRESERVE: Vorkosigen

# Vehicles
PRESERVE: Baneblade
PRESERVE: Mars Triumphant

# Weapons
PRESERVE_WITH_GRAMMAR: lascannon
PRESERVE_WITH_GRAMMAR: bolter
PRESERVE_WITH_GRAMMAR: plasma gun

# Factions
TRANSLATE: Space Marine → Vesmírný mariňák
TRANSLATE: Imperial Guard → Imperiální garda

# Common
TRANSLATE: Chapter → Kapitola
```

**Step 3: Translate with glossary**

```bash
claude "translate baneblade.epub from English to Czech using glossary glossaries/baneblade-en-cs.txt"
```

**Step 4: Verify consistency**

```bash
# Check that glossary was applied
grep "Vesmírný mariňák" epub_workspace/translated/OEBPS/*.xhtml
# Should find translations

grep "Space Marine" epub_workspace/translated/OEBPS/*.xhtml
# Should find ZERO (was translated)

grep "Cortein" epub_workspace/translated/OEBPS/*.xhtml
# Should find many (was preserved)
```

**Done!** Consistent translation following glossary rules.

---

## Next Steps

1. **Try the templates** - Use provided glossary files for your first translation
2. **Build your own** - Create custom glossary for your book
3. **Share glossaries** - Contribute to community collection
4. **Reuse for sequels** - Same glossary across book series

---

**See also:**
- [SKILL.md](../claude-skill/SKILL.md) - How skill uses glossaries automatically
- [Prompt 03](../prompts/03-translate-chapter.md) - Manual glossary usage
- [Community Glossaries](../glossaries/community/) - Pre-made dictionaries
