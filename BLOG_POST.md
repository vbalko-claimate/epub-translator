# How I Translated a 300-Page Book in 2 Hours Using AI Code Agents

## A universal workflow for translating EPUB books with Claude Code, Gemini CLI, Cursor, or any AI assistant

---

*Published on Medium • 12 min read*

---

I just translated a 300-page Warhammer 40,000 novel from English to Czech in under 2 hours. Not by hiring a translator, not by using Google Translate, but by leveraging AI code assistants in a way most people haven't considered.

Here's the thing: **AI code assistants aren't just for programming anymore.**

Tools like Claude Code, Cursor, and Gemini CLI are designed to manipulate files, preserve structure, and follow complex instructions. These are exactly the skills needed for translating EPUB books while maintaining formatting, navigation, and metadata.

And the best part? **This workflow works with ANY AI code assistant** — not just the one I used.

Let me show you how.

---

## The Challenge

I'm a fan of Warhammer 40,000 novels. The universe is rich, the stories are epic, and the books are... mostly unavailable in Czech. *Baneblade* by Guy Haley looked amazing, but there was no official translation, and I wasn't about to wait years hoping one would appear.

Professional translation? **€9,500 (~$10,000)** for a 95,000-word book. That's €0.10 per word at standard rates.

Traditional tools? Google Translate would destroy the formatting. Copy-pasting into ChatGPT would lose the HTML structure. EPUB editors like Calibre require manual, tedious work.

There had to be a better way.

---

## The Realization: EPUB is Just HTML in a ZIP File

Here's what most people don't know about EPUB files:

**An EPUB is literally a ZIP archive containing:**
- XHTML files (your chapters)
- CSS stylesheets (formatting)
- Images (cover, illustrations)
- XML metadata (table of contents, language codes)

That's it. No magic, no proprietary format. Just web files in a folder.

This means:
1. **Extract** the ZIP → Get HTML files
2. **Translate** the HTML → Preserve tags, change text
3. **Rebuild** the ZIP → Valid EPUB

AI code assistants excel at exactly this workflow.

---

## How EPUB Books Work (3-Minute Crash Course)

Before we translate, you need to understand the anatomy of an EPUB:

```
book.epub (ZIP archive)
│
├── mimetype                  ← "I'm an EPUB" identifier
├── META-INF/
│   └── container.xml        ← Points to metadata
│
└── OEBPS/                   ← Main content folder
    ├── content.opf          ← Book metadata (title, language)
    ├── toc.ncx             ← Table of contents
    │
    ├── Text/                ← Your chapters (XHTML)
    │   ├── chapter-1.xhtml
    │   ├── chapter-2.xhtml
    │   └── ...
    │
    ├── Styles/
    │   └── style.css        ← Formatting
    │
    └── Images/
        └── cover.jpg
```

**Key insight:** The `Text/` folder contains XHTML files—basically HTML with stricter rules. These are what we translate.

**Critical rule:** We translate the *text* inside tags, but preserve *all* the tags themselves.

Example:

```xml
<!-- Original English -->
<p class="body-text">The battle raged across the frozen wastes.</p>

<!-- Translated to Czech -->
<p class="body-text">Bitva zuřila napříč zmrzlými pustinami.</p>
```

Note: The `<p class="body-text">` tag stayed identical. Only the text changed.

---

## The Translation Workflow (Step by Step)

I developed a **6-step process** that works with any AI code assistant:

### Step 1: Extract the EPUB (5 minutes)

```bash
mkdir -p epub_workspace/{original,translated,temp}
unzip book.epub -d epub_workspace/original/
cp -r epub_workspace/original/* epub_workspace/translated/
```

This creates:
- `original/` — Untouched backup
- `translated/` — Working copy
- `temp/` — Scratch space

### Step 2: Identify Content (10 minutes)

Not all files need translation:

**Translate:**
- ✅ Chapter files (`chapter-1.xhtml`, `chapter-2.xhtml`, etc.)
- ✅ Table of Contents
- ✅ "About the Author"

