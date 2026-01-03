# Translation Examples

Real-world examples showing different translation scenarios and workflows.

---

## Table of Contents

- [Quick Example: Short Story](#quick-example-short-story)
- [Medium Example: Novel](#medium-example-novel)
- [Advanced Example: Technical Book](#advanced-example-technical-book)
- [Batch Translation: Book Series](#batch-translation-book-series)
- [Special Cases](#special-cases)

---

## Quick Example: Short Story

**Book:** The Egg by Andy Weir
**Length:** ~1,000 words (single file)
**Time:** 5 minutes
**Difficulty:** ⭐ Beginner

### Setup

```bash
# Extract
mkdir epub_workspace
unzip the-egg.epub -d epub_workspace/original/
cp -r epub_workspace/original/* epub_workspace/translated/

# Structure
epub_workspace/translated/
├── mimetype
├── META-INF/
│   └── container.xml
└── OEBPS/
    ├── content.opf
    ├── toc.ncx
    └── story.xhtml  ← Only one file to translate!
```

### Translation

**Prompt to AI:**

```
Translate this short story from English to Spanish.

File: epub_workspace/translated/OEBPS/story.xhtml

Rules:
1. Preserve ALL HTML tags
2. Change xml:lang="en" to xml:lang="es-ES"
3. Translate the narrative text
4. Keep character name "You" as "Tú" (formal) or "Vos" (informal) - your choice for consistency

Write the translated file back to the same location.
```

**Result:**

```xml
<!-- Before -->
<p>You were on your way home when you died.</p>

<!-- After -->
<p>Ibas de camino a casa cuando moriste.</p>
```

### Metadata Update

```bash
# Update content.opf
sed -i '' 's/<dc:language>en<\/dc:language>/<dc:language>es-ES<\/dc:language>/' \
    epub_workspace/translated/OEBPS/content.opf
```

### Rebuild

```bash
cd epub_workspace/translated/
zip -0 -X ../../the-egg-spanish.epub mimetype
zip -r ../../the-egg-spanish.epub META-INF OEBPS
cd ../..
```

### Verification

```bash
unzip -t the-egg-spanish.epub
open the-egg-spanish.epub  # macOS
```

**Total time:** ~5 minutes
**Files translated:** 1
**Complexity:** Very simple (no proper names to preserve, single file)

---

## Medium Example: Novel

**Book:** Pride and Prejudice by Jane Austen
**Length:** ~130,000 words
**Chapters:** 61
**Time:** 3-4 hours
**Difficulty:** ⭐⭐ Intermediate

### Setup

```bash
# Extract
mkdir epub_workspace
unzip pride-and-prejudice.epub -d epub_workspace/original/
cp -r epub_workspace/original/* epub_workspace/translated/

# Analyze structure
find epub_workspace/translated -name "*.xhtml" | sort
```

**Output:**
```
epub_workspace/translated/OEBPS/Text/
├── cover.xhtml (skip - just image)
├── title.xhtml (translate title page? optional)
├── chapter-1.xhtml
├── chapter-2.xhtml
├── ... (59 more chapters)
├── chapter-61.xhtml
└── about.xhtml (translate author bio)
```

### Identify Proper Names

Read first chapter, create list:

```
Characters (DO NOT translate):
- Elizabeth Bennet
- Mr. Darcy
- Jane Bennet
- Mr. Bingley
- Mrs. Bennet
- Mary, Kitty, Lydia (sisters)

Places (TRANSLATE if applicable):
- Longbourn → keep (estate name, proper noun)
- Netherfield → keep (estate name)
- London → Londres (in French/Spanish), Londýn (Czech)

Titles (TRANSLATE):
- Mr. → Monsieur (French), Señor (Spanish), Pan (Czech)
- Mrs. → Madame, Señora, Paní
- Miss → Mademoiselle, Señorita, Slečna
```

### Translation Workflow

**Option 1: Sequential** (slower but simpler)

```bash
# Translate one chapter at a time
for i in {1..61}; do
    echo "Translating chapter $i..."
    # Paste prompt to AI with chapter-$i.xhtml
    sleep 30  # Wait for AI to complete
done
```

**Option 2: Batch** (faster, recommended)

```bash
# Group chapters: 1-10, 11-20, 21-30, etc.
# Use 5 parallel AI sessions
# Session 1: chapters 1-12
# Session 2: chapters 13-24
# Session 3: chapters 25-36
# Session 4: chapters 37-48
# Session 5: chapters 49-61
```

**Prompt template for each chapter:**

```
Translate this chapter of Pride and Prejudice from English to French.

File: epub_workspace/translated/OEBPS/Text/chapter-15.xhtml

Critical rules:
1. Preserve ALL HTML tags and attributes
2. Change xml:lang="en-GB" to xml:lang="fr-FR"
3. DO NOT translate these character names:
   Elizabeth Bennet, Mr. Darcy, Jane Bennet, Mr. Bingley, Mrs. Bennet
4. DO translate titles:
   - Mr. → Monsieur
   - Mrs. → Madame
   - Miss → Mademoiselle
5. Translate "Chapter 15" as "Chapitre 15"

Write translated file back to same location.
```

### Update Metadata

**File: content.opf**

```xml
<!-- Change language -->
<dc:language>en-GB</dc:language>
→
<dc:language>fr-FR</dc:language>

<!-- Optionally translate title -->
<dc:title>Pride and Prejudice</dc:title>
→
<dc:title>Orgueil et Préjugés</dc:title>
```

**File: toc.ncx**

```xml
<!-- Before -->
<navLabel><text>Chapter 1</text></navLabel>

<!-- After -->
<navLabel><text>Chapitre 1</text></navLabel>
```

### Quality Check

Sample 5 random chapters:

```bash
# Chapter 10
grep -A2 "Elizabeth" epub_workspace/translated/OEBPS/Text/chapter-10.xhtml
# Verify: Name "Elizabeth" NOT translated, but dialogue around it IS translated

# Chapter 25
grep -A2 "Mr. Darcy" epub_workspace/translated/OEBPS/Text/chapter-25.xhtml
# Verify: "Mr. Darcy" → "Monsieur Darcy"

# Chapter 40
grep "xml:lang" epub_workspace/translated/OEBPS/Text/chapter-40.xhtml
# Verify: xml:lang="fr-FR"
```

### Rebuild

```bash
cd epub_workspace/translated/
zip -0 -X ../../pride-prejudice-french.epub mimetype
zip -r ../../pride-prejudice-french.epub META-INF OEBPS
cd ../..
```

### Verification

```bash
# Test integrity
unzip -t pride-prejudice-french.epub

# EPUBCheck (if available)
java -jar epubcheck.jar pride-prejudice-french.epub

# Open in reader
open pride-prejudice-french.epub
```

**Check in reader:**
- Cover displays ✓
- TOC shows "Chapitre 1, Chapitre 2..." ✓
- Click chapter link navigates correctly ✓
- Text is in French ✓
- Character names preserved ✓
- "Monsieur Darcy" not "Mr. Darcy" ✓

**Total time:** ~3 hours (with parallel processing)
**Files translated:** 63 (61 chapters + title + about)
**Complexity:** Moderate (historical novel, formal language, many characters)

---

## Advanced Example: Technical Book

**Book:** Python Crash Course (hypothetical)
**Length:** ~500 pages
**Chapters:** 20 + appendices
**Time:** 6-8 hours
**Difficulty:** ⭐⭐⭐ Advanced

### Challenges

1. **Code snippets** must NOT be translated
2. **Technical terms** need consistency (e.g., "variable" → always same translation)
3. **Output examples** should stay in English (they're code output)
4. **File paths** must remain in English (`/usr/bin/python` not `/användare/bin/pytonas`)

### Setup

```bash
mkdir epub_workspace
unzip python-crash-course.epub -d epub_workspace/original/
cp -r epub_workspace/original/* epub_workspace/translated/

# Analyze
find epub_workspace/translated -name "*.xhtml" | wc -l
# Output: 45 files
```

### Create Technical Glossary

**File: glossary.txt**

```
English → Czech (target language)
========================
variable → proměnná
function → funkce
list → seznam
dictionary → slovník
loop → smyčka
if statement → podmínka if
class → třída
object → objekt
method → metoda
import → import (keep as-is, it's a keyword)
```

### Special Translation Rules

**Prompt addition:**

```
CRITICAL RULES FOR TECHNICAL BOOK:

1. DO NOT translate code blocks:
   <pre class="code">...</pre>
   <code>...</code>
   Keep these EXACTLY as-is!

2. DO NOT translate:
   - Python keywords: if, for, while, def, class, import, etc.
   - Variable names in examples: user_name, first_name, age
   - File paths: /usr/bin/python, C:\Python39\
   - Command prompts: $ python script.py
   - Output text: "Hello, World!"

3. Use this glossary for technical terms:
   - variable → proměnná
   - function → funkce
   - list → seznam
   [... full glossary ...]

4. Translate:
   - Explanatory paragraphs
   - Chapter titles
   - Exercise instructions
   - Captions and notes

Example:
ORIGINAL:
"A variable is a container for storing data. In Python, you create
a variable like this:
<code>user_name = 'Alice'</code>"

TRANSLATED:
"Proměnná je kontejner pro ukládání dat. V Pythonu vytvoříte
proměnnou takto:
<code>user_name = 'Alice'</code>"

Note: "variable" translated to "proměnná", but code stayed as-is!
```

### Sample Chapter Translation

**File: chapter-3-lists.xhtml**

**Before:**
```xml
<h1>Chapter 3: Introducing Lists</h1>

<p>A list is a collection of items in a particular order. You can
make a list that includes letters, numbers, or any type of object.</p>

<p>Here's a simple example:</p>

<pre class="code">
bicycles = ['trek', 'cannondale', 'redline', 'specialized']
print(bicycles)
</pre>

<p>The output is:</p>

<pre class="output">
['trek', 'cannondale', 'redline', 'specialized']
</pre>
```

**After (Czech):**
```xml
<h1>Kapitola 3: Úvod do seznamů</h1>

<p>Seznam je kolekce položek v určitém pořadí. Můžete vytvořit
seznam, který obsahuje písmena, čísla nebo jakýkoliv typ objektu.</p>

<p>Zde je jednoduchý příklad:</p>

<pre class="code">
bicycles = ['trek', 'cannondale', 'redline', 'specialized']
print(bicycles)
</pre>

<p>Výstup je:</p>

<pre class="output">
['trek', 'cannondale', 'redline', 'specialized']
</pre>
```

**Note:**
- "Chapter 3" → "Kapitola 3" ✓
- "list" → "seznam" ✓
- Code block unchanged ✓
- Output unchanged ✓
- "The output is:" → "Výstup je:" ✓

### Verification Script

```bash
#!/bin/bash
# verify-tech-book.sh

echo "Checking for accidentally translated code..."

# Check if Python keywords were translated
grep -r "pokud\|pro\|zatímco" epub_workspace/translated/OEBPS/*.xhtml | grep "<code>"
# Should return NOTHING (if found, keywords were wrongly translated inside code!)

# Check if file paths were translated
grep -r "uživatel/bin" epub_workspace/translated/OEBPS/*.xhtml
# Should return NOTHING

# Verify glossary terms used consistently
echo "Checking 'variable' translations..."
grep -o "proměnná\|variabla\|proměnlivá" epub_workspace/translated/OEBPS/*.xhtml | sort | uniq -c
# Should show only "proměnná", not other variants

echo "Done!"
```

### Common Mistakes to Avoid

❌ **WRONG:**
```xml
<code>seznam = [1, 2, 3]</code>
<!-- "list" translated to "seznam" inside code! -->
```

✓ **CORRECT:**
```xml
<code>list = [1, 2, 3]</code>
<!-- Code keywords stay in English -->
```

❌ **WRONG:**
```
$ pytonas skript.py
<!-- Command translated! -->
```

✓ **CORRECT:**
```
$ python script.py
<!-- Commands stay in English -->
```

**Total time:** ~8 hours
**Files translated:** 45
**Complexity:** High (technical accuracy critical, code preservation required)

---

## Batch Translation: Book Series

**Series:** The Hunger Games Trilogy
**Books:** 3 (The Hunger Games, Catching Fire, Mockingjay)
**Total chapters:** ~75
**Time:** 10-12 hours
**Difficulty:** ⭐⭐⭐ Advanced

### Why Batch?

- **Consistency:** Same character names, place names, terminology across all 3 books
- **Efficiency:** Reuse glossary and prompts
- **Quality:** Establish translation style once, apply everywhere

### Setup

```bash
# Extract all 3 books
mkdir -p epub_workspace/{book1,book2,book3}

unzip hunger-games-1.epub -d epub_workspace/book1/original/
unzip hunger-games-2.epub -d epub_workspace/book2/original/
unzip hunger-games-3.epub -d epub_workspace/book3/original/

# Create translated workspaces
for book in book1 book2 book3; do
    cp -r epub_workspace/$book/original/* epub_workspace/$book/translated/
done
```

### Create Series-Wide Glossary

**File: hunger-games-glossary.txt**

```
CHARACTER NAMES (DO NOT TRANSLATE):
- Katniss Everdeen
- Peeta Mellark
- Gale Hawthorne
- Primrose "Prim"
- Haymitch Abernathy
- President Snow
- Effie Trinket

PLACE NAMES (DO NOT TRANSLATE):
- Panem (fictional country)
- District 12, District 13
- The Capitol
- The Seam

INVENTED TERMS (DO NOT TRANSLATE):
- Mockingjay (symbol)
- Tracker jacker (fictional creature)
- Gamemaker
- Tribute
- Reaping

ITEMS (TRANSLATE):
- Bow and arrow → Arc et flèches (French)
- Bread → Pain
- Train → Train

TITLES:
- The Hunger Games → Les Jeux de la Faim (French)
- Catching Fire → L'Embrasement
- Mockingjay → La Révolte
```

### Translation Order

**Strategy:** Translate books sequentially (not in parallel) to maintain consistency

**Week 1:** The Hunger Games
- Days 1-2: Chapters 1-10
- Days 3-4: Chapters 11-20
- Day 5: Chapters 21-27 + metadata

**Week 2:** Catching Fire
- Days 1-2: Chapters 1-10
- Days 3-4: Chapters 11-20
- Day 5: Chapters 21-27 + metadata

**Week 3:** Mockingjay
- Days 1-2: Chapters 1-10
- Days 3-4: Chapters 11-20
- Day 5: Chapters 21-27 + metadata

### Quality Assurance

After Book 1, before starting Book 2:

```bash
# Extract terminology used in Book 1
grep -oh "Katniss\|Peeta\|Gale" epub_workspace/book1/translated/OEBPS/*.xhtml | sort | uniq
# Verify: Names NOT translated

# Check consistency of "The Hunger Games" translation
grep -i "hunger games\|jeux de la faim" epub_workspace/book1/translated/OEBPS/*.xhtml
# Verify: Always "Les Jeux de la Faim", never variants

# Ensure dialogue formatting preserved
grep -A1 "\"" epub_workspace/book1/translated/OEBPS/chapter-5.xhtml
# Verify: Quotes around dialogue maintained
```

### Cross-Book Validation

After completing all 3 books:

```bash
#!/bin/bash
# validate-series.sh

echo "Checking character name consistency across trilogy..."

# Extract all occurrences of main character
grep -rh "Katniss" epub_workspace/book*/translated/OEBPS/*.xhtml > katniss-occurrences.txt

# Should NOT find translated versions
grep -i "katnissova\|katnis" katniss-occurrences.txt
# Output should be empty (if not, some instances were wrongly translated)

echo "Checking 'Mockingjay' term consistency..."
grep -rh -i "mockingjay" epub_workspace/book*/translated/OEBPS/*.xhtml | sort | uniq
# Should show: "Mockingjay" (not translated variations)

echo "Validation complete!"
```

### Rebuild All

```bash
#!/bin/bash
# rebuild-trilogy.sh

for i in 1 2 3; do
    echo "Building book $i..."
    cd epub_workspace/book$i/translated/
    zip -0 -X ../../../hunger-games-$i-french.epub mimetype
    zip -r ../../../hunger-games-$i-french.epub META-INF OEBPS
    cd ../../..
    echo "Book $i complete!"
done

echo "Trilogy translation complete! 🎉"
```

**Total time:** ~12 hours
**Files translated:** ~225 (75 chapters × 3 books)
**Complexity:** Very high (consistency across multiple books critical)

---

## Special Cases

### Poetry Book

**Example:** The Raven by Edgar Allan Poe

**Challenges:**
- Rhyme scheme must be preserved (or adapted)
- Meter/rhythm important
- Line breaks critical

**Translation approach:**

```
This is POETRY. Special rules:

1. Preserve line breaks EXACTLY:
   <br/> tags must stay in same places

2. Rhyme scheme:
   Original: ABCBBB (lines 1-6)
   Try to maintain rhyme in target language
   If impossible, prioritize MEANING over rhyme

3. Formatting:
   - Preserve stanza breaks (empty <p> tags)
   - Keep italics for emphasis
   - Maintain indentation (CSS classes)

4. Consider this a LITERARY translation, not literal:
   "Once upon a midnight dreary" can become more poetic than literal
```

**Tip:** Poetry translation may require human post-editing for quality!

---

### Children's Book with Illustrations

**Example:** The Very Hungry Caterpillar

**Challenges:**
- Text integrated with images
- Simple vocabulary (don't over-complicate)
- Repetitive patterns must be consistent

**Translation rules:**

```
This is a CHILDREN'S BOOK:

1. Use SIMPLE vocabulary appropriate for ages 3-7
2. Keep sentences SHORT
3. Repetitive phrases must be IDENTICAL each time:
   "But he was still hungry" → always same translation
4. Food names:
   - Translate: apple → pomme (French)
   - Keep if cultural: "ice cream cone" → "cornet de glace" (not "cône de crème glacée")
5. Numbers:
   - Translate: "One apple" → "Une pomme"
   - Keep numeric: "1" stays as "1"
```

---

### Graphic Novel / Comic

**Example:** Watchmen

**Challenges:**
- Speech bubbles (text length constraints!)
- Sound effects (translate or keep?)
- Cultural references

**Special instructions:**

```
GRAPHIC NOVEL translation:

1. TEXT LENGTH matters:
   - Original: "What?" (4 chars)
   - Translation must fit bubble: "Quoi?" not "Qu'est-ce que tu dis?"

2. Sound effects:
   - Keep English: "BOOM", "POW", "CRASH"
   - Or adapt: "BOOM" → "BOUM" (French)
   - Be consistent!

3. Cultural references:
   - Explain in footnote if necessary
   - Or adapt to target culture (risky!)

4. Image text:
   - Note any text in images
   - Flag for graphic designer to re-create
```

---

## Summary

Different book types require different approaches:

| Type | Difficulty | Key Challenge | Time (avg novel) |
|------|-----------|---------------|------------------|
| Short story | ⭐ | None | 5-10 min |
| Standard novel | ⭐⭐ | Proper names | 3-5 hours |
| Technical book | ⭐⭐⭐ | Code preservation | 6-10 hours |
| Poetry | ⭐⭐⭐⭐ | Rhyme/meter | Varies greatly |
| Series | ⭐⭐⭐ | Consistency | 10-15 hours/trilogy |
| Children's book | ⭐⭐ | Simplicity | 1-2 hours |
| Graphic novel | ⭐⭐⭐⭐ | Text length limits | Varies |

**General advice:**

1. Always start with a **test chapter**
2. Create a **glossary** before translating
3. Use **parallel processing** when possible
4. **Validate frequently** (don't wait until the end!)
5. Keep the **original workspace** as backup

---

For more detailed guidance, see:
- [How It Works](how-it-works.md) - EPUB technical details
- [Troubleshooting](troubleshooting.md) - Fix common problems
- [Baneblade Case Study](../examples/baneblade-case-study.md) - Full real-world example

---

*Happy translating!* 📚✨