**Skip:**
- ❌ Copyright notices
- ❌ Publisher promotional pages
- ❌ Cover image (it's just a JPEG)

For *Baneblade*, I found:
- **34 files to translate** (31 chapters + 3 metadata files)
- **17 files to skip** (legal, promotional)

### Step 3: Translate Chapters (The Core Work)

Here's where AI code assistants shine.

**The prompt template I used:**

```
Translate this EPUB chapter from English to Czech.

File: epub_workspace/translated/OEBPS/Text/chapter-5.xhtml

Critical Rules:

1. Preserve ALL HTML tags and attributes
2. Change xml:lang="en-GB" to xml:lang="cs-CZ"
3. DO NOT translate these proper names:
   - Cortein, Bannick (character names)
   - Baneblade, Mars Triumphant (equipment names)
   - Kalidar IV (planet name)
   - Emperor, Omnissiah (titles in this universe)
   - Lascannon, vox, augur (technical terms)

4. DO translate:
   - "Chapter 5" → "Kapitola 5"
   - All narrative text, dialogue, descriptions

Write the translated file back to the same location.
```

**Why this works:**

AI code assistants are trained on millions of HTML files. They understand:
- What tags do (structure)
- What text does (content)
- How to preserve the former while translating the latter

**Time savings through parallelization:**

Here's the secret: Translate **5-10 chapters simultaneously** using multiple AI sessions.

I opened 5 sessions:
- Session 1: Chapters 1-6
- Session 2: Chapters 7-13
- Session 3: Chapters 14-20
- Session 4: Chapters 21-27
- Session 5: Chapters 28-31

What would have taken 3+ hours sequentially took **~45 minutes in parallel**.

### Step 4: Update Metadata (15 minutes)

Two files need language code updates:

**File 1: `content.opf` (Book Metadata)**

```xml
<!-- Before -->
<dc:language>en-GB</dc:language>

<!-- After -->
<dc:language>cs-CZ</dc:language>
```

**File 2: `toc.ncx` (Navigation Labels)**

```xml
<!-- Before -->
<navLabel><text>Chapter 1</text></navLabel>

<!-- After -->
<navLabel><text>Kapitola 1</text></navLabel>
```

These changes tell EPUB readers the book is now in Czech, enabling proper spell-check and font selection.

### Step 5: Rebuild the EPUB (5 minutes)

**Critical detail:** EPUB archives have **strict requirements**:

1. `mimetype` file MUST be first in the ZIP
2. `mimetype` file MUST be uncompressed (no compression!)

Here's the rebuild script:

```bash
cd epub_workspace/translated/

# Step 1: Add mimetype FIRST, UNCOMPRESSED
zip -0 -X ../../translated-book.epub mimetype

# Step 2: Add everything else (compressed)
zip -r ../../translated-book.epub META-INF OEBPS

cd ../..
```

**What those flags mean:**
- `-0` = No compression (store only)
- `-X` = Exclude system file attributes
- `-r` = Recursive (include folders)

Get this wrong, and many EPUB readers will reject your file.

### Step 6: Validate (5 minutes)

```bash
# Test ZIP integrity
unzip -t translated-book.epub

# Verify mimetype is first
unzip -l translated-book.epub | head -5

# Open in a reader
open translated-book.epub  # macOS
```

Check in the reader:
- ✅ Cover displays
- ✅ Table of Contents works (click chapters)
- ✅ Text is translated
- ✅ Formatting preserved (bold, italic)
- ✅ Images show up

---

## Real Results: The Baneblade Translation

**Book Stats:**
- **Pages:** ~300
- **Chapters:** 31
- **Words:** ~95,000
- **Files translated:** 34

**Time Breakdown:**

| Task | Time |
|------|------|
| Planning & setup | 30 min |
| Test translation (1 chapter) | 15 min |
| Batch translation (31 chapters) | 2 hours |
| Metadata updates | 30 min |
| Rebuild & validate | 20 min |
| **Total** | **~3.5 hours** |

**Quality Metrics:**
- Proper names preserved: **100%** (all 47 terms)
- HTML structure intact: **100%**
- Formatting preserved: **100%**
- Grammar errors: ~2-3 minor (fixed in 20 min post-editing)

**Cost:**
- AI API credits: **~$6**
- Professional translation: **~$10,000**
- Savings: **$9,994** 💰

---

## Tool Comparison: Which AI Assistant to Use?

The beauty of this workflow: **it works with ANY AI code assistant**.

### Option 1: Claude Code Skill (Fully Automated)

If you use Claude Code CLI, I created a **native skill** that automates the entire process:

```bash
# Install skill
cp -r epub-translator ~/.claude/skills/

# Translate a book (one command!)
claude "translate this EPUB from English to Czech: book.epub"
```

**Pros:**
- Fully automated (extraction → translation → rebuild)
- Parallel processing built-in
- Progress tracking

**Cons:**
- Claude Code CLI only
- Requires skill installation

**Best for:** Power users, frequent translations

### Option 2: Universal Prompt Templates (Works Everywhere)

For users of Claude.ai (web), Cursor, Gemini CLI, or any AI assistant:

I created **6 prompt templates** that you copy-paste step-by-step:

1. `01-setup-workspace.md` — Extract EPUB
2. `02-identify-chapters.md` — Find content
3. `03-translate-chapter.md` — Translate chapters
4. `04-translate-metadata.md` — Translate TOC, etc.
5. `05-update-config.md` — Language codes
6. `06-rebuild-epub.md` — Compile EPUB

**Pros:**
- Works with ANY AI assistant
- Maximum flexibility
- No installation required

**Cons:**
- More manual steps
- You manage parallelization yourself

**Best for:** One-time translations, flexibility, non-CLI users

---

## Special Cases: What About...?

### Proper Names (Harry Potter, Game of Thrones, etc.)

**Challenge:** AI might translate character names:
- "Harry Potter" → "Harry Hrnčíř" (Czech for Potter) ❌

**Solution:** Create an explicit list BEFORE translating:

```
DO NOT TRANSLATE these character names:
- Harry Potter (character, not occupation)
- Hermione Granger (character)
- Hogwarts (place name, invented)
- Quidditch (invented sport)
```

### Technical Books (Programming, Science)

**Challenge:** Code snippets must stay EXACTLY as-is.

**Solution:** Add to prompt:

```
CRITICAL: Do NOT translate content inside:
- <pre class="code">...</pre> (code blocks)
- <code>...</code> (inline code)
- Command examples: $ python script.py

Keep ALL code in original English.
```

### Poetry (Rhyme & Meter)

**Challenge:** Rhyme schemes don't translate directly.

**Recommendation:** Use AI for a **first draft**, then:
- Human poet refines for rhythm
- Prioritize meaning over perfect rhyme
- Maintain line breaks (preserve `<br/>` tags)

---

## Limitations & Ethics

**What this workflow CAN'T do:**
- Translate text embedded in images (book covers, diagrams)
- Handle DRM-protected EPUBs (you can't extract them)
- Match professional literary translation nuance (yet)

**Ethical considerations:**

✅ **Personal use:** Translate books you own, for yourself
✅ **Sharing with friends:** Usually OK (check local copyright laws)
✅ **Public domain books:** Free to translate and share
❌ **Commercial sale:** Requires copyright holder permission
❌ **Piracy:** Don't translate pirated books

**My take:** I translated *Baneblade* because:
1. I own the original EPUB
2. No official Czech translation exists
3. It's for personal reading, not sale
4. It introduces me to a universe I can then support by buying more books

---

## Getting Started (What You Need)

**Requirements:**
- An EPUB file (DRM-free)
- Access to an AI code assistant:
  - Claude Code (CLI)
  - Claude.ai (web)
  - Cursor (IDE)
  - Gemini CLI
  - Any code-capable AI
- `zip`/`unzip` utilities (pre-installed on macOS/Linux)

**Time investment:**
- Small book (100 pages): ~1 hour
- Medium novel (300 pages): ~3 hours
- Large book (500+ pages): ~6 hours

**Cost:**
- Free tier: Use Claude.ai web (free messages per day)
- API: ~$5-10 per 300-page book

---

## Try It Yourself

I've open-sourced the entire workflow:

**GitHub Repository:** [epub-translator](https://github.com/your-username/epub-translator)

**What's included:**
- ✅ Claude Code skill (for CLI users)
- ✅ 6 universal prompt templates (for everyone)
- ✅ Bash automation scripts
- ✅ Complete documentation
- ✅ Real-world examples
- ✅ Troubleshooting guide

**Quick start paths:**

**Path 1 (Claude Code users):**
```bash
# Clone repo
git clone https://github.com/your-username/epub-translator.git

# Install skill
cp -r epub-translator/claude-skill ~/.claude/skills/epub-translator

# Translate!
claude "translate book.epub from English to Spanish"
```

**Path 2 (Everyone else):**
1. Clone the repo
2. Navigate to `prompts/` directory
3. Copy-paste prompts to your AI assistant
4. Follow step-by-step instructions

**Start small:** Try a short story or novella first (~50 pages). Get comfortable with the workflow before tackling War and Peace.

---

## What This Means for the Future

This project taught me something profound:

**AI code assistants are general-purpose file manipulation tools.** They happen to be marketed for programming, but their capabilities extend far beyond code.

What else could we automate?
- Subtitle file translation (`.srt` files)
- Batch image caption translation
- Document format conversion (while preserving styling)
- Data extraction from structured files

The pattern is the same:
1. Understand the file structure
2. Identify what to change vs. preserve
3. Write clear instructions
4. Let AI handle the tedious parts

We're just scratching the surface.

---

## Conclusion: Translation Democratized

For decades, book translation has been the domain of professionals. It's expensive, time-consuming, and often unavailable for niche content.

AI code assistants don't replace professional translators—they **democratize access** for individuals.

Now, anyone can:
- Read books unavailable in their language
- Share stories across language barriers
- Learn from technical books not yet translated
- Preserve literary works in new languages

I translated *Baneblade* in 3.5 hours for $6. It would have cost $10,000 and taken months professionally.

For fans, hobbyists, and curious readers, that's game-changing.

---

## What's Next?

I'm planning to translate the entire Warhammer 40k Armageddon series (Baneblade, Shadowsword, Stormlord). The workflow is proven, the tools are ready, and the results speak for themselves.

If you try this, I'd love to hear about it:
- What book did you translate?
- Which AI assistant did you use?
- How long did it take?
- Any challenges you faced?

**Find me:**
- GitHub: [epub-translator repo](https://github.com/your-username/epub-translator)
- Open an issue or discussion!

---

**Resources:**

📦 **GitHub Repository:** [epub-translator](https://github.com/your-username/epub-translator)
📖 **Documentation:** [How It Works](https://github.com/your-username/epub-translator/blob/main/docs/how-it-works.md)
🛠️ **Troubleshooting:** [Common Issues](https://github.com/your-username/epub-translator/blob/main/docs/troubleshooting.md)
📚 **Case Study:** [Baneblade Translation](https://github.com/your-username/epub-translator/blob/main/examples/baneblade-case-study.md)

---

*Happy translating!* 📚✨

---

**About the Author**

[Your bio here - 2-3 sentences about you, your background with AI/coding, and why you built this]

---

**Tags:** #AI #Translation #EPUB #ClaudeCode #Automation #Books #NaturalLanguageProcessing #Tutorial

---

**Word count:** ~2,450 words

**Reading time:** ~12 minutes

---

## Call to Action

If you found this useful:

1. ⭐ **Star the GitHub repo** to bookmark it
2. 🔄 **Share this post** with friends who read eBooks
3. 💬 **Comment below** with your translation experience
4. 🤝 **Contribute** improvements to the workflow

Together, we can make all books accessible in all languages. 🌍

---

*Disclaimer: This workflow is for personal, educational use. Respect copyright laws in your jurisdiction. Don't pirate books or sell translated works without permission.*
